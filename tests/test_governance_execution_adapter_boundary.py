from __future__ import annotations

from copy import deepcopy
import json
import math
from pathlib import Path

import pytest

from hermes_memory_fabric.governance_execution_adapter_boundary import (
    EXECUTION_ADAPTER_BOUNDARY_STAGE,
    GOVERNANCE_EXECUTION_ADAPTER_BOUNDARY_HASH_ALGORITHM,
    GOVERNANCE_EXECUTION_ADAPTER_BOUNDARY_SCHEMA_VERSION,
    GOVERNANCE_EXECUTION_ADAPTER_BOUNDARY_TYPE,
    GOVERNANCE_EXECUTION_ADAPTER_BOUNDARY_VERSION,
    SAFETY_BOUNDARIES,
    STAR_COSMOS_ENTRY_STATUS,
    _execution_adapter_boundary_hash,
    build_governance_execution_adapter_boundary,
    get_governance_execution_adapter_boundary_check,
    get_governance_execution_adapter_boundary_contract,
    governance_execution_adapter_boundary_to_json,
    list_governance_execution_adapter_boundary_check_names,
    list_governance_execution_adapter_boundary_contract_names,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CORE_MODULE = (
    PROJECT_ROOT
    / "src"
    / "hermes_memory_fabric"
    / "governance_execution_adapter_boundary.py"
)

EXPECTED_CONTRACT_NAMES = [
    "adapter_declaration_contract",
    "adapter_identity_contract",
    "adapter_capability_contract",
    "adapter_input_contract",
    "adapter_output_contract",
    "adapter_invocation_prohibition_contract",
    "adapter_side_effect_prohibition_contract",
    "dry_run_inspection_contract",
    "external_call_prohibition_contract",
    "durable_write_prohibition_contract",
    "memory_graph_mutation_prohibition_contract",
    "operation_ledger_write_prohibition_contract",
    "human_approval_non_execution_contract",
    "star_cosmos_candidate_only_contract",
]

EXPECTED_CHECK_NAMES = [
    "readiness_audit_pass_check",
    "boundary_stage_check",
    "declaration_only_mode_check",
    "adapter_not_implemented_check",
    "adapter_not_invoked_check",
    "real_execution_disabled_check",
    "external_calls_disabled_check",
    "durable_writes_disabled_check",
    "memory_graph_mutation_disabled_check",
    "operation_ledger_writes_disabled_check",
    "autonomous_execution_disabled_check",
    "star_cosmos_candidate_only_check",
    "contract_completeness_check",
    "deterministic_hash_check",
    "redaction_boundary_check",
]

SENSITIVE_BLOCKED_TERMS = (
    '"approval_phrase"',
    '"stdout_tail"',
    '"stdout"',
    '"raw_logs"',
    '"token"',
    '"api_key"',
    '"secret"',
    '"password"',
    '"credential"',
    "fixture-approval-phrase-4-10",
    "fixture-stdout-tail-4-10",
    "fixture-stdout-4-10",
    "fixture-raw-logs-4-10",
    "fixture-token-4-10",
    "fixture-api-key-4-10",
    "fixture-secret-4-10",
    "fixture-password-4-10",
    "fixture-credential-4-10",
    "fixture-approval-phrase-5-0",
    "fixture-stdout-tail-5-0",
    "fixture-stdout-5-0",
    "fixture-raw-logs-5-0",
    "fixture-token-5-0",
    "fixture-api-key-5-0",
    "fixture-secret-5-0",
    "fixture-password-5-0",
    "fixture-credential-5-0",
)

FORBIDDEN_ACTIVE_SOURCE_TERMS = (
    "subprocess",
    "socket",
    "requests",
    "urllib",
    "open(",
    ".open(",
    "write_text",
    "git " + "push",
    "g" + "h api",
    "OpenClaw",
    "GitHub API",
    "Composio",
    "create_" + "memory_write_proposal",
    "memory_graph_write",
    "memory_graph_mutate",
)


def _boundary() -> dict[str, object]:
    return build_governance_execution_adapter_boundary()


def _assert_safety(value: object) -> None:
    if isinstance(value, dict):
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
    assert GOVERNANCE_EXECUTION_ADAPTER_BOUNDARY_VERSION == "6.2.0"
    assert GOVERNANCE_EXECUTION_ADAPTER_BOUNDARY_SCHEMA_VERSION == "6.2.0"
    assert (
        GOVERNANCE_EXECUTION_ADAPTER_BOUNDARY_TYPE
        == "governance_execution_adapter_boundary"
    )
    assert GOVERNANCE_EXECUTION_ADAPTER_BOUNDARY_HASH_ALGORITHM == "sha256"
    assert EXECUTION_ADAPTER_BOUNDARY_STAGE == "v5.0_execution_adapter_boundary_candidate"
    assert STAR_COSMOS_ENTRY_STATUS == "candidate_only"


def test_execution_adapter_boundary_shape_is_deterministic():
    first = _boundary()
    second = _boundary()

    assert first == second
    assert first["version"] == "6.2.0"
    assert first["schema_version"] == "6.2.0"
    assert (
        first["execution_adapter_boundary_type"]
        == "governance_execution_adapter_boundary"
    )
    assert first["execution_adapter_boundary_status"] == "pass"
    assert first["boundary_stage"] == "v5.0_execution_adapter_boundary_candidate"
    assert first["boundary_mode"] == "declaration_only"
    assert first["star_cosmos_entry_status"] == "candidate_only"
    assert first["handoff_status"] == "ready_for_future_adapter_contract_design"
    assert first["blocking_reasons"] == []
    assert first["readiness_audit_version"] == "6.2.0"
    assert isinstance(first["readiness_audit_hash"], str)
    assert len(first["readiness_audit_hash"]) == 64
    assert len(first["deterministic_execution_adapter_boundary_hash"]) == 64
    _assert_string_keys_and_finite_values(first)


def test_contract_names_are_stable_and_complete():
    boundary = _boundary()

    assert (
        list_governance_execution_adapter_boundary_contract_names()
        == EXPECTED_CONTRACT_NAMES
    )
    assert [
        contract["contract_name"]
        for contract in boundary["adapter_boundary_contracts"]
    ] == EXPECTED_CONTRACT_NAMES


def test_check_names_are_stable_and_complete():
    boundary = _boundary()

    assert list_governance_execution_adapter_boundary_check_names() == EXPECTED_CHECK_NAMES
    assert [
        check["check_name"] for check in boundary["boundary_checks"]
    ] == EXPECTED_CHECK_NAMES


def test_get_boundary_contract_by_name_returns_detached_copies():
    first = get_governance_execution_adapter_boundary_contract(
        "adapter_declaration_contract"
    )
    original = deepcopy(first)
    first["observed"]["boundary_mode"] = "mutated"  # type: ignore[index]
    first["blocking_reasons"].append("mutated")  # type: ignore[union-attr]

    second = get_governance_execution_adapter_boundary_contract(
        "adapter_declaration_contract"
    )

    assert second == original
    assert second["observed"]["boundary_mode"] == "declaration_only"  # type: ignore[index]
    assert second["blocking_reasons"] == []


def test_get_boundary_check_by_name_returns_detached_copies():
    first = get_governance_execution_adapter_boundary_check(
        "declaration_only_mode_check"
    )
    original = deepcopy(first)
    first["observed"]["value"] = "mutated"  # type: ignore[index]
    first["blocking_reasons"].append("mutated")  # type: ignore[union-attr]

    second = get_governance_execution_adapter_boundary_check(
        "declaration_only_mode_check"
    )

    assert second == original
    assert second["observed"]["value"] == "declaration_only"  # type: ignore[index]
    assert second["blocking_reasons"] == []


def test_unknown_contract_name_returns_blocked_style_result():
    result = get_governance_execution_adapter_boundary_contract("missing_contract")
    second = get_governance_execution_adapter_boundary_contract("missing_contract")

    assert result == second
    assert result["contract_name"] == "missing_contract"
    assert result["contract_type"] == "unknown_contract"
    assert result["contract_status"] == "blocked"
    assert result["expected"] == {"known_contract_name": True}
    assert result["observed"] == {
        "known_contract_name": False,
        "requested_contract_name": "missing_contract",
    }
    assert result["blocking_reasons"] == [
        "adapter boundary contract name is not recognized"
    ]


def test_unknown_check_name_returns_blocked_style_result():
    result = get_governance_execution_adapter_boundary_check("missing_check")
    second = get_governance_execution_adapter_boundary_check("missing_check")

    assert result == second
    assert result["check_name"] == "missing_check"
    assert result["check_status"] == "blocked"
    assert result["expected"] == {"known_check_name": True}
    assert result["observed"] == {
        "known_check_name": False,
        "requested_check_name": "missing_check",
    }
    assert result["blocking_reasons"] == [
        "execution adapter boundary check name is not recognized"
    ]


def test_all_execution_and_star_cosmos_flags_remain_disabled():
    boundary = _boundary()

    assert boundary["star_cosmos_memory_active"] is False
    assert boundary["execution_adapter_implemented"] is False
    assert boundary["execution_adapter_invoked"] is False
    assert boundary["real_execution_enabled"] is False
    assert boundary["external_calls_enabled"] is False
    assert boundary["durable_writes_enabled"] is False
    assert boundary["memory_graph_mutation_enabled"] is False
    assert boundary["operation_ledger_writes_enabled"] is False
    assert boundary["autonomous_execution_enabled"] is False


def test_all_contracts_and_checks_pass_without_blocking_reasons():
    boundary = _boundary()

    assert boundary["execution_adapter_boundary_status"] == "pass"
    assert boundary["blocking_reasons"] == []
    for contract in boundary["adapter_boundary_contracts"]:
        assert contract["contract_status"] == "pass"
        assert contract["blocking_reasons"] == []
    for check in boundary["boundary_checks"]:
        assert check["check_status"] == "pass"
        assert check["blocking_reasons"] == []


def test_deterministic_boundary_hash_is_stable_and_sensitive_to_contract_data():
    boundary = _boundary()
    repeated = _boundary()
    mutated = deepcopy(boundary)
    mutated["adapter_boundary_contracts"][0]["observed"]["boundary_mode"] = "mutated"  # type: ignore[index]

    assert (
        boundary["deterministic_execution_adapter_boundary_hash"]
        == repeated["deterministic_execution_adapter_boundary_hash"]
    )
    assert _execution_adapter_boundary_hash(boundary) == boundary[
        "deterministic_execution_adapter_boundary_hash"
    ]
    assert _execution_adapter_boundary_hash(mutated) != boundary[
        "deterministic_execution_adapter_boundary_hash"
    ]


def test_deterministic_boundary_hash_is_sensitive_to_check_data():
    boundary = _boundary()
    mutated = deepcopy(boundary)
    mutated["boundary_checks"][0]["observed"]["readiness_audit_status"] = "blocked"  # type: ignore[index]

    assert _execution_adapter_boundary_hash(mutated) != boundary[
        "deterministic_execution_adapter_boundary_hash"
    ]


def test_boundary_json_is_deterministic():
    boundary = _boundary()
    payload = governance_execution_adapter_boundary_to_json(boundary)
    repeated_payload = governance_execution_adapter_boundary_to_json(_boundary())

    assert payload == repeated_payload
    assert payload.endswith("\n")
    assert json.loads(payload) == boundary
    assert json.dumps(json.loads(payload), allow_nan=False)


def test_boundary_json_rejects_non_string_keys_and_non_finite_floats():
    with pytest.raises(ValueError, match="mapping keys must be strings"):
        governance_execution_adapter_boundary_to_json({1: "bad"})

    with pytest.raises(ValueError, match="floats must be finite"):
        governance_execution_adapter_boundary_to_json({"bad": math.inf})


def test_no_sensitive_keys_or_values_leak():
    boundary = _boundary()
    protected = {
        "contracts": boundary["adapter_boundary_contracts"],
        "checks": boundary["boundary_checks"],
        "summary": boundary["boundary_summary"],
        "hashes": {
            "boundary": boundary["deterministic_execution_adapter_boundary_hash"],
            "readiness": boundary["readiness_audit_hash"],
        },
        "json": governance_execution_adapter_boundary_to_json(boundary),
    }
    serialized = json.dumps(protected, sort_keys=True)

    for blocked in SENSITIVE_BLOCKED_TERMS:
        assert blocked not in serialized


def test_all_safety_fields_remain_false():
    _assert_safety(_boundary())


def test_execution_adapter_boundary_module_has_no_active_execution_surfaces():
    source = CORE_MODULE.read_text(encoding="utf-8")

    for forbidden in FORBIDDEN_ACTIVE_SOURCE_TERMS:
        assert forbidden not in source
