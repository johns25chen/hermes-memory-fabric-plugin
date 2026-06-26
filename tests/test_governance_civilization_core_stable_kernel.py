from __future__ import annotations

import ast
from copy import deepcopy
import json
import math
from pathlib import Path

import pytest

from hermes_memory_fabric.governance_civilization_core_stable_kernel import (
    AUDIT_LOG_WRITE_STATUS,
    AUDIT_REPLAY_EXECUTION_STATUS,
    CIVILIZATION_CORE_STABLE_KERNEL_ACTIVE_STATUS,
    CIVILIZATION_CORE_STABLE_KERNEL_MODE,
    CIVILIZATION_CORE_STABLE_KERNEL_STAGE,
    CIVILIZATION_CORE_STABLE_KERNEL_STATUS,
    CLOSURE_AUDIT_EXECUTION_STATUS,
    CLOSURE_DECISION_STATUS,
    COMMON_DISABLED_FLAGS,
    CROSS_LAYER_REPAIR_STATUS,
    CROSS_LAYER_VALIDATION_EXECUTION_STATUS,
    FINAL_AUTHORITY_STATUS,
    FINAL_AUTONOMY_STATUS,
    FINALIZATION_STATUS,
    GOVERNANCE_CIVILIZATION_CORE_STABLE_KERNEL_HASH_ALGORITHM,
    GOVERNANCE_CIVILIZATION_CORE_STABLE_KERNEL_SCHEMA_VERSION,
    GOVERNANCE_CIVILIZATION_CORE_STABLE_KERNEL_TYPE,
    GOVERNANCE_CIVILIZATION_CORE_STABLE_KERNEL_VERSION,
    HUMAN_APPROVAL_STATUS,
    HUMAN_AUTHORIZATION_STATUS,
    KERNEL_EXECUTION_STATUS,
    LAYER_15_ACTIVE_STATUS,
    LEDGER_WRITE_STATUS,
    MEMORY_OR_SOURCE_MIGRATION_STATUS,
    NEXT_STAGE,
    NEXT_STAGE_TITLE,
    POLICY_ENFORCEMENT_STATUS,
    REQUIRED_GOVERNANCE_CIVILIZATION_CORE_STABLE_KERNEL_CHECK_NAMES,
    REQUIRED_GOVERNANCE_CIVILIZATION_CORE_STABLE_KERNEL_CONTRACT_NAMES,
    REQUIRED_GOVERNANCE_CIVILIZATION_CORE_STABLE_KERNEL_RECORD_IDS,
    REQUIRED_GOVERNANCE_CIVILIZATION_CORE_STABLE_KERNEL_SECTION_NAMES,
    SAFETY_BOUNDARIES,
    SOURCE_HANDOFF_EXECUTION_STATUS,
    SOURCE_HANDOFF_EXPORT_STATUS,
    SOURCE_HANDOFF_IMPORT_STATUS,
    SOURCE_HANDOFF_MIGRATION_STATUS,
    SOURCE_MUTATION_APPROVAL_STATUS,
    SOURCE_MUTATION_EXECUTION_STATUS,
    SOURCE_MUTATION_REJECTION_STATUS,
    SOURCE_MUTATION_RUNTIME_STATUS,
    SOURCE_MUTATION_STATUS,
    STABILITY_INDEX_EXECUTION_STATUS,
    STABILITY_MONITORING_STATUS,
    STABILITY_SCORE_RUNTIME_STATUS,
    STABLE_KERNEL_ACTIVATION_STATUS,
    STABLE_KERNEL_RUNTIME_STATUS,
    STABLE_KERNEL_STATUS,
    STAR_SOURCE_MEMORY_ACTIVE_STATUS,
    SYSTEM_FINALIZATION_STATUS,
    V6_TERMINAL_HANDOFF_STATUS,
    _civilization_core_stable_kernel_hash,
    _kernel_hash,
    _kernel_record_hash,
    build_governance_civilization_core_stable_kernel,
    get_governance_civilization_core_stable_kernel_check,
    get_governance_civilization_core_stable_kernel_contract,
    get_governance_civilization_core_stable_kernel_record,
    get_governance_civilization_core_stable_kernel_section,
    governance_civilization_core_stable_kernel_to_json,
    list_governance_civilization_core_stable_kernel_check_names,
    list_governance_civilization_core_stable_kernel_contract_names,
    list_governance_civilization_core_stable_kernel_record_ids,
    list_governance_civilization_core_stable_kernel_section_names,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = (
    PROJECT_ROOT
    / "src"
    / "hermes_memory_fabric"
    / "governance_civilization_core_stable_kernel.py"
)
SMOKE_PATH = PROJECT_ROOT / "scripts" / "smoke_governance_civilization_core_stable_kernel.py"

EXPECTED_RECORD_IDS = (
    "civilization_core_stable_kernel_intake",
    "upstream_star_source_closure_audit_hash_kernel_reference",
    "ordered_layer_15_stable_kernel_chain_registry",
    "civilization_core_stable_kernel_scope_metadata_registry",
    "civilization_core_stable_kernel_input_contract_registry",
    "civilization_core_stable_kernel_output_contract_registry",
    "no_stable_kernel_activation",
    "no_kernel_execution_or_runtime",
    "no_system_finalization_or_final_authority",
    "no_source_memory_graph_or_ledger_mutation",
    "no_autonomy_self_authorization_or_identity_escalation",
    "v6_series_terminal_boundary_record",
)

REQUIRED_FALSE_RECORD_FIELDS = (
    "civilization_core_stable_kernel_active",
    "stable_kernel_activated",
    "stable_kernel_runtime_created",
    "kernel_execution_performed",
    "system_finalization_performed",
    "final_autonomy_created",
    "final_authority_created",
    "closure_audit_executed",
    "closure_decision_performed",
    "finalization_performed",
    "source_handoff_executed",
    "source_handoff_migration_performed",
    "source_handoff_export_performed",
    "source_handoff_import_performed",
    "memory_or_source_migration_performed",
    "stability_index_executed",
    "stability_score_runtime_created",
    "stability_monitoring_performed",
    "cross_layer_validation_executed",
    "cross_layer_repair_performed",
    "audit_replay_executed",
    "audit_log_written",
    "ledger_write_performed",
    "operation_ledger_entry_written",
    "human_approval_performed",
    "human_authorization_performed",
    "source_mutation_approval_performed",
    "source_mutation_rejection_performed",
    "source_mutation_execution_created",
    "source_mutation_performed",
    "source_graph_mutated",
    "memory_graph_mutated",
    "real_ledger_write_performed",
    "external_call_performed",
    "network_call_performed",
    "durable_write_performed",
    "filesystem_write_performed",
    "database_write_performed",
    "execution_authorization_created",
    "authorization_token_created",
    "authorization_grant_created",
    "approval_notification_sent",
    "adapter_dispatched",
    "manifest_dispatched",
    "autonomous_authority_claim_allowed",
    "self_authorization_allowed",
    "identity_escalation_allowed",
    "personhood_claim_allowed",
    "life_claim_allowed",
    "awakening_claim_allowed",
    "legal_subject_claim_allowed",
    "religious_object_claim_allowed",
)


@pytest.fixture(scope="module")
def result() -> dict[str, object]:
    return build_governance_civilization_core_stable_kernel()


def test_constants_and_public_shape(result):
    assert GOVERNANCE_CIVILIZATION_CORE_STABLE_KERNEL_VERSION == "6.16.0"
    assert GOVERNANCE_CIVILIZATION_CORE_STABLE_KERNEL_SCHEMA_VERSION == "6.16.0"
    assert (
        GOVERNANCE_CIVILIZATION_CORE_STABLE_KERNEL_TYPE
        == "governance_civilization_core_stable_kernel"
    )
    assert GOVERNANCE_CIVILIZATION_CORE_STABLE_KERNEL_HASH_ALGORITHM == "sha256"
    assert CIVILIZATION_CORE_STABLE_KERNEL_STAGE == "v6.16_civilization_core_stable_kernel"
    assert CIVILIZATION_CORE_STABLE_KERNEL_MODE == "civilization_core_stable_kernel_design_only"
    assert CIVILIZATION_CORE_STABLE_KERNEL_STATUS == "civilization_core_stable_kernel_candidate_only"
    assert CIVILIZATION_CORE_STABLE_KERNEL_ACTIVE_STATUS == "not_active"
    assert STABLE_KERNEL_STATUS == "metadata_only"
    assert STABLE_KERNEL_ACTIVATION_STATUS == "not_performed"
    assert STABLE_KERNEL_RUNTIME_STATUS == "not_performed"
    assert KERNEL_EXECUTION_STATUS == "not_performed"
    assert SYSTEM_FINALIZATION_STATUS == "not_performed"
    assert FINAL_AUTONOMY_STATUS == "not_active"
    assert FINAL_AUTHORITY_STATUS == "not_active"
    assert CLOSURE_AUDIT_EXECUTION_STATUS == "not_performed"
    assert CLOSURE_DECISION_STATUS == "not_performed"
    assert FINALIZATION_STATUS == "not_performed"
    assert SOURCE_HANDOFF_EXECUTION_STATUS == "not_performed"
    assert SOURCE_HANDOFF_MIGRATION_STATUS == "not_performed"
    assert SOURCE_HANDOFF_EXPORT_STATUS == "not_performed"
    assert SOURCE_HANDOFF_IMPORT_STATUS == "not_performed"
    assert MEMORY_OR_SOURCE_MIGRATION_STATUS == "not_performed"
    assert STABILITY_INDEX_EXECUTION_STATUS == "not_performed"
    assert STABILITY_SCORE_RUNTIME_STATUS == "not_performed"
    assert STABILITY_MONITORING_STATUS == "not_performed"
    assert CROSS_LAYER_VALIDATION_EXECUTION_STATUS == "not_performed"
    assert CROSS_LAYER_REPAIR_STATUS == "not_performed"
    assert AUDIT_REPLAY_EXECUTION_STATUS == "not_performed"
    assert AUDIT_LOG_WRITE_STATUS == "not_performed"
    assert LEDGER_WRITE_STATUS == "not_performed"
    assert POLICY_ENFORCEMENT_STATUS == "not_performed"
    assert HUMAN_APPROVAL_STATUS == "not_performed"
    assert HUMAN_AUTHORIZATION_STATUS == "not_performed"
    assert SOURCE_MUTATION_APPROVAL_STATUS == "not_active"
    assert SOURCE_MUTATION_REJECTION_STATUS == "not_active"
    assert SOURCE_MUTATION_RUNTIME_STATUS == "not_active"
    assert SOURCE_MUTATION_EXECUTION_STATUS == "not_active"
    assert SOURCE_MUTATION_STATUS == "not_performed"
    assert STAR_SOURCE_MEMORY_ACTIVE_STATUS == "not_active"
    assert LAYER_15_ACTIVE_STATUS == "not_active"
    assert NEXT_STAGE == "v6_series_terminal_boundary"
    assert NEXT_STAGE_TITLE == "V6 Series Terminal Boundary"
    assert V6_TERMINAL_HANDOFF_STATUS == "v6_series_terminal_boundary_ready"
    assert result["civilization_core_stable_kernel_status"] == "pass"
    assert result["blocking_reasons"] == []


def test_deterministic_repeated_build_and_hash(result):
    repeated = build_governance_civilization_core_stable_kernel()
    assert result == repeated
    assert (
        result["deterministic_civilization_core_stable_kernel_hash"]
        == _civilization_core_stable_kernel_hash(result)
    )


def test_upstream_v6_15_handoff_verification(result):
    assert result["upstream_star_source_closure_audit_status"] == "pass"
    assert len(result["upstream_star_source_closure_audit_hash"]) == 64
    assert result["upstream_handoff_status"] == (
        "ready_for_civilization_core_stable_kernel_design"
    )
    assert result["upstream_next_stage"] == "v6.16_civilization_core_stable_kernel"
    assert result["upstream_next_stage_title"] == "Civilization Core Stable Kernel"
    assert result["upstream_star_source_closure_audit_statuses_safe"] is True
    assert result["upstream_star_source_closure_audit_required_flags_false"] is True
    assert result["upstream_safety_boundaries_clear"] is True


def test_all_twelve_records_complete_stable_and_metadata_only(result):
    records = result["civilization_core_stable_kernel_records"]
    assert REQUIRED_GOVERNANCE_CIVILIZATION_CORE_STABLE_KERNEL_RECORD_IDS == (
        EXPECTED_RECORD_IDS
    )
    assert [record["kernel_record_id"] for record in records] == list(
        EXPECTED_RECORD_IDS
    )
    assert len(records) == 12
    for record in records:
        assert record["kernel_record_status"] == "registered_metadata_only"
        assert record["introduced_in_version"] == "6.16.0"
        assert record["introduced_in_stage"] == "v6.16_civilization_core_stable_kernel"
        assert record["introduced_in_layer"] == "layer_15_star_source_memory"
        assert record["inherited_from_stage"] == "v6.15_star_source_closure_audit"
        assert record["required"] is True
        assert record["metadata_only"] is True
        assert record["civilization_core_stable_kernel_metadata_required"] is True
        assert record["metadata_only_disposition"] == "metadata_only"
        assert record["blocking_reasons"] == []
        assert record["kernel_hash"] == _kernel_hash(record)
        assert record["kernel_record_hash"] == _kernel_record_hash(record)


def test_records_and_getters_are_detached_copy_safe(result):
    record_id = EXPECTED_RECORD_IDS[0]
    first = get_governance_civilization_core_stable_kernel_record(record_id)
    second = get_governance_civilization_core_stable_kernel_record(record_id)
    first["kernel_scope"] = "changed"
    first["network_call_performed"] = True
    assert second["kernel_scope"] != "changed"
    assert second["network_call_performed"] is False
    result_records = result["civilization_core_stable_kernel_records"]
    copied_records = deepcopy(result_records)
    copied_records[0]["filesystem_write_performed"] = True
    assert result_records[0]["filesystem_write_performed"] is False


def test_unknown_getters_return_blocked_style_results():
    unknown_record = get_governance_civilization_core_stable_kernel_record("unknown")
    assert unknown_record["kernel_record_status"] == "blocked"
    assert unknown_record["required"] is False
    assert unknown_record["metadata_only"] is True
    assert unknown_record["civilization_core_stable_kernel_active"] is False
    assert unknown_record["blocking_reasons"]

    for getter, status_key in (
        (get_governance_civilization_core_stable_kernel_section, "section_status"),
        (get_governance_civilization_core_stable_kernel_contract, "contract_status"),
        (get_governance_civilization_core_stable_kernel_check, "check_status"),
    ):
        unknown = getter("unknown")
        assert unknown[status_key] == "blocked"
        assert unknown["required"] is False
        assert unknown["metadata_only"] is True
        assert unknown["civilization_core_stable_kernel_active"] is False


def test_lists_are_stable_and_all_sections_contracts_checks_pass(result):
    assert list_governance_civilization_core_stable_kernel_record_ids() == list(
        EXPECTED_RECORD_IDS
    )
    assert list_governance_civilization_core_stable_kernel_section_names() == list(
        REQUIRED_GOVERNANCE_CIVILIZATION_CORE_STABLE_KERNEL_SECTION_NAMES
    )
    assert list_governance_civilization_core_stable_kernel_contract_names() == list(
        REQUIRED_GOVERNANCE_CIVILIZATION_CORE_STABLE_KERNEL_CONTRACT_NAMES
    )
    assert list_governance_civilization_core_stable_kernel_check_names() == list(
        REQUIRED_GOVERNANCE_CIVILIZATION_CORE_STABLE_KERNEL_CHECK_NAMES
    )
    for container, status_key in (
        ("civilization_core_stable_kernel_sections", "section_status"),
        ("civilization_core_stable_kernel_contracts", "contract_status"),
        ("civilization_core_stable_kernel_checks", "check_status"),
    ):
        assert all(
            item[status_key] == "pass" and item["blocking_reasons"] == []
            for item in result[container]
        )


def test_all_safety_fields_false(result):
    for field in REQUIRED_FALSE_RECORD_FIELDS:
        assert result[field] is False
    for record in result["civilization_core_stable_kernel_records"]:
        for field in REQUIRED_FALSE_RECORD_FIELDS:
            assert record[field] is False
    for key in (*COMMON_DISABLED_FLAGS, *SAFETY_BOUNDARIES):
        assert result[key] is False


def test_no_stable_kernel_activation_runtime_execution_or_final_authority(result):
    assert result["stable_kernel_activation_status"] == "not_performed"
    assert result["stable_kernel_runtime_status"] == "not_performed"
    assert result["kernel_execution_status"] == "not_performed"
    assert result["system_finalization_status"] == "not_performed"
    assert result["final_autonomy_status"] == "not_active"
    assert result["final_authority_status"] == "not_active"
    assert result["stable_kernel_activated"] is False
    assert result["stable_kernel_runtime_created"] is False
    assert result["kernel_execution_performed"] is False
    assert result["system_finalization_performed"] is False
    assert result["final_autonomy_created"] is False
    assert result["final_authority_created"] is False


def test_no_closure_handoff_migration_stability_or_replay_execution(result):
    assert result["closure_audit_execution_status"] == "not_performed"
    assert result["closure_decision_status"] == "not_performed"
    assert result["finalization_status"] == "not_performed"
    assert result["source_handoff_execution_status"] == "not_performed"
    assert result["source_handoff_migration_status"] == "not_performed"
    assert result["source_handoff_export_status"] == "not_performed"
    assert result["source_handoff_import_status"] == "not_performed"
    assert result["memory_or_source_migration_status"] == "not_performed"
    assert result["stability_index_execution_status"] == "not_performed"
    assert result["stability_score_runtime_status"] == "not_performed"
    assert result["stability_monitoring_status"] == "not_performed"
    assert result["cross_layer_validation_execution_status"] == "not_performed"
    assert result["cross_layer_repair_status"] == "not_performed"
    assert result["audit_replay_execution_status"] == "not_performed"


def test_no_write_approval_authorization_dispatch_graph_or_network_surfaces(result):
    assert result["audit_log_write_status"] == "not_performed"
    assert result["ledger_write_status"] == "not_performed"
    assert result["human_approval_status"] == "not_performed"
    assert result["human_authorization_status"] == "not_performed"
    assert result["source_mutation_approval_status"] == "not_active"
    assert result["source_mutation_rejection_status"] == "not_active"
    assert result["source_mutation_execution_status"] == "not_active"
    assert result["source_mutation_status"] == "not_performed"
    for field in (
        "authorization_token_created",
        "authorization_grant_created",
        "approval_notification_sent",
        "adapter_dispatched",
        "manifest_dispatched",
        "source_graph_mutated",
        "memory_graph_mutated",
        "network_call_performed",
        "durable_write_performed",
        "filesystem_write_performed",
        "database_write_performed",
        "ledger_write_performed",
        "operation_ledger_entry_written",
    ):
        assert result[field] is False


def test_no_active_memory_layer_authority_identity_or_claims(result):
    assert result["star_source_memory_active_status"] == "not_active"
    assert result["layer_15_active_status"] == "not_active"
    assert result["star_source_memory_active"] is False
    assert result["layer_15_active"] is False
    for field in (
        "autonomous_authority_claim_allowed",
        "self_authorization_allowed",
        "identity_escalation_allowed",
        "personhood_claim_allowed",
        "life_claim_allowed",
        "awakening_claim_allowed",
        "legal_subject_claim_allowed",
        "religious_object_claim_allowed",
    ):
        assert result[field] is False


def test_terminal_boundary_marker_is_not_v6_17(result):
    assert result["handoff_status"] == "v6_series_terminal_boundary_ready"
    assert result["next_stage"] == "v6_series_terminal_boundary"
    assert result["next_stage_title"] == "V6 Series Terminal Boundary"
    assert result["civilization_core_stable_kernel_summary"]["next_stage_is_v6_17"] is False


def test_json_deterministic_hash_stable_and_safe_mapping_keys(result):
    payload = governance_civilization_core_stable_kernel_to_json(result)
    assert payload.endswith("\n")
    assert payload == governance_civilization_core_stable_kernel_to_json(result)
    decoded = json.loads(payload)
    assert decoded == result
    assert decoded["deterministic_civilization_core_stable_kernel_hash"] == (
        result["deterministic_civilization_core_stable_kernel_hash"]
    )

    def walk(value):
        if isinstance(value, dict):
            for key, nested in value.items():
                assert isinstance(key, str)
                walk(nested)
        elif isinstance(value, list):
            for nested in value:
                walk(nested)
        elif isinstance(value, float):
            assert math.isfinite(value)

    walk(result)


def test_no_sensitive_terms_or_old_wrong_v6_1_wording_leak():
    content = MODULE_PATH.read_text(encoding="utf-8") + SMOKE_PATH.read_text(
        encoding="utf-8"
    )
    forbidden = (
        "_".join(("governance", "improvement", "planner")),
        "_".join(("governance", "plan", "writer")),
        "_".join(("governance", "plan", "schema")),
        "_".join(("governance", "plan", "rules")),
        "_".join(("agent", "action", "surface")),
        "_".join(("v6.1", "star", "source", "provenance", "boundary", "candidate")),
        "_".join(
            (
                "ready",
                "for",
                "star",
                "source",
                "provenance",
                "boundary",
                "candidate",
                "design",
            )
        ),
        " ".join(("Star-Source", "Provenance", "Boundary", "Candidate")),
    )
    for term in forbidden:
        assert term not in content


def test_no_live_io_execution_runtime_surfaces():
    tree = ast.parse(MODULE_PATH.read_text(encoding="utf-8"))
    forbidden_calls = {"open", "exec", "eval", "compile", "__import__"}
    forbidden_imports = {
        "os",
        "socket",
        "subprocess",
        "urllib",
        "http",
        "requests",
        "pathlib",
        "sqlite3",
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                assert alias.name.split(".")[0] not in forbidden_imports
        if isinstance(node, ast.ImportFrom) and node.module:
            assert node.module.split(".")[0] not in forbidden_imports
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name):
                assert func.id not in forbidden_calls
            if isinstance(func, ast.Attribute):
                assert func.attr not in {"write", "send", "request", "connect"}


def test_no_uv_lock():
    assert not (PROJECT_ROOT / "uv.lock").exists()
