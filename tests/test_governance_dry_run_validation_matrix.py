from __future__ import annotations

import ast
from copy import deepcopy
import json
import math
from pathlib import Path

from hermes_memory_fabric.governance_dry_run_validation_matrix import (
    GOVERNANCE_DRY_RUN_VALIDATION_MATRIX_HASH_ALGORITHM,
    GOVERNANCE_DRY_RUN_VALIDATION_MATRIX_SCHEMA_VERSION,
    GOVERNANCE_DRY_RUN_VALIDATION_MATRIX_TYPE,
    GOVERNANCE_DRY_RUN_VALIDATION_MATRIX_VERSION,
    SAFETY_BOUNDARIES,
    _validation_matrix_hash,
    build_governance_dry_run_validation_matrix,
    get_governance_dry_run_validation_matrix_row,
    governance_dry_run_validation_matrix_to_json,
    list_governance_dry_run_validation_matrix_fixture_names,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CORE_MODULE = (
    PROJECT_ROOT
    / "src"
    / "hermes_memory_fabric"
    / "governance_dry_run_validation_matrix.py"
)

EXPECTED_FIXTURE_NAMES = [
    "valid_full_sequence",
    "valid_partial_sequence",
    "blocked_event_sequence",
    "duplicate_event_id_sequence",
    "invalid_previous_event_chain_sequence",
    "invalid_transition_sequence",
    "invalid_payload_schema_sequence",
    "malformed_event_sequence",
    "unknown_event_type_sequence",
    "sensitive_redaction_sequence",
]

EXPECTED_ERROR_CATEGORIES = {
    "blocked_event_sequence": ["blocked_event"],
    "duplicate_event_id_sequence": ["duplicate_event_id"],
    "invalid_previous_event_chain_sequence": [
        "invalid_previous_event_chain"
    ],
    "invalid_transition_sequence": ["invalid_state_transition"],
    "invalid_payload_schema_sequence": ["invalid_payload_schema"],
    "malformed_event_sequence": ["malformed_event"],
    "unknown_event_type_sequence": ["unknown_event_type"],
}

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
)


def _matrix() -> dict[str, object]:
    return build_governance_dry_run_validation_matrix()


def _row(name: str) -> dict[str, object]:
    rows = _matrix()["matrix_rows"]
    assert isinstance(rows, list)
    for row in rows:
        assert isinstance(row, dict)
        if row["fixture_name"] == name:
            return row
    raise AssertionError(name)


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
    assert GOVERNANCE_DRY_RUN_VALIDATION_MATRIX_VERSION == "5.8.0"
    assert GOVERNANCE_DRY_RUN_VALIDATION_MATRIX_SCHEMA_VERSION == "5.8.0"
    assert (
        GOVERNANCE_DRY_RUN_VALIDATION_MATRIX_TYPE
        == "governance_dry_run_validation_matrix"
    )
    assert GOVERNANCE_DRY_RUN_VALIDATION_MATRIX_HASH_ALGORITHM == "sha256"


def test_validation_matrix_shape_is_deterministic():
    first = _matrix()
    second = _matrix()

    assert first == second
    assert first["version"] == "5.8.0"
    assert first["schema_version"] == "5.8.0"
    assert (
        first["validation_matrix_type"]
        == "governance_dry_run_validation_matrix"
    )
    assert first["validation_matrix_status"] == "pass"
    assert first["fixture_pack_version"] == "5.8.0"
    assert first["row_count"] == len(EXPECTED_FIXTURE_NAMES)
    assert first["pass_count"] == 3
    assert first["blocked_count"] == 7
    assert first["mismatch_count"] == 0
    assert len(first["deterministic_validation_matrix_hash"]) == 64


def test_matrix_fixture_names_are_stable_and_complete():
    matrix = _matrix()

    assert (
        list_governance_dry_run_validation_matrix_fixture_names()
        == EXPECTED_FIXTURE_NAMES
    )
    assert matrix["matrix_summary"]["fixture_names"] == EXPECTED_FIXTURE_NAMES  # type: ignore[index]
    assert [row["fixture_name"] for row in matrix["matrix_rows"]] == EXPECTED_FIXTURE_NAMES  # type: ignore[index]


def test_get_matrix_row_by_name_returns_detached_copies():
    first = get_governance_dry_run_validation_matrix_row(
        "valid_full_sequence"
    )
    original = deepcopy(first)
    first["observed_final_state"] = "mutated"
    first["blocking_reasons"].append("mutated")  # type: ignore[union-attr]

    second = get_governance_dry_run_validation_matrix_row(
        "valid_full_sequence"
    )

    assert second == original
    assert second["observed_final_state"] == "finalized"
    assert second["blocking_reasons"] == []


