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

from google.api_core import exceptions as google_exceptions
from google.api_core import operation
from google.cloud.cloudsecuritycompliance_v1.services.config import ConfigClient
from google.cloud.cloudsecuritycompliance_v1.services.deployment import DeploymentClient
from google.cloud.cloudsecuritycompliance_v1.types import (
    CreateFrameworkDeploymentRequest,
    DeleteFrameworkDeploymentRequest,
    Framework,
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
)
from google.protobuf import json_format
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("compliance-manager-mcp")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("compliance-manager-mcp")
logger.setLevel(logging.INFO)

# Add handler to see uvicorn/fastapi logs if they use standard logging
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logging.getLogger().addHandler(handler)

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
    location: str = "global",
    target_resource: Optional[str] = None,
) -> Dict[str, Any]:
    """Name: create_framework_deployment

    Description: Creates a new framework deployment on a target resource. This applies a compliance framework
                 to an organization, folder, or project.
    Parameters:
    parent (required): The parent resource in format 'organizations/{org_id}', 'folders/{folder_id}', or 'projects/{project_id}'.
    framework_deployment_id (required): The ID for the new framework deployment.
    framework_name (required): The full name of the framework to deploy (e.g., 'organizations/{org_id}/locations/global/frameworks/{framework_id}').
    location (optional): The location for the deployment. Defaults to 'global'.
    target_resource (optional): The target resource name. If not provided, uses the parent resource.
    """
    if not deployment_client:
        return {"error": "Deployment Client not initialized."}

    parent_with_location = f"{parent}/locations/{location}"
    logger.info(f"Creating framework deployment '{framework_deployment_id}' in parent: {parent_with_location}")

    try:
        # Create the framework deployment object
        framework_deployment = FrameworkDeployment(
            framework=framework_name,
        )

        # Set target resource if provided
        if target_resource:
            framework_deployment.target_resource_config = TargetResourceConfig(
                target_resource_name=target_resource
            )

        request = CreateFrameworkDeploymentRequest(
            parent=parent_with_location,
            framework_deployment_id=framework_deployment_id,
            framework_deployment=framework_deployment,
        )

        # This is a long-running operation
        operation_result = deployment_client.create_framework_deployment(request=request)

        # Wait for the operation to complete
        logger.info(f"Waiting for framework deployment creation to complete...")
        result = operation_result.result()

        return {
            "status": "success",
            "framework_deployment": proto_message_to_dict(result),
        }

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

    Description: Deletes a framework deployment. This removes the compliance framework from the target resource.
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
        logger.info(f"Waiting for framework deployment deletion to complete...")
        operation_result.result()

        return {
            "status": "success",
            "message": f"Framework deployment '{framework_deployment_id}' deleted successfully.",
        }

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

