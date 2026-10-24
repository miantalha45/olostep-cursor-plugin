---
name: setup
description: Configure Olostep securely in Cursor. Use when the user is setting up Olostep for the first time, has no API key configured, or is getting authentication errors. Never request an API key in chat.
---

# Olostep Setup

Get the Olostep MCP server running in Cursor so all Olostep skills work.

## Steps

1. **Get an API key**: If the user doesn't have one, direct them to https://olostep.com/auth. Never ask them to paste an API key into chat.

2. **Configure the plugin**: In Cursor, open **Customize**, select **Olostep**, then choose **Configure** and enter the key there. Then reload Cursor (**Developer: Reload Window**) so the MCP server picks up the key. Cursor supplies the configured value to the plugin without placing it in this repository.

3. **API-key fallback**: If the plugin configuration UI is unavailable, set `OLOSTEP_API_KEY` in the environment that launches Cursor, then add the following to your private `.cursor/mcp.json` or `~/.cursor/mcp.json`. Do not commit the file or paste the key into agent chat.

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

4. **Verify it works**: Suggest the user tries a simple test:
   - `/olostep-scrape` a URL to confirm scraping works
   - `/olostep-search` a question to confirm search works

## Troubleshooting

- **"401 Unauthorized"**: The API key is missing or invalid. Check it at https://olostep.com/auth.
- **"npx not found"**: Node.js is not installed. Install it from https://nodejs.org.
- **Tools not appearing**: Restart Cursor after adding the MCP config. Open **Customize** in the sidebar to confirm the server is listed and enabled.
- **Stale npx cache**: If tools seem outdated, run `npx clear-npx-cache` in a terminal, then restart Cursor.

## What you get

Once configured, use the matching Olostep skills or slash commands. Start with `/olostep-scrape`, `/olostep-search`, or `/olostep-docs-to-code`.

## Links
- Get your API key: https://olostep.com/auth
- Documentation: https://docs.olostep.com
- MCP server on npm: https://www.npmjs.com/package/olostep-mcp
- GitHub: https://github.com/olostep/olostep-mcp-server
