from __future__ import annotations

import ast
from copy import deepcopy
import json
import math
from pathlib import Path

import pytest

from hermes_memory_fabric.governance_civilization_core_stability_index import (
    AUDIT_LOG_WRITE_STATUS,
    AUDIT_REPLAY_EXECUTION_STATUS,
    COMMON_DISABLED_FLAGS,
    CROSS_LAYER_REPAIR_STATUS,
    CROSS_LAYER_VALIDATION_EXECUTION_STATUS,
    GOVERNANCE_CIVILIZATION_CORE_STABILITY_INDEX_HASH_ALGORITHM,
    GOVERNANCE_CIVILIZATION_CORE_STABILITY_INDEX_SCHEMA_VERSION,
    GOVERNANCE_CIVILIZATION_CORE_STABILITY_INDEX_TYPE,
    GOVERNANCE_CIVILIZATION_CORE_STABILITY_INDEX_VERSION,
    HUMAN_APPROVAL_STATUS,
    HUMAN_AUTHORIZATION_STATUS,
    LAYER_15_ACTIVE_STATUS,
    LEDGER_WRITE_STATUS,
    NEXT_STAGE,
    NEXT_STAGE_TITLE,
    POLICY_ENFORCEMENT_STATUS,
    REQUIRED_GOVERNANCE_CIVILIZATION_CORE_STABILITY_INDEX_CHECK_NAMES,
    REQUIRED_GOVERNANCE_CIVILIZATION_CORE_STABILITY_INDEX_CONTRACT_NAMES,
    REQUIRED_GOVERNANCE_CIVILIZATION_CORE_STABILITY_INDEX_RECORD_IDS,
    REQUIRED_GOVERNANCE_CIVILIZATION_CORE_STABILITY_INDEX_SECTION_NAMES,
    SAFETY_BOUNDARIES,
    CIVILIZATION_CORE_STABILITY_INDEX_ACTIVE_STATUS,
    CIVILIZATION_CORE_STABILITY_INDEX_MODE,
    CIVILIZATION_CORE_STABILITY_INDEX_STAGE,
    CIVILIZATION_CORE_STABILITY_INDEX_STATUS,
    SOURCE_MUTATION_APPROVAL_STATUS,
    SOURCE_MUTATION_EXECUTION_STATUS,
    SOURCE_MUTATION_REJECTION_STATUS,
    SOURCE_MUTATION_RUNTIME_STATUS,
    SOURCE_MUTATION_STATUS,
    STAR_SOURCE_MEMORY_ACTIVE_STATUS,
    STABILITY_INDEX_EXECUTION_STATUS,
    STABILITY_INDEX_STATUS,
    STABILITY_MONITORING_STATUS,
    STABILITY_SCORE_RUNTIME_STATUS,
    V6_14_HANDOFF_STATUS,
    _stability_hash,
    _stability_record_hash,
    _civilization_core_stability_index_hash,
    build_governance_civilization_core_stability_index,
    get_governance_civilization_core_stability_index_check,
    get_governance_civilization_core_stability_index_contract,
    get_governance_civilization_core_stability_index_record,
    get_governance_civilization_core_stability_index_section,
    governance_civilization_core_stability_index_to_json,
    list_governance_civilization_core_stability_index_check_names,
    list_governance_civilization_core_stability_index_contract_names,
    list_governance_civilization_core_stability_index_record_ids,
    list_governance_civilization_core_stability_index_section_names,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = (
    PROJECT_ROOT
    / "src"
    / "hermes_memory_fabric"
    / "governance_civilization_core_stability_index.py"
)
SMOKE_PATH = PROJECT_ROOT / "scripts" / "smoke_governance_civilization_core_stability_index.py"

EXPECTED_RECORD_IDS = (
    "civilization_core_stability_index_intake",
    "upstream_integrity_validator_hash_stability_reference",
    "ordered_layer_15_stability_chain_registry",
    "stability_scope_metadata_registry",
    "stability_input_contract_registry",
    "stability_output_contract_registry",
    "no_stability_index_execution",
    "no_live_stability_scoring_or_monitoring",
    "no_cross_layer_repair_or_mutation",
    "no_audit_log_or_ledger_write",
    "no_source_or_memory_graph_mutation",
    "source_handoff_boundary_handoff",
)

REQUIRED_FALSE_RECORD_FIELDS = (
    "stability_index_active",
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
    return build_governance_civilization_core_stability_index()


def test_constants_and_public_shape(result):
    assert GOVERNANCE_CIVILIZATION_CORE_STABILITY_INDEX_VERSION == "6.13.0"
    assert GOVERNANCE_CIVILIZATION_CORE_STABILITY_INDEX_SCHEMA_VERSION == "6.13.0"
    assert (
        GOVERNANCE_CIVILIZATION_CORE_STABILITY_INDEX_TYPE
        == "governance_civilization_core_stability_index"
    )
    assert GOVERNANCE_CIVILIZATION_CORE_STABILITY_INDEX_HASH_ALGORITHM == "sha256"
    assert CIVILIZATION_CORE_STABILITY_INDEX_STAGE == "v6.13_civilization_core_stability_index"
    assert CIVILIZATION_CORE_STABILITY_INDEX_MODE == "civilization_core_stability_index_only"
    assert CIVILIZATION_CORE_STABILITY_INDEX_STATUS == "stability_index_candidate_only"
    assert CIVILIZATION_CORE_STABILITY_INDEX_ACTIVE_STATUS == "not_active"
    assert STABILITY_INDEX_STATUS == "metadata_only"
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
    assert NEXT_STAGE == "v6.14_source_handoff_boundary"
    assert NEXT_STAGE_TITLE == "Source Handoff Boundary"
    assert V6_14_HANDOFF_STATUS == "ready_for_source_handoff_boundary_design"
    assert result["civilization_core_stability_index_status"] == "pass"
    assert result["blocking_reasons"] == []


def test_deterministic_repeated_build_and_hash(result):
    repeated = build_governance_civilization_core_stability_index()
    assert result == repeated
    assert (
        result["deterministic_civilization_core_stability_index_hash"]
        == _civilization_core_stability_index_hash(result)
    )


def test_upstream_v6_12_handoff_verification(result):
    assert result["upstream_cross_layer_integrity_validator_status"] == "pass"
    assert len(result["upstream_cross_layer_integrity_validator_hash"]) == 64
    assert result["upstream_handoff_status"] == (
        "ready_for_civilization_core_stability_index_design"
    )
    assert result["upstream_next_stage"] == "v6.13_civilization_core_stability_index"
    assert result["upstream_next_stage_title"] == "Civilization Core Stability Index"
    assert result["upstream_cross_layer_integrity_validator_statuses_safe"] is True
    assert (
        result[
            "upstream_cross_layer_integrity_validator_required_flags_false"
        ]
        is True
    )
    assert result["upstream_safety_boundaries_clear"] is True


def test_all_twelve_records_complete_stable_and_metadata_only(result):
    records = result["civilization_core_stability_records"]
    assert REQUIRED_GOVERNANCE_CIVILIZATION_CORE_STABILITY_INDEX_RECORD_IDS == (
        EXPECTED_RECORD_IDS
    )
    assert [record["stability_record_id"] for record in records] == list(
        EXPECTED_RECORD_IDS
    )
    assert len(records) == 12
    for record in records:
        assert record["stability_record_status"] == "registered_metadata_only"
        assert record["introduced_in_version"] == "6.13.0"
        assert record["introduced_in_stage"] == "v6.13_civilization_core_stability_index"
        assert record["introduced_in_layer"] == "layer_15_star_source_memory"
        assert record["inherited_from_stage"] == (
            "v6.12_cross_layer_integrity_validator"
        )
        assert record["required"] is True
        assert record["metadata_only"] is True
        assert record["civilization_core_stability_metadata_required"] is True
        assert record["metadata_only_disposition"] == "metadata_only"
        assert record["blocking_reasons"] == []
        assert record["stability_hash"] == _stability_hash(record)
        assert record["stability_record_hash"] == _stability_record_hash(record)


def test_records_and_getters_are_detached_copy_safe(result):
    record_id = EXPECTED_RECORD_IDS[0]
    first = get_governance_civilization_core_stability_index_record(record_id)
    second = get_governance_civilization_core_stability_index_record(record_id)
    first["stability_scope"] = "changed"
    first["network_call_performed"] = True
    assert second["stability_scope"] != "changed"
    assert second["network_call_performed"] is False
    assert result["civilization_core_stability_records"][0] != first

    for getter, name in (
        (
            get_governance_civilization_core_stability_index_section,
            REQUIRED_GOVERNANCE_CIVILIZATION_CORE_STABILITY_INDEX_SECTION_NAMES[0],
        ),
        (
            get_governance_civilization_core_stability_index_contract,
            REQUIRED_GOVERNANCE_CIVILIZATION_CORE_STABILITY_INDEX_CONTRACT_NAMES[0],
        ),
        (
            get_governance_civilization_core_stability_index_check,
            REQUIRED_GOVERNANCE_CIVILIZATION_CORE_STABILITY_INDEX_CHECK_NAMES[0],
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
            get_governance_civilization_core_stability_index_record,
            "stability_record_status",
        ),
        (
            get_governance_civilization_core_stability_index_section,
            "section_status",
        ),
        (
            get_governance_civilization_core_stability_index_contract,
            "contract_status",
        ),
        (
            get_governance_civilization_core_stability_index_check,
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
        list_governance_civilization_core_stability_index_record_ids(),
        list_governance_civilization_core_stability_index_section_names(),
        list_governance_civilization_core_stability_index_contract_names(),
        list_governance_civilization_core_stability_index_check_names(),
    )
    expected = (
        list(REQUIRED_GOVERNANCE_CIVILIZATION_CORE_STABILITY_INDEX_RECORD_IDS),
        list(REQUIRED_GOVERNANCE_CIVILIZATION_CORE_STABILITY_INDEX_SECTION_NAMES),
        list(REQUIRED_GOVERNANCE_CIVILIZATION_CORE_STABILITY_INDEX_CONTRACT_NAMES),
        list(REQUIRED_GOVERNANCE_CIVILIZATION_CORE_STABILITY_INDEX_CHECK_NAMES),
    )
    assert observed == expected
    observed[0].append("changed")
    assert list_governance_civilization_core_stability_index_record_ids() == expected[0]


def test_all_sections_contracts_and_checks_pass(result):
    for container, name_key, status_key, expected_names in (
        (
            "civilization_core_stability_sections",
            "section_name",
            "section_status",
            REQUIRED_GOVERNANCE_CIVILIZATION_CORE_STABILITY_INDEX_SECTION_NAMES,
        ),
        (
            "civilization_core_stability_contracts",
            "contract_name",
            "contract_status",
            REQUIRED_GOVERNANCE_CIVILIZATION_CORE_STABILITY_INDEX_CONTRACT_NAMES,
        ),
        (
            "civilization_core_stability_checks",
            "check_name",
            "check_status",
            REQUIRED_GOVERNANCE_CIVILIZATION_CORE_STABILITY_INDEX_CHECK_NAMES,
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
    for record in result["civilization_core_stability_records"]:
        for field_name in REQUIRED_FALSE_RECORD_FIELDS:
            assert record[field_name] is False


def test_no_integrity_write_approval_authorization_dispatch_or_mutation(result):
    expected_statuses = {
        "civilization_core_stability_index_active_status": "not_active",
        "stability_index_status": "metadata_only",
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
        "handoff_status": "ready_for_source_handoff_boundary_design",
        "next_stage": "v6.14_source_handoff_boundary",
        "next_stage_title": "Source Handoff Boundary",
    }
    for key, value in expected_statuses.items():
        assert result[key] == value
    for field_name in REQUIRED_FALSE_RECORD_FIELDS:
        assert result[field_name] is False


def test_json_is_deterministic_and_rejects_non_finite(result):
    first = governance_civilization_core_stability_index_to_json(result)
    second = governance_civilization_core_stability_index_to_json(result)
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
        governance_civilization_core_stability_index_to_json({"value": math.nan})
    with pytest.raises(TypeError):
        governance_civilization_core_stability_index_to_json({1: "invalid"})


def test_no_sensitive_terms_leak(result):
    payload = governance_civilization_core_stability_index_to_json(result).lower()
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
