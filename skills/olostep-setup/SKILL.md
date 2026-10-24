---
name: olostep-setup
description: Connect Cursor to Olostep. Use when the user is setting up Olostep for the first time, the olostep MCP server is not connected, or tool calls fail with an authentication error. Never request an API key in chat.
---

# Olostep Setup

Get the Olostep MCP server connected in Cursor so all Olostep skills work.

## Steps

1. **Sign in**: The plugin uses Olostep's hosted MCP server (`https://mcp.olostep.com/mcp`) with OAuth. In Cursor, open **Customize**, select the **olostep** MCP server, and use its sign-in / connect option. A browser window opens where the user logs in to Olostep (or creates a free account at https://olostep.com/auth).

2. **Confirm the connection**: Back in Cursor, the olostep server should show as connected with 10 tools.

3. **Verify it works**: Suggest a simple test:
   - `/olostep-scrape` a URL to confirm scraping works
   - `/olostep-search` a question to confirm search works

## API-key fallback

If OAuth sign-in isn't available (for example, the sign-in window is blocked), the user can run the MCP server locally with an API key. Never ask them to paste the key into chat. They should set `OLOSTEP_API_KEY` in the environment that launches Cursor, then add this to their private `.cursor/mcp.json` or `~/.cursor/mcp.json` and reload Cursor:

```json
{
  "mcpServers": {
    "olostep": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "olostep-mcp"],
      "env": {
        "OLOSTEP_API_KEY": "${env:OLOSTEP_API_KEY}"
      }
    }
  }
}
```

## Troubleshooting

- **"401 Unauthorized" / needs authentication**: Sign in again from the olostep server in **Customize**. For the API-key fallback, check the key at https://olostep.com/auth and reload Cursor.
- **Sign-in window doesn't open**: Reload Cursor (**Developer: Reload Window**) and try again from **Customize**.
- **Tools not appearing**: Open **Customize** to confirm the olostep server is listed and enabled.
- **"npx not found"** (API-key fallback only): Node.js is not installed. Install it from https://nodejs.org.

## What you get

Once connected, use the matching Olostep skills or slash commands. Start with `/olostep-scrape`, `/olostep-search`, or `/olostep-docs-to-code`.

## Links
- Create an account: https://olostep.com/auth
- Documentation: https://docs.olostep.com
- MCP server on GitHub: https://github.com/olostep/olostep-mcp-server
