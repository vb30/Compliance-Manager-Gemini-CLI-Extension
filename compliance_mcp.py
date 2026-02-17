# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
from typing import Any, Dict, List, Optional
import time
import sys

from google.api_core import exceptions as google_exceptions
from google.cloud import auditmanager_v1
from google.api_core.client_options import ClientOptions
from google.api_core import operation
from google.longrunning import operations_pb2
from google.cloud.cloudsecuritycompliance_v1.services.config import ConfigClient
from google.cloud.cloudsecuritycompliance_v1.services.deployment import DeploymentClient
from google.cloud.cloudsecuritycompliance_v1.types import (
    CloudControl,
    CreateCloudControlRequest,
    CreateFrameworkDeploymentRequest,
    CreateFrameworkRequest,
    DeleteFrameworkDeploymentRequest,
    Framework,
    FrameworkReference,
    FrameworkDeployment,
    GetCloudControlDeploymentRequest,
    GetCloudControlRequest,
    GetFrameworkDeploymentRequest,
    GetFrameworkRequest,
    ListCloudControlDeploymentsRequest,
    ListCloudControlsRequest,
    ListFrameworkDeploymentsRequest,
    ListFrameworksRequest,
    TargetResourceConfig,
    EnforcementMode,
    CloudControlDetails,
    CloudControlMetadata,
    Rule,
    CELExpression,
    StringList,
    Severity,
    RuleActionType,
)
from google.protobuf import json_format
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("compliance-mcp")

# Configure logging
# IMPORTANT: MCP requires stdout to be clean JSON only
# All logging must go to stderr to avoid breaking JSON-RPC protocol

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stderr,  # Send all logs to stderr, not stdout
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("compliance-mcp")
logger.setLevel(logging.INFO)

# --- Client Initialization ---
# The clients automatically use Application Default Credentials (ADC).
# Ensure ADC are configured in the environment where the server runs
# (e.g., by running `gcloud auth application-default login`).
try:
    config_client = ConfigClient()
    logger.info("Successfully initialized Compliance Manager Config Client.")
except Exception as e:
    logger.error(f"Failed to initialize Config Client: {e}", exc_info=True)
    config_client = None

try:
    deployment_client = DeploymentClient()
    logger.info("Successfully initialized Compliance Manager Deployment Client.")
except Exception as e:
    logger.error(f"Failed to initialize Deployment Client: {e}", exc_info=True)
    deployment_client = None

try:
    audit_manager_client = auditmanager_v1.AuditManagerClient(transport="rest")
    logger.info("Successfully initialized Audit Manager Client.")
except Exception as e:
    logger.error(f"Failed to initialize Audit Manager Client: {e}", exc_info=True)
    audit_manager_client = None


# --- Helper Function for Proto to Dict Conversion ---
def proto_message_to_dict(message: Any) -> Dict[str, Any]:
    """Converts a protobuf message to a dictionary."""
    try:
        return json_format.MessageToDict(message._pb)
    except Exception as e:
        logger.error(f"Error converting protobuf message to dict: {e}")
        return {"error": "Failed to serialize response part", "details": str(e)}

def fetch_lro_status(lro_name: str) -> Dict[str, Any]:
    """Fetches the status of a long-running operation using DeploymentClient.get_operation."""
    if not deployment_client:
        return {"result": "failed", "error": "Deployment Client not initialized."}

    logger.info(f"Fetching status for LRO: {lro_name}")
    request = operations_pb2.GetOperationRequest(name=lro_name)
    logger.info(f"Request for get operation {request}")

    for i in range(30):  # Poll for a maximum of 30 * 10 = 300 seconds
        try:
            # Use the DeploymentClient's get_operation method
            operation_result = deployment_client.get_operation(request=request)
            if operation_result.done:
                if operation_result.HasField("error"):
                    logger.error(f"LRO {lro_name} failed: {operation_result.error}")
                    return {"result": "failed",
                            "error": operation_result.error.message}
                else:
                    logger.info(f"LRO {lro_name} completed successfully.")
                    return {"result": "passed"}
            else:
                logger.debug(
                    f"LRO {lro_name} is still in progress... (Attempt {i + 1})"
                )
                time.sleep(10)
        except google_exceptions.GoogleAPICallError as e:
            logger.error(
                f"Error calling GetOperation for {lro_name}: {e}", exc_info=True
            )
            return {"result": "failed", "error": str(e)}
        except Exception as e:
            logger.error(
                f"Unexpected error fetching LRO status for {lro_name}: {e}",
                exc_info=True,
            )
            return {"result": "failed", "error": f"Unexpected error: {str(e)}"}

    logger.warning(f"LRO {lro_name} timed out after 300 seconds.")
    return {"result": "timeout"}


