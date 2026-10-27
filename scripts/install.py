#!/usr/bin/env python3
"""Install the standalone skill without silently overwriting an existing one."""

import argparse
import os
from pathlib import Path
import shutil
import tempfile
import uuid


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "plugins/we-need-to-talk/skills/we-need-to-talk"
NAME = "we-need-to-talk"


def contents(path: Path) -> dict[str, bytes]:
    """Compare actual payloads, ignoring only bytecode and macOS metadata."""
    result = {}
    for item in path.rglob("*"):
        if item.is_symlink():
            raise ValueError(f"Refusing a skill containing a symlink: {item}")
        if item.is_file() and item.name != ".DS_Store" and "__pycache__" not in item.parts:
            result[item.relative_to(path).as_posix()] = item.read_bytes()
    return result


def install(source: Path, skills_dir: Path, backup_existing: bool = False) -> tuple[Path, Path | None, bool]:
    source = source.resolve()
    if not (source / "SKILL.md").is_file():
        raise ValueError(f"Not a skill directory: {source}")
    skills_dir = skills_dir.expanduser().resolve()
    destination = skills_dir / NAME
    if destination == source or source in destination.parents or destination in source.parents:
        raise ValueError("Installation must be outside the source skill directory.")
    if destination.is_symlink():
        raise ValueError(f"Refusing to replace a symlink: {destination}")
    payload = contents(source)
    if destination.exists():
        if not destination.is_dir():
            raise ValueError(f"Destination is not a directory: {destination}")
        if contents(destination) == payload:
            return destination, None, False
        if not backup_existing:
            raise FileExistsError(f"Existing skill differs: {destination}. Use --backup-existing to preserve it before installing.")

    skills_dir.mkdir(parents=True, exist_ok=True)
    backup = None
    # Stage a complete copy before moving the existing installation.
    with tempfile.TemporaryDirectory(prefix=".we-need-to-talk-install-", dir=skills_dir) as stage:
        staged = Path(stage) / NAME
        shutil.copytree(source, staged)
        if contents(staged) != payload:
            raise OSError("The staged copy does not match the source.")
        if destination.exists():
            backup_dir = skills_dir / ".we-need-to-talk-backups"
            backup_dir.mkdir(exist_ok=True)
            backup = backup_dir / uuid.uuid4().hex
            destination.rename(backup)
        try:
            staged.rename(destination)
        except OSError:
            if backup is not None and not destination.exists():
                backup.rename(destination)
            raise
    return destination, backup, True


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", choices=("codex", "claude"))
    parser.add_argument("--skills-dir", type=Path, help="Override the parent directory that contains skills")
    parser.add_argument("--backup-existing", action="store_true", help="Back up a different existing skill before replacing it")
    args = parser.parse_args()
    if args.skills_dir is not None:
        directory = args.skills_dir
    elif args.target == "codex":
        directory = Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex") / "skills"
    else:
        directory = Path.home() / ".claude" / "skills"
    try:
        destination, backup, changed = install(SOURCE, directory, args.backup_existing)
    except (OSError, ValueError) as error:
        parser.exit(1, f"Install failed: {error}\n")
    print(f"{'Installed' if changed else 'Already up to date'}: {destination}")
    if backup is not None:
        print(f"Previous installation preserved: {backup}")
    print("Start a new chat to discover the skill.")


if __name__ == "__main__":
    main()
