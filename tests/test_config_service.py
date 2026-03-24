import unittest
from unittest.mock import MagicMock, patch, AsyncMock
import sys
import os

# Add the parent directory to the path so we can import compliance_mcp
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import tools to test
from compliance_mcp import (
    list_frameworks,
    get_framework,
    create_framework,
    list_cloud_controls,
    get_cloud_control,
    create_cloud_control
)

class TestConfigService(unittest.IsolatedAsyncioTestCase):

    @patch('compliance_mcp.config_client')
    async def test_list_frameworks_success(self, mock_client):
        # Mock response
        mock_pager = MagicMock()
        mock_framework = MagicMock()
        # Mocking _pb for proto_message_to_dict
        mock_framework._pb = MagicMock()
        mock_pager.frameworks = [mock_framework]
        mock_pager.next_page_token = "next_token"
        mock_client.list_frameworks.return_value = mock_pager

        with patch('compliance_mcp.proto_message_to_dict') as mock_to_dict:
            mock_to_dict.return_value = {"name": "framework1"}
            
            result = await list_frameworks(organization_id="123")
            
            self.assertEqual(result["frameworks"], [{"name": "framework1"}])
            self.assertEqual(result["page_token"], "next_token")
            mock_client.list_frameworks.assert_called_once()

    @patch('compliance_mcp.config_client')
    async def test_get_framework_success(self, mock_client):
        mock_framework = MagicMock()
        mock_client.get_framework.return_value = mock_framework

        with patch('compliance_mcp.proto_message_to_dict') as mock_to_dict:
            mock_to_dict.return_value = {"name": "framework1"}
            
            result = await get_framework(organization_id="123", framework_id="fw-1")
            
            self.assertEqual(result, {"name": "framework1"})
            mock_client.get_framework.assert_called_once()

    @patch('compliance_mcp.config_client')
    async def test_create_framework_success(self, mock_client):
        mock_framework = MagicMock()
        mock_client.create_framework.return_value = mock_framework

        with patch('compliance_mcp.proto_message_to_dict') as mock_to_dict:
            mock_to_dict.return_value = {"name": "framework1"}
            
            result = await create_framework(
                organization_id="123",
                framework_id="fw-1",
                display_name="Test Framework",
                cloud_control_ids="cc-1, cc-2"
            )
            
            self.assertEqual(result["status"], "success")
            self.assertEqual(result["framework"], {"name": "framework1"})
            mock_client.create_framework.assert_called_once()

    @patch('compliance_mcp.config_client')
    async def test_list_cloud_controls_success(self, mock_client):
        mock_pager = MagicMock()
        mock_control = MagicMock()
        mock_pager.cloud_controls = [mock_control]
        mock_pager.next_page_token = ""
        mock_client.list_cloud_controls.return_value = mock_pager

        with patch('compliance_mcp.proto_message_to_dict') as mock_to_dict:
            mock_to_dict.return_value = {"name": "control1"}
            
            result = await list_cloud_controls(organization_id="123")
            
            self.assertEqual(result["cloud_controls"], [{"name": "control1"}])
            mock_client.list_cloud_controls.assert_called_once()

    @patch('compliance_mcp.config_client')
    async def test_create_cloud_control_success(self, mock_client):
        mock_control = MagicMock()
        mock_client.create_cloud_control.return_value = mock_control

        with patch('compliance_mcp.proto_message_to_dict') as mock_to_dict:
            mock_to_dict.return_value = {"name": "control1"}
            
            result = await create_cloud_control(
                organization_id="123",
                cloud_control_id="cc-1",
                display_name="Test Control",
                resource_types="compute.googleapis.com/Instance",
                cel_expression="request.resource.name.startsWith('prod')",
                rule_action_types="DETECTIVE"
            )
            
            self.assertEqual(result["status"], "success")
            self.assertEqual(result["cloud_control"], {"name": "control1"})
            mock_client.create_cloud_control.assert_called_once()

    @patch('compliance_mcp.config_client')
    async def test_client_not_initialized(self, mock_client):
        with patch('compliance_mcp.config_client', None):
            result = await list_frameworks("123")
            self.assertEqual(result, {"error": "Config Client not initialized."})

if __name__ == '__main__':
    unittest.main()
