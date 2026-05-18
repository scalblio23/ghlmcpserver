"""
MCP tools for GoHighLevel Opportunities (Pipeline CRM) API.

Endpoints used:
  GET    /opportunities/search
  GET    /opportunities/{id}
  POST   /opportunities/
  PUT    /opportunities/{id}
  DELETE /opportunities/{id}
  PUT    /opportunities/{id}/status
"""

from __future__ import annotations

from typing import Optional

from mcp.server.fastmcp import FastMCP

from ..client import get_client
from ..config import get_location_id


def register(mcp: FastMCP) -> None:
    """Register all opportunity-related tools on the MCP server."""

    @mcp.tool()
    def get_opportunities(
        pipeline_id: Optional[str] = None,
        pipeline_stage_id: Optional[str] = None,
        contact_id: Optional[str] = None,
        status: Optional[str] = None,
        assigned_to: Optional[str] = None,
        query: Optional[str] = None,
        limit: int = 20,
        skip: int = 0,
        order: str = "added_desc",
    ) -> dict:
        """
        Search and list opportunities in the GoHighLevel pipeline.

        Args:
            pipeline_id: Filter by pipeline ID.
            pipeline_stage_id: Filter by a specific pipeline stage ID.
            contact_id: Filter by associated contact ID.
            status: Filter by status — 'open', 'won', 'lost', or 'abandoned'.
            assigned_to: Filter by assigned user ID.
            query: Text search across opportunity names.
            limit: Maximum results to return (default 20, max 100).
            skip: Offset for pagination.
            order: Sort order — e.g. 'added_desc', 'added_asc', 'updated_desc'.

        Returns:
            A dict with an 'opportunities' list and 'meta' pagination info.
        """
        client = get_client()
        params: dict = {
            "location_id": get_location_id(),
            "limit": limit,
            "skip": skip,
            "order": order,
        }
        if pipeline_id:
            params["pipeline_id"] = pipeline_id
        if pipeline_stage_id:
            params["pipeline_stage_id"] = pipeline_stage_id
        if contact_id:
            params["contact_id"] = contact_id
        if status:
            params["status"] = status
        if assigned_to:
            params["assigned_to"] = assigned_to
        if query:
            params["q"] = query
        return client.get("/opportunities/search", params=params)

    @mcp.tool()
    def get_opportunity(opportunity_id: str) -> dict:
        """
        Get full details of a single GoHighLevel opportunity.

        Args:
            opportunity_id: The opportunity ID to retrieve.

        Returns:
            Opportunity details including stage, value, contact, and pipeline.
        """
        client = get_client()
        return client.get(f"/opportunities/{opportunity_id}")

    @mcp.tool()
    def create_opportunity(
        pipeline_id: str,
        pipeline_stage_id: str,
        contact_id: str,
        name: str,
        status: str = "open",
        monetary_value: Optional[float] = None,
        assigned_to: Optional[str] = None,
        close_date: Optional[str] = None,
    ) -> dict:
        """
        Create a new opportunity in a GoHighLevel pipeline.

        Args:
            pipeline_id: The pipeline ID to add the opportunity to.
            pipeline_stage_id: The stage ID within the pipeline.
            contact_id: The contact ID this opportunity is linked to.
            name: Name/title of the opportunity.
            status: Opportunity status — 'open', 'won', 'lost', or 'abandoned'
                    (default 'open').
            monetary_value: Deal value in dollars (e.g. 5000.00).
            assigned_to: User ID to assign the opportunity to.
            close_date: Expected close date in ISO 8601 format (e.g. '2025-12-31').

        Returns:
            The newly created opportunity object.
        """
        client = get_client()
        body: dict = {
            "locationId": get_location_id(),
            "pipelineId": pipeline_id,
            "pipelineStageId": pipeline_stage_id,
            "contactId": contact_id,
            "name": name,
            "status": status,
        }
        if monetary_value is not None:
            body["monetaryValue"] = monetary_value
        if assigned_to:
            body["assignedTo"] = assigned_to
        if close_date:
            body["closeDate"] = close_date
        return client.post("/opportunities/", body=body)

    @mcp.tool()
    def update_opportunity(
        opportunity_id: str,
        pipeline_stage_id: Optional[str] = None,
        name: Optional[str] = None,
        status: Optional[str] = None,
        monetary_value: Optional[float] = None,
        assigned_to: Optional[str] = None,
        close_date: Optional[str] = None,
    ) -> dict:
        """
        Update an existing GoHighLevel opportunity.
        Only the fields you provide will be changed.

        Args:
            opportunity_id: The opportunity ID to update.
            pipeline_stage_id: Move to a different stage ID.
            name: New opportunity name.
            status: New status — 'open', 'won', 'lost', or 'abandoned'.
            monetary_value: New deal value in dollars.
            assigned_to: New assigned user ID.
            close_date: New expected close date (ISO 8601).

        Returns:
            The updated opportunity object.
        """
        client = get_client()
        body: dict = {}
        if pipeline_stage_id is not None:
            body["pipelineStageId"] = pipeline_stage_id
        if name is not None:
            body["name"] = name
        if status is not None:
            body["status"] = status
        if monetary_value is not None:
            body["monetaryValue"] = monetary_value
        if assigned_to is not None:
            body["assignedTo"] = assigned_to
        if close_date is not None:
            body["closeDate"] = close_date
        return client.put(f"/opportunities/{opportunity_id}", body=body)

    @mcp.tool()
    def update_opportunity_status(
        opportunity_id: str,
        status: str,
    ) -> dict:
        """
        Quickly update only the status of a GoHighLevel opportunity.

        Args:
            opportunity_id: The opportunity ID to update.
            status: New status — 'open', 'won', 'lost', or 'abandoned'.

        Returns:
            Confirmation of the status change.
        """
        client = get_client()
        return client.put(
            f"/opportunities/{opportunity_id}/status",
            body={"status": status},
        )

    @mcp.tool()
    def delete_opportunity(opportunity_id: str) -> dict:
        """
        Delete a GoHighLevel opportunity permanently.

        Args:
            opportunity_id: The opportunity ID to delete.

        Returns:
            Confirmation dict with 'succeeded' boolean.
        """
        client = get_client()
        return client.delete(f"/opportunities/{opportunity_id}")
