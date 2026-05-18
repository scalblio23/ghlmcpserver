"""
MCP tools for GoHighLevel Conversations & Messages API.

Endpoints used:
  GET    /conversations/search
  GET    /conversations/{conversationId}
  POST   /conversations/
  GET    /conversations/{conversationId}/messages
  POST   /conversations/messages
"""

from __future__ import annotations

from typing import Optional

from mcp.server.fastmcp import FastMCP

from ..client import get_client
from ..config import get_location_id


def register(mcp: FastMCP) -> None:
    """Register all conversation-related tools on the MCP server."""

    @mcp.tool()
    def get_conversations(
        contact_id: Optional[str] = None,
        limit: int = 20,
        skip: int = 0,
        sort: str = "desc",
    ) -> dict:
        """
        List conversations in the GoHighLevel location.
        Optionally filter by a specific contact.

        Args:
            contact_id: Filter conversations to a specific contact ID.
            limit: Maximum number of results (default 20, max 100).
            skip: Number of results to skip for pagination.
            sort: Sort order for results — 'asc' or 'desc' (default 'desc').

        Returns:
            A dict with a 'conversations' list and 'total' count.
        """
        client = get_client()
        params: dict = {
            "locationId": get_location_id(),
            "limit": limit,
            "skip": skip,
            "sort": sort,
        }
        if contact_id:
            params["contactId"] = contact_id
        return client.get("/conversations/search", params=params)

    @mcp.tool()
    def get_conversation(conversation_id: str) -> dict:
        """
        Get details of a specific GoHighLevel conversation.

        Args:
            conversation_id: The conversation ID to retrieve.

        Returns:
            Conversation details including contact info, channel, and last message.
        """
        client = get_client()
        return client.get(f"/conversations/{conversation_id}")

    @mcp.tool()
    def create_conversation(
        contact_id: str,
    ) -> dict:
        """
        Create or retrieve an existing conversation with a contact.

        Args:
            contact_id: The contact ID to start a conversation with.

        Returns:
            The conversation object (new or existing).
        """
        client = get_client()
        body = {
            "locationId": get_location_id(),
            "contactId": contact_id,
        }
        return client.post("/conversations/", body=body)

    @mcp.tool()
    def get_messages(
        conversation_id: str,
        limit: int = 20,
        last_message_id: Optional[str] = None,
    ) -> dict:
        """
        Retrieve messages from a GoHighLevel conversation.

        Args:
            conversation_id: The conversation ID to fetch messages from.
            limit: Maximum number of messages to return (default 20).
            last_message_id: Cursor for pagination — pass the last message ID
                             from a previous call to get the next page.

        Returns:
            A dict with a 'messages' list.
        """
        client = get_client()
        params: dict = {"limit": limit}
        if last_message_id:
            params["lastMessageId"] = last_message_id
        return client.get(f"/conversations/{conversation_id}/messages", params=params)

    @mcp.tool()
    def send_message(
        conversation_id: str,
        message_type: str,
        message: str,
        subject: Optional[str] = None,
        html: Optional[str] = None,
        from_name: Optional[str] = None,
        from_email: Optional[str] = None,
        email_to: Optional[str] = None,
        email_cc: Optional[list[str]] = None,
        email_bcc: Optional[list[str]] = None,
        scheduled_timestamp: Optional[int] = None,
    ) -> dict:
        """
        Send a message in a GoHighLevel conversation.

        Args:
            conversation_id: The conversation ID to send the message to.
            message_type: Message channel — one of: 'SMS', 'Email', 'WhatsApp',
                         'GMB', 'IG', 'FB', 'Custom', 'Live_Chat'.
            message: The plain-text body of the message.
            subject: Email subject line (required for Email type).
            html: HTML body for email messages (optional).
            from_name: Sender display name (for email).
            from_email: Sender email address (for email).
            email_to: Recipient email address (for email).
            email_cc: List of CC email addresses (for email).
            email_bcc: List of BCC email addresses (for email).
            scheduled_timestamp: Unix timestamp (seconds) to schedule the
                                  message for future delivery.

        Returns:
            The sent message object with its ID and status.
        """
        client = get_client()
        body: dict = {
            "type": message_type,
            "conversationId": conversation_id,
            "message": message,
        }
        if subject:
            body["subject"] = subject
        if html:
            body["html"] = html
        if from_name:
            body["fromName"] = from_name
        if from_email:
            body["from"] = from_email
        if email_to:
            body["emailTo"] = email_to
        if email_cc:
            body["emailCc"] = email_cc
        if email_bcc:
            body["emailBcc"] = email_bcc
        if scheduled_timestamp:
            body["scheduledTimestamp"] = scheduled_timestamp
        return client.post("/conversations/messages", body=body)