def create_cloud_control_metadata_list(
    cloud_controls: str, parent: str
) -> list[CloudControlMetadata]:
    cloud_control_metadata_list = []

    for control_entry in cloud_controls.split(","):
        control_entry = control_entry.strip()
        if not control_entry:
            continue

        # Split control ID and revision
        parts = control_entry.split("#")           
        
        enforcement_mode_str = "DETECTIVE"
        if len(parts) == 2:
            cloud_control_id, major_revision_str = parts
        elif len(parts) == 3:
            cloud_control_id, major_revision_str, enforcement_mode_str = parts
        else:
            print(
                f"Skipping malformed entry: {control_entry} - missing # or too many #"
            )
            continue

        if not major_revision_str.isdigit():
            print(
                f"Skipping non-integer revision: {major_revision_str} in {control_entry}"
            )
            continue

        major_revision_id = int(major_revision_str)
        print(f"ID: {cloud_control_id}, Major: {major_revision_id}")

        cloud_control_metadata = CloudControlMetadata(
            cloud_control_details=CloudControlDetails(
                name=f"{parent}/cloudControls/{cloud_control_id}",
                major_revision_id=major_revision_id,
            ),
            enforcement_mode=EnforcementMode[enforcement_mode_str],
        )
        cloud_control_metadata_list.append(cloud_control_metadata)
    return cloud_control_metadata_list

# --- Config Service Tools (Frameworks and Cloud Controls) ---

@mcp.tool()
async def list_frameworks(
    organization_id: str,
    page_token: str = "",
    page_size: int = 50,
) -> Dict[str, Any]:
    """Name: list_frameworks

    Description: Lists all compliance frameworks available in an organization. Frameworks can be built-in
                 (e.g., CIS, NIST, FedRAMP) or custom-defined.
    Parameters:
    organization_id (required): The Google Cloud organization ID (e.g., '123456789012').
    page_size (optional): Maximum number of frameworks to return. Defaults to 50.
    page_token (optional): Token to get the next page. Passed by default by gemini.
    """
    if not config_client:
        return {"error": "Config Client not initialized."}

    parent = f"organizations/{organization_id}/locations/global"
    logger.info(f"Listing frameworks for parent: {parent}")

    try:
        request = ListFrameworksRequest(
            parent=parent,
            page_size=page_size,
            page_token=page_token,
        )

        response_pager = config_client.list_frameworks(request=request)

        frameworks = []
        for framework in response_pager.frameworks:
            framework_dict = proto_message_to_dict(framework)
            frameworks.append(framework_dict)

        return {
            "frameworks": frameworks,
            "page_token": response_pager.next_page_token
        }

    except google_exceptions.NotFound as e:
        logger.error(f"Organization not found: {e}")
        return {
            "error": "Not Found",
            "details": f"Could not find organization '{organization_id}'. {str(e)}",
        }
    except google_exceptions.PermissionDenied as e:
        logger.error(f"Permission denied: {e}")
        return {"error": "Permission Denied", "details": str(e)}
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        return {"error": "An unexpected error occurred", "details": str(e)}


@mcp.tool()
async def get_framework(
    organization_id: str,
    framework_id: str,
    major_revision_id: int = 0,
) -> Dict[str, Any]:
    """Name: get_framework

    Description: Gets detailed information about a specific compliance framework, including its cloud controls
                 and regulatory control mappings.
    Parameters:
    organization_id (required): The Google Cloud organization ID.
    framework_id (required): The ID of the framework to retrieve.
    major_revision_id (optional): The framework version to retrieve. If not specified, the most recent one is retrieved.
    """
    if not config_client:
        return {"error": "Config Client not initialized."}

    name = f"organizations/{organization_id}/locations/global/frameworks/{framework_id}"
    logger.info(f"Getting framework: {name}")

    try:
        request = GetFrameworkRequest(name=name, major_revision_id=major_revision_id)
        framework = config_client.get_framework(request=request)

        return proto_message_to_dict(framework)

    except google_exceptions.NotFound as e:
        logger.error(f"Framework not found: {e}")
        return {
            "error": "Not Found",
            "details": f"Could not find framework '{framework_id}'. {str(e)}",
        }
    except google_exceptions.PermissionDenied as e:
        logger.error(f"Permission denied: {e}")
        return {"error": "Permission Denied", "details": str(e)}
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        return {"error": "An unexpected error occurred", "details": str(e)}


@mcp.tool()
async def list_cloud_controls(
    organization_id: str,
    page_token: str = "",
    page_size: int = 50,
) -> Dict[str, Any]:
    """Name: list_cloud_controls

    Description: Lists all cloud controls available in an organization. Cloud controls are technical items
                 that help meet compliance requirements.
    Parameters:
    organization_id (required): The Google Cloud organization ID.
    page_size (optional): Maximum number of cloud controls to return. Defaults to 50.
    page_token (optional): Token to get the next page. Passed by default by gemini.
    """
    if not config_client:
        return {"error": "Config Client not initialized."}

    parent = f"organizations/{organization_id}/locations/global"
    logger.info(f"Listing cloud controls for parent: {parent}")

    try:
        request = ListCloudControlsRequest(
            parent=parent,
            page_size=page_size,
            page_token=page_token,
        )

        response_pager = config_client.list_cloud_controls(request=request)

        cloud_controls = []
        for control in response_pager.cloud_controls:
            control_dict = proto_message_to_dict(control)
            cloud_controls.append(control_dict)

        return {
            "cloud_controls": cloud_controls,
            "page_token": response_pager.next_page_token
        }

    except google_exceptions.NotFound as e:
        logger.error(f"Organization not found: {e}")
        return {
            "error": "Not Found",
            "details": f"Could not find organization '{organization_id}'. {str(e)}",
        }
    except google_exceptions.PermissionDenied as e:
        logger.error(f"Permission denied: {e}")
        return {"error": "Permission Denied", "details": str(e)}
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        return {"error": "An unexpected error occurred", "details": str(e)}


