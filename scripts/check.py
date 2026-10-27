#!/usr/bin/env python3
"""Validate the shared skill, distribution metadata, and local documentation links."""

import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote

import yaml


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/we-need-to-talk"
SKILL = PLUGIN / "skills/we-need-to-talk"


def check() -> list[str]:
    errors = []
    def require(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    documents = list(ROOT.glob("*.md")) + list((ROOT / "docs").rglob("*.md")) + list(PLUGIN.rglob("*.md"))
    for path in documents:
        text = path.read_text(encoding="utf-8")
        require("[TODO:" not in text, f"Unfinished scaffold: {path.relative_to(ROOT)}")
        if SKILL / "assets" in path.parents:
            continue  # These links describe generated session files, not repository files.
        # Fenced examples are not documentation links.
        prose = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
        for target in re.findall(r"\]\(([^)]+)\)", prose):
            if target.startswith(("https://", "http://", "mailto:", "#")):
                continue
            linked = (path.parent / unquote(target.split("#")[0].strip("<>"))).resolve()
            require(linked.exists(), f"Broken link in {path.relative_to(ROOT)}: {target}")
            require(linked == ROOT or ROOT in linked.parents, f"Link escapes repository: {target}")

    text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
    match = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    require(match is not None, "Missing skill frontmatter")
    if match:
        frontmatter = yaml.safe_load(match.group(1))
        require(isinstance(frontmatter, dict), "Skill frontmatter must be a mapping")
        if isinstance(frontmatter, dict):
            require(frontmatter.get("name") == "we-need-to-talk", "Unexpected skill name")
            description = frontmatter.get("description", "")
            require(isinstance(description, str) and 0 < len(description) <= 1024, "Invalid skill description")

    interface = yaml.safe_load((SKILL / "agents/openai.yaml").read_text(encoding="utf-8"))["interface"]
    require(25 <= len(interface["short_description"]) <= 64, "UI description must be 25–64 characters")
    require("$we-need-to-talk" in interface["default_prompt"], "UI prompt must invoke this skill")
    codex = json.loads((PLUGIN / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    claude = json.loads((PLUGIN / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
    for field in ("name", "version", "description", "author", "license", "repository"):
        require(codex.get(field) == claude.get(field), f"Plugin manifests disagree: {field}")
    require((PLUGIN / codex["skills"]).resolve() == SKILL.parent, "Invalid Codex skill path")
    for relative, kind in ((".agents/plugins/marketplace.json", "codex"), (".claude-plugin/marketplace.json", "claude")):
        catalog = json.loads((ROOT / relative).read_text(encoding="utf-8"))
        require(catalog["name"] == "we-need-to-talk", "Marketplace name must match README install commands")
        entry = catalog["plugins"][0]
        path = entry["source"]["path"] if kind == "codex" else entry["source"]
        require((ROOT / path).resolve() == PLUGIN, f"Invalid marketplace path: {relative}")
    require((ROOT / "LICENSE").read_bytes() == (PLUGIN / "LICENSE").read_bytes(), "Packaged license differs from root license")
    require((ROOT / "docs/assets/we-need-to-talk.png").read_bytes().startswith(b"\x89PNG\r\n\x1a\n"), "README image must be a PNG")
    return errors


if __name__ == "__main__":
    try:
        failures = check()
    except (OSError, ValueError, KeyError, TypeError, yaml.YAMLError) as error:
        sys.exit(f"Validation failed: {error}")
    if failures:
        sys.exit("\n".join(failures))
    print("PASS: skill metadata, manifests, licenses, README image, and local documentation links")
