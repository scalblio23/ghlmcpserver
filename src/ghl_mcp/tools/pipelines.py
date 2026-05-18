"""
MCP tools for GoHighLevel Pipelines API.

Endpoints used:
  GET    /opportunities/pipelines
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from ..client import get_client
from ..config import get_location_id


def register(mcp: FastMCP) -> None:
    """Register all pipeline-related tools on the MCP server."""

    @mcp.tool()
    def get_pipelines() -> dict:
        """
        List all sales pipelines and their stages in the GoHighLevel location.

        Returns:
            A dict with a 'pipelines' list. Each pipeline contains its ID, name,
            and a 'stages' list with stage IDs and names.
        """
        client = get_client()
        return client.get(
            "/opportunities/pipelines",
            params={"locationId": get_location_id()},
        )