@mcp.tool()
async def get_cloud_control(
    organization_id: str,
    cloud_control_id: str,
) -> Dict[str, Any]:
    """Name: get_cloud_control

    Description: Gets detailed information about a specific cloud control, including its rules, parameters,
                 and enforcement mode.
    Parameters:
    organization_id (required): The Google Cloud organization ID.
    cloud_control_id (required): The ID of the cloud control to retrieve.
    """
    if not config_client:
        return {"error": "Config Client not initialized."}

    name = f"organizations/{organization_id}/locations/global/cloudControls/{cloud_control_id}"
    logger.info(f"Getting cloud control: {name}")

    try:
        request = GetCloudControlRequest(name=name)
        cloud_control = config_client.get_cloud_control(request=request)

        return proto_message_to_dict(cloud_control)

    except google_exceptions.NotFound as e:
        logger.error(f"Cloud control not found: {e}")
        return {
            "error": "Not Found",
            "details": f"Could not find cloud control '{cloud_control_id}'. {str(e)}",
        }
    except google_exceptions.PermissionDenied as e:
        logger.error(f"Permission denied: {e}")
        return {"error": "Permission Denied", "details": str(e)}
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        return {"error": "An unexpected error occurred", "details": str(e)}


@mcp.tool()
async def create_cloud_control(
    organization_id: str,
    cloud_control_id: str,
    display_name: str,
    resource_types: str,
    cel_expression: str,
    rule_action_types: str,
    description: str = "",
    severity: str = "MEDIUM",
    remediation_instructions: str = "",
) -> Dict[str, Any]:
    """Name: create_cloud_control
    Description: Creates a custom cloud control with CEL-based detection logic. Custom cloud controls allow you to
                 define your own compliance requirements using Common Expression Language (CEL) to evaluate
                 Cloud Asset Inventory resources.
    Parameters:
    organization_id (required): The Google Cloud organization ID (e.g., "123456789012").
    cloud_control_id (required): Unique identifier for the cloud control (e.g., "require-secure-boot").
    display_name (required): Human-readable name for the cloud control.
    resource_types (required): Comma separated Cloud Asset Inventory resource types to evaluate 
                               (e.g., "compute.googleapis.com/Instance,storage.googleapis.com/Bucket",
                                "sqladmin.googleapis.com/Instance").
    cel_expression (required): CEL expression that evaluates to FALSE to trigger a finding.
                              The expression evaluates properties of the resource as defined in Cloud Asset Inventory.
                              CEL Expression Rules:
                              - Must return boolean false to trigger a finding
                              - All enums must be represented as strings
                              - Use has() to check if a field exists before accessing it
                              - Common operators: ==, !=, &&, ||, matches(), contains(), exists()
                              Example CEL Expressions:
                              - Check KMS key rotation period (7776000s = 90 days):
                                "has(resource.data.rotationPeriod) && resource.data.rotationPeriod <= duration('7776000s')"
                              - Check if Compute Engine instance has Secure Boot enabled:
                                "has(resource.data.shieldedInstanceConfig) && resource.data.shieldedInstanceConfig.enableSecureBoot"
                              - Check if Cloud Storage bucket is not public:
                                "!(resource.data.iamConfiguration.publicAccessPrevention == 'ENFORCED')"
                              - Check if Cloud SQL instance has public IP disabled:
                                "!(resource.data.settings.ipConfiguration.ipv4Enabled)"
                              - Match resource name pattern:
                                "resource.data.name.matches('^gcp-vm-(linux|windows)-v\\\\d+$')"
                              - Check if service is enabled (for serviceusage.googleapis.com/Service):
                                "resource.data.state == 'ENABLED' && !resource.data.name.matches('storage-api.googleapis.com')"
    rule_action_types (reqired): Comma separated list of the functionalities that are enabled by the rule, possible values are a combination of PREVENTIVE, DETECTIVE, AUDIT actions.
        (e.g. "PREVENTIVE,AUDIT" or "PREVENTIVE,DETECTIVE,AUDIT", "PREVENTIVE,DETECTIVE", etc) 
    description (optional): Description of what the cloud control checks for.
    severity (optional): Finding severity level. One of: "CRITICAL", "HIGH", "MEDIUM", "LOW". Defaults to "MEDIUM".
    remediation_instructions (optional): Instructions for remediating findings from this control.
    Returns: Dictionary with status and created cloud control details.
    Example:
        create_cloud_control(
            organization_id="123456789012",
            cloud_control_id="require-secure-boot",
            display_name="Require Secure Boot on VMs",
            description="Ensures all Compute Engine instances have Secure Boot enabled for enhanced security",
            resource_type="compute.googleapis.com/Instance",
            cel_expression="has(resource.data.shieldedInstanceConfig) && resource.data.shieldedInstanceConfig.enableSecureBoot",
            severity="HIGH",
            remediation_instructions="Enable Secure Boot in the Shielded VM settings: gcloud compute instances update INSTANCE_NAME --shielded-secure-boot"
        )
    Note: For a complete list of Cloud Asset Inventory resource types and their properties, see:
          https://cloud.google.com/asset-inventory/docs/supported-asset-types
    """
    if not config_client:
        return {"error": "Config Client not initialized."}

    parent = f"organizations/{organization_id}/locations/global"
    logger.info(f"Creating cloud control '{cloud_control_id}' in parent: {parent}")
    logger.info(f"Resource type: {resource_types}, CEL expression: {cel_expression}")

    try:
        # Note: The CloudControl message structure may need to be adjusted based on the actual API
        # The current implementation creates a basic cloud control
        # CEL expression and resource type configuration may need to be set through additional API calls
        resource_type_values = []
        for value in resource_types.split(","):
            resource_type_values.append(value.strip())

        rule_action_types_array = []
        for rule_action_type in rule_action_types.split(","):
            match rule_action_type:
                case "PREVENTIVE":
                    rule_action_types_array.append(RuleActionType.RULE_ACTION_TYPE_PREVENTIVE)
                case "DETECTIVE":
                    rule_action_types_array.append(RuleActionType.RULE_ACTION_TYPE_DETECTIVE)
                case "AUDIT":
                    rule_action_types_array.append(RuleActionType.RULE_ACTION_TYPE_AUDIT)
        
        rule = Rule(
            cel_expression = CELExpression(
                expression = cel_expression,
                resource_types_values = StringList(values=resource_type_values),
            ),
            rule_action_types = rule_action_types_array,
        )
        
        cloud_control = CloudControl(
            display_name = display_name,
            description = description,
            rules = [rule],
            severity = Severity[severity],
            remediation_steps = remediation_instructions,
        )

        request = CreateCloudControlRequest(
            parent=parent,
            cloud_control_id=cloud_control_id,
            cloud_control=cloud_control,
        )

        result = config_client.create_cloud_control(request=request)

        return {
            "status": "success",
            "cloud_control": proto_message_to_dict(result),
            "configuration": {
                "resource_type": resource_types,
                "cel_expression": cel_expression,
                "severity": severity,
                "remediation_instructions": remediation_instructions,
            },
            "note": "Cloud control created. You may need to configure the CEL expression and resource type through the Google Cloud Console or additional API calls.",
        }

    except google_exceptions.AlreadyExists as e:
        logger.error(f"Cloud control already exists: {e}")
        return {
            "error": "Already Exists",
            "details": f"Cloud control '{cloud_control_id}' already exists. {str(e)}",
        }
    except google_exceptions.PermissionDenied as e:
        logger.error(f"Permission denied: {e}")
        return {"error": "Permission Denied", "details": str(e)}
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        return {"error": "An unexpected error occurred", "details": str(e)}


