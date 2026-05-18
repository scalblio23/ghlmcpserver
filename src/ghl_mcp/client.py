"""
GoHighLevel API v2 HTTP client wrapper.

All requests are authenticated with the Bearer token and include the
required `Version` header. Errors are surfaced as plain dicts so that
MCP tools can return human-readable messages to Claude.
"""

from __future__ import annotations

import json
from typing import Any

import httpx

from .config import get_api_key, get_api_version, get_base_url


class GHLClient:
    """Thin async HTTP client for the GoHighLevel v2 REST API."""

    def __init__(self) -> None:
        self._base_url = get_base_url()
        self._headers = {
            "Authorization": f"Bearer {get_api_key()}",
            "Version": get_api_version(),
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _url(self, path: str) -> str:
        return f"{self._base_url}/{path.lstrip('/')}"

    def _handle_response(self, response: httpx.Response) -> dict[str, Any]:
        """Parse response JSON and wrap HTTP errors in a friendly dict."""
        try:
            data = response.json()
        except Exception:
            data = {"raw": response.text}

        if response.is_error:
            return {
                "error": True,
                "status_code": response.status_code,
                "message": data.get("message", response.text),
                "details": data,
            }
        return data

    # ------------------------------------------------------------------
    # Public CRUD methods
    # ------------------------------------------------------------------

    def get(self, path: str, params: dict | None = None) -> dict[str, Any]:
        with httpx.Client(headers=self._headers, timeout=30) as client:
            response = client.get(self._url(path), params=params)
        return self._handle_response(response)

    def post(self, path: str, body: dict | None = None) -> dict[str, Any]:
        with httpx.Client(headers=self._headers, timeout=30) as client:
            response = client.post(self._url(path), content=json.dumps(body or {}))
        return self._handle_response(response)

    def put(self, path: str, body: dict | None = None) -> dict[str, Any]:
        with httpx.Client(headers=self._headers, timeout=30) as client:
            response = client.put(self._url(path), content=json.dumps(body or {}))
        return self._handle_response(response)

    def patch(self, path: str, body: dict | None = None) -> dict[str, Any]:
        with httpx.Client(headers=self._headers, timeout=30) as client:
            response = client.patch(self._url(path), content=json.dumps(body or {}))
        return self._handle_response(response)

    def delete(self, path: str) -> dict[str, Any]:
        with httpx.Client(headers=self._headers, timeout=30) as client:
            response = client.delete(self._url(path))
        return self._handle_response(response)


# Module-level singleton — instantiated lazily so that missing env vars
# only raise at tool call time, not at import time.
_client: GHLClient | None = None


def get_client() -> GHLClient:
    global _client
    if _client is None:
        _client = GHLClient()
    return _client
