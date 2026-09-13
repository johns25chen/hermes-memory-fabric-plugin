from __future__ import annotations

import io
import json
import re
from copy import deepcopy
from pathlib import Path

import pytest

from hermes_memory_fabric import MemoryFabricProvider
from hermes_memory_fabric.candidate_jsonl_source import load_candidate_jsonl_source
from hermes_memory_fabric.codex_task_summary_ingestion import (
    DEFAULT_PROJECT_ID,
    candidates_to_jsonl,
    cli_main,
    detect_codex_task_summary_risk_level,
    generate_codex_task_summary_candidates,
    parse_codex_task_summary,
    write_candidates_jsonl,
)


def _summary() -> str:
    return """# v1.3.1 Codex Task Summary Ingestion Dry Run

Goal / Purpose
Implement Codex task summary ingestion dry run for Memory Fabric candidates.

Included / Changed files
- src/hermes_memory_fabric/codex_task_summary_ingestion.py
- scripts/ingest_codex_task_summary_dry_run.py

Validation
- PYTHONPATH="$PWD/src:$PWD" /Users/han/.hermes/hermes-agent/.venv/bin/python -m pytest -o addopts='' tests/test_codex_task_summary_ingestion.py -q
- PYTHONPATH="$PWD/src:$PWD" /Users/han/.hermes/hermes-agent/.venv/bin/python scripts/smoke_codex_task_summary_ingestion.py

Boundary
- Dry-run candidate generation only.
- No model calls.
- No network calls.
- No provider tools.

Version
1.3.1

Result
Generated JSONL candidates from explicit Codex task summary sections.
"""


def _candidate_by_kind(candidates, kind):
    return next(candidate for candidate in candidates if kind in candidate["tags"])


CODEX_ADMISSION_WORKSPACE = "/workspace/codex-task-summary-ingestion"
CODEX_ADMISSION_NAMESPACE = "codex-task-summary-ingestion"
CODEX_JSONL_SOURCE = {
    "provider_id": "codex-task-summary-jsonl",
    "source_class": "LOCAL_PROVIDER",
    "source_instance": "provider:codex-task-summary-jsonl",
}
CODEX_PROVIDER_REGISTRY = {
    "codex-task-summary-jsonl": {
        "enabled": True,
        "source_classes": ["LOCAL_PROVIDER"],
        "capabilities": ["READ_CANDIDATE"],
        "review_only": False,
        "trusted_ingestion": True,
    }
}


def _codex_provider_runtime_config(output_path, **overrides):
    config = {
        "project_scope": DEFAULT_PROJECT_ID,
        "candidate_jsonl_path": str(output_path),
        "candidate_jsonl_required_fields": ["id", "content"],
        "memory_limit": 5,
        "context_budget_chars": 2400,
        "admission_scope": {
            "project": DEFAULT_PROJECT_ID,
            "workspace": CODEX_ADMISSION_WORKSPACE,
            "namespace": CODEX_ADMISSION_NAMESPACE,
        },
        "candidate_jsonl_source": dict(CODEX_JSONL_SOURCE),
        "provider_registry_snapshot": deepcopy(CODEX_PROVIDER_REGISTRY),
    }
    config.update(overrides)
    return config


def test_parses_structured_sections():
    parsed = parse_codex_task_summary(_summary())

    keys = [section["key"] for section in parsed["sections"]]
    assert keys == ["goal", "changed_files", "validation", "boundary", "version", "result"]
    assert parsed["section_map"]["goal"][0]["content"].startswith("Implement Codex task summary ingestion")
    assert parsed["section_map"]["validation"][0]["line_start"] > parsed["section_map"]["goal"][0]["line_start"]


def test_emits_deterministic_candidate_ids():
    first = generate_codex_task_summary_candidates(_summary())
    second = generate_codex_task_summary_candidates(_summary())

    assert [candidate["id"] for candidate in first] == [candidate["id"] for candidate in second]
    assert candidates_to_jsonl(first) == candidates_to_jsonl(second)


