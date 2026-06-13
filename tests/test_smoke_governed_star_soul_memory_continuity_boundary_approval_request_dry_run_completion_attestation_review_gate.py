from __future__ import annotations

from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    PROJECT_ROOT
    / "scripts"
    / "smoke_governed_star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_review_gate.py"
)


def test_smoke_governed_star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_review_gate():
    completed = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert (
        completed.stdout
        == "governed_star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_review_gate=passed\n"
    )
    assert completed.stderr == ""
