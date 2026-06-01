"""v2.0 dry-run authority boundary contract for future token issuance."""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from typing import Any, Mapping, Sequence


MEMORY_TOKEN_AUTHORITY_BOUNDARY_CONTRACT_DRY_RUN_VERSION = "2.0.0"
SOURCE_TOKEN_ISSUANCE_VERSION = "1.9.0"
AUTHORITY_CONTRACT_KIND = "token_authority_boundary_contract_candidate"
READY_NEXT_STEP = "manual_authority_contract_review_required_no_token_created"
LOCKED_NEXT_STEP = "repair_source_token_issuance_or_authority_boundary_before_real_token"
DEFAULT_AUTHORITY_SCOPE = ("memory_proposal_apply_preview_only",)

ALLOWED_FUTURE_AUTHORITY_ACTIONS = (
    "define_token_scope",
    "define_token_expiry",
    "define_token_revocation",
    "define_token_audit_requirements",
    "define_executor_boundary",
    "define_ledger_boundary",
)

FORBIDDEN_FUTURE_AUTHORITY_ACTIONS = (
    "issue_real_approval_token",
    "create_token_value",
    "write_token_file",
    "append_operation_ledger",
    "invoke_real_executor",
    "apply_memory_proposal",
    "write_memory",
    "write_graph",
    "write_config",
    "write_sqlite",
    "write_approval_audit",
    "expose_provider_tools",
)

SOURCE_REQUIRED_KEYS = (
    "version",
    "dry_run",
    "token_issuance_status",
    "token_draft_id",
    "token_intent_id",
    "required_next_step",
    "approval_token_issued",
    "approval_token_id",
    "approval_token_value",
    "creates_usable_token",
    "creates_real_proposal",
    "writes_proposal_files",
    "writes_operation_ledger",
    "writes_memory",
    "writes_graph",
    "writes_config",
    "writes_sqlite",
    "writes_token_files",
    "writes_approval_audit",
    "invokes_real_executor",
    "applies_proposals",
    "provider_tools",
    "safety_summary",
)

SOURCE_FALSE_FLAGS = (
    "approval_token_issued",
    "creates_usable_token",
    "creates_real_proposal",
    "writes_proposal_files",
    "writes_operation_ledger",
    "writes_memory",
    "writes_graph",
    "writes_config",
    "writes_sqlite",
    "writes_token_files",
    "writes_approval_audit",
    "invokes_real_executor",
    "applies_proposals",
)

NO_TOKEN_NO_WRITE_FLAGS = {
    "approval_token_issued": False,
    "approval_token_id": None,
    "approval_token_value": None,
    "creates_usable_token": False,
    "creates_real_proposal": False,
    "writes_proposal_files": False,
    "writes_operation_ledger": False,
    "writes_memory": False,
    "writes_graph": False,
    "writes_config": False,
    "writes_sqlite": False,
    "writes_token_files": False,
    "writes_approval_audit": False,
    "invokes_real_executor": False,
    "applies_proposals": False,
    "provider_tools": [],
}


