from __future__ import annotations

from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_civilization_core_stability_index_smoke_script_exits_zero():
    completed = subprocess.run(
        [
            sys.executable,
            str(PROJECT_ROOT / "scripts" / "smoke_governance_civilization_core_stability_index.py"),
        ],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert completed.stdout == "governance_civilization_core_stability_index=passed\n"
    assert completed.stderr == ""
