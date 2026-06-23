from __future__ import annotations

import ast
from copy import deepcopy
import json
import math
from pathlib import Path

import pytest

from hermes_memory_fabric.governance_human_sovereignty_lock import (
    COMMON_DISABLED_FLAGS,
    GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_HASH_ALGORITHM,
    GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_SCHEMA_VERSION,
    GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_TYPE,
    GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_VERSION,
    HUMAN_APPROVAL_STATUS,
    HUMAN_AUTHORIZATION_STATUS,
    HUMAN_SOVEREIGNTY_LOCK_ACTIVE_STATUS,
    HUMAN_SOVEREIGNTY_LOCK_MODE,
    HUMAN_SOVEREIGNTY_LOCK_STAGE,
    HUMAN_SOVEREIGNTY_LOCK_STATUS,
    LAYER_15_ACTIVE_STATUS,
    NEXT_STAGE,
    NEXT_STAGE_TITLE,
    REQUIRED_GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_CHECK_NAMES,
    REQUIRED_GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_CONTRACT_NAMES,
    REQUIRED_GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_RECORD_IDS,
    REQUIRED_GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_SECTION_NAMES,
    SAFETY_BOUNDARIES,
    SOURCE_MUTATION_APPROVAL_STATUS,
    SOURCE_MUTATION_EXECUTION_STATUS,
    SOURCE_MUTATION_REJECTION_STATUS,
    SOURCE_MUTATION_RUNTIME_STATUS,
    SOURCE_MUTATION_STATUS,
    STAR_SOURCE_MEMORY_ACTIVE_STATUS,
    V6_10_HANDOFF_STATUS,
    _human_sovereignty_lock_hash,
    _lock_hash,
    _lock_record_hash,
    build_governance_human_sovereignty_lock,
    get_governance_human_sovereignty_lock_check,
    get_governance_human_sovereignty_lock_contract,
    get_governance_human_sovereignty_lock_record,
    get_governance_human_sovereignty_lock_section,
    governance_human_sovereignty_lock_to_json,
    list_governance_human_sovereignty_lock_check_names,
    list_governance_human_sovereignty_lock_contract_names,
    list_governance_human_sovereignty_lock_record_ids,
    list_governance_human_sovereignty_lock_section_names,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = (
    PROJECT_ROOT
    / "src"
    / "hermes_memory_fabric"
    / "governance_human_sovereignty_lock.py"
)

EXPECTED_RECORD_IDS = (
    "human_sovereignty_lock_intake",
    "explicit_human_sovereignty_required",
    "no_substitute_human_approval",
    "no_automatic_approval",
    "no_automatic_rejection",
    "no_authorization_token_creation",
    "no_source_mutation_execution",
    "no_source_or_memory_graph_mutation",
    "no_active_star_source_memory",
    "no_autonomous_authority",
    "audit_replay_required_before_unlock",
    "anti_overreach_firewall_handoff",
)

REQUIRED_FALSE_RECORD_FIELDS = (
    "lock_active",
    "human_approval_performed",
    "human_authorization_performed",
    "source_mutation_approval_performed",
    "source_mutation_rejection_performed",
    "source_mutation_execution_created",
    "source_mutation_performed",
    "source_graph_mutated",
    "memory_graph_mutated",
    "real_ledger_write_performed",
    "operation_ledger_entry_written",
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
    return build_governance_human_sovereignty_lock()


def test_constants_and_public_shape(result):
    assert GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_VERSION == "6.9.0"
    assert GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_SCHEMA_VERSION == "6.9.0"
    assert (
        GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_TYPE
        == "governance_human_sovereignty_lock"
    )
    assert GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_HASH_ALGORITHM == "sha256"
    assert HUMAN_SOVEREIGNTY_LOCK_STAGE == "v6.9_human_sovereignty_lock"
    assert HUMAN_SOVEREIGNTY_LOCK_MODE == "human_sovereignty_lock_only"
    assert HUMAN_SOVEREIGNTY_LOCK_STATUS == "lock_candidate_only"
    assert HUMAN_SOVEREIGNTY_LOCK_ACTIVE_STATUS == "not_active"
    assert HUMAN_APPROVAL_STATUS == "not_performed"
    assert HUMAN_AUTHORIZATION_STATUS == "not_performed"
    assert SOURCE_MUTATION_APPROVAL_STATUS == "not_active"
    assert SOURCE_MUTATION_REJECTION_STATUS == "not_active"
    assert SOURCE_MUTATION_RUNTIME_STATUS == "not_active"
    assert SOURCE_MUTATION_EXECUTION_STATUS == "not_active"
    assert SOURCE_MUTATION_STATUS == "not_performed"
    assert STAR_SOURCE_MEMORY_ACTIVE_STATUS == "not_active"
    assert LAYER_15_ACTIVE_STATUS == "not_active"
    assert NEXT_STAGE == "v6.10_anti_overreach_governance_firewall"
    assert NEXT_STAGE_TITLE == "Anti-Overreach Governance Firewall"
    assert (
        V6_10_HANDOFF_STATUS
        == "ready_for_anti_overreach_governance_firewall_design"
    )
    assert result["human_sovereignty_lock_status"] == "pass"
    assert result["blocking_reasons"] == []


def test_deterministic_repeated_build_and_hash(result):
    repeated = build_governance_human_sovereignty_lock()
    assert result == repeated
    assert (
        result["deterministic_human_sovereignty_lock_hash"]
        == _human_sovereignty_lock_hash(result)
    )


def test_upstream_v6_8_handoff_verification(result):
    assert result["upstream_source_mutation_review_gate_status"] == "pass"
    assert len(result["upstream_source_mutation_review_gate_hash"]) == 64
    assert result["upstream_handoff_status"] == (
        "ready_for_human_sovereignty_lock_design"
    )
    assert result["upstream_next_stage"] == "v6.9_human_sovereignty_lock"
    assert result["upstream_next_stage_title"] == "Human Sovereignty Lock"
    assert (
        result["upstream_source_mutation_review_gate_statuses_safe"] is True
    )
    assert (
        result[
            "upstream_source_mutation_review_gate_required_flags_false"
        ]
        is True
    )
    assert result["upstream_safety_boundaries_clear"] is True


def test_all_twelve_records_complete_stable_and_metadata_only(result):
    records = result["human_sovereignty_lock_records"]
    assert REQUIRED_GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_RECORD_IDS == (
        EXPECTED_RECORD_IDS
    )
    assert [record["lock_record_id"] for record in records] == list(
        EXPECTED_RECORD_IDS
    )
    assert len(records) == 12
    for record in records:
        assert record["lock_record_status"] == "registered_metadata_only"
        assert record["introduced_in_version"] == "6.9.0"
        assert record["introduced_in_stage"] == (
            "v6.9_human_sovereignty_lock"
        )
        assert record["introduced_in_layer"] == "layer_15_star_source_memory"
        assert record["inherited_from_stage"] == (
            "v6.8_source_mutation_review_gate"
        )
        assert record["required"] is True
        assert record["human_sovereignty_required"] is True
        assert record["explicit_human_review_required"] is True
        assert record["metadata_only"] is True
        assert record["blocking_reasons"] == []
        assert record["lock_hash"] == _lock_hash(record)
        assert record["lock_record_hash"] == _lock_record_hash(record)


def test_records_and_getters_are_detached_copy_safe(result):
    record_id = EXPECTED_RECORD_IDS[0]
    first = get_governance_human_sovereignty_lock_record(record_id)
    second = get_governance_human_sovereignty_lock_record(record_id)
    first["lock_scope"] = "changed"
    first["network_call_performed"] = True
    assert second["lock_scope"] != "changed"
    assert second["network_call_performed"] is False
    assert result["human_sovereignty_lock_records"][0] != first

    for getter, name in (
        (
            get_governance_human_sovereignty_lock_section,
            REQUIRED_GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_SECTION_NAMES[0],
        ),
        (
            get_governance_human_sovereignty_lock_contract,
            REQUIRED_GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_CONTRACT_NAMES[0],
        ),
        (
            get_governance_human_sovereignty_lock_check,
            REQUIRED_GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_CHECK_NAMES[0],
        ),
    ):
        observed = getter(name)
        baseline = deepcopy(observed)
        observed["blocking_reasons"].append("changed")
        assert getter(name) == baseline


@pytest.mark.parametrize(
    ("getter", "status_key"),
    (
        (get_governance_human_sovereignty_lock_record, "lock_record_status"),
        (get_governance_human_sovereignty_lock_section, "section_status"),
        (get_governance_human_sovereignty_lock_contract, "contract_status"),
        (get_governance_human_sovereignty_lock_check, "check_status"),
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
        list_governance_human_sovereignty_lock_record_ids(),
        list_governance_human_sovereignty_lock_section_names(),
        list_governance_human_sovereignty_lock_contract_names(),
        list_governance_human_sovereignty_lock_check_names(),
    )
    expected = (
        list(REQUIRED_GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_RECORD_IDS),
        list(REQUIRED_GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_SECTION_NAMES),
        list(REQUIRED_GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_CONTRACT_NAMES),
        list(REQUIRED_GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_CHECK_NAMES),
    )
    assert observed == expected
    observed[0].append("changed")
    assert (
        list_governance_human_sovereignty_lock_record_ids()
        == expected[0]
    )


def test_all_sections_contracts_and_checks_pass(result):
    for container, name_key, status_key, expected_names in (
        (
            "human_sovereignty_lock_sections",
            "section_name",
            "section_status",
            REQUIRED_GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_SECTION_NAMES,
        ),
        (
            "human_sovereignty_lock_contracts",
            "contract_name",
            "contract_status",
            REQUIRED_GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_CONTRACT_NAMES,
        ),
        (
            "human_sovereignty_lock_checks",
            "check_name",
            "check_status",
            REQUIRED_GOVERNANCE_HUMAN_SOVEREIGNTY_LOCK_CHECK_NAMES,
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
    for record in result["human_sovereignty_lock_records"]:
        for field_name in REQUIRED_FALSE_RECORD_FIELDS:
            assert record[field_name] is False


def test_status_and_handoff_contract(result):
    expected_statuses = {
        "human_sovereignty_lock_active_status": "not_active",
        "human_approval_status": "not_performed",
        "human_authorization_status": "not_performed",
        "source_mutation_approval_status": "not_active",
        "source_mutation_rejection_status": "not_active",
        "source_mutation_runtime_status": "not_active",
        "source_mutation_execution_status": "not_active",
        "source_mutation_status": "not_performed",
        "star_source_memory_active_status": "not_active",
        "layer_15_active_status": "not_active",
        "personhood_claim_status": "forbidden",
        "life_claim_status": "forbidden",
        "awakening_claim_status": "forbidden",
        "legal_subject_claim_status": "forbidden",
        "religious_object_claim_status": "forbidden",
        "autonomous_authority_status": "forbidden",
        "identity_escalation_status": "forbidden",
        "handoff_status": (
            "ready_for_anti_overreach_governance_firewall_design"
        ),
        "next_stage": "v6.10_anti_overreach_governance_firewall",
        "next_stage_title": "Anti-Overreach Governance Firewall",
    }
    for key, value in expected_statuses.items():
        assert result[key] == value


def test_json_is_deterministic_and_rejects_non_finite(result):
    first = governance_human_sovereignty_lock_to_json(result)
    second = governance_human_sovereignty_lock_to_json(result)
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
        governance_human_sovereignty_lock_to_json({"value": math.nan})
    with pytest.raises(TypeError):
        governance_human_sovereignty_lock_to_json({1: "invalid"})


def test_no_sensitive_terms_leak(result):
    payload = governance_human_sovereignty_lock_to_json(result).lower()
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
    paths = (
        MODULE_PATH,
        PROJECT_ROOT / "scripts" / "smoke_governance_human_sovereignty_lock.py",
        Path(__file__),
    )
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
