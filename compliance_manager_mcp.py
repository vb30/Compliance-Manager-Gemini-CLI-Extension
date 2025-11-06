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
from google.api_core import operation
from google.longrunning import operations_pb2
from google.cloud.cloudsecuritycompliance_v1.services.config import ConfigClient
from google.cloud.cloudsecuritycompliance_v1.services.deployment import DeploymentClient
from google.cloud.cloudsecuritycompliance_v1.types import (
    CloudControl,
    CreateCloudControlRequest,
    CreateFrameworkDeploymentRequest,
    CreateFrameworkRequest,
    DeleteCloudControlRequest,
    DeleteFrameworkDeploymentRequest,
    DeleteFrameworkRequest,
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
    UpdateCloudControlRequest,
    UpdateFrameworkRequest,
    EnforcementMode,
    CloudControlDetails,
    CloudControlMetadata,
)
from google.protobuf import json_format
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("compliance-manager-mcp")

# Configure logging
# IMPORTANT: MCP requires stdout to be clean JSON only
# All logging must go to stderr to avoid breaking JSON-RPC protocol

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stderr,  # Send all logs to stderr, not stdout
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("compliance-manager-mcp")
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
                    return {"result": "failed"}
                else:
                    logger.info(f"LRO {lro_name} completed successfully.")
                    return {"result": "passed"}
            else:
                logger.debug(f"LRO {lro_name} is still in progress... (Attempt {i + 1})")
                time.sleep(10)
        except google_exceptions.GoogleAPICallError as e:
            logger.error(f"Error calling GetOperation for {lro_name}: {e}", exc_info=True)
            return {"result": "failed", "error": str(e)}
        except Exception as e:
            logger.error(f"Unexpected error fetching LRO status for {lro_name}: {e}", exc_info=True)
            return {"result": "failed", "error": f"Unexpected error: {str(e)}"}

    logger.warning(f"LRO {lro_name} timed out after 300 seconds.")
    return {"result": "timeout"}

def create_cloud_control_metadata_list(cloud_controls: str, parent: str) -> list[CloudControlMetadata]:
    cloud_control_metadata_list = []
    for control_entry in cloud_controls.split(','):

        control_entry = control_entry.strip()
        if not control_entry:
            continue

        # Split control ID and revision
        parts = control_entry.split('#')
        if len(parts) != 2:
            print(f"Skipping malformed entry: {control_entry} - missing # or too many #")
            continue

        cloud_control_id, major_revision_str = parts
        
        if not major_revision_str.isdigit():
            print(f"Skipping non-integer revision: {major_revision_str} in {control_entry}")
            continue

        major_revision_id = int(major_revision_str)

        # Construct the full control name
        # control_name = f"{parent_with_location}/cloudControls/{cloud_control_id}"

        print(f"ID: {cloud_control_id}, Major: {major_revision_id}")


        cloud_control_metadata = CloudControlMetadata(
            cloud_control_details=CloudControlDetails(name=f"{parent}/cloudControls/{cloud_control_id}", major_revision_id=major_revision_id),
            enforcement_mode=EnforcementMode.DETECTIVE
        )
        cloud_control_metadata_list.append(cloud_control_metadata)
    return cloud_control_metadata_list

# --- Config Service Tools (Frameworks and Cloud Controls) ---

