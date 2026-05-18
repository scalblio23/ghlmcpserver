"""
Custom runner for the GoHighLevel MCP Server.
Starts the SSE transport on 0.0.0.0:8080 using Uvicorn directly.
Disables DNS rebinding protection for proxy compatibility.
"""
import sys
import os

# Ensure the src directory is on the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

import uvicorn
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from ghl_mcp.tools import calendars, contacts, conversations, locations, opportunities, pipelines

# Create server with DNS rebinding protection disabled
mcp = FastMCP(
    name="GoHighLevel MCP",
    instructions=(
        "You are connected to a GoHighLevel CRM account. "
        "You can manage contacts, conversations, opportunities, "
        "appointments, pipelines, and location settings. "
        "Always confirm destructive actions (delete, status change to 'lost') "
        "with the user before proceeding."
    ),
    host="0.0.0.0",
    port=8080,
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=False,
    ),
)

# Register all tool categories
contacts.register(mcp)
conversations.register(mcp)
opportunities.register(mcp)
calendars.register(mcp)
pipelines.register(mcp)
locations.register(mcp)

# Get the SSE app
app = mcp.sse_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    host = os.environ.get("HOST", "0.0.0.0")
    print(f"Starting GoHighLevel MCP Server (SSE) on {host}:{port}", file=sys.stderr)
    uvicorn.run(app, host=host, port=port, forwarded_allow_ips="*")
