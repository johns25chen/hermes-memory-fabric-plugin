from __future__ import annotations

from copy import deepcopy
import json
import math
from pathlib import Path

import pytest

from hermes_memory_fabric.governance_execution_adapter_manifest_fixture_pack import (
    EXECUTION_ADAPTER_MANIFEST_FIXTURE_PACK_STAGE,
    GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_FIXTURE_PACK_HASH_ALGORITHM,
    GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_FIXTURE_PACK_SCHEMA_VERSION,
    GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_FIXTURE_PACK_TYPE,
    GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_FIXTURE_PACK_VERSION,
    MANIFEST_FIXTURE_PACK_MODE,
    SAFETY_BOUNDARIES,
    STAR_COSMOS_ENTRY_STATUS,
    _execution_adapter_manifest_fixture_pack_hash,
    build_governance_execution_adapter_manifest_fixture_pack,
    get_governance_execution_adapter_manifest_fixture,
    get_governance_execution_adapter_manifest_fixture_check,
    get_governance_execution_adapter_manifest_fixture_contract,
    governance_execution_adapter_manifest_fixture_pack_to_json,
    list_governance_execution_adapter_manifest_fixture_check_names,
    list_governance_execution_adapter_manifest_fixture_contract_names,
    list_governance_execution_adapter_manifest_fixture_names,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CORE_MODULE = (
    PROJECT_ROOT
    / "src"
    / "hermes_memory_fabric"
    / "governance_execution_adapter_manifest_fixture_pack.py"
)

EXPECTED_FIXTURE_NAMES = [
    "minimal_read_only_manifest_fixture",
    "permission_declared_manifest_fixture",
    "external_dependency_declared_manifest_fixture",
    "durable_write_declared_but_disabled_manifest_fixture",
    "memory_graph_mutation_declared_but_disabled_manifest_fixture",
    "operation_ledger_write_declared_but_disabled_manifest_fixture",
    "approval_required_manifest_fixture",
    "redaction_required_manifest_fixture",
    "star_cosmos_candidate_only_manifest_fixture",
]

EXPECTED_CONTRACT_NAMES = [
    "fixture_pack_only_contract",
    "manifest_dry_run_design_pass_contract",
    "sanitized_fixture_payload_contract",
    "fixture_names_complete_contract",
    "fixture_payload_json_contract",
    "no_executable_command_fixture_contract",
    "no_live_endpoint_fixture_contract",
    "no_secret_fixture_contract",
    "no_raw_log_fixture_contract",
    "adapter_not_implemented_fixture_contract",
    "adapter_not_invoked_fixture_contract",
    "manifest_not_executed_fixture_contract",
    "dry_run_plan_not_executed_fixture_contract",
    "external_calls_disabled_fixture_contract",
    "durable_writes_disabled_fixture_contract",
    "filesystem_writes_disabled_fixture_contract",
    "database_writes_disabled_fixture_contract",
    "memory_graph_mutation_disabled_fixture_contract",
    "operation_ledger_writes_disabled_fixture_contract",
    "autonomous_execution_disabled_fixture_contract",
    "star_cosmos_candidate_only_fixture_contract",
]

EXPECTED_CHECK_NAMES = [
    "manifest_dry_run_design_pass_check",
    "manifest_fixture_pack_stage_check",
    "fixture_only_mode_check",
    "fixture_names_complete_check",
    "fixture_payloads_sanitized_check",
    "fixture_payloads_json_compatible_check",
    "fixture_payloads_deterministic_check",
    "no_executable_command_check",
    "no_live_endpoint_check",
    "no_secret_or_token_check",
    "no_raw_log_check",
    "adapter_not_implemented_check",
    "adapter_not_invoked_check",
    "manifest_not_executed_check",
    "dry_run_plan_not_executed_check",
    "real_execution_disabled_check",
    "external_calls_disabled_check",
    "durable_writes_disabled_check",
    "filesystem_writes_disabled_check",
    "database_writes_disabled_check",
    "memory_graph_mutation_disabled_check",
    "operation_ledger_writes_disabled_check",
    "autonomous_execution_disabled_check",
    "star_cosmos_candidate_only_check",
    "deterministic_hash_check",
    "redaction_boundary_check",
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

FORBIDDEN_PAYLOAD_TERMS = (
    "http://",
    "https://",
    "ssh://",
    "git@",
    "/Users/",
    "/private/",
    "/tmp/",
    "C:\\",
    "tool_" + "call",
    "adapter_" + "dispatch",
    "manifest_" + "dispatch",
    "git " + "push",
    "g" + "h api",
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


def _pack() -> dict[str, object]:
    return build_governance_execution_adapter_manifest_fixture_pack()


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
    assert (
        GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_FIXTURE_PACK_VERSION
        == "6.7.0"
    )
    assert (
        GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_FIXTURE_PACK_SCHEMA_VERSION
        == "6.7.0"
    )
    assert (
        GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_FIXTURE_PACK_TYPE
        == "governance_execution_adapter_manifest_fixture_pack"
    )
    assert (
        GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_FIXTURE_PACK_HASH_ALGORITHM
        == "sha256"
    )
    assert (
        EXECUTION_ADAPTER_MANIFEST_FIXTURE_PACK_STAGE
        == "v5.3_execution_adapter_manifest_fixture_pack_candidate"
    )
    assert MANIFEST_FIXTURE_PACK_MODE == "fixture_only"
    assert STAR_COSMOS_ENTRY_STATUS == "candidate_only"


def test_manifest_fixture_pack_shape_is_deterministic():
    first = _pack()
    second = _pack()

    assert first == second
    assert first["version"] == "6.7.0"
    assert first["schema_version"] == "6.7.0"
    assert (
        first["manifest_fixture_pack_type"]
        == "governance_execution_adapter_manifest_fixture_pack"
    )
    assert first["manifest_fixture_pack_status"] == "pass"
    assert (
        first["manifest_fixture_pack_stage"]
        == "v5.3_execution_adapter_manifest_fixture_pack_candidate"
    )
    assert first["manifest_fixture_pack_mode"] == "fixture_only"
    assert first["star_cosmos_entry_status"] == "candidate_only"
    for key in COMMON_FALSE_FIELDS:
        assert first[key] is False
    assert (
        first["handoff_status"]
        == "ready_for_future_manifest_validation_matrix_design"
    )
    assert first["blocking_reasons"] == []
    assert first["manifest_dry_run_design_version"] == "6.7.0"
    assert first["manifest_dry_run_design_status"] == "pass"
    assert isinstance(first["manifest_dry_run_design_hash"], str)
    assert len(first["manifest_dry_run_design_hash"]) == 64
    assert len(first["deterministic_manifest_fixture_pack_hash"]) == 64
    _assert_string_keys_and_finite_values(first)


def test_fixture_names_are_stable_and_complete():
    pack = _pack()

    assert (
        list_governance_execution_adapter_manifest_fixture_names()
        == EXPECTED_FIXTURE_NAMES
    )
    assert [
        fixture["fixture_name"] for fixture in pack["manifest_fixtures"]
    ] == EXPECTED_FIXTURE_NAMES


def test_contract_names_are_stable_and_complete():
    pack = _pack()

    assert (
        list_governance_execution_adapter_manifest_fixture_contract_names()
        == EXPECTED_CONTRACT_NAMES
    )
    assert [
        contract["contract_name"]
        for contract in pack["manifest_fixture_contracts"]
    ] == EXPECTED_CONTRACT_NAMES


def test_check_names_are_stable_and_complete():
    pack = _pack()

    assert (
        list_governance_execution_adapter_manifest_fixture_check_names()
        == EXPECTED_CHECK_NAMES
    )
    assert [
        check["check_name"] for check in pack["manifest_fixture_checks"]
    ] == EXPECTED_CHECK_NAMES


def test_get_fixture_by_name_returns_detached_copies():
    first = get_governance_execution_adapter_manifest_fixture(
        "minimal_read_only_manifest_fixture"
    )
    original = deepcopy(first)
    first["fixture_payload"]["manifest_id"] = "mutated"  # type: ignore[index]
    first["blocking_reasons"].append("mutated")  # type: ignore[union-attr]

    second = get_governance_execution_adapter_manifest_fixture(
        "minimal_read_only_manifest_fixture"
    )

    assert second == original
    assert second["fixture_payload"]["manifest_id"] != "mutated"  # type: ignore[index]
    assert second["blocking_reasons"] == []


def test_get_contract_by_name_returns_detached_copies():
    first = get_governance_execution_adapter_manifest_fixture_contract(
        "fixture_pack_only_contract"
    )
    original = deepcopy(first)
    first["observed"]["manifest_executed"] = True  # type: ignore[index]
    first["blocking_reasons"].append("mutated")  # type: ignore[union-attr]

    second = get_governance_execution_adapter_manifest_fixture_contract(
        "fixture_pack_only_contract"
    )

    assert second == original
    assert second["observed"]["manifest_executed"] is False  # type: ignore[index]
    assert second["blocking_reasons"] == []


def test_get_check_by_name_returns_detached_copies():
    first = get_governance_execution_adapter_manifest_fixture_check(
        "fixture_only_mode_check"
    )
    original = deepcopy(first)
    first["observed"]["value"] = "mutated"  # type: ignore[index]
    first["blocking_reasons"].append("mutated")  # type: ignore[union-attr]

    second = get_governance_execution_adapter_manifest_fixture_check(
        "fixture_only_mode_check"
    )

    assert second == original
    assert second["observed"]["value"] == "fixture_only"  # type: ignore[index]
    assert second["blocking_reasons"] == []


def test_unknown_fixture_name_returns_blocked_style_result():
    result = get_governance_execution_adapter_manifest_fixture(
        "missing_fixture"
    )
    second = get_governance_execution_adapter_manifest_fixture(
        "missing_fixture"
    )

    assert result == second
    assert result["fixture_name"] == "missing_fixture"
    assert result["fixture_type"] == "unknown_manifest_fixture"
    assert result["fixture_status"] == "blocked"
    assert result["blocking_reasons"] == [
        "execution adapter manifest fixture name is not recognized"
    ]


def test_unknown_contract_name_returns_blocked_style_result():
    result = get_governance_execution_adapter_manifest_fixture_contract(
        "missing_contract"
    )
    second = get_governance_execution_adapter_manifest_fixture_contract(
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
    result = get_governance_execution_adapter_manifest_fixture_check(
        "missing_check"
    )
    second = get_governance_execution_adapter_manifest_fixture_check(
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


def test_all_fixtures_contracts_and_checks_pass_without_blocking_reasons():
    pack = _pack()

    assert pack["manifest_fixture_pack_status"] == "pass"
    assert pack["blocking_reasons"] == []
    for fixture in pack["manifest_fixtures"]:
        assert fixture["fixture_status"] == "pass"
        assert fixture["blocking_reasons"] == []
    for contract in pack["manifest_fixture_contracts"]:
        assert contract["contract_status"] == "pass"
        assert contract["blocking_reasons"] == []
    for check in pack["manifest_fixture_checks"]:
        assert check["check_status"] == "pass"
        assert check["blocking_reasons"] == []


def test_deterministic_fixture_pack_hash_is_stable_and_sensitive_to_fixture_data():
    pack = _pack()
    repeated = _pack()
    mutated = deepcopy(pack)
    mutated["manifest_fixtures"][0]["fixture_type"] = "mutated"  # type: ignore[index]

    assert (
        pack["deterministic_manifest_fixture_pack_hash"]
        == repeated["deterministic_manifest_fixture_pack_hash"]
    )
    assert _execution_adapter_manifest_fixture_pack_hash(pack) == pack[
        "deterministic_manifest_fixture_pack_hash"
    ]
    assert _execution_adapter_manifest_fixture_pack_hash(mutated) != pack[
        "deterministic_manifest_fixture_pack_hash"
    ]


def test_deterministic_fixture_pack_hash_is_sensitive_to_contract_and_check_data():
    pack = _pack()
    contract_mutated = deepcopy(pack)
    check_mutated = deepcopy(pack)
    contract_mutated["manifest_fixture_contracts"][0]["observed"][  # type: ignore[index]
        "manifest_executed"
    ] = True
    check_mutated["manifest_fixture_checks"][0]["observed"][  # type: ignore[index]
        "manifest_dry_run_design_status"
    ] = "blocked"

    assert _execution_adapter_manifest_fixture_pack_hash(
        contract_mutated
    ) != pack["deterministic_manifest_fixture_pack_hash"]
    assert _execution_adapter_manifest_fixture_pack_hash(check_mutated) != pack[
        "deterministic_manifest_fixture_pack_hash"
    ]


def test_fixture_pack_json_is_deterministic():
    pack = _pack()
    payload = governance_execution_adapter_manifest_fixture_pack_to_json(pack)
    repeated_payload = governance_execution_adapter_manifest_fixture_pack_to_json(
        _pack()
    )

    assert payload == repeated_payload
    assert payload.endswith("\n")
    assert json.loads(payload) == pack
    assert json.dumps(json.loads(payload), allow_nan=False)


def test_fixture_pack_json_rejects_non_string_keys_and_non_finite_floats():
    with pytest.raises(ValueError, match="mapping keys must be strings"):
        governance_execution_adapter_manifest_fixture_pack_to_json({1: "bad"})

    with pytest.raises(ValueError, match="floats must be finite"):
        governance_execution_adapter_manifest_fixture_pack_to_json(
            {"bad": math.inf}
        )


def test_no_sensitive_keys_or_values_leak():
    pack = _pack()
    protected = {
        "fixtures": pack["manifest_fixtures"],
        "contracts": pack["manifest_fixture_contracts"],
        "checks": pack["manifest_fixture_checks"],
        "summary": pack["manifest_fixture_pack_summary"],
        "hashes": {
            "fixture_pack": pack["deterministic_manifest_fixture_pack_hash"],
            "manifest_dry_run_design": pack["manifest_dry_run_design_hash"],
        },
        "json": governance_execution_adapter_manifest_fixture_pack_to_json(pack),
    }
    serialized = json.dumps(protected, sort_keys=True)

    for blocked in SENSITIVE_BLOCKED_TERMS:
        assert blocked not in serialized


def test_all_safety_fields_remain_false():
    _assert_safety(_pack())


def test_fixture_payloads_are_synthetic_sanitized_metadata_only():
    pack = _pack()
    serialized_payloads = json.dumps(
        [fixture["fixture_payload"] for fixture in pack["manifest_fixtures"]],
        sort_keys=True,
    )

    for blocked in (*SENSITIVE_BLOCKED_TERMS, *FORBIDDEN_PAYLOAD_TERMS):
        assert blocked not in serialized_payloads
    for fixture in pack["manifest_fixtures"]:
        payload = fixture["fixture_payload"]
        assert payload["manifest_id"].startswith("synthetic-manifest-")
        assert payload["adapter_reference"]["adapter_id"].startswith("synthetic.")
        for key in COMMON_FALSE_FIELDS:
            assert payload["disabled_runtime_flags"][key] is False
        assert payload["fixture_sanitization"]["metadata_only"] is True
        assert payload["fixture_sanitization"]["external_call_enabled"] is False
        assert payload["fixture_sanitization"]["durable_write_enabled"] is False


def test_manifest_fixture_pack_module_has_no_active_execution_surfaces():
    source = CORE_MODULE.read_text(encoding="utf-8")

    for forbidden in FORBIDDEN_ACTIVE_SOURCE_TERMS:
        assert forbidden not in source
