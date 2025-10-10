#!/usr/bin/env python3
# Copyright 2025 Varun Bhardwaj
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

"""
Test script to verify the Compliance Manager MCP server can be imported and initialized.
"""

import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_imports():
    """Test that all required modules can be imported."""
    logger.info("Testing imports...")
    
    try:
        import google.cloud.cloudsecuritycompliance_v1
        logger.info("✓ google-cloud-cloudsecuritycompliance imported successfully")
    except ImportError as e:
        logger.error(f"✗ Failed to import google-cloud-cloudsecuritycompliance: {e}")
        return False
    
    try:
        import mcp.server.fastmcp
        logger.info("✓ mcp.server.fastmcp imported successfully")
    except ImportError as e:
        logger.error(f"✗ Failed to import mcp.server.fastmcp: {e}")
        return False
    
    try:
        import compliance_manager_mcp
        logger.info("✓ compliance_manager_mcp imported successfully")
    except ImportError as e:
        logger.error(f"✗ Failed to import compliance_manager_mcp: {e}")
        return False
    
    return True

def test_client_initialization():
    """Test that the MCP server clients can be initialized."""
    logger.info("Testing client initialization...")
    
    try:
        from google.cloud.cloudsecuritycompliance_v1.services.config import ConfigClient
        from google.cloud.cloudsecuritycompliance_v1.services.deployment import DeploymentClient
        
        # Note: These will fail if credentials are not configured, but we're just testing import
        logger.info("✓ Client classes imported successfully")
        logger.info("  Note: Actual client initialization requires valid Google Cloud credentials")
        return True
    except Exception as e:
        logger.error(f"✗ Failed to import client classes: {e}")
        return False

def test_mcp_server():
    """Test that the MCP server can be imported."""
    logger.info("Testing MCP server...")
    
    try:
        import compliance_manager_mcp
        
        # Check that the server has the expected tools
        if hasattr(compliance_manager_mcp, 'mcp'):
            logger.info("✓ MCP server object found")
            
            # Try to get the list of tools (this may vary depending on FastMCP version)
            try:
                tools = compliance_manager_mcp.mcp._tools if hasattr(compliance_manager_mcp.mcp, '_tools') else []
                logger.info(f"  Found {len(tools)} tools registered")
            except:
                logger.info("  Could not enumerate tools (this is okay)")
            
            return True
        else:
            logger.error("✗ MCP server object not found")
            return False
    except Exception as e:
        logger.error(f"✗ Failed to test MCP server: {e}")
        return False

def test_authentication():
    """Test Google Cloud authentication."""
    logger.info("Testing Google Cloud authentication...")
    
    try:
        import google.auth
        from google.auth import default
        
        credentials, project = default()
        logger.info("✓ Google Cloud credentials found")
        if project:
            logger.info(f"  Default project: {project}")
        else:
            logger.info("  No default project set")
        return True
    except Exception as e:
        logger.warning(f"⚠ Google Cloud authentication not configured: {e}")
        logger.info("  Run: gcloud auth application-default login")
        return False

def main():
    """Run all tests."""
    logger.info("=" * 60)
    logger.info("Compliance Manager Extension Test Suite")
    logger.info("=" * 60)
    logger.info("")
    
    results = {
        "Imports": test_imports(),
        "Client Initialization": test_client_initialization(),
        "MCP Server": test_mcp_server(),
        "Authentication": test_authentication(),
    }
    
    logger.info("")
    logger.info("=" * 60)
    logger.info("Test Results Summary")
    logger.info("=" * 60)
    
    all_passed = True
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        logger.info(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    logger.info("")
    if all_passed:
        logger.info("✓ All tests passed!")
        logger.info("")
        logger.info("The extension is ready to use.")
        logger.info("Start Gemini CLI and try: @compliance-manager-mcp list_frameworks organization_id=\"YOUR_ORG_ID\"")
        return 0
    else:
        logger.error("✗ Some tests failed")
        logger.info("")
        logger.info("Please check the errors above and:")
        logger.info("1. Ensure all dependencies are installed: uv pip install -e .")
        logger.info("2. Configure Google Cloud authentication: gcloud auth application-default login")
        logger.info("3. Verify you have the required IAM permissions")
        return 1

if __name__ == "__main__":
    sys.exit(main())