@mcp.tool()
async def list_frameworks(
    organization_id: str,
    location: str = "global",
    page_size: int = 50,
) -> Dict[str, Any]:
    """Name: list_frameworks

    Description: Lists all compliance frameworks available in an organization. Frameworks can be built-in
                 (e.g., CIS, NIST, FedRAMP) or custom-defined.
    Parameters:
    organization_id (required): The Google Cloud organization ID (e.g., '123456789012').
    location (optional): The location for the frameworks. Defaults to 'global'.
    page_size (optional): Maximum number of frameworks to return. Defaults to 50.
    """
    if not config_client:
        return {"error": "Config Client not initialized."}

    parent = f"organizations/{organization_id}/locations/{location}"
    logger.info(f"Listing frameworks for parent: {parent}")

    try:
        request = ListFrameworksRequest(
            parent=parent,
            page_size=page_size,
        )
        
        response_pager = config_client.list_frameworks(request=request)
        
        frameworks = []
        for framework in response_pager:
            framework_dict = proto_message_to_dict(framework)
            frameworks.append(framework_dict)

        return {
            "frameworks": frameworks,
            "count": len(frameworks),
        }

    except google_exceptions.NotFound as e:
        logger.error(f"Organization not found: {e}")
        return {"error": "Not Found", "details": f"Could not find organization '{organization_id}'. {str(e)}"}
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
    location: str = "global",
) -> Dict[str, Any]:
    """Name: get_framework

    Description: Gets detailed information about a specific compliance framework, including its cloud controls
                 and regulatory control mappings.
    Parameters:
    organization_id (required): The Google Cloud organization ID.
    framework_id (required): The ID of the framework to retrieve.
    location (optional): The location for the framework. Defaults to 'global'.
    """
    if not config_client:
        return {"error": "Config Client not initialized."}

    name = f"organizations/{organization_id}/locations/{location}/frameworks/{framework_id}"
    logger.info(f"Getting framework: {name}")

    try:
        request = GetFrameworkRequest(name=name)
        framework = config_client.get_framework(request=request)

        return proto_message_to_dict(framework)

    except google_exceptions.NotFound as e:
        logger.error(f"Framework not found: {e}")
        return {"error": "Not Found", "details": f"Could not find framework '{framework_id}'. {str(e)}"}
    except google_exceptions.PermissionDenied as e:
        logger.error(f"Permission denied: {e}")
        return {"error": "Permission Denied", "details": str(e)}
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        return {"error": "An unexpected error occurred", "details": str(e)}


@mcp.tool()
async def list_cloud_controls(
    organization_id: str,
    location: str = "global",
    page_size: int = 50,
) -> Dict[str, Any]:
    """Name: list_cloud_controls

    Description: Lists all cloud controls available in an organization. Cloud controls are technical items
                 that help meet compliance requirements.
    Parameters:
    organization_id (required): The Google Cloud organization ID.
    location (optional): The location for the cloud controls. Defaults to 'global'.
    page_size (optional): Maximum number of cloud controls to return. Defaults to 50.
    """
    if not config_client:
        return {"error": "Config Client not initialized."}

    parent = f"organizations/{organization_id}/locations/{location}"
    logger.info(f"Listing cloud controls for parent: {parent}")

    try:
        request = ListCloudControlsRequest(
            parent=parent,
            page_size=page_size,
        )

        response_pager = config_client.list_cloud_controls(request=request)

        cloud_controls = []
        for control in response_pager:
            control_dict = proto_message_to_dict(control)
            cloud_controls.append(control_dict)

        return {
            "cloud_controls": cloud_controls,
            "count": len(cloud_controls),
        }

    except google_exceptions.NotFound as e:
        logger.error(f"Organization not found: {e}")
        return {"error": "Not Found", "details": f"Could not find organization '{organization_id}'. {str(e)}"}
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
    location: str = "global",
) -> Dict[str, Any]:
    """Name: get_cloud_control

    Description: Gets detailed information about a specific cloud control, including its rules, parameters,
                 and enforcement mode.
    Parameters:
    organization_id (required): The Google Cloud organization ID.
    cloud_control_id (required): The ID of the cloud control to retrieve.
    location (optional): The location for the cloud control. Defaults to 'global'.
    """
    if not config_client:
        return {"error": "Config Client not initialized."}

    name = f"organizations/{organization_id}/locations/{location}/cloudControls/{cloud_control_id}"
    logger.info(f"Getting cloud control: {name}")

    try:
        request = GetCloudControlRequest(name=name)
        cloud_control = config_client.get_cloud_control(request=request)

        return proto_message_to_dict(cloud_control)

    except google_exceptions.NotFound as e:
        logger.error(f"Cloud control not found: {e}")
        return {"error": "Not Found", "details": f"Could not find cloud control '{cloud_control_id}'. {str(e)}"}
    except google_exceptions.PermissionDenied as e:
        logger.error(f"Permission denied: {e}")
        return {"error": "Permission Denied", "details": str(e)}
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        return {"error": "An unexpected error occurred", "details": str(e)}