def test_preserves_validation_evidence():
    candidates = generate_codex_task_summary_candidates(_summary())
    validation = _candidate_by_kind(candidates, "validation")

    assert "tests/test_codex_task_summary_ingestion.py -q" in validation["content"]
    assert "scripts/smoke_codex_task_summary_ingestion.py" in validation["content"]


def test_preserves_boundary_limitations():
    candidates = generate_codex_task_summary_candidates(_summary())
    boundary = _candidate_by_kind(candidates, "boundary")

    assert "Dry-run candidate generation only." in boundary["content"]
    assert "No model calls." in boundary["content"]
    assert "No network calls." in boundary["content"]
    assert "No provider tools." in boundary["content"]


def _v14_e2e_summary() -> str:
    return """# v1.4.0 Codex Task Summary Ingestion E2E

Goal / Purpose
Generate HERMES_V14_INGESTION_E2E_OK from a bounded Codex task summary fixture.

Validation
The answer token is exactly HERMES_V14_INGESTION_E2E_OK.

Boundary
- No token write.
- No approval audit write.
- No executor call.

Version
1.4.0

Result
HERMES_V14_INGESTION_E2E_OK confirms JSONL candidates can feed MemoryFabricProvider.prefetch.
"""


def test_defaults_to_low_risk_for_normal_summaries():
    candidates = generate_codex_task_summary_candidates(_summary())

    assert {candidate["risk_level"] for candidate in candidates} == {"low"}


def test_negative_safety_boundary_statements_remain_low_risk():
    statements = [
        "No token write.",
        "No approval audit write.",
        "No executor call.",
        "No model calls.",
        "No network calls.",
        "No durable memory write.",
        "Does not write token files.",
        "Do not call executor.",
        "Never deletes credentials.",
        "Without model calls or network calls.",
    ]

    assert {detect_codex_task_summary_risk_level(statement) for statement in statements} == {"low"}


def test_benign_validation_marker_token_statements_remain_low_risk():
    statements = [
        "The answer token is exactly HERMES_V14_INGESTION_E2E_OK.",
        "The E2E token is HERMES_V14_INGESTION_E2E_OK.",
        "Expected reply token: HERMES_V14_INGESTION_E2E_OK.",
        "Expected output token: HERMES_V14_INGESTION_E2E_OK.",
    ]

    assert {detect_codex_task_summary_risk_level(statement) for statement in statements} == {"low"}


def test_real_credential_token_contexts_remain_high_risk():
    statements = [
        "Store API token in a file.",
        "Writes auth token files.",
        "Creates bearer token.",
    ]

    assert {detect_codex_task_summary_risk_level(statement) for statement in statements} == {"high"}


def test_affirmative_dangerous_statements_still_high_risk():
    statements = [
        "Writes token files.",
        "Creates approval token.",
        "Runs executor.",
        "Deletes credentials.",
        "Migrates memory.",
        "Modifies auth config.",
        "Makes model calls.",
        "Calls the network.",
    ]

    assert {detect_codex_task_summary_risk_level(statement) for statement in statements} == {"high"}


def test_mixed_summary_with_only_negative_boundaries_remains_low_risk():
    text = """Goal / Purpose
Keep Codex task summary ingestion bounded and deterministic.

Boundary
- No token write.
- No approval audit write.
- No executor call.
- No model calls.
- No network calls.
- No durable memory write.

Result
Generated local JSONL candidates from explicit summary text.
"""

    candidates = generate_codex_task_summary_candidates(text)

    assert {candidate["risk_level"] for candidate in candidates} == {"low"}


def test_escalates_risk_when_high_risk_terms_appear():
    text = """Goal
Review auth token credential handling and executor migration approval deletion behavior.

Result
Captured the risky terms in an explicit summary section.
"""

    candidates = generate_codex_task_summary_candidates(text)

    assert _candidate_by_kind(candidates, "capability")["risk_level"] == "high"


