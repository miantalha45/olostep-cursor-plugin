"""
Shared fixtures and configuration for plugin integrity tests.
"""
import os
import re
from pathlib import Path

import pytest

PLUGIN_ROOT = Path(__file__).parent.parent
SKILLS_DIR = PLUGIN_ROOT / "skills"

# Canonical MCP tool names registered by olostep-mcp (npm package)
KNOWN_MCP_TOOLS = {
    "answers",
    "batch_scrape_urls",
    "create_crawl",
    "create_map",
    "get_batch_results",
    "get_crawl_results",
    "get_webpage_content",
    "get_website_urls",
    "scrape_website",
    "search_web",
}

# Parameter names that were valid in old SDK versions but are now wrong
STALE_PARAMS = [
    "json_schema=",       # → json_format=
]

# Removed from the current olostep-mcp tool list.
STALE_MCP_TOOLS = ["google_search"]

# MCP tool reference pattern for Claude Code (mcp__<server>__<tool>)
MCP_REF_PATTERN = re.compile(r"mcp__olostep__(\w+)")

# Code block patterns
PYTHON_BLOCK_RE = re.compile(r"```python\n(.*?)```", re.DOTALL)
TS_BLOCK_RE = re.compile(r"```typescript\n(.*?)```", re.DOTALL)
JS_BLOCK_RE = re.compile(r"```(?:js|javascript)\n(.*?)```", re.DOTALL)


def all_skill_files():
    return sorted(SKILLS_DIR.glob("*/SKILL.md"))


@pytest.fixture(scope="session")
def api_key():
    key = os.getenv("OLOSTEP_API_KEY")
    if not key:
        pytest.skip("OLOSTEP_API_KEY not set — skipping live tests")
    return key