def run_memory_token_authority_boundary_contract_dry_run(
    token_issuance_candidate: Mapping[str, Any],
    *,
    authority_scope: Sequence[str] | None = None,
    expiry_seconds: int = 900,
    revocation_required: bool = True,
    audit_required: bool = True,
) -> dict[str, Any]:
    """Create a deterministic authority boundary contract candidate.

    This is a declarative dry run only. It does not issue, sign, persist, audit,
    or execute tokens, proposals, memory writes, ledger appends, or provider
    tools.
    """

    source = deepcopy(dict(token_issuance_candidate)) if isinstance(token_issuance_candidate, Mapping) else {}
    clean_scope = list(DEFAULT_AUTHORITY_SCOPE if authority_scope is None else authority_scope)
    ledger_required = True
    executor_boundary_required = True
    validation = _validate(source, clean_scope, expiry_seconds, revocation_required, audit_required)
    status = "ready" if validation["valid"] is True else "locked"
    required_next_step = READY_NEXT_STEP if status == "ready" else LOCKED_NEXT_STEP

    contract_id = _authority_contract_id(
        source=source,
        authority_scope=clean_scope,
        expiry_seconds=expiry_seconds,
        revocation_required=revocation_required,
        audit_required=audit_required,
        ledger_required=ledger_required,
        executor_boundary_required=executor_boundary_required,
    )

    result = {
        "version": MEMORY_TOKEN_AUTHORITY_BOUNDARY_CONTRACT_DRY_RUN_VERSION,
        "dry_run": True,
        "authority_contract_status": status,
        "authority_contract_id": contract_id,
        "authority_contract_kind": AUTHORITY_CONTRACT_KIND,
        "authority_contract_status_reason": _status_reason(validation, status),
        "source_token_issuance_version": source.get("version"),
        "source_token_issuance_status": source.get("token_issuance_status"),
        "source_token_draft_id": source.get("token_draft_id"),
        "source_token_intent_id": source.get("token_intent_id"),
        "source_required_next_step": source.get("required_next_step"),
        "authority_scope": clean_scope,
        "expiry_seconds": expiry_seconds,
        "revocation_required": revocation_required,
        "audit_required": audit_required,
        "ledger_required": ledger_required,
        "executor_boundary_required": executor_boundary_required,
        "allowed_future_authority_actions": list(ALLOWED_FUTURE_AUTHORITY_ACTIONS),
        "forbidden_future_authority_actions": list(FORBIDDEN_FUTURE_AUTHORITY_ACTIONS),
        "required_next_step": required_next_step,
        **deepcopy(NO_TOKEN_NO_WRITE_FLAGS),
        "safety_summary": _safety_summary(validation, status),
        "source_token_issuance_snapshot": source,
    }
    return deepcopy(result)


def memory_token_authority_boundary_contract_dry_run(
    token_issuance_candidate: Mapping[str, Any],
    **kwargs: Any,
) -> dict[str, Any]:
    """Alias for the v2.0 token authority boundary contract dry-run."""

    return run_memory_token_authority_boundary_contract_dry_run(
        token_issuance_candidate,
        **kwargs,
    )


def token_authority_boundary_contract_dry_run_to_json(result: Mapping[str, Any]) -> str:
    """Serialize a v2.0 authority boundary contract report deterministically."""

    return json.dumps(dict(result), sort_keys=True, indent=2, ensure_ascii=True) + "\n"


def _validate(
    source: Mapping[str, Any],
    authority_scope: Sequence[Any],
    expiry_seconds: Any,
    revocation_required: Any,
    audit_required: Any,
) -> dict[str, Any]:
    missing = [key for key in SOURCE_REQUIRED_KEYS if key not in source]
    errors = [f"missing_{key}" for key in missing]

    if source.get("version") != SOURCE_TOKEN_ISSUANCE_VERSION:
        errors.append("source_token_issuance_version_must_be_1.9.0")
    if source.get("dry_run") is not True:
        errors.append("source_token_issuance_dry_run_must_be_true")
    if source.get("token_issuance_status") != "ready":
        errors.append("source_token_issuance_status_must_be_ready")
    if source.get("required_next_step") != "manual_token_issuance_review_required_no_token_created":
        errors.append(
            "source_required_next_step_must_be_manual_token_issuance_review_required_no_token_created"
        )
    if source.get("approval_token_id") is not None:
        errors.append("source_approval_token_id_must_be_null")
    if source.get("approval_token_value") is not None:
        errors.append("source_approval_token_value_must_be_null")

    unsafe_false_flags = [flag for flag in SOURCE_FALSE_FLAGS if source.get(flag) is not False]
    errors.extend(f"source_{flag}_must_be_false" for flag in unsafe_false_flags)

    provider_tools = source.get("provider_tools")
    if provider_tools != []:
        errors.append("source_provider_tools_must_be_empty")

    invalid_scope_values = [
        value for value in authority_scope if not isinstance(value, str) or not value.strip()
    ]
    if not isinstance(authority_scope, list) or not authority_scope:
        errors.append("authority_scope_must_be_non_empty_list")
    if invalid_scope_values:
        errors.append("authority_scope_values_must_be_non_empty_strings")
    if not isinstance(expiry_seconds, int) or isinstance(expiry_seconds, bool) or expiry_seconds <= 0:
        errors.append("expiry_seconds_must_be_positive_int")
    if revocation_required is not True:
        errors.append("revocation_required_must_be_true")
    if audit_required is not True:
        errors.append("audit_required_must_be_true")

    return {
        "valid": not errors,
        "errors": _dedupe(errors),
        "missing_keys": missing,
        "source_unsafe_false_flags": unsafe_false_flags,
        "source_provider_tools": deepcopy(provider_tools),
        "invalid_authority_scope_values": deepcopy(invalid_scope_values),
    }


