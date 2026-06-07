from __future__ import annotations

from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_review_gate_exits_zero():
    completed = subprocess.run(
        [
            sys.executable,
            str(
                PROJECT_ROOT
                / "scripts"
                / "smoke_governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_review_gate.py"
            ),
        ],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert (
        completed.stdout
        == "governed_star_law_candidate_rule_violation_response_audit_completion_attestation_completion_boundary_review_gate=passed\n"
    )
    assert completed.stderr == ""
