from __future__ import annotations

from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_star_source_memory_entry_candidate_smoke():
    completed = subprocess.run(
        [
            sys.executable,
            str(
                PROJECT_ROOT
                / "scripts"
                / "smoke_governance_star_source_memory_entry_candidate.py"
            ),
        ],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=240,
    )

    assert completed.returncode == 0
    assert completed.stdout == (
        "governance_star_source_memory_entry_candidate=passed\n"
    )
    assert completed.stderr == ""
