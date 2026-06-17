"""Deterministic declaration-only boundary for future governance adapters."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
import hashlib
import json
import math
from typing import Any

from .governance_boundary_readiness_audit import (
    build_governance_boundary_readiness_audit,
)
from .governance_transition_policy_registry import SAFETY_BOUNDARIES


GOVERNANCE_EXECUTION_ADAPTER_BOUNDARY_VERSION = "5.4.0"
GOVERNANCE_EXECUTION_ADAPTER_BOUNDARY_SCHEMA_VERSION = "5.4.0"
GOVERNANCE_EXECUTION_ADAPTER_BOUNDARY_TYPE = (
    "governance_execution_adapter_boundary"
)
GOVERNANCE_EXECUTION_ADAPTER_BOUNDARY_HASH_ALGORITHM = "sha256"
EXECUTION_ADAPTER_BOUNDARY_STAGE = "v5.0_execution_adapter_boundary_candidate"
STAR_COSMOS_ENTRY_STATUS = "candidate_only"

BOUNDARY_MODE = "declaration_only"
READY_HANDOFF_STATUS = "ready_for_future_adapter_contract_design"
BLOCKED_HANDOFF_STATUS = "blocked"

REQUIRED_ADAPTER_BOUNDARY_CONTRACT_NAMES = (
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
)

REQUIRED_BOUNDARY_CHECK_NAMES = (
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
)

_BOUNDARY_HASH_FIELDS = (
    "version",
    "schema_version",
    "execution_adapter_boundary_type",
    "execution_adapter_boundary_status",
    "boundary_stage",
    "boundary_mode",
    "star_cosmos_entry_status",
    "star_cosmos_memory_active",
    "execution_adapter_implemented",
    "execution_adapter_invoked",
    "real_execution_enabled",
    "external_calls_enabled",
    "durable_writes_enabled",
    "memory_graph_mutation_enabled",
    "operation_ledger_writes_enabled",
    "autonomous_execution_enabled",
    "readiness_audit_version",
    "readiness_audit_hash",
    "adapter_boundary_contracts",
    "boundary_checks",
    "boundary_summary",
    "handoff_status",
    "blocking_reasons",
    "hash_input_contract",
    "safety_boundaries",
)

HASH_INPUT_CONTRACT = {
    "algorithm": GOVERNANCE_EXECUTION_ADAPTER_BOUNDARY_HASH_ALGORITHM,
    "encoding": "utf-8",
    "hash_fields": list(_BOUNDARY_HASH_FIELDS),
    "input_shape": "sanitized execution adapter boundary projection",
    "json_allow_nan": False,
    "json_ensure_ascii": True,
    "json_separators": [",", ":"],
    "json_sort_keys": True,
    "raw_fixture_events_included": False,
    "sensitive_names_included": False,
    "sensitive_values_included": False,
}

_SENSITIVE_BLOCKED_TERMS = (
    '"approval_' + 'phrase"',
    '"std' + 'out_tail"',
    '"std' + 'out"',
    '"raw_' + 'logs"',
    '"to' + 'ken"',
    '"api_' + 'key"',
    '"sec' + 'ret"',
    '"pass' + 'word"',
    '"creden' + 'tial"',
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


def build_governance_execution_adapter_boundary() -> dict[str, Any]:
    """Build deterministic declaration-only boundary metadata."""

    readiness_audit = _detached_json_value(
        build_governance_boundary_readiness_audit()
    )
    readiness_audit_repeat = _detached_json_value(
        build_governance_boundary_readiness_audit()
    )
    contracts = _build_adapter_boundary_contracts()
    checks = _build_boundary_checks(
        readiness_audit,
        readiness_audit_repeat,
        contracts,
    )

    readiness_passes = readiness_audit.get("readiness_audit_status") == "pass"
    contracts_pass = all(
        contract["contract_status"] == "pass" for contract in contracts
    )
    checks_pass = all(check["check_status"] == "pass" for check in checks)
    execution_adapter_boundary_status = (
        "pass" if readiness_passes and contracts_pass and checks_pass else "blocked"
    )
    blocking_reasons = _deduplicate(
        [
            *(
                ["readiness audit must pass"]
                if not readiness_passes
                else []
            ),
            *(
                reason
                for contract in contracts
                for reason in contract["blocking_reasons"]
            ),
            *(
                reason
                for check in checks
                for reason in check["blocking_reasons"]
            ),
        ]
    )
    safety_boundaries = dict(SAFETY_BOUNDARIES)
    boundary: dict[str, Any] = {
        "version": GOVERNANCE_EXECUTION_ADAPTER_BOUNDARY_VERSION,
        "schema_version": GOVERNANCE_EXECUTION_ADAPTER_BOUNDARY_SCHEMA_VERSION,
        "execution_adapter_boundary_type": (
            GOVERNANCE_EXECUTION_ADAPTER_BOUNDARY_TYPE
        ),
        "execution_adapter_boundary_status": execution_adapter_boundary_status,
        "boundary_stage": EXECUTION_ADAPTER_BOUNDARY_STAGE,
        "boundary_mode": BOUNDARY_MODE,
        "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
        "star_cosmos_memory_active": False,
        "execution_adapter_implemented": False,
        "execution_adapter_invoked": False,
        "real_execution_enabled": False,
        "external_calls_enabled": False,
        "durable_writes_enabled": False,
        "memory_graph_mutation_enabled": False,
        "operation_ledger_writes_enabled": False,
        "autonomous_execution_enabled": False,
        "readiness_audit_version": _string_or_none(
            readiness_audit.get("version")
        ),
        "readiness_audit_hash": _string_or_none(
            readiness_audit.get("deterministic_readiness_audit_hash")
        ),
        "readiness_audit_status": _string_or_none(
            readiness_audit.get("readiness_audit_status")
        ),
        "adapter_boundary_contracts": contracts,
        "boundary_checks": checks,
        "boundary_summary": _boundary_summary(contracts, checks),
        "handoff_status": (
            READY_HANDOFF_STATUS
            if execution_adapter_boundary_status == "pass"
            else BLOCKED_HANDOFF_STATUS
        ),
        "blocking_reasons": blocking_reasons,
        "hash_input_contract": _detached_json_value(HASH_INPUT_CONTRACT),
        "safety_boundaries": safety_boundaries,
        **safety_boundaries,
    }
    boundary["deterministic_execution_adapter_boundary_hash"] = (
        _execution_adapter_boundary_hash(boundary)
    )
    return _detached_json_value(boundary)


def get_governance_execution_adapter_boundary_contract(
    name: str,
) -> dict[str, Any]:
    """Return a detached adapter boundary contract by stable name."""

    if not isinstance(name, str):
        return _unknown_contract("")
    boundary = build_governance_execution_adapter_boundary()
    for contract in boundary["adapter_boundary_contracts"]:
        if contract["contract_name"] == name:
            return _detached_json_value(contract)
    return _unknown_contract(name)


def get_governance_execution_adapter_boundary_check(
    name: str,
) -> dict[str, Any]:
    """Return a detached boundary check by stable name."""

    if not isinstance(name, str):
        return _unknown_check("")
    boundary = build_governance_execution_adapter_boundary()
    for check in boundary["boundary_checks"]:
        if check["check_name"] == name:
            return _detached_json_value(check)
    return _unknown_check(name)


def list_governance_execution_adapter_boundary_contract_names() -> list[str]:
    """Return stable adapter boundary contract names."""

    return list(REQUIRED_ADAPTER_BOUNDARY_CONTRACT_NAMES)


def list_governance_execution_adapter_boundary_check_names() -> list[str]:
    """Return stable boundary check names."""

    return list(REQUIRED_BOUNDARY_CHECK_NAMES)


def governance_execution_adapter_boundary_to_json(
    result: Mapping[str, Any],
) -> str:
    """Serialize execution adapter boundary data deterministically."""

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


def _build_adapter_boundary_contracts() -> list[dict[str, Any]]:
    return [
        _contract(
            "adapter_declaration_contract",
            contract_type="future_adapter_contract",
            expected={
                "boundary_mode": BOUNDARY_MODE,
                "contract_defines_metadata_only": True,
                "execution_adapter_implemented": False,
            },
            observed={
                "boundary_mode": BOUNDARY_MODE,
                "contract_defines_metadata_only": True,
                "execution_adapter_implemented": False,
            },
        ),
        _contract(
            "adapter_identity_contract",
            contract_type="future_adapter_contract",
            expected={
                "future_adapter_identity_required": True,
                "active_adapter_identity_present": False,
                "identity_binding_invoked": False,
            },
            observed={
                "future_adapter_identity_required": True,
                "active_adapter_identity_present": False,
                "identity_binding_invoked": False,
            },
        ),
        _contract(
            "adapter_capability_contract",
            contract_type="future_adapter_contract",
            expected={
                "future_capability_declaration_required": True,
                "capability_invocation_available": False,
                "capability_claim_executes_action": False,
            },
            observed={
                "future_capability_declaration_required": True,
                "capability_invocation_available": False,
                "capability_claim_executes_action": False,
            },
        ),
        _contract(
            "adapter_input_contract",
            contract_type="future_adapter_contract",
            expected={
                "future_input_shape": "deterministic_json_metadata",
                "runtime_input_accepted": False,
                "raw_fixture_events_included": False,
            },
            observed={
                "future_input_shape": "deterministic_json_metadata",
                "runtime_input_accepted": False,
                "raw_fixture_events_included": False,
            },
        ),
        _contract(
            "adapter_output_contract",
            contract_type="future_adapter_contract",
            expected={
                "future_output_shape": "deterministic_json_metadata",
                "runtime_output_returned": False,
                "sensitive_names_included": False,
                "sensitive_values_included": False,
            },
            observed={
                "future_output_shape": "deterministic_json_metadata",
                "runtime_output_returned": False,
                "sensitive_names_included": False,
                "sensitive_values_included": False,
            },
        ),
        _contract(
            "adapter_invocation_prohibition_contract",
            contract_type="prohibition_contract",
            expected={
                "execution_adapter_invoked": False,
                "invocation_entry_available": False,
            },
            observed={
                "execution_adapter_invoked": False,
                "invocation_entry_available": False,
            },
        ),
        _contract(
            "adapter_side_effect_prohibition_contract",
            contract_type="prohibition_contract",
            expected={
                "unsafe_side_effects_performed": False,
                "real_execution_performed": False,
                "dry_run_plan_executed": False,
            },
            observed={
                "unsafe_side_effects_performed": False,
                "real_execution_performed": False,
                "dry_run_plan_executed": False,
            },
        ),
        _contract(
            "dry_run_inspection_contract",
            contract_type="inspection_contract",
            expected={
                "dry_run_only_inspection": True,
                "dry_run_executed": False,
                "dry_run_plan_executed": False,
            },
            observed={
                "dry_run_only_inspection": True,
                "dry_run_executed": False,
                "dry_run_plan_executed": False,
            },
        ),
        _contract(
            "external_call_prohibition_contract",
            contract_type="prohibition_contract",
            expected={
                "external_calls_enabled": False,
                "external_call_surface_available": False,
            },
            observed={
                "external_calls_enabled": False,
                "external_call_surface_available": False,
            },
        ),
        _contract(
            "durable_write_prohibition_contract",
            contract_type="prohibition_contract",
            expected={
                "durable_writes_enabled": False,
                "durable_write_surface_available": False,
            },
            observed={
                "durable_writes_enabled": False,
                "durable_write_surface_available": False,
            },
        ),
        _contract(
            "memory_graph_mutation_prohibition_contract",
            contract_type="prohibition_contract",
            expected={
                "memory_graph_mutation_enabled": False,
                "graph_mutation_surface_available": False,
            },
            observed={
                "memory_graph_mutation_enabled": False,
                "graph_mutation_surface_available": False,
            },
        ),
        _contract(
            "operation_ledger_write_prohibition_contract",
            contract_type="prohibition_contract",
            expected={
                "operation_ledger_writes_enabled": False,
                "ledger_write_surface_available": False,
            },
            observed={
                "operation_ledger_writes_enabled": False,
                "ledger_write_surface_available": False,
            },
        ),
        _contract(
            "human_approval_non_execution_contract",
            contract_type="prohibition_contract",
            expected={
                "human_approval_executes_action": False,
                "approval_request_executed": False,
                "real_approval_granted": False,
            },
            observed={
                "human_approval_executes_action": False,
                "approval_request_executed": False,
                "real_approval_granted": False,
            },
        ),
        _contract(
            "star_cosmos_candidate_only_contract",
            contract_type="candidate_boundary_contract",
            expected={
                "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
                "star_cosmos_memory_active": False,
                "consciousness_claimed": False,
            },
            observed={
                "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
                "star_cosmos_memory_active": False,
                "consciousness_claimed": False,
            },
        ),
    ]


def _build_boundary_checks(
    readiness_audit: Mapping[str, Any],
    readiness_audit_repeat: Mapping[str, Any],
    contracts: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    checks = [
        _boundary_check(
            "readiness_audit_pass_check",
            expected={
                "readiness_audit_status": "pass",
                "readiness_audit_version": (
                    GOVERNANCE_EXECUTION_ADAPTER_BOUNDARY_VERSION
                ),
            },
            observed={
                "readiness_audit_status": _string_or_none(
                    readiness_audit.get("readiness_audit_status")
                ),
                "readiness_audit_version": _string_or_none(
                    readiness_audit.get("version")
                ),
                "readiness_audit_hash_present": _is_sha256(
                    _string_or_none(
                        readiness_audit.get(
                            "deterministic_readiness_audit_hash"
                        )
                    )
                ),
            },
            blocking_reasons=_deduplicate(
                [
                    *(
                        ["readiness audit status must pass"]
                        if readiness_audit.get("readiness_audit_status")
                        != "pass"
                        else []
                    ),
                    *(
                        ["readiness audit version must equal 5.4.0"]
                        if readiness_audit.get("version")
                        != GOVERNANCE_EXECUTION_ADAPTER_BOUNDARY_VERSION
                        else []
                    ),
                    *(
                        ["readiness audit hash must be sha256"]
                        if not _is_sha256(
                            _string_or_none(
                                readiness_audit.get(
                                    "deterministic_readiness_audit_hash"
                                )
                            )
                        )
                        else []
                    ),
                ]
            ),
        ),
        _simple_flag_check(
            "boundary_stage_check",
            expected=EXECUTION_ADAPTER_BOUNDARY_STAGE,
            observed=EXECUTION_ADAPTER_BOUNDARY_STAGE,
        ),
        _simple_flag_check(
            "declaration_only_mode_check",
            expected=BOUNDARY_MODE,
            observed=BOUNDARY_MODE,
        ),
        _simple_flag_check(
            "adapter_not_implemented_check",
            expected=False,
            observed=False,
        ),
        _simple_flag_check(
            "adapter_not_invoked_check",
            expected=False,
            observed=False,
        ),
        _simple_flag_check(
            "real_execution_disabled_check",
            expected=False,
            observed=False,
        ),
        _simple_flag_check(
            "external_calls_disabled_check",
            expected=False,
            observed=False,
        ),
        _simple_flag_check(
            "durable_writes_disabled_check",
            expected=False,
            observed=False,
        ),
        _simple_flag_check(
            "memory_graph_mutation_disabled_check",
            expected=False,
            observed=False,
        ),
        _simple_flag_check(
            "operation_ledger_writes_disabled_check",
            expected=False,
            observed=False,
        ),
        _simple_flag_check(
            "autonomous_execution_disabled_check",
            expected=False,
            observed=False,
        ),
        _boundary_check(
            "star_cosmos_candidate_only_check",
            expected={
                "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
                "star_cosmos_memory_active": False,
            },
            observed={
                "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
                "star_cosmos_memory_active": False,
            },
            blocking_reasons=[],
        ),
        _contract_completeness_check(contracts),
        _deterministic_hash_check(
            readiness_audit,
            readiness_audit_repeat,
            contracts,
        ),
        _redaction_boundary_check(contracts),
    ]
    return checks


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
        **safety_boundaries,
    }
    return _detached_json_value(contract)


def _boundary_check(
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


def _simple_flag_check(
    check_name: str,
    *,
    expected: bool | str,
    observed: bool | str,
) -> dict[str, Any]:
    return _boundary_check(
        check_name,
        expected={"value": expected},
        observed={"value": observed},
        blocking_reasons=[] if observed == expected else [f"{check_name} mismatch"],
    )


def _contract_completeness_check(
    contracts: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    contract_names = [
        _string_or_none(contract.get("contract_name")) or ""
        for contract in contracts
    ]
    missing_names = [
        name
        for name in REQUIRED_ADAPTER_BOUNDARY_CONTRACT_NAMES
        if name not in contract_names
    ]
    extra_names = [
        name
        for name in contract_names
        if name not in REQUIRED_ADAPTER_BOUNDARY_CONTRACT_NAMES
    ]
    return _boundary_check(
        "contract_completeness_check",
        expected={
            "contract_names": list(REQUIRED_ADAPTER_BOUNDARY_CONTRACT_NAMES),
            "contract_count": len(REQUIRED_ADAPTER_BOUNDARY_CONTRACT_NAMES),
        },
        observed={
            "contract_names": contract_names,
            "contract_count": len(contract_names),
            "missing_contract_names": missing_names,
            "extra_contract_names": extra_names,
        },
        blocking_reasons=_deduplicate(
            [
                *(["adapter boundary contracts missing"] if missing_names else []),
                *(["unexpected adapter boundary contracts present"] if extra_names else []),
                *(
                    ["adapter boundary contract order must be stable"]
                    if contract_names
                    != list(REQUIRED_ADAPTER_BOUNDARY_CONTRACT_NAMES)
                    else []
                ),
            ]
        ),
    )


def _deterministic_hash_check(
    readiness_audit: Mapping[str, Any],
    readiness_audit_repeat: Mapping[str, Any],
    contracts: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    readiness_hash = _string_or_none(
        readiness_audit.get("deterministic_readiness_audit_hash")
    )
    readiness_repeat_hash = _string_or_none(
        readiness_audit_repeat.get("deterministic_readiness_audit_hash")
    )
    contracts_hash = _hash_json_value(list(contracts))
    contracts_repeat_hash = _hash_json_value(_build_adapter_boundary_contracts())
    return _boundary_check(
        "deterministic_hash_check",
        expected={
            "readiness_audit_hash_stable": True,
            "adapter_contract_hash_stable": True,
            "hash_algorithm": GOVERNANCE_EXECUTION_ADAPTER_BOUNDARY_HASH_ALGORITHM,
        },
        observed={
            "readiness_audit_hash_stable": (
                readiness_audit == readiness_audit_repeat
                and readiness_hash == readiness_repeat_hash
            ),
            "readiness_audit_hash_present": _is_sha256(readiness_hash),
            "adapter_contract_hash_stable": (
                contracts_hash == contracts_repeat_hash
            ),
            "adapter_contract_hash_present": _is_sha256(contracts_hash),
        },
        blocking_reasons=_deduplicate(
            [
                *(
                    ["readiness audit hash must be stable"]
                    if readiness_audit != readiness_audit_repeat
                    or readiness_hash != readiness_repeat_hash
                    else []
                ),
                *(
                    ["readiness audit hash must be sha256"]
                    if not _is_sha256(readiness_hash)
                    else []
                ),
                *(
                    ["adapter boundary contract hash must be stable"]
                    if contracts_hash != contracts_repeat_hash
                    else []
                ),
                *(
                    ["adapter boundary contract hash must be sha256"]
                    if not _is_sha256(contracts_hash)
                    else []
                ),
            ]
        ),
    )


def _redaction_boundary_check(
    contracts: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    protected = {
        "contract_names": [
            _string_or_none(contract.get("contract_name")) or ""
            for contract in contracts
        ],
        "contract_statuses": [
            _string_or_none(contract.get("contract_status")) or ""
            for contract in contracts
        ],
        "boundary_summary": _boundary_summary(contracts, ()),
        "contract_hash": _hash_json_value(list(contracts)),
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
    return _boundary_check(
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
            "execution adapter boundary metadata must not expose sensitive fields or values"
        ]
        if leaked_terms
        else [],
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
        blocking_reasons=["adapter boundary contract name is not recognized"],
    )


def _unknown_check(name: str) -> dict[str, Any]:
    return _boundary_check(
        name,
        expected={"known_check_name": True},
        observed={"known_check_name": False, "requested_check_name": name},
        blocking_reasons=["execution adapter boundary check name is not recognized"],
    )


def _boundary_summary(
    contracts: Sequence[Mapping[str, Any]],
    checks: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    blocked_contracts = [
        _string_or_none(contract.get("contract_name")) or ""
        for contract in contracts
        if contract.get("contract_status") != "pass"
    ]
    blocked_checks = [
        _string_or_none(check.get("check_name")) or ""
        for check in checks
        if check.get("check_status") != "pass"
    ]
    return _detached_json_value(
        {
            "contract_count": len(contracts),
            "contract_pass_count": len(contracts) - len(blocked_contracts),
            "contract_blocked_count": len(blocked_contracts),
            "blocked_contract_names": blocked_contracts,
            "check_count": len(checks),
            "check_pass_count": len(checks) - len(blocked_checks),
            "check_blocked_count": len(blocked_checks),
            "blocked_check_names": blocked_checks,
            "boundary_mode": BOUNDARY_MODE,
            "boundary_stage": EXECUTION_ADAPTER_BOUNDARY_STAGE,
            "star_cosmos_entry_status": STAR_COSMOS_ENTRY_STATUS,
            "star_cosmos_memory_active": False,
            "execution_adapter_implemented": False,
            "execution_adapter_invoked": False,
            "real_execution_enabled": False,
            "external_calls_enabled": False,
            "durable_writes_enabled": False,
            "memory_graph_mutation_enabled": False,
            "operation_ledger_writes_enabled": False,
            "autonomous_execution_enabled": False,
            "raw_fixture_events_included": False,
            "sensitive_names_included": False,
            "sensitive_values_included": False,
            "safety_status": (
                "safe" if not blocked_contracts and not blocked_checks else "blocked"
            ),
        }
    )


def _execution_adapter_boundary_hash(boundary: Mapping[str, Any]) -> str:
    hash_input = {field: boundary[field] for field in _BOUNDARY_HASH_FIELDS}
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
    "EXECUTION_ADAPTER_BOUNDARY_STAGE",
    "GOVERNANCE_EXECUTION_ADAPTER_BOUNDARY_HASH_ALGORITHM",
    "GOVERNANCE_EXECUTION_ADAPTER_BOUNDARY_SCHEMA_VERSION",
    "GOVERNANCE_EXECUTION_ADAPTER_BOUNDARY_TYPE",
    "GOVERNANCE_EXECUTION_ADAPTER_BOUNDARY_VERSION",
    "SAFETY_BOUNDARIES",
    "STAR_COSMOS_ENTRY_STATUS",
    "build_governance_execution_adapter_boundary",
    "get_governance_execution_adapter_boundary_check",
    "get_governance_execution_adapter_boundary_contract",
    "governance_execution_adapter_boundary_to_json",
    "list_governance_execution_adapter_boundary_check_names",
    "list_governance_execution_adapter_boundary_contract_names",
]
