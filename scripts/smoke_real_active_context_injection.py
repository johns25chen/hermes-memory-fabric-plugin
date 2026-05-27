#!/usr/bin/env python3
"""Deterministic local smoke for the real active context injection contract."""

from __future__ import annotations

from hermes_memory_fabric import MemoryFabricProvider


def _candidate(memory_id: str, **overrides):
    base = {
        "id": memory_id,
        "content": "Hermes real active context injection smoke selected context.",
        "project_id": "hermes-memory-fabric",
        "entity_ids": ["hermes-memory-fabric"],
        "created_at": "2026-05-27T00:00:00Z",
        "source_id": memory_id,
        "source": "smoke",
        "provenance": f"smoke:real-active-context:{memory_id}",
        "risk_level": "low",
        "governance": {"read_only": True, "proposal_governed": True},
    }
    base.update(overrides)
    return base


def main() -> int:
    provider = MemoryFabricProvider(
        runtime_memory_candidates=[
            _candidate("selected"),
            _candidate(
                "unrelated",
                content="Lovart unrelated smoke context must not appear.",
                project_id="lovart",
                entity_ids=["lovart"],
            ),
            _candidate(
                "rejected",
                content="Rejected write-capable smoke context must not appear.",
                governance={"read_only": True, "would_write_memory": True},
            ),
        ],
        runtime_config={
            "project_scope": "hermes-memory-fabric",
            "memory_limit": 3,
            "context_budget_chars": 800,
        },
    )

    context = provider.prefetch("Hermes real active context injection smoke selected context")

    assert "smoke selected context" in context
    assert "Lovart unrelated smoke context" not in context
    assert "Rejected write-capable smoke context" not in context
    assert provider.get_tool_schemas() == []
    print("real_active_context_injection_smoke=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
