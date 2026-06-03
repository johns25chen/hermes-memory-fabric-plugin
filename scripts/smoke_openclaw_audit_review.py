#!/usr/bin/env python3
"""Smoke test for the read-only OpenClaw audit review."""

from __future__ import annotations

from pathlib import Path
import sys
import tempfile

REPO_SRC = Path(__file__).resolve().parents[1] / "src"
if REPO_SRC.is_dir():
    sys.path.insert(0, str(REPO_SRC))

from hermes_memory_fabric.openclaw_audit_review import build_openclaw_audit_review


EXPECTED_RESULT = {
    "status": "missing_audit_log",
    "read_only": True,
    "read_only_memory": True,
    "would_mutate_memory": False,
    "invokes_openclaw": False,
    "writes_files": False,
    "entries": [],
}


def main() -> int:
    try:
        with tempfile.TemporaryDirectory(prefix="openclaw-audit-review-smoke-") as directory:
            result = build_openclaw_audit_review(repo_root=Path(directory))

        for key, expected in EXPECTED_RESULT.items():
            if result.get(key) != expected:
                print(f"openclaw_audit_review=failed {key}", file=sys.stderr)
                return 1
    except Exception as exc:
        print(f"openclaw_audit_review=failed {type(exc).__name__}", file=sys.stderr)
        return 1

    print("openclaw_audit_review=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
