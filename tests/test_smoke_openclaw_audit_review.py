from __future__ import annotations

from pathlib import Path
import subprocess
import sys

from hermes_memory_fabric.openclaw_audit_review import build_openclaw_audit_review


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_smoke_openclaw_audit_review_script_exits_zero():
    completed = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "scripts" / "smoke_openclaw_audit_review.py")],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert completed.stdout == "openclaw_audit_review=passed\n"
    assert completed.stderr == ""


def test_openclaw_audit_review_missing_log_safety_contract(tmp_path):
    result = build_openclaw_audit_review(repo_root=tmp_path)

    assert result["status"] == "missing_audit_log"
    assert result["read_only"] is True
    assert result["read_only_memory"] is True
    assert result["would_mutate_memory"] is False
    assert result["invokes_openclaw"] is False
    assert result["writes_files"] is False
    assert result["entries"] == []