@mcp.tool()
async def create_framework(
    organization_id: str,
    framework_id: str,
    display_name: str,
    cloud_control_ids: str,
    description: str = "",
) -> Dict[str, Any]:
    """Name: create_framework
    Description: Creates a custom compliance framework. Frameworks are collections of cloud controls that help
        meet specific compliance requirements.
    Parameters:
    organization_id (required): The Google Cloud organization ID.
    framework_id (required): The ID for the new framework (must be unique).
    display_name (required): A human-readable name for the framework.
    cloud_control_ids (required): This is a comma separated list of could_control ids.
    description (optional): A description of the framework's purpose.
    """
    if not config_client:
        return {"error": "Config Client not initialized."}

    parent = f"organizations/{organization_id}/locations/global"
    logger.info(f"Creating framework '{framework_id}' in parent: {parent}")

    try:
        # Build cloud control references
        cloud_control_detail_list = []
        for cloud_control_id in cloud_control_ids.split(","):
            if not cloud_control_id:
                print(f"skipping malformed cloud control id: {cloud_control_id}")
            cloud_control_detail = CloudControlDetails(
                name=f"{parent}/cloudControls/{cloud_control_id.strip()}",
            )
            cloud_control_detail_list.append(cloud_control_detail)

        framework = Framework(
            name = f"{parent}/frameworks/{framework_id}",
            display_name = display_name,
            description = description,
            cloud_control_details = cloud_control_detail_list,
        )

        request = CreateFrameworkRequest(
            parent=parent,
            framework_id=framework_id,
            framework=framework,
        )

        result = config_client.create_framework(request=request)

        return {
            "status": "success",
            "framework": proto_message_to_dict(result),
        }

    except google_exceptions.AlreadyExists as e:
        logger.error(f"Framework already exists: {e}")
        return {
            "error": "Already Exists",
            "details": f"Framework '{framework_id}' already exists. {str(e)}",
        }
    except google_exceptions.NotFound as e:
        logger.error(f"One or more cloud controls not found: {e}")
        return {
            "error": "Not Found",
            "details": f"One or more cloud controls not found. {str(e)}",
        }
    except google_exceptions.PermissionDenied as e:
        logger.error(f"Permission denied: {e}")
        return {"error": "Permission Denied", "details": str(e)}
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        return {"error": "An unexpected error occurred", "details": str(e)}


# --- Deployment Service Tools ---


