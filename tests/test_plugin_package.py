"""Static checks for the Cursor plugin package and its clean-install contract."""

import json
import re

from conftest import PLUGIN_ROOT


MANIFEST_PATH = PLUGIN_ROOT / ".cursor-plugin" / "plugin.json"
MCP_PATH = PLUGIN_ROOT / "mcp.json"
COMMANDS_DIR = PLUGIN_ROOT / "commands"
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
COMMAND_NAME_RE = re.compile(r"^name:\s*([a-z0-9-]+)$", re.MULTILINE)
COMMAND_DESCRIPTION_RE = re.compile(r"^description:\s*.+$", re.MULTILINE)
VARIABLE_RE = re.compile(r"\$\{([A-Z][A-Z0-9_]*)\}")


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_manifest_references_existing_package_files():
    """Every explicitly configured plugin component must exist at its path."""
    manifest = read_json(MANIFEST_PATH)

    for field in ("skills", "commands", "mcpServers", "logo"):
        value = manifest[field]
        assert isinstance(value, str), f"{field} must use one relative package path"
        assert not value.startswith("/") and ".." not in value.split("/"), (
            f"{field} must use a safe relative path: {value}"
        )
        resolved = PLUGIN_ROOT / value.removeprefix("./")
        assert resolved.exists(), f"{field} points to a missing path: {value}"


def test_manifest_declares_the_mcp_api_key_variable():
    """Cursor plugin variables must cover each placeholder in the MCP config."""
    manifest = read_json(MANIFEST_PATH)
    mcp = read_json(MCP_PATH)
    variables = manifest["variables"]

    assert variables["type"] == "object"
    assert "OLOSTEP_API_KEY" in variables["properties"]
    assert "OLOSTEP_API_KEY" in variables["required"]

    placeholders = set(VARIABLE_RE.findall(json.dumps(mcp)))
    assert placeholders <= set(variables["properties"])


def test_stdio_mcp_configuration_is_complete():
    """The local fallback remains a valid, dependency-light Cursor MCP server."""
    server = read_json(MCP_PATH)["mcpServers"]["olostep"]

    assert server["type"] == "stdio"
    assert server["command"] == "npx"
    assert server["args"] == ["-y", "olostep-mcp"]
    assert server["env"] == {"OLOSTEP_API_KEY": "${OLOSTEP_API_KEY}"}


def test_commands_have_cursor_frontmatter_and_reuse_existing_workflows():
    """Commands are discoverable and intentionally delegate to the skills."""
    commands = sorted(COMMANDS_DIR.glob("*.md"))
    assert {command.stem for command in commands} == {
        "olostep-setup",
        "olostep-scrape",
        "olostep-search",
        "olostep-docs-to-code",
    }

    for command in commands:
        content = command.read_text(encoding="utf-8")
        frontmatter = FRONTMATTER_RE.search(content)
        assert frontmatter, f"No frontmatter in {command.name}"
        assert COMMAND_NAME_RE.search(frontmatter.group(1)), f"Invalid name in {command.name}"
        assert COMMAND_DESCRIPTION_RE.search(frontmatter.group(1)), f"Missing description in {command.name}"
        assert "skill" in content.lower(), f"{command.name} must reuse an existing skill"


def test_package_does_not_include_a_local_secret_file():
    """A clean plugin checkout must not ship a local environment file."""
    assert not any(path.name == ".env" for path in PLUGIN_ROOT.rglob(".env"))


def test_setup_guidance_never_uses_a_chat_credential_placeholder():
    """Onboarding must direct secrets to Cursor configuration, never agent chat."""
    setup = (PLUGIN_ROOT / "skills" / "setup" / "SKILL.md").read_text(encoding="utf-8")
    assert "<their-api-key>" not in setup
    assert "your-api-key-here" not in setup
    assert "Never ask them to paste an API key into chat." in setup
