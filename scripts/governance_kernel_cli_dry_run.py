#!/usr/bin/env python3
"""Run the local governance kernel CLI dry-run facade from a checkout."""

from __future__ import annotations

from pathlib import Path
import sys

REPO_SRC = Path(__file__).resolve().parents[1] / "src"
if REPO_SRC.is_dir():
    sys.path.insert(0, str(REPO_SRC))

from hermes_memory_fabric.governance_kernel_cli_dry_run import main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main())