@mcp.tool()
async def list_framework_deployments(
    organization_id: str,
    page_token: str = "",
    page_size: int = 50,
) -> Dict[str, Any]:
    """Name: list_framework_deployments

    Description: Lists all framework deployments for a given organization.
    Parameters:
    organization_id (required): The Google Cloud organization ID (e.g., '123456789012')
    page_token (optional): Token to get the next page. Passed by default by gemini.
    page_size (optional): Maximum number of deployments to return. Defaults to 50.
    """
    if not deployment_client:
        return {"error": "Deployment Client not initialized."}

    parent_with_location = f"organizations/{organization_id}/locations/global"
    logger.info(f"Listing framework deployments for parent: {parent_with_location}")

    try:
        request = ListFrameworkDeploymentsRequest(
            parent = parent_with_location,
            page_size = page_size,
            page_token = page_token,
        )

        response_pager = deployment_client.list_framework_deployments(request=request)

        deployments = []
        for deployment in response_pager.framework_deployments:
            deployment_dict = proto_message_to_dict(deployment)
            deployments.append(deployment_dict)

        return {
            "framework_deployments": deployments,
            "page_token": response_pager.next_page_token,
        }

    except google_exceptions.NotFound as e:
        logger.error(f"Parent resource not found: {e}")
        return {
            "error": "Not Found",
            "details": f"Could not find the org '{organization_id}'. {str(e)}",
        }
    except google_exceptions.PermissionDenied as e:
        logger.error(f"Permission denied: {e}")
        return {"error": "Permission Denied", "details": str(e)}
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        return {"error": "An unexpected error occurred", "details": str(e)}


@mcp.tool()
async def get_framework_deployment(
    organization_id: str,
    framework_deployment_id: str,
) -> Dict[str, Any]:
    """Name: get_framework_deployment

    Description: Gets detailed information about a specific framework deployment, including its state and configuration.
    Parameters:
    organization_id (required): The Google Cloud organization ID (e.g., '123456789012')
    framework_deployment_id (required): The ID of the framework deployment to retrieve.
    """
    if not deployment_client:
        return {"error": "Deployment Client not initialized."}

    name = (
        f"organizations/{organization_id}/locations/global/frameworkDeployments/{framework_deployment_id}"
    )
    logger.info(f"Getting framework deployment: {name}")

    try:
        request = GetFrameworkDeploymentRequest(name=name)
        deployment = deployment_client.get_framework_deployment(request=request)

        return proto_message_to_dict(deployment)

    except google_exceptions.NotFound as e:
        logger.error(f"Framework deployment not found: {e}")
        return {
            "error": "Not Found",
            "details": f"Could not find framework deployment '{framework_deployment_id}'. {str(e)}",
        }
    except google_exceptions.PermissionDenied as e:
        logger.error(f"Permission denied: {e}")
        return {"error": "Permission Denied", "details": str(e)}
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        return {"error": "An unexpected error occurred", "details": str(e)}


@mcp.tool()
async def create_framework_deployment(
    organization_id: str,
    framework_deployment_id: str,
    framework_name: str,
    cloud_controls: str,
    framework_version: int,
    target_resource: Optional[str] = None,
) -> Dict[str, Any]:
    """Name: create_framework_deployment

    Description: Creates a new framework deployment on a target resource. This applies a compliance framework
                 to an organization, folder, or project. This is a long-running operation.
    Parameters:
    organization_id (required): The Google Cloud organization ID (e.g., '123456789012')
    framework_deployment_id (required): The ID for the new framework deployment.
    framework_name (required): The full name of the framework to deploy (e.g., 'organizations/{org_id}/locations/global/frameworks/{framework_id}').
    cloud_controls (required): This is a comma seperated list of could_control ids along with their revision number seperated by a hash.
        Optionally you can also mention the enforcement mode separate by `#`, if not mentioned/incorrect DETECTIVE is used.
        So the entire string is of format: cloud_control_id1#revision1#AUDIT,cloud_control_id2#revision2.
        Possible enforcement modes are: PREVENTIVE, DETECTIVE & AUDIT
    framework_version (required): The major version of the framework.
    target_resource (optional): The target resource name. If not provided, uses the organization_id(parent resource).
    """
    if not deployment_client:
        return {"error": "Deployment Client not initialized."}

    parent_with_location = f"organizations/{organization_id}/locations/global"
    logger.info(
        f"Creating framework deployment '{framework_deployment_id}' in parent: {parent_with_location}, {cloud_controls}"
    )

    cloud_control_metadata_list = create_cloud_control_metadata_list(
        cloud_controls, parent_with_location
    )

    # Set target resource if provided
    if not target_resource:
        target_resource = f"organizations/{organization_id}"

    framework_reference = FrameworkReference(framework = framework_name, major_revision_id = framework_version)

    try:
        # Create the framework deployment object
        framework_deployment = FrameworkDeployment(
            framework=framework_reference,
            cloud_control_metadata=cloud_control_metadata_list,
            target_resource_config = TargetResourceConfig(
                existing_target_resource=target_resource
            ),
        )

        request = CreateFrameworkDeploymentRequest(
            parent=parent_with_location,
            framework_deployment_id=framework_deployment_id,
            framework_deployment=framework_deployment,
        )

        logger.info(f"Request for create framework deployment {request}")

        # This is a long-running operation
        operation_result = deployment_client.create_framework_deployment(
            request=request
        )

        # Wait for the operation to complete
        logger.info(
            f"Waiting for framework deployment creation to complete...: {operation_result.operation.name}"
        )
        return fetch_lro_status(operation_result.operation.name)

    except google_exceptions.NotFound as e:
        logger.error(f"Parent resource or framework not found: {e}")
        return {
            "error": "Not Found",
            "details": f"Could not find the organization '{organization_id}' or framework '{framework_name}'. {str(e)}",
        }
    except google_exceptions.PermissionDenied as e:
        logger.error(f"Permission denied: {e}")
        return {"error": "Permission Denied", "details": str(e)}
    except google_exceptions.AlreadyExists as e:
        logger.error(f"Framework deployment already exists: {e}")
        return {
            "error": "Already Exists",
            "details": f"Framework deployment '{framework_deployment_id}' already exists. {str(e)}",
        }
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        return {"error": "An unexpected error occurred", "details": str(e)}


