"""
Configuration loader for the GoHighLevel MCP Server.
Reads settings from environment variables (or a .env file).
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from the project root (two levels up from this file)
_env_path = Path(__file__).resolve().parents[3] / ".env"
load_dotenv(dotenv_path=_env_path, override=False)


def get_api_key() -> str:
    """Return the GHL v2 API key, raising if not set."""
    key = os.environ.get("GHL_API_KEY", "").strip()
    if not key:
        raise EnvironmentError(
            "GHL_API_KEY is not set. "
            "Copy .env.example to .env and add your GoHighLevel API key."
        )
    return key


def get_location_id() -> str:
    """Return the default GHL location/sub-account ID, raising if not set."""
    loc = os.environ.get("GHL_LOCATION_ID", "").strip()
    if not loc:
        raise EnvironmentError(
            "GHL_LOCATION_ID is not set. "
            "Copy .env.example to .env and add your GoHighLevel Location ID."
        )
    return loc


def get_base_url() -> str:
    """Return the GHL API base URL."""
    return os.environ.get(
        "GHL_BASE_URL", "https://services.leadconnectorhq.com"
    ).rstrip("/")


def get_api_version() -> str:
    """Return the GHL API version header value."""
    return os.environ.get("GHL_API_VERSION", "2021-07-28")
