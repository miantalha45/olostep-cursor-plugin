# Olostep Plugin for Cursor

Turn any website into clean, LLM-ready markdown or structured data. Olostep integrates powerful web scraping, crawling, search, and AI-powered answers directly into Cursor.

## Features

- **Scrape** — Extract content from any webpage as markdown, HTML, JSON, or text
- **Search** — Search the web and get structured results
- **Crawl** — Autonomously discover and scrape entire websites
- **Map** — Discover all URLs on a site for analysis and planning
- **Batch** — Scrape up to 10,000 URLs in parallel
- **AI Answers** — Get AI-powered answers with citations from live web data
- **Docs-to-code** — Turn current API and library documentation into implementation-ready code

All with automatic JavaScript rendering, anti-bot handling, and proxy rotation built in.

## Installation

### From the Cursor Marketplace

1. In Cursor, open **Customize** in the sidebar and search for **Olostep**, or open the Olostep page on the [Cursor Marketplace](https://cursor.com/marketplace) and select **Add to Cursor**.
2. Select **Install** and choose a project or user scope.
3. Add your API key as described in [Setup and authentication](#setup-and-authentication).

### From source

1. Clone this repository into `~/.cursor/plugins/local/olostep`. Copy the files rather than symlinking; Cursor skips symlinked plugin folders.
2. Restart Cursor, or run **Developer: Reload Window**.
3. Open **Customize** and confirm the Olostep skills, commands, and MCP server are listed.

## Setup and authentication

1. Get a free API key at [olostep.com/auth](https://olostep.com/auth).
2. In Cursor, open **Customize**, select **Olostep**, then select **Configure**. Paste the key into **Olostep API key** and select **Save**.
3. Reload Cursor (**Developer: Reload Window**) so the MCP server picks up the key.

Cursor passes the key to the local MCP server; it is not stored in this repository. Never paste an API key into an agent chat.

### Manual MCP setup (without the plugin)

To use only the MCP tools without installing the plugin, set `OLOSTEP_API_KEY` in the environment that launches Cursor, then add this private configuration to either `.cursor/mcp.json` (project) or `~/.cursor/mcp.json` (global):

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

Restart Cursor and confirm that the Olostep MCP server is enabled in **Customize**.

### Troubleshooting

If a tool call fails with **401 Unauthorized**, check the key in **Configure** (or your environment, for manual setup), then reload Cursor. The MCP server only reads the key when it starts.

## Available Skills

| Skill | Description |
|-------|-------------|
| `setup` | Configure your Olostep API key |
| `scrape` | Extract content from a single webpage |
| `search` | Search the web for information |
| `crawl` | Crawl an entire website from a start URL |
| `map` | Discover all URLs on a website |
| `batch` | Batch scrape up to 10,000 URLs |
| `answers` | Get AI-powered answers with citations |
| `docs-to-code` | Build code from current API or library documentation |
| `debug-error` | Research current errors and known fixes |
| `research` | Perform cited, multi-source technical research |

## Slash Commands

| Command | Description |
|---------|-------------|
| `/olostep-setup` | Configure Olostep without sharing credentials in chat |
| `/olostep-scrape` | Scrape a webpage and return useful content |
| `/olostep-search` | Search the live web for current information |
| `/olostep-docs-to-code` | Use current documentation to write implementation-ready code |

## MCP Tools

The following MCP tools are available directly in Cursor chat:

| Tool | Description |
|------|-------------|
| `create_map` | Discover all URLs on a site |
| `create_crawl` | Autonomously crawl a website |
| `get_crawl_results` | Check crawl status and retrieve crawl results |
| `batch_scrape_urls` | Batch scrape up to 10k URLs |
| `get_batch_results` | Check batch status and retrieve batch results |
| `answers` | AI-powered answers with citations |
| `search_web` | Search the web with structured results |
| `scrape_website` | Extract content from a single URL |
| `get_webpage_content` | Retrieve a webpage as markdown |
| `get_website_urls` | Search and retrieve relevant URLs |

## Usage Examples

**Scrape a webpage:**
> "Scrape https://example.com and give me the main content"

**Search the web:**
> "Search for the top web scraping APIs in 2026"

**Crawl a site:**
> "Crawl https://docs.example.com up to 50 pages and summarize the content"

**Map a site:**
> "Map https://example.com and find all blog URLs"

**Batch scrape:**
> "Scrape all these 20 product URLs and extract the price and title from each"

**AI Answers:**
> "What are the pricing plans for the top 5 web scraping services? Return as JSON with name and price fields."

**Docs-to-code:**
> "Read the current Stripe Payment Intents documentation and write a typed TypeScript helper that creates a payment intent."

## Links

- [Olostep Website](https://olostep.com)
- [API Documentation](https://docs.olostep.com)
- [Get API Key](https://olostep.com/auth)
- [MCP Server on npm](https://www.npmjs.com/package/olostep-mcp)
- [Cursor MCP documentation](https://cursor.com/docs/mcp)

## License

MIT License — see [LICENSE](LICENSE) for details.