def test_unknown_row_name_returns_blocked_style_result():
    result = get_governance_dry_run_validation_matrix_row("missing_fixture")
    second = get_governance_dry_run_validation_matrix_row("missing_fixture")

    assert result == second
    assert result["fixture_name"] == "missing_fixture"
    assert result["fixture_kind"] == "unknown_fixture"
    assert result["row_status"] == "blocked"
    assert result["expectation_match"] is False
    assert result["blocking_reasons"] == ["fixture name is not recognized"]


def test_valid_full_sequence_row_passes_and_finalized():
    row = _row("valid_full_sequence")

    assert row["row_status"] == "pass"
    assert row["expectation_match"] is True
    assert row["observed_final_state"] == "finalized"
    assert row["observed_error_categories"] == []


def test_valid_partial_sequence_row_passes_and_non_final():
    row = _row("valid_partial_sequence")

    assert row["row_status"] == "pass"
    assert row["expectation_match"] is True
    assert row["observed_final_state"] == "review_ready"
    assert row["observed_final_state"] != "finalized"


def test_blocked_scenario_rows_are_blocked_with_expected_categories():
    for name, expected_categories in EXPECTED_ERROR_CATEGORIES.items():
        row = _row(name)

        assert row["row_status"] == "blocked"
        assert row["expectation_match"] is True
        assert row["observed_fixture_status"] == "blocked"
        assert row["observed_replay_status"] == "blocked"
        assert row["observed_cli_status"] == "blocked"
        assert row["observed_envelope_status"] == "blocked"
        assert row["observed_final_state"] == "blocked"
        assert row["observed_error_categories"] == expected_categories


def test_sensitive_redaction_sequence_row_does_not_leak_sensitive_terms():
    matrix = _matrix()
    row = _row("sensitive_redaction_sequence")
    protected = {
        "row": row,
        "summary": matrix["matrix_summary"],
        "hashes": {
            "matrix": matrix["deterministic_validation_matrix_hash"],
            "fixture_pack": matrix["fixture_pack_hash"],
            "fixture": row["fixture_hash"],
            "audit": row["audit_report_hash"],
            "cli": row["cli_hash"],
            "envelope": row["envelope_hash"],
        },
        "json": governance_dry_run_validation_matrix_to_json(matrix),
    }
    serialized = json.dumps(protected, sort_keys=True)

    assert row["row_status"] == "pass"
    assert row["observed_final_state"] == "finalized"
    for blocked in SENSITIVE_BLOCKED_TERMS:
        assert blocked not in serialized


def test_all_rows_have_expectation_match_true():
    matrix = _matrix()

    assert matrix["mismatch_count"] == 0
    for row in matrix["matrix_rows"]:  # type: ignore[union-attr]
        assert row["expectation_match"] is True


def test_matrix_hash_stable_across_repeated_runs():
    first = _matrix()
    second = _matrix()

    assert (
        first["deterministic_validation_matrix_hash"]
        == second["deterministic_validation_matrix_hash"]
    )


def test_matrix_hash_changes_when_row_data_changes():
    matrix = _matrix()
    mutated = deepcopy(matrix)
    mutated["matrix_rows"][0]["observed_final_state"] = "mutated"  # type: ignore[index]

    assert (
        _validation_matrix_hash(mutated)
        != matrix["deterministic_validation_matrix_hash"]
    )


def test_matrix_json_is_deterministic():
    matrix = _matrix()
    original = deepcopy(matrix)

    first = governance_dry_run_validation_matrix_to_json(matrix)
    second = governance_dry_run_validation_matrix_to_json(matrix)

    assert first == second
    assert first.endswith("\n")
    assert json.loads(first)["validation_matrix_status"] == "pass"
    assert matrix == original


def test_all_safety_fields_remain_false():
    _assert_safety(_matrix())


def test_all_mapping_keys_are_strings_and_floats_are_finite():
    _assert_string_keys_and_finite_values(_matrix())


def test_validation_matrix_module_has_only_local_standard_library_surfaces():
    source = CORE_MODULE.read_text(encoding="utf-8")
    tree = ast.parse(source)
    imported_roots = {
        alias.name.split(".", 1)[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    imported_roots.update(
        node.module.split(".", 1)[0]
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module
    )
    called_names = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }

    assert imported_roots <= {
        "__future__",
        "collections",
        "governance_dry_run_fixture_pack",
        "governance_transition_policy_registry",
        "hashlib",
        "json",
        "math",
        "typing",
    }
    assert called_names.isdisjoint(
        {
            "open",
            "exec",
            "eval",
            "compile",
            "__import__",
        }
    )
    for forbidden in (
        "subprocess",
        "socket",
        "filesystem",
        "database",
        "network",
        "url" + "open",
        "urllib" + "." + "request",
        "requests" + ".",
        "github",
        "openclaw",
        "composio",
        "memory_graph",
        "memory graph",
        "operation_ledger",
        "write",
        "execution",
    ):
        assert forbidden not in source.casefold()
