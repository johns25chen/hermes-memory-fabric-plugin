from __future__ import annotations

import ast
from copy import deepcopy
import json
import math
from pathlib import Path

import pytest

from hermes_memory_fabric.governance_boundary_readiness_audit import (
    GOVERNANCE_BOUNDARY_READINESS_AUDIT_HASH_ALGORITHM,
    GOVERNANCE_BOUNDARY_READINESS_AUDIT_SCHEMA_VERSION,
    GOVERNANCE_BOUNDARY_READINESS_AUDIT_TYPE,
    GOVERNANCE_BOUNDARY_READINESS_AUDIT_VERSION,
    SAFETY_BOUNDARIES,
    _readiness_audit_hash,
    build_governance_boundary_readiness_audit,
    get_governance_boundary_readiness_check,
    governance_boundary_readiness_audit_to_json,
    list_governance_boundary_readiness_check_names,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CORE_MODULE = (
    PROJECT_ROOT
    / "src"
    / "hermes_memory_fabric"
    / "governance_boundary_readiness_audit.py"
)

EXPECTED_CHECK_NAMES = [
    "version_alignment_check",
    "validation_matrix_status_check",
    "fixture_pack_presence_check",
    "fixture_coverage_check",
    "expected_vs_observed_check",
    "deterministic_hash_check",
    "redaction_boundary_check",
    "local_only_boundary_check",
    "no_execution_boundary_check",
    "no_durable_write_boundary_check",
    "no_external_call_boundary_check",
    "no_star_cosmos_claim_check",
    "handoff_candidate_check",
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
)


def _audit() -> dict[str, object]:
    return build_governance_boundary_readiness_audit()


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
    assert GOVERNANCE_BOUNDARY_READINESS_AUDIT_VERSION == "6.9.0"
    assert GOVERNANCE_BOUNDARY_READINESS_AUDIT_SCHEMA_VERSION == "6.9.0"
    assert (
        GOVERNANCE_BOUNDARY_READINESS_AUDIT_TYPE
        == "governance_boundary_readiness_audit"
    )
    assert GOVERNANCE_BOUNDARY_READINESS_AUDIT_HASH_ALGORITHM == "sha256"


def test_readiness_audit_shape_is_deterministic():
    first = _audit()
    second = _audit()

    assert first == second
    assert first["version"] == "6.9.0"
    assert first["schema_version"] == "6.9.0"
    assert (
        first["readiness_audit_type"]
        == "governance_boundary_readiness_audit"
    )
    assert first["readiness_audit_status"] == "pass"
    assert first["readiness_stage"] == "13.5_boundary_closure"
    assert (
        first["next_stage_candidate"]
        == "v5.0_execution_adapter_boundary_candidate"
    )
    assert first["star_cosmos_entry_claimed"] is False
    assert first["execution_adapter_implemented"] is False
    assert first["real_execution_enabled"] is False
    assert first["validation_matrix_version"] == "6.9.0"
    assert len(first["validation_matrix_hash"]) == 64
    assert len(first["deterministic_readiness_audit_hash"]) == 64


def test_readiness_check_names_are_stable_and_complete():
    audit = _audit()

    assert list_governance_boundary_readiness_check_names() == EXPECTED_CHECK_NAMES
    assert [
        check["check_name"] for check in audit["readiness_checks"]
    ] == EXPECTED_CHECK_NAMES


def test_get_readiness_check_by_name_returns_detached_copies():
    first = get_governance_boundary_readiness_check(
        "version_alignment_check"
    )
    original = deepcopy(first)
    first["observed"]["versions"]["kernel_version"] = "mutated"  # type: ignore[index]
    first["blocking_reasons"].append("mutated")  # type: ignore[union-attr]

    second = get_governance_boundary_readiness_check(
        "version_alignment_check"
    )

    assert second == original
    assert second["observed"]["versions"]["kernel_version"] == "6.9.0"  # type: ignore[index]
    assert second["blocking_reasons"] == []


def test_unknown_readiness_check_name_returns_blocked_style_result():
    result = get_governance_boundary_readiness_check("missing_check")
    second = get_governance_boundary_readiness_check("missing_check")

    assert result == second
    assert result["check_name"] == "missing_check"
    assert result["check_status"] == "blocked"
    assert result["expected"] == {"known_check_name": True}
    assert result["observed"] == {
        "known_check_name": False,
        "requested_check_name": "missing_check",
    }
    assert result["blocking_reasons"] == [
        "readiness check name is not recognized"
    ]


def test_readiness_audit_passes_with_ready_handoff_recommendation():
    audit = _audit()

    assert audit["readiness_audit_status"] == "pass"
    assert audit["handoff_recommendation"] == "ready_for_v5_0_boundary_candidate"
    assert audit["blocking_reasons"] == []
    assert audit["readiness_summary"]["blocked_count"] == 0  # type: ignore[index]
    assert audit["readiness_summary"]["pass_count"] == len(EXPECTED_CHECK_NAMES)  # type: ignore[index]


def test_all_readiness_checks_pass_without_blocking_reasons():
    audit = _audit()

    for check in audit["readiness_checks"]:
        assert check["check_status"] == "pass"
        assert check["blocking_reasons"] == []


def test_validation_matrix_metadata_is_present():
    audit = _audit()

    assert audit["validation_matrix_version"] == "6.9.0"
    assert isinstance(audit["validation_matrix_hash"], str)
    assert len(audit["validation_matrix_hash"]) == 64


def test_deterministic_readiness_audit_hash_is_stable_and_sensitive_to_checks():
    audit = _audit()
    repeated = _audit()
    mutated = deepcopy(audit)
    mutated["readiness_checks"][0]["observed"]["versions"]["kernel_version"] = "mutated"  # type: ignore[index]

    assert (
        audit["deterministic_readiness_audit_hash"]
        == repeated["deterministic_readiness_audit_hash"]
    )
    assert _readiness_audit_hash(audit) == audit[
        "deterministic_readiness_audit_hash"
    ]
    assert _readiness_audit_hash(mutated) != audit[
        "deterministic_readiness_audit_hash"
    ]


def test_readiness_audit_json_is_deterministic():
    audit = _audit()
    payload = governance_boundary_readiness_audit_to_json(audit)
    repeated_payload = governance_boundary_readiness_audit_to_json(_audit())

    assert payload == repeated_payload
    assert payload.endswith("\n")
    assert json.loads(payload) == audit
    assert json.dumps(json.loads(payload), allow_nan=False)


def test_readiness_audit_rejects_non_string_keys_and_non_finite_floats():
    with pytest.raises(ValueError, match="mapping keys must be strings"):
        governance_boundary_readiness_audit_to_json({1: "bad"})

    with pytest.raises(ValueError, match="floats must be finite"):
        governance_boundary_readiness_audit_to_json({"bad": math.inf})


def test_no_sensitive_keys_or_values_leak():
    audit = _audit()
    protected = {
        "checks": audit["readiness_checks"],
        "summary": audit["readiness_summary"],
        "hashes": {
            "audit": audit["deterministic_readiness_audit_hash"],
            "matrix": audit["validation_matrix_hash"],
        },
        "json": governance_boundary_readiness_audit_to_json(audit),
    }
    serialized = json.dumps(protected, sort_keys=True)

    for blocked in SENSITIVE_BLOCKED_TERMS:
        assert blocked not in serialized


def test_all_safety_fields_remain_false():
    _assert_safety(_audit())


def test_outputs_are_json_compatible_with_string_keys_and_finite_values():
    _assert_string_keys_and_finite_values(_audit())


def test_local_metadata_contracts_include_required_module_smoke_and_tests():
    audit = _audit()
    contracts = audit["local_metadata_contracts"]

    assert "src/hermes_memory_fabric/governance_boundary_readiness_audit.py" in contracts["modules"]  # type: ignore[index]
    assert "scripts/smoke_governance_boundary_readiness_audit.py" in contracts["smoke_scripts"]  # type: ignore[index]
    assert "tests/test_governance_boundary_readiness_audit.py" in contracts["tests"]  # type: ignore[index]
    assert "tests/test_smoke_governance_boundary_readiness_audit.py" in contracts["tests"]  # type: ignore[index]


def test_readiness_audit_module_exposes_no_real_io_or_external_call_apis():
    source = CORE_MODULE.read_text(encoding="utf-8")
    tree = ast.parse(source)
    forbidden_import_roots = {
        "os",
        "pathlib",
        "subprocess",
        "socket",
        "sqlite3",
        "urllib",
        "http",
        "requests",
    }
    forbidden_calls = {
        "open",
        "exec",
        "eval",
        "compile",
        "__import__",
        "run",
        "Popen",
        "request",
        "url" + "open",
        "connect",
    }

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_roots = {
                alias.name.split(".", maxsplit=1)[0] for alias in node.names
            }
            assert not (imported_roots & forbidden_import_roots)
        if isinstance(node, ast.ImportFrom) and node.module is not None:
            assert node.module.split(".", maxsplit=1)[0] not in forbidden_import_roots
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Name):
                assert func.id not in forbidden_calls
            if isinstance(func, ast.Attribute):
                assert func.attr not in forbidden_calls

    blocked_source_terms = (
        "url" + "open",
        "urllib" + ".request",
        "requests.",
        "sqlite3",
        "subprocess",
        "gh" + " api",
        "git " + "push",
        "composio" + " execute",
        "create_" + "memory_write_proposal",
    )
    for term in blocked_source_terms:
        assert term not in source