# --- Deployment Service Tools ---

@mcp.tool()
async def list_framework_deployments(
    parent: str,
    location: str = "global",
    page_size: int = 50,
) -> Dict[str, Any]:
    """Name: list_framework_deployments

    Description: Lists all framework deployments for a given parent resource (organization, folder, or project).
    Parameters:
    parent (required): The parent resource in format 'organizations/{org_id}', 'folders/{folder_id}', or 'projects/{project_id}'.
    location (optional): The location for the deployments. Defaults to 'global'.
    page_size (optional): Maximum number of deployments to return. Defaults to 50.
    """
    if not deployment_client:
        return {"error": "Deployment Client not initialized."}

    parent_with_location = f"{parent}/locations/{location}"
    logger.info(f"Listing framework deployments for parent: {parent_with_location}")

    try:
        request = ListFrameworkDeploymentsRequest(
            parent=parent_with_location,
            page_size=page_size,
        )

        response_pager = deployment_client.list_framework_deployments(request=request)

        deployments = []
        for deployment in response_pager:
            deployment_dict = proto_message_to_dict(deployment)
            deployments.append(deployment_dict)

        return {
            "framework_deployments": deployments,
            "count": len(deployments),
        }

    except google_exceptions.NotFound as e:
        logger.error(f"Parent resource not found: {e}")
        return {"error": "Not Found", "details": f"Could not find parent resource '{parent}'. {str(e)}"}
    except google_exceptions.PermissionDenied as e:
        logger.error(f"Permission denied: {e}")
        return {"error": "Permission Denied", "details": str(e)}
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        return {"error": "An unexpected error occurred", "details": str(e)}


@mcp.tool()
async def get_framework_deployment(
    parent: str,
    framework_deployment_id: str,
    location: str = "global",
) -> Dict[str, Any]:
    """Name: get_framework_deployment

    Description: Gets detailed information about a specific framework deployment, including its state and configuration.
    Parameters:
    parent (required): The parent resource in format 'organizations/{org_id}', 'folders/{folder_id}', or 'projects/{project_id}'.
    framework_deployment_id (required): The ID of the framework deployment to retrieve.
    location (optional): The location for the deployment. Defaults to 'global'.
    """
    if not deployment_client:
        return {"error": "Deployment Client not initialized."}

    name = f"{parent}/locations/{location}/frameworkDeployments/{framework_deployment_id}"
    logger.info(f"Getting framework deployment: {name}")

    try:
        request = GetFrameworkDeploymentRequest(name=name)
        deployment = deployment_client.get_framework_deployment(request=request)

        return proto_message_to_dict(deployment)

    except google_exceptions.NotFound as e:
        logger.error(f"Framework deployment not found: {e}")
        return {"error": "Not Found", "details": f"Could not find framework deployment '{framework_deployment_id}'. {str(e)}"}
    except google_exceptions.PermissionDenied as e:
        logger.error(f"Permission denied: {e}")
        return {"error": "Permission Denied", "details": str(e)}
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        return {"error": "An unexpected error occurred", "details": str(e)}


