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


def test_manifest_declares_every_mcp_variable():
    """Cursor plugin variables must cover each placeholder in the MCP config."""
    manifest = read_json(MANIFEST_PATH)
    placeholders = set(VARIABLE_RE.findall(MCP_PATH.read_text(encoding="utf-8")))
    declared = set(manifest.get("variables", {}).get("properties", {}))

    assert placeholders <= declared, f"Undeclared variables: {placeholders - declared}"


def test_mcp_uses_hosted_oauth_server():
    """The plugin connects to the hosted server so Cursor handles OAuth sign-in."""
    server = read_json(MCP_PATH)["mcpServers"]["olostep"]

    assert server == {"url": "https://mcp.olostep.com/mcp"}, (
        "mcp.json must point at the hosted server with no API key or local command"
    )


def test_skill_names_are_namespaced():
    """Skills use the olostep- prefix and match their folder, to avoid clashing with other plugins."""
    for skill in sorted((PLUGIN_ROOT / "skills").glob("*/SKILL.md")):
        frontmatter = FRONTMATTER_RE.search(skill.read_text(encoding="utf-8"))
        assert frontmatter, f"No frontmatter in {skill}"
        name = COMMAND_NAME_RE.search(frontmatter.group(1))
        assert name, f"Invalid name in {skill}"
        assert name.group(1).startswith("olostep-"), f"{skill.parent.name} must be prefixed with olostep-"
        assert name.group(1) == skill.parent.name, f"Skill name {name.group(1)} != folder {skill.parent.name}"


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
    setup = (PLUGIN_ROOT / "skills" / "olostep-setup" / "SKILL.md").read_text(encoding="utf-8")
    assert "<their-api-key>" not in setup
    assert "your-api-key-here" not in setup
    assert "Never ask them to paste the key into chat." in setup
