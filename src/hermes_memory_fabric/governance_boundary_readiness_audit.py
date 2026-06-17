"""Deterministic local boundary readiness audit for governance handoff."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
import hashlib
import json
import math
from typing import Any

from .event_driven_governance_kernel import KERNEL_VERSION
from .governance_cli_report_envelope import (
    GOVERNANCE_CLI_REPORT_ENVELOPE_SCHEMA_VERSION,
    GOVERNANCE_CLI_REPORT_ENVELOPE_VERSION,
)
from .governance_dry_run_fixture_pack import (
    GOVERNANCE_DRY_RUN_FIXTURE_PACK_VERSION,
    GOVERNANCE_DRY_RUN_FIXTURE_SCHEMA_VERSION,
    build_governance_dry_run_fixture_pack,
    list_governance_dry_run_fixture_names,
)
from .governance_dry_run_validation_matrix import (
    GOVERNANCE_DRY_RUN_VALIDATION_MATRIX_SCHEMA_VERSION,
    GOVERNANCE_DRY_RUN_VALIDATION_MATRIX_VERSION,
    build_governance_dry_run_validation_matrix,
)
from .governance_event_canonicalizer import (
    CANONICAL_EVENT_SCHEMA_VERSION as CANONICALIZER_EVENT_SCHEMA_VERSION,
    CANONICALIZER_VERSION,
)
from .governance_event_schema_registry import (
    CANONICAL_EVENT_SCHEMA_VERSION,
    SCHEMA_REGISTRY_VERSION,
)
from .governance_kernel_cli_dry_run import (
    GOVERNANCE_KERNEL_CLI_DRY_RUN_VERSION,
    GOVERNANCE_KERNEL_CLI_SCHEMA_VERSION,
)
from .governance_local_event_store_dry_run import (
    LOCAL_EVENT_STORE_DRY_RUN_VERSION,
    LOCAL_EVENT_STORE_SCHEMA_VERSION,
)
from .governance_replay_audit_report import (
    REPLAY_AUDIT_REPORT_VERSION,
    REPLAY_AUDIT_SCHEMA_VERSION,
)
from .governance_transition_policy_registry import (
    GOVERNANCE_STATE_MACHINE_POLICY_VERSION,
    SAFETY_BOUNDARIES,
    TRANSITION_POLICY_REGISTRY_VERSION,
    TRANSITION_POLICY_SCHEMA_VERSION,
)


GOVERNANCE_BOUNDARY_READINESS_AUDIT_VERSION = "5.5.0"
GOVERNANCE_BOUNDARY_READINESS_AUDIT_SCHEMA_VERSION = "5.5.0"
GOVERNANCE_BOUNDARY_READINESS_AUDIT_TYPE = (
    "governance_boundary_readiness_audit"
)
GOVERNANCE_BOUNDARY_READINESS_AUDIT_HASH_ALGORITHM = "sha256"

READINESS_STAGE = "13.5_boundary_closure"
NEXT_STAGE_CANDIDATE = "v5.0_execution_adapter_boundary_candidate"
READY_HANDOFF_RECOMMENDATION = "ready_for_v5_0_boundary_candidate"
NOT_READY_HANDOFF_RECOMMENDATION = "not_ready"

REQUIRED_READINESS_CHECK_NAMES = (
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
)

REQUIRED_MODULE_CONTRACTS = (
    "src/hermes_memory_fabric/event_driven_governance_kernel.py",
    "src/hermes_memory_fabric/governance_event_schema_registry.py",
    "src/hermes_memory_fabric/governance_event_canonicalizer.py",
    "src/hermes_memory_fabric/governance_replay_audit_report.py",
    "src/hermes_memory_fabric/governance_transition_policy_registry.py",
    "src/hermes_memory_fabric/governance_local_event_store_dry_run.py",
    "src/hermes_memory_fabric/governance_kernel_cli_dry_run.py",
    "src/hermes_memory_fabric/governance_cli_report_envelope.py",
    "src/hermes_memory_fabric/governance_dry_run_fixture_pack.py",
    "src/hermes_memory_fabric/governance_dry_run_validation_matrix.py",
    "src/hermes_memory_fabric/governance_boundary_readiness_audit.py",
)
REQUIRED_SMOKE_CONTRACTS = (
    "scripts/smoke_event_driven_governance_kernel.py",
    "scripts/smoke_governance_event_schema_registry.py",
    "scripts/smoke_governance_event_canonicalizer.py",
    "scripts/smoke_governance_replay_audit_report.py",
    "scripts/smoke_governance_transition_policy_registry.py",
    "scripts/smoke_governance_local_event_store_dry_run.py",
    "scripts/smoke_governance_kernel_cli_dry_run.py",
    "scripts/smoke_governance_cli_report_envelope.py",
    "scripts/smoke_governance_dry_run_fixture_pack.py",
    "scripts/smoke_governance_dry_run_validation_matrix.py",
    "scripts/smoke_governance_boundary_readiness_audit.py",
)
REQUIRED_TEST_CONTRACTS = (
    "tests/test_event_driven_governance_kernel.py",
    "tests/test_governance_event_schema_registry.py",
    "tests/test_governance_event_canonicalizer.py",
    "tests/test_governance_replay_audit_report.py",
    "tests/test_governance_transition_policy_registry.py",
    "tests/test_governance_local_event_store_dry_run.py",
    "tests/test_governance_kernel_cli_dry_run.py",
    "tests/test_governance_cli_report_envelope.py",
    "tests/test_governance_dry_run_fixture_pack.py",
    "tests/test_governance_dry_run_validation_matrix.py",
    "tests/test_governance_boundary_readiness_audit.py",
    "tests/test_smoke_governance_boundary_readiness_audit.py",
)

_AUDIT_HASH_FIELDS = (
    "version",
    "schema_version",
    "readiness_audit_type",
    "readiness_audit_status",
    "readiness_stage",
    "next_stage_candidate",
    "star_cosmos_entry_claimed",
    "execution_adapter_implemented",
    "real_execution_enabled",
    "validation_matrix_version",
    "validation_matrix_hash",
    "readiness_checks",
    "readiness_summary",
    "handoff_recommendation",
    "blocking_reasons",
    "hash_input_contract",
    "safety_boundaries",
    "local_metadata_contracts",
)

HASH_INPUT_CONTRACT = {
    "algorithm": GOVERNANCE_BOUNDARY_READINESS_AUDIT_HASH_ALGORITHM,
    "encoding": "utf-8",
    "hash_fields": list(_AUDIT_HASH_FIELDS),
    "input_shape": "sanitized boundary readiness audit projection",
    "json_allow_nan": False,
    "json_ensure_ascii": True,
    "json_separators": [",", ":"],
    "json_sort_keys": True,
    "raw_fixture_events_included": False,
    "sensitive_names_included": False,
    "sensitive_values_included": False,
}

_SENSITIVE_BLOCKED_TERMS = (
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


def build_governance_boundary_readiness_audit() -> dict[str, Any]:
    """Build deterministic local readiness metadata for governance handoff."""

    matrix = _detached_json_value(build_governance_dry_run_validation_matrix())
    matrix_repeat = _detached_json_value(
        build_governance_dry_run_validation_matrix()
    )
    fixture_pack = _detached_json_value(build_governance_dry_run_fixture_pack())
    fixture_pack_repeat = _detached_json_value(
        build_governance_dry_run_fixture_pack()
    )

    checks = _build_readiness_checks(
        matrix,
        matrix_repeat,
        fixture_pack,
        fixture_pack_repeat,
    )
    readiness_audit_status = (
        "pass"
        if all(check["check_status"] == "pass" for check in checks)
        else "blocked"
    )
    handoff_recommendation = (
        READY_HANDOFF_RECOMMENDATION
        if readiness_audit_status == "pass"
        else NOT_READY_HANDOFF_RECOMMENDATION
    )
    blocking_reasons = _deduplicate(
        reason
        for check in checks
        for reason in check["blocking_reasons"]
    )
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    audit: dict[str, Any] = {
        "version": GOVERNANCE_BOUNDARY_READINESS_AUDIT_VERSION,
        "schema_version": GOVERNANCE_BOUNDARY_READINESS_AUDIT_SCHEMA_VERSION,
        "readiness_audit_type": GOVERNANCE_BOUNDARY_READINESS_AUDIT_TYPE,
        "readiness_audit_status": readiness_audit_status,
        "readiness_stage": READINESS_STAGE,
        "next_stage_candidate": NEXT_STAGE_CANDIDATE,
        "star_cosmos_entry_claimed": False,
        "execution_adapter_implemented": False,
        "real_execution_enabled": False,
        "validation_matrix_version": _string_or_none(matrix.get("version")),
        "validation_matrix_hash": _string_or_none(
            matrix.get("deterministic_validation_matrix_hash")
        ),
        "readiness_checks": checks,
        "readiness_summary": _readiness_summary(matrix, checks),
        "handoff_recommendation": handoff_recommendation,
        "blocking_reasons": blocking_reasons,
        "hash_input_contract": _detached_json_value(HASH_INPUT_CONTRACT),
        "safety_boundaries": safety_boundaries,
        "local_metadata_contracts": _local_metadata_contracts(),
        **safety_boundaries,
    }
    audit["deterministic_readiness_audit_hash"] = _readiness_audit_hash(audit)
    return _detached_json_value(audit)


def get_governance_boundary_readiness_check(name: str) -> dict[str, Any]:
    """Return a detached readiness check by stable check name."""

    if not isinstance(name, str):
        return _unknown_check("")
    audit = build_governance_boundary_readiness_audit()
    for check in audit["readiness_checks"]:
        if check["check_name"] == name:
            return _detached_json_value(check)
    return _unknown_check(name)


def list_governance_boundary_readiness_check_names() -> list[str]:
    """Return stable readiness check names in deterministic order."""

    return list(REQUIRED_READINESS_CHECK_NAMES)


def governance_boundary_readiness_audit_to_json(
    result: Mapping[str, Any],
) -> str:
    """Serialize readiness audit data deterministically."""

    return (
        json.dumps(
            _detached_json_value(dict(result)),
            ensure_ascii=True,
            indent=2,
            allow_nan=False,
            sort_keys=True,
        )
        + "\n"
    )


def _build_readiness_checks(
    matrix: Mapping[str, Any],
    matrix_repeat: Mapping[str, Any],
    fixture_pack: Mapping[str, Any],
    fixture_pack_repeat: Mapping[str, Any],
) -> list[dict[str, Any]]:
    checks = [
        _version_alignment_check(),
        _validation_matrix_status_check(matrix),
        _fixture_pack_presence_check(matrix, fixture_pack),
        _fixture_coverage_check(matrix, fixture_pack),
        _expected_vs_observed_check(matrix),
        _deterministic_hash_check(
            matrix,
            matrix_repeat,
            fixture_pack,
            fixture_pack_repeat,
        ),
        _redaction_boundary_check(matrix),
        _local_only_boundary_check(),
        _no_execution_boundary_check(),
        _no_durable_write_boundary_check(),
        _no_external_call_boundary_check(),
        _no_star_cosmos_claim_check(),
    ]
    checks.append(_handoff_candidate_check(checks))
    return checks


def _version_alignment_check() -> dict[str, Any]:
    expected_version = GOVERNANCE_BOUNDARY_READINESS_AUDIT_VERSION
    observed = {
        "boundary_readiness_audit_version": (
            GOVERNANCE_BOUNDARY_READINESS_AUDIT_VERSION
        ),
        "boundary_readiness_audit_schema_version": (
            GOVERNANCE_BOUNDARY_READINESS_AUDIT_SCHEMA_VERSION
        ),
        "schema_registry_version": SCHEMA_REGISTRY_VERSION,
        "event_schema_version": CANONICAL_EVENT_SCHEMA_VERSION,
        "canonicalizer_version": CANONICALIZER_VERSION,
        "canonicalization_version": CANONICALIZER_VERSION,
        "canonicalizer_event_schema_version": (
            CANONICALIZER_EVENT_SCHEMA_VERSION
        ),
        "transition_policy_registry_version": (
            TRANSITION_POLICY_REGISTRY_VERSION
        ),
        "transition_policy_schema_version": TRANSITION_POLICY_SCHEMA_VERSION,
        "transition_policy_version": GOVERNANCE_STATE_MACHINE_POLICY_VERSION,
        "replay_audit_report_version": REPLAY_AUDIT_REPORT_VERSION,
        "replay_audit_schema_version": REPLAY_AUDIT_SCHEMA_VERSION,
        "local_event_store_dry_run_version": LOCAL_EVENT_STORE_DRY_RUN_VERSION,
        "local_event_store_schema_version": LOCAL_EVENT_STORE_SCHEMA_VERSION,
        "governance_kernel_cli_dry_run_version": (
            GOVERNANCE_KERNEL_CLI_DRY_RUN_VERSION
        ),
        "governance_kernel_cli_schema_version": (
            GOVERNANCE_KERNEL_CLI_SCHEMA_VERSION
        ),
        "governance_cli_report_envelope_version": (
            GOVERNANCE_CLI_REPORT_ENVELOPE_VERSION
        ),
        "governance_cli_report_envelope_schema_version": (
            GOVERNANCE_CLI_REPORT_ENVELOPE_SCHEMA_VERSION
        ),
        "governance_dry_run_fixture_pack_version": (
            GOVERNANCE_DRY_RUN_FIXTURE_PACK_VERSION
        ),
        "governance_dry_run_fixture_schema_version": (
            GOVERNANCE_DRY_RUN_FIXTURE_SCHEMA_VERSION
        ),
        "governance_dry_run_validation_matrix_version": (
            GOVERNANCE_DRY_RUN_VALIDATION_MATRIX_VERSION
        ),
        "governance_dry_run_validation_matrix_schema_version": (
            GOVERNANCE_DRY_RUN_VALIDATION_MATRIX_SCHEMA_VERSION
        ),
        "kernel_version": KERNEL_VERSION,
    }
    mismatches = [
        name
        for name, version in observed.items()
        if version != expected_version
    ]
    return _readiness_check(
        "version_alignment_check",
        expected={
            "all_versions": expected_version,
            "component_count": len(observed),
        },
        observed={
            "versions": observed,
            "mismatched_components": mismatches,
        },
        blocking_reasons=[
            "governance stack versions must align to 5.5.0"
        ]
        if mismatches
        else [],
    )


def _validation_matrix_status_check(
    matrix: Mapping[str, Any],
) -> dict[str, Any]:
    blocking_reasons = _deduplicate(
        [
            *(
                ["validation matrix version must equal 5.5.0"]
                if matrix.get("version") != GOVERNANCE_BOUNDARY_READINESS_AUDIT_VERSION
                else []
            ),
            *(
                ["validation matrix status must pass"]
                if matrix.get("validation_matrix_status") != "pass"
                else []
            ),
            *(
                ["validation matrix mismatch count must be zero"]
                if matrix.get("mismatch_count") != 0
                else []
            ),
        ]
    )
    return _readiness_check(
        "validation_matrix_status_check",
        expected={
            "validation_matrix_version": (
                GOVERNANCE_BOUNDARY_READINESS_AUDIT_VERSION
            ),
            "validation_matrix_status": "pass",
            "mismatch_count": 0,
        },
        observed={
            "validation_matrix_version": _string_or_none(
                matrix.get("version")
            ),
            "validation_matrix_status": _string_or_none(
                matrix.get("validation_matrix_status")
            ),
            "row_count": matrix.get("row_count"),
            "pass_count": matrix.get("pass_count"),
            "blocked_count": matrix.get("blocked_count"),
            "mismatch_count": matrix.get("mismatch_count"),
        },
        blocking_reasons=blocking_reasons,
    )


def _fixture_pack_presence_check(
    matrix: Mapping[str, Any],
    fixture_pack: Mapping[str, Any],
) -> dict[str, Any]:
    matrix_fixture_hash = _string_or_none(matrix.get("fixture_pack_hash"))
    fixture_pack_hash = _string_or_none(
        fixture_pack.get("deterministic_fixture_pack_hash")
    )
    blocking_reasons = _deduplicate(
        [
            *(
                ["fixture pack version must equal 5.5.0"]
                if matrix.get("fixture_pack_version")
                != GOVERNANCE_BOUNDARY_READINESS_AUDIT_VERSION
                or fixture_pack.get("version")
                != GOVERNANCE_BOUNDARY_READINESS_AUDIT_VERSION
                else []
            ),
            *(
                ["fixture pack hash must be present"]
                if not _is_sha256(matrix_fixture_hash)
                or not _is_sha256(fixture_pack_hash)
                else []
            ),
            *(
                ["validation matrix fixture hash must match fixture pack hash"]
                if matrix_fixture_hash != fixture_pack_hash
                else []
            ),
        ]
    )
    return _readiness_check(
        "fixture_pack_presence_check",
        expected={
            "fixture_pack_version": GOVERNANCE_BOUNDARY_READINESS_AUDIT_VERSION,
            "fixture_pack_hash_algorithm": (
                GOVERNANCE_BOUNDARY_READINESS_AUDIT_HASH_ALGORITHM
            ),
            "fixture_pack_status": "pass",
        },
        observed={
            "matrix_fixture_pack_version": _string_or_none(
                matrix.get("fixture_pack_version")
            ),
            "fixture_pack_version": _string_or_none(fixture_pack.get("version")),
            "fixture_pack_status": _string_or_none(
                fixture_pack.get("fixture_pack_status")
            ),
            "matrix_fixture_pack_hash_present": _is_sha256(matrix_fixture_hash),
            "fixture_pack_hash_present": _is_sha256(fixture_pack_hash),
            "hashes_match": matrix_fixture_hash == fixture_pack_hash,
        },
        blocking_reasons=blocking_reasons,
    )


def _fixture_coverage_check(
    matrix: Mapping[str, Any],
    fixture_pack: Mapping[str, Any],
) -> dict[str, Any]:
    required_fixture_names = list_governance_dry_run_fixture_names()
    matrix_fixture_names = _matrix_fixture_names(matrix)
    fixture_pack_names = _string_list(fixture_pack.get("fixture_names"))
    missing_from_matrix = [
        name for name in required_fixture_names if name not in matrix_fixture_names
    ]
    missing_from_pack = [
        name for name in required_fixture_names if name not in fixture_pack_names
    ]
    blocking_reasons = _deduplicate(
        [
            *(["required fixtures missing from validation matrix"] if missing_from_matrix else []),
            *(["required fixtures missing from fixture pack"] if missing_from_pack else []),
            *(
                ["validation matrix fixture order must match required order"]
                if matrix_fixture_names != required_fixture_names
                else []
            ),
            *(
                ["fixture pack fixture order must match required order"]
                if fixture_pack_names != required_fixture_names
                else []
            ),
        ]
    )
    return _readiness_check(
        "fixture_coverage_check",
        expected={
            "fixture_names": required_fixture_names,
            "fixture_count": len(required_fixture_names),
        },
        observed={
            "matrix_fixture_names": matrix_fixture_names,
            "fixture_pack_names": fixture_pack_names,
            "missing_from_matrix": missing_from_matrix,
            "missing_from_fixture_pack": missing_from_pack,
        },
        blocking_reasons=blocking_reasons,
    )


def _expected_vs_observed_check(matrix: Mapping[str, Any]) -> dict[str, Any]:
    rows = _matrix_rows(matrix)
    mismatches = [
        _string_or_none(row.get("fixture_name")) or ""
        for row in rows
        if row.get("expectation_match") is not True
    ]
    blocked_rows_without_expectation_match = [
        _string_or_none(row.get("fixture_name")) or ""
        for row in rows
        if row.get("row_status") == "blocked"
        and row.get("expectation_match") is not True
    ]
    summary = matrix.get("matrix_summary")
    summary_mismatches = []
    if isinstance(summary, Mapping):
        summary_mismatches = _string_list(summary.get("mismatch_fixture_names"))
    blocking_reasons = _deduplicate(
        [
            *(["matrix row expectations must all match"] if mismatches else []),
            *(
                ["matrix summary mismatch list must be empty"]
                if summary_mismatches
                else []
            ),
        ]
    )
    return _readiness_check(
        "expected_vs_observed_check",
        expected={
            "all_expectations_matched": True,
            "mismatch_fixture_names": [],
        },
        observed={
            "mismatch_fixture_names": mismatches,
            "summary_mismatch_fixture_names": summary_mismatches,
            "blocked_rows_without_expectation_match": (
                blocked_rows_without_expectation_match
            ),
        },
        blocking_reasons=blocking_reasons,
    )


def _deterministic_hash_check(
    matrix: Mapping[str, Any],
    matrix_repeat: Mapping[str, Any],
    fixture_pack: Mapping[str, Any],
    fixture_pack_repeat: Mapping[str, Any],
) -> dict[str, Any]:
    matrix_hash = _string_or_none(
        matrix.get("deterministic_validation_matrix_hash")
    )
    matrix_repeat_hash = _string_or_none(
        matrix_repeat.get("deterministic_validation_matrix_hash")
    )
    fixture_pack_hash = _string_or_none(
        fixture_pack.get("deterministic_fixture_pack_hash")
    )
    fixture_pack_repeat_hash = _string_or_none(
        fixture_pack_repeat.get("deterministic_fixture_pack_hash")
    )
    matrix_stable = matrix == matrix_repeat and matrix_hash == matrix_repeat_hash
    fixture_pack_stable = (
        fixture_pack == fixture_pack_repeat
        and fixture_pack_hash == fixture_pack_repeat_hash
    )
    blocking_reasons = _deduplicate(
        [
            *(["validation matrix hash must be stable"] if not matrix_stable else []),
            *(["fixture pack hash must be stable"] if not fixture_pack_stable else []),
            *(["validation matrix hash must be sha256"] if not _is_sha256(matrix_hash) else []),
            *(["fixture pack hash must be sha256"] if not _is_sha256(fixture_pack_hash) else []),
        ]
    )
    return _readiness_check(
        "deterministic_hash_check",
        expected={
            "validation_matrix_hash_stable": True,
            "fixture_pack_hash_stable": True,
            "hash_algorithm": GOVERNANCE_BOUNDARY_READINESS_AUDIT_HASH_ALGORITHM,
        },
        observed={
            "validation_matrix_hash_stable": matrix_stable,
            "fixture_pack_hash_stable": fixture_pack_stable,
            "validation_matrix_hash_present": _is_sha256(matrix_hash),
            "fixture_pack_hash_present": _is_sha256(fixture_pack_hash),
        },
        blocking_reasons=blocking_reasons,
    )


def _redaction_boundary_check(matrix: Mapping[str, Any]) -> dict[str, Any]:
    protected = {
        "validation_matrix_hash": _string_or_none(
            matrix.get("deterministic_validation_matrix_hash")
        ),
        "fixture_pack_hash": _string_or_none(matrix.get("fixture_pack_hash")),
        "matrix_summary": matrix.get("matrix_summary"),
        "matrix_rows": [
            {
                "fixture_name": _string_or_none(row.get("fixture_name")),
                "fixture_hash": _string_or_none(row.get("fixture_hash")),
                "audit_report_hash": _string_or_none(
                    row.get("audit_report_hash")
                ),
                "cli_hash": _string_or_none(row.get("cli_hash")),
                "envelope_hash": _string_or_none(row.get("envelope_hash")),
                "blocking_reasons": _string_list(
                    row.get("blocking_reasons")
                ),
            }
            for row in _matrix_rows(matrix)
        ],
    }
    serialized = json.dumps(
        _detached_json_value(protected),
        ensure_ascii=True,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    leaked_terms = [
        term for term in _SENSITIVE_BLOCKED_TERMS if term in serialized
    ]
    return _readiness_check(
        "redaction_boundary_check",
        expected={
            "raw_fixture_events_included": False,
            "sensitive_names_included": False,
            "sensitive_values_included": False,
        },
        observed={
            "raw_fixture_events_included": False,
            "sensitive_term_hit_count": len(leaked_terms),
            "sensitive_terms_leaked": bool(leaked_terms),
        },
        blocking_reasons=[
            "readiness metadata must not expose sensitive fixture fields or values"
        ]
        if leaked_terms
        else [],
    )


def _local_only_boundary_check() -> dict[str, Any]:
    contracts = _local_metadata_contracts()
    all_represented = all(
        contracts[key]
        for key in ("modules", "smoke_scripts", "tests")
    )
    truthy_safety_flags = _truthy_safety_values(SAFETY_BOUNDARIES)
    return _readiness_check(
        "local_only_boundary_check",
        expected={
            "local_only": True,
            "all_safety_flags": False,
            "contract_groups": ["modules", "smoke_scripts", "tests"],
        },
        observed={
            "local_only": True,
            "deterministic_metadata_only": True,
            "contract_group_counts": {
                key: len(value) for key, value in contracts.items()
            },
            "contracts_represented": all_represented,
            "truthy_safety_flags": truthy_safety_flags,
        },
        blocking_reasons=_deduplicate(
            [
                *(
                    ["required local metadata contracts must be represented"]
                    if not all_represented
                    else []
                ),
                *(
                    ["shared safety boundary flags must remain false"]
                    if truthy_safety_flags
                    else []
                ),
            ]
        ),
    )


def _no_execution_boundary_check() -> dict[str, Any]:
    safety = _safety_subset(_execution_safety_keys())
    blocked = _truthy_safety_values(safety)
    return _readiness_check(
        "no_execution_boundary_check",
        expected={
            "execution_adapter_implemented": False,
            "real_execution_enabled": False,
            "all_execution_safety_flags": False,
        },
        observed={
            "execution_adapter_implemented": False,
            "real_execution_enabled": False,
            "truthy_execution_safety_flags": blocked,
        },
        blocking_reasons=[
            "execution boundary flags must remain false"
        ]
        if blocked
        else [],
    )


def _no_durable_write_boundary_check() -> dict[str, Any]:
    safety = _safety_subset(_durable_write_safety_keys())
    blocked = _truthy_safety_values(safety)
    return _readiness_check(
        "no_durable_write_boundary_check",
        expected={
            "durable_write_surface_exposed": False,
            "all_durable_write_safety_flags": False,
        },
        observed={
            "durable_write_surface_exposed": False,
            "truthy_durable_write_safety_flags": blocked,
        },
        blocking_reasons=[
            "durable write boundary flags must remain false"
        ]
        if blocked
        else [],
    )


def _no_external_call_boundary_check() -> dict[str, Any]:
    safety = _safety_subset(_external_call_safety_keys())
    blocked = _truthy_safety_values(safety)
    return _readiness_check(
        "no_external_call_boundary_check",
        expected={
            "external_call_surface_exposed": False,
            "all_external_call_safety_flags": False,
        },
        observed={
            "external_call_surface_exposed": False,
            "truthy_external_call_safety_flags": blocked,
        },
        blocking_reasons=[
            "external call boundary flags must remain false"
        ]
        if blocked
        else [],
    )


def _no_star_cosmos_claim_check() -> dict[str, Any]:
    return _readiness_check(
        "no_star_cosmos_claim_check",
        expected={
            "star_cosmos_entry_claimed": False,
            "readiness_stage": READINESS_STAGE,
        },
        observed={
            "star_cosmos_entry_claimed": False,
            "readiness_stage": READINESS_STAGE,
            "next_stage_candidate": NEXT_STAGE_CANDIDATE,
        },
        blocking_reasons=[],
    )


def _handoff_candidate_check(
    prior_checks: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    prior_blocked = [
        _string_or_none(check.get("check_name")) or ""
        for check in prior_checks
        if check.get("check_status") != "pass"
    ]
    recommendation = (
        READY_HANDOFF_RECOMMENDATION
        if not prior_blocked
        else NOT_READY_HANDOFF_RECOMMENDATION
    )
    return _readiness_check(
        "handoff_candidate_check",
        expected={
            "handoff_recommendation": READY_HANDOFF_RECOMMENDATION,
            "all_prior_checks_pass": True,
        },
        observed={
            "handoff_recommendation": recommendation,
            "blocked_prior_checks": prior_blocked,
            "v5_entered": False,
        },
        blocking_reasons=[
            "handoff candidate requires all prior readiness checks to pass"
        ]
        if prior_blocked
        else [],
    )


def _readiness_check(
    check_name: str,
    *,
    expected: Mapping[str, Any],
    observed: Mapping[str, Any],
    blocking_reasons: Sequence[str],
) -> dict[str, Any]:
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    check: dict[str, Any] = {
        "check_name": check_name,
        "expected": _detached_json_value(expected),
        "observed": _detached_json_value(observed),
        "check_status": "pass" if not blocking_reasons else "blocked",
        "blocking_reasons": _deduplicate(blocking_reasons),
        "safety_boundaries": safety_boundaries,
        **safety_boundaries,
    }
    return _detached_json_value(check)


def _unknown_check(name: str) -> dict[str, Any]:
    return _readiness_check(
        name,
        expected={"known_check_name": True},
        observed={"known_check_name": False, "requested_check_name": name},
        blocking_reasons=["readiness check name is not recognized"],
    )


def _readiness_summary(
    matrix: Mapping[str, Any],
    checks: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    blocked_checks = [
        _string_or_none(check.get("check_name")) or ""
        for check in checks
        if check.get("check_status") != "pass"
    ]
    fixture_names = _matrix_fixture_names(matrix)
    return _detached_json_value(
        {
            "check_count": len(checks),
            "pass_count": len(checks) - len(blocked_checks),
            "blocked_count": len(blocked_checks),
            "blocked_check_names": blocked_checks,
            "validation_matrix_status": _string_or_none(
                matrix.get("validation_matrix_status")
            ),
            "validation_matrix_mismatch_count": matrix.get("mismatch_count"),
            "fixture_count": len(fixture_names),
            "fixture_names": fixture_names,
            "local_only": True,
            "deterministic": True,
            "safety_status": "safe" if not blocked_checks else "blocked",
            "raw_fixture_events_included": False,
            "star_cosmos_entry_claimed": False,
            "execution_adapter_implemented": False,
            "real_execution_enabled": False,
        }
    )


def _local_metadata_contracts() -> dict[str, list[str]]:
    return {
        "modules": list(REQUIRED_MODULE_CONTRACTS),
        "smoke_scripts": list(REQUIRED_SMOKE_CONTRACTS),
        "tests": list(REQUIRED_TEST_CONTRACTS),
    }


def _matrix_rows(matrix: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    rows = matrix.get("matrix_rows")
    if not isinstance(rows, list):
        return []
    return [row for row in rows if isinstance(row, Mapping)]


def _matrix_fixture_names(matrix: Mapping[str, Any]) -> list[str]:
    summary = matrix.get("matrix_summary")
    if isinstance(summary, Mapping):
        names = _string_list(summary.get("fixture_names"))
        if names:
            return names
    return [
        _string_or_none(row.get("fixture_name")) or ""
        for row in _matrix_rows(matrix)
    ]


def _execution_safety_keys() -> list[str]:
    return [
        key
        for key in SAFETY_BOUNDARIES
        if "execution" in key
        or "executed" in key
        or "adapter" in key
        or key in {"dry_run_executed", "dry_run_plan_executed"}
    ]


def _durable_write_safety_keys() -> list[str]:
    return [
        key
        for key in SAFETY_BOUNDARIES
        if "written" in key
        or "mutated" in key
        or "ledger_entry_created" in key
    ]


def _external_call_safety_keys() -> list[str]:
    return [
        key
        for key in SAFETY_BOUNDARIES
        if key == "external_calls_performed" or key.endswith("_called")
    ]


def _safety_subset(keys: Sequence[str]) -> dict[str, bool]:
    return {key: SAFETY_BOUNDARIES[key] for key in keys}


def _truthy_safety_values(safety: Mapping[str, bool]) -> list[str]:
    return [key for key, value in safety.items() if value is not False]


def _readiness_audit_hash(audit: Mapping[str, Any]) -> str:
    hash_input = {field: audit[field] for field in _AUDIT_HASH_FIELDS}
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


def _is_sha256(value: str | None) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(character in "0123456789abcdef" for character in value)
    )


def _string_or_none(value: Any) -> str | None:
    return value if isinstance(value, str) else None


def _string_list(value: Any) -> list[str]:
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return list(value)
    return []


def _deduplicate(values: Sequence[str] | Any) -> list[str]:
    return list(dict.fromkeys(list(values)))


__all__ = [
    "GOVERNANCE_BOUNDARY_READINESS_AUDIT_HASH_ALGORITHM",
    "GOVERNANCE_BOUNDARY_READINESS_AUDIT_SCHEMA_VERSION",
    "GOVERNANCE_BOUNDARY_READINESS_AUDIT_TYPE",
    "GOVERNANCE_BOUNDARY_READINESS_AUDIT_VERSION",
    "SAFETY_BOUNDARIES",
    "build_governance_boundary_readiness_audit",
    "get_governance_boundary_readiness_check",
    "governance_boundary_readiness_audit_to_json",
    "list_governance_boundary_readiness_check_names",
]
