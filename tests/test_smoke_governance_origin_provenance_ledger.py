from __future__ import annotations

import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_smoke_governance_origin_provenance_ledger_exits_zero():
    completed = subprocess.run(
        [
            sys.executable,
            str(
                PROJECT_ROOT
                / "scripts"
                / "smoke_governance_origin_provenance_ledger.py"
            ),
        ],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=180,
    )

    assert completed.returncode == 0
    assert completed.stdout == "governance_origin_provenance_ledger=passed\n"
    assert completed.stderr == ""
