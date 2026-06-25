from __future__ import annotations

import ast
from copy import deepcopy
import json
import math
from pathlib import Path

import pytest

from hermes_memory_fabric.governance_star_source_closure_audit import (
    AUDIT_LOG_WRITE_STATUS,
    AUDIT_REPLAY_EXECUTION_STATUS,
    COMMON_DISABLED_FLAGS,
    CROSS_LAYER_REPAIR_STATUS,
    CROSS_LAYER_VALIDATION_EXECUTION_STATUS,
    GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_HASH_ALGORITHM,
    GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_SCHEMA_VERSION,
    GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_TYPE,
    GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_VERSION,
    HUMAN_APPROVAL_STATUS,
    HUMAN_AUTHORIZATION_STATUS,
    LAYER_15_ACTIVE_STATUS,
    LEDGER_WRITE_STATUS,
    MEMORY_OR_SOURCE_MIGRATION_STATUS,
    NEXT_STAGE,
    NEXT_STAGE_TITLE,
    POLICY_ENFORCEMENT_STATUS,
    REQUIRED_GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_CHECK_NAMES,
    REQUIRED_GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_CONTRACT_NAMES,
    REQUIRED_GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_RECORD_IDS,
    REQUIRED_GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_SECTION_NAMES,
    SAFETY_BOUNDARIES,
    STAR_SOURCE_CLOSURE_AUDIT_ACTIVE_STATUS,
    STAR_SOURCE_CLOSURE_AUDIT_MODE,
    STAR_SOURCE_CLOSURE_AUDIT_STAGE,
    STAR_SOURCE_CLOSURE_AUDIT_STATUS,
    SOURCE_HANDOFF_EXECUTION_STATUS,
    SOURCE_HANDOFF_EXPORT_STATUS,
    SOURCE_HANDOFF_IMPORT_STATUS,
    SOURCE_HANDOFF_MIGRATION_STATUS,
    SOURCE_MUTATION_APPROVAL_STATUS,
    SOURCE_MUTATION_EXECUTION_STATUS,
    SOURCE_MUTATION_REJECTION_STATUS,
    SOURCE_MUTATION_RUNTIME_STATUS,
    SOURCE_MUTATION_STATUS,
    STAR_SOURCE_MEMORY_ACTIVE_STATUS,
    STABILITY_INDEX_EXECUTION_STATUS,
    CLOSURE_AUDIT_EXECUTION_STATUS,
    CLOSURE_AUDIT_STATUS,
    CLOSURE_DECISION_STATUS,
    FINALIZATION_STATUS,
    STABLE_KERNEL_ACTIVATION_STATUS,
    STABILITY_MONITORING_STATUS,
    STABILITY_SCORE_RUNTIME_STATUS,
    V6_16_HANDOFF_STATUS,
    _closure_hash,
    _closure_record_hash,
    _star_source_closure_audit_hash,
    build_governance_star_source_closure_audit,
    get_governance_star_source_closure_audit_check,
    get_governance_star_source_closure_audit_contract,
    get_governance_star_source_closure_audit_record,
    get_governance_star_source_closure_audit_section,
    governance_star_source_closure_audit_to_json,
    list_governance_star_source_closure_audit_check_names,
    list_governance_star_source_closure_audit_contract_names,
    list_governance_star_source_closure_audit_record_ids,
    list_governance_star_source_closure_audit_section_names,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = (
    PROJECT_ROOT
    / "src"
    / "hermes_memory_fabric"
    / "governance_star_source_closure_audit.py"
)
SMOKE_PATH = PROJECT_ROOT / "scripts" / "smoke_governance_star_source_closure_audit.py"

EXPECTED_RECORD_IDS = (
    "star_source_closure_audit_intake",
    "upstream_source_handoff_hash_closure_reference",
    "ordered_layer_15_closure_chain_registry",
    "star_source_closure_scope_metadata_registry",
    "star_source_closure_input_contract_registry",
    "star_source_closure_output_contract_registry",
    "no_star_source_closure_execution",
    "no_finalization_or_kernel_activation",
    "no_source_handoff_execution_or_migration",
    "no_audit_log_or_ledger_write",
    "no_source_or_memory_graph_mutation",
    "civilization_core_stable_kernel_handoff",
)

REQUIRED_FALSE_RECORD_FIELDS = (
    "star_source_closure_audit_active",
    "star_source_closure_executed",
    "closure_decision_performed",
    "finalization_performed",
    "stable_kernel_activation_performed",
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
    return build_governance_star_source_closure_audit()


def test_constants_and_public_shape(result):
    assert GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_VERSION == "6.15.0"
    assert GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_SCHEMA_VERSION == "6.15.0"
    assert (
        GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_TYPE
        == "governance_star_source_closure_audit"
    )
    assert GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_HASH_ALGORITHM == "sha256"
    assert STAR_SOURCE_CLOSURE_AUDIT_STAGE == "v6.15_star_source_closure_audit"
    assert STAR_SOURCE_CLOSURE_AUDIT_MODE == "star_source_closure_audit_only"
    assert STAR_SOURCE_CLOSURE_AUDIT_STATUS == "star_source_closure_audit_candidate_only"
    assert STAR_SOURCE_CLOSURE_AUDIT_ACTIVE_STATUS == "not_active"
    assert CLOSURE_AUDIT_STATUS == "metadata_only"
    assert CLOSURE_AUDIT_EXECUTION_STATUS == "not_performed"
    assert CLOSURE_DECISION_STATUS == "not_performed"
    assert FINALIZATION_STATUS == "not_performed"
    assert STABLE_KERNEL_ACTIVATION_STATUS == "not_performed"
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
    assert NEXT_STAGE == "v6.16_civilization_core_stable_kernel"
    assert NEXT_STAGE_TITLE == "Civilization Core Stable Kernel"
    assert V6_16_HANDOFF_STATUS == "ready_for_civilization_core_stable_kernel_design"
    assert result["star_source_closure_audit_status"] == "pass"
    assert result["blocking_reasons"] == []


def test_deterministic_repeated_build_and_hash(result):
    repeated = build_governance_star_source_closure_audit()
    assert result == repeated
    assert (
        result["deterministic_star_source_closure_audit_hash"]
        == _star_source_closure_audit_hash(result)
    )


def test_upstream_v6_14_handoff_verification(result):
    assert result["upstream_source_handoff_boundary_status"] == "pass"
    assert len(result["upstream_source_handoff_boundary_hash"]) == 64
    assert result["upstream_handoff_status"] == (
        "ready_for_star_source_closure_audit_design"
    )
    assert result["upstream_next_stage"] == "v6.15_star_source_closure_audit"
    assert result["upstream_next_stage_title"] == "Star-Source Closure Audit"
    assert result["upstream_source_handoff_boundary_statuses_safe"] is True
    assert (
        result[
            "upstream_source_handoff_boundary_required_flags_false"
        ]
        is True
    )
    assert result["upstream_safety_boundaries_clear"] is True


def test_all_twelve_records_complete_stable_and_metadata_only(result):
    records = result["star_source_closure_audit_records"]
    assert REQUIRED_GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_RECORD_IDS == (
        EXPECTED_RECORD_IDS
    )
    assert [record["closure_record_id"] for record in records] == list(
        EXPECTED_RECORD_IDS
    )
    assert len(records) == 12
    for record in records:
        assert record["closure_record_status"] == "registered_metadata_only"
        assert record["introduced_in_version"] == "6.15.0"
        assert record["introduced_in_stage"] == "v6.15_star_source_closure_audit"
        assert record["introduced_in_layer"] == "layer_15_star_source_memory"
        assert record["inherited_from_stage"] == (
            "v6.14_source_handoff_boundary"
        )
        assert record["required"] is True
        assert record["metadata_only"] is True
        assert record["star_source_closure_audit_metadata_required"] is True
        assert record["metadata_only_disposition"] == "metadata_only"
        assert record["blocking_reasons"] == []
        assert record["closure_hash"] == _closure_hash(record)
        assert record["closure_record_hash"] == _closure_record_hash(record)


def test_records_and_getters_are_detached_copy_safe(result):
    record_id = EXPECTED_RECORD_IDS[0]
    first = get_governance_star_source_closure_audit_record(record_id)
    second = get_governance_star_source_closure_audit_record(record_id)
    first["closure_scope"] = "changed"
    first["network_call_performed"] = True
    assert second["closure_scope"] != "changed"
    assert second["network_call_performed"] is False
    assert result["star_source_closure_audit_records"][0] != first

    for getter, name in (
        (
            get_governance_star_source_closure_audit_section,
            REQUIRED_GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_SECTION_NAMES[0],
        ),
        (
            get_governance_star_source_closure_audit_contract,
            REQUIRED_GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_CONTRACT_NAMES[0],
        ),
        (
            get_governance_star_source_closure_audit_check,
            REQUIRED_GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_CHECK_NAMES[0],
        ),
    ):
        observed = getter(name)
        baseline = deepcopy(observed)
        observed["blocking_reasons"].append("changed")
        assert getter(name) == baseline


@pytest.mark.parametrize(
    ("getter", "status_key"),
    (
        (
            get_governance_star_source_closure_audit_record,
            "closure_record_status",
        ),
        (
            get_governance_star_source_closure_audit_section,
            "section_status",
        ),
        (
            get_governance_star_source_closure_audit_contract,
            "contract_status",
        ),
        (
            get_governance_star_source_closure_audit_check,
            "check_status",
        ),
    ),
)
def test_unknown_getters_are_blocked(getter, status_key):
    first = getter("unknown")
    second = getter("unknown")
    assert first == second
    assert first[status_key] == "blocked"
    assert first["blocking_reasons"]


def test_lists_are_stable_and_detached():
    observed = (
        list_governance_star_source_closure_audit_record_ids(),
        list_governance_star_source_closure_audit_section_names(),
        list_governance_star_source_closure_audit_contract_names(),
        list_governance_star_source_closure_audit_check_names(),
    )
    expected = (
        list(REQUIRED_GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_RECORD_IDS),
        list(REQUIRED_GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_SECTION_NAMES),
        list(REQUIRED_GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_CONTRACT_NAMES),
        list(REQUIRED_GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_CHECK_NAMES),
    )
    assert observed == expected
    observed[0].append("changed")
    assert list_governance_star_source_closure_audit_record_ids() == expected[0]


def test_all_sections_contracts_and_checks_pass(result):
    for container, name_key, status_key, expected_names in (
        (
            "star_source_closure_audit_sections",
            "section_name",
            "section_status",
            REQUIRED_GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_SECTION_NAMES,
        ),
        (
            "star_source_closure_audit_contracts",
            "contract_name",
            "contract_status",
            REQUIRED_GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_CONTRACT_NAMES,
        ),
        (
            "star_source_closure_audit_checks",
            "check_name",
            "check_status",
            REQUIRED_GOVERNANCE_STAR_SOURCE_CLOSURE_AUDIT_CHECK_NAMES,
        ),
    ):
        items = result[container]
        assert [item[name_key] for item in items] == list(expected_names)
        assert all(
            item[status_key] == "pass" and item["blocking_reasons"] == []
            for item in items
        )


def _assert_false_safety_fields(value):
    if isinstance(value, dict):
        for key in (*COMMON_DISABLED_FLAGS, *SAFETY_BOUNDARIES):
            if key in value:
                assert value[key] is False, key
        for nested in value.values():
            _assert_false_safety_fields(nested)
    elif isinstance(value, list):
        for nested in value:
            _assert_false_safety_fields(nested)


def test_all_safety_fields_false(result):
    _assert_false_safety_fields(result)
    for record in result["star_source_closure_audit_records"]:
        for field_name in REQUIRED_FALSE_RECORD_FIELDS:
            assert record[field_name] is False


def test_no_integrity_write_approval_authorization_dispatch_or_mutation(result):
    expected_statuses = {
        "star_source_closure_audit_active_status": "not_active",
        "closure_audit_status": "metadata_only",
        "closure_audit_execution_status": "not_performed",
        "closure_decision_status": "not_performed",
        "finalization_status": "not_performed",
        "stable_kernel_activation_status": "not_performed",
        "source_handoff_execution_status": "not_performed",
        "source_handoff_migration_status": "not_performed",
        "source_handoff_export_status": "not_performed",
        "source_handoff_import_status": "not_performed",
        "memory_or_source_migration_status": "not_performed",
        "stability_index_execution_status": "not_performed",
        "stability_score_runtime_status": "not_performed",
        "stability_monitoring_status": "not_performed",
        "cross_layer_validation_execution_status": "not_performed",
        "cross_layer_repair_status": "not_performed",
        "audit_replay_execution_status": "not_performed",
        "audit_log_write_status": "not_performed",
        "ledger_write_status": "not_performed",
        "policy_enforcement_status": "not_performed",
        "human_approval_status": "not_performed",
        "human_authorization_status": "not_performed",
        "source_mutation_approval_status": "not_active",
        "source_mutation_rejection_status": "not_active",
        "source_mutation_runtime_status": "not_active",
        "source_mutation_execution_status": "not_active",
        "source_mutation_status": "not_performed",
        "star_source_memory_active_status": "not_active",
        "layer_15_active_status": "not_active",
        "handoff_status": "ready_for_civilization_core_stable_kernel_design",
        "next_stage": "v6.16_civilization_core_stable_kernel",
        "next_stage_title": "Civilization Core Stable Kernel",
    }
    for key, value in expected_statuses.items():
        assert result[key] == value
    for field_name in REQUIRED_FALSE_RECORD_FIELDS:
        assert result[field_name] is False


def test_json_is_deterministic_and_rejects_non_finite(result):
    first = governance_star_source_closure_audit_to_json(result)
    second = governance_star_source_closure_audit_to_json(result)
    assert first == second
    assert first.endswith("\n")
    assert first == json.dumps(
        result,
        ensure_ascii=True,
        indent=2,
        sort_keys=True,
        allow_nan=False,
    ) + "\n"
    with pytest.raises(ValueError):
        governance_star_source_closure_audit_to_json({"value": math.nan})
    with pytest.raises(TypeError):
        governance_star_source_closure_audit_to_json({1: "invalid"})


def test_no_sensitive_terms_leak(result):
    payload = governance_star_source_closure_audit_to_json(result).lower()
    sensitive_terms = (
        "api_" + "key",
        "pass" + "word",
        "creden" + "tial",
        "raw_" + "logs",
        "stdout",
        "stderr",
        "network_" + "target",
        "source_" + "record_payload",
        "operation_" + "ledger_entry_payload",
        "http" + "://",
        "https" + "://",
        "/users/",
        "/private/",
        "/tmp/",
    )
    for term in sensitive_terms:
        assert term not in payload


def test_core_module_has_no_live_io_execution_runtime_surfaces():
    source = MODULE_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported_roots = {
        alias.name.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    imported_roots.update(
        node.module.split(".")[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module
    )
    forbidden_imports = {
        "asyncio",
        "http",
        "os",
        "pathlib",
        "requests",
        "shutil",
        "socket",
        "sqlite3",
        "subprocess",
        "urllib",
    }
    assert imported_roots.isdisjoint(forbidden_imports)
    called_names = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    assert called_names.isdisjoint({"open", "exec", "eval", "compile"})


def test_no_forbidden_contamination_or_obsolete_wording():
    paths = (MODULE_PATH, SMOKE_PATH, Path(__file__))
    forbidden_terms = (
        "governance_improvement_" + "planner",
        "governance_plan_" + "writer",
        "governance_plan_" + "schema",
        "governance_plan_" + "rules",
        "agent_action_" + "surface",
        "v6.1_star_source_" + "provenance_boundary_candidate",
        "ready_for_star_source_" + "provenance_boundary_candidate_design",
        "Star-Source Provenance " + "Boundary Candidate",
    )
    for path in paths:
        source = path.read_text(encoding="utf-8")
        for term in forbidden_terms:
            assert term not in source
    assert not (PROJECT_ROOT / "uv.lock").exists()
