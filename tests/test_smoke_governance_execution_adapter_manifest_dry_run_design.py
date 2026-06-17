from __future__ import annotations

from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SMOKE_SCRIPT = (
    PROJECT_ROOT
    / "scripts"
    / "smoke_governance_execution_adapter_manifest_dry_run_design.py"
)


def test_smoke_governance_execution_adapter_manifest_dry_run_design():
    completed = subprocess.run(
        [sys.executable, str(SMOKE_SCRIPT)],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert (
        completed.stdout
        == "governance_execution_adapter_manifest_dry_run_design=passed\n"
    )
    assert completed.stderr == ""
