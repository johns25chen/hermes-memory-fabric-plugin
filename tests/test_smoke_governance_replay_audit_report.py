from __future__ import annotations

from pathlib import Path
import subprocess
import sys


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "scripts"
    / "smoke_governance_replay_audit_report.py"
)


def test_smoke_governance_replay_audit_report():
    completed = subprocess.run(
        [sys.executable, str(SCRIPT)],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert completed.stdout == "governance_replay_audit_report=passed\n"
    assert completed.stderr == ""
