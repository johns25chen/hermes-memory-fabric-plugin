#!/usr/bin/env python3
"""Deterministic local smoke for Codex task summary ingestion dry-run."""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

from hermes_memory_fabric import MemoryFabricProvider
from hermes_memory_fabric.candidate_jsonl_source import load_candidate_jsonl_source
from hermes_memory_fabric.codex_task_summary_ingestion import (
    generate_codex_task_summary_candidates,
    write_candidates_jsonl,
)


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    fixture_path = repo_root / "benchmarks" / "candidate_ingestion" / "fixtures" / "v13_codex_task_summary.txt"
    fixture_text = fixture_path.read_text(encoding="utf-8")

    candidates = generate_codex_task_summary_candidates(fixture_text)
    candidate_kinds = {tag for candidate in candidates for tag in candidate.get("tags", [])}

    assert len(candidates) >= 3
    assert "capability" in candidate_kinds
    assert "validation" in candidate_kinds
    assert "boundary" in candidate_kinds
    assert all(candidate["governance"]["read_only"] is True for candidate in candidates)
    assert all(candidate["governance"]["proposal_governed"] is True for candidate in candidates)
    assert all(candidate["governance"]["dry_run"] is True for candidate in candidates)

    provider = MemoryFabricProvider()
    assert provider.get_tool_schemas() == []

    with TemporaryDirectory(prefix="codex-task-summary-ingestion-") as temp_dir_name:
        temp_dir = Path(temp_dir_name)
        output_path = temp_dir / "candidates.jsonl"
        before = sorted(path.relative_to(temp_dir) for path in temp_dir.rglob("*"))
        write_candidates_jsonl(candidates, output_path)
        after = sorted(path.relative_to(temp_dir) for path in temp_dir.rglob("*"))
        assert before == []
        assert after == [Path("candidates.jsonl")]

        loaded = load_candidate_jsonl_source(output_path, required_fields=["id", "content"])
        assert len(loaded) == len(candidates)

        provider = MemoryFabricProvider(
            runtime_config={
                "project_scope": "hermes-memory-fabric",
                "candidate_jsonl_path": str(output_path),
                "candidate_jsonl_required_fields": ["id", "content"],
                "memory_limit": 5,
                "context_budget_chars": 2000,
            }
        )
        context = provider.prefetch("bounded read-only memory candidates from candidate_jsonl_path")
        assert "bounded read-only memory candidates" in context
        assert provider.get_tool_schemas() == []

    print("codex_task_summary_ingestion_smoke=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
