from __future__ import annotations

from pathlib import Path
import subprocess
import sys


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "scripts"
    / "smoke_governed_star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_approval_request_dry_run_proposal.py"
)


def test_smoke_governed_star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_approval_request_dry_run_proposal():
    completed = subprocess.run(
        [sys.executable, str(SCRIPT)],
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )

    assert completed.returncode == 0
    assert (
        completed.stdout
        == "governed_star_soul_memory_continuity_boundary_approval_request_dry_run_completion_attestation_approval_request_dry_run_proposal=passed\n"
    )
    assert completed.stderr == ""
