import unittest
from unittest.mock import MagicMock, patch, AsyncMock
import sys
import os

# Add the parent directory to the path so we can import compliance_mcp
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import tools to test
from compliance_mcp import (
    enroll_resource,
    generate_audit_scope_report,
    list_audit_reports,
    get_audit_report,
    get_resource_enrollment_status,
    list_resource_enrollment_statuses
)

class TestAuditManager(unittest.IsolatedAsyncioTestCase):

    @patch('compliance_mcp.audit_manager_client')
    async def test_enroll_resource_success(self, mock_client):
        mock_enrollment = MagicMock()
        mock_client.enroll_resource.return_value = mock_enrollment

        with patch('compliance_mcp.proto_message_to_dict') as mock_to_dict:
            mock_to_dict.return_value = {"state": "ENROLLED"}
            
            result = enroll_resource(scope="projects/p1", destinations=["gs://bucket"])
            
            self.assertEqual(result, {"state": "ENROLLED"})
            mock_client.enroll_resource.assert_called_once()

    @patch('compliance_mcp.audit_manager_client')
    async def test_generate_audit_scope_report(self, mock_client):
        mock_operation = MagicMock()
        mock_client.generate_audit_scope_report.return_value = mock_operation
        
        with patch('compliance_mcp.proto_message_to_dict') as mock_to_dict:
            mock_to_dict.return_value = {"name": "op-1"}

            result = generate_audit_scope_report(
                scope="projects/p1",
                compliance_standard="FEDRAMP"
            )
            
            self.assertEqual(result, {"name": "op-1"})
            mock_client.generate_audit_scope_report.assert_called_once()

    @patch('compliance_mcp.audit_manager_client')
    async def test_list_audit_reports(self, mock_client):
        mock_pager = MagicMock()
        mock_report = MagicMock()
        mock_pager.__iter__.return_value = [mock_report]
        mock_pager.next_page_token = ""
        mock_client.list_audit_reports.return_value = mock_pager

        with patch('compliance_mcp.proto_message_to_dict') as mock_to_dict:
            mock_to_dict.return_value = {"name": "report1"}
            
            result = list_audit_reports(parent="projects/p1")
            
            self.assertEqual(result["audit_reports"], [{"name": "report1"}])
            mock_client.list_audit_reports.assert_called_once()

    @patch('compliance_mcp.audit_manager_client')
    async def test_get_audit_report(self, mock_client):
        mock_report = MagicMock()
        mock_client.get_audit_report.return_value = mock_report

        with patch('compliance_mcp.proto_message_to_dict') as mock_to_dict:
            mock_to_dict.return_value = {"name": "report1"}
            
            result = get_audit_report(parent="projects/p1", audit_report_id="rep-1")
            
            self.assertEqual(result, {"name": "report1"})
            mock_client.get_audit_report.assert_called_once()
    
    @patch('compliance_mcp.audit_manager_client')
    async def test_client_not_initialized(self, mock_client):
        with patch('compliance_mcp.audit_manager_client', None):
            result = list_audit_reports(parent="projects/p1")
            self.assertEqual(result, {"error": "Audit Manager Client not initialized"})

if __name__ == '__main__':
    unittest.main()
