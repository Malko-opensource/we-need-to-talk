#!/usr/bin/env python3
"""Build a plugin ZIP from an explicit payload allowlist, without local sessions."""

import argparse
import hashlib
import json
from pathlib import Path
import zipfile


ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/we-need-to-talk"


def build(output_dir: Path) -> Path:
    manifest = json.loads((PLUGIN / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
    output_dir.mkdir(parents=True, exist_ok=True)
    archive = output_dir / f"we-need-to-talk-{manifest['version']}.zip"
    files = [p for p in PLUGIN.rglob("*") if p.is_file() and p.name != ".DS_Store" and "__pycache__" not in p.parts]
    entries = [(p, "we-need-to-talk/" + p.relative_to(PLUGIN).as_posix()) for p in files]
    entries.append((ROOT / "SOURCES.md", "we-need-to-talk/SOURCES.md"))
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for source, name in sorted(entries, key=lambda entry: entry[1]):
            if source.is_symlink():
                raise ValueError(f"Do not package symlinks: {source}")
            info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            bundle.writestr(info, source.read_bytes())
    with zipfile.ZipFile(archive) as bundle:
        if bundle.testzip() is not None:
            raise OSError("Archive integrity check failed")
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    archive.with_suffix(".zip.sha256").write_text(f"{digest}  {archive.name}\n", encoding="utf-8")
    return archive


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "dist")
    print(build(parser.parse_args().output_dir).resolve())
