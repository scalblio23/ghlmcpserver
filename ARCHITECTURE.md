# GoHighLevel MCP Server — Architecture Design

## Overview

This MCP server bridges Claude (and any MCP-compatible LLM client) with the GoHighLevel (GHL) CRM platform via the GHL v2 REST API. It uses the **FastMCP** framework from the official `mcp` Python SDK.

## Tool Categories

### 1. Contacts
- `search_contacts` — Search contacts by name, email, or phone
- `get_contact` — Get full contact details by ID
- `create_contact` — Create a new contact
- `update_contact` — Update contact fields
- `delete_contact` — Delete a contact
- `add_contact_tag` — Add tags to a contact
- `remove_contact_tag` — Remove tags from a contact
- `get_contact_notes` — List notes for a contact
- `create_contact_note` — Add a note to a contact

### 2. Conversations & Messages
- `get_conversations` — List conversations for a location
- `get_conversation` — Get a conversation by ID
- `create_conversation` — Start a new conversation
- `send_message` — Send a message in a conversation (SMS/Email)
- `get_messages` — Get messages in a conversation

### 3. Opportunities (Pipeline / CRM)
- `get_opportunities` — List opportunities with filters
- `get_opportunity` — Get opportunity details
- `create_opportunity` — Create a new opportunity
- `update_opportunity` — Update opportunity stage/status/value
- `delete_opportunity` — Delete an opportunity

### 4. Calendars & Appointments
- `get_calendars` — List available calendars
- `get_appointments` — List appointments
- `create_appointment` — Book an appointment
- `update_appointment` — Update appointment details
- `delete_appointment` — Cancel an appointment

### 5. Pipelines
- `get_pipelines` — List all pipelines and stages

### 6. Users & Locations
- `get_location` — Get location/sub-account info
- `get_users` — List users in a location

### 7. Custom Fields & Tags
- `get_custom_fields` — List custom fields for contacts
- `get_tags` — List all tags

## Authentication

The server supports two authentication modes:
1. **API Key** (simple, for private use) — passed as `Authorization: Bearer <API_KEY>` header
2. **OAuth2** (for marketplace apps) — access token passed via environment variable

Configuration is done via environment variables:
- `GHL_API_KEY` — Private API key (v2)
- `GHL_LOCATION_ID` — Default location/sub-account ID
- `GHL_BASE_URL` — API base URL (default: `https://services.leadconnectorhq.com`)

## Transport

The server runs via **stdio** transport (default for Claude Desktop) and optionally via **streamable HTTP** for remote deployments.

## File Structure

```
ghl-mcp-server/
├── src/
│   └── ghl_mcp/
│       ├── __init__.py
│       ├── server.py          # FastMCP server entry point
│       ├── client.py          # GHL API HTTP client wrapper
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── contacts.py
│       │   ├── conversations.py
│       │   ├── opportunities.py
│       │   ├── calendars.py
│       │   ├── pipelines.py
│       │   └── locations.py
│       └── config.py          # Environment config loader
├── tests/
│   └── test_tools.py
├── docs/
│   └── setup.md
├── pyproject.toml
├── README.md
└── .env.example
```
