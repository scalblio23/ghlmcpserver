"""
MCP tools for GoHighLevel Locations, Users, Custom Fields, and Tags API.

Endpoints used:
  GET    /locations/{locationId}
  GET    /users/search
  GET    /locations/{locationId}/customFields
  GET    /locations/{locationId}/tags
  GET    /locations/{locationId}/customValues
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from ..client import get_client
from ..config import get_location_id


def register(mcp: FastMCP) -> None:
    """Register all location, user, and metadata tools on the MCP server."""

    @mcp.tool()
    def get_location() -> dict:
        """
        Get details of the configured GoHighLevel location (sub-account).

        Returns:
            Location details including name, address, timezone, and settings.
        """
        client = get_client()
        loc_id = get_location_id()
        return client.get(f"/locations/{loc_id}")

    @mcp.tool()
    def get_users(
        limit: int = 25,
        skip: int = 0,
    ) -> dict:
        """
        List all users (team members) in the GoHighLevel location.

        Args:
            limit: Maximum number of users to return (default 25).
            skip: Offset for pagination.

        Returns:
            A dict with a 'users' list containing IDs, names, emails, and roles.
        """
        client = get_client()
        params = {
            "locationId": get_location_id(),
            "limit": limit,
            "skip": skip,
        }
        return client.get("/users/search", params=params)

    @mcp.tool()
    def get_custom_fields() -> dict:
        """
        List all custom contact fields defined in the GoHighLevel location.

        Returns:
            A dict with a 'customFields' list, each containing id, name,
            fieldKey, dataType, and options (for dropdown fields).
        """
        client = get_client()
        loc_id = get_location_id()
        return client.get(f"/locations/{loc_id}/customFields")

    @mcp.tool()
    def get_tags() -> dict:
        """
        List all contact tags available in the GoHighLevel location.

        Returns:
            A dict with a 'tags' list of tag names.
        """
        client = get_client()
        loc_id = get_location_id()
        return client.get(f"/locations/{loc_id}/tags")

    @mcp.tool()
    def get_custom_values() -> dict:
        """
        List all custom values (snippets/variables) defined in the GoHighLevel location.
        These are reusable text snippets used in templates and messages.

        Returns:
            A dict with a 'customValues' list containing id, name, and value.
        """
        client = get_client()
        loc_id = get_location_id()
        return client.get(f"/locations/{loc_id}/customValues")
