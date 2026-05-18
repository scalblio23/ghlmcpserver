"""
Basic tests for the GoHighLevel MCP server.

These tests verify that:
1. The server can be created without errors.
2. All tool categories register their tools correctly.
3. The GHL client handles missing config gracefully.

Run with:
    cd ghl-mcp-server
    python -m pytest tests/ -v
"""

import os
import sys

import pytest

# Ensure the src package is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


# ---------------------------------------------------------------------------
# Server instantiation
# ---------------------------------------------------------------------------

def test_server_creates_without_error():
    """The MCP server should instantiate even without env vars set."""
    # We import here so that missing env vars don't fail at module level
    from ghl_mcp.server import create_server
    mcp = create_server()
    assert mcp is not None
    assert mcp.name == "GoHighLevel MCP"


def test_all_tools_registered():
    """All expected tools should be registered on the server."""
    from ghl_mcp.server import create_server
    mcp = create_server()

    # Retrieve registered tool names
    # FastMCP stores tools in _tool_manager
    tool_names = set(mcp._tool_manager._tools.keys())

    expected_tools = {
        # Contacts
        "search_contacts",
        "get_contact",
        "create_contact",
        "update_contact",
        "delete_contact",
        "add_contact_tags",
        "remove_contact_tags",
        "get_contact_notes",
        "create_contact_note",
        # Conversations
        "get_conversations",
        "get_conversation",
        "create_conversation",
        "get_messages",
        "send_message",
        # Opportunities
        "get_opportunities",
        "get_opportunity",
        "create_opportunity",
        "update_opportunity",
        "update_opportunity_status",
        "delete_opportunity",
        # Calendars
        "get_calendars",
        "get_free_slots",
        "get_appointments",
        "get_appointment",
        "create_appointment",
        "update_appointment",
        "delete_appointment",
        # Pipelines
        "get_pipelines",
        # Locations
        "get_location",
        "get_users",
        "get_custom_fields",
        "get_tags",
        "get_custom_values",
    }

    missing = expected_tools - tool_names
    assert not missing, f"Missing tools: {missing}"


# ---------------------------------------------------------------------------
# Config validation
# ---------------------------------------------------------------------------

def test_missing_api_key_raises():
    """get_api_key() should raise EnvironmentError when GHL_API_KEY is unset."""
    # Temporarily remove the env var
    original = os.environ.pop("GHL_API_KEY", None)
    try:
        from ghl_mcp import config
        # Reload to clear any cached value
        import importlib
        importlib.reload(config)
        with pytest.raises(EnvironmentError, match="GHL_API_KEY"):
            config.get_api_key()
    finally:
        if original is not None:
            os.environ["GHL_API_KEY"] = original


def test_missing_location_id_raises():
    """get_location_id() should raise EnvironmentError when GHL_LOCATION_ID is unset."""
    original = os.environ.pop("GHL_LOCATION_ID", None)
    try:
        from ghl_mcp import config
        import importlib
        importlib.reload(config)
        with pytest.raises(EnvironmentError, match="GHL_LOCATION_ID"):
            config.get_location_id()
    finally:
        if original is not None:
            os.environ["GHL_LOCATION_ID"] = original


def test_default_base_url():
    """get_base_url() should return the default GHL API URL."""
    from ghl_mcp import config
    import importlib
    importlib.reload(config)
    url = config.get_base_url()
    assert url == "https://services.leadconnectorhq.com"


def test_default_api_version():
    """get_api_version() should return the expected default version string."""
    from ghl_mcp import config
    import importlib
    importlib.reload(config)
    version = config.get_api_version()
    assert version == "2021-07-28"
