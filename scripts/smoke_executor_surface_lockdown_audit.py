#!/usr/bin/env python3
"""Deterministic local smoke for Executor Surface Lockdown Audit."""

from __future__ import annotations

import os
from pathlib import Path
from tempfile import TemporaryDirectory

from hermes_memory_fabric.memory_executor_surface_lockdown_audit import (
    audit_executor_surface_lockdown,
)


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]

    with TemporaryDirectory(prefix="executor-surface-lockdown-audit-") as temp_dir_name:
        temp_dir = Path(temp_dir_name)
        hermes_home = temp_dir / "hermes-home"
        old_hermes_home = os.environ.get("HERMES_HOME")
        os.environ["HERMES_HOME"] = str(hermes_home)
        try:
            before = _relative_files(hermes_home)
            report = audit_executor_surface_lockdown(repo_root)
            after = _relative_files(hermes_home)
        finally:
            if old_hermes_home is None:
                os.environ.pop("HERMES_HOME", None)
            else:
                os.environ["HERMES_HOME"] = old_hermes_home

    assert report["audit_status"] == "pass"
    assert report["provider_tools"] == []
    assert report["forbidden_files_present"] == []
    assert report["forbidden_calls"] == []
    assert report["forbidden_write_surfaces"] == []
    assert report["missing_no_write_flags"] == []
    assert report["v15_boundary_status"] == "pass"
    assert before == []
    assert after == []

    print("executor_surface_lockdown_audit_smoke=passed")
    return 0


def _relative_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(path.relative_to(root) for path in root.rglob("*") if path.is_file())


if __name__ == "__main__":
    raise SystemExit(main())
