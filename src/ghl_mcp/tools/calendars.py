"""
MCP tools for GoHighLevel Calendars & Appointments API.

Endpoints used:
  GET    /calendars/
  GET    /calendars/events/appointments
  GET    /calendars/events/appointments/{eventId}
  POST   /calendars/events/appointments
  PUT    /calendars/events/appointments/{eventId}
  DELETE /calendars/events/appointments/{eventId}
  GET    /calendars/{calendarId}/free-slots
"""

from __future__ import annotations

from typing import Optional

from mcp.server.fastmcp import FastMCP

from ..client import get_client
from ..config import get_location_id


def register(mcp: FastMCP) -> None:
    """Register all calendar and appointment tools on the MCP server."""

    @mcp.tool()
    def get_calendars() -> dict:
        """
        List all calendars available in the GoHighLevel location.

        Returns:
            A dict with a 'calendars' list, each containing id, name, and type.
        """
        client = get_client()
        return client.get("/calendars/", params={"locationId": get_location_id()})

    @mcp.tool()
    def get_free_slots(
        calendar_id: str,
        start_date: str,
        end_date: str,
        timezone: str = "UTC",
    ) -> dict:
        """
        Get available (free) time slots for a GoHighLevel calendar.

        Args:
            calendar_id: The calendar ID to check availability for.
            start_date: Start of the date range in ISO 8601 (e.g. '2025-06-01').
            end_date: End of the date range in ISO 8601 (e.g. '2025-06-07').
            timezone: Timezone for the slots (e.g. 'America/New_York', default 'UTC').

        Returns:
            A dict with available time slots grouped by date.
        """
        client = get_client()
        params = {
            "startDate": start_date,
            "endDate": end_date,
            "timezone": timezone,
        }
        return client.get(f"/calendars/{calendar_id}/free-slots", params=params)

    @mcp.tool()
    def get_appointments(
        calendar_id: Optional[str] = None,
        contact_id: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        limit: int = 20,
        skip: int = 0,
    ) -> dict:
        """
        List appointments in the GoHighLevel location.

        Args:
            calendar_id: Filter by specific calendar ID.
            contact_id: Filter by specific contact ID.
            start_time: Filter appointments starting after this ISO 8601 datetime.
            end_time: Filter appointments ending before this ISO 8601 datetime.
            limit: Maximum number of results (default 20).
            skip: Offset for pagination.

        Returns:
            A dict with an 'events' list of appointment objects.
        """
        client = get_client()
        params: dict = {
            "locationId": get_location_id(),
            "limit": limit,
            "skip": skip,
        }
        if calendar_id:
            params["calendarId"] = calendar_id
        if contact_id:
            params["contactId"] = contact_id
        if start_time:
            params["startTime"] = start_time
        if end_time:
            params["endTime"] = end_time
        return client.get("/calendars/events/appointments", params=params)

    @mcp.tool()
    def get_appointment(appointment_id: str) -> dict:
        """
        Get details of a specific GoHighLevel appointment.

        Args:
            appointment_id: The appointment/event ID to retrieve.

        Returns:
            Full appointment details including time, contact, calendar, and status.
        """
        client = get_client()
        return client.get(f"/calendars/events/appointments/{appointment_id}")

    @mcp.tool()
    def create_appointment(
        calendar_id: str,
        contact_id: str,
        start_time: str,
        end_time: str,
        title: str = "",
        timezone: str = "UTC",
        meeting_location_type: str = "default",
        notes: str = "",
    ) -> dict:
        """
        Book a new appointment in a GoHighLevel calendar.

        Args:
            calendar_id: The calendar ID to book the appointment on.
            contact_id: The contact ID this appointment is for.
            start_time: Appointment start in ISO 8601 format
                        (e.g. '2025-06-15T10:00:00Z').
            end_time: Appointment end in ISO 8601 format
                      (e.g. '2025-06-15T11:00:00Z').
            title: Appointment title/subject (optional).
            timezone: Timezone for the appointment (default 'UTC').
            meeting_location_type: Location type — 'default', 'zoom', 'phone',
                                    or 'custom' (default 'default').
            notes: Additional notes for the appointment.

        Returns:
            The created appointment object with its ID and confirmation details.
        """
        client = get_client()
        body: dict = {
            "locationId": get_location_id(),
            "calendarId": calendar_id,
            "contactId": contact_id,
            "startTime": start_time,
            "endTime": end_time,
            "timezone": timezone,
            "meetingLocationType": meeting_location_type,
        }
        if title:
            body["title"] = title
        if notes:
            body["notes"] = notes
        return client.post("/calendars/events/appointments", body=body)

    @mcp.tool()
    def update_appointment(
        appointment_id: str,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        title: Optional[str] = None,
        status: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> dict:
        """
        Update an existing GoHighLevel appointment.

        Args:
            appointment_id: The appointment ID to update.
            start_time: New start time in ISO 8601 format.
            end_time: New end time in ISO 8601 format.
            title: New appointment title.
            status: New status — 'confirmed', 'cancelled', 'showed', 'noshow',
                    or 'invalid'.
            notes: Updated notes.

        Returns:
            The updated appointment object.
        """
        client = get_client()
        body: dict = {}
        if start_time is not None:
            body["startTime"] = start_time
        if end_time is not None:
            body["endTime"] = end_time
        if title is not None:
            body["title"] = title
        if status is not None:
            body["status"] = status
        if notes is not None:
            body["notes"] = notes
        return client.put(f"/calendars/events/appointments/{appointment_id}", body=body)

    @mcp.tool()
    def delete_appointment(appointment_id: str) -> dict:
        """
        Cancel and delete a GoHighLevel appointment.

        Args:
            appointment_id: The appointment ID to delete.

        Returns:
            Confirmation of deletion.
        """
        client = get_client()
        return client.delete(f"/calendars/events/appointments/{appointment_id}")
