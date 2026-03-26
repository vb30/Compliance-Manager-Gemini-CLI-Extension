import unittest
from unittest.mock import MagicMock, patch
import sys
import os
import asyncio

# Add the parent directory to the path so we can import compliance_mcp
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from compliance_mcp import create_workload, get_workload, list_workloads
from compliance_mcp import update_workload, restrict_allowed_resources, delete_workload
from compliance_mcp import list_violations, get_violation, acknowledge_violation

class TestAssuredWorkloads(unittest.IsolatedAsyncioTestCase):
    
    @patch('compliance_mcp.assuredworkloads_v1.AssuredWorkloadsServiceClient')
    async def test_create_workload_success(self, mock_client_class):
        # Mock the client instance
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        mock_operation = MagicMock()
        mock_operation.operation.name = "organizations/123/locations/us-central1/operations/456"
        mock_client.create_workload.return_value = mock_operation

        result = await create_workload(
            organization_id="123",
            location="us-central1",
            display_name="Test Workload",
            compliance_regime="FEDRAMP_MODERATE",
            billing_account="billingAccounts/123"
        )

        self.assertEqual(result["status"], "operation_started")
        self.assertEqual(result["operation"], "organizations/123/locations/us-central1/operations/456")
        mock_client.create_workload.assert_called_once()

    @patch('compliance_mcp.assured_workloads_client')
    async def test_get_workload_success(self, mock_client):
        # Mock the client response - returning a MagicMock that acts like a proto
        mock_workload = MagicMock()
        # We need to mock _pb for proto_message_to_dict to work, OR mock proto_message_to_dict
        # Since proto_message_to_dict uses json_format.MessageToDict(message._pb)
        # It's easier to patch proto_message_to_dict for this test to avoid proto complexity
        pass
    
    @patch('compliance_mcp.assuredworkloads_v1.AssuredWorkloadsServiceClient')
    @patch('compliance_mcp.proto_message_to_dict')
    async def test_get_workload_success_with_mock_converter(self, mock_converter, mock_client_class):
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        mock_client.get_workload.return_value = MagicMock()
        mock_converter.return_value = {"name": "workload/123", "displayName": "Test"}

        result = await get_workload(
            organization_id="123",
            location="us-central1",
            workload_id="workload-1"
        )

        self.assertEqual(result["name"], "workload/123")
        mock_client.get_workload.assert_called_once()

    @patch('compliance_mcp.assured_workloads_client')
    async def test_client_not_initialized(self, mock_client):
        # Temporarily set client to None
        with patch('compliance_mcp.assured_workloads_client', None):
            result = await create_workload("1","2","3","4","5")
            self.assertIn("error", result)
            self.assertEqual(result["error"], "Assured Workloads Client not initialized.")

if __name__ == '__main__':
    unittest.main()
