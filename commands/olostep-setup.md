---
name: olostep-setup
description: Configure the Olostep Cursor plugin without sharing credentials in chat.
---

# Set up Olostep

Check whether the Olostep MCP server is available in Cursor.

- If it is not configured, direct the user to **Customize → Olostep → Configure** and to https://olostep.com/auth if they need an API key. After saving, they must reload Cursor (**Developer: Reload Window**) for the key to take effect.
- Never ask for, accept, display, or write an API key in chat, source code, or a tracked file.
- If the plugin configuration UI is unavailable, explain the private environment-variable fallback in the `setup` skill.
- After configuration, suggest a harmless scrape of `https://example.com` to confirm the connection.
