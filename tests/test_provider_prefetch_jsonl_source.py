from __future__ import annotations

import json
from pathlib import Path

from hermes_memory_fabric import MemoryFabricProvider


FIXTURE_PATH = (
    Path(__file__).resolve().parents[1]
    / "benchmarks"
    / "persistent_candidate_retrieval"
    / "fixtures"
    / "v11_candidates.jsonl"
)
ADMISSION_SCOPE = {
    "project": "hermes-memory-fabric",
    "workspace": "/workspace/hermes-memory-fabric",
    "namespace": "memory",
}
JSONL_SOURCE = {
    "provider_id": "configured-jsonl",
    "source_class": "LOCAL_PROVIDER",
    "source_instance": "provider:jsonl",
}
RUNTIME_SOURCE = {
    "provider_id": "runtime-local-caller",
    "source_class": "LOCAL_CALLER",
    "source_instance": "provider:runtime",
}
PROVIDER_REGISTRY = {
    "configured-jsonl": {
        "enabled": True,
        "source_classes": ["LOCAL_PROVIDER"],
        "capabilities": ["READ_CANDIDATE"],
        "review_only": False,
        "trusted_ingestion": True,
    },
    "runtime-local-caller": {
        "enabled": True,
        "source_classes": ["LOCAL_CALLER"],
        "capabilities": ["READ_CANDIDATE"],
        "review_only": False,
        "trusted_ingestion": True,
    },
}


def _candidate(memory_id: str, **overrides):
    base = {
        "id": memory_id,
        "content": "Hermes runtime JSONL override candidate source selected context.",
        "project_id": "hermes-memory-fabric",
        "entity_ids": ["hermes-memory-fabric"],
        "created_at": "2026-05-27T00:00:00Z",
        "source_id": memory_id,
        "source": "test",
        "provenance": f"test:provider-jsonl:{memory_id}",
        "risk_level": "low",
        "governance": {"read_only": True, "proposal_governed": True},
    }
    base.update(overrides)
    return base


def _provider(*, runtime_candidates=None, runtime_config=None, **runtime_config_overrides):
    config = {
        "project_scope": "hermes-memory-fabric",
        "candidate_jsonl_path": str(FIXTURE_PATH),
        "candidate_jsonl_required_fields": ["id", "content"],
        "memory_limit": 5,
        "context_budget_chars": 1600,
        "admission_scope": ADMISSION_SCOPE,
        "provider_registry_snapshot": PROVIDER_REGISTRY,
        "candidate_jsonl_source": JSONL_SOURCE,
        "runtime_candidate_source": RUNTIME_SOURCE,
    }
    if runtime_config:
        config.update(runtime_config)
    config.update(runtime_config_overrides)
    return MemoryFabricProvider(
        runtime_memory_candidates=runtime_candidates,
        runtime_config=config,
    )


def test_provider_prefetch_reads_configured_jsonl_and_returns_selected_context():
    provider = _provider()

    result = provider.prefetch("Hermes v1.1 JSONL candidate source selected project memory")

    assert "selected project memory proves bounded read-only candidate loading" in result
    assert provider.get_tool_schemas() == []


def test_unrelated_jsonl_memory_is_excluded():
    provider = _provider()

    result = provider.prefetch("Hermes v1.1 JSONL candidate source selected project memory")

    assert "Lovart JSONL candidate source unrelated project memory" not in result


def test_archived_jsonl_memory_is_rejected_by_default():
    provider = _provider()

    result = provider.prefetch("Archived JSONL candidate source memory must stay out by default")

    assert "Archived JSONL candidate source memory must stay out by default" not in result


def test_high_risk_jsonl_memory_rejected_unless_runtime_config_allows_it():
    blocked = _provider()
    allowed = _provider(allowed_risk_levels=["low", "medium", "high"])

    blocked_result = blocked.prefetch("High risk JSONL candidate source memory may appear only when explicitly allowed")
    allowed_result = allowed.prefetch("High risk JSONL candidate source memory may appear only when explicitly allowed")

    assert "High risk JSONL candidate source memory" not in blocked_result
    assert "High risk JSONL candidate source memory" in allowed_result


def test_same_bare_id_from_runtime_and_jsonl_remains_distinct_by_compound_identity():
    provider = _provider(
        runtime_candidates=[
            _candidate(
                "v11-selected-project",
                content="Runtime override JSONL candidate source should win over fixture content.",
                source_id="runtime-override",
            )
        ]
    )

    result = provider.prefetch("Runtime override JSONL candidate source should win")

    assert "Runtime override JSONL candidate source should win over fixture content" in result
    assert "selected project memory proves bounded read-only candidate loading" in result


def test_provider_get_tool_schemas_remains_empty_with_jsonl_source():
    provider = _provider()

    assert provider.get_tool_schemas() == []


def test_provider_prefetch_writes_no_files_under_temp_hermes_home_or_candidate_directory(tmp_path, monkeypatch):
    hermes_home = tmp_path / "hermes-home"
    candidate_dir = tmp_path / "candidate-dir"
    candidate_dir.mkdir()
    candidate_path = candidate_dir / "candidates.jsonl"
    candidate_path.write_text(
        json.dumps(
            {
                "id": "selected",
                "content": "Hermes temp JSONL candidate source selected context.",
                "project_id": "hermes-memory-fabric",
                "entity_ids": ["hermes-memory-fabric"],
                "created_at": "2026-05-27T00:00:00Z",
                "source_id": "selected",
                "source": "test",
                "provenance": "test:provider-jsonl:no-writes",
                "risk_level": "low",
                "governance": {"read_only": True, "proposal_governed": True},
            },
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("HERMES_HOME", str(hermes_home))
    provider = MemoryFabricProvider(
        runtime_config={
            "project_scope": "hermes-memory-fabric",
            "candidate_jsonl_path": str(candidate_path),
            "memory_limit": 3,
            "context_budget_chars": 800,
            "admission_scope": ADMISSION_SCOPE,
            "provider_registry_snapshot": PROVIDER_REGISTRY,
            "candidate_jsonl_source": JSONL_SOURCE,
        }
    )
    provider.initialize("session-jsonl-no-writes", hermes_home=str(hermes_home))

    before = sorted(path.relative_to(tmp_path) for path in tmp_path.rglob("*"))
    result = provider.prefetch("Hermes temp JSONL candidate source selected context")
    after = sorted(path.relative_to(tmp_path) for path in tmp_path.rglob("*"))

    assert "Hermes temp JSONL candidate source selected context" in result
    assert after == before


def test_jsonl_candidates_without_admission_configuration_fail_closed(tmp_path):
    candidate_path = tmp_path / "untrusted.jsonl"
    candidate_path.write_text(
        json.dumps({"id": "untrusted", "content": "SECRET UNTRUSTED JSONL"}) + "\n",
        encoding="utf-8",
    )
    provider = MemoryFabricProvider(
        runtime_config={
            "project_scope": "hermes-memory-fabric",
            "candidate_jsonl_path": str(candidate_path),
        }
    )

    assert provider.prefetch("SECRET UNTRUSTED JSONL") == ""