@mcp.tool()
async def delete_framework_deployment(
    organization_id: str,
    framework_deployment_id: str,
) -> Dict[str, Any]:
    """Name: delete_framework_deployment

    Description: Deletes a framework deployment. This removes the compliance framework from the target resource. This is a long-running operation.
    Parameters:
    organization_id (required): The Google Cloud organization ID (e.g., '123456789012')
    framework_deployment_id (required): The ID of the framework deployment to delete.
    """
    if not deployment_client:
        return {"error": "Deployment Client not initialized."}

    name = f"organizations/{organization_id}/locations/global/frameworkDeployments/{framework_deployment_id}"
    logger.info(f"Deleting framework deployment: {name}")

    try:
        request = DeleteFrameworkDeploymentRequest(name=name)

        # This is a long-running operation
        operation_result = deployment_client.delete_framework_deployment(
            request=request
        )

        # Wait for the operation to complete
        logger.info(
            f"Waiting for framework deployment deletion to complete... LRO Name: {operation_result.operation.name}"
        )
        return fetch_lro_status(operation_result.operation.name)

    except google_exceptions.NotFound as e:
        logger.error(f"Framework deployment not found: {e}")
        return {
            "error": "Not Found",
            "details": f"Could not find framework deployment '{framework_deployment_id}'. {str(e)}",
        }
    except google_exceptions.PermissionDenied as e:
        logger.error(f"Permission denied: {e}")
        return {"error": "Permission Denied", "details": str(e)}
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        return {"error": "An unexpected error occurred", "details": str(e)}


@mcp.tool()
async def list_cloud_control_deployments(
    organization_id: str,
    page_token: str = "",
    page_size: int = 50,
) -> Dict[str, Any]:
    """Name: list_cloud_control_deployments

    Description: Lists all cloud control deployments for a given organization.
    Parameters:
    organization_id (required): The Google Cloud organization ID (e.g., '123456789012')
    page_token (optional): Token to get the next page. Passed by default by gemini.
    page_size (optional): Maximum number of deployments to return. Defaults to 50.
    """
    if not deployment_client:
        return {"error": "Deployment Client not initialized."}

    parent_with_location = f"organizations/{organization_id}/locations/global"
    logger.info(f"Listing cloud control deployments for parent: {parent_with_location}")

    try:
        request = ListCloudControlDeploymentsRequest(
            parent=parent_with_location,
            page_size=page_size,
            page_token=page_token
        )

        response_pager = deployment_client.list_cloud_control_deployments(
            request=request
        )

        deployments = []
        for deployment in response_pager.cloud_control_deployments:
            deployment_dict = proto_message_to_dict(deployment)
            deployments.append(deployment_dict)

        return {
            "cloud_control_deployments": deployments,
            "page_token": response_pager.next_page_token,
        }

    except google_exceptions.NotFound as e:
        logger.error(f"Parent resource not found: {e}")
        return {
            "error": "Not Found",
            "details": f"Could not find the organization '{organization_id}'. {str(e)}",
        }
    except google_exceptions.PermissionDenied as e:
        logger.error(f"Permission denied: {e}")
        return {"error": "Permission Denied", "details": str(e)}
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        return {"error": "An unexpected error occurred", "details": str(e)}


@mcp.tool()
async def get_cloud_control_deployment(
    organization_id: str,
    cloud_control_deployment_id: str,
) -> Dict[str, Any]:
    """Name: get_cloud_control_deployment

    Description: Gets detailed information about a specific cloud control deployment, including its enforcement
                 mode and state.
    Parameters:
    organization_id (required): The Google Cloud organization ID (e.g., '123456789012')
    cloud_control_deployment_id (required): The ID of the cloud control deployment to retrieve.
    """
    if not deployment_client:
        return {"error": "Deployment Client not initialized."}

    name = f"organizations/{organization_id}/locations/global/cloudControlDeployments/{cloud_control_deployment_id}"
    logger.info(f"Getting cloud control deployment: {name}")

    try:
        request = GetCloudControlDeploymentRequest(name=name)
        deployment = deployment_client.get_cloud_control_deployment(request=request)

        return proto_message_to_dict(deployment)

    except google_exceptions.NotFound as e:
        logger.error(f"Cloud control deployment not found: {e}")
        return {
            "error": "Not Found",
            "details": f"Could not find cloud control deployment '{cloud_control_deployment_id}'. {str(e)}",
        }
    except google_exceptions.PermissionDenied as e:
        logger.error(f"Permission denied: {e}")
        return {"error": "Permission Denied", "details": str(e)}
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        return {"error": "An unexpected error occurred", "details": str(e)}

# --- Audit Manager Tools ---