@mcp.tool()
async def create_framework_deployment(
    parent: str,
    framework_deployment_id: str,
    framework_name: str,
    cloud_controls: str,
    framework_version: int = None,
    location: str = "global",
    target_resource: Optional[str] = None,
) -> Dict[str, Any]:
    """Name: create_framework_deployment

    Description: Creates a new framework deployment on a target resource. This applies a compliance framework
                 to an organization, folder, or project. This is a long-running operation.
    Parameters:
    parent (required): The parent resource in format 'organizations/{org_id}', 'folders/{folder_id}', or 'projects/{project_id}'.
    framework_deployment_id (required): The ID for the new framework deployment.
    framework_name (required): The full name of the framework to deploy (e.g., 'organizations/{org_id}/locations/global/frameworks/{framework_id}').
    cloud_controls (required): This is a comma seperated list of could_control ids along with their revision number seperated by a hash.
        So the entire string is of format: cloud_control_id1#revision1,cloud_control_id2#revision2.
    location (optional): The location for the deployment. Defaults to 'global'.
    target_resource (optional): The target resource name. If not provided, uses the parent resource.
    framework_version (optional): The major version of the framework. If not specified the latest version of the framework is used.
    """
    if not deployment_client:
        return {"error": "Deployment Client not initialized."}

    parent_with_location = f"{parent}/locations/{location}"
    complete_framework_deployment_id = f"{parent_with_location}/frameworkDeployments/{framework_deployment_id}"
    logger.info(f"Creating framework deployment '{framework_deployment_id}' in parent: {parent_with_location}")

    cloud_control_metadata_list = create_cloud_control_metadata_list(cloud_controls, parent_with_location)

    # Set target resource if provided
    if not target_resource:
        target_resource = parent

    framework_reference = FrameworkReference(framework = framework_name)
    if framework_version:
        framework_reference.major_revision_id = framework_version

    try:
        # Create the framework deployment object
        framework_deployment = FrameworkDeployment(
            framework=framework_reference,
            cloud_control_metadata=cloud_control_metadata_list,
            target_resource_config = TargetResourceConfig(
                existing_target_resource=target_resource
            ),
            name = complete_framework_deployment_id
        )

        request = CreateFrameworkDeploymentRequest(
            parent=parent_with_location,
            framework_deployment_id=framework_deployment_id,
            framework_deployment=framework_deployment,
        )

        logger.info(f"Request for create framework deployment {request}")

        # This is a long-running operation
        operation_result = deployment_client.create_framework_deployment(request=request)

        # Wait for the operation to complete
        logger.info(f"Waiting for framework deployment creation to complete...: {operation_result.operation.name}")
        return fetch_lro_status(operation_result.operation.name)

    except google_exceptions.NotFound as e:
        logger.error(f"Parent resource or framework not found: {e}")
        return {"error": "Not Found", "details": f"Could not find parent resource '{parent}' or framework '{framework_name}'. {str(e)}"}
    except google_exceptions.PermissionDenied as e:
        logger.error(f"Permission denied: {e}")
        return {"error": "Permission Denied", "details": str(e)}
    except google_exceptions.AlreadyExists as e:
        logger.error(f"Framework deployment already exists: {e}")
        return {"error": "Already Exists", "details": f"Framework deployment '{framework_deployment_id}' already exists. {str(e)}"}
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        return {"error": "An unexpected error occurred", "details": str(e)}


@mcp.tool()
async def delete_framework_deployment(
    parent: str,
    framework_deployment_id: str,
    location: str = "global",
) -> Dict[str, Any]:
    """Name: delete_framework_deployment

    Description: Deletes a framework deployment. This removes the compliance framework from the target resource. This is a long-running operation.
    Parameters:
    parent (required): The parent resource in format 'organizations/{org_id}', 'folders/{folder_id}', or 'projects/{project_id}'.
    framework_deployment_id (required): The ID of the framework deployment to delete.
    location (optional): The location for the deployment. Defaults to 'global'.
    """
    if not deployment_client:
        return {"error": "Deployment Client not initialized."}

    name = f"{parent}/locations/{location}/frameworkDeployments/{framework_deployment_id}"
    logger.info(f"Deleting framework deployment: {name}")

    try:
        request = DeleteFrameworkDeploymentRequest(name=name)

        # This is a long-running operation
        operation_result = deployment_client.delete_framework_deployment(request=request)

        # Wait for the operation to complete
        logger.info(f"Waiting for framework deployment deletion to complete... LRO Name: {operation_result.operation.name}")
        return fetch_lro_status(operation_result.operation.name)

    except google_exceptions.NotFound as e:
        logger.error(f"Framework deployment not found: {e}")
        return {"error": "Not Found", "details": f"Could not find framework deployment '{framework_deployment_id}'. {str(e)}"}
    except google_exceptions.PermissionDenied as e:
        logger.error(f"Permission denied: {e}")
        return {"error": "Permission Denied", "details": str(e)}
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        return {"error": "An unexpected error occurred", "details": str(e)}


