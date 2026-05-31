#!/usr/bin/env python3
"""Deterministic local smoke for Approval Intent Review Gate Dry Run."""

from __future__ import annotations

import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory

from hermes_memory_fabric.codex_task_summary_ingestion import (
    candidates_to_jsonl,
    generate_codex_task_summary_candidates,
)
from hermes_memory_fabric.memory_approval_intent_dry_run import run_memory_approval_intent_dry_run
from hermes_memory_fabric.memory_approval_intent_review_gate_dry_run import (
    run_memory_approval_intent_review_gate_dry_run,
)
from hermes_memory_fabric.memory_candidate_proposal_dry_run import run_memory_candidate_proposal_dry_run


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    fixture_path = repo_root / "benchmarks" / "candidate_ingestion" / "fixtures" / "v13_codex_task_summary.txt"
    summary_text = fixture_path.read_text(encoding="utf-8")

    with TemporaryDirectory(prefix="approval-intent-review-gate-dry-run-") as temp_dir_name:
        temp_dir = Path(temp_dir_name)
        hermes_home = temp_dir / "hermes-home"
        candidate_jsonl_path = temp_dir / "candidates.jsonl"
        old_hermes_home = os.environ.get("HERMES_HOME")
        os.environ["HERMES_HOME"] = str(hermes_home)
        try:
            before = _relative_files(hermes_home)
            candidates = generate_codex_task_summary_candidates(summary_text)
            candidate_jsonl_path.write_text(candidates_to_jsonl(candidates), encoding="utf-8")
            loaded_candidates = [
                json.loads(line)
                for line in candidate_jsonl_path.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            preview = run_memory_candidate_proposal_dry_run(loaded_candidates)
            intent = run_memory_approval_intent_dry_run(preview, repo_root=repo_root)
            result = run_memory_approval_intent_review_gate_dry_run(
                intent,
                "approve",
                "smoke approval",
            )
            after = _relative_files(hermes_home)
        finally:
            if old_hermes_home is None:
                os.environ.pop("HERMES_HOME", None)
            else:
                os.environ["HERMES_HOME"] = old_hermes_home

    assert candidate_jsonl_path.name == "candidates.jsonl"
    assert intent["approval_intent_status"] == "ready"
    assert result["review_gate_status"] == "approved"
    assert result["reviewer_decision"] == "approve"
    assert result["approval_token_issued"] is False
    assert result["approval_token_id"] is None
    assert result["creates_real_proposal"] is False
    assert result["writes_proposal_files"] is False
    assert result["writes_operation_ledger"] is False
    assert result["writes_memory"] is False
    assert result["writes_graph"] is False
    assert result["writes_config"] is False
    assert result["writes_sqlite"] is False
    assert result["writes_token_files"] is False
    assert result["writes_approval_audit"] is False
    assert result["invokes_real_executor"] is False
    assert result["applies_proposals"] is False
    assert result["provider_tools"] == []
    assert before == []
    assert after == []

    print("approval_intent_review_gate_dry_run_smoke=passed")
    return 0


def _relative_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(path.relative_to(root) for path in root.rglob("*") if path.is_file())


if __name__ == "__main__":
    raise SystemExit(main())
