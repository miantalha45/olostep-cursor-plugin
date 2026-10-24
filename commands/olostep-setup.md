---
name: olostep-setup
description: Connect the Olostep Cursor plugin via OAuth sign-in, without sharing credentials in chat.
---

# Set up Olostep

Check whether the olostep MCP server is connected in Cursor.

- If it is not connected, follow the `olostep-setup` skill: direct the user to **Customize → olostep** to sign in with their Olostep account (or create one at https://olostep.com/auth).
- Never ask for, accept, display, or write an API key in chat, source code, or a tracked file.
- If OAuth sign-in is unavailable, explain the API-key fallback in the `olostep-setup` skill.
- After connecting, suggest a harmless scrape of `https://example.com` to confirm the connection.
