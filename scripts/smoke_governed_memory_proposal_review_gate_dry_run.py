#!/usr/bin/env python3
"""Smoke test for the v2.5.0 governed memory proposal review-gate dry run."""

from __future__ import annotations

from pathlib import Path
import sys

REPO_SRC = Path(__file__).resolve().parents[1] / "src"
if REPO_SRC.is_dir():
    sys.path.insert(0, str(REPO_SRC))

from hermes_memory_fabric.governed_memory_proposal_review_gate_dry_run import (
    run_governed_memory_proposal_review_gate_dry_run,
)


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    proposal_path = repo_root / "docs" / "CIVILIZATION_CORE_VIDEO_AI_SKILLS_MEMORY_PROPOSAL.md"
    result = run_governed_memory_proposal_review_gate_dry_run(proposal_path)

    assert result["version"] == "2.5.0"
    assert result["review_gate_status"] == "ready"
    assert result["pack_version"] == "2.4.0"
    assert result["pack_status"] == "ready"
    assert result["entry_count"] > 0
    assert result["decision_count"] == result["entry_count"]
    assert result["approve_candidate_count"] > 0
    assert result["reject_locked_count"] > 0
    assert result["risk_note_only_count"] > 0
    assert result["defer_for_human_review_count"] == 0
    assert result["writes_memory"] is False
    assert result["writes_graph"] is False
    assert result["writes_operation_ledger"] is False
    assert result["provider_tools"] == []
    assert result["issues_approval_token"] is False
    assert result["approval_token_issued"] is False
    assert result["approval_token_value"] is None
    assert result["creates_usable_token"] is False

    print("governed_memory_proposal_review_gate_dry_run=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
