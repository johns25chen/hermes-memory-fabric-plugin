from __future__ import annotations

from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_smoke_governed_star_law_design_boundary_proposal():
    completed = subprocess.run(
        [
            sys.executable,
            str(
                PROJECT_ROOT
                / "scripts"
                / "smoke_governed_star_law_design_boundary_proposal.py"
            ),
        ],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert completed.stdout == "governed_star_law_design_boundary_proposal=passed\n"
    assert completed.stderr == ""
