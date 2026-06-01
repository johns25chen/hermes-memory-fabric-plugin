#!/usr/bin/env python3
"""Smoke test for the local release integrity audit."""

from __future__ import annotations

from pathlib import Path
import sys

REPO_SRC = Path(__file__).resolve().parents[1] / "src"
if REPO_SRC.is_dir():
    sys.path.insert(0, str(REPO_SRC))

from hermes_memory_fabric.release_integrity_audit import run_release_integrity_audit


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    result = run_release_integrity_audit(repo_root)
    if result["audit_status"] != "pass":
        print("release_integrity_audit=failed", file=sys.stderr)
        return 1
    print("release_integrity_audit=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
