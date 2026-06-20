from __future__ import annotations

from copy import deepcopy
import json
import math
from pathlib import Path

import pytest

from hermes_memory_fabric.governance_execution_adapter_manifest_validation_matrix import (
    EXECUTION_ADAPTER_MANIFEST_VALIDATION_MATRIX_STAGE,
    GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_VALIDATION_MATRIX_HASH_ALGORITHM,
    GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_VALIDATION_MATRIX_SCHEMA_VERSION,
    GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_VALIDATION_MATRIX_TYPE,
    GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_VALIDATION_MATRIX_VERSION,
    MANIFEST_VALIDATION_MATRIX_MODE,
    SAFETY_BOUNDARIES,
    STAR_COSMOS_ENTRY_STATUS,
    _execution_adapter_manifest_validation_matrix_hash,
    build_governance_execution_adapter_manifest_validation_matrix,
    get_governance_execution_adapter_manifest_validation_check,
    get_governance_execution_adapter_manifest_validation_contract,
    get_governance_execution_adapter_manifest_validation_row,
    governance_execution_adapter_manifest_validation_matrix_to_json,
    list_governance_execution_adapter_manifest_validation_check_names,
    list_governance_execution_adapter_manifest_validation_contract_names,
    list_governance_execution_adapter_manifest_validation_row_names,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CORE_MODULE = (
    PROJECT_ROOT
    / "src"
    / "hermes_memory_fabric"
    / "governance_execution_adapter_manifest_validation_matrix.py"
)

EXPECTED_ROW_NAMES = [
    "minimal_read_only_fixture_validation_row",
    "permission_declared_fixture_validation_row",
    "external_dependency_declared_fixture_validation_row",
    "durable_write_disabled_fixture_validation_row",
    "memory_graph_mutation_disabled_fixture_validation_row",
    "operation_ledger_write_disabled_fixture_validation_row",
    "approval_required_fixture_validation_row",
    "redaction_required_fixture_validation_row",
    "star_cosmos_candidate_only_fixture_validation_row",
    "fixture_pack_integrity_validation_row",
    "fixture_contract_integrity_validation_row",
    "fixture_check_integrity_validation_row",
    "deterministic_hash_validation_row",
    "sanitized_payload_validation_row",
    "safety_boundary_validation_row",
    "candidate_only_boundary_validation_row",
]

EXPECTED_CONTRACT_NAMES = [
    "validation_matrix_only_contract",
    "manifest_fixture_pack_pass_contract",
    "validation_row_names_complete_contract",
    "validation_rows_pass_contract",
    "fixture_pack_hash_present_contract",
    "fixture_pack_hash_stable_contract",
    "fixture_payload_sanitized_contract",
    "fixture_contracts_pass_contract",
    "fixture_checks_pass_contract",
    "no_executable_command_validation_contract",
    "no_live_endpoint_validation_contract",
    "no_secret_validation_contract",
    "no_raw_log_validation_contract",
    "adapter_not_implemented_validation_contract",
    "adapter_not_invoked_validation_contract",
    "manifest_not_executed_validation_contract",
    "dry_run_plan_not_executed_validation_contract",
    "real_execution_disabled_validation_contract",
    "external_calls_disabled_validation_contract",
    "durable_writes_disabled_validation_contract",
    "filesystem_writes_disabled_validation_contract",
    "database_writes_disabled_validation_contract",
    "memory_graph_mutation_disabled_validation_contract",
    "operation_ledger_writes_disabled_validation_contract",
    "autonomous_execution_disabled_validation_contract",
    "star_cosmos_candidate_only_validation_contract",
]

EXPECTED_CHECK_NAMES = [
    "manifest_fixture_pack_pass_check",
    "manifest_validation_matrix_stage_check",
    "validation_only_mode_check",
    "validation_row_names_complete_check",
    "validation_rows_pass_check",
    "validation_contracts_pass_check",
    "fixture_pack_hash_present_check",
    "fixture_pack_hash_stable_check",
    "fixture_payloads_sanitized_check",
    "fixture_contracts_pass_check",
    "fixture_checks_pass_check",
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

FORBIDDEN_ROW_TERMS = (
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
    "governance_" + "plan_rules",
    "governance_" + "plan_schema",
    "governance_" + "plan_writer",
    "smoke_governance_" + "improvement_planner",
    "test_governance_" + "improvement_planner",
    "test_governance_" + "plan_writer",
    "uv" + ".lock",
)


def _matrix() -> dict[str, object]:
    return build_governance_execution_adapter_manifest_validation_matrix()


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
        GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_VALIDATION_MATRIX_VERSION
        == "6.0.0"
    )
    assert (
        GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_VALIDATION_MATRIX_SCHEMA_VERSION
        == "6.0.0"
    )
    assert (
        GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_VALIDATION_MATRIX_TYPE
        == "governance_execution_adapter_manifest_validation_matrix"
    )
    assert (
        GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_VALIDATION_MATRIX_HASH_ALGORITHM
        == "sha256"
    )
    assert (
        EXECUTION_ADAPTER_MANIFEST_VALIDATION_MATRIX_STAGE
        == "v5.4_execution_adapter_manifest_validation_matrix_candidate"
    )
    assert MANIFEST_VALIDATION_MATRIX_MODE == "validation_only"
    assert STAR_COSMOS_ENTRY_STATUS == "candidate_only"


def test_manifest_validation_matrix_shape_is_deterministic():
    first = _matrix()
    second = _matrix()

    assert first == second
    assert first["version"] == "6.0.0"
    assert first["schema_version"] == "6.0.0"
    assert (
        first["manifest_validation_matrix_type"]
        == "governance_execution_adapter_manifest_validation_matrix"
    )
    assert first["manifest_validation_matrix_status"] == "pass"
    assert (
        first["manifest_validation_matrix_stage"]
        == "v5.4_execution_adapter_manifest_validation_matrix_candidate"
    )
    assert first["manifest_validation_matrix_mode"] == "validation_only"
    assert first["star_cosmos_entry_status"] == "candidate_only"
    for key in COMMON_FALSE_FIELDS:
        assert first[key] is False
    assert first["handoff_status"] == "ready_for_future_manifest_policy_gate_design"
    assert first["blocking_reasons"] == []
    assert first["manifest_fixture_pack_version"] == "6.0.0"
    assert first["manifest_fixture_pack_status"] == "pass"
    assert isinstance(first["manifest_fixture_pack_hash"], str)
    assert len(first["manifest_fixture_pack_hash"]) == 64
    assert len(first["deterministic_manifest_validation_matrix_hash"]) == 64
    _assert_string_keys_and_finite_values(first)


def test_validation_row_names_are_stable_and_complete():
    matrix = _matrix()

    assert (
        list_governance_execution_adapter_manifest_validation_row_names()
        == EXPECTED_ROW_NAMES
    )
    assert [
        row["row_name"] for row in matrix["manifest_validation_rows"]
    ] == EXPECTED_ROW_NAMES


def test_validation_contract_names_are_stable_and_complete():
    matrix = _matrix()

    assert (
        list_governance_execution_adapter_manifest_validation_contract_names()
        == EXPECTED_CONTRACT_NAMES
    )
    assert [
        contract["contract_name"]
        for contract in matrix["manifest_validation_contracts"]
    ] == EXPECTED_CONTRACT_NAMES


def test_validation_check_names_are_stable_and_complete():
    matrix = _matrix()

    assert (
        list_governance_execution_adapter_manifest_validation_check_names()
        == EXPECTED_CHECK_NAMES
    )
    assert [
        check["check_name"] for check in matrix["manifest_validation_checks"]
    ] == EXPECTED_CHECK_NAMES


def test_get_row_by_name_returns_detached_copies():
    first = get_governance_execution_adapter_manifest_validation_row(
        "minimal_read_only_fixture_validation_row"
    )
    original = deepcopy(first)
    first["observed"]["fixture_statuses"][  # type: ignore[index]
        "minimal_read_only_manifest_fixture"
    ] = "blocked"
    first["blocking_reasons"].append("mutated")  # type: ignore[union-attr]

    second = get_governance_execution_adapter_manifest_validation_row(
        "minimal_read_only_fixture_validation_row"
    )

    assert second == original
    assert second["observed"]["fixture_statuses"][  # type: ignore[index]
        "minimal_read_only_manifest_fixture"
    ] == "pass"
    assert second["blocking_reasons"] == []


def test_get_contract_by_name_returns_detached_copies():
    first = get_governance_execution_adapter_manifest_validation_contract(
        "validation_matrix_only_contract"
    )
    original = deepcopy(first)
    first["observed"]["manifest_executed"] = True  # type: ignore[index]
    first["blocking_reasons"].append("mutated")  # type: ignore[union-attr]

    second = get_governance_execution_adapter_manifest_validation_contract(
        "validation_matrix_only_contract"
    )

    assert second == original
    assert second["observed"]["manifest_executed"] is False  # type: ignore[index]
    assert second["blocking_reasons"] == []


def test_get_check_by_name_returns_detached_copies():
    first = get_governance_execution_adapter_manifest_validation_check(
        "validation_only_mode_check"
    )
    original = deepcopy(first)
    first["observed"]["value"] = "mutated"  # type: ignore[index]
    first["blocking_reasons"].append("mutated")  # type: ignore[union-attr]

    second = get_governance_execution_adapter_manifest_validation_check(
        "validation_only_mode_check"
    )

    assert second == original
    assert second["observed"]["value"] == "validation_only"  # type: ignore[index]
    assert second["blocking_reasons"] == []


def test_unknown_row_name_returns_blocked_style_result():
    result = get_governance_execution_adapter_manifest_validation_row(
        "missing_row"
    )
    second = get_governance_execution_adapter_manifest_validation_row(
        "missing_row"
    )

    assert result == second
    assert result["row_name"] == "missing_row"
    assert result["row_type"] == "unknown_manifest_validation_row"
    assert result["row_status"] == "blocked"
    assert result["blocking_reasons"] == [
        "execution adapter manifest validation row name is not recognized"
    ]


def test_unknown_contract_name_returns_blocked_style_result():
    result = get_governance_execution_adapter_manifest_validation_contract(
        "missing_contract"
    )
    second = get_governance_execution_adapter_manifest_validation_contract(
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
    result = get_governance_execution_adapter_manifest_validation_check(
        "missing_check"
    )
    second = get_governance_execution_adapter_manifest_validation_check(
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


def test_all_rows_contracts_and_checks_pass_without_blocking_reasons():
    matrix = _matrix()

    assert matrix["manifest_validation_matrix_status"] == "pass"
    assert matrix["blocking_reasons"] == []
    for row in matrix["manifest_validation_rows"]:
        assert row["row_status"] == "pass"
        assert row["blocking_reasons"] == []
    for contract in matrix["manifest_validation_contracts"]:
        assert contract["contract_status"] == "pass"
        assert contract["blocking_reasons"] == []
    for check in matrix["manifest_validation_checks"]:
        assert check["check_status"] == "pass"
        assert check["blocking_reasons"] == []


def test_all_execution_write_and_external_call_flags_remain_false():
    matrix = _matrix()

    for key in COMMON_FALSE_FIELDS:
        assert matrix[key] is False
    _assert_safety(matrix)


def test_deterministic_validation_matrix_hash_is_stable_and_sensitive_to_row_data():
    matrix = _matrix()
    repeated = _matrix()
    mutated = deepcopy(matrix)
    mutated["manifest_validation_rows"][0]["observed"][  # type: ignore[index]
        "disabled_runtime_flags_false"
    ] = False

    assert (
        matrix["deterministic_manifest_validation_matrix_hash"]
        == repeated["deterministic_manifest_validation_matrix_hash"]
    )
    assert _execution_adapter_manifest_validation_matrix_hash(matrix) == matrix[
        "deterministic_manifest_validation_matrix_hash"
    ]
    assert _execution_adapter_manifest_validation_matrix_hash(mutated) != matrix[
        "deterministic_manifest_validation_matrix_hash"
    ]


def test_validation_matrix_hash_is_sensitive_to_contract_and_check_data():
    matrix = _matrix()
    contract_mutated = deepcopy(matrix)
    check_mutated = deepcopy(matrix)
    contract_mutated["manifest_validation_contracts"][0]["observed"][  # type: ignore[index]
        "manifest_executed"
    ] = True
    check_mutated["manifest_validation_checks"][0]["observed"][  # type: ignore[index]
        "manifest_fixture_pack_status"
    ] = "blocked"

    assert _execution_adapter_manifest_validation_matrix_hash(
        contract_mutated
    ) != matrix["deterministic_manifest_validation_matrix_hash"]
    assert _execution_adapter_manifest_validation_matrix_hash(
        check_mutated
    ) != matrix["deterministic_manifest_validation_matrix_hash"]


def test_validation_matrix_json_is_deterministic():
    matrix = _matrix()
    payload = governance_execution_adapter_manifest_validation_matrix_to_json(
        matrix
    )
    repeated_payload = governance_execution_adapter_manifest_validation_matrix_to_json(
        _matrix()
    )

    assert payload == repeated_payload
    assert payload.endswith("\n")
    assert json.loads(payload) == matrix
    assert json.dumps(json.loads(payload), allow_nan=False)


def test_validation_matrix_json_rejects_non_string_keys_and_non_finite_floats():
    with pytest.raises(ValueError, match="mapping keys must be strings"):
        governance_execution_adapter_manifest_validation_matrix_to_json({1: "bad"})

    with pytest.raises(ValueError, match="floats must be finite"):
        governance_execution_adapter_manifest_validation_matrix_to_json(
            {"bad": math.inf}
        )


def test_no_sensitive_keys_or_values_leak():
    matrix = _matrix()
    protected = {
        "rows": matrix["manifest_validation_rows"],
        "contracts": matrix["manifest_validation_contracts"],
        "checks": matrix["manifest_validation_checks"],
        "summary": matrix["manifest_validation_matrix_summary"],
        "hashes": {
            "validation_matrix": matrix[
                "deterministic_manifest_validation_matrix_hash"
            ],
            "manifest_fixture_pack": matrix["manifest_fixture_pack_hash"],
        },
        "json": governance_execution_adapter_manifest_validation_matrix_to_json(
            matrix
        ),
    }
    serialized = json.dumps(protected, sort_keys=True)

    for blocked in SENSITIVE_BLOCKED_TERMS:
        assert blocked not in serialized


def test_validation_rows_do_not_expose_live_or_sensitive_surfaces():
    matrix = _matrix()
    serialized_rows = json.dumps(
        matrix["manifest_validation_rows"],
        sort_keys=True,
    )

    for blocked in FORBIDDEN_ROW_TERMS:
        assert blocked not in serialized_rows


def test_all_safety_fields_remain_false():
    _assert_safety(_matrix())


def test_manifest_validation_matrix_module_has_no_active_surfaces():
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
