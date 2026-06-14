from __future__ import annotations

from pathlib import Path
import subprocess
import sys


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "scripts"
    / "smoke_event_driven_governance_kernel.py"
)


def test_smoke_event_driven_governance_kernel():
    completed = subprocess.run(
        [sys.executable, str(SCRIPT)],
        check=False,
        capture_output=True,
        text=True,
        timeout=10,
    )

    assert completed.returncode == 0
    assert completed.stdout == "event_driven_governance_kernel=passed\n"
    assert completed.stderr == ""