def _safety_summary(validation: Mapping[str, Any], status: str) -> dict[str, Any]:
    return {
        "adapter": "memory_token_authority_boundary_contract_dry_run",
        "version": MEMORY_TOKEN_AUTHORITY_BOUNDARY_CONTRACT_DRY_RUN_VERSION,
        "dry_run_only": True,
        "authority_contract_status": status,
        "source_token_issuance_required_version": SOURCE_TOKEN_ISSUANCE_VERSION,
        "source_token_issuance_valid": validation.get("valid") is True,
        "source_token_issuance_errors": list(validation.get("errors", [])),
        "source_missing_keys": list(validation.get("missing_keys", [])),
        "source_unsafe_false_flags": list(validation.get("source_unsafe_false_flags", [])),
        "source_provider_tools": deepcopy(validation.get("source_provider_tools")),
        "invalid_authority_scope_values": deepcopy(
            validation.get("invalid_authority_scope_values", [])
        ),
        "approval_token_issued": False,
        "approval_token_id": None,
        "approval_token_value": None,
        "creates_usable_token": False,
        "creates_real_proposal": False,
        "writes_proposal_files": False,
        "writes_operation_ledger": False,
        "writes_memory": False,
        "writes_graph": False,
        "writes_config": False,
        "writes_sqlite": False,
        "writes_token_files": False,
        "writes_approval_audit": False,
        "invokes_real_executor": False,
        "applies_proposals": False,
        "provider_tools": [],
        "token_strings_created": False,
        "token_files_created": False,
        "proposal_files_created": False,
        "operation_ledger_appended": False,
        "memory_written": False,
        "executor_invoked": False,
    }


def _status_reason(validation: Mapping[str, Any], status: str) -> str:
    if status == "ready":
        return "source_token_issuance_ready_authority_boundary_valid"
    errors = list(validation.get("errors", []))
    return "locked:" + ",".join(errors) if errors else "locked:unknown_validation_error"


def _authority_contract_id(
    *,
    source: Mapping[str, Any],
    authority_scope: Sequence[str],
    expiry_seconds: int,
    revocation_required: bool,
    audit_required: bool,
    ledger_required: bool,
    executor_boundary_required: bool,
) -> str:
    payload = {
        "version": MEMORY_TOKEN_AUTHORITY_BOUNDARY_CONTRACT_DRY_RUN_VERSION,
        "authority_contract_kind": AUTHORITY_CONTRACT_KIND,
        "source_token_draft_id": source.get("token_draft_id"),
        "source_token_intent_id": source.get("token_intent_id"),
        "source_token_issuance_status": source.get("token_issuance_status"),
        "source_required_next_step": source.get("required_next_step"),
        "authority_scope": list(authority_scope),
        "expiry_seconds": expiry_seconds,
        "revocation_required": revocation_required,
        "audit_required": audit_required,
        "ledger_required": ledger_required,
        "executor_boundary_required": executor_boundary_required,
    }
    return "token-authority-boundary-contract-dry-run-" + _hash_payload(payload)


def _hash_payload(payload: Mapping[str, Any]) -> str:
    rendered = json.dumps(dict(payload), sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(rendered.encode("utf-8")).hexdigest()[:32]


def _dedupe(values: list[str]) -> list[str]:
    deduped: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value not in seen:
            seen.add(value)
            deduped.append(value)
    return deduped


__all__ = [
    "MEMORY_TOKEN_AUTHORITY_BOUNDARY_CONTRACT_DRY_RUN_VERSION",
    "SOURCE_TOKEN_ISSUANCE_VERSION",
    "AUTHORITY_CONTRACT_KIND",
    "READY_NEXT_STEP",
    "LOCKED_NEXT_STEP",
    "DEFAULT_AUTHORITY_SCOPE",
    "ALLOWED_FUTURE_AUTHORITY_ACTIONS",
    "FORBIDDEN_FUTURE_AUTHORITY_ACTIONS",
    "SOURCE_REQUIRED_KEYS",
    "SOURCE_FALSE_FLAGS",
    "NO_TOKEN_NO_WRITE_FLAGS",
    "run_memory_token_authority_boundary_contract_dry_run",
    "memory_token_authority_boundary_contract_dry_run",
    "token_authority_boundary_contract_dry_run_to_json",
]