@mcp.tool()
def enroll_resource(
    scope: str,
    destinations: List[str],
    location: str = "global",
) -> Dict[str, Any]:
    """Name: enroll_resource

    Description: Enrolls a resource (organization, folder, or project) in Audit Manager.
    Parameters:
    scope (required): The resource to enroll. Format: 'organizations/<org_id>', 'folders/<folder_id>', 'projects/<project_id>'.
    destinations (required): A list of GCS bucket URIs for report delivery. Format: ["gs://<bucket_name>"]
    location (optional): The location of the resource. Defaults to "global".
    """
    if not audit_manager_client:
        return {"error": "Audit Manager Client not initialized"}

    scope = scope + "/locations/" + location
    logger.info(f"Enrolling resource: {scope} with destinations: {destinations}")

    try:
        destination_objs = []
        for dest in destinations:
            destination_objs.append(
                auditmanager_v1.EnrollResourceRequest.EligibleDestination(
                    eligible_gcs_bucket=dest
                )
            )

        request = auditmanager_v1.EnrollResourceRequest(
            scope=scope,
            destinations=destination_objs,
        )

        enrollment = audit_manager_client.enroll_resource(request=request)
        return proto_message_to_dict(enrollment)

    except google_exceptions.PermissionDenied as e:
        logger.error(f"Permission denied: {e}")
        return {"error": "Permission Denied", "details": str(e)}
    except Exception as e:
        logger.error(f"Error enrolling resource: {e}", exc_info=True)
        return {"error": "Internal Error", "details": str(e)}


@mcp.tool()
def generate_audit_scope_report(
    scope: str,
    compliance_standard: str,
    location: str = "global",
) -> Dict[str, Any]:
    """Name: generate_audit_scope_report

    Description: Generates an audit scope report for a given scope and standard.
    Parameters:
    scope (required): The resource scope. Format: 'folders/<folder_id>' or 'projects/<project_id>'.
    compliance_standard (required): The compliance standard (e.g., "FEDRAMP_MODERATE").
    location (optional): The location of the resource. Defaults to "global".
    """
    if not audit_manager_client:
        return {"error": "Audit Manager Client not initialized"}

    scope = scope + "/locations/" + location
    logger.info(f"Generating audit scope report for scope: {scope}, compliance_standard: {compliance_standard}")

    try:
        request = auditmanager_v1.GenerateAuditScopeReportRequest(
            scope=scope,
            compliance_standard=compliance_standard,
            report_format=auditmanager_v1.GenerateAuditScopeReportRequest.AuditScopeReportFormat.AUDIT_SCOPE_REPORT_FORMAT_ODF,
        )

        response = audit_manager_client.generate_audit_scope_report(request=request)
        return proto_message_to_dict(response)

    except google_exceptions.PermissionDenied as e:
        logger.error(f"Permission denied: {e}")
        return {"error": "Permission Denied", "details": str(e)}
    except Exception as e:
        logger.error(f"Error generating audit scope report: {e}", exc_info=True)
        return {"error": "Internal Error", "details": str(e)}


@mcp.tool()
def generate_audit_report(
    scope: str,
    gcs_uri: str,
    compliance_standard: str,
    location: str = "global",
) -> Dict[str, Any]:
    """Name: generate_audit_report

    Description: Generates an audit report. This is a long-running operation.
    Parameters:
    scope (required): The resource scope. It can be in one of the following formats: 'folders/<folder_id>' or 'projects/<project_id>'.
    gcs_uri (required): The destination GCS bucket URI. Format: "gs://<bucket_name>"
    compliance_standard (required): The compliance standard (e.g., "FEDRAMP_MODERATE").
    location (optional): The location of the resource. Defaults to "global".
    """
    if not audit_manager_client:
        return {"error": "Audit Manager Client not initialized"}

    scope = scope + "/locations/" + location
    logger.info(f"Generating audit report for scope: {scope} to {gcs_uri}")

    try:
        request = auditmanager_v1.GenerateAuditReportRequest(
            scope=scope,
            gcs_uri=gcs_uri,
            compliance_standard=compliance_standard,
            report_format=auditmanager_v1.GenerateAuditReportRequest.AuditReportFormat.AUDIT_REPORT_FORMAT_ODF,
        )

        operation = audit_manager_client.generate_audit_report(request=request)
        # Return the operation name so the user can check status if needed.
        return {
            "operation_name": operation.operation.name,
            "status": "IN_PROGRESS",
            "details": "Audit report generation started. Check status using client tools or console."
        }

    except google_exceptions.PermissionDenied as e:
        logger.error(f"Permission denied: {e}")
        return {"error": "Permission Denied", "details": str(e)}
    except Exception as e:
        logger.error(f"Error generating audit report: {e}", exc_info=True)
        return {"error": "Internal Error", "details": str(e)}


@mcp.tool()
def list_audit_reports(
    parent: str,
    page_size: int = 50,
    page_token: str = "",
    location: str = "global",
) -> Dict[str, Any]:
    """Name: list_audit_reports

    Description: Lists audit reports.
    Parameters:
    parent (required): The parent scope. Format: 'folders/<folder_id>' or 'projects/<project_id>'.
    page_size (optional): Maximum number of results to return. Defaults to 50.
    page_token (optional): Token to get the next page.
    location (optional): The location of the resource. Defaults to "global".
    """
    if not audit_manager_client:
        return {"error": "Audit Manager Client not initialized"}

    parent = parent + "/locations/" + location
    logger.info(f"Listing audit reports for parent: {parent}")

    try:
        request = auditmanager_v1.ListAuditReportsRequest(
            parent=parent,
            page_size=page_size,
            page_token=page_token,
        )

        page_result = audit_manager_client.list_audit_reports(request=request)
        
        # Convert the first page of results to a list of dicts
        reports = []
        for report in page_result:
            reports.append(proto_message_to_dict(report))

        return {
            "audit_reports": reports,
            "next_page_token": page_result.next_page_token,
        }

    except google_exceptions.PermissionDenied as e:
        logger.error(f"Permission denied: {e}")
        return {"error": "Permission Denied", "details": str(e)}
    except Exception as e:
        logger.error(f"Error listing audit reports: {e}", exc_info=True)
        return {"error": "Internal Error", "details": str(e)}


