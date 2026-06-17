"""Deterministic manifest validation-matrix metadata for future adapters."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
import hashlib
import json
import math
from typing import Any

from .governance_execution_adapter_manifest_fixture_pack import (
    build_governance_execution_adapter_manifest_fixture_pack,
)
from .governance_transition_policy_registry import SAFETY_BOUNDARIES


GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_VALIDATION_MATRIX_VERSION = "5.5.0"
GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_VALIDATION_MATRIX_SCHEMA_VERSION = "5.5.0"
GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_VALIDATION_MATRIX_TYPE = (
    "governance_execution_adapter_manifest_validation_matrix"
)
GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_VALIDATION_MATRIX_HASH_ALGORITHM = "sha256"
EXECUTION_ADAPTER_MANIFEST_VALIDATION_MATRIX_STAGE = (
    "v5.4_execution_adapter_manifest_validation_matrix_candidate"
)
STAR_COSMOS_ENTRY_STATUS = "candidate_only"
MANIFEST_VALIDATION_MATRIX_MODE = "validation_only"

READY_HANDOFF_STATUS = "ready_for_future_manifest_policy_gate_design"
BLOCKED_HANDOFF_STATUS = "blocked"

REQUIRED_MANIFEST_VALIDATION_ROW_NAMES = (
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
)

REQUIRED_MANIFEST_VALIDATION_CONTRACT_NAMES = (
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
)

REQUIRED_MANIFEST_VALIDATION_CHECK_NAMES = (
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
)

COMMON_DISABLED_FLAGS = {
    "star_cosmos_memory_active": False,
    "execution_adapter_implemented": False,
    "execution_adapter_invoked": False,
    "manifest_executed": False,
    "dry_run_plan_executed": False,
    "real_execution_enabled": False,
    "external_calls_enabled": False,
    "durable_writes_enabled": False,
    "filesystem_writes_enabled": False,
    "database_writes_enabled": False,
    "memory_graph_mutation_enabled": False,
    "operation_ledger_writes_enabled": False,
    "autonomous_execution_enabled": False,
}

_MANIFEST_VALIDATION_MATRIX_HASH_FIELDS = (
    "version",
    "schema_version",
    "manifest_validation_matrix_type",
    "manifest_validation_matrix_status",
    "manifest_validation_matrix_stage",
    "manifest_validation_matrix_mode",
    "star_cosmos_entry_status",
    *COMMON_DISABLED_FLAGS,
    "manifest_fixture_pack_version",
    "manifest_fixture_pack_status",
    "manifest_fixture_pack_hash",
    "manifest_validation_rows",
    "manifest_validation_contracts",
    "manifest_validation_checks",
    "manifest_validation_matrix_summary",
    "handoff_status",
    "blocking_reasons",
    "hash_input_contract",
    "safety_boundaries",
)

HASH_INPUT_CONTRACT = {
    "algorithm": GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_VALIDATION_MATRIX_HASH_ALGORITHM,
    "encoding": "utf-8",
    "hash_fields": list(_MANIFEST_VALIDATION_MATRIX_HASH_FIELDS),
    "input_shape": "sanitized future execution adapter manifest validation matrix projection",
    "json_allow_nan": False,
    "json_ensure_ascii": True,
    "json_separators": [",", ":"],
    "json_sort_keys": True,
    "raw_fixture_events_included": False,
    "sensitive_names_included": False,
    "sensitive_values_included": False,
}

_PAYLOAD_BLOCKED_FRAGMENTS = (
    '"approval_' + 'phrase"',
    '"std' + 'out_tail"',
    '"std' + 'out"',
    '"std' + 'err"',
    '"raw_' + 'logs"',
    '"to' + 'ken"',
    '"api_' + 'key"',
    '"sec' + 'ret"',
    '"pass' + 'word"',
    '"creden' + 'tial"',
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
    "http" + "://",
    "https" + "://",
    "ssh" + "://",
    "git" + "@",
    "/users/",
    "/private/",
    "/tmp/",
    "c:\\",
    "tool_" + "call",
    "adapter_" + "dispatch",
    "manifest_" + "dispatch",
    "git " + "push",
    "g" + "h api",
)


def build_governance_execution_adapter_manifest_validation_matrix() -> dict[str, Any]:
    """Build deterministic validation-only manifest matrix metadata."""

    fixture_pack = _detached_json_value(
        build_governance_execution_adapter_manifest_fixture_pack()
    )
    fixture_pack_repeat = _detached_json_value(
        build_governance_execution_adapter_manifest_fixture_pack()
    )
    rows = _build_manifest_validation_rows(fixture_pack, fixture_pack_repeat)
    contracts = _build_manifest_validation_contracts(
        fixture_pack,
        fixture_pack_repeat,
        rows,
    )
    checks = _build_manifest_validation_checks(
        fixture_pack,
        fixture_pack_repeat,
        rows,
        contracts,
    )

    fixture_pack_passes = _fixture_pack_passes(fixture_pack)
    rows_pass = all(row["row_status"] == "pass" for row in rows)
    contracts_pass = all(
        contract["contract_status"] == "pass" for contract in contracts
    )
    checks_pass = all(check["check_status"] == "pass" for check in checks)
    matrix_status = (
        "pass"
        if fixture_pack_passes and rows_pass and contracts_pass and checks_pass
        else "blocked"
    )
    blocking_reasons = _deduplicate(
        [
            *(
                ["manifest fixture pack must pass at version 5.5.0"]
                if not fixture_pack_passes
                else []
            ),
            *(reason for row in rows for reason in row["blocking_reasons"]),
            *(
                reason
                for contract in contracts
                for reason in contract["blocking_reasons"]
            ),
            *(reason for check in checks for reason in check["blocking_reasons"]),
        ]
    )
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    matrix: dict[str, Any] = {
        "version": GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_VALIDATION_MATRIX_VERSION,
        "schema_version": (
            GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_VALIDATION_MATRIX_SCHEMA_VERSION
        ),
        "manifest_validation_matrix_type": (
            GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_VALIDATION_MATRIX_TYPE
        ),
        "manifest_validation_matrix_status": matrix_status,
        "manifest_validation_matrix_stage": (
            EXECUTION_ADAPTER_MANIFEST_VALIDATION_MATRIX_STAGE
        ),
        "manifest_validation_matrix_mode": MANIFEST_VALIDATION_MATRIX_MODE,
        "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
        **COMMON_DISABLED_FLAGS,
        "manifest_fixture_pack_version": _string_or_none(
            fixture_pack.get("version")
        ),
        "manifest_fixture_pack_status": _string_or_none(
            fixture_pack.get("manifest_fixture_pack_status")
        ),
        "manifest_fixture_pack_hash": _string_or_none(
            fixture_pack.get("deterministic_manifest_fixture_pack_hash")
        ),
        "manifest_validation_rows": rows,
        "manifest_validation_contracts": contracts,
        "manifest_validation_checks": checks,
        "manifest_validation_matrix_summary": (
            _manifest_validation_matrix_summary(rows, contracts, checks)
        ),
        "handoff_status": (
            READY_HANDOFF_STATUS
            if matrix_status == "pass"
            else BLOCKED_HANDOFF_STATUS
        ),
        "blocking_reasons": blocking_reasons,
        "hash_input_contract": _detached_json_value(HASH_INPUT_CONTRACT),
        "safety_boundaries": safety_boundaries,
        **safety_boundaries,
    }
    matrix["deterministic_manifest_validation_matrix_hash"] = (
        _execution_adapter_manifest_validation_matrix_hash(matrix)
    )
    return _detached_json_value(matrix)


def get_governance_execution_adapter_manifest_validation_row(
    name: str,
) -> dict[str, Any]:
    """Return a detached manifest validation row by stable name."""

    if not isinstance(name, str):
        return _unknown_row("")
    matrix = build_governance_execution_adapter_manifest_validation_matrix()
    for row in matrix["manifest_validation_rows"]:
        if row["row_name"] == name:
            return _detached_json_value(row)
    return _unknown_row(name)


def get_governance_execution_adapter_manifest_validation_contract(
    name: str,
) -> dict[str, Any]:
    """Return a detached manifest validation contract by stable name."""

    if not isinstance(name, str):
        return _unknown_contract("")
    matrix = build_governance_execution_adapter_manifest_validation_matrix()
    for contract in matrix["manifest_validation_contracts"]:
        if contract["contract_name"] == name:
            return _detached_json_value(contract)
    return _unknown_contract(name)


def get_governance_execution_adapter_manifest_validation_check(
    name: str,
) -> dict[str, Any]:
    """Return a detached manifest validation check by stable name."""

    if not isinstance(name, str):
        return _unknown_check("")
    matrix = build_governance_execution_adapter_manifest_validation_matrix()
    for check in matrix["manifest_validation_checks"]:
        if check["check_name"] == name:
            return _detached_json_value(check)
    return _unknown_check(name)


def list_governance_execution_adapter_manifest_validation_row_names() -> list[str]:
    """Return stable manifest validation row names."""

    return list(REQUIRED_MANIFEST_VALIDATION_ROW_NAMES)


def list_governance_execution_adapter_manifest_validation_contract_names() -> list[str]:
    """Return stable manifest validation contract names."""

    return list(REQUIRED_MANIFEST_VALIDATION_CONTRACT_NAMES)


def list_governance_execution_adapter_manifest_validation_check_names() -> list[str]:
    """Return stable manifest validation check names."""

    return list(REQUIRED_MANIFEST_VALIDATION_CHECK_NAMES)


def governance_execution_adapter_manifest_validation_matrix_to_json(
    result: Mapping[str, Any],
) -> str:
    """Serialize manifest validation-matrix metadata deterministically."""

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


def _build_manifest_validation_rows(
    fixture_pack: Mapping[str, Any],
    fixture_pack_repeat: Mapping[str, Any],
) -> list[dict[str, Any]]:
    payload_findings = _fixture_payload_findings(fixture_pack)
    return [
        _fixture_validation_row(
            fixture_pack,
            "minimal_read_only_fixture_validation_row",
            row_type="fixture_structure_validation",
            fixture_refs=["minimal_read_only_manifest_fixture"],
            contract_refs=[
                "fixture_pack_only_contract",
                "sanitized_fixture_payload_contract",
                "adapter_not_invoked_fixture_contract",
            ],
            check_refs=[
                "fixture_only_mode_check",
                "fixture_payloads_sanitized_check",
                "adapter_not_invoked_check",
            ],
            notes=[
                "minimal fixture remains metadata only",
                "read-only fixture does not enable runtime behavior",
            ],
        ),
        _fixture_validation_row(
            fixture_pack,
            "permission_declared_fixture_validation_row",
            row_type="fixture_contract_validation",
            fixture_refs=["permission_declared_manifest_fixture"],
            contract_refs=[
                "fixture_payload_json_contract",
                "external_calls_disabled_fixture_contract",
            ],
            check_refs=[
                "fixture_payloads_json_compatible_check",
                "real_execution_disabled_check",
                "external_calls_disabled_check",
            ],
            notes=[
                "permission fixture remains declaration metadata",
                "permission declaration does not grant execution authority",
            ],
        ),
        _fixture_validation_row(
            fixture_pack,
            "external_dependency_declared_fixture_validation_row",
            row_type="fixture_dependency_validation",
            fixture_refs=["external_dependency_declared_manifest_fixture"],
            contract_refs=[
                "no_live_endpoint_fixture_contract",
                "external_calls_disabled_fixture_contract",
            ],
            check_refs=[
                "no_live_endpoint_check",
                "external_calls_disabled_check",
            ],
            notes=[
                "external dependency fixture uses synthetic disabled metadata",
                "no live endpoint locator is included",
            ],
        ),
        _fixture_validation_row(
            fixture_pack,
            "durable_write_disabled_fixture_validation_row",
            row_type="fixture_write_boundary_validation",
            fixture_refs=[
                "durable_write_declared_but_disabled_manifest_fixture"
            ],
            contract_refs=[
                "durable_writes_disabled_fixture_contract",
                "filesystem_writes_disabled_fixture_contract",
                "database_writes_disabled_fixture_contract",
            ],
            check_refs=[
                "durable_writes_disabled_check",
                "filesystem_writes_disabled_check",
                "database_writes_disabled_check",
            ],
            notes=[
                "durable write fixture is declared only",
                "storage side effects remain disabled",
            ],
        ),
        _fixture_validation_row(
            fixture_pack,
            "memory_graph_mutation_disabled_fixture_validation_row",
            row_type="fixture_graph_boundary_validation",
            fixture_refs=[
                "memory_graph_mutation_declared_but_disabled_manifest_fixture"
            ],
            contract_refs=["memory_graph_mutation_disabled_fixture_contract"],
            check_refs=["memory_graph_mutation_disabled_check"],
            notes=[
                "graph mutation fixture remains declared only",
                "graph mutation behavior remains disabled",
            ],
        ),
        _fixture_validation_row(
            fixture_pack,
            "operation_ledger_write_disabled_fixture_validation_row",
            row_type="fixture_ledger_boundary_validation",
            fixture_refs=[
                "operation_ledger_write_declared_but_disabled_manifest_fixture"
            ],
            contract_refs=[
                "operation_ledger_writes_disabled_fixture_contract"
            ],
            check_refs=["operation_ledger_writes_disabled_check"],
            notes=[
                "ledger write fixture remains declared only",
                "ledger side effects remain disabled",
            ],
        ),
        _fixture_validation_row(
            fixture_pack,
            "approval_required_fixture_validation_row",
            row_type="fixture_approval_boundary_validation",
            fixture_refs=["approval_required_manifest_fixture"],
            contract_refs=[
                "fixture_pack_only_contract",
                "manifest_not_executed_fixture_contract",
                "star_cosmos_candidate_only_fixture_contract",
            ],
            check_refs=[
                "manifest_not_executed_check",
                "dry_run_plan_not_executed_check",
                "autonomous_execution_disabled_check",
            ],
            notes=[
                "human review requirement is metadata only",
                "approval requirement does not authorize execution",
            ],
        ),
        _fixture_validation_row(
            fixture_pack,
            "redaction_required_fixture_validation_row",
            row_type="fixture_redaction_boundary_validation",
            fixture_refs=["redaction_required_manifest_fixture"],
            contract_refs=[
                "sanitized_fixture_payload_contract",
                "no_secret_fixture_contract",
                "no_raw_log_fixture_contract",
            ],
            check_refs=[
                "fixture_payloads_sanitized_check",
                "no_secret_or_token_check",
                "no_raw_log_check",
                "redaction_boundary_check",
            ],
            notes=[
                "redaction fixture keeps raw values absent",
                "sanitized placeholder metadata is expected",
            ],
        ),
        _fixture_validation_row(
            fixture_pack,
            "star_cosmos_candidate_only_fixture_validation_row",
            row_type="fixture_candidate_boundary_validation",
            fixture_refs=["star_cosmos_candidate_only_manifest_fixture"],
            contract_refs=["star_cosmos_candidate_only_fixture_contract"],
            check_refs=["star_cosmos_candidate_only_check"],
            notes=[
                "candidate-only status remains explicit",
                "active-entry status is not claimed",
            ],
        ),
        _fixture_pack_integrity_row(fixture_pack),
        _fixture_contract_integrity_row(fixture_pack),
        _fixture_check_integrity_row(fixture_pack),
        _deterministic_hash_row(fixture_pack, fixture_pack_repeat),
        _sanitized_payload_row(fixture_pack, payload_findings),
        _safety_boundary_row(fixture_pack),
        _candidate_only_boundary_row(fixture_pack),
    ]


def _build_manifest_validation_contracts(
    fixture_pack: Mapping[str, Any],
    fixture_pack_repeat: Mapping[str, Any],
    rows: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    row_names = _row_names(rows)
    payload_findings = _fixture_payload_findings(fixture_pack)
    return [
        _contract(
            "validation_matrix_only_contract",
            contract_type="manifest_validation_matrix_contract",
            expected={
                "manifest_validation_matrix_mode": MANIFEST_VALIDATION_MATRIX_MODE,
                "manifest_executed": False,
                "dry_run_plan_executed": False,
            },
            observed={
                "manifest_validation_matrix_mode": MANIFEST_VALIDATION_MATRIX_MODE,
                "manifest_executed": False,
                "dry_run_plan_executed": False,
            },
        ),
        _contract(
            "manifest_fixture_pack_pass_contract",
            contract_type="upstream_manifest_fixture_pack_contract",
            expected={
                "manifest_fixture_pack_status": "pass",
                "manifest_fixture_pack_version": (
                    GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_VALIDATION_MATRIX_VERSION
                ),
                "manifest_fixture_pack_hash_present": True,
            },
            observed={
                "manifest_fixture_pack_status": _string_or_none(
                    fixture_pack.get("manifest_fixture_pack_status")
                ),
                "manifest_fixture_pack_version": _string_or_none(
                    fixture_pack.get("version")
                ),
                "manifest_fixture_pack_hash_present": _is_sha256(
                    _string_or_none(
                        fixture_pack.get(
                            "deterministic_manifest_fixture_pack_hash"
                        )
                    )
                ),
            },
            blocking_reasons=_fixture_pack_blocking_reasons(fixture_pack),
        ),
        _contract(
            "validation_row_names_complete_contract",
            contract_type="validation_row_name_contract",
            expected={
                "row_names": list(REQUIRED_MANIFEST_VALIDATION_ROW_NAMES),
                "row_count": len(REQUIRED_MANIFEST_VALIDATION_ROW_NAMES),
            },
            observed={
                "row_names": row_names,
                "row_count": len(row_names),
                "missing_row_names": _missing_row_names(row_names),
                "extra_row_names": _extra_row_names(row_names),
            },
            blocking_reasons=_row_name_blocking_reasons(row_names),
        ),
        _contract(
            "validation_rows_pass_contract",
            contract_type="validation_row_status_contract",
            expected={"rows_pass": True, "blocked_row_count": 0},
            observed={
                "rows_pass": _rows_pass(rows),
                "blocked_row_count": len(_blocked_row_names(rows)),
                "blocked_row_names": _blocked_row_names(rows),
            },
            blocking_reasons=[]
            if _rows_pass(rows)
            else ["manifest validation rows must pass"],
        ),
        _hash_present_contract(fixture_pack),
        _hash_stable_contract(fixture_pack, fixture_pack_repeat),
        _contract(
            "fixture_payload_sanitized_contract",
            contract_type="fixture_payload_validation_contract",
            expected={
                "blocked_fragment_hit_count": 0,
                "payload_count": len(_manifest_fixtures(fixture_pack)),
            },
            observed={
                "blocked_fragment_hit_count": len(payload_findings),
                "payload_count": len(_manifest_fixtures(fixture_pack)),
            },
            blocking_reasons=[]
            if not payload_findings
            else ["fixture payloads must not include blocked fragments"],
        ),
        _contract_status_contract(
            "fixture_contracts_pass_contract",
            fixture_pack,
        ),
        _check_status_contract("fixture_checks_pass_contract", fixture_pack),
        _blocked_fragment_contract(
            "no_executable_command_validation_contract",
            "executable_command_present",
            payload_findings,
        ),
        _blocked_fragment_contract(
            "no_live_endpoint_validation_contract",
            "live_endpoint_present",
            payload_findings,
        ),
        _blocked_fragment_contract(
            "no_secret_validation_contract",
            "sensitive_fragment_present",
            payload_findings,
        ),
        _blocked_fragment_contract(
            "no_raw_log_validation_contract",
            "log_material_present",
            payload_findings,
        ),
        _disabled_flag_contract(
            "adapter_not_implemented_validation_contract",
            "execution_adapter_implemented",
            fixture_pack,
        ),
        _disabled_flag_contract(
            "adapter_not_invoked_validation_contract",
            "execution_adapter_invoked",
            fixture_pack,
        ),
        _disabled_flag_contract(
            "manifest_not_executed_validation_contract",
            "manifest_executed",
            fixture_pack,
        ),
        _disabled_flag_contract(
            "dry_run_plan_not_executed_validation_contract",
            "dry_run_plan_executed",
            fixture_pack,
        ),
        _disabled_flag_contract(
            "real_execution_disabled_validation_contract",
            "real_execution_enabled",
            fixture_pack,
        ),
        _disabled_flag_contract(
            "external_calls_disabled_validation_contract",
            "external_calls_enabled",
            fixture_pack,
        ),
        _disabled_flag_contract(
            "durable_writes_disabled_validation_contract",
            "durable_writes_enabled",
            fixture_pack,
        ),
        _disabled_flag_contract(
            "filesystem_writes_disabled_validation_contract",
            "filesystem_writes_enabled",
            fixture_pack,
        ),
        _disabled_flag_contract(
            "database_writes_disabled_validation_contract",
            "database_writes_enabled",
            fixture_pack,
        ),
        _disabled_flag_contract(
            "memory_graph_mutation_disabled_validation_contract",
            "memory_graph_mutation_enabled",
            fixture_pack,
        ),
        _disabled_flag_contract(
            "operation_ledger_writes_disabled_validation_contract",
            "operation_ledger_writes_enabled",
            fixture_pack,
        ),
        _disabled_flag_contract(
            "autonomous_execution_disabled_validation_contract",
            "autonomous_execution_enabled",
            fixture_pack,
        ),
        _contract(
            "star_cosmos_candidate_only_validation_contract",
            contract_type="candidate_validation_contract",
            expected={
                "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
                "star_cosmos_memory_active": False,
            },
            observed={
                "star_cosmos_entry_status": _string_or_none(
                    fixture_pack.get("star_cosmos_entry_status")
                ),
                "star_cosmos_memory_active": (
                    False
                    if _pack_flag_false(
                        fixture_pack,
                        "star_cosmos_memory_active",
                    )
                    else True
                ),
            },
            blocking_reasons=[]
            if fixture_pack.get("star_cosmos_entry_status")
            == STAR_COSMOS_ENTRY_STATUS
            and _pack_flag_false(fixture_pack, "star_cosmos_memory_active")
            else ["Star-Cosmos candidate-only boundary must remain false-active"],
        ),
    ]


def _build_manifest_validation_checks(
    fixture_pack: Mapping[str, Any],
    fixture_pack_repeat: Mapping[str, Any],
    rows: Sequence[Mapping[str, Any]],
    contracts: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    row_names = _row_names(rows)
    payload_findings = _fixture_payload_findings(fixture_pack)
    return [
        _check(
            "manifest_fixture_pack_pass_check",
            expected={
                "manifest_fixture_pack_status": "pass",
                "manifest_fixture_pack_version": (
                    GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_VALIDATION_MATRIX_VERSION
                ),
                "manifest_fixture_pack_hash_present": True,
            },
            observed={
                "manifest_fixture_pack_status": _string_or_none(
                    fixture_pack.get("manifest_fixture_pack_status")
                ),
                "manifest_fixture_pack_version": _string_or_none(
                    fixture_pack.get("version")
                ),
                "manifest_fixture_pack_hash_present": _is_sha256(
                    _string_or_none(
                        fixture_pack.get(
                            "deterministic_manifest_fixture_pack_hash"
                        )
                    )
                ),
            },
            blocking_reasons=_fixture_pack_blocking_reasons(fixture_pack),
        ),
        _simple_check(
            "manifest_validation_matrix_stage_check",
            EXECUTION_ADAPTER_MANIFEST_VALIDATION_MATRIX_STAGE,
            EXECUTION_ADAPTER_MANIFEST_VALIDATION_MATRIX_STAGE,
        ),
        _simple_check(
            "validation_only_mode_check",
            MANIFEST_VALIDATION_MATRIX_MODE,
            MANIFEST_VALIDATION_MATRIX_MODE,
        ),
        _check(
            "validation_row_names_complete_check",
            expected={
                "row_names": list(REQUIRED_MANIFEST_VALIDATION_ROW_NAMES),
                "row_count": len(REQUIRED_MANIFEST_VALIDATION_ROW_NAMES),
            },
            observed={
                "row_names": row_names,
                "row_count": len(row_names),
                "missing_row_names": _missing_row_names(row_names),
                "extra_row_names": _extra_row_names(row_names),
            },
            blocking_reasons=_row_name_blocking_reasons(row_names),
        ),
        _check(
            "validation_rows_pass_check",
            expected={"rows_pass": True, "blocked_row_count": 0},
            observed={
                "rows_pass": _rows_pass(rows),
                "blocked_row_count": len(_blocked_row_names(rows)),
                "blocked_row_names": _blocked_row_names(rows),
            },
            blocking_reasons=[]
            if _rows_pass(rows)
            else ["manifest validation rows must pass"],
        ),
        _check(
            "validation_contracts_pass_check",
            expected={"contracts_pass": True, "blocked_contract_count": 0},
            observed={
                "contracts_pass": _contracts_pass(contracts),
                "blocked_contract_count": len(_blocked_contract_names(contracts)),
                "blocked_contract_names": _blocked_contract_names(contracts),
            },
            blocking_reasons=[]
            if _contracts_pass(contracts)
            else ["manifest validation contracts must pass"],
        ),
        _hash_present_check(fixture_pack),
        _hash_stable_check(fixture_pack, fixture_pack_repeat),
        _payload_findings_check(
            "fixture_payloads_sanitized_check",
            payload_findings,
        ),
        _contract_status_check("fixture_contracts_pass_check", fixture_pack),
        _fixture_check_status_check("fixture_checks_pass_check", fixture_pack),
        _payload_findings_check("no_executable_command_check", payload_findings),
        _payload_findings_check("no_live_endpoint_check", payload_findings),
        _payload_findings_check("no_secret_or_token_check", payload_findings),
        _payload_findings_check("no_raw_log_check", payload_findings),
        _flag_check(
            "adapter_not_implemented_check",
            "execution_adapter_implemented",
            fixture_pack,
        ),
        _flag_check(
            "adapter_not_invoked_check",
            "execution_adapter_invoked",
            fixture_pack,
        ),
        _flag_check(
            "manifest_not_executed_check",
            "manifest_executed",
            fixture_pack,
        ),
        _flag_check(
            "dry_run_plan_not_executed_check",
            "dry_run_plan_executed",
            fixture_pack,
        ),
        _flag_check(
            "real_execution_disabled_check",
            "real_execution_enabled",
            fixture_pack,
        ),
        _flag_check(
            "external_calls_disabled_check",
            "external_calls_enabled",
            fixture_pack,
        ),
        _flag_check(
            "durable_writes_disabled_check",
            "durable_writes_enabled",
            fixture_pack,
        ),
        _flag_check(
            "filesystem_writes_disabled_check",
            "filesystem_writes_enabled",
            fixture_pack,
        ),
        _flag_check(
            "database_writes_disabled_check",
            "database_writes_enabled",
            fixture_pack,
        ),
        _flag_check(
            "memory_graph_mutation_disabled_check",
            "memory_graph_mutation_enabled",
            fixture_pack,
        ),
        _flag_check(
            "operation_ledger_writes_disabled_check",
            "operation_ledger_writes_enabled",
            fixture_pack,
        ),
        _flag_check(
            "autonomous_execution_disabled_check",
            "autonomous_execution_enabled",
            fixture_pack,
        ),
        _check(
            "star_cosmos_candidate_only_check",
            expected={
                "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
                "star_cosmos_memory_active": False,
            },
            observed={
                "star_cosmos_entry_status": _string_or_none(
                    fixture_pack.get("star_cosmos_entry_status")
                ),
                "star_cosmos_memory_active": (
                    False
                    if _pack_flag_false(
                        fixture_pack,
                        "star_cosmos_memory_active",
                    )
                    else True
                ),
            },
            blocking_reasons=[]
            if fixture_pack.get("star_cosmos_entry_status")
            == STAR_COSMOS_ENTRY_STATUS
            and _pack_flag_false(fixture_pack, "star_cosmos_memory_active")
            else ["Star-Cosmos candidate-only boundary must remain false-active"],
        ),
        _deterministic_hash_check(fixture_pack, fixture_pack_repeat, rows, contracts),
        _payload_findings_check("redaction_boundary_check", payload_findings),
    ]


def _fixture_validation_row(
    fixture_pack: Mapping[str, Any],
    row_name: str,
    *,
    row_type: str,
    fixture_refs: Sequence[str],
    contract_refs: Sequence[str],
    check_refs: Sequence[str],
    notes: Sequence[str],
) -> dict[str, Any]:
    fixture_status = _fixture_statuses(fixture_pack, fixture_refs)
    contract_status = _fixture_contract_statuses(fixture_pack, contract_refs)
    check_status = _fixture_check_statuses(fixture_pack, check_refs)
    disabled_flags_false = all(
        _pack_flag_false(fixture_pack, flag_name)
        for flag_name in COMMON_DISABLED_FLAGS
    )
    blocking_reasons = _deduplicate(
        [
            *(
                f"fixture {name} must pass"
                for name, status in fixture_status.items()
                if status != "pass"
            ),
            *(
                f"fixture contract {name} must pass"
                for name, status in contract_status.items()
                if status != "pass"
            ),
            *(
                f"fixture check {name} must pass"
                for name, status in check_status.items()
                if status != "pass"
            ),
            *(
                ["all disabled runtime flags must remain false"]
                if not disabled_flags_false
                else []
            ),
        ]
    )
    return _row(
        row_name,
        row_type=row_type,
        source_fixture_refs=fixture_refs,
        source_contract_refs=contract_refs,
        source_check_refs=check_refs,
        expected={
            "source_fixtures_pass": True,
            "source_contracts_pass": True,
            "source_checks_pass": True,
            "disabled_runtime_flags_false": True,
        },
        observed={
            "fixture_statuses": fixture_status,
            "contract_statuses": contract_status,
            "check_statuses": check_status,
            "disabled_runtime_flags_false": disabled_flags_false,
        },
        validation_notes=notes,
        blocking_reasons=blocking_reasons,
    )


def _fixture_pack_integrity_row(
    fixture_pack: Mapping[str, Any],
) -> dict[str, Any]:
    fixture_names = _fixture_names(fixture_pack)
    blocking_reasons = _deduplicate(
        [
            *(["manifest fixture names must be complete"] if _missing_fixture_names(fixture_names) else []),
            *(["manifest fixture names must not include extras"] if _extra_fixture_names(fixture_names) else []),
            *(
                ["manifest fixture pack must pass"]
                if fixture_pack.get("manifest_fixture_pack_status") != "pass"
                else []
            ),
        ]
    )
    return _row(
        "fixture_pack_integrity_validation_row",
        row_type="fixture_pack_integrity_validation",
        source_fixture_refs=fixture_names,
        source_contract_refs=["fixture_names_complete_contract"],
        source_check_refs=["fixture_names_complete_check"],
        expected={
            "fixture_names": list(_expected_fixture_names()),
            "fixture_pack_status": "pass",
        },
        observed={
            "fixture_names": fixture_names,
            "missing_fixture_names": _missing_fixture_names(fixture_names),
            "extra_fixture_names": _extra_fixture_names(fixture_names),
            "fixture_pack_status": _string_or_none(
                fixture_pack.get("manifest_fixture_pack_status")
            ),
        },
        validation_notes=[
            "fixture pack exposes the expected deterministic fixture set",
            "fixture pack status is used as upstream gate metadata",
        ],
        blocking_reasons=blocking_reasons,
    )


def _fixture_contract_integrity_row(
    fixture_pack: Mapping[str, Any],
) -> dict[str, Any]:
    contract_names = _fixture_contract_names(fixture_pack)
    blocked_contracts = _blocked_fixture_contract_names(fixture_pack)
    return _row(
        "fixture_contract_integrity_validation_row",
        row_type="fixture_contract_integrity_validation",
        source_fixture_refs=[],
        source_contract_refs=contract_names,
        source_check_refs=["fixture_contracts_pass_check"],
        expected={"fixture_contracts_pass": True, "blocked_contract_count": 0},
        observed={
            "fixture_contracts_pass": not blocked_contracts,
            "blocked_contract_count": len(blocked_contracts),
            "blocked_contract_names": blocked_contracts,
        },
        validation_notes=[
            "fixture contracts remain metadata-only pass contracts",
            "contract names are consumed without copying fixture payload content",
        ],
        blocking_reasons=[]
        if not blocked_contracts
        else ["manifest fixture contracts must pass"],
    )


def _fixture_check_integrity_row(
    fixture_pack: Mapping[str, Any],
) -> dict[str, Any]:
    check_names = _fixture_check_names(fixture_pack)
    blocked_checks = _blocked_fixture_check_names(fixture_pack)
    return _row(
        "fixture_check_integrity_validation_row",
        row_type="fixture_check_integrity_validation",
        source_fixture_refs=[],
        source_contract_refs=[],
        source_check_refs=check_names,
        expected={"fixture_checks_pass": True, "blocked_check_count": 0},
        observed={
            "fixture_checks_pass": not blocked_checks,
            "blocked_check_count": len(blocked_checks),
            "blocked_check_names": blocked_checks,
        },
        validation_notes=[
            "fixture checks remain deterministic pass metadata",
            "check names are consumed without runtime dispatch",
        ],
        blocking_reasons=[]
        if not blocked_checks
        else ["manifest fixture checks must pass"],
    )


def _deterministic_hash_row(
    fixture_pack: Mapping[str, Any],
    fixture_pack_repeat: Mapping[str, Any],
) -> dict[str, Any]:
    fixture_hash = _string_or_none(
        fixture_pack.get("deterministic_manifest_fixture_pack_hash")
    )
    repeat_hash = _string_or_none(
        fixture_pack_repeat.get("deterministic_manifest_fixture_pack_hash")
    )
    stable = fixture_hash == repeat_hash
    blocking_reasons = _deduplicate(
        [
            *(["manifest fixture pack hash must be sha256"] if not _is_sha256(fixture_hash) else []),
            *(["manifest fixture pack hash must be stable"] if not stable else []),
        ]
    )
    return _row(
        "deterministic_hash_validation_row",
        row_type="deterministic_hash_validation",
        source_fixture_refs=[],
        source_contract_refs=[
            "fixture_pack_hash_present_contract",
            "fixture_pack_hash_stable_contract",
        ],
        source_check_refs=[
            "fixture_pack_hash_present_check",
            "fixture_pack_hash_stable_check",
            "deterministic_hash_check",
        ],
        expected={
            "fixture_pack_hash_present": True,
            "fixture_pack_hash_stable": True,
            "hash_algorithm": (
                GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_VALIDATION_MATRIX_HASH_ALGORITHM
            ),
        },
        observed={
            "fixture_pack_hash_present": _is_sha256(fixture_hash),
            "fixture_pack_hash_stable": stable,
            "hash_algorithm": (
                GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_VALIDATION_MATRIX_HASH_ALGORITHM
            ),
        },
        validation_notes=[
            "fixture pack hash is consumed as deterministic metadata",
            "validation matrix hash input remains row-contract-check sensitive",
        ],
        blocking_reasons=blocking_reasons,
    )


def _sanitized_payload_row(
    fixture_pack: Mapping[str, Any],
    payload_findings: Sequence[str],
) -> dict[str, Any]:
    fixture_count = len(_manifest_fixtures(fixture_pack))
    return _row(
        "sanitized_payload_validation_row",
        row_type="fixture_payload_sanitization_validation",
        source_fixture_refs=_fixture_names(fixture_pack),
        source_contract_refs=[
            "sanitized_fixture_payload_contract",
            "no_executable_command_fixture_contract",
            "no_live_endpoint_fixture_contract",
            "no_secret_fixture_contract",
            "no_raw_log_fixture_contract",
        ],
        source_check_refs=[
            "fixture_payloads_sanitized_check",
            "no_executable_command_check",
            "no_live_endpoint_check",
            "no_secret_or_token_check",
            "no_raw_log_check",
            "redaction_boundary_check",
        ],
        expected={
            "blocked_fragment_hit_count": 0,
            "fixture_payload_count": fixture_count,
            "raw_fixture_events_included": False,
        },
        observed={
            "blocked_fragment_hit_count": len(payload_findings),
            "fixture_payload_count": fixture_count,
            "raw_fixture_events_included": False,
        },
        validation_notes=[
            "validation row records only payload sanitization counts",
            "raw fixture payload values are not included in this row",
        ],
        blocking_reasons=[]
        if not payload_findings
        else ["fixture payloads must not include blocked fragments"],
    )


def _safety_boundary_row(fixture_pack: Mapping[str, Any]) -> dict[str, Any]:
    safety_flags_false = _all_safety_flags_false(fixture_pack)
    disabled_flags_false = all(
        _pack_flag_false(fixture_pack, flag_name)
        for flag_name in COMMON_DISABLED_FLAGS
    )
    return _row(
        "safety_boundary_validation_row",
        row_type="safety_boundary_validation",
        source_fixture_refs=_fixture_names(fixture_pack),
        source_contract_refs=_fixture_contract_names(fixture_pack),
        source_check_refs=_fixture_check_names(fixture_pack),
        expected={
            "safety_flags_false": True,
            "disabled_runtime_flags_false": True,
        },
        observed={
            "safety_flags_false": safety_flags_false,
            "disabled_runtime_flags_false": disabled_flags_false,
        },
        validation_notes=[
            "safety boundary fields remain false across fixture pack metadata",
            "validation matrix mirrors the same disabled runtime boundary",
        ],
        blocking_reasons=_deduplicate(
            [
                *(
                    ["safety boundary flags must remain false"]
                    if not safety_flags_false
                    else []
                ),
                *(
                    ["disabled runtime flags must remain false"]
                    if not disabled_flags_false
                    else []
                ),
            ]
        ),
    )


def _candidate_only_boundary_row(
    fixture_pack: Mapping[str, Any],
) -> dict[str, Any]:
    candidate_fixture = _fixture_by_name(
        fixture_pack,
        "star_cosmos_candidate_only_manifest_fixture",
    )
    candidate_fixture_status = (
        _string_or_none(candidate_fixture.get("fixture_status"))
        if isinstance(candidate_fixture, Mapping)
        else None
    )
    star_false = _pack_flag_false(fixture_pack, "star_cosmos_memory_active")
    return _row(
        "candidate_only_boundary_validation_row",
        row_type="candidate_only_boundary_validation",
        source_fixture_refs=["star_cosmos_candidate_only_manifest_fixture"],
        source_contract_refs=["star_cosmos_candidate_only_fixture_contract"],
        source_check_refs=["star_cosmos_candidate_only_check"],
        expected={
            "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
            "star_cosmos_memory_active": False,
            "candidate_fixture_status": "pass",
        },
        observed={
            "star_cosmos_entry_status": _string_or_none(
                fixture_pack.get("star_cosmos_entry_status")
            ),
            "star_cosmos_memory_active": False if star_false else True,
            "candidate_fixture_status": candidate_fixture_status,
        },
        validation_notes=[
            "candidate-only state is retained for future policy gate design",
            "active-entry status is not asserted",
        ],
        blocking_reasons=_deduplicate(
            [
                *(
                    ["Star-Cosmos entry status must remain candidate-only"]
                    if fixture_pack.get("star_cosmos_entry_status")
                    != STAR_COSMOS_ENTRY_STATUS
                    else []
                ),
                *(
                    ["Star-Cosmos memory active flag must remain false"]
                    if not star_false
                    else []
                ),
                *(
                    ["candidate fixture must pass"]
                    if candidate_fixture_status != "pass"
                    else []
                ),
            ]
        ),
    )


def _row(
    row_name: str,
    *,
    row_type: str,
    source_fixture_refs: Sequence[str],
    source_contract_refs: Sequence[str],
    source_check_refs: Sequence[str],
    expected: Mapping[str, Any],
    observed: Mapping[str, Any],
    validation_notes: Sequence[str],
    blocking_reasons: Sequence[str] = (),
) -> dict[str, Any]:
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    row: dict[str, Any] = {
        "row_name": row_name,
        "row_type": row_type,
        "row_status": "pass" if not blocking_reasons else "blocked",
        "source_fixture_refs": list(source_fixture_refs),
        "source_contract_refs": list(source_contract_refs),
        "source_check_refs": list(source_check_refs),
        "expected": _detached_json_value(expected),
        "observed": _detached_json_value(observed),
        "validation_notes": list(validation_notes),
        "blocking_reasons": _deduplicate(blocking_reasons),
        "safety_boundaries": safety_boundaries,
        **COMMON_DISABLED_FLAGS,
        **safety_boundaries,
    }
    return _detached_json_value(row)


def _contract(
    contract_name: str,
    *,
    contract_type: str,
    expected: Mapping[str, Any],
    observed: Mapping[str, Any],
    blocking_reasons: Sequence[str] = (),
) -> dict[str, Any]:
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    contract: dict[str, Any] = {
        "contract_name": contract_name,
        "contract_type": contract_type,
        "expected": _detached_json_value(expected),
        "observed": _detached_json_value(observed),
        "contract_status": "pass" if not blocking_reasons else "blocked",
        "blocking_reasons": _deduplicate(blocking_reasons),
        "safety_boundaries": safety_boundaries,
        **COMMON_DISABLED_FLAGS,
        **safety_boundaries,
    }
    return _detached_json_value(contract)


def _check(
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
        **COMMON_DISABLED_FLAGS,
        **safety_boundaries,
    }
    return _detached_json_value(check)


def _simple_check(
    check_name: str,
    expected: bool | str,
    observed: bool | str,
) -> dict[str, Any]:
    return _check(
        check_name,
        expected={"value": expected},
        observed={"value": observed},
        blocking_reasons=[] if observed == expected else [f"{check_name} mismatch"],
    )


def _hash_present_contract(fixture_pack: Mapping[str, Any]) -> dict[str, Any]:
    fixture_hash = _string_or_none(
        fixture_pack.get("deterministic_manifest_fixture_pack_hash")
    )
    return _contract(
        "fixture_pack_hash_present_contract",
        contract_type="fixture_pack_hash_contract",
        expected={"manifest_fixture_pack_hash_present": True},
        observed={"manifest_fixture_pack_hash_present": _is_sha256(fixture_hash)},
        blocking_reasons=[]
        if _is_sha256(fixture_hash)
        else ["manifest fixture pack hash must be sha256"],
    )


def _hash_stable_contract(
    fixture_pack: Mapping[str, Any],
    fixture_pack_repeat: Mapping[str, Any],
) -> dict[str, Any]:
    fixture_hash = _string_or_none(
        fixture_pack.get("deterministic_manifest_fixture_pack_hash")
    )
    repeat_hash = _string_or_none(
        fixture_pack_repeat.get("deterministic_manifest_fixture_pack_hash")
    )
    return _contract(
        "fixture_pack_hash_stable_contract",
        contract_type="fixture_pack_hash_contract",
        expected={"manifest_fixture_pack_hash_stable": True},
        observed={"manifest_fixture_pack_hash_stable": fixture_hash == repeat_hash},
        blocking_reasons=[]
        if fixture_hash == repeat_hash
        else ["manifest fixture pack hash must be stable"],
    )


def _contract_status_contract(
    contract_name: str,
    fixture_pack: Mapping[str, Any],
) -> dict[str, Any]:
    blocked_contracts = _blocked_fixture_contract_names(fixture_pack)
    return _contract(
        contract_name,
        contract_type="fixture_contract_status_contract",
        expected={"fixture_contracts_pass": True, "blocked_contract_count": 0},
        observed={
            "fixture_contracts_pass": not blocked_contracts,
            "blocked_contract_count": len(blocked_contracts),
            "blocked_contract_names": blocked_contracts,
        },
        blocking_reasons=[]
        if not blocked_contracts
        else ["manifest fixture contracts must pass"],
    )


def _check_status_contract(
    contract_name: str,
    fixture_pack: Mapping[str, Any],
) -> dict[str, Any]:
    blocked_checks = _blocked_fixture_check_names(fixture_pack)
    return _contract(
        contract_name,
        contract_type="fixture_check_status_contract",
        expected={"fixture_checks_pass": True, "blocked_check_count": 0},
        observed={
            "fixture_checks_pass": not blocked_checks,
            "blocked_check_count": len(blocked_checks),
            "blocked_check_names": blocked_checks,
        },
        blocking_reasons=[]
        if not blocked_checks
        else ["manifest fixture checks must pass"],
    )


def _blocked_fragment_contract(
    contract_name: str,
    observed_key: str,
    payload_findings: Sequence[str],
) -> dict[str, Any]:
    return _contract(
        contract_name,
        contract_type="fixture_payload_sanitization_contract",
        expected={observed_key: False, "blocked_fragment_hit_count": 0},
        observed={
            observed_key: bool(payload_findings),
            "blocked_fragment_hit_count": len(payload_findings),
        },
        blocking_reasons=[
            "fixture payloads must not include blocked fragments"
        ]
        if payload_findings
        else [],
    )


def _disabled_flag_contract(
    contract_name: str,
    flag_name: str,
    fixture_pack: Mapping[str, Any],
) -> dict[str, Any]:
    flag_is_false = _pack_flag_false(fixture_pack, flag_name)
    return _contract(
        contract_name,
        contract_type="validation_disabled_flag_contract",
        expected={flag_name: False},
        observed={flag_name: False if flag_is_false else True},
        blocking_reasons=[]
        if flag_is_false
        else [f"{flag_name} must remain false"],
    )


def _hash_present_check(fixture_pack: Mapping[str, Any]) -> dict[str, Any]:
    fixture_hash = _string_or_none(
        fixture_pack.get("deterministic_manifest_fixture_pack_hash")
    )
    return _check(
        "fixture_pack_hash_present_check",
        expected={"manifest_fixture_pack_hash_present": True},
        observed={"manifest_fixture_pack_hash_present": _is_sha256(fixture_hash)},
        blocking_reasons=[]
        if _is_sha256(fixture_hash)
        else ["manifest fixture pack hash must be sha256"],
    )


def _hash_stable_check(
    fixture_pack: Mapping[str, Any],
    fixture_pack_repeat: Mapping[str, Any],
) -> dict[str, Any]:
    fixture_hash = _string_or_none(
        fixture_pack.get("deterministic_manifest_fixture_pack_hash")
    )
    repeat_hash = _string_or_none(
        fixture_pack_repeat.get("deterministic_manifest_fixture_pack_hash")
    )
    return _check(
        "fixture_pack_hash_stable_check",
        expected={"manifest_fixture_pack_hash_stable": True},
        observed={"manifest_fixture_pack_hash_stable": fixture_hash == repeat_hash},
        blocking_reasons=[]
        if fixture_hash == repeat_hash
        else ["manifest fixture pack hash must be stable"],
    )


def _contract_status_check(
    check_name: str,
    fixture_pack: Mapping[str, Any],
) -> dict[str, Any]:
    blocked_contracts = _blocked_fixture_contract_names(fixture_pack)
    return _check(
        check_name,
        expected={"fixture_contracts_pass": True, "blocked_contract_count": 0},
        observed={
            "fixture_contracts_pass": not blocked_contracts,
            "blocked_contract_count": len(blocked_contracts),
            "blocked_contract_names": blocked_contracts,
        },
        blocking_reasons=[]
        if not blocked_contracts
        else ["manifest fixture contracts must pass"],
    )


def _fixture_check_status_check(
    check_name: str,
    fixture_pack: Mapping[str, Any],
) -> dict[str, Any]:
    blocked_checks = _blocked_fixture_check_names(fixture_pack)
    return _check(
        check_name,
        expected={"fixture_checks_pass": True, "blocked_check_count": 0},
        observed={
            "fixture_checks_pass": not blocked_checks,
            "blocked_check_count": len(blocked_checks),
            "blocked_check_names": blocked_checks,
        },
        blocking_reasons=[]
        if not blocked_checks
        else ["manifest fixture checks must pass"],
    )


def _payload_findings_check(
    check_name: str,
    payload_findings: Sequence[str],
) -> dict[str, Any]:
    return _check(
        check_name,
        expected={"blocked_fragment_hit_count": 0},
        observed={"blocked_fragment_hit_count": len(payload_findings)},
        blocking_reasons=[
            "fixture payloads must not include blocked fragments"
        ]
        if payload_findings
        else [],
    )


def _flag_check(
    check_name: str,
    flag_name: str,
    fixture_pack: Mapping[str, Any],
) -> dict[str, Any]:
    flag_is_false = _pack_flag_false(fixture_pack, flag_name)
    return _check(
        check_name,
        expected={flag_name: False},
        observed={flag_name: False if flag_is_false else True},
        blocking_reasons=[]
        if flag_is_false
        else [f"{flag_name} must remain false"],
    )


def _deterministic_hash_check(
    fixture_pack: Mapping[str, Any],
    fixture_pack_repeat: Mapping[str, Any],
    rows: Sequence[Mapping[str, Any]],
    contracts: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    rows_repeat = _build_manifest_validation_rows(
        fixture_pack_repeat,
        fixture_pack_repeat,
    )
    contracts_repeat = _build_manifest_validation_contracts(
        fixture_pack_repeat,
        fixture_pack_repeat,
        rows_repeat,
    )
    fixture_hash = _string_or_none(
        fixture_pack.get("deterministic_manifest_fixture_pack_hash")
    )
    repeat_hash = _string_or_none(
        fixture_pack_repeat.get("deterministic_manifest_fixture_pack_hash")
    )
    row_hash = _hash_json_value(list(rows))
    row_repeat_hash = _hash_json_value(rows_repeat)
    contract_hash = _hash_json_value(list(contracts))
    contract_repeat_hash = _hash_json_value(contracts_repeat)
    return _check(
        "deterministic_hash_check",
        expected={
            "fixture_pack_hash_stable": True,
            "row_hash_stable": True,
            "contract_hash_stable": True,
            "row_names_complete": True,
            "contract_names_complete": True,
        },
        observed={
            "fixture_pack_hash_stable": fixture_hash == repeat_hash,
            "fixture_pack_hash_present": _is_sha256(fixture_hash),
            "row_hash_stable": row_hash == row_repeat_hash,
            "row_hash_present": _is_sha256(row_hash),
            "contract_hash_stable": contract_hash == contract_repeat_hash,
            "contract_hash_present": _is_sha256(contract_hash),
            "row_names_complete": (
                _row_names(rows) == list(REQUIRED_MANIFEST_VALIDATION_ROW_NAMES)
            ),
            "contract_names_complete": (
                _contract_names(contracts)
                == list(REQUIRED_MANIFEST_VALIDATION_CONTRACT_NAMES)
            ),
        },
        blocking_reasons=_deduplicate(
            [
                *(
                    ["manifest fixture pack hash must be stable"]
                    if fixture_hash != repeat_hash
                    else []
                ),
                *(
                    ["manifest fixture pack hash must be sha256"]
                    if not _is_sha256(fixture_hash)
                    else []
                ),
                *(
                    ["manifest validation row hash must be stable"]
                    if row_hash != row_repeat_hash
                    else []
                ),
                *(
                    ["manifest validation row hash must be sha256"]
                    if not _is_sha256(row_hash)
                    else []
                ),
                *(
                    ["manifest validation contract hash must be stable"]
                    if contract_hash != contract_repeat_hash
                    else []
                ),
                *(
                    ["manifest validation contract hash must be sha256"]
                    if not _is_sha256(contract_hash)
                    else []
                ),
                *(
                    ["manifest validation row names must be complete"]
                    if _row_names(rows)
                    != list(REQUIRED_MANIFEST_VALIDATION_ROW_NAMES)
                    else []
                ),
                *(
                    ["manifest validation contract names must be complete"]
                    if _contract_names(contracts)
                    != list(REQUIRED_MANIFEST_VALIDATION_CONTRACT_NAMES)
                    else []
                ),
            ]
        ),
    )


def _unknown_row(name: str) -> dict[str, Any]:
    return _row(
        name,
        row_type="unknown_manifest_validation_row",
        source_fixture_refs=[],
        source_contract_refs=[],
        source_check_refs=[],
        expected={"known_row_name": True},
        observed={"known_row_name": False, "requested_row_name": name},
        validation_notes=[],
        blocking_reasons=[
            "execution adapter manifest validation row name is not recognized"
        ],
    )


def _unknown_contract(name: str) -> dict[str, Any]:
    return _contract(
        name,
        contract_type="unknown_contract",
        expected={"known_contract_name": True},
        observed={
            "known_contract_name": False,
            "requested_contract_name": name,
        },
        blocking_reasons=[
            "execution adapter manifest validation contract name is not recognized"
        ],
    )


def _unknown_check(name: str) -> dict[str, Any]:
    return _check(
        name,
        expected={"known_check_name": True},
        observed={"known_check_name": False, "requested_check_name": name},
        blocking_reasons=[
            "execution adapter manifest validation check name is not recognized"
        ],
    )


def _manifest_validation_matrix_summary(
    rows: Sequence[Mapping[str, Any]],
    contracts: Sequence[Mapping[str, Any]],
    checks: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    blocked_rows = _blocked_row_names(rows)
    blocked_contracts = _blocked_contract_names(contracts)
    blocked_checks = _blocked_check_names(checks)
    return _detached_json_value(
        {
            "row_count": len(rows),
            "row_pass_count": len(rows) - len(blocked_rows),
            "row_blocked_count": len(blocked_rows),
            "blocked_row_names": blocked_rows,
            "contract_count": len(contracts),
            "contract_pass_count": len(contracts) - len(blocked_contracts),
            "contract_blocked_count": len(blocked_contracts),
            "blocked_contract_names": blocked_contracts,
            "check_count": len(checks),
            "check_pass_count": len(checks) - len(blocked_checks),
            "check_blocked_count": len(blocked_checks),
            "blocked_check_names": blocked_checks,
            "manifest_validation_matrix_mode": MANIFEST_VALIDATION_MATRIX_MODE,
            "manifest_validation_matrix_stage": (
                EXECUTION_ADAPTER_MANIFEST_VALIDATION_MATRIX_STAGE
            ),
            "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
            **COMMON_DISABLED_FLAGS,
            "raw_fixture_events_included": False,
            "sensitive_names_included": False,
            "sensitive_values_included": False,
            "executable_command_included": False,
            "live_endpoint_included": False,
            "manifest_validation_matrix_summary_status": (
                "safe"
                if not blocked_rows and not blocked_contracts and not blocked_checks
                else "blocked"
            ),
        }
    )


def _fixture_pack_passes(fixture_pack: Mapping[str, Any]) -> bool:
    return (
        fixture_pack.get("manifest_fixture_pack_status") == "pass"
        and fixture_pack.get("version")
        == GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_VALIDATION_MATRIX_VERSION
        and _is_sha256(
            _string_or_none(
                fixture_pack.get("deterministic_manifest_fixture_pack_hash")
            )
        )
    )


def _fixture_pack_blocking_reasons(
    fixture_pack: Mapping[str, Any],
) -> list[str]:
    fixture_hash = _string_or_none(
        fixture_pack.get("deterministic_manifest_fixture_pack_hash")
    )
    return _deduplicate(
        [
            *(
                ["manifest fixture pack status must pass"]
                if fixture_pack.get("manifest_fixture_pack_status") != "pass"
                else []
            ),
            *(
                ["manifest fixture pack version must equal 5.5.0"]
                if fixture_pack.get("version")
                != GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_VALIDATION_MATRIX_VERSION
                else []
            ),
            *(
                ["manifest fixture pack hash must be sha256"]
                if not _is_sha256(fixture_hash)
                else []
            ),
        ]
    )


def _manifest_fixtures(fixture_pack: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    fixtures = fixture_pack.get("manifest_fixtures")
    if not isinstance(fixtures, list):
        return []
    return [fixture for fixture in fixtures if isinstance(fixture, Mapping)]


def _manifest_fixture_contracts(
    fixture_pack: Mapping[str, Any],
) -> list[Mapping[str, Any]]:
    contracts = fixture_pack.get("manifest_fixture_contracts")
    if not isinstance(contracts, list):
        return []
    return [contract for contract in contracts if isinstance(contract, Mapping)]


def _manifest_fixture_checks(
    fixture_pack: Mapping[str, Any],
) -> list[Mapping[str, Any]]:
    checks = fixture_pack.get("manifest_fixture_checks")
    if not isinstance(checks, list):
        return []
    return [check for check in checks if isinstance(check, Mapping)]


def _expected_fixture_names() -> list[str]:
    return [
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


def _fixture_names(fixture_pack: Mapping[str, Any]) -> list[str]:
    return [
        _string_or_none(fixture.get("fixture_name")) or ""
        for fixture in _manifest_fixtures(fixture_pack)
    ]


def _fixture_contract_names(fixture_pack: Mapping[str, Any]) -> list[str]:
    return [
        _string_or_none(contract.get("contract_name")) or ""
        for contract in _manifest_fixture_contracts(fixture_pack)
    ]


def _fixture_check_names(fixture_pack: Mapping[str, Any]) -> list[str]:
    return [
        _string_or_none(check.get("check_name")) or ""
        for check in _manifest_fixture_checks(fixture_pack)
    ]


def _missing_fixture_names(fixture_names: Sequence[str]) -> list[str]:
    return [name for name in _expected_fixture_names() if name not in fixture_names]


def _extra_fixture_names(fixture_names: Sequence[str]) -> list[str]:
    return [name for name in fixture_names if name not in _expected_fixture_names()]


def _fixture_by_name(
    fixture_pack: Mapping[str, Any],
    name: str,
) -> Mapping[str, Any] | None:
    for fixture in _manifest_fixtures(fixture_pack):
        if fixture.get("fixture_name") == name:
            return fixture
    return None


def _contract_by_name(
    fixture_pack: Mapping[str, Any],
    name: str,
) -> Mapping[str, Any] | None:
    for contract in _manifest_fixture_contracts(fixture_pack):
        if contract.get("contract_name") == name:
            return contract
    return None


def _check_by_name(
    fixture_pack: Mapping[str, Any],
    name: str,
) -> Mapping[str, Any] | None:
    for check in _manifest_fixture_checks(fixture_pack):
        if check.get("check_name") == name:
            return check
    return None


def _fixture_statuses(
    fixture_pack: Mapping[str, Any],
    names: Sequence[str],
) -> dict[str, str | None]:
    statuses: dict[str, str | None] = {}
    for name in names:
        fixture = _fixture_by_name(fixture_pack, name)
        statuses[name] = (
            _string_or_none(fixture.get("fixture_status"))
            if isinstance(fixture, Mapping)
            else None
        )
    return statuses


def _fixture_contract_statuses(
    fixture_pack: Mapping[str, Any],
    names: Sequence[str],
) -> dict[str, str | None]:
    statuses: dict[str, str | None] = {}
    for name in names:
        contract = _contract_by_name(fixture_pack, name)
        statuses[name] = (
            _string_or_none(contract.get("contract_status"))
            if isinstance(contract, Mapping)
            else None
        )
    return statuses


def _fixture_check_statuses(
    fixture_pack: Mapping[str, Any],
    names: Sequence[str],
) -> dict[str, str | None]:
    statuses: dict[str, str | None] = {}
    for name in names:
        check = _check_by_name(fixture_pack, name)
        statuses[name] = (
            _string_or_none(check.get("check_status"))
            if isinstance(check, Mapping)
            else None
        )
    return statuses


def _blocked_fixture_contract_names(
    fixture_pack: Mapping[str, Any],
) -> list[str]:
    return [
        _string_or_none(contract.get("contract_name")) or ""
        for contract in _manifest_fixture_contracts(fixture_pack)
        if contract.get("contract_status") != "pass"
    ]


def _blocked_fixture_check_names(
    fixture_pack: Mapping[str, Any],
) -> list[str]:
    return [
        _string_or_none(check.get("check_name")) or ""
        for check in _manifest_fixture_checks(fixture_pack)
        if check.get("check_status") != "pass"
    ]


def _row_names(rows: Sequence[Mapping[str, Any]]) -> list[str]:
    return [_string_or_none(row.get("row_name")) or "" for row in rows]


def _contract_names(contracts: Sequence[Mapping[str, Any]]) -> list[str]:
    return [
        _string_or_none(contract.get("contract_name")) or ""
        for contract in contracts
    ]


def _missing_row_names(row_names: Sequence[str]) -> list[str]:
    return [
        name
        for name in REQUIRED_MANIFEST_VALIDATION_ROW_NAMES
        if name not in row_names
    ]


def _extra_row_names(row_names: Sequence[str]) -> list[str]:
    return [
        name
        for name in row_names
        if name not in REQUIRED_MANIFEST_VALIDATION_ROW_NAMES
    ]


def _row_name_blocking_reasons(row_names: Sequence[str]) -> list[str]:
    return _deduplicate(
        [
            *(["manifest validation rows missing"] if _missing_row_names(row_names) else []),
            *(["unexpected manifest validation rows present"] if _extra_row_names(row_names) else []),
            *(
                ["manifest validation row order must be stable"]
                if list(row_names) != list(REQUIRED_MANIFEST_VALIDATION_ROW_NAMES)
                else []
            ),
        ]
    )


def _rows_pass(rows: Sequence[Mapping[str, Any]]) -> bool:
    return all(row.get("row_status") == "pass" for row in rows)


def _contracts_pass(contracts: Sequence[Mapping[str, Any]]) -> bool:
    return all(
        contract.get("contract_status") == "pass" for contract in contracts
    )


def _blocked_row_names(rows: Sequence[Mapping[str, Any]]) -> list[str]:
    return [
        _string_or_none(row.get("row_name")) or ""
        for row in rows
        if row.get("row_status") != "pass"
    ]


def _blocked_contract_names(
    contracts: Sequence[Mapping[str, Any]],
) -> list[str]:
    return [
        _string_or_none(contract.get("contract_name")) or ""
        for contract in contracts
        if contract.get("contract_status") != "pass"
    ]


def _blocked_check_names(checks: Sequence[Mapping[str, Any]]) -> list[str]:
    return [
        _string_or_none(check.get("check_name")) or ""
        for check in checks
        if check.get("check_status") != "pass"
    ]


def _pack_flag_false(fixture_pack: Mapping[str, Any], flag_name: str) -> bool:
    return _nested_key_false(fixture_pack, flag_name)


def _all_safety_flags_false(value: Any) -> bool:
    return all(_nested_key_false(value, key) for key in SAFETY_BOUNDARIES)


def _nested_key_false(value: Any, key_name: str) -> bool:
    if isinstance(value, Mapping):
        for key, nested_value in value.items():
            if key == key_name and nested_value is not False:
                return False
            if isinstance(nested_value, (Mapping, list)):
                if not _nested_key_false(nested_value, key_name):
                    return False
    elif isinstance(value, list):
        for item in value:
            if not _nested_key_false(item, key_name):
                return False
    return True


def _fixture_payload_findings(
    fixture_pack: Mapping[str, Any],
) -> list[str]:
    payloads = [
        fixture.get("fixture_payload")
        for fixture in _manifest_fixtures(fixture_pack)
    ]
    serialized_payloads = json.dumps(
        _detached_json_value(payloads),
        ensure_ascii=True,
        allow_nan=False,
        separators=(",", ":"),
        sort_keys=True,
    ).lower()
    return [
        fragment
        for fragment in _PAYLOAD_BLOCKED_FRAGMENTS
        if fragment.lower() in serialized_payloads
    ]


def _execution_adapter_manifest_validation_matrix_hash(
    matrix: Mapping[str, Any],
) -> str:
    hash_input = {
        field: matrix[field]
        for field in _MANIFEST_VALIDATION_MATRIX_HASH_FIELDS
    }
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


def _deduplicate(values: Sequence[str] | Any) -> list[str]:
    return list(dict.fromkeys(list(values)))


__all__ = [
    "EXECUTION_ADAPTER_MANIFEST_VALIDATION_MATRIX_STAGE",
    "GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_VALIDATION_MATRIX_HASH_ALGORITHM",
    "GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_VALIDATION_MATRIX_SCHEMA_VERSION",
    "GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_VALIDATION_MATRIX_TYPE",
    "GOVERNANCE_EXECUTION_ADAPTER_MANIFEST_VALIDATION_MATRIX_VERSION",
    "MANIFEST_VALIDATION_MATRIX_MODE",
    "SAFETY_BOUNDARIES",
    "STAR_COSMOS_ENTRY_STATUS",
    "build_governance_execution_adapter_manifest_validation_matrix",
    "get_governance_execution_adapter_manifest_validation_check",
    "get_governance_execution_adapter_manifest_validation_contract",
    "get_governance_execution_adapter_manifest_validation_row",
    "governance_execution_adapter_manifest_validation_matrix_to_json",
    "list_governance_execution_adapter_manifest_validation_check_names",
    "list_governance_execution_adapter_manifest_validation_contract_names",
    "list_governance_execution_adapter_manifest_validation_row_names",
]
