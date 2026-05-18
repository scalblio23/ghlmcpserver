"""
MCP tools for GoHighLevel Contacts API.

Endpoints used:
  GET    /contacts/search
  POST   /contacts/search  (advanced search with filters)
  GET    /contacts/{contactId}
  POST   /contacts/
  PUT    /contacts/{contactId}
  DELETE /contacts/{contactId}
  POST   /contacts/{contactId}/tags
  DELETE /contacts/{contactId}/tags
  GET    /contacts/{contactId}/notes
  POST   /contacts/{contactId}/notes
"""

from __future__ import annotations

from typing import Optional

from mcp.server.fastmcp import FastMCP

from ..client import get_client
from ..config import get_location_id


def register(mcp: FastMCP) -> None:
    """Register all contact-related tools on the MCP server."""

    # ------------------------------------------------------------------ #
    # Search / List
    # ------------------------------------------------------------------ #

    @mcp.tool()
    def search_contacts(
        query: str,
        limit: int = 20,
        skip: int = 0,
    ) -> dict:
        """
        Search GoHighLevel contacts by name, email, or phone number.

        Args:
            query: Search string (name, email, or phone).
            limit: Maximum number of results to return (default 20, max 100).
            skip: Number of results to skip for pagination (default 0).

        Returns:
            A dict with a 'contacts' list and 'total' count.
        """
        client = get_client()
        params = {
            "locationId": get_location_id(),
            "query": query,
            "limit": limit,
            "skip": skip,
        }
        result = client.get("/contacts/search", params=params)
        return result

    # ------------------------------------------------------------------ #
    # Advanced Search (POST /contacts/search)
    # ------------------------------------------------------------------ #

    @mcp.tool()
    def search_contacts_advanced(
        tags: Optional[list[str]] = None,
        date_added_from: Optional[str] = None,
        date_added_to: Optional[str] = None,
        query: Optional[str] = None,
        country: Optional[str] = None,
        source: Optional[str] = None,
        page: int = 1,
        page_limit: int = 20,
    ) -> dict:
        """
        Search GoHighLevel contacts using advanced filters (tags, date ranges, etc.).
        Uses POST /contacts/search which supports structured filter groups.

        Args:
            tags: List of tag names to filter by (e.g. ['S.IO - Funnel Leads', 'VIP']).
                  Returns contacts that have ALL specified tags.
            date_added_from: Start date for filtering by dateAdded (ISO format, e.g. '2026-05-16').
            date_added_to: End date for filtering by dateAdded (ISO format, e.g. '2026-05-18').
            query: Optional free-text search query (name, email, phone).
            country: Filter by country code (e.g. 'US', 'AU').
            source: Filter by lead source (e.g. 'Website', 'Referral').
            page: Page number for pagination (default 1).
            page_limit: Number of results per page (default 20, max 100).

        Returns:
            A dict with a 'contacts' list and 'total' count.
        """
        client = get_client()
        location_id = get_location_id()

        # Build the request body
        body: dict = {
            "locationId": location_id,
            "page": page,
            "pageLimit": min(page_limit, 100),
        }

        # Add free-text query if provided
        if query:
            body["query"] = query

        # Build filter groups for structured filtering
        filters: list[dict] = []

        if tags:
            for tag in tags:
                filters.append({
                    "field": "tags",
                    "operator": "contains",
                    "value": tag,
                })

        if date_added_from or date_added_to:
            date_filter: dict = {
                "field": "dateAdded",
                "operator": "range",
            }
            value: dict = {}
            if date_added_from:
                value["startDate"] = date_added_from
            if date_added_to:
                value["endDate"] = date_added_to
            date_filter["value"] = value
            filters.append(date_filter)

        if country:
            filters.append({
                "field": "country",
                "operator": "eq",
                "value": country,
            })

        if source:
            filters.append({
                "field": "source",
                "operator": "eq",
                "value": source,
            })

        if filters:
            body["filterGroups"] = [
                {
                    "filters": filters,
                }
            ]

        result = client.post("/contacts/search", body=body)
        return result

    # ------------------------------------------------------------------ #
    # Get single contact
    # ------------------------------------------------------------------ #

    @mcp.tool()
    def get_contact(contact_id: str) -> dict:
        """
        Retrieve full details for a GoHighLevel contact by their ID.

        Args:
            contact_id: The GoHighLevel contact ID (e.g. 'abc123xyz').

        Returns:
            A dict containing all contact fields.
        """
        client = get_client()
        return client.get(f"/contacts/{contact_id}")

    # ------------------------------------------------------------------ #
    # Create contact
    # ------------------------------------------------------------------ #

    @mcp.tool()
    def create_contact(
        first_name: str,
        last_name: str = "",
        email: str = "",
        phone: str = "",
        company_name: str = "",
        address1: str = "",
        city: str = "",
        state: str = "",
        postal_code: str = "",
        country: str = "",
        source: str = "",
        tags: Optional[list[str]] = None,
    ) -> dict:
        """
        Create a new contact in GoHighLevel.

        Args:
            first_name: Contact's first name (required).
            last_name: Contact's last name.
            email: Contact's email address.
            phone: Contact's phone number (E.164 format recommended, e.g. +14155552671).
            company_name: Name of the contact's company.
            address1: Street address line 1.
            city: City.
            state: State or province.
            postal_code: ZIP or postal code.
            country: Country code (e.g. 'US').
            source: Lead source label (e.g. 'Website', 'Referral').
            tags: List of tag strings to apply to the contact.

        Returns:
            The newly created contact object.
        """
        client = get_client()
        body: dict = {
            "locationId": get_location_id(),
            "firstName": first_name,
        }
        if last_name:
            body["lastName"] = last_name
        if email:
            body["email"] = email
        if phone:
            body["phone"] = phone
        if company_name:
            body["companyName"] = company_name
        if address1:
            body["address1"] = address1
        if city:
            body["city"] = city
        if state:
            body["state"] = state
        if postal_code:
            body["postalCode"] = postal_code
        if country:
            body["country"] = country
        if source:
            body["source"] = source
        if tags:
            body["tags"] = tags
        return client.post("/contacts/", body=body)

    # ------------------------------------------------------------------ #
    # Update contact
    # ------------------------------------------------------------------ #

    @mcp.tool()
    def update_contact(
        contact_id: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        company_name: Optional[str] = None,
        address1: Optional[str] = None,
        city: Optional[str] = None,
        state: Optional[str] = None,
        postal_code: Optional[str] = None,
        country: Optional[str] = None,
        source: Optional[str] = None,
    ) -> dict:
        """
        Update fields on an existing GoHighLevel contact.
        Only the fields you provide will be changed.

        Args:
            contact_id: The GoHighLevel contact ID to update.
            first_name: New first name.
            last_name: New last name.
            email: New email address.
            phone: New phone number (E.164 format).
            company_name: New company name.
            address1: New street address.
            city: New city.
            state: New state.
            postal_code: New postal code.
            country: New country code.
            source: New lead source.

        Returns:
            The updated contact object.
        """
        client = get_client()
        body: dict = {}
        if first_name is not None:
            body["firstName"] = first_name
        if last_name is not None:
            body["lastName"] = last_name
        if email is not None:
            body["email"] = email
        if phone is not None:
            body["phone"] = phone
        if company_name is not None:
            body["companyName"] = company_name
        if address1 is not None:
            body["address1"] = address1
        if city is not None:
            body["city"] = city
        if state is not None:
            body["state"] = state
        if postal_code is not None:
            body["postalCode"] = postal_code
        if country is not None:
            body["country"] = country
        if source is not None:
            body["source"] = source
        return client.put(f"/contacts/{contact_id}", body=body)

    # ------------------------------------------------------------------ #
    # Delete contact
    # ------------------------------------------------------------------ #

    @mcp.tool()
    def delete_contact(contact_id: str) -> dict:
        """
        Permanently delete a contact from GoHighLevel.

        Args:
            contact_id: The GoHighLevel contact ID to delete.

        Returns:
            Confirmation dict with 'succeeded' boolean.
        """
        client = get_client()
        return client.delete(f"/contacts/{contact_id}")

    # ------------------------------------------------------------------ #
    # Tags
    # ------------------------------------------------------------------ #

    @mcp.tool()
    def add_contact_tags(contact_id: str, tags: list[str]) -> dict:
        """
        Add one or more tags to a GoHighLevel contact.

        Args:
            contact_id: The contact ID to tag.
            tags: List of tag strings to add (e.g. ['VIP', 'Hot Lead']).

        Returns:
            Updated contact tags.
        """
        client = get_client()
        return client.post(f"/contacts/{contact_id}/tags", body={"tags": tags})

    @mcp.tool()
    def remove_contact_tags(contact_id: str, tags: list[str]) -> dict:
        """
        Remove one or more tags from a GoHighLevel contact.

        Args:
            contact_id: The contact ID to update.
            tags: List of tag strings to remove.

        Returns:
            Updated contact tags.
        """
        client = get_client()
        # GHL uses DELETE with a body for tag removal
        import json
        import httpx
        from ..config import get_api_key, get_api_version, get_base_url
        headers = {
            "Authorization": f"Bearer {get_api_key()}",
            "Version": get_api_version(),
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        url = f"{get_base_url()}/contacts/{contact_id}/tags"
        with httpx.Client(headers=headers, timeout=30) as http:
            response = http.request("DELETE", url, content=json.dumps({"tags": tags}))
        try:
            data = response.json()
        except Exception:
            data = {"raw": response.text}
        if response.is_error:
            return {"error": True, "status_code": response.status_code, "message": data.get("message", response.text)}
        return data

    # ------------------------------------------------------------------ #
    # Notes
    # ------------------------------------------------------------------ #

    @mcp.tool()
    def get_contact_notes(contact_id: str) -> dict:
        """
        Retrieve all notes attached to a GoHighLevel contact.

        Args:
            contact_id: The contact ID whose notes to fetch.

        Returns:
            A dict with a 'notes' list.
        """
        client = get_client()
        return client.get(f"/contacts/{contact_id}/notes")

    @mcp.tool()
    def create_contact_note(contact_id: str, body: str, user_id: str = "") -> dict:
        """
        Add a note to a GoHighLevel contact.

        Args:
            contact_id: The contact ID to attach the note to.
            body: The text content of the note.
            user_id: Optional GHL user ID to attribute the note to.

        Returns:
            The created note object.
        """
        client = get_client()
        payload: dict = {"body": body}
        if user_id:
            payload["userId"] = user_id
        return client.post(f"/contacts/{contact_id}/notes", body=payload)
