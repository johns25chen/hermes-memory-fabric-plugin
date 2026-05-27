#!/usr/bin/env python3
"""Deterministic local smoke for the read-only JSONL candidate source."""

from __future__ import annotations

from pathlib import Path

from hermes_memory_fabric import MemoryFabricProvider


def main() -> int:
    repo_root = Path(__file__).resolve().parents[1]
    fixture_path = repo_root / "benchmarks" / "persistent_candidate_retrieval" / "fixtures" / "v11_candidates.jsonl"
    provider = MemoryFabricProvider(
        runtime_config={
            "project_scope": "hermes-memory-fabric",
            "candidate_jsonl_path": str(fixture_path),
            "candidate_jsonl_required_fields": ["id", "content"],
            "memory_limit": 5,
            "context_budget_chars": 1600,
        }
    )

    context = provider.prefetch("Hermes v1.1 JSONL candidate source selected project memory")
    provider_tools = provider.get_tool_schemas()

    assert "selected project memory proves bounded read-only candidate loading" in context
    assert "Lovart JSONL candidate source unrelated project memory" not in context
    assert "Archived JSONL candidate source memory" not in context
    assert provider_tools == []
    print("jsonl_candidate_source_smoke=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
