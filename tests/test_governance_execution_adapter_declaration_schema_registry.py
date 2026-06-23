from __future__ import annotations

from copy import deepcopy
import json
import math
from pathlib import Path

import pytest

from hermes_memory_fabric.governance_execution_adapter_declaration_schema_registry import (
    DECLARATION_REGISTRY_MODE,
    EXECUTION_ADAPTER_DECLARATION_SCHEMA_REGISTRY_STAGE,
    GOVERNANCE_EXECUTION_ADAPTER_DECLARATION_SCHEMA_REGISTRY_HASH_ALGORITHM,
    GOVERNANCE_EXECUTION_ADAPTER_DECLARATION_SCHEMA_REGISTRY_SCHEMA_VERSION,
    GOVERNANCE_EXECUTION_ADAPTER_DECLARATION_SCHEMA_REGISTRY_TYPE,
    GOVERNANCE_EXECUTION_ADAPTER_DECLARATION_SCHEMA_REGISTRY_VERSION,
    SAFETY_BOUNDARIES,
    STAR_COSMOS_ENTRY_STATUS,
    _execution_adapter_declaration_schema_registry_hash,
    build_governance_execution_adapter_declaration_schema_registry,
    get_governance_execution_adapter_declaration_schema_check,
    get_governance_execution_adapter_declaration_schema_contract,
    get_governance_execution_adapter_declaration_schema_field,
    governance_execution_adapter_declaration_schema_registry_to_json,
    list_governance_execution_adapter_declaration_schema_check_names,
    list_governance_execution_adapter_declaration_schema_contract_names,
    list_governance_execution_adapter_declaration_schema_field_names,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CORE_MODULE = (
    PROJECT_ROOT
    / "src"
    / "hermes_memory_fabric"
    / "governance_execution_adapter_declaration_schema_registry.py"
)

EXPECTED_FIELD_NAMES = [
    "adapter_id",
    "adapter_name",
    "adapter_kind",
    "adapter_version",
    "adapter_owner",
    "adapter_description",
    "declared_capabilities",
    "declared_inputs",
    "declared_outputs",
    "declared_permissions",
    "declared_side_effects",
    "declared_external_dependencies",
    "declared_durable_writes",
    "declared_memory_graph_mutations",
    "declared_operation_ledger_writes",
    "declared_approval_requirements",
    "declared_dry_run_inspection",
    "declared_redaction_policy",
    "declared_safety_boundaries",
    "declared_star_cosmos_entry_status",
]

EXPECTED_CONTRACT_NAMES = [
    "schema_registry_declaration_only_contract",
    "adapter_identity_schema_contract",
    "adapter_capability_schema_contract",
    "adapter_input_schema_contract",
    "adapter_output_schema_contract",
    "adapter_permission_schema_contract",
    "adapter_side_effect_schema_contract",
    "adapter_external_dependency_schema_contract",
    "adapter_durable_write_schema_contract",
    "adapter_memory_graph_mutation_schema_contract",
    "adapter_operation_ledger_write_schema_contract",
    "adapter_human_approval_schema_contract",
    "adapter_dry_run_inspection_schema_contract",
    "adapter_redaction_schema_contract",
    "star_cosmos_candidate_only_schema_contract",
]

EXPECTED_CHECK_NAMES = [
    "execution_adapter_boundary_pass_check",
    "declaration_schema_registry_stage_check",
    "schema_only_mode_check",
    "declaration_fields_complete_check",
    "declaration_contracts_complete_check",
    "adapter_not_implemented_check",
    "adapter_not_invoked_check",
    "real_execution_disabled_check",
    "external_calls_disabled_check",
    "durable_writes_disabled_check",
    "memory_graph_mutation_disabled_check",
    "operation_ledger_writes_disabled_check",
    "autonomous_execution_disabled_check",
    "star_cosmos_candidate_only_check",
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
    "fixture-approval-phrase-5-1",
    "fixture-stdout-tail-5-1",
    "fixture-stdout-5-1",
    "fixture-raw-logs-5-1",
    "fixture-token-5-1",
    "fixture-api-key-5-1",
    "fixture-secret-5-1",
    "fixture-password-5-1",
    "fixture-credential-5-1",
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


def _registry() -> dict[str, object]:
    return build_governance_execution_adapter_declaration_schema_registry()


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
    assert (
        GOVERNANCE_EXECUTION_ADAPTER_DECLARATION_SCHEMA_REGISTRY_VERSION
        == "6.8.0"
    )
    assert (
        GOVERNANCE_EXECUTION_ADAPTER_DECLARATION_SCHEMA_REGISTRY_SCHEMA_VERSION
        == "6.8.0"
    )
    assert (
        GOVERNANCE_EXECUTION_ADAPTER_DECLARATION_SCHEMA_REGISTRY_TYPE
        == "governance_execution_adapter_declaration_schema_registry"
    )
    assert (
        GOVERNANCE_EXECUTION_ADAPTER_DECLARATION_SCHEMA_REGISTRY_HASH_ALGORITHM
        == "sha256"
    )
    assert (
        EXECUTION_ADAPTER_DECLARATION_SCHEMA_REGISTRY_STAGE
        == "v5.1_execution_adapter_declaration_schema_registry_candidate"
    )
    assert DECLARATION_REGISTRY_MODE == "schema_only"
    assert STAR_COSMOS_ENTRY_STATUS == "candidate_only"


def test_declaration_schema_registry_shape_is_deterministic():
    first = _registry()
    second = _registry()

    assert first == second
    assert first["version"] == "6.8.0"
    assert first["schema_version"] == "6.8.0"
    assert (
        first["declaration_schema_registry_type"]
        == "governance_execution_adapter_declaration_schema_registry"
    )
    assert first["declaration_schema_registry_status"] == "pass"
    assert (
        first["declaration_schema_registry_stage"]
        == "v5.1_execution_adapter_declaration_schema_registry_candidate"
    )
    assert first["declaration_registry_mode"] == "schema_only"
    assert first["star_cosmos_entry_status"] == "candidate_only"
    assert first["star_cosmos_memory_active"] is False
    assert first["execution_adapter_implemented"] is False
    assert first["execution_adapter_invoked"] is False
    assert first["real_execution_enabled"] is False
    assert first["external_calls_enabled"] is False
    assert first["durable_writes_enabled"] is False
    assert first["memory_graph_mutation_enabled"] is False
    assert first["operation_ledger_writes_enabled"] is False
    assert first["autonomous_execution_enabled"] is False
    assert (
        first["handoff_status"]
        == "ready_for_future_adapter_manifest_dry_run_design"
    )
    assert first["blocking_reasons"] == []
    assert first["boundary_version"] == "6.8.0"
    assert first["boundary_status"] == "pass"
    assert isinstance(first["boundary_hash"], str)
    assert len(first["boundary_hash"]) == 64
    assert len(first["deterministic_declaration_schema_registry_hash"]) == 64
    _assert_string_keys_and_finite_values(first)


def test_field_names_are_stable_and_complete():
    registry = _registry()

    assert (
        list_governance_execution_adapter_declaration_schema_field_names()
        == EXPECTED_FIELD_NAMES
    )
    assert [
        field["field_name"] for field in registry["declaration_schema_fields"]
    ] == EXPECTED_FIELD_NAMES


def test_contract_names_are_stable_and_complete():
    registry = _registry()

    assert (
        list_governance_execution_adapter_declaration_schema_contract_names()
        == EXPECTED_CONTRACT_NAMES
    )
    assert [
        contract["contract_name"]
        for contract in registry["declaration_schema_contracts"]
    ] == EXPECTED_CONTRACT_NAMES


def test_check_names_are_stable_and_complete():
    registry = _registry()

    assert (
        list_governance_execution_adapter_declaration_schema_check_names()
        == EXPECTED_CHECK_NAMES
    )
    assert [
        check["check_name"] for check in registry["declaration_schema_checks"]
    ] == EXPECTED_CHECK_NAMES


def test_get_field_by_name_returns_detached_copies():
    first = get_governance_execution_adapter_declaration_schema_field(
        "adapter_kind"
    )
    original = deepcopy(first)
    first["allowed_values"].append("mutated")  # type: ignore[union-attr]
    first["blocking_reasons"].append("mutated")  # type: ignore[union-attr]

    second = get_governance_execution_adapter_declaration_schema_field(
        "adapter_kind"
    )

    assert second == original
    assert "mutated" not in second["allowed_values"]  # type: ignore[operator]
    assert second["blocking_reasons"] == []


def test_get_contract_by_name_returns_detached_copies():
    first = get_governance_execution_adapter_declaration_schema_contract(
        "schema_registry_declaration_only_contract"
    )
    original = deepcopy(first)
    first["observed"]["declaration_registry_mode"] = "mutated"  # type: ignore[index]
    first["blocking_reasons"].append("mutated")  # type: ignore[union-attr]

    second = get_governance_execution_adapter_declaration_schema_contract(
        "schema_registry_declaration_only_contract"
    )

    assert second == original
    assert second["observed"]["declaration_registry_mode"] == "schema_only"  # type: ignore[index]
    assert second["blocking_reasons"] == []


def test_get_check_by_name_returns_detached_copies():
    first = get_governance_execution_adapter_declaration_schema_check(
        "schema_only_mode_check"
    )
    original = deepcopy(first)
    first["observed"]["value"] = "mutated"  # type: ignore[index]
    first["blocking_reasons"].append("mutated")  # type: ignore[union-attr]

    second = get_governance_execution_adapter_declaration_schema_check(
        "schema_only_mode_check"
    )

    assert second == original
    assert second["observed"]["value"] == "schema_only"  # type: ignore[index]
    assert second["blocking_reasons"] == []


def test_unknown_field_name_returns_blocked_style_result():
    result = get_governance_execution_adapter_declaration_schema_field(
        "missing_field"
    )
    second = get_governance_execution_adapter_declaration_schema_field(
        "missing_field"
    )

    assert result == second
    assert result["field_name"] == "missing_field"
    assert result["field_type"] == "unknown_field"
    assert result["field_status"] == "blocked"
    assert result["value_constraints"] == {"known_field_name": True}
    assert result["blocking_reasons"] == [
        "execution adapter declaration schema field name is not recognized"
    ]


def test_unknown_contract_name_returns_blocked_style_result():
    result = get_governance_execution_adapter_declaration_schema_contract(
        "missing_contract"
    )
    second = get_governance_execution_adapter_declaration_schema_contract(
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
    assert result["blocking_reasons"] == [
        "execution adapter declaration schema contract name is not recognized"
    ]


def test_unknown_check_name_returns_blocked_style_result():
    result = get_governance_execution_adapter_declaration_schema_check(
        "missing_check"
    )
    second = get_governance_execution_adapter_declaration_schema_check(
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
    assert result["blocking_reasons"] == [
        "execution adapter declaration schema check name is not recognized"
    ]


def test_all_fields_contracts_and_checks_pass_without_blocking_reasons():
    registry = _registry()

    assert registry["declaration_schema_registry_status"] == "pass"
    assert registry["blocking_reasons"] == []
    for field in registry["declaration_schema_fields"]:
        assert field["field_status"] == "pass"
        assert field["blocking_reasons"] == []
    for contract in registry["declaration_schema_contracts"]:
        assert contract["contract_status"] == "pass"
        assert contract["blocking_reasons"] == []
    for check in registry["declaration_schema_checks"]:
        assert check["check_status"] == "pass"
        assert check["blocking_reasons"] == []


def test_deterministic_registry_hash_is_stable_and_sensitive_to_field_data():
    registry = _registry()
    repeated = _registry()
    mutated = deepcopy(registry)
    mutated["declaration_schema_fields"][0]["field_type"] = "mutated"  # type: ignore[index]

    assert (
        registry["deterministic_declaration_schema_registry_hash"]
        == repeated["deterministic_declaration_schema_registry_hash"]
    )
    assert _execution_adapter_declaration_schema_registry_hash(registry) == registry[
        "deterministic_declaration_schema_registry_hash"
    ]
    assert _execution_adapter_declaration_schema_registry_hash(mutated) != registry[
        "deterministic_declaration_schema_registry_hash"
    ]


def test_deterministic_registry_hash_is_sensitive_to_contract_and_check_data():
    registry = _registry()
    contract_mutated = deepcopy(registry)
    check_mutated = deepcopy(registry)
    contract_mutated["declaration_schema_contracts"][0]["observed"][  # type: ignore[index]
        "schema_metadata_only"
    ] = False
    check_mutated["declaration_schema_checks"][0]["observed"][  # type: ignore[index]
        "boundary_status"
    ] = "blocked"

    assert _execution_adapter_declaration_schema_registry_hash(
        contract_mutated
    ) != registry["deterministic_declaration_schema_registry_hash"]
    assert _execution_adapter_declaration_schema_registry_hash(
        check_mutated
    ) != registry["deterministic_declaration_schema_registry_hash"]


def test_registry_json_is_deterministic():
    registry = _registry()
    payload = governance_execution_adapter_declaration_schema_registry_to_json(
        registry
    )
    repeated_payload = governance_execution_adapter_declaration_schema_registry_to_json(
        _registry()
    )

    assert payload == repeated_payload
    assert payload.endswith("\n")
    assert json.loads(payload) == registry
    assert json.dumps(json.loads(payload), allow_nan=False)


def test_registry_json_rejects_non_string_keys_and_non_finite_floats():
    with pytest.raises(ValueError, match="mapping keys must be strings"):
        governance_execution_adapter_declaration_schema_registry_to_json({1: "bad"})

    with pytest.raises(ValueError, match="floats must be finite"):
        governance_execution_adapter_declaration_schema_registry_to_json(
            {"bad": math.inf}
        )


def test_no_sensitive_keys_or_values_leak():
    registry = _registry()
    protected = {
        "fields": registry["declaration_schema_fields"],
        "contracts": registry["declaration_schema_contracts"],
        "checks": registry["declaration_schema_checks"],
        "summary": registry["registry_summary"],
        "hashes": {
            "registry": registry["deterministic_declaration_schema_registry_hash"],
            "boundary": registry["boundary_hash"],
        },
        "json": governance_execution_adapter_declaration_schema_registry_to_json(
            registry
        ),
    }
    serialized = json.dumps(protected, sort_keys=True)

    for blocked in SENSITIVE_BLOCKED_TERMS:
        assert blocked not in serialized


def test_all_safety_fields_remain_false():
    _assert_safety(_registry())


def test_declaration_schema_registry_module_has_no_active_execution_surfaces():
    source = CORE_MODULE.read_text(encoding="utf-8")

    for forbidden in FORBIDDEN_ACTIVE_SOURCE_TERMS:
        assert forbidden not in source