@mcp.tool()
async def list_cloud_control_deployments(
    parent: str,
    location: str = "global",
    page_size: int = 50,
) -> Dict[str, Any]:
    """Name: list_cloud_control_deployments

    Description: Lists all cloud control deployments for a given parent resource.
    Parameters:
    parent (required): The parent resource in format 'organizations/{org_id}', 'folders/{folder_id}', or 'projects/{project_id}'.
    location (optional): The location for the deployments. Defaults to 'global'.
    page_size (optional): Maximum number of deployments to return. Defaults to 50.
    """
    if not deployment_client:
        return {"error": "Deployment Client not initialized."}

    parent_with_location = f"{parent}/locations/{location}"
    logger.info(f"Listing cloud control deployments for parent: {parent_with_location}")

    try:
        request = ListCloudControlDeploymentsRequest(
            parent=parent_with_location,
            page_size=page_size,
        )

        response_pager = deployment_client.list_cloud_control_deployments(request=request)

        deployments = []
        for deployment in response_pager:
            deployment_dict = proto_message_to_dict(deployment)
            deployments.append(deployment_dict)

        return {
            "cloud_control_deployments": deployments,
            "count": len(deployments),
        }

    except google_exceptions.NotFound as e:
        logger.error(f"Parent resource not found: {e}")
        return {"error": "Not Found", "details": f"Could not find parent resource '{parent}'. {str(e)}"}
    except google_exceptions.PermissionDenied as e:
        logger.error(f"Permission denied: {e}")
        return {"error": "Permission Denied", "details": str(e)}
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        return {"error": "An unexpected error occurred", "details": str(e)}


@mcp.tool()
async def get_cloud_control_deployment(
    parent: str,
    cloud_control_deployment_id: str,
    location: str = "global",
) -> Dict[str, Any]:
    """Name: get_cloud_control_deployment

    Description: Gets detailed information about a specific cloud control deployment, including its enforcement
                 mode and state.
    Parameters:
    parent (required): The parent resource in format 'organizations/{org_id}', 'folders/{folder_id}', or 'projects/{project_id}'.
    cloud_control_deployment_id (required): The ID of the cloud control deployment to retrieve.
    location (optional): The location for the deployment. Defaults to 'global'.
    """
    if not deployment_client:
        return {"error": "Deployment Client not initialized."}

    name = f"{parent}/locations/{location}/cloudControlDeployments/{cloud_control_deployment_id}"
    logger.info(f"Getting cloud control deployment: {name}")

    try:
        request = GetCloudControlDeploymentRequest(name=name)
        deployment = deployment_client.get_cloud_control_deployment(request=request)

        return proto_message_to_dict(deployment)

    except google_exceptions.NotFound as e:
        logger.error(f"Cloud control deployment not found: {e}")
        return {"error": "Not Found", "details": f"Could not find cloud control deployment '{cloud_control_deployment_id}'. {str(e)}"}
    except google_exceptions.PermissionDenied as e:
        logger.error(f"Permission denied: {e}")
        return {"error": "Permission Denied", "details": str(e)}
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        return {"error": "An unexpected error occurred", "details": str(e)}


# --- Main execution ---

def main() -> None:
    """Runs the FastMCP server."""
    if not config_client:
        logger.critical("Config Client failed to initialize. MCP server cannot serve config tools.")

    if not deployment_client:
        logger.critical("Deployment Client failed to initialize. MCP server cannot serve deployment tools.")

    logger.info("Starting Compliance Manager MCP server...")

    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()