def test_v14_style_e2e_summary_low_risk_and_prefetchable_with_default_risk_gate(tmp_path):
    candidates = generate_codex_task_summary_candidates(_v14_e2e_summary())
    original_candidates = deepcopy(candidates)
    output_path = tmp_path / "v14-e2e-candidates.jsonl"

    assert {candidate["risk_level"] for candidate in candidates} == {"low"}

    write_candidates_jsonl(candidates, output_path)
    runtime_config = _codex_provider_runtime_config(output_path)
    assert "allowed_risk_levels" not in runtime_config
    provider = MemoryFabricProvider(runtime_config=runtime_config)

    context = provider.prefetch("HERMES_V14_INGESTION_E2E_OK Codex task summary ingestion")

    assert "HERMES_V14_INGESTION_E2E_OK" in context
    assert provider.get_tool_schemas() == []
    assert candidates == original_candidates


def test_high_risk_generated_candidates_blocked_by_default_unless_explicitly_allowed(tmp_path, monkeypatch):
    text = """Goal
Writes token files for HERMES_HIGH_RISK_TASK_MARKER.

Result
Runs executor and deletes credentials.
"""
    candidates = generate_codex_task_summary_candidates(text)
    output_path = tmp_path / "high-risk-candidates.jsonl"

    assert {candidate["risk_level"] for candidate in candidates} == {"high"}

    write_candidates_jsonl(candidates, output_path)
    runtime_config = _codex_provider_runtime_config(output_path)
    blocked = MemoryFabricProvider(runtime_config=runtime_config)
    allowed = MemoryFabricProvider(
        runtime_config={**runtime_config, "allowed_risk_levels": ["low", "medium", "high"]}
    )
    captured = {}
    original_compose = blocked._compose_active_context

    def capture_compose(**kwargs):
        captured["candidates"] = list(kwargs["memory_candidates"])
        packet = original_compose(**kwargs)
        captured["packet"] = packet
        return packet

    monkeypatch.setattr(blocked, "_compose_active_context", capture_compose)

    query = "HERMES_HIGH_RISK_TASK_MARKER writes token files"
    assert "HERMES_HIGH_RISK_TASK_MARKER" not in blocked.prefetch(query)
    assert captured["candidates"]
    assert any(
        item.get("reason") == "risk_level_not_allowed:high"
        for item in captured["packet"].get("rejected_memories", [])
    )
    assert "HERMES_HIGH_RISK_TASK_MARKER" in allowed.prefetch(query)


def test_stdout_mode_does_not_write_files(tmp_path):
    input_path = tmp_path / "summary.txt"
    input_path.write_text(_summary(), encoding="utf-8")
    stdout = io.StringIO()
    stderr = io.StringIO()
    before = sorted(path.relative_to(tmp_path) for path in tmp_path.rglob("*"))

    exit_code = cli_main(["--input", str(input_path)], stdout=stdout, stderr=stderr)

    after = sorted(path.relative_to(tmp_path) for path in tmp_path.rglob("*"))
    assert exit_code == 0
    assert after == before == [Path("summary.txt")]
    assert stdout.getvalue().strip()
    assert stderr.getvalue() == ""
    assert all(json.loads(line)["governance"]["dry_run"] is True for line in stdout.getvalue().splitlines())


def test_explicit_output_writes_only_to_requested_path(tmp_path):
    input_path = tmp_path / "summary.txt"
    output_path = tmp_path / "generated.jsonl"
    input_path.write_text(_summary(), encoding="utf-8")
    stdout = io.StringIO()
    stderr = io.StringIO()

    exit_code = cli_main(
        ["--input", str(input_path), "--output", str(output_path), "--print-summary"],
        stdout=stdout,
        stderr=stderr,
    )

    assert exit_code == 0
    assert sorted(path.relative_to(tmp_path) for path in tmp_path.rglob("*")) == [
        Path("generated.jsonl"),
        Path("summary.txt"),
    ]
    assert stdout.getvalue() == ""
    assert "codex_task_summary_ingestion_summary=" in stderr.getvalue()
    assert output_path.read_text(encoding="utf-8").strip()