@mcp.tool()
def get_audit_report(
    parent: str,
    audit_report_id: str,
    location: str = "global",
) -> Dict[str, Any]:
    """Name: get_audit_report

    Description: Gets a specific audit report.
    Parameters:
    parent (required): The parent scope. Format: 'folders/<folder_id>' or 'projects/<project_id>'.
    audit_report_id (required): The ID of the audit report to retrieve.
    location (optional): The location of the resource. Defaults to "global".
    """
    if not audit_manager_client:
        return {"error": "Audit Manager Client not initialized"}

    name = parent + "/locations/" + location + "/auditReports/" + audit_report_id
    logger.info(f"Getting audit report: {name}")

    try:
        request = auditmanager_v1.GetAuditReportRequest(name=name)
        report = audit_manager_client.get_audit_report(request=request)
        return proto_message_to_dict(report)

    except google_exceptions.NotFound as e:
        logger.error(f"Audit report not found: {e}")
        return {"error": "Not Found", "details": str(e)}
    except google_exceptions.PermissionDenied as e:
        logger.error(f"Permission denied: {e}")
        return {"error": "Permission Denied", "details": str(e)}
    except Exception as e:
        logger.error(f"Error getting audit report: {e}", exc_info=True)
        return {"error": "Internal Error", "details": str(e)}


@mcp.tool()
def get_resource_enrollment_status(
    parent: str,
    location: str = "global",
) -> Dict[str, Any]:
    """Name: get_resource_enrollment_status

    Description: Gets the enrollment status of a resource.
    Parameters:
    parent (required): The parent scope. Format: 'organizations/<org_id>' or 'folders/<folder_id>' or 'projects/<project_id>'.
    location (optional): The location of the resource. Defaults to "global".
    """
    if not audit_manager_client:
        return {"error": "Audit Manager Client not initialized"}

    name = parent + "/locations/" + location + "/resourceEnrollmentStatuses/-"
    logger.info(f"Getting resource enrollment status: {name}")

    try:
        request = auditmanager_v1.GetResourceEnrollmentStatusRequest(name=name)
        status = audit_manager_client.get_resource_enrollment_status(request=request)
        return proto_message_to_dict(status)

    except google_exceptions.NotFound as e:
        logger.error(f"Enrollment status not found: {e}")
        return {"error": "Not Found", "details": str(e)}
    except google_exceptions.PermissionDenied as e:
        logger.error(f"Permission denied: {e}")
        return {"error": "Permission Denied", "details": str(e)}
    except Exception as e:
        logger.error(f"Error getting enrollment status: {e}", exc_info=True)
        return {"error": "Internal Error", "details": str(e)}


@mcp.tool()
def list_resource_enrollment_statuses(
    parent: str,
    page_size: int = 50,
    page_token: str = "",
    location: str = "global",
) -> Dict[str, Any]:
    """Name: list_resource_enrollment_statuses

    Description: Lists resource enrollment statuses for all resources under the given parent scope.
    Parameters:
    parent (required): The parent scope. Format: 'organizations/<org_id>', 'folders/<folder_id>'.
    page_size (optional): Page size. Defaults to 50.
    page_token (optional): Page token.
    location (optional): The location of the resource. Defaults to "global".
    """
    if not audit_manager_client:
        return {"error": "Audit Manager Client not initialized"}

    parent = parent + "/locations/" + location
    logger.info(f"Listing enrollment statuses for parent: {parent}")

    try:
        request = auditmanager_v1.ListResourceEnrollmentStatusesRequest(
            parent=parent,
            page_size=page_size,
            page_token=page_token,
        )

        page_result = audit_manager_client.list_resource_enrollment_statuses(request=request)
        
        statuses = []
        for status in page_result:
            statuses.append(proto_message_to_dict(status))

        return {
            "resource_enrollment_statuses": statuses,
            "next_page_token": page_result.next_page_token,
        }

    except google_exceptions.PermissionDenied as e:
        logger.error(f"Permission denied: {e}")
        return {"error": "Permission Denied", "details": str(e)}
    except Exception as e:
        logger.error(f"Error listing enrollment statuses: {e}", exc_info=True)
        return {"error": "Internal Error", "details": str(e)}

# --- Main execution ---


def main() -> None:
    """Runs the FastMCP server."""
    if not config_client:
        logger.critical(
            "Config Client failed to initialize. MCP server cannot serve config tools."
        )

    if not deployment_client:
        logger.critical(
            "Deployment Client failed to initialize. MCP server cannot serve deployment tools."
        )

    if not audit_manager_client:
        logger.critical(
            "Audit Manager Client failed to initialize. MCP server cannot serve audit manager tools."
        )

    logger.info("Starting Compliance Manager MCP server...")

    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()

