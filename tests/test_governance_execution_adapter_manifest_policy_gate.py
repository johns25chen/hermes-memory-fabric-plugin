from __future__ import annotations

from copy import deepcopy
from functools import lru_cache
import json
import math
from pathlib import Path

import pytest

from hermes_memory_fabric.governance_execution_adapter_manifest_policy_gate import (
    EXECUTION_ADAPTER_MANIFEST_POLICY_GATE_STAGE,
    GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_POLICY_GATE_HASH_ALGORITHM,
    GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_POLICY_GATE_SCHEMA_VERSION,
    GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_POLICY_GATE_TYPE,
    GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_POLICY_GATE_VERSION,
    MANIFEST_POLICY_GATE_MODE,
    SAFETY_BOUNDARIES,
    STAR_COSMOS_ENTRY_STATUS,
    _execution_adapter_manifest_policy_gate_hash,
    build_governance_execution_adapter_manifest_policy_gate,
    get_governance_execution_adapter_manifest_policy_check,
    get_governance_execution_adapter_manifest_policy_contract,
    get_governance_execution_adapter_manifest_policy_decision,
    governance_execution_adapter_manifest_policy_gate_to_json,
    list_governance_execution_adapter_manifest_policy_check_names,
    list_governance_execution_adapter_manifest_policy_contract_names,
    list_governance_execution_adapter_manifest_policy_decision_names,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CORE_MODULE = (
    PROJECT_ROOT
    / "src"
    / "hermes_memory_fabric"
    / "governance_execution_adapter_manifest_policy_gate.py"
)

EXPECTED_DECISION_NAMES = [
    "validation_matrix_pass_policy_decision",
    "validation_rows_pass_policy_decision",
    "validation_contracts_pass_policy_decision",
    "validation_checks_pass_policy_decision",
    "deterministic_hash_policy_decision",
    "sanitized_payload_policy_decision",
    "candidate_only_policy_decision",
    "safety_boundary_policy_decision",
    "no_real_execution_policy_decision",
    "no_adapter_invocation_policy_decision",
    "no_manifest_execution_policy_decision",
    "no_dry_run_plan_execution_policy_decision",
    "no_external_call_policy_decision",
    "no_durable_write_policy_decision",
    "no_filesystem_write_policy_decision",
    "no_database_write_policy_decision",
    "no_memory_graph_mutation_policy_decision",
    "no_operation_ledger_write_policy_decision",
    "no_autonomous_execution_policy_decision",
    "star_cosmos_candidate_only_policy_decision",
]

EXPECTED_CONTRACT_NAMES = [
    "policy_gate_only_contract",
    "manifest_validation_matrix_pass_contract",
    "policy_decision_names_complete_contract",
    "policy_decisions_pass_contract",
    "validation_matrix_hash_present_contract",
    "validation_matrix_hash_stable_contract",
    "sanitized_payload_policy_contract",
    "candidate_only_policy_contract",
    "no_real_execution_policy_contract",
    "no_adapter_invocation_policy_contract",
    "no_manifest_execution_policy_contract",
    "no_dry_run_plan_execution_policy_contract",
    "no_external_call_policy_contract",
    "no_durable_write_policy_contract",
    "no_filesystem_write_policy_contract",
    "no_database_write_policy_contract",
    "no_memory_graph_mutation_policy_contract",
    "no_operation_ledger_write_policy_contract",
    "no_autonomous_execution_policy_contract",
    "star_cosmos_candidate_only_policy_contract",
]

EXPECTED_CHECK_NAMES = [
    "manifest_validation_matrix_pass_check",
    "manifest_policy_gate_stage_check",
    "policy_gate_only_mode_check",
    "policy_decision_names_complete_check",
    "policy_decisions_pass_check",
    "policy_contracts_pass_check",
    "validation_matrix_hash_present_check",
    "validation_matrix_hash_stable_check",
    "sanitized_payload_policy_check",
    "candidate_only_policy_check",
    "no_real_execution_policy_check",
    "no_adapter_invocation_policy_check",
    "no_manifest_execution_policy_check",
    "no_dry_run_plan_execution_policy_check",
    "no_external_call_policy_check",
    "no_durable_write_policy_check",
    "no_filesystem_write_policy_check",
    "no_database_write_policy_check",
    "no_memory_graph_mutation_policy_check",
    "no_operation_ledger_write_policy_check",
    "no_autonomous_execution_policy_check",
    "star_cosmos_candidate_only_policy_check",
    "deterministic_policy_gate_hash_check",
    "policy_handoff_readiness_check",
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

FORBIDDEN_DECISION_TERMS = (
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
    "tool_" + "call",
    "adapter_" + "dispatch",
    "manifest_" + "dispatch",
    "bash -",
    "sh -",
    "python -",
    "$(",
)

FORBIDDEN_ACTIVE_SOURCE_TERMS = (
    "subprocess",
    "socket",
    "requests",
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
    return governance_execution_adapter_manifest_policy_gate_to_json(
        build_governance_execution_adapter_manifest_policy_gate()
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
    assert GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_POLICY_GATE_VERSION == "5.5.0"
    assert (
        GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_POLICY_GATE_SCHEMA_VERSION
        == "5.5.0"
    )
    assert (
        GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_POLICY_GATE_TYPE
        == "governance_execution_adapter_manifest_policy_gate"
    )
    assert (
        GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_POLICY_GATE_HASH_ALGORITHM
        == "sha256"
    )
    assert (
        EXECUTION_ADAPTER_MANIFEST_POLICY_GATE_STAGE
        == "v5.5_execution_adapter_manifest_policy_gate_candidate"
    )
    assert MANIFEST_POLICY_GATE_MODE == "policy_gate_only"
    assert STAR_COSMOS_ENTRY_STATUS == "candidate_only"


def test_manifest_policy_gate_shape_is_deterministic():
    first = _gate()
    second = _gate()

    assert first == second
    assert first["version"] == "5.5.0"
    assert first["schema_version"] == "5.5.0"
    assert (
        first["manifest_policy_gate_type"]
        == "governance_execution_adapter_manifest_policy_gate"
    )
    assert first["manifest_policy_gate_status"] == "pass"
    assert (
        first["manifest_policy_gate_stage"]
        == "v5.5_execution_adapter_manifest_policy_gate_candidate"
    )
    assert first["manifest_policy_gate_mode"] == "policy_gate_only"
    assert first["star_cosmos_entry_status"] == "candidate_only"
    for key in COMMON_FALSE_FIELDS:
        assert first[key] is False
    assert (
        first["handoff_status"]
        == "ready_for_future_manifest_approval_gate_design"
    )
    assert first["blocking_reasons"] == []
    assert first["manifest_validation_matrix_version"] == "5.5.0"
    assert first["manifest_validation_matrix_status"] == "pass"
    assert isinstance(first["manifest_validation_matrix_hash"], str)
    assert len(first["manifest_validation_matrix_hash"]) == 64
    assert len(first["deterministic_manifest_policy_gate_hash"]) == 64
    _assert_string_keys_and_finite_values(first)


def test_policy_decision_names_are_stable_and_complete():
    gate = _gate()

    assert (
        list_governance_execution_adapter_manifest_policy_decision_names()
        == EXPECTED_DECISION_NAMES
    )
    assert [
        decision["decision_name"]
        for decision in gate["manifest_policy_gate_decisions"]
    ] == EXPECTED_DECISION_NAMES


def test_policy_contract_names_are_stable_and_complete():
    gate = _gate()

    assert (
        list_governance_execution_adapter_manifest_policy_contract_names()
        == EXPECTED_CONTRACT_NAMES
    )
    assert [
        contract["contract_name"]
        for contract in gate["manifest_policy_gate_contracts"]
    ] == EXPECTED_CONTRACT_NAMES


def test_policy_check_names_are_stable_and_complete():
    gate = _gate()

    assert (
        list_governance_execution_adapter_manifest_policy_check_names()
        == EXPECTED_CHECK_NAMES
    )
    assert [
        check["check_name"] for check in gate["manifest_policy_gate_checks"]
    ] == EXPECTED_CHECK_NAMES


def test_get_decision_by_name_returns_detached_copies():
    first = get_governance_execution_adapter_manifest_policy_decision(
        "validation_matrix_pass_policy_decision"
    )
    original = deepcopy(first)
    first["observed"]["manifest_validation_matrix_status"] = "blocked"  # type: ignore[index]
    first["blocking_reasons"].append("mutated")  # type: ignore[union-attr]

    second = get_governance_execution_adapter_manifest_policy_decision(
        "validation_matrix_pass_policy_decision"
    )

    assert second == original
    assert second["observed"]["manifest_validation_matrix_status"] == "pass"  # type: ignore[index]
    assert second["blocking_reasons"] == []


def test_get_contract_by_name_returns_detached_copies():
    first = get_governance_execution_adapter_manifest_policy_contract(
        "policy_gate_only_contract"
    )
    original = deepcopy(first)
    first["observed"]["manifest_executed"] = True  # type: ignore[index]
    first["blocking_reasons"].append("mutated")  # type: ignore[union-attr]

    second = get_governance_execution_adapter_manifest_policy_contract(
        "policy_gate_only_contract"
    )

    assert second == original
    assert second["observed"]["manifest_executed"] is False  # type: ignore[index]
    assert second["blocking_reasons"] == []


def test_get_check_by_name_returns_detached_copies():
    first = get_governance_execution_adapter_manifest_policy_check(
        "policy_gate_only_mode_check"
    )
    original = deepcopy(first)
    first["observed"]["value"] = "mutated"  # type: ignore[index]
    first["blocking_reasons"].append("mutated")  # type: ignore[union-attr]

    second = get_governance_execution_adapter_manifest_policy_check(
        "policy_gate_only_mode_check"
    )

    assert second == original
    assert second["observed"]["value"] == "policy_gate_only"  # type: ignore[index]
    assert second["blocking_reasons"] == []


def test_unknown_decision_name_returns_blocked_style_result():
    result = get_governance_execution_adapter_manifest_policy_decision(
        "missing_decision"
    )
    second = get_governance_execution_adapter_manifest_policy_decision(
        "missing_decision"
    )

    assert result == second
    assert result["decision_name"] == "missing_decision"
    assert result["decision_type"] == "unknown_manifest_policy_decision"
    assert result["decision_status"] == "blocked"
    assert result["blocking_reasons"] == [
        "execution adapter manifest policy decision name is not recognized"
    ]


def test_unknown_contract_name_returns_blocked_style_result():
    result = get_governance_execution_adapter_manifest_policy_contract(
        "missing_contract"
    )
    second = get_governance_execution_adapter_manifest_policy_contract(
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
    result = get_governance_execution_adapter_manifest_policy_check(
        "missing_check"
    )
    second = get_governance_execution_adapter_manifest_policy_check(
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

    assert gate["manifest_policy_gate_status"] == "pass"
    assert gate["blocking_reasons"] == []
    for decision in gate["manifest_policy_gate_decisions"]:
        assert decision["decision_status"] == "pass"
        assert decision["blocking_reasons"] == []
    for contract in gate["manifest_policy_gate_contracts"]:
        assert contract["contract_status"] == "pass"
        assert contract["blocking_reasons"] == []
    for check in gate["manifest_policy_gate_checks"]:
        assert check["check_status"] == "pass"
        assert check["blocking_reasons"] == []


def test_all_execution_write_and_external_call_flags_remain_false():
    gate = _gate()

    for key in COMMON_FALSE_FIELDS:
        assert gate[key] is False
    _assert_safety(gate)


def test_deterministic_policy_gate_hash_is_stable_and_sensitive_to_decision_data():
    gate = _gate()
    repeated = _gate()
    mutated = deepcopy(gate)
    mutated["manifest_policy_gate_decisions"][0]["observed"][  # type: ignore[index]
        "manifest_validation_matrix_status"
    ] = "blocked"

    assert (
        gate["deterministic_manifest_policy_gate_hash"]
        == repeated["deterministic_manifest_policy_gate_hash"]
    )
    assert _execution_adapter_manifest_policy_gate_hash(gate) == gate[
        "deterministic_manifest_policy_gate_hash"
    ]
    assert _execution_adapter_manifest_policy_gate_hash(mutated) != gate[
        "deterministic_manifest_policy_gate_hash"
    ]


def test_policy_gate_hash_is_sensitive_to_contract_and_check_data():
    gate = _gate()
    contract_mutated = deepcopy(gate)
    check_mutated = deepcopy(gate)
    contract_mutated["manifest_policy_gate_contracts"][0]["observed"][  # type: ignore[index]
        "manifest_executed"
    ] = True
    check_mutated["manifest_policy_gate_checks"][0]["observed"][  # type: ignore[index]
        "manifest_validation_matrix_status"
    ] = "blocked"

    assert _execution_adapter_manifest_policy_gate_hash(
        contract_mutated
    ) != gate["deterministic_manifest_policy_gate_hash"]
    assert _execution_adapter_manifest_policy_gate_hash(check_mutated) != gate[
        "deterministic_manifest_policy_gate_hash"
    ]


def test_policy_gate_json_is_deterministic():
    gate = _gate()
    payload = governance_execution_adapter_manifest_policy_gate_to_json(gate)
    repeated_payload = governance_execution_adapter_manifest_policy_gate_to_json(
        _gate()
    )

    assert payload == repeated_payload
    assert payload.endswith("\n")
    assert json.loads(payload) == gate
    assert json.dumps(json.loads(payload), allow_nan=False)


def test_policy_gate_json_rejects_non_string_keys_and_non_finite_floats():
    with pytest.raises(ValueError, match="mapping keys must be strings"):
        governance_execution_adapter_manifest_policy_gate_to_json({1: "bad"})

    with pytest.raises(ValueError, match="floats must be finite"):
        governance_execution_adapter_manifest_policy_gate_to_json(
            {"bad": math.inf}
        )


def test_no_sensitive_keys_or_values_leak():
    gate = _gate()
    protected = {
        "decisions": gate["manifest_policy_gate_decisions"],
        "contracts": gate["manifest_policy_gate_contracts"],
        "checks": gate["manifest_policy_gate_checks"],
        "summary": gate["manifest_policy_gate_summary"],
        "hashes": {
            "policy_gate": gate["deterministic_manifest_policy_gate_hash"],
            "manifest_validation_matrix": gate["manifest_validation_matrix_hash"],
        },
        "json": governance_execution_adapter_manifest_policy_gate_to_json(gate),
    }
    serialized = json.dumps(protected, sort_keys=True)

    for blocked in SENSITIVE_BLOCKED_TERMS:
        assert blocked not in serialized


def test_policy_decisions_do_not_expose_live_or_sensitive_surfaces():
    gate = _gate()
    serialized_decisions = json.dumps(
        gate["manifest_policy_gate_decisions"],
        sort_keys=True,
    )

    for blocked in FORBIDDEN_DECISION_TERMS:
        assert blocked not in serialized_decisions


def test_all_safety_fields_remain_false():
    _assert_safety(_gate())


def test_manifest_policy_gate_module_has_no_active_surfaces():
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