def test_no_writes_to_home_hermes(tmp_path, monkeypatch):
    input_path = tmp_path / "summary.txt"
    home = tmp_path / "home"
    hermes_home = home / ".hermes"
    input_path.write_text(_summary(), encoding="utf-8")
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("HERMES_HOME", str(hermes_home))

    exit_code = cli_main(["--input", str(input_path)], stdout=io.StringIO(), stderr=io.StringIO())

    assert exit_code == 0
    assert not hermes_home.exists()


def test_generated_jsonl_can_be_loaded_by_existing_candidate_jsonl_source(tmp_path):
    candidates = generate_codex_task_summary_candidates(_summary())
    output_path = tmp_path / "generated.jsonl"

    write_candidates_jsonl(candidates, output_path)
    loaded = load_candidate_jsonl_source(output_path, required_fields=["id", "content"])

    assert loaded == candidates
    assert {field for candidate in loaded for field in candidate} >= {
        "id",
        "content",
        "project_id",
        "entity_ids",
        "source",
        "provenance",
        "risk_level",
        "governance",
        "created_at",
        "tags",
    }


def test_generated_candidates_can_feed_memory_fabric_provider_prefetch(tmp_path):
    candidates = generate_codex_task_summary_candidates(_summary())
    output_path = tmp_path / "generated.jsonl"
    write_candidates_jsonl(candidates, output_path)
    provider = MemoryFabricProvider(runtime_config=_codex_provider_runtime_config(output_path))

    context = provider.prefetch("Codex task summary ingestion dry run Memory Fabric candidates")

    assert "Implement Codex task summary ingestion dry run for Memory Fabric candidates." in context
    assert provider.get_tool_schemas() == []


def test_low_risk_candidate_requires_admission_context(tmp_path):
    candidates = generate_codex_task_summary_candidates(_v14_e2e_summary())
    output_path = tmp_path / "missing-admission-context.jsonl"
    write_candidates_jsonl(candidates, output_path)

    provider = MemoryFabricProvider(
        runtime_config={
            "project_scope": DEFAULT_PROJECT_ID,
            "candidate_jsonl_path": str(output_path),
            "candidate_jsonl_required_fields": ["id", "content"],
            "memory_limit": 5,
            "context_budget_chars": 2400,
        }
    )

    assert provider.prefetch("HERMES_V14_INGESTION_E2E_OK") == ""


def test_explicit_high_risk_allow_does_not_bypass_source_admission(tmp_path):
    text = """Goal
Writes token files for HERMES_HIGH_RISK_TASK_MARKER.

Result
Runs executor and deletes credentials.
"""
    candidates = generate_codex_task_summary_candidates(text)
    output_path = tmp_path / "high-risk-source-boundary.jsonl"
    write_candidates_jsonl(candidates, output_path)
    base_config = _codex_provider_runtime_config(output_path, allowed_risk_levels=["low", "medium", "high"])

    missing_registry = MemoryFabricProvider(runtime_config={**base_config, "provider_registry_snapshot": None})
    external_source = MemoryFabricProvider(
        runtime_config={
            **base_config,
            "candidate_jsonl_source": {
                **CODEX_JSONL_SOURCE,
                "source_class": "EXTERNAL_FEDERATED_CANDIDATE",
            },
            "provider_registry_snapshot": {
                CODEX_JSONL_SOURCE["provider_id"]: {
                    **CODEX_PROVIDER_REGISTRY[CODEX_JSONL_SOURCE["provider_id"]],
                    "source_classes": ["EXTERNAL_FEDERATED_CANDIDATE"],
                }
            },
        }
    )

    query = "HERMES_HIGH_RISK_TASK_MARKER writes token files"
    assert missing_registry.prefetch(query) == ""
    assert external_source.prefetch(query) == ""


