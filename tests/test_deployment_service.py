import unittest
from unittest.mock import MagicMock, patch, AsyncMock
import sys
import os

# Add the parent directory to the path so we can import compliance_mcp
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import tools to test
from compliance_mcp import (
    list_framework_deployments,
    get_framework_deployment,
    create_framework_deployment,
    delete_framework_deployment,
    list_cloud_control_deployments,
    get_cloud_control_deployment
)

class TestDeploymentService(unittest.IsolatedAsyncioTestCase):

    @patch('compliance_mcp.deployment_client')
    async def test_list_framework_deployments_success(self, mock_client):
        mock_pager = MagicMock()
        mock_deployment = MagicMock()
        mock_pager.framework_deployments = [mock_deployment]
        mock_pager.next_page_token = ""
        mock_client.list_framework_deployments.return_value = mock_pager

        with patch('compliance_mcp.proto_message_to_dict') as mock_to_dict:
            mock_to_dict.return_value = {"name": "deployment1"}
            
            result = await list_framework_deployments(organization_id="123")
            
            self.assertEqual(result["framework_deployments"], [{"name": "deployment1"}])
            mock_client.list_framework_deployments.assert_called_once()

    @patch('compliance_mcp.deployment_client')
    async def test_get_framework_deployment_success(self, mock_client):
        mock_deployment = MagicMock()
        mock_client.get_framework_deployment.return_value = mock_deployment

        with patch('compliance_mcp.proto_message_to_dict') as mock_to_dict:
            mock_to_dict.return_value = {"name": "deployment1"}
            
            result = await get_framework_deployment(organization_id="123", framework_deployment_id="dep-1")
            
            self.assertEqual(result, {"name": "deployment1"})
            mock_client.get_framework_deployment.assert_called_once()

    @patch('compliance_mcp.deployment_client')
    async def test_create_framework_deployment_success(self, mock_client):
        mock_operation = MagicMock()
        mock_operation.operation.name = "op-1"
        mock_operation.done = True
        # HasField is a method on protobuf messages, so we need to mock it
        mock_operation.HasField.return_value = False
        mock_client.create_framework_deployment.return_value = mock_operation
        mock_client.get_operation.return_value = mock_operation

        result = await create_framework_deployment(
            organization_id="123",
            framework_deployment_id="dep-1",
            framework_name="frameworks/fw-1",
            framework_version=1,
            cloud_controls="cc-1#1#DETECTIVE"
        )
        
        self.assertEqual(result["result"], "passed")
        mock_client.create_framework_deployment.assert_called_once()

    @patch('compliance_mcp.deployment_client')
    async def test_delete_framework_deployment_success(self, mock_client):
        mock_operation = MagicMock()
        mock_operation.operation.name = "op-1"
        mock_operation.done = True
        mock_operation.HasField.return_value = False
        mock_client.delete_framework_deployment.return_value = mock_operation
        mock_client.get_operation.return_value = mock_operation

        result = await delete_framework_deployment(organization_id="123", framework_deployment_id="dep-1")
        
        self.assertEqual(result["result"], "passed")
        mock_client.delete_framework_deployment.assert_called_once()
    
    @patch('compliance_mcp.deployment_client')
    async def test_client_not_initialized(self, mock_client):
        with patch('compliance_mcp.deployment_client', None):
            result = await list_framework_deployments("123")
            self.assertEqual(result, {"error": "Deployment Client not initialized."})

if __name__ == '__main__':
    unittest.main()
