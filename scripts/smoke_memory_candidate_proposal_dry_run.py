#!/usr/bin/env python3
"""Deterministic local smoke for Memory Candidate Proposal Dry Run."""

from __future__ import annotations

import os
from pathlib import Path
from tempfile import TemporaryDirectory

from hermes_memory_fabric.codex_task_summary_ingestion import generate_codex_task_summary_candidates
from hermes_memory_fabric.memory_candidate_proposal_dry_run import run_memory_candidate_proposal_dry_run


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    fixture_path = repo_root / "benchmarks" / "candidate_ingestion" / "fixtures" / "v13_codex_task_summary.txt"
    summary_text = fixture_path.read_text(encoding="utf-8")

    candidates = generate_codex_task_summary_candidates(summary_text)

    with TemporaryDirectory(prefix="memory-candidate-proposal-dry-run-") as temp_dir_name:
        temp_dir = Path(temp_dir_name)
        hermes_home = temp_dir / "hermes-home"
        old_hermes_home = os.environ.get("HERMES_HOME")
        os.environ["HERMES_HOME"] = str(hermes_home)
        try:
            before = _relative_files(hermes_home)
            result = run_memory_candidate_proposal_dry_run(candidates)
            after = _relative_files(hermes_home)
        finally:
            if old_hermes_home is None:
                os.environ.pop("HERMES_HOME", None)
            else:
                os.environ["HERMES_HOME"] = old_hermes_home

    assert result["accepted_count"] >= 1
    assert result["created_real_proposal"] is False
    assert result["writes_proposal_files"] is False
    assert result["writes_operation_ledger"] is False
    assert result["writes_memory"] is False
    assert result["writes_graph"] is False
    assert result["writes_token_files"] is False
    assert result["writes_approval_audit"] is False
    assert result["provider_tools"] == []
    assert before == []
    assert after == []

    print("memory_candidate_proposal_dry_run_smoke=passed")
    return 0


def _relative_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(path.relative_to(root) for path in root.rglob("*") if path.is_file())


if __name__ == "__main__":
    raise SystemExit(main())
