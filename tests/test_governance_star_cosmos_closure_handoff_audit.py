from __future__ import annotations

from copy import deepcopy
import json
import math
from pathlib import Path

import pytest

from hermes_memory_fabric.governance_star_cosmos_closure_handoff_audit import (
    COMMON_DISABLED_FLAGS,
    GOVERNANCE_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_HASH_ALGORITHM,
    GOVERNANCE_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_SCHEMA_VERSION,
    GOVERNANCE_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_TYPE,
    GOVERNANCE_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_VERSION,
    LAYER_14_CLOSURE_STATUS,
    REQUIRED_STAR_COSMOS_CLOSURE_BLOCKING_CONDITION_NAMES,
    REQUIRED_STAR_COSMOS_CLOSURE_EVIDENCE_REQUIREMENT_NAMES,
    REQUIRED_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_CHECK_NAMES,
    REQUIRED_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_CONTRACT_NAMES,
    REQUIRED_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_SECTION_NAMES,
    REQUIRED_STAR_COSMOS_CLOSURE_READINESS_CONDITION_NAMES,
    SAFETY_BOUNDARIES,
    STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_MODE,
    STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_STAGE,
    STAR_COSMOS_CLOSURE_MODE,
    STAR_COSMOS_CLOSURE_STATUS,
    STAR_COSMOS_ENTRY_STATUS,
    STAR_SOURCE_ENTRY_STATUS,
    STAR_SOURCE_MEMORY_ACTIVE_STATUS,
    V6_HANDOFF_STATUS,
    _star_cosmos_closure_handoff_audit_hash,
    build_governance_star_cosmos_closure_handoff_audit,
    get_governance_star_cosmos_closure_handoff_audit_check,
    get_governance_star_cosmos_closure_handoff_audit_contract,
    get_governance_star_cosmos_closure_handoff_audit_section,
    governance_star_cosmos_closure_handoff_audit_to_json,
    list_governance_star_cosmos_closure_handoff_audit_check_names,
    list_governance_star_cosmos_closure_handoff_audit_contract_names,
    list_governance_star_cosmos_closure_handoff_audit_section_names,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = (
    PROJECT_ROOT
    / "src"
    / "hermes_memory_fabric"
    / "governance_star_cosmos_closure_handoff_audit.py"
)

EXPECTED_INVENTORY_NAMES = (
    "v5.0.0_execution_adapter_boundary_candidate",
    "v5.1.0_execution_adapter_declaration_schema_registry_candidate",
    "v5.2.0_execution_adapter_manifest_dry_run_design_candidate",
    "v5.3.0_execution_adapter_manifest_fixture_pack_candidate",
    "v5.4.0_execution_adapter_manifest_validation_matrix_candidate",
    "v5.5.0_execution_adapter_manifest_policy_gate_candidate",
    "v5.6.0_execution_adapter_manifest_approval_gate_candidate",
    "v5.7.0_execution_adapter_manifest_authorization_gate_candidate",
    "v5.8.0_adapter_handoff_audit",
    "v5.9.0_operation_ledger_proposal_boundary",
    "v5.10.0_cross_system_coordination_boundary",
    "v5.11.0_controlled_adapter_sandbox_candidate",
    "v5.12.0_post_sandbox_review_boundary",
)

EXPECTED_TOP_LEVEL_FALSE_FIELDS = (
    "star_cosmos_memory_active",
    "star_source_memory_active",
    "v6_started",
    "layer_15_started",
    "star_source_entry_candidate_activated",
    "actual_layer_14_closure_performed",
    "closure_handoff_audit_executed",
    "closure_record_written",
    "closure_audit_log_written",
    "closure_evidence_persisted",
    "source_provenance_engine_created",
    "source_evolution_engine_created",
    "source_graph_mutation_enabled",
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
    "audit_evidence_persisted",
    "failure_handling_executed",
    "remediation_executed",
    "hermes_connected",
    "codex_connected",
    "openclaw_connected",
    "github_connected",
    "tool_routing_enabled",
    "command_routing_enabled",
    "cross_system_coordination_enabled",
    "system_handoff_completed",
    "execution_adapter_implemented",
    "execution_adapter_invoked",
    "adapter_dispatched",
    "manifest_dispatched",
    "manifest_executed",
    "dry_run_plan_executed",
    "real_execution_enabled",
    "external_calls_enabled",
    "network_calls_enabled",
    "durable_writes_enabled",
    "filesystem_writes_enabled",
    "database_writes_enabled",
    "memory_graph_mutation_enabled",
    "operation_ledger_writes_enabled",
    "operation_ledger_entry_created",
    "operation_ledger_entry_written",
    "operation_ledger_proposal_persisted",
    "operation_ledger_proposal_submitted",
    "operation_ledger_proposal_dispatched",
    "autonomous_execution_enabled",
    "approval_request_created",
    "approval_notification_sent",
    "real_approval_record_written",
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
    '"sandbox_runtime_payload"',
    '"sandbox_result_payload"',
    '"rollback_payload"',
    '"quarantine_payload"',
    '"incident_payload"',
    '"audit_log_payload"',
    '"closure_record_payload"',
    '"source_provenance_payload"',
    '"source_evolution_payload"',
    '"source_graph_mutation_payload"',
    '"operation_ledger_entry_payload"',
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
    "adapter_" + "dispatch_call",
    "manifest_" + "dispatch_call",
    "git " + "push",
    "g" + "h api",
)


@pytest.fixture(scope="module")
def audit() -> dict[str, object]:
    return build_governance_star_cosmos_closure_handoff_audit()


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


def test_constants_match_v5_13_contract():
    assert GOVERNANCE_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_VERSION == "6.1.0"
    assert (
        GOVERNANCE_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_SCHEMA_VERSION
        == "6.1.0"
    )
    assert (
        GOVERNANCE_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_TYPE
        == "governance_star_cosmos_closure_handoff_audit"
    )
    assert GOVERNANCE_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_HASH_ALGORITHM == "sha256"
    assert (
        STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_STAGE
        == "v5.13_star_cosmos_closure_handoff_audit"
    )
    assert (
        STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_MODE
        == "star_cosmos_closure_handoff_audit_only"
    )
    assert STAR_COSMOS_CLOSURE_MODE == "metadata_only"
    assert STAR_COSMOS_CLOSURE_STATUS == "closure_candidate_only"
    assert LAYER_14_CLOSURE_STATUS == "closure_candidate_only"
    assert V6_HANDOFF_STATUS == "ready_for_star_source_entry_candidate_design"
    assert STAR_SOURCE_ENTRY_STATUS == "not_entered"
    assert STAR_SOURCE_MEMORY_ACTIVE_STATUS == "not_active"
    assert STAR_COSMOS_ENTRY_STATUS == "candidate_only"


def test_audit_shape_is_deterministic_and_passes(audit):
    repeated = build_governance_star_cosmos_closure_handoff_audit()

    assert repeated == audit
    assert audit["version"] == "6.1.0"
    assert audit["schema_version"] == "6.1.0"
    assert audit["star_cosmos_closure_handoff_audit_status"] == "pass"
    assert (
        audit["star_cosmos_closure_handoff_audit_stage"]
        == "v5.13_star_cosmos_closure_handoff_audit"
    )
    assert (
        audit["star_cosmos_closure_handoff_audit_mode"]
        == "star_cosmos_closure_handoff_audit_only"
    )
    assert audit["star_cosmos_closure_mode"] == "metadata_only"
    assert audit["star_cosmos_closure_status"] == "closure_candidate_only"
    assert audit["layer_14_closure_status"] == "closure_candidate_only"
    assert (
        audit["v6_handoff_status"]
        == "ready_for_star_source_entry_candidate_design"
    )
    assert audit["star_source_entry_status"] == "not_entered"
    assert audit["star_source_memory_active_status"] == "not_active"
    assert audit["star_cosmos_entry_status"] == "candidate_only"
    assert audit["post_sandbox_review_boundary_version"] == "6.1.0"
    assert audit["post_sandbox_review_boundary_status"] == "pass"
    assert len(audit["post_sandbox_review_boundary_hash"]) == 64
    assert (
        audit["handoff_status"]
        == "ready_for_v6_star_source_entry_candidate_design"
    )
    assert audit["blocking_reasons"] == []


def test_closure_metadata_is_deterministic_and_metadata_only(audit):
    metadata = audit["star_cosmos_closure_metadata"]

    assert (
        metadata["star_cosmos_closure_metadata_type"]
        == "layer_14_star_cosmos_closure_handoff_audit_metadata"
    )
    assert metadata["star_cosmos_closure_metadata_mode"] == "metadata_only"
    assert metadata["star_cosmos_closure_status"] == "closure_candidate_only"
    assert metadata["layer_14_closure_status"] == "closure_candidate_only"
    assert (
        metadata["v6_handoff_status"]
        == "ready_for_star_source_entry_candidate_design"
    )
    assert metadata["v6_entry_candidate_design_allowed"] is True
    assert metadata["v6_entry_candidate_started"] is False
    assert (
        metadata["star_cosmos_closure_handoff_status"]
        == "ready_for_v6_star_source_entry_candidate_design"
    )


def test_v5_layer_stack_inventory_is_stable_and_complete(audit):
    inventory = audit["v5_layer_stack_closure_inventory"]

    assert [item["layer_stage_name"] for item in inventory] == list(
        EXPECTED_INVENTORY_NAMES
    )
    assert len(inventory) == 13
    assert all(
        item["layer_stage_status"] == "sealed_metadata_boundary"
        and item["layer_stage_execution_status"] == "no_execution"
        and item["layer_stage_closure_status"]
        == "included_in_layer_14_closure_candidate"
        for item in inventory
    )


def test_required_name_registries_are_stable_and_complete(audit):
    metadata = audit["star_cosmos_closure_metadata"]

    assert metadata["star_cosmos_closure_readiness_conditions"] == list(
        REQUIRED_STAR_COSMOS_CLOSURE_READINESS_CONDITION_NAMES
    )
    assert metadata["required_star_cosmos_closure_evidence"] == list(
        REQUIRED_STAR_COSMOS_CLOSURE_EVIDENCE_REQUIREMENT_NAMES
    )
    assert metadata["star_cosmos_closure_blocking_conditions"] == list(
        REQUIRED_STAR_COSMOS_CLOSURE_BLOCKING_CONDITION_NAMES
    )
    assert list_governance_star_cosmos_closure_handoff_audit_section_names() == list(
        REQUIRED_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_SECTION_NAMES
    )
    assert list_governance_star_cosmos_closure_handoff_audit_contract_names() == list(
        REQUIRED_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_CONTRACT_NAMES
    )
    assert list_governance_star_cosmos_closure_handoff_audit_check_names() == list(
        REQUIRED_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_CHECK_NAMES
    )
    assert len(REQUIRED_STAR_COSMOS_CLOSURE_READINESS_CONDITION_NAMES) == 60
    assert len(REQUIRED_STAR_COSMOS_CLOSURE_EVIDENCE_REQUIREMENT_NAMES) == 51
    assert len(REQUIRED_STAR_COSMOS_CLOSURE_BLOCKING_CONDITION_NAMES) == 59
    assert len(REQUIRED_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_SECTION_NAMES) == 26
    assert len(REQUIRED_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_CONTRACT_NAMES) == 58
    assert len(REQUIRED_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_CHECK_NAMES) == 62


@pytest.mark.parametrize(
    ("getter", "names", "status_field"),
    (
        (
            get_governance_star_cosmos_closure_handoff_audit_section,
            REQUIRED_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_SECTION_NAMES,
            "section_status",
        ),
        (
            get_governance_star_cosmos_closure_handoff_audit_contract,
            REQUIRED_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_CONTRACT_NAMES,
            "contract_status",
        ),
        (
            get_governance_star_cosmos_closure_handoff_audit_check,
            REQUIRED_STAR_COSMOS_CLOSURE_HANDOFF_AUDIT_CHECK_NAMES,
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
            get_governance_star_cosmos_closure_handoff_audit_section,
            "section_status",
        ),
        (
            get_governance_star_cosmos_closure_handoff_audit_contract,
            "contract_status",
        ),
        (
            get_governance_star_cosmos_closure_handoff_audit_check,
            "check_status",
        ),
    ),
)
def test_unknown_getters_return_blocked_style_results(getter, status_field):
    unknown = getter("unknown_name")

    assert unknown[status_field] == "blocked"
    assert unknown["blocking_reasons"]
    _assert_all_safety_false(unknown)


def test_all_sections_contracts_and_checks_pass(audit):
    assert all(
        item["section_status"] == "pass"
        for item in audit["star_cosmos_closure_sections"]
    )
    assert all(
        item["contract_status"] == "pass"
        for item in audit["star_cosmos_closure_contracts"]
    )
    assert all(
        item["check_status"] == "pass"
        for item in audit["star_cosmos_closure_checks"]
    )


def test_all_execution_write_routing_and_active_entry_flags_remain_false(audit):
    assert tuple(COMMON_DISABLED_FLAGS) == EXPECTED_TOP_LEVEL_FALSE_FIELDS
    for field_name in EXPECTED_TOP_LEVEL_FALSE_FIELDS:
        assert audit[field_name] is False
    _assert_all_safety_false(audit)


def test_deterministic_hash_is_stable(audit):
    repeated = build_governance_star_cosmos_closure_handoff_audit()

    assert (
        audit["deterministic_star_cosmos_closure_handoff_audit_hash"]
        == repeated["deterministic_star_cosmos_closure_handoff_audit_hash"]
    )
    assert len(audit["deterministic_star_cosmos_closure_handoff_audit_hash"]) == 64


@pytest.mark.parametrize(
    ("field_name", "mutator"),
    (
        (
            "star_cosmos_closure_metadata",
            lambda value: value.update({"closure_handoff_audit_declared": False}),
        ),
        (
            "v5_layer_stack_closure_inventory",
            lambda value: value[0].update({"layer_stage_status": "changed"}),
        ),
        (
            "star_cosmos_closure_sections",
            lambda value: value[0].update({"section_status": "blocked"}),
        ),
        (
            "star_cosmos_closure_contracts",
            lambda value: value[0].update({"contract_status": "blocked"}),
        ),
        (
            "star_cosmos_closure_checks",
            lambda value: value[0].update({"check_status": "blocked"}),
        ),
    ),
)
def test_hash_changes_when_governed_data_changes(audit, field_name, mutator):
    changed = deepcopy(audit)
    original_hash = _star_cosmos_closure_handoff_audit_hash(audit)
    mutator(changed[field_name])

    assert _star_cosmos_closure_handoff_audit_hash(changed) != original_hash


def test_json_is_deterministic_and_rejects_non_finite_values(audit):
    first = governance_star_cosmos_closure_handoff_audit_to_json(audit)
    second = governance_star_cosmos_closure_handoff_audit_to_json(audit)

    assert first == second
    assert first.endswith("\n")
    assert json.loads(first) == audit
    with pytest.raises(ValueError):
        governance_star_cosmos_closure_handoff_audit_to_json(
            {"invalid": math.nan}
        )
    with pytest.raises(TypeError):
        governance_star_cosmos_closure_handoff_audit_to_json({1: "invalid"})


def test_no_sensitive_keys_or_values_leak(audit):
    _assert_no_sensitive_terms(
        {
            "metadata": audit["star_cosmos_closure_metadata"],
            "inventory": audit["v5_layer_stack_closure_inventory"],
            "sections": audit["star_cosmos_closure_sections"],
            "contracts": audit["star_cosmos_closure_contracts"],
            "checks": audit["star_cosmos_closure_checks"],
            "summary": audit["star_cosmos_closure_summary"],
            "hash": audit[
                "deterministic_star_cosmos_closure_handoff_audit_hash"
            ],
            "json": governance_star_cosmos_closure_handoff_audit_to_json(audit),
        }
    )


def test_new_module_has_no_live_execution_or_mutation_surfaces():
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
