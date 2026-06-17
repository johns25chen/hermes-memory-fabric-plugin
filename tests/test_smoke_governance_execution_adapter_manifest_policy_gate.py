from __future__ import annotations

from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_smoke_governance_execution_adapter_manifest_policy_gate():
    completed = subprocess.run(
        [
            sys.executable,
            str(
                PROJECT_ROOT
                / "scripts"
                / "smoke_governance_execution_adapter_manifest_policy_gate.py"
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
        == "governance_execution_adapter_manifest_policy_gate=passed\n"
    )
    assert completed.stderr == ""