def test_payload_identity_does_not_override_trusted_source_configuration(tmp_path, monkeypatch):
    candidates = generate_codex_task_summary_candidates(_v14_e2e_summary())
    candidates[0]["project_id"] = "attacker-project"
    candidates[0]["source"] = "attacker-source"
    output_path = tmp_path / "payload-identity-spoof.jsonl"
    write_candidates_jsonl(candidates, output_path)
    provider = MemoryFabricProvider(runtime_config=_codex_provider_runtime_config(output_path))
    captured = {}
    original_compose = provider._compose_active_context

    def capture_compose(**kwargs):
        captured["candidates"] = list(kwargs["memory_candidates"])
        return original_compose(**kwargs)

    monkeypatch.setattr(provider, "_compose_active_context", capture_compose)
    context = provider.prefetch("HERMES_V14_INGESTION_E2E_OK")

    assert "HERMES_V14_INGESTION_E2E_OK" in context
    identity = captured["candidates"][0]["provider_federation_identity"]
    assert identity["provider_id"] == CODEX_JSONL_SOURCE["provider_id"]
    assert identity["source_class"] == CODEX_JSONL_SOURCE["source_class"]
    assert identity["source_instance"] == CODEX_JSONL_SOURCE["source_instance"]


@pytest.mark.parametrize("project_length", [209, 210])
def test_adapter_jsonl_provider_accepts_legal_project_id_length_boundary(
    tmp_path, monkeypatch, project_length
):
    # Both project IDs are canonical ASCII strings within the contract's
    # 1-256 character project limit. Do not shorten them to fit generated IDs.
    project_id = "p" * project_length
    candidates = generate_codex_task_summary_candidates(
        "Goal\nIdentity boundary record.", project_id=project_id
    )
    assert len(candidates) == 1
    output_path = tmp_path / "identity-length-boundary.jsonl"
    write_candidates_jsonl(candidates, output_path)
    assert load_candidate_jsonl_source(
        output_path, required_fields=["id", "content"]
    ) == candidates

    config = _codex_provider_runtime_config(output_path, project_scope=project_id)
    config["admission_scope"]["project"] = project_id
    provider = MemoryFabricProvider(runtime_config=config)
    captured = {}
    original_compose = provider._compose_active_context

    def capture_compose(**kwargs):
        captured["candidates"] = list(kwargs["memory_candidates"])
        return original_compose(**kwargs)

    monkeypatch.setattr(provider, "_compose_active_context", capture_compose)
    context = provider.prefetch("Identity boundary record")

    assert captured.get("candidates"), (
        f"No downstream candidates: legal project length {project_length}, "
        f"generated ID length {len(candidates[0]['id'])}"
    )
    assert 1 <= len(candidates[0]["id"]) <= 256
    assert re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:/-]*", candidates[0]["id"])
    assert [item["id"] for item in captured["candidates"]] == [
        candidates[0]["id"]
    ]
    assert captured["candidates"][0]["provider_federation_identity"]["candidate_id"] == candidates[0]["id"]
    assert "Identity boundary record" in context


def _observe_identity_pipeline(
    tmp_path, monkeypatch, records, *, project_id=DEFAULT_PROJECT_ID,
    runtime_memory_candidates=None, **overrides
):
    output = tmp_path / "identity-pipeline.jsonl"
    write_candidates_jsonl(records, output)
    assert load_candidate_jsonl_source(output) == records
    config = _codex_provider_runtime_config(output, project_scope=project_id, **overrides)
    config["admission_scope"]["project"] = project_id
    provider = MemoryFabricProvider(
        runtime_config=config, runtime_memory_candidates=runtime_memory_candidates
    )
    captured = {}
    original_admit = provider._admit_candidate_sources
    original_compose = provider._compose_active_context

    def observe_admit(**kwargs):
        result = original_admit(**kwargs)
        captured["admitted"] = deepcopy(result)
        return result

    def observe_compose(**kwargs):
        captured["downstream"] = deepcopy(list(kwargs["memory_candidates"]))
        return original_compose(**kwargs)

    monkeypatch.setattr(provider, "_admit_candidate_sources", observe_admit)
    monkeypatch.setattr(provider, "_compose_active_context", observe_compose)
    context = provider.prefetch("Identity boundary record")
    assert "admitted" in captured, "Provider did not execute admission"
    return captured, context


