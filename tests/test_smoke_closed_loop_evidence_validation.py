from __future__ import annotations

from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_smoke_closed_loop_evidence_validation_script_exits_zero():
    completed = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "scripts" / "smoke_closed_loop_evidence_validation.py")],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert completed.stdout == "closed_loop_evidence_validation=passed\n"
    assert completed.stderr == ""
