from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import json
import math
from pathlib import Path

import pytest

from hermes_memory_fabric.governance_execution_adapter_manifest_approval_gate import (
    EXECUTION_ADAPTER_MANIFEST_APPROVAL_GATE_STAGE,
    GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_APPROVAL_GATE_HASH_ALGORITHM,
    GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_APPROVAL_GATE_SCHEMA_VERSION,
    GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_APPROVAL_GATE_TYPE,
    GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_APPROVAL_GATE_VERSION,
    MANIFEST_APPROVAL_GATE_MODE,
    SAFETY_BOUNDARIES,
    STAR_COSMOS_ENTRY_STATUS,
    _execution_adapter_manifest_approval_gate_hash,
    build_governance_execution_adapter_manifest_approval_gate,
    get_governance_execution_adapter_manifest_approval_check,
    get_governance_execution_adapter_manifest_approval_contract,
    get_governance_execution_adapter_manifest_approval_decision,
    governance_execution_adapter_manifest_approval_gate_to_json,
    list_governance_execution_adapter_manifest_approval_check_names,
    list_governance_execution_adapter_manifest_approval_contract_names,
    list_governance_execution_adapter_manifest_approval_decision_names,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CORE_MODULE = (
    PROJECT_ROOT
    / "src"
    / "hermes_memory_fabric"
    / "governance_execution_adapter_manifest_approval_gate.py"
)

EXPECTED_ROLE_NAMES = [
    "governance_owner_review",
    "safety_boundary_review",
    "manifest_policy_review",
    "execution_adapter_boundary_review",
    "star_cosmos_candidate_review",
]

EXPECTED_EVIDENCE_REQUIREMENT_NAMES = [
    "manifest_policy_gate_pass_evidence",
    "deterministic_policy_gate_hash_evidence",
    "sanitized_payload_evidence",
    "candidate_only_boundary_evidence",
    "no_real_execution_evidence",
    "no_adapter_invocation_evidence",
    "no_manifest_execution_evidence",
    "no_dry_run_plan_execution_evidence",
    "no_external_call_evidence",
    "no_durable_write_evidence",
    "no_memory_graph_mutation_evidence",
    "no_operation_ledger_write_evidence",
    "no_star_cosmos_active_entry_evidence",
]

EXPECTED_BLOCKING_CONDITION_NAMES = [
    "policy_gate_blocked",
    "missing_policy_gate_hash",
    "unsafe_payload_evidence",
    "candidate_only_boundary_missing",
    "real_execution_enabled",
    "adapter_invocation_enabled",
    "manifest_execution_enabled",
    "dry_run_plan_execution_enabled",
    "external_calls_enabled",
    "durable_writes_enabled",
    "filesystem_writes_enabled",
    "database_writes_enabled",
    "memory_graph_mutation_enabled",
    "operation_ledger_writes_enabled",
    "autonomous_execution_enabled",
    "star_cosmos_active_entry_claimed",
    "real_approval_record_written",
    "approval_notification_sent",
]

EXPECTED_DECISION_NAMES = [
    "policy_gate_pass_approval_decision",
    "policy_gate_hash_approval_decision",
    "approval_request_metadata_only_decision",
    "approval_roles_declared_decision",
    "approval_evidence_requirements_declared_decision",
    "approval_blocking_conditions_declared_decision",
    "sanitized_payload_approval_decision",
    "candidate_only_approval_decision",
    "no_real_execution_approval_decision",
    "no_adapter_invocation_approval_decision",
    "no_manifest_execution_approval_decision",
    "no_dry_run_plan_execution_approval_decision",
    "no_external_call_approval_decision",
    "no_durable_write_approval_decision",
    "no_filesystem_write_approval_decision",
    "no_database_write_approval_decision",
    "no_memory_graph_mutation_approval_decision",
    "no_operation_ledger_write_approval_decision",
    "no_autonomous_execution_approval_decision",
    "no_real_approval_record_write_decision",
    "no_approval_notification_decision",
    "star_cosmos_candidate_only_approval_decision",
]

EXPECTED_CONTRACT_NAMES = [
    "approval_gate_only_contract",
    "manifest_policy_gate_pass_contract",
    "approval_request_metadata_only_contract",
    "approval_roles_declared_contract",
    "approval_evidence_requirements_declared_contract",
    "approval_blocking_conditions_declared_contract",
    "approval_decision_names_complete_contract",
    "approval_decisions_pass_contract",
    "policy_gate_hash_present_contract",
    "policy_gate_hash_stable_contract",
    "sanitized_payload_approval_contract",
    "candidate_only_approval_contract",
    "no_real_execution_approval_contract",
    "no_adapter_invocation_approval_contract",
    "no_manifest_execution_approval_contract",
    "no_dry_run_plan_execution_approval_contract",
    "no_external_call_approval_contract",
    "no_durable_write_approval_contract",
    "no_filesystem_write_approval_contract",
    "no_database_write_approval_contract",
    "no_memory_graph_mutation_approval_contract",
    "no_operation_ledger_write_approval_contract",
    "no_autonomous_execution_approval_contract",
    "no_real_approval_record_write_contract",
    "no_approval_notification_contract",
    "star_cosmos_candidate_only_approval_contract",
]

EXPECTED_CHECK_NAMES = [
    "manifest_policy_gate_pass_check",
    "manifest_approval_gate_stage_check",
    "approval_gate_only_mode_check",
    "approval_request_metadata_only_check",
    "approval_roles_declared_check",
    "approval_evidence_requirements_declared_check",
    "approval_blocking_conditions_declared_check",
    "approval_decision_names_complete_check",
    "approval_decisions_pass_check",
    "approval_contracts_pass_check",
    "policy_gate_hash_present_check",
    "policy_gate_hash_stable_check",
    "sanitized_payload_approval_check",
    "candidate_only_approval_check",
    "no_real_execution_approval_check",
    "no_adapter_invocation_approval_check",
    "no_manifest_execution_approval_check",
    "no_dry_run_plan_execution_approval_check",
    "no_external_call_approval_check",
    "no_durable_write_approval_check",
    "no_filesystem_write_approval_check",
    "no_database_write_approval_check",
    "no_memory_graph_mutation_approval_check",
    "no_operation_ledger_write_approval_check",
    "no_autonomous_execution_approval_check",
    "no_real_approval_record_write_check",
    "no_approval_notification_check",
    "star_cosmos_candidate_only_approval_check",
    "deterministic_approval_gate_hash_check",
    "approval_handoff_readiness_check",
]

COMMON_FALSE_FIELDS = (
    "star_cosmos_memory_active",
    "execution_adapter_implemented",
    "execution_adapter_invoked",
    "manifest_executed",
    "dry_run_plan_executed",
    "real_execution_enabled",
    "external_calls_enabled",
    "durable_writes_enabled",
    "filesystem_writes_enabled",
    "database_writes_enabled",
    "memory_graph_mutation_enabled",
    "operation_ledger_writes_enabled",
    "autonomous_execution_enabled",
    "approval_request_created",
    "approval_notification_sent",
    "real_approval_record_written",
)

SENSITIVE_BLOCKED_TERMS = (
    '"approval_phrase"',
    '"stdout_tail"',
    '"stdout"',
    '"stderr"',
    '"raw_logs"',
    '"token"',
    '"api_key"',
    '"secret"',
    '"password"',
    '"credential"',
    "fixture-approval-phrase",
    "fixture-stdout-tail",
    "fixture-stdout",
    "fixture-stderr",
    "fixture-raw-logs",
    "fixture-token",
    "fixture-api-key",
    "fixture-secret",
    "fixture-password",
    "fixture-credential",
)

FORBIDDEN_APPROVAL_METADATA_TERMS = (
    *SENSITIVE_BLOCKED_TERMS,
    "http://",
    "https://",
    "ssh://",
    "git@",
    "github" + ".com",
    "/Users/",
    "/private/",
    "/tmp/",
    "C:\\",
    "@example" + ".com",
    "tool_" + "call",
    "adapter_" + "dispatch",
    "manifest_" + "dispatch",
    "bash -",
    "sh -",
    "python -",
    "$(",
    "send_" + "email",
    "web" + "hook",
    "notification_" + "sender",
)

FORBIDDEN_ACTIVE_SOURCE_TERMS = (
    "sub" + "process",
    "socket",
    "requ" + "ests",
    "urllib",
    "url" + "open",
    "open(",
    ".open(",
    "write_text",
    "git " + "push",
    "g" + "h api",
    "Open" + "Claw",
    "Git" + "Hub API",
    "Composio",
    "memory_graph_mutation_" + "api",
    "adapter_" + "dispatch",
    "manifest_" + "dispatch",
    "shell commands",
    "operation-ledger write APIs",
    "create_" + "memory_write_proposal",
    "send_" + "email",
    "web" + "hook",
    "notification_" + "sender",
    "notification_" + "routing",
)

CONTAMINATION_TERMS = (
    "governance_" + "improvement_planner",
    "governance_" + "improvement_planner_activation",
    "governance_" + "plan_rules",
    "governance_" + "plan_schema",
    "governance_" + "plan_writer",
    "smoke_governance_" + "improvement_planner",
    "smoke_governance_" + "improvement_planner_activation",
    "test_governance_" + "improvement_planner",
    "test_governance_" + "improvement_planner_activation",
    "test_governance_" + "plan_writer",
    "uv" + ".lock",
)


@lru_cache(maxsize=1)
def _gate_payload() -> str:
    return governance_execution_adapter_manifest_approval_gate_to_json(
        build_governance_execution_adapter_manifest_approval_gate()
    )


def _gate() -> dict[str, object]:
    return json.loads(_gate_payload())


def _assert_safety(value: object) -> None:
    if isinstance(value, dict):
        for key in COMMON_FALSE_FIELDS:
            if key in value:
                assert value[key] is False
        boundaries = value.get("safety_boundaries")
        if isinstance(boundaries, dict):
            for key in SAFETY_BOUNDARIES:
                assert value[key] is False
                assert boundaries[key] is False
        for nested_value in value.values():
            _assert_safety(nested_value)
    elif isinstance(value, list):
        for item in value:
            _assert_safety(item)


def _assert_string_keys_and_finite_values(value: object) -> None:
    if isinstance(value, dict):
        assert all(isinstance(key, str) for key in value)
        for nested_value in value.values():
            _assert_string_keys_and_finite_values(nested_value)
    elif isinstance(value, list):
        for item in value:
            _assert_string_keys_and_finite_values(item)
    elif isinstance(value, float):
        assert math.isfinite(value)


def test_public_constants():
    assert GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_APPROVAL_GATE_VERSION == "6.1.0"
    assert (
        GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_APPROVAL_GATE_SCHEMA_VERSION
        == "6.1.0"
    )
    assert (
        GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_APPROVAL_GATE_TYPE
        == "governance_execution_adapter_manifest_approval_gate"
    )
    assert (
        GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_APPROVAL_GATE_HASH_ALGORITHM
        == "sha256"
    )
    assert (
        EXECUTION_ADAPTER_MANIFEST_APPROVAL_GATE_STAGE
        == "v5.6_execution_adapter_manifest_approval_gate_candidate"
    )
    assert MANIFEST_APPROVAL_GATE_MODE == "approval_gate_only"
    assert STAR_COSMOS_ENTRY_STATUS == "candidate_only"


def test_manifest_approval_gate_shape_is_deterministic():
    first = _gate()
    second = _gate()

    assert first == second
    assert first["version"] == "6.1.0"
    assert first["schema_version"] == "6.1.0"
    assert (
        first["manifest_approval_gate_type"]
        == "governance_execution_adapter_manifest_approval_gate"
    )
    assert first["manifest_approval_gate_status"] == "pass"
    assert (
        first["manifest_approval_gate_stage"]
        == "v5.6_execution_adapter_manifest_approval_gate_candidate"
    )
    assert first["manifest_approval_gate_mode"] == "approval_gate_only"
    assert first["star_cosmos_entry_status"] == "candidate_only"
    assert first["manifest_policy_gate_version"] == "6.1.0"
    assert first["manifest_policy_gate_status"] == "pass"
    assert isinstance(first["manifest_policy_gate_hash"], str)
    assert len(first["manifest_policy_gate_hash"]) == 64
    assert first["handoff_status"] == (
        "ready_for_future_execution_authorization_gate_design"
    )
    assert first["blocking_reasons"] == []
    assert len(first["deterministic_manifest_approval_gate_hash"]) == 64
    for key in COMMON_FALSE_FIELDS:
        assert first[key] is False
    _assert_string_keys_and_finite_values(first)


def test_approval_request_metadata_is_deterministic_and_metadata_only():
    metadata = _gate()["manifest_approval_request_metadata"]
    repeated_metadata = _gate()["manifest_approval_request_metadata"]

    assert metadata == repeated_metadata
    assert metadata["approval_request_type"] == (
        "future_execution_adapter_manifest_approval_request_metadata"
    )
    assert metadata["approval_request_mode"] == "metadata_only"
    assert metadata["approval_request_status"] == "not_created"
    assert metadata["approval_required"] is True
    assert metadata["approval_handoff_status"] == (
        "ready_for_future_execution_authorization_gate_design"
    )
    assert metadata["candidate_only"] is True
    assert metadata["execution_authorized"] is False
    assert metadata["adapter_invocation_authorized"] is False
    assert metadata["manifest_execution_authorized"] is False
    assert metadata["dry_run_plan_execution_authorized"] is False
    for key in COMMON_FALSE_FIELDS:
        if key in metadata:
            assert metadata[key] is False
    _assert_safety(metadata)


def test_approval_role_names_are_stable_and_complete():
    metadata = _gate()["manifest_approval_request_metadata"]

    assert metadata["required_approval_roles"] == EXPECTED_ROLE_NAMES


def test_approval_evidence_requirement_names_are_stable_and_complete():
    metadata = _gate()["manifest_approval_request_metadata"]

    assert (
        metadata["approval_evidence_requirements"]
        == EXPECTED_EVIDENCE_REQUIREMENT_NAMES
    )


def test_approval_blocking_condition_names_are_stable_and_complete():
    metadata = _gate()["manifest_approval_request_metadata"]

    assert (
        metadata["approval_blocking_conditions"]
        == EXPECTED_BLOCKING_CONDITION_NAMES
    )


def test_approval_decision_names_are_stable_and_complete():
    gate = _gate()

    assert (
        list_governance_execution_adapter_manifest_approval_decision_names()
        == EXPECTED_DECISION_NAMES
    )
    assert [
        decision["decision_name"]
        for decision in gate["manifest_approval_gate_decisions"]
    ] == EXPECTED_DECISION_NAMES


def test_approval_contract_names_are_stable_and_complete():
    gate = _gate()

    assert (
        list_governance_execution_adapter_manifest_approval_contract_names()
        == EXPECTED_CONTRACT_NAMES
    )
    assert [
        contract["contract_name"]
        for contract in gate["manifest_approval_gate_contracts"]
    ] == EXPECTED_CONTRACT_NAMES


def test_approval_check_names_are_stable_and_complete():
    gate = _gate()

    assert (
        list_governance_execution_adapter_manifest_approval_check_names()
        == EXPECTED_CHECK_NAMES
    )
    assert [
        check["check_name"] for check in gate["manifest_approval_gate_checks"]
    ] == EXPECTED_CHECK_NAMES


def test_get_decision_by_name_returns_detached_copies():
    first = get_governance_execution_adapter_manifest_approval_decision(
        "policy_gate_pass_approval_decision"
    )
    original = deepcopy(first)
    first["observed"]["manifest_policy_gate_status"] = "blocked"  # type: ignore[index]
    first["blocking_reasons"].append("mutated")  # type: ignore[union-attr]

    second = get_governance_execution_adapter_manifest_approval_decision(
        "policy_gate_pass_approval_decision"
    )

    assert second == original
    assert second["observed"]["manifest_policy_gate_status"] == "pass"  # type: ignore[index]
    assert second["blocking_reasons"] == []


def test_get_contract_by_name_returns_detached_copies():
    first = get_governance_execution_adapter_manifest_approval_contract(
        "approval_gate_only_contract"
    )
    original = deepcopy(first)
    first["observed"]["approval_request_created"] = True  # type: ignore[index]
    first["blocking_reasons"].append("mutated")  # type: ignore[union-attr]

    second = get_governance_execution_adapter_manifest_approval_contract(
        "approval_gate_only_contract"
    )

    assert second == original
    assert second["observed"]["approval_request_created"] is False  # type: ignore[index]
    assert second["blocking_reasons"] == []


def test_get_check_by_name_returns_detached_copies():
    first = get_governance_execution_adapter_manifest_approval_check(
        "approval_gate_only_mode_check"
    )
    original = deepcopy(first)
    first["observed"]["value"] = "mutated"  # type: ignore[index]
    first["blocking_reasons"].append("mutated")  # type: ignore[union-attr]

    second = get_governance_execution_adapter_manifest_approval_check(
        "approval_gate_only_mode_check"
    )

    assert second == original
    assert second["observed"]["value"] == "approval_gate_only"  # type: ignore[index]
    assert second["blocking_reasons"] == []


def test_unknown_decision_name_returns_blocked_style_result():
    result = get_governance_execution_adapter_manifest_approval_decision(
        "missing_decision"
    )
    second = get_governance_execution_adapter_manifest_approval_decision(
        "missing_decision"
    )

    assert result == second
    assert result["decision_name"] == "missing_decision"
    assert result["decision_type"] == "unknown_manifest_approval_decision"
    assert result["decision_status"] == "blocked"
    assert result["blocking_reasons"] == [
        "execution adapter manifest approval decision name is not recognized"
    ]


def test_unknown_contract_name_returns_blocked_style_result():
    result = get_governance_execution_adapter_manifest_approval_contract(
        "missing_contract"
    )
    second = get_governance_execution_adapter_manifest_approval_contract(
        "missing_contract"
    )

    assert result == second
    assert result["contract_name"] == "missing_contract"
    assert result["contract_type"] == "unknown_contract"
    assert result["contract_status"] == "blocked"
    assert result["expected"] == {"known_contract_name": True}
    assert result["observed"] == {
        "known_contract_name": False,
        "requested_contract_name": "missing_contract",
    }


def test_unknown_check_name_returns_blocked_style_result():
    result = get_governance_execution_adapter_manifest_approval_check(
        "missing_check"
    )
    second = get_governance_execution_adapter_manifest_approval_check(
        "missing_check"
    )

    assert result == second
    assert result["check_name"] == "missing_check"
    assert result["check_status"] == "blocked"
    assert result["expected"] == {"known_check_name": True}
    assert result["observed"] == {
        "known_check_name": False,
        "requested_check_name": "missing_check",
    }


def test_all_decisions_contracts_and_checks_pass_without_blocking_reasons():
    gate = _gate()

    assert gate["manifest_approval_gate_status"] == "pass"
    assert gate["blocking_reasons"] == []
    for decision in gate["manifest_approval_gate_decisions"]:
        assert decision["decision_status"] == "pass"
        assert decision["blocking_reasons"] == []
    for contract in gate["manifest_approval_gate_contracts"]:
        assert contract["contract_status"] == "pass"
        assert contract["blocking_reasons"] == []
    for check in gate["manifest_approval_gate_checks"]:
        assert check["check_status"] == "pass"
        assert check["blocking_reasons"] == []


def test_all_execution_write_external_call_and_approval_write_flags_remain_false():
    gate = _gate()

    for key in COMMON_FALSE_FIELDS:
        assert gate[key] is False
    _assert_safety(gate)


def test_deterministic_approval_gate_hash_is_stable_and_sensitive_to_metadata():
    gate = _gate()
    repeated = _gate()
    mutated = deepcopy(gate)
    mutated["manifest_approval_request_metadata"]["approval_request_mode"] = (  # type: ignore[index]
        "mutated"
    )

    assert gate["deterministic_manifest_approval_gate_hash"] == repeated[
        "deterministic_manifest_approval_gate_hash"
    ]
    assert _execution_adapter_manifest_approval_gate_hash(gate) == gate[
        "deterministic_manifest_approval_gate_hash"
    ]
    assert _execution_adapter_manifest_approval_gate_hash(mutated) != gate[
        "deterministic_manifest_approval_gate_hash"
    ]


def test_approval_gate_hash_is_sensitive_to_decision_contract_and_check_data():
    gate = _gate()
    decision_mutated = deepcopy(gate)
    contract_mutated = deepcopy(gate)
    check_mutated = deepcopy(gate)
    decision_mutated["manifest_approval_gate_decisions"][0]["observed"][  # type: ignore[index]
        "manifest_policy_gate_status"
    ] = "blocked"
    contract_mutated["manifest_approval_gate_contracts"][0]["observed"][  # type: ignore[index]
        "approval_request_created"
    ] = True
    check_mutated["manifest_approval_gate_checks"][0]["observed"][  # type: ignore[index]
        "manifest_policy_gate_status"
    ] = "blocked"

    assert _execution_adapter_manifest_approval_gate_hash(
        decision_mutated
    ) != gate["deterministic_manifest_approval_gate_hash"]
    assert _execution_adapter_manifest_approval_gate_hash(
        contract_mutated
    ) != gate["deterministic_manifest_approval_gate_hash"]
    assert _execution_adapter_manifest_approval_gate_hash(check_mutated) != gate[
        "deterministic_manifest_approval_gate_hash"
    ]


def test_approval_gate_json_is_deterministic():
    gate = _gate()
    payload = governance_execution_adapter_manifest_approval_gate_to_json(gate)
    repeated_payload = governance_execution_adapter_manifest_approval_gate_to_json(
        _gate()
    )

    assert payload == repeated_payload
    assert payload.endswith("\n")
    assert json.loads(payload) == gate
    assert json.dumps(json.loads(payload), allow_nan=False)


def test_approval_gate_json_rejects_non_string_keys_and_non_finite_floats():
    with pytest.raises(ValueError, match="mapping keys must be strings"):
        governance_execution_adapter_manifest_approval_gate_to_json({1: "bad"})

    with pytest.raises(ValueError, match="floats must be finite"):
        governance_execution_adapter_manifest_approval_gate_to_json(
            {"bad": math.inf}
        )


def test_no_sensitive_keys_or_values_leak():
    gate = _gate()
    protected = {
        "metadata": gate["manifest_approval_request_metadata"],
        "decisions": gate["manifest_approval_gate_decisions"],
        "contracts": gate["manifest_approval_gate_contracts"],
        "checks": gate["manifest_approval_gate_checks"],
        "summary": gate["manifest_approval_gate_summary"],
        "hashes": {
            "approval_gate": gate["deterministic_manifest_approval_gate_hash"],
            "manifest_policy_gate": gate["manifest_policy_gate_hash"],
        },
        "json": governance_execution_adapter_manifest_approval_gate_to_json(gate),
    }
    serialized = json.dumps(protected, sort_keys=True)

    for blocked in SENSITIVE_BLOCKED_TERMS:
        assert blocked not in serialized


def test_approval_metadata_and_decisions_do_not_expose_live_or_sensitive_surfaces():
    gate = _gate()
    serialized = json.dumps(
        {
            "metadata": gate["manifest_approval_request_metadata"],
            "decisions": gate["manifest_approval_gate_decisions"],
        },
        sort_keys=True,
    )

    for blocked in FORBIDDEN_APPROVAL_METADATA_TERMS:
        assert blocked not in serialized


def test_all_safety_fields_remain_false():
    _assert_safety(_gate())


def test_manifest_approval_gate_module_has_no_active_surfaces():
    source = CORE_MODULE.read_text(encoding="utf-8")

    for forbidden in FORBIDDEN_ACTIVE_SOURCE_TERMS:
        assert forbidden not in source


def test_no_unrelated_planner_or_lock_references_exist():
    search_roots = [
        PROJECT_ROOT / "pyproject.toml",
        PROJECT_ROOT / "scripts",
        PROJECT_ROOT / "src" / "hermes_memory_fabric",
        PROJECT_ROOT / "tests",
    ]
    files: list[Path] = []
    for root in search_roots:
        if root.is_file():
            files.append(root)
        else:
            files.extend(
                path
                for path in sorted(root.rglob("*"))
                if path.is_file() and path.suffix in {".py", ".toml"}
            )

    for path in files:
        text = path.read_text(encoding="utf-8")
        for forbidden in CONTAMINATION_TERMS:
            assert forbidden not in text, path
