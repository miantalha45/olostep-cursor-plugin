"""
Static integrity tests for all SKILL.md files in the plugin.

Checks:
- Python code blocks are syntactically valid (AST parse)
- MCP tool references match registered tool names in olostep-mcp
- No stale/deprecated parameter names in code examples
- Required frontmatter fields are present
"""
import ast
import re

import pytest

from conftest import (
    KNOWN_MCP_TOOLS,
    MCP_REF_PATTERN,
    PYTHON_BLOCK_RE,
    SKILLS_DIR,
    STALE_MCP_TOOLS,
    STALE_PARAMS,
    all_skill_files,
)

FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---", re.DOTALL)
FRONTMATTER_FIELD_RE = re.compile(r"^(\w+):\s*.+", re.MULTILINE)
REQUIRED_FRONTMATTER = {"name", "description"}


# ---------------------------------------------------------------------------
# Parametrize over skill files
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("skill_file", all_skill_files(), ids=lambda f: f.parent.name)
def test_frontmatter_present(skill_file):
    """Every SKILL.md must have a frontmatter block with name and description."""
    content = skill_file.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.search(content)
    assert match, f"No frontmatter block found in {skill_file}"
    found = {m.group(1) for m in FRONTMATTER_FIELD_RE.finditer(match.group(1))}
    missing = REQUIRED_FRONTMATTER - found
    assert not missing, f"Missing frontmatter fields {missing} in {skill_file}"


@pytest.mark.parametrize("skill_file", all_skill_files(), ids=lambda f: f.parent.name)
def test_no_stale_params(skill_file):
    """No deprecated parameter names should appear in code examples."""
    content = skill_file.read_text(encoding="utf-8")
    for param in STALE_PARAMS:
        assert param not in content, (
            f"Stale parameter '{param}' found in {skill_file.relative_to(SKILLS_DIR.parent)}"
        )


@pytest.mark.parametrize("skill_file", all_skill_files(), ids=lambda f: f.parent.name)
def test_mcp_tool_references_valid(skill_file):
    """
    Any mcp__olostep__<tool> reference in the file must match a real tool
    registered by the olostep-mcp npm package.
    """
    content = skill_file.read_text(encoding="utf-8")
    refs = MCP_REF_PATTERN.findall(content)
    unknown = [r for r in refs if r not in KNOWN_MCP_TOOLS]
    assert not unknown, (
        f"Unknown MCP tool(s) {unknown} in {skill_file.relative_to(SKILLS_DIR.parent)}\n"
        f"Known tools: {sorted(KNOWN_MCP_TOOLS)}"
    )


@pytest.mark.parametrize("skill_file", all_skill_files(), ids=lambda f: f.parent.name)
def test_no_removed_mcp_tools(skill_file):
    """Skills should not advertise MCP tools removed from olostep-mcp."""
    content = skill_file.read_text(encoding="utf-8")
    stale = [tool for tool in STALE_MCP_TOOLS if tool in content]
    assert not stale, (
        f"Removed MCP tool(s) {stale} found in {skill_file.relative_to(SKILLS_DIR.parent)}"
    )


@pytest.mark.parametrize("skill_file", all_skill_files(), ids=lambda f: f.parent.name)
def test_python_code_blocks_syntax(skill_file):
    """All Python code blocks must parse without syntax errors."""
    content = skill_file.read_text(encoding="utf-8")
    blocks = PYTHON_BLOCK_RE.findall(content)
    errors = []
    for i, block in enumerate(blocks):
        try:
            ast.parse(block)
        except SyntaxError as e:
            errors.append(f"Block {i + 1}: {e}")
    assert not errors, (
        f"Syntax error(s) in Python code blocks in "
        f"{skill_file.relative_to(SKILLS_DIR.parent)}:\n" + "\n".join(errors)
    )


def test_all_skills_have_skill_file():
    """Every subdirectory of skills/ must have a SKILL.md."""
    dirs = [d for d in SKILLS_DIR.iterdir() if d.is_dir()]
    missing = [d for d in dirs if not (d / "SKILL.md").exists()]
    assert not missing, f"Skill dirs without SKILL.md: {missing}"