@pytest.mark.parametrize("kwargs, expected", [
    ({}, "codex-task-summary:hermes-memory-fabric:capability:9417b07538b93d7b"),
    ({"project_id": "p" * 209}, "codex-task-summary:" + "p" * 209 + ":capability:a82440bc474939f9"),
    ({"source": "  Source A  ", "project_id": " project-a "}, "source-a:project-a:capability:df28143eb64ed4ce"),
])
def test_adapter_short_ids_keep_frozen_compatibility(tmp_path, monkeypatch, kwargs, expected):
    records = generate_codex_task_summary_candidates("Goal\nIdentity boundary record.", **kwargs)
    assert records[0]["id"] == expected  # Captured from the pre-repair adapter.
    observed, context = _observe_identity_pipeline(
        tmp_path, monkeypatch, records, project_id=records[0]["project_id"]
    )
    assert observed["admitted"][0]["provider_federation_identity"]["candidate_id"] == expected
    assert "Identity boundary record" in context


@pytest.mark.parametrize("project_length", [1, 210, 256])
def test_adapter_long_source_suffixes_and_legal_projects(tmp_path, monkeypatch, project_length):
    project = "p" * project_length
    # The suffix is past any display prefix; punctuation variants also share a slug.
    sources = ["Source" * 100 + suffix for suffix in ["-alpha", "-beta", "_alpha"]]
    records = [generate_codex_task_summary_candidates(
        "Goal\nIdentity boundary record.", source=source, project_id=project
    )[0] for source in sources]
    assert len({record["id"] for record in records}) == 3
    for record in records:
        assert 1 <= len(record["id"]) <= 256
        assert re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._:/-]*", record["id"])
    first, context = _observe_identity_pipeline(tmp_path, monkeypatch, records, project_id=project)
    regenerated = [generate_codex_task_summary_candidates(
        "Goal\nIdentity boundary record.", source="  " + source + "  ", project_id=project
    )[0] for source in sources]
    assert regenerated == records
    second, _ = _observe_identity_pipeline(tmp_path, monkeypatch, list(reversed(regenerated)), project_id=project)
    identities = lambda observed: {r["id"]: r["provider_federation_identity"] for r in observed["admitted"]}
    assert set(identities(first)) == {r["id"] for r in records}
    assert identities(first) == identities(second)
    assert len(first["downstream"]) == len(second["downstream"]) == 3
    assert "Identity boundary record" in context


def test_adapter_long_project_suffixes_remain_distinct(tmp_path, monkeypatch):
    ids = []
    for suffix in ["a", "b"]:
        project = "p" * 255 + suffix
        records = generate_codex_task_summary_candidates("Goal\nIdentity boundary record.", project_id=project)
        observed, _ = _observe_identity_pipeline(tmp_path, monkeypatch, records, project_id=project)
        assert len(observed["admitted"]) == 1
        ids.append(observed["admitted"][0]["id"])
    assert len(set(ids)) == 2


@pytest.mark.parametrize("source", ["codex-task-summary", "s" * 400])
def test_adapter_content_derived_records_are_distinct(tmp_path, monkeypatch, source):
    before = generate_codex_task_summary_candidates("Goal\nIdentity boundary record first.", source=source)
    after = generate_codex_task_summary_candidates("Goal\nIdentity boundary record second.", source=source)
    assert before[0]["id"] != after[0]["id"]
    observed, context = _observe_identity_pipeline(tmp_path, monkeypatch, before + after)
    assert len(observed["admitted"]) == len(observed["downstream"]) == 2
    assert len({r["provider_federation_identity"]["payload_digest"] for r in observed["admitted"]}) == 2
    assert "Identity boundary record" in context


