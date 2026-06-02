#!/usr/bin/env python3
"""Smoke test for the v2.6.0 governed memory approval-request dry run."""

from __future__ import annotations

from pathlib import Path
import sys

REPO_SRC = Path(__file__).resolve().parents[1] / "src"
if REPO_SRC.is_dir():
    sys.path.insert(0, str(REPO_SRC))

from hermes_memory_fabric.governed_memory_approval_request_dry_run import (
    build_governed_memory_approval_request_dry_run,
)


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    proposal_path = repo_root / "docs" / "CIVILIZATION_CORE_VIDEO_AI_SKILLS_MEMORY_PROPOSAL.md"
    result = build_governed_memory_approval_request_dry_run(proposal_path)

    assert result["version"] == "2.6.0"
    assert result["approval_request_status"] == "ready"
    assert result["review_gate_version"] == "2.5.0"
    assert result["review_gate_status"] == "ready"
    assert result["approval_request_count"] == 15
    assert result["blocked_decision_count"] == 3
    assert result["approval_request_count"] == result["approve_candidate_count"]
    assert result["writes_memory"] is False
    assert result["writes_graph"] is False
    assert result["writes_operation_ledger"] is False
    assert result["writes_config"] is False
    assert result["writes_sqlite"] is False
    assert result["provider_tools"] == []
    assert result["issues_approval_token"] is False
    assert result["approval_token_issued"] is False
    assert result["approval_token_value"] is None
    assert result["creates_usable_token"] is False

    print("governed_memory_approval_request_dry_run=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
