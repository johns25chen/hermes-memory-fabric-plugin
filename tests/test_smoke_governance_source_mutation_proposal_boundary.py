from __future__ import annotations

import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_source_mutation_proposal_boundary_smoke_stdout_contract():
    completed = subprocess.run(
        [
            sys.executable,
            str(
                PROJECT_ROOT
                / "scripts"
                / "smoke_governance_source_mutation_proposal_boundary.py"
            ),
        ],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=480,
    )

    assert completed.returncode == 0
    assert completed.stdout == (
        "governance_source_mutation_proposal_boundary=passed\n"
    )
    assert completed.stderr == ""
