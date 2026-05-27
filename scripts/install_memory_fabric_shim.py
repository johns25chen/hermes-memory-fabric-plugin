#!/usr/bin/env python3
"""Install the Hermes directory-loader shim for Memory Fabric."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


PLUGIN_NAME = "memory-fabric"
PLUGIN_DESCRIPTION = "Civilization Core / Hermes Memory Fabric read-only provider shim."

INIT_PY_CONTENT = '''"""Local Hermes memory provider shim for hermes-memory-fabric-plugin.

This shim lets Hermes' directory-based plugins.memory loader discover the
installed pip package as a MemoryProvider.
"""

from hermes_memory_fabric.provider import MemoryFabricProvider


def register(ctx):
    ctx.register_memory_provider(MemoryFabricProvider())
'''

PLUGIN_YAML_CONTENT = f"""name: {PLUGIN_NAME}
description: {PLUGIN_DESCRIPTION}
"""


class InstallerError(RuntimeError):
    """Raised when the shim cannot be installed safely."""


@dataclass(frozen=True)
class FileInstallResult:
    path: Path
    action: str


@dataclass(frozen=True)
class InstallSummary:
    hermes_home: Path
    plugin_dir: Path
    dry_run: bool
    force: bool
    files: tuple[FileInstallResult, ...]


def default_hermes_home() -> Path:
    return Path.home() / ".hermes"


def install_shim(
    hermes_home: Path | str | None = None,
    *,
    dry_run: bool = False,
    force: bool = False,
) -> InstallSummary:
    """Create or update the Memory Fabric shim under a Hermes home directory."""

    resolved_home = Path(hermes_home).expanduser() if hermes_home is not None else default_hermes_home()
    plugin_dir = resolved_home / "plugins" / PLUGIN_NAME

    if plugin_dir.exists() and not plugin_dir.is_dir():
        if not force:
            raise InstallerError(f"{plugin_dir} exists and is not a directory; rerun with --force to replace it")
        if not dry_run:
            plugin_dir.unlink()

    if not dry_run:
        plugin_dir.mkdir(parents=True, exist_ok=True)

    files = (
        _install_file(plugin_dir / "__init__.py", INIT_PY_CONTENT, dry_run=dry_run, force=force),
        _install_file(plugin_dir / "plugin.yaml", PLUGIN_YAML_CONTENT, dry_run=dry_run, force=force),
    )
    return InstallSummary(
        hermes_home=resolved_home,
        plugin_dir=plugin_dir,
        dry_run=dry_run,
        force=force,
        files=files,
    )


def format_summary(summary: InstallSummary) -> str:
    mode = "dry-run" if summary.dry_run else "install"
    lines = [
        "Hermes Memory Fabric shim installer",
        f"Mode: {mode}",
        f"Hermes home: {summary.hermes_home}",
        f"Plugin dir: {summary.plugin_dir}",
        f"Force: {'yes' if summary.force else 'no'}",
        "Files:",
    ]
    for file_result in summary.files:
        lines.append(f"- {file_result.path}: {file_result.action}")
    lines.extend(
        [
            "Safety:",
            "- auth.json: not touched",
            "- provider tool exposure: unchanged",
            "- real model calls: none",
            "",
        ]
    )
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Install the Hermes plugins.memory shim for hermes-memory-fabric-plugin."
    )
    parser.add_argument(
        "--hermes-home",
        type=Path,
        default=None,
        help="Hermes home directory to update. Defaults to ~/.hermes.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would change without writing files.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace a non-directory shim path and rewrite managed files.",
    )
    args = parser.parse_args(argv)

    try:
        summary = install_shim(args.hermes_home, dry_run=args.dry_run, force=args.force)
    except InstallerError as exc:
        parser.exit(status=1, message=f"error: {exc}\n")
        return 1

    print(format_summary(summary), end="")
    return 0


def _install_file(path: Path, content: str, *, dry_run: bool, force: bool) -> FileInstallResult:
    exists = path.exists()
    current = path.read_text(encoding="utf-8") if exists and path.is_file() else None

    if exists and not path.is_file():
        raise InstallerError(f"{path} exists and is not a regular file")

    if current == content and not force:
        return FileInstallResult(path=path, action="unchanged")

    if dry_run:
        if not exists:
            action = "would create"
        elif current == content:
            action = "would rewrite"
        else:
            action = "would update"
        return FileInstallResult(path=path, action=action)

    path.write_text(content, encoding="utf-8")
    if not exists:
        action = "created"
    elif current == content:
        action = "rewritten"
    else:
        action = "updated"
    return FileInstallResult(path=path, action=action)


if __name__ == "__main__":
    raise SystemExit(main())
