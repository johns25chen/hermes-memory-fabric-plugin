from __future__ import annotations

from pathlib import Path
import subprocess
import sys


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "scripts"
    / "smoke_governance_transition_policy_registry.py"
)


def test_smoke_governance_transition_policy_registry():
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
        == "governance_transition_policy_registry=passed\n"
    )
    assert completed.stderr == ""
