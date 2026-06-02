#!/usr/bin/env python3
"""Smoke test for the v2.4.0 governed memory proposal pack dry run."""

from __future__ import annotations

from pathlib import Path
import sys

REPO_SRC = Path(__file__).resolve().parents[1] / "src"
if REPO_SRC.is_dir():
    sys.path.insert(0, str(REPO_SRC))

from hermes_memory_fabric.governed_memory_proposal_pack_dry_run import (
    build_governed_memory_proposal_pack_dry_run,
)


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    proposal_path = repo_root / "docs" / "CIVILIZATION_CORE_VIDEO_AI_SKILLS_MEMORY_PROPOSAL.md"
    result = build_governed_memory_proposal_pack_dry_run(proposal_path)

    assert result["pack_status"] == "ready"
    assert result["entry_count"] > 0
    assert result["proposed_count"] > 0
    assert result["rejected_count"] > 0
    assert result["risk_note_count"] > 0
    assert result["writes_memory"] is False
    assert result["writes_graph"] is False
    assert result["writes_operation_ledger"] is False
    assert result["provider_tools"] == []

    print("governed_memory_proposal_pack_dry_run=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
