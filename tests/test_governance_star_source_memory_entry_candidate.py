from __future__ import annotations

from copy import deepcopy
import json
import math
from pathlib import Path

import pytest

from hermes_memory_fabric.governance_star_source_memory_entry_candidate import (
    COMMON_DISABLED_FLAGS,
    GOVERNANCE_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_HASH_ALGORITHM,
    GOVERNANCE_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_SCHEMA_VERSION,
    GOVERNANCE_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_TYPE,
    GOVERNANCE_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_VERSION,
    LAYER_15_ENTRY_STATUS,
    METHODOLOGY_REVERSE_INFERENCE_STATUS,
    REQUIRED_STAR_SOURCE_ENTRY_BLOCKING_CONDITION_NAMES,
    REQUIRED_STAR_SOURCE_ENTRY_EVIDENCE_REQUIREMENT_NAMES,
    REQUIRED_STAR_SOURCE_ENTRY_READINESS_CONDITION_NAMES,
    REQUIRED_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_CHECK_NAMES,
    REQUIRED_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_CONTRACT_NAMES,
    REQUIRED_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_SECTION_NAMES,
    SAFETY_BOUNDARIES,
    SELF_EVOLUTION_STATUS,
    SOURCE_PROVENANCE_STATUS,
    STAR_SOURCE_ENTRY_STATUS,
    STAR_SOURCE_ENTRY_NEXT_STAGE,
    STAR_SOURCE_ENTRY_NEXT_STAGE_TITLE,
    STAR_SOURCE_MEMORY_ACTIVE_STATUS,
    STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_MODE,
    STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_STAGE,
    STAR_SOURCE_MEMORY_MODE,
    V6_ENTRY_STATUS,
    V6_HANDOFF_ACCEPTANCE_STATUS,
    _star_source_memory_entry_candidate_hash,
    build_governance_star_source_memory_entry_candidate,
    get_governance_star_source_memory_entry_candidate_check,
    get_governance_star_source_memory_entry_candidate_contract,
    get_governance_star_source_memory_entry_candidate_section,
    governance_star_source_memory_entry_candidate_to_json,
    list_governance_star_source_memory_entry_candidate_check_names,
    list_governance_star_source_memory_entry_candidate_contract_names,
    list_governance_star_source_memory_entry_candidate_section_names,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = (
    PROJECT_ROOT
    / "src"
    / "hermes_memory_fabric"
    / "governance_star_source_memory_entry_candidate.py"
)

EXPECTED_FALSE_FIELDS = (
    "star_source_memory_active",
    "star_source_active_entry_claimed",
    "star_source_entry_candidate_activated",
    "layer_15_active",
    "source_provenance_active",
    "methodology_reverse_inference_active",
    "self_evolution_active",
    "source_graph_created",
    "source_graph_mutation_enabled",
    "source_provenance_engine_created",
    "methodology_reverse_inference_engine_created",
    "self_evolution_engine_created",
    "autonomous_rule_mutation_enabled",
    "governance_policy_mutation_enabled",
    "memory_graph_mutation_enabled",
    "real_execution_enabled",
    "execution_adapter_implemented",
    "execution_adapter_invoked",
    "adapter_dispatched",
    "manifest_dispatched",
    "manifest_executed",
    "dry_run_plan_executed",
    "controlled_adapter_sandbox_started",
    "adapter_sandbox_entered",
    "sandbox_runtime_created",
    "sandbox_execution_enabled",
    "sandbox_network_enabled",
    "sandbox_writes_enabled",
    "sandbox_result_available",
    "actual_post_sandbox_review_performed",
    "rollback_triggered",
    "quarantine_triggered",
    "incident_triggered",
    "audit_log_written",
    "closure_record_written",
    "external_calls_enabled",
    "network_calls_enabled",
    "durable_writes_enabled",
    "filesystem_writes_enabled",
    "database_writes_enabled",
    "hermes_connected",
    "codex_connected",
    "openclaw_connected",
    "github_connected",
    "composio_connected",
    "tool_routing_enabled",
    "command_routing_enabled",
    "cross_system_coordination_enabled",
    "system_handoff_completed",
    "operation_ledger_writes_enabled",
    "operation_ledger_entry_created",
    "operation_ledger_entry_written",
    "operation_ledger_proposal_persisted",
    "operation_ledger_proposal_submitted",
    "operation_ledger_proposal_dispatched",
    "autonomous_execution_enabled",
    "approval_request_created",
    "real_approval_record_written",
    "approval_notification_sent",
    "execution_authorization_issued",
    "authorization_token_created",
    "authorization_grant_created",
)

SENSITIVE_TERMS = (
    '"approval_phrase"',
    '"authorization_value"',
    '"authorization_token_value"',
    '"authorization_grant_value"',
    '"stdout"',
    '"stderr"',
    '"raw_logs"',
    '"api_key"',
    '"secret"',
    '"password"',
    '"credential"',
    '"source_record_payload"',
    '"source_graph_payload"',
    '"source_provenance_payload"',
    '"methodology_inference_payload"',
    '"self_evolution_payload"',
    '"sandbox_runtime_payload"',
    '"sandbox_result_payload"',
    '"rollback_payload"',
    '"quarantine_payload"',
    '"incident_payload"',
    '"audit_log_payload"',
    '"closure_record_payload"',
    '"operation_ledger_entry_payload"',
    '"network_target"',
    "http://",
    "https://",
    "ssh://",
    "git@",
    "/Users/",
    "/private/",
    "/tmp/",
    "C:\\",
    "@example" + ".com",
    "tool_" + "call_instruction",
    "shell_" + "command",
    "git " + "push",
    "g" + "h api",
)


@pytest.fixture(scope="module")
def candidate() -> dict[str, object]:
    return build_governance_star_source_memory_entry_candidate()


def _assert_all_safety_false(value: object) -> None:
    if isinstance(value, dict):
        for field_name in COMMON_DISABLED_FLAGS:
            if field_name in value:
                assert value[field_name] is False
        boundaries = value.get("safety_boundaries")
        if isinstance(boundaries, dict):
            for field_name in SAFETY_BOUNDARIES:
                assert value[field_name] is False
                assert boundaries[field_name] is False
        for nested_value in value.values():
            _assert_all_safety_false(nested_value)
    elif isinstance(value, list):
        for item in value:
            _assert_all_safety_false(item)


def _assert_no_sensitive_terms(value: object) -> None:
    payload = json.dumps(value, sort_keys=True).lower()
    for term in SENSITIVE_TERMS:
        candidate = term if term.startswith("/") else term.lower()
        assert candidate not in payload


def test_constants_match_v6_contract():
    assert GOVERNANCE_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_VERSION == "6.6.0"
    assert GOVERNANCE_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_SCHEMA_VERSION == "6.6.0"
    assert (
        GOVERNANCE_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_TYPE
        == "governance_star_source_memory_entry_candidate"
    )
    assert GOVERNANCE_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_HASH_ALGORITHM == "sha256"
    assert (
        STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_STAGE
        == "v6.0_star_source_memory_entry_candidate"
    )
    assert (
        STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_MODE
        == "star_source_entry_candidate_only"
    )
    assert STAR_SOURCE_MEMORY_MODE == "metadata_only"
    assert STAR_SOURCE_ENTRY_STATUS == "entry_candidate_only"
    assert STAR_SOURCE_MEMORY_ACTIVE_STATUS == "not_active"
    assert LAYER_15_ENTRY_STATUS == "entry_candidate_only"
    assert SOURCE_PROVENANCE_STATUS == "not_active"
    assert METHODOLOGY_REVERSE_INFERENCE_STATUS == "not_active"
    assert SELF_EVOLUTION_STATUS == "not_active"
    assert V6_ENTRY_STATUS == "entry_candidate_only"
    assert V6_HANDOFF_ACCEPTANCE_STATUS == "accepted_as_metadata_only"
    assert STAR_SOURCE_ENTRY_NEXT_STAGE == "v6.1_source_constitution_registry"
    assert STAR_SOURCE_ENTRY_NEXT_STAGE_TITLE == "Source Constitution Registry"


def test_candidate_shape_is_deterministic_and_passes(candidate):
    repeated = build_governance_star_source_memory_entry_candidate()

    assert repeated == candidate
    assert candidate["version"] == "6.6.0"
    assert candidate["schema_version"] == "6.6.0"
    assert candidate["star_source_memory_entry_candidate_status"] == "pass"
    assert (
        candidate["star_source_memory_entry_candidate_stage"]
        == "v6.0_star_source_memory_entry_candidate"
    )
    assert (
        candidate["star_source_memory_entry_candidate_mode"]
        == "star_source_entry_candidate_only"
    )
    assert candidate["star_source_memory_mode"] == "metadata_only"
    assert candidate["star_source_entry_status"] == "entry_candidate_only"
    assert candidate["star_source_memory_active_status"] == "not_active"
    assert candidate["layer_15_entry_status"] == "entry_candidate_only"
    assert candidate["source_provenance_status"] == "not_active"
    assert candidate["methodology_reverse_inference_status"] == "not_active"
    assert candidate["self_evolution_status"] == "not_active"
    assert candidate["v6_entry_status"] == "entry_candidate_only"
    assert candidate["v6_handoff_acceptance_status"] == "accepted_as_metadata_only"
    assert candidate["star_cosmos_closure_handoff_audit_version"] == "6.6.0"
    assert candidate["star_cosmos_closure_handoff_audit_status"] == "pass"
    assert len(candidate["star_cosmos_closure_handoff_audit_hash"]) == 64
    assert (
        candidate["handoff_status"]
        == "ready_for_source_constitution_registry_design"
    )
    assert candidate["blocking_reasons"] == []


def test_entry_metadata_is_deterministic_metadata_only_and_inactive(candidate):
    metadata = candidate["star_source_entry_metadata"]

    assert (
        metadata["star_source_entry_metadata_type"]
        == "layer_15_star_source_memory_entry_candidate_metadata"
    )
    assert metadata["star_source_entry_metadata_mode"] == "metadata_only"
    assert metadata["star_source_entry_status"] == "entry_candidate_only"
    assert metadata["star_source_memory_active_status"] == "not_active"
    assert metadata["layer_15_entry_status"] == "entry_candidate_only"
    assert metadata["star_source_entry_candidate_declared"] is True
    assert metadata["star_source_entry_candidate_activated"] is False
    assert metadata["star_cosmos_closure_handoff_audit_hash_present"] is True
    assert metadata["star_cosmos_closure_handoff_audit_hash_stable"] is True
    assert metadata["star_cosmos_handoff_ready"] is True
    assert (
        metadata["star_source_entry_next_stage"]
        == "v6.1_source_constitution_registry"
    )
    assert (
        metadata["star_source_entry_next_stage_title"]
        == "Source Constitution Registry"
    )
    assert (
        metadata["star_source_entry_handoff_status"]
        == "ready_for_source_constitution_registry_design"
    )


@pytest.mark.parametrize(
    ("field_name", "metadata_type", "status_field", "declared_field", "active_field"),
    (
        (
            "source_provenance_entry_metadata",
            "source_provenance_entry_candidate_metadata",
            "source_provenance_status",
            "source_provenance_entry_declared",
            "source_provenance_active",
        ),
        (
            "methodology_reverse_inference_entry_metadata",
            "methodology_reverse_inference_entry_candidate_metadata",
            "methodology_reverse_inference_status",
            "methodology_reverse_inference_entry_declared",
            "methodology_reverse_inference_active",
        ),
        (
            "self_evolution_entry_metadata",
            "self_evolution_entry_candidate_metadata",
            "self_evolution_status",
            "self_evolution_entry_declared",
            "self_evolution_active",
        ),
    ),
)
def test_future_capability_entry_metadata_is_metadata_only_and_inactive(
    candidate,
    field_name,
    metadata_type,
    status_field,
    declared_field,
    active_field,
):
    metadata = candidate[field_name]

    assert metadata["entry_metadata_type"] == metadata_type
    assert metadata["entry_metadata_mode"] == "metadata_only"
    assert metadata["entry_status"] == "entry_candidate_only"
    assert metadata[status_field] == "not_active"
    assert metadata[declared_field] is True
    assert metadata[active_field] is False
    assert metadata["runtime_created"] is False
    assert metadata["live_output_included"] is False


def test_required_name_registries_are_stable_and_complete(candidate):
    metadata = candidate["star_source_entry_metadata"]

    assert metadata["star_source_entry_readiness_conditions"] == list(
        REQUIRED_STAR_SOURCE_ENTRY_READINESS_CONDITION_NAMES
    )
    assert metadata["required_star_source_entry_evidence"] == list(
        REQUIRED_STAR_SOURCE_ENTRY_EVIDENCE_REQUIREMENT_NAMES
    )
    assert metadata["star_source_entry_blocking_conditions"] == list(
        REQUIRED_STAR_SOURCE_ENTRY_BLOCKING_CONDITION_NAMES
    )
    assert list_governance_star_source_memory_entry_candidate_section_names() == list(
        REQUIRED_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_SECTION_NAMES
    )
    assert list_governance_star_source_memory_entry_candidate_contract_names() == list(
        REQUIRED_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_CONTRACT_NAMES
    )
    assert list_governance_star_source_memory_entry_candidate_check_names() == list(
        REQUIRED_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_CHECK_NAMES
    )


@pytest.mark.parametrize(
    ("getter", "names", "status_field"),
    (
        (
            get_governance_star_source_memory_entry_candidate_section,
            REQUIRED_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_SECTION_NAMES,
            "section_status",
        ),
        (
            get_governance_star_source_memory_entry_candidate_contract,
            REQUIRED_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_CONTRACT_NAMES,
            "contract_status",
        ),
        (
            get_governance_star_source_memory_entry_candidate_check,
            REQUIRED_STAR_SOURCE_MEMORY_ENTRY_CANDIDATE_CHECK_NAMES,
            "check_status",
        ),
    ),
)
def test_named_getters_return_detached_copies(getter, names, status_field):
    first = getter(names[0])
    first["blocking_reasons"].append("mutated")
    second = getter(names[0])

    assert second[status_field] == "pass"
    assert second["blocking_reasons"] == []


@pytest.mark.parametrize(
    ("getter", "status_field"),
    (
        (
            get_governance_star_source_memory_entry_candidate_section,
            "section_status",
        ),
        (
            get_governance_star_source_memory_entry_candidate_contract,
            "contract_status",
        ),
        (
            get_governance_star_source_memory_entry_candidate_check,
            "check_status",
        ),
    ),
)
def test_unknown_getters_return_blocked_style_results(getter, status_field):
    unknown = getter("unknown_name")

    assert unknown[status_field] == "blocked"
    assert unknown["blocking_reasons"]
    _assert_all_safety_false(unknown)


def test_all_sections_contracts_and_checks_pass(candidate):
    assert all(
        item["section_status"] == "pass"
        for item in candidate["star_source_entry_sections"]
    )
    assert all(
        item["contract_status"] == "pass"
        for item in candidate["star_source_entry_contracts"]
    )
    assert all(
        item["check_status"] == "pass"
        for item in candidate["star_source_entry_checks"]
    )


def test_all_active_execution_write_routing_and_authorization_flags_are_false(
    candidate,
):
    assert tuple(COMMON_DISABLED_FLAGS) == EXPECTED_FALSE_FIELDS
    for field_name in EXPECTED_FALSE_FIELDS:
        assert candidate[field_name] is False
    _assert_all_safety_false(candidate)


def test_deterministic_hash_is_stable(candidate):
    repeated = build_governance_star_source_memory_entry_candidate()

    assert (
        candidate["deterministic_star_source_memory_entry_candidate_hash"]
        == repeated["deterministic_star_source_memory_entry_candidate_hash"]
    )
    assert len(candidate["deterministic_star_source_memory_entry_candidate_hash"]) == 64


@pytest.mark.parametrize(
    ("field_name", "mutator"),
    (
        (
            "star_source_entry_metadata",
            lambda value: value.update({"star_source_entry_candidate_declared": False}),
        ),
        (
            "source_provenance_entry_metadata",
            lambda value: value.update({"source_provenance_status": "changed"}),
        ),
        (
            "methodology_reverse_inference_entry_metadata",
            lambda value: value.update(
                {"methodology_reverse_inference_status": "changed"}
            ),
        ),
        (
            "self_evolution_entry_metadata",
            lambda value: value.update({"self_evolution_status": "changed"}),
        ),
        (
            "star_source_entry_sections",
            lambda value: value[0].update({"section_status": "blocked"}),
        ),
        (
            "star_source_entry_contracts",
            lambda value: value[0].update({"contract_status": "blocked"}),
        ),
        (
            "star_source_entry_checks",
            lambda value: value[0].update({"check_status": "blocked"}),
        ),
    ),
)
def test_hash_changes_when_governed_data_changes(candidate, field_name, mutator):
    changed = deepcopy(candidate)
    original_hash = _star_source_memory_entry_candidate_hash(candidate)
    mutator(changed[field_name])

    assert _star_source_memory_entry_candidate_hash(changed) != original_hash


def test_json_is_deterministic_and_rejects_invalid_values(candidate):
    first = governance_star_source_memory_entry_candidate_to_json(candidate)
    second = governance_star_source_memory_entry_candidate_to_json(candidate)

    assert first == second
    assert first.endswith("\n")
    assert json.loads(first) == candidate
    with pytest.raises(ValueError):
        governance_star_source_memory_entry_candidate_to_json(
            {"invalid": math.nan}
        )
    with pytest.raises(TypeError):
        governance_star_source_memory_entry_candidate_to_json({1: "invalid"})


def test_no_sensitive_keys_or_values_leak(candidate):
    _assert_no_sensitive_terms(
        {
            "metadata": candidate["star_source_entry_metadata"],
            "provenance": candidate["source_provenance_entry_metadata"],
            "methodology": candidate[
                "methodology_reverse_inference_entry_metadata"
            ],
            "evolution": candidate["self_evolution_entry_metadata"],
            "sections": candidate["star_source_entry_sections"],
            "contracts": candidate["star_source_entry_contracts"],
            "checks": candidate["star_source_entry_checks"],
            "summary": candidate["star_source_entry_summary"],
            "hash": candidate[
                "deterministic_star_source_memory_entry_candidate_hash"
            ],
            "json": governance_star_source_memory_entry_candidate_to_json(
                candidate
            ),
        }
    )


def test_new_module_has_no_live_io_execution_or_runtime_surfaces():
    source = MODULE_PATH.read_text(encoding="utf-8").lower()
    blocked_surfaces = (
        "sub" + "process",
        "sock" + "et",
        "req" + "uests",
        "url" + "lib",
        "open" + "(",
        "write_" + "text",
        "write_" + "bytes",
        "git " + "push",
        "g" + "h api",
        "web" + "hook",
        "send_" + "email",
        "url" + "open",
        "popen" + "(",
        "system" + "(",
        "run" + "(",
        "sqlite",
        "psycopg",
        "mysql",
    )

    for blocked in blocked_surfaces:
        assert blocked not in source


def test_no_contamination_references_or_uv_lock_exist():
    contaminated_names = (
        "governance_" + "improvement_planner",
        "governance_" + "improvement_planner_activation",
        "governance_" + "plan_rules",
        "governance_" + "plan_schema",
        "governance_" + "plan_writer",
        "smoke_" + "governance_" + "improvement_planner",
        "smoke_" + "governance_" + "improvement_planner_activation",
        "test_" + "governance_" + "improvement_planner",
        "test_" + "governance_" + "improvement_planner_activation",
        "test_" + "governance_" + "plan_writer",
    )
    roots = (
        PROJECT_ROOT / "pyproject.toml",
        PROJECT_ROOT / "scripts",
        PROJECT_ROOT / "src" / "hermes_memory_fabric",
        PROJECT_ROOT / "tests",
    )
    for root in roots:
        paths = [root] if root.is_file() else list(root.rglob("*.py"))
        for path in paths:
            source = path.read_text(encoding="utf-8")
            for contaminated_name in contaminated_names:
                assert contaminated_name not in source
    assert not (PROJECT_ROOT / ("uv" + ".lock")).exists()
