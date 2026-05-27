from __future__ import annotations

from copy import deepcopy

import pytest

from hermes_memory_fabric import MemoryFabricProvider


def _candidate(memory_id: str, **overrides):
    base = {
        "id": memory_id,
        "content": "Hermes real active context injection contract selects this memory.",
        "project_id": "hermes-memory-fabric",
        "entity_ids": ["hermes-memory-fabric"],
        "created_at": "2026-05-27T00:00:00Z",
        "source_id": memory_id,
        "source": "test",
        "provenance": f"test:prefetch:{memory_id}",
        "risk_level": "low",
        "governance": {"read_only": True, "proposal_governed": True},
    }
    base.update(overrides)
    return base


def _provider(*, candidates=None, runtime_config=None, **runtime_config_overrides):
    config = {"project_scope": "hermes-memory-fabric"}
    if runtime_config:
        config.update(runtime_config)
    config.update(runtime_config_overrides)
    return MemoryFabricProvider(runtime_memory_candidates=candidates, runtime_config=config)


def test_prefetch_returns_empty_string_with_no_candidates():
    provider = _provider()

    assert provider.prefetch("Hermes real active context injection") == ""


def test_prefetch_returns_compact_context_text_with_matching_runtime_candidates():
    provider = _provider(
        candidates=[
            _candidate(
                "selected",
                content="Hermes real active context injection selected runtime candidate.",
            )
        ]
    )

    result = provider.prefetch("Hermes real active context injection selected runtime candidate")

    assert result
    assert "selected runtime candidate" in result
    assert result == provider.prefetch("Hermes real active context injection selected runtime candidate")


def test_prefetch_excludes_unrelated_and_rejected_memory_content():
    provider = _provider(
        candidates=[
            _candidate("selected", content="Hermes injection selected provider context."),
            _candidate(
                "unrelated",
                content="Lovart unrelated project context must not appear.",
                project_id="lovart",
                entity_ids=["lovart"],
            ),
            _candidate(
                "rejected",
                content="Unsafe rejected write instruction must not appear.",
                governance={"read_only": True, "would_write_memory": True},
            ),
        ],
        memory_limit=3,
    )

    result = provider.prefetch("Hermes injection selected provider context")

    assert "Hermes injection selected provider context" in result
    assert "Lovart unrelated project context" not in result
    assert "Unsafe rejected write instruction" not in result


def test_prefetch_respects_context_budget_chars():
    provider = _provider(
        candidates=[
            _candidate("a", content="Hermes injection short selected memory.", source_id="a"),
            _candidate(
                "b",
                content="Hermes injection second selected memory that should not fit the active context budget.",
                source_id="b",
            ),
        ],
        memory_limit=2,
        context_budget_chars=60,
    )

    result = provider.prefetch("Hermes injection selected memory active context budget")

    assert "short selected memory" in result
    assert "second selected memory" not in result
    assert len(result) <= 60


def test_prefetch_rejects_archived_memory_by_default():
    provider = _provider(
        candidates=[
            _candidate(
                "archived",
                content="Archived Hermes injection context must stay out by default.",
                lifecycle_status="archived",
            )
        ]
    )

    assert provider.prefetch("Archived Hermes injection context") == ""


def test_prefetch_allows_high_risk_memory_only_when_runtime_config_allows_it():
    high_risk = _candidate(
        "high-risk",
        content="Hermes high risk active context may appear only when explicitly allowed.",
        risk_level="high",
    )
    blocked = _provider(candidates=[high_risk])
    allowed = _provider(candidates=[high_risk], allowed_risk_levels=["low", "medium", "high"])

    assert blocked.prefetch("Hermes high risk active context explicitly allowed") == ""
    assert "high risk active context" in allowed.prefetch("Hermes high risk active context explicitly allowed")


def test_prefetch_failure_returns_empty_string_and_does_not_raise(monkeypatch):
    provider = _provider(candidates=[_candidate("selected")])

    def fail(*args, **kwargs):
        raise RuntimeError("boom")

    monkeypatch.setattr(provider, "build_active_context", fail)

    assert provider.prefetch("Hermes injection") == ""


def test_runtime_candidates_are_defensively_copied():
    candidates = [
        _candidate(
            "selected",
            content="Hermes defensive copy active context remains original.",
            governance={"read_only": True, "proposal_governed": True, "nested": {"safe": True}},
        )
    ]
    original_candidates = deepcopy(candidates)
    provider = _provider(candidates=candidates)

    candidates[0]["content"] = "MUTATED CONTENT MUST NOT APPEAR"
    candidates[0]["governance"]["nested"]["safe"] = False

    result = provider.prefetch("Hermes defensive copy active context original")

    assert "remains original" in result
    assert "MUTATED CONTENT MUST NOT APPEAR" not in result
    assert provider._runtime_memory_candidates == original_candidates
    assert provider._runtime_memory_candidates[0] is not candidates[0]
    assert provider._runtime_memory_candidates[0]["governance"] is not candidates[0]["governance"]


def test_provider_get_tool_schemas_remains_empty():
    provider = _provider(candidates=[_candidate("selected")])

    assert provider.get_tool_schemas() == []


def test_prefetch_writes_no_files_to_temp_hermes_home_or_temp_directory(tmp_path, monkeypatch):
    hermes_home = tmp_path / "hermes-home"
    scratch = tmp_path / "scratch"
    monkeypatch.setenv("HERMES_HOME", str(hermes_home))
    monkeypatch.setenv("TMPDIR", str(scratch))
    provider = _provider(candidates=[_candidate("selected")])
    provider.initialize("session-no-writes", hermes_home=str(hermes_home))

    before = sorted(path.relative_to(tmp_path) for path in tmp_path.rglob("*"))
    result = provider.prefetch("Hermes real active context injection contract")
    after = sorted(path.relative_to(tmp_path) for path in tmp_path.rglob("*"))

    assert "real active context injection contract" in result
    assert after == before == []
