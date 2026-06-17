"""Deterministic validation matrix for governance dry-run fixtures."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
import hashlib
import json
import math
from typing import Any

from .governance_dry_run_fixture_pack import (
    build_governance_dry_run_fixture_pack,
    list_governance_dry_run_fixture_names,
)
from .governance_transition_policy_registry import SAFETY_BOUNDARIES


GOVERNANCE_DRY_RUN_VALIDATION_MATRIX_VERSION = "5.3.0"
GOVERNANCE_DRY_RUN_VALIDATION_MATRIX_SCHEMA_VERSION = "5.3.0"
GOVERNANCE_DRY_RUN_VALIDATION_MATRIX_TYPE = (
    "governance_dry_run_validation_matrix"
)
GOVERNANCE_DRY_RUN_VALIDATION_MATRIX_HASH_ALGORITHM = "sha256"

_MATRIX_HASH_FIELDS = (
    "version",
    "schema_version",
    "validation_matrix_type",
    "validation_matrix_status",
    "fixture_pack_version",
    "fixture_pack_hash",
    "row_count",
    "pass_count",
    "blocked_count",
    "mismatch_count",
    "matrix_rows",
    "matrix_summary",
    "hash_input_contract",
    "safety_boundaries",
)

HASH_INPUT_CONTRACT = {
    "algorithm": GOVERNANCE_DRY_RUN_VALIDATION_MATRIX_HASH_ALGORITHM,
    "encoding": "utf-8",
    "hash_fields": list(_MATRIX_HASH_FIELDS),
    "input_shape": "sanitized validation matrix projection",
    "json_allow_nan": False,
    "json_ensure_ascii": True,
    "json_separators": [",", ":"],
    "json_sort_keys": True,
    "raw_fixture_events_included": False,
    "sensitive_names_included": False,
    "sensitive_values_included": False,
}


def build_governance_dry_run_validation_matrix() -> dict[str, Any]:
    """Build a deterministic expected-vs-observed fixture matrix."""

    fixture_pack = build_governance_dry_run_fixture_pack()
    fixture_names = _fixture_names(fixture_pack)
    fixtures = fixture_pack.get("fixtures")
    if not isinstance(fixtures, Mapping):
        fixtures = {}

    matrix_rows = [
        _build_matrix_row(fixtures.get(name), name)
        for name in fixture_names
    ]
    pass_count = sum(1 for row in matrix_rows if row["row_status"] == "pass")
    blocked_count = sum(
        1 for row in matrix_rows if row["row_status"] == "blocked"
    )
    mismatch_count = sum(
        1 for row in matrix_rows if row["expectation_match"] is not True
    )
    matrix_summary = _matrix_summary(matrix_rows)
    validation_matrix_status = "pass" if mismatch_count == 0 else "blocked"
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    matrix: dict[str, Any] = {
        "version": GOVERNANCE_DRY_RUN_VALIDATION_MATRIX_VERSION,
        "schema_version": GOVERNANCE_DRY_RUN_VALIDATION_MATRIX_SCHEMA_VERSION,
        "validation_matrix_type": GOVERNANCE_DRY_RUN_VALIDATION_MATRIX_TYPE,
        "validation_matrix_status": validation_matrix_status,
        "fixture_pack_version": _string_or_none(fixture_pack.get("version")),
        "fixture_pack_hash": _string_or_none(
            fixture_pack.get("deterministic_fixture_pack_hash")
        ),
        "row_count": len(matrix_rows),
        "pass_count": pass_count,
        "blocked_count": blocked_count,
        "mismatch_count": mismatch_count,
        "matrix_rows": matrix_rows,
        "matrix_summary": matrix_summary,
        "hash_input_contract": _detached_json_value(HASH_INPUT_CONTRACT),
        "safety_boundaries": safety_boundaries,
        **safety_boundaries,
    }
    matrix["deterministic_validation_matrix_hash"] = (
        _validation_matrix_hash(matrix)
    )
    return _detached_json_value(matrix)


def get_governance_dry_run_validation_matrix_row(
    name: str,
) -> dict[str, Any]:
    """Return a detached matrix row by stable fixture name."""

    if not isinstance(name, str):
        return _unknown_row("")
    matrix = build_governance_dry_run_validation_matrix()
    for row in matrix["matrix_rows"]:
        if row["fixture_name"] == name:
            return _detached_json_value(row)
    return _unknown_row(name)


def list_governance_dry_run_validation_matrix_fixture_names() -> list[str]:
    """Return fixture names in matrix order."""

    return list_governance_dry_run_fixture_names()


def governance_dry_run_validation_matrix_to_json(
    result: Mapping[str, Any],
) -> str:
    """Serialize validation matrix data deterministically."""

    return (
        json.dumps(
            dict(result),
            ensure_ascii=True,
            indent=2,
            allow_nan=False,
            sort_keys=True,
        )
        + "\n"
    )


def _fixture_names(fixture_pack: Mapping[str, Any]) -> list[str]:
    names = fixture_pack.get("fixture_names")
    if isinstance(names, list) and all(isinstance(name, str) for name in names):
        return list(names)
    return list_governance_dry_run_fixture_names()


def _build_matrix_row(value: Any, fixture_name: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        return _malformed_row(fixture_name, ["fixture is missing"])

    validation_summary = value.get("validation_summary")
    replay_audit_report = value.get("replay_audit_report")
    cli_dry_run_result = value.get("cli_dry_run_result")
    cli_report_envelope = value.get("cli_report_envelope")
    if not all(
        isinstance(candidate, Mapping)
        for candidate in (
            validation_summary,
            replay_audit_report,
            cli_dry_run_result,
            cli_report_envelope,
        )
    ):
        return _malformed_row(fixture_name, ["fixture layers are incomplete"])

    expected_status = _status_value(value.get("expected_status"))
    expected_final_state = _string_or_none(value.get("expected_final_state"))
    expected_error_categories = _string_list(
        value.get("expected_error_categories")
    )

    observed_fixture_status = _status_value(
        validation_summary.get("observed_status")
    )
    observed_replay_status = _status_value(
        replay_audit_report.get("audit_report_status")
    )
    observed_cli_status = _status_value(
        cli_dry_run_result.get("dry_run_status")
    )
    observed_envelope_status = _status_value(
        cli_report_envelope.get("envelope_status")
    )
    observed_final_state = _string_or_none(
        replay_audit_report.get("final_state")
    )
    observed_error_categories = _string_list(
        replay_audit_report.get("error_categories")
    )

    status_match = _all_equal(
        expected_status,
        (
            observed_fixture_status,
            observed_replay_status,
            observed_cli_status,
            observed_envelope_status,
        ),
    )
    final_state_match = _all_equal(
        expected_final_state,
        _final_state_observations(
            validation_summary,
            replay_audit_report,
            cli_dry_run_result,
            cli_report_envelope,
        ),
    )
    error_categories_match = _all_lists_equal(
        expected_error_categories,
        _error_category_observations(
            validation_summary,
            replay_audit_report,
            cli_dry_run_result,
            cli_report_envelope,
        ),
    )
    hash_reasons = _hash_reasons(
        value,
        replay_audit_report,
        cli_dry_run_result,
        cli_report_envelope,
    )
    blocking_reasons = _deduplicate(
        [
            *(["status mismatch"] if not status_match else []),
            *(["final state mismatch"] if not final_state_match else []),
            *(
                ["error category mismatch"]
                if not error_categories_match
                else []
            ),
            *hash_reasons,
            *_safety_reasons(value),
            *_safety_reasons(replay_audit_report),
            *_safety_reasons(cli_dry_run_result),
            *_safety_reasons(cli_report_envelope),
        ]
    )
    expectation_match = (
        status_match
        and final_state_match
        and error_categories_match
        and not blocking_reasons
    )
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    row: dict[str, Any] = {
        "fixture_name": _string_or_none(value.get("fixture_name")) or fixture_name,
        "fixture_kind": _string_or_none(value.get("fixture_kind")),
        "expected_status": expected_status,
        "expected_final_state": expected_final_state,
        "expected_error_categories": expected_error_categories,
        "observed_fixture_status": observed_fixture_status,
        "observed_replay_status": observed_replay_status,
        "observed_cli_status": observed_cli_status,
        "observed_envelope_status": observed_envelope_status,
        "observed_final_state": observed_final_state,
        "observed_error_categories": observed_error_categories,
        "fixture_hash": _string_or_none(
            value.get("deterministic_fixture_hash")
        ),
        "audit_report_hash": _string_or_none(
            replay_audit_report.get("audit_report_hash")
        ),
        "cli_hash": _string_or_none(
            cli_dry_run_result.get("deterministic_cli_hash")
        ),
        "envelope_hash": _string_or_none(
            cli_report_envelope.get("deterministic_envelope_hash")
        ),
        "expectation_match": expectation_match,
        "status_match": status_match,
        "final_state_match": final_state_match,
        "error_categories_match": error_categories_match,
        "row_status": expected_status if expectation_match else "blocked",
        "blocking_reasons": blocking_reasons,
        "safety_boundaries": safety_boundaries,
        **safety_boundaries,
    }
    return _detached_json_value(row)


def _matrix_summary(rows: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    mismatch_fixture_names = [
        str(row["fixture_name"])
        for row in rows
        if row["expectation_match"] is not True
    ]
    expected_status_counts = {
        "pass": sum(1 for row in rows if row["expected_status"] == "pass"),
        "blocked": sum(
            1 for row in rows if row["expected_status"] == "blocked"
        ),
    }
    observed_status_counts = {
        "pass": sum(
            1 for row in rows if row["observed_fixture_status"] == "pass"
        ),
        "blocked": sum(
            1 for row in rows if row["observed_fixture_status"] == "blocked"
        ),
    }
    row_status_counts = {
        "pass": sum(1 for row in rows if row["row_status"] == "pass"),
        "blocked": sum(1 for row in rows if row["row_status"] == "blocked"),
    }
    return {
        "fixture_names": [str(row["fixture_name"]) for row in rows],
        "all_expectations_matched": not mismatch_fixture_names,
        "mismatch_fixture_names": mismatch_fixture_names,
        "expected_status_counts": expected_status_counts,
        "observed_fixture_status_counts": observed_status_counts,
        "row_status_counts": row_status_counts,
        "safety_status": "safe",
    }


def _final_state_observations(
    validation_summary: Mapping[str, Any],
    replay_audit_report: Mapping[str, Any],
    cli_dry_run_result: Mapping[str, Any],
    cli_report_envelope: Mapping[str, Any],
) -> list[str | None]:
    observations = [
        _string_or_none(validation_summary.get("observed_final_state")),
        _string_or_none(replay_audit_report.get("final_state")),
        _string_or_none(
            _nested_value(cli_dry_run_result, ("result", "final_state"))
        ),
        _string_or_none(
            _nested_value(
                cli_report_envelope,
                ("report", "result", "final_state"),
            )
        ),
    ]
    return [value for value in observations if value is not None]


def _error_category_observations(
    validation_summary: Mapping[str, Any],
    replay_audit_report: Mapping[str, Any],
    cli_dry_run_result: Mapping[str, Any],
    cli_report_envelope: Mapping[str, Any],
) -> list[list[str]]:
    return [
        _string_list(validation_summary.get("observed_error_categories")),
        _string_list(replay_audit_report.get("error_categories")),
        _string_list(_nested_value(cli_dry_run_result, ("result", "error_categories"))),
        _string_list(
            _nested_value(
                cli_report_envelope,
                ("report", "result", "error_categories"),
            )
        ),
    ]


def _hash_reasons(
    fixture: Mapping[str, Any],
    replay_audit_report: Mapping[str, Any],
    cli_dry_run_result: Mapping[str, Any],
    cli_report_envelope: Mapping[str, Any],
) -> list[str]:
    required_hashes = (
        (fixture, "deterministic_fixture_hash", "fixture hash is missing"),
        (replay_audit_report, "audit_report_hash", "audit report hash is missing"),
        (cli_dry_run_result, "deterministic_cli_hash", "CLI hash is missing"),
        (
            cli_report_envelope,
            "deterministic_envelope_hash",
            "envelope hash is missing",
        ),
    )
    reasons: list[str] = []
    for mapping, key, reason in required_hashes:
        value = mapping.get(key)
        if not isinstance(value, str) or len(value) != 64:
            reasons.append(reason)
    return reasons


def _safety_reasons(value: Mapping[str, Any]) -> list[str]:
    boundaries = value.get("safety_boundaries")
    if not isinstance(boundaries, Mapping):
        return ["safety boundaries are missing"]
    for key in SAFETY_BOUNDARIES:
        if value.get(key) is not False or boundaries.get(key) is not False:
            return ["safety boundaries must remain false"]
    return []


def _malformed_row(
    fixture_name: str,
    reasons: Sequence[str],
) -> dict[str, Any]:
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    row: dict[str, Any] = {
        "fixture_name": fixture_name,
        "fixture_kind": "malformed_fixture",
        "expected_status": "blocked",
        "expected_final_state": "blocked",
        "expected_error_categories": ["malformed_fixture"],
        "observed_fixture_status": "blocked",
        "observed_replay_status": "blocked",
        "observed_cli_status": "blocked",
        "observed_envelope_status": "blocked",
        "observed_final_state": "blocked",
        "observed_error_categories": ["malformed_fixture"],
        "fixture_hash": None,
        "audit_report_hash": None,
        "cli_hash": None,
        "envelope_hash": None,
        "expectation_match": False,
        "status_match": False,
        "final_state_match": False,
        "error_categories_match": False,
        "row_status": "blocked",
        "blocking_reasons": list(reasons),
        "safety_boundaries": safety_boundaries,
        **safety_boundaries,
    }
    return _detached_json_value(row)


def _unknown_row(name: str) -> dict[str, Any]:
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    row: dict[str, Any] = {
        "fixture_name": name,
        "fixture_kind": "unknown_fixture",
        "expected_status": "blocked",
        "expected_final_state": "blocked",
        "expected_error_categories": ["unknown_fixture_name"],
        "observed_fixture_status": "blocked",
        "observed_replay_status": "blocked",
        "observed_cli_status": "blocked",
        "observed_envelope_status": "blocked",
        "observed_final_state": "blocked",
        "observed_error_categories": ["unknown_fixture_name"],
        "fixture_hash": None,
        "audit_report_hash": None,
        "cli_hash": None,
        "envelope_hash": None,
        "expectation_match": False,
        "status_match": False,
        "final_state_match": False,
        "error_categories_match": False,
        "row_status": "blocked",
        "blocking_reasons": ["fixture name is not recognized"],
        "safety_boundaries": safety_boundaries,
        **safety_boundaries,
    }
    return _detached_json_value(row)


def _status_value(value: Any) -> str | None:
    return value if value in {"pass", "blocked"} else None


def _string_or_none(value: Any) -> str | None:
    return value if isinstance(value, str) else None


def _string_list(value: Any) -> list[str]:
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return list(value)
    return []


def _nested_value(value: Mapping[str, Any], path: Sequence[str]) -> Any:
    current: Any = value
    for key in path:
        if not isinstance(current, Mapping):
            return None
        current = current.get(key)
    return current


def _all_equal(expected: Any, observed: Sequence[Any]) -> bool:
    return expected is not None and all(value == expected for value in observed)


def _all_lists_equal(expected: list[str], observed: Sequence[list[str]]) -> bool:
    return all(value == expected for value in observed)


def _validation_matrix_hash(matrix: Mapping[str, Any]) -> str:
    hash_input = {field: matrix[field] for field in _MATRIX_HASH_FIELDS}
    return _hash_json_value(hash_input)


def _hash_json_value(value: Any) -> str:
    serialized = json.dumps(
        _detached_json_value(value),
        ensure_ascii=True,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def _detached_json_value(value: Any) -> Any:
    return json.loads(
        json.dumps(
            _reject_non_finite(value),
            ensure_ascii=True,
            allow_nan=False,
            separators=(",", ":"),
            sort_keys=True,
        )
    )


def _reject_non_finite(value: Any) -> Any:
    if isinstance(value, Mapping):
        if any(not isinstance(key, str) for key in value):
            raise ValueError("mapping keys must be strings")
        return {key: _reject_non_finite(value[key]) for key in value}
    if isinstance(value, list):
        return [_reject_non_finite(item) for item in value]
    if value is None or isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("floats must be finite")
        return value
    raise ValueError("value must be deterministic JSON-compatible")


def _deduplicate(values: Sequence[str]) -> list[str]:
    return list(dict.fromkeys(values))


__all__ = [
    "GOVERNANCE_DRY_RUN_VALIDATION_MATRIX_HASH_ALGORITHM",
    "GOVERNANCE_DRY_RUN_VALIDATION_MATRIX_SCHEMA_VERSION",
    "GOVERNANCE_DRY_RUN_VALIDATION_MATRIX_TYPE",
    "GOVERNANCE_DRY_RUN_VALIDATION_MATRIX_VERSION",
    "SAFETY_BOUNDARIES",
    "build_governance_dry_run_validation_matrix",
    "get_governance_dry_run_validation_matrix_row",
    "governance_dry_run_validation_matrix_to_json",
    "list_governance_dry_run_validation_matrix_fixture_names",
]
