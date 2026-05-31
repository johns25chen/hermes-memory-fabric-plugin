#!/usr/bin/env python3
"""Deterministic local smoke for Approval Token Issuance Dry Run."""

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
from hermes_memory_fabric.memory_approval_token_issuance_dry_run import (
    run_memory_approval_token_issuance_dry_run,
)
from hermes_memory_fabric.memory_candidate_proposal_dry_run import run_memory_candidate_proposal_dry_run


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    summary_text = _summary()

    with TemporaryDirectory(prefix="approval-token-issuance-dry-run-") as temp_dir_name:
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
            review = run_memory_approval_intent_review_gate_dry_run(
                intent,
                "approve",
                "smoke approval",
            )
            result = run_memory_approval_token_issuance_dry_run(
                review,
                issuance_reason="smoke token draft",
            )
            after = _relative_files(hermes_home)
        finally:
            if old_hermes_home is None:
                os.environ.pop("HERMES_HOME", None)
            else:
                os.environ["HERMES_HOME"] = old_hermes_home

    assert candidate_jsonl_path.name == "candidates.jsonl"
    assert preview["version"] == "1.5.0"
    assert intent["approval_intent_status"] == "ready"
    assert review["review_gate_status"] == "approved"
    assert result["token_issuance_status"] == "ready"
    assert result["approval_token_issued"] is False
    assert result["approval_token_id"] is None
    assert result["approval_token_value"] is None
    assert result["creates_usable_token"] is False
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

    print("approval_token_issuance_dry_run_smoke=passed")
    return 0


def _summary() -> str:
    return """# v1.9.0 Approval Token Issuance Dry Run

Goal / Purpose
Convert an approved v1.8 approval-intent review outcome into a token issuance dry-run candidate.

Included / Changed files
- src/hermes_memory_fabric/memory_approval_token_issuance_dry_run.py
- scripts/issue_approval_token_dry_run.py
- scripts/smoke_approval_token_issuance_dry_run.py

Validation
- focused pytest
- smoke_approval_token_issuance_dry_run.py

Boundary
- Dry-run token issuance candidate only.
- No usable token.
- No token file.
- No proposal creation.
- No operation ledger append.
- No executor invocation.
- No memory write.

Version
1.9.0

Result
Generated local approval token issuance dry-run candidates.
"""


def _relative_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(path.relative_to(root) for path in root.rglob("*") if path.is_file())


if __name__ == "__main__":
    raise SystemExit(main())