@pytest.mark.parametrize("change", ["content", "provenance", "timestamp"])
def test_adapter_same_key_payload_conflicts_block_both(tmp_path, monkeypatch, change):
    original = generate_codex_task_summary_candidates("Goal\nIdentity boundary record.", source="s" * 400)[0]
    if change == "provenance":
        changed = generate_codex_task_summary_candidates("\nGoal\nIdentity boundary record.", source="s" * 400)[0]
        assert changed["provenance"] != original["provenance"]
        assert changed["content"] == original["content"]
    elif change == "timestamp":
        changed = generate_codex_task_summary_candidates(
            "Goal\nIdentity boundary record.", source="s" * 400, created_at="2026-09-09T00:00:00Z"
        )[0]
        assert changed["created_at"] != original["created_at"]
    else:
        # Deliberate conflicting input; ordinary adapter content changes get new IDs.
        changed = deepcopy(original)
        changed["content"] = "Identity boundary record with explicitly conflicting content."
    assert changed["id"] == original["id"]
    first, _ = _observe_identity_pipeline(tmp_path, monkeypatch, [original])
    second, _ = _observe_identity_pipeline(tmp_path, monkeypatch, [changed])
    assert len(first["admitted"]) == len(second["admitted"]) == 1
    assert first["admitted"][0]["provider_federation_identity"]["payload_digest"] != second["admitted"][0]["provider_federation_identity"]["payload_digest"]
    both, context = _observe_identity_pipeline(tmp_path, monkeypatch, [original, changed])
    assert both["admitted"] == []
    assert "downstream" not in both
    assert context == ""


def test_adapter_same_record_different_source_instances(tmp_path, monkeypatch):
    records = generate_codex_task_summary_candidates("Goal\nIdentity boundary record.")
    second_file = tmp_path / "second-instance.jsonl"
    write_candidates_jsonl(records, second_file)
    second_source = dict(CODEX_JSONL_SOURCE, source_instance="provider:second-instance")
    observed, context = _observe_identity_pipeline(
        tmp_path, monkeypatch, records,
        runtime_memory_candidates=load_candidate_jsonl_source(second_file),
        runtime_candidate_source=second_source,
    )
    assert len(observed["admitted"]) == len(observed["downstream"]) == 2
    identities = [r["provider_federation_identity"] for r in observed["admitted"]]
    assert {r["candidate_id"] for r in identities} == {records[0]["id"]}
    assert {r["source_instance"] for r in identities} == {CODEX_JSONL_SOURCE["source_instance"], second_source["source_instance"]}
    assert "Identity boundary record" in context


@pytest.mark.parametrize("bad_id", [None, "", 123, "bad id", "x" * 257, "/bad"])
def test_adapter_jsonl_invalid_id_loads_but_is_not_admitted(tmp_path, monkeypatch, bad_id):
    record = generate_codex_task_summary_candidates("Goal\nIdentity boundary record.")[0]
    record["id"] = bad_id
    observed, context = _observe_identity_pipeline(tmp_path, monkeypatch, [record])
    # required_fields checks presence only, including a present null ID.
    assert load_candidate_jsonl_source(tmp_path / "identity-pipeline.jsonl", required_fields=["id", "content"]) == [record]
    assert observed["admitted"] == []
    assert "downstream" not in observed
    assert context == ""


def test_adapter_jsonl_missing_id_loading_policy_and_admission(tmp_path, monkeypatch):
    record = generate_codex_task_summary_candidates("Goal\nIdentity boundary record.")[0]
    del record["id"]
    observed, context = _observe_identity_pipeline(
        tmp_path, monkeypatch, [record], candidate_jsonl_required_fields=[]
    )
    output = tmp_path / "identity-pipeline.jsonl"
    assert load_candidate_jsonl_source(output) == [record]
    assert load_candidate_jsonl_source(output, required_fields=["id", "content"]) == []
    assert load_candidate_jsonl_source(output, required_fields=["id", "content"], ignore_invalid_lines=False) == []
    assert observed["admitted"] == []
    assert "downstream" not in observed
    assert context == ""
