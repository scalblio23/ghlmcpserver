"""
GoHighLevel MCP Server — Main Entry Point

This module creates the FastMCP server instance, registers all tool
categories, and exposes the server via stdio (default) or HTTP transport.

Usage:
    # stdio (for Claude Desktop / Claude Code)
    python -m ghl_mcp.server

    # HTTP (for remote deployments)
    python -m ghl_mcp.server --transport http --port 8000
"""

from __future__ import annotations

import argparse
import sys

from mcp.server.fastmcp import FastMCP

from .tools import calendars, contacts, conversations, locations, opportunities, pipelines

# ---------------------------------------------------------------------------
# Server creation
# ---------------------------------------------------------------------------

def create_server() -> FastMCP:
    """Instantiate and configure the GoHighLevel MCP server."""
    mcp = FastMCP(
        name="GoHighLevel MCP",
        instructions=(
            "You are connected to a GoHighLevel CRM account. "
            "You can manage contacts, conversations, opportunities, "
            "appointments, pipelines, and location settings. "
            "Always confirm destructive actions (delete, status change to 'lost') "
            "with the user before proceeding."
        ),
    )

    # Register all tool categories
    contacts.register(mcp)
    conversations.register(mcp)
    opportunities.register(mcp)
    calendars.register(mcp)
    pipelines.register(mcp)
    locations.register(mcp)

    return mcp


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="GoHighLevel MCP Server — connects Claude to GoHighLevel CRM"
    )
    parser.add_argument(
        "--transport",
        choices=["stdio", "http", "sse"],
        default="stdio",
        help="Transport protocol (default: stdio for Claude Desktop/Code)",
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host to bind when using HTTP transport (default: 0.0.0.0)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to listen on when using HTTP transport (default: 8000)",
    )
    args = parser.parse_args()

    mcp = create_server()

    if args.transport == "http":
        import os
        os.environ["UVICORN_HOST"] = args.host
        os.environ["UVICORN_PORT"] = str(args.port)
        os.environ["HOST"] = args.host
        os.environ["PORT"] = str(args.port)
        print(
            f"Starting GoHighLevel MCP Server via streamable-http on {args.host}:{args.port}",
            file=sys.stderr,
        )
        mcp.run(transport="streamable-http")
    elif args.transport == "sse":
        import os
        os.environ["UVICORN_HOST"] = args.host
        os.environ["UVICORN_PORT"] = str(args.port)
        os.environ["HOST"] = args.host
        os.environ["PORT"] = str(args.port)
        print(
            f"Starting GoHighLevel MCP Server via SSE on {args.host}:{args.port}",
            file=sys.stderr,
        )
        mcp.run(transport="sse")
    else:
        # stdio is the default — used by Claude Desktop and Claude Code
        mcp.run(transport="stdio")


# Allow running as a module: python -m ghl_mcp.server
if __name__ == "__main__":
    main()
