#!/usr/bin/env python3
"""Smoke test for the local Skill Fabric GitHub archive simulation."""

from __future__ import annotations

from pathlib import Path
import sys
import tempfile

REPO_SRC = Path(__file__).resolve().parents[1] / "src"
if REPO_SRC.is_dir():
    sys.path.insert(0, str(REPO_SRC))

from hermes_memory_fabric.skill_fabric_simulation import run_skill_fabric_github_archive_simulation


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="skill-fabric-simulation-smoke-") as directory:
        result = run_skill_fabric_github_archive_simulation(Path(directory))
    if result["simulation_status"] != "pass":
        print(f"skill_fabric_github_archive_simulation=failed", file=sys.stderr)
        return 1
    print("skill_fabric_github_archive_simulation=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
