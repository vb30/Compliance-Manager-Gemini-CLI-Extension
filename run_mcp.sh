#!/bin/bash
# Wrapper script to run the MCP server with proper environment configuration
# This suppresses stderr warnings that interfere with the MCP protocol

cd "$(dirname "$0")"

# Suppress all Google Cloud and Python logging
export GRPC_VERBOSITY=ERROR
export GLOG_minloglevel=3
export PYTHONUNBUFFERED=1

# Run Python with stderr redirected to /dev/null
exec .venv/bin/python3 -W ignore compliance_manager_mcp.py 2>/dev/null

