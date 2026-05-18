# GoHighLevel MCP Server

A Model Context Protocol (MCP) server that connects Claude (and other MCP-compatible LLM clients) to the GoHighLevel (GHL) CRM platform via the v2 REST API.

## Features

This server exposes 30+ tools across 6 categories, allowing Claude to:
- **Contacts:** Search, create, update, delete, tag, and add notes to contacts.
- **Conversations:** List conversations, fetch messages, and send SMS/Email messages.
- **Opportunities:** Manage pipeline deals, update stages, and change statuses.
- **Calendars:** List calendars, check free slots, and book/update/cancel appointments.
- **Pipelines:** Retrieve all sales pipelines and their stages.
- **Locations:** Fetch location details, users, custom fields, and tags.

## Prerequisites

- Python 3.10 or higher
- A GoHighLevel account with API access
- Your GoHighLevel **v2 Private API Key**
- Your GoHighLevel **Location ID** (Sub-Account ID)

## Installation

1. Clone or download this repository.
2. Install the package and its dependencies:
   ```bash
   pip install -e .
   ```
   *(Alternatively, use `uv pip install -e .` if you use `uv`)*

3. Copy the environment template:
   ```bash
   cp .env.example .env
   ```

4. Edit `.env` and add your GoHighLevel credentials:
   ```env
   GHL_API_KEY=your_api_key_here
   GHL_LOCATION_ID=your_location_id_here
   ```

## Usage with Claude Desktop

To use this server with Claude Desktop, add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "gohighlevel": {
      "command": "python",
      "args": ["-m", "ghl_mcp.server"],
      "env": {
        "GHL_API_KEY": "your_api_key_here",
        "GHL_LOCATION_ID": "your_location_id_here"
      }
    }
  }
}
```

## Usage with Claude Code

You can add the server to Claude Code using the CLI:

```bash
claude mcp add gohighlevel python -m ghl_mcp.server
```
*(Make sure your `.env` file is in the directory where you run Claude Code, or pass the environment variables directly).*

## Running as an HTTP Server

If you want to deploy the server remotely and connect via HTTP/SSE:

```bash
python -m ghl_mcp.server --transport http --port 8000
```

## Development & Testing

To run the test suite:
```bash
pip install pytest
PYTHONPATH=src python -m pytest tests/ -v
```

## License

MIT License
# Trigger redeploy
