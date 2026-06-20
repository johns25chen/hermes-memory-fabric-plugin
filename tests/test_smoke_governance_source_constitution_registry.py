from __future__ import annotations

from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_source_constitution_registry_smoke():
    completed = subprocess.run(
        [
            sys.executable,
            str(
                PROJECT_ROOT
                / "scripts"
                / "smoke_governance_source_constitution_registry.py"
            ),
        ],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=240,
    )

    assert completed.returncode == 0
    assert completed.stdout == "governance_source_constitution_registry=passed\n"
    assert completed.stderr == ""

