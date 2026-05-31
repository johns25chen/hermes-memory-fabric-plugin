"""v1.9 dry-run adapter from v1.8 review outcomes to token issuance drafts."""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from typing import Any, Mapping


MEMORY_APPROVAL_TOKEN_ISSUANCE_DRY_RUN_VERSION = "1.9.0"
SOURCE_REVIEW_GATE_VERSION = "1.8.0"
TOKEN_KIND = "approval_token_issuance_draft_candidate"
READY_NEXT_STEP = "manual_token_issuance_review_required_no_token_created"
LOCKED_NEXT_STEP = "repair_source_review_outcome_before_token_issuance_dry_run"

SOURCE_REQUIRED_KEYS = (
    "version",
    "dry_run",
    "review_gate_status",
    "review_outcome_id",
    "reviewer_decision",
    "required_next_step",
    "approval_token_issued",
    "approval_token_id",
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

SOURCE_FALSE_WRITE_FLAGS = (
    "approval_token_issued",
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

TOKEN_NO_WRITE_FLAGS = {
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


def run_memory_approval_token_issuance_dry_run(
    review_outcome: Mapping[str, Any],
    *,
    issuer: str = "manual-human-review",
    issuance_reason: str | None = None,
) -> dict[str, Any]:
    """Create a deterministic token issuance dry-run candidate from v1.8 output.

    The result is only a token draft candidate. It never creates a usable token,
    persists token state, creates proposals, appends ledgers, invokes executors,
    or writes memory.
    """

    source = deepcopy(dict(review_outcome)) if isinstance(review_outcome, Mapping) else {}
    clean_issuer = str(issuer)
    clean_reason = "" if issuance_reason is None else str(issuance_reason)
    validation = _validate_source_review_outcome(source)
    status = "ready" if validation["valid"] is True else "locked"
    required_next_step = READY_NEXT_STEP if status == "ready" else LOCKED_NEXT_STEP

    token_draft_id = _token_draft_id(
        issuer=clean_issuer,
        issuance_reason=clean_reason,
        source=source,
    )
    token_intent_id = _token_intent_id(
        token_draft_id=token_draft_id,
        source=source,
    )

    result = {
        "version": MEMORY_APPROVAL_TOKEN_ISSUANCE_DRY_RUN_VERSION,
        "dry_run": True,
        "token_issuance_status": status,
        "token_draft_id": token_draft_id,
        "token_intent_id": token_intent_id,
        "token_kind": TOKEN_KIND,
        "token_status": "draft_ready" if status == "ready" else "locked",
        "issuer": clean_issuer,
        "issuance_reason": clean_reason,
        "source_review_gate_version": source.get("version"),
        "source_review_gate_status": source.get("review_gate_status"),
        "source_review_outcome_id": source.get("review_outcome_id"),
        "source_reviewer_decision": source.get("reviewer_decision"),
        "source_required_next_step": source.get("required_next_step"),
        "required_next_step": required_next_step,
        **deepcopy(TOKEN_NO_WRITE_FLAGS),
        "safety_summary": _safety_summary(validation, status),
        "source_review_outcome_snapshot": source,
    }
    return deepcopy(result)


def memory_approval_token_issuance_dry_run(
    review_outcome: Mapping[str, Any],
    **kwargs: Any,
) -> dict[str, Any]:
    """Alias for the v1.9 approval-token issuance dry-run entry point."""

    return run_memory_approval_token_issuance_dry_run(review_outcome, **kwargs)


def approval_token_issuance_dry_run_to_json(result: Mapping[str, Any]) -> str:
    """Serialize a token issuance dry-run result deterministically."""

    return json.dumps(dict(result), sort_keys=True, indent=2, ensure_ascii=True) + "\n"


def _validate_source_review_outcome(source: Mapping[str, Any]) -> dict[str, Any]:
    missing = [key for key in SOURCE_REQUIRED_KEYS if key not in source]
    errors = [f"missing_{key}" for key in missing]

    if source.get("version") != SOURCE_REVIEW_GATE_VERSION:
        errors.append("source_review_gate_version_must_be_1.8.0")
    if source.get("dry_run") is not True:
        errors.append("source_review_outcome_dry_run_must_be_true")
    if source.get("review_gate_status") != "approved":
        errors.append("source_review_gate_status_must_be_approved")
    if source.get("reviewer_decision") != "approve":
        errors.append("source_reviewer_decision_must_be_approve")
    if source.get("required_next_step") != "manual_review_outcome_recorded_no_token_issued":
        errors.append("source_required_next_step_must_be_manual_review_outcome_recorded_no_token_issued")
    if source.get("approval_token_id") is not None:
        errors.append("source_approval_token_id_must_be_null")

    true_write_flags = [flag for flag in SOURCE_FALSE_WRITE_FLAGS if source.get(flag) is True]
    errors.extend(f"source_{flag}_must_be_false" for flag in true_write_flags)

    provider_tools = source.get("provider_tools")
    if provider_tools != []:
        errors.append("source_provider_tools_must_be_empty")

    return {
        "valid": not errors,
        "errors": _dedupe(errors),
        "missing_keys": missing,
        "true_write_flags": true_write_flags,
        "provider_tools": deepcopy(provider_tools),
    }


def _safety_summary(validation: Mapping[str, Any], status: str) -> dict[str, Any]:
    return {
        "adapter": "memory_approval_token_issuance_dry_run",
        "version": MEMORY_APPROVAL_TOKEN_ISSUANCE_DRY_RUN_VERSION,
        "dry_run_only": True,
        "token_issuance_status": status,
        "source_review_gate_required_version": SOURCE_REVIEW_GATE_VERSION,
        "source_review_outcome_valid": validation.get("valid") is True,
        "source_review_outcome_errors": list(validation.get("errors", [])),
        "source_missing_keys": list(validation.get("missing_keys", [])),
        "source_true_write_flags": list(validation.get("true_write_flags", [])),
        "source_provider_tools": deepcopy(validation.get("provider_tools")),
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


def _token_draft_id(
    *,
    issuer: str,
    issuance_reason: str,
    source: Mapping[str, Any],
) -> str:
    payload = {
        "version": MEMORY_APPROVAL_TOKEN_ISSUANCE_DRY_RUN_VERSION,
        "token_kind": TOKEN_KIND,
        "issuer": issuer,
        "issuance_reason": issuance_reason,
        "source_review_outcome_id": source.get("review_outcome_id"),
        "source_review_gate_status": source.get("review_gate_status"),
        "source_reviewer_decision": source.get("reviewer_decision"),
        "source_required_next_step": source.get("required_next_step"),
    }
    return "approval-token-issuance-draft-dry-run-" + _hash_payload(payload)


def _token_intent_id(
    *,
    token_draft_id: str,
    source: Mapping[str, Any],
) -> str:
    source_snapshot = source.get("source_approval_intent_snapshot")
    source_approval_intent_id = None
    if isinstance(source_snapshot, Mapping):
        source_approval_intent_id = source_snapshot.get("approval_intent_id")
    if source_approval_intent_id is None:
        source_approval_intent_id = source.get("source_approval_intent_id")

    payload = {
        "version": MEMORY_APPROVAL_TOKEN_ISSUANCE_DRY_RUN_VERSION,
        "token_draft_id": token_draft_id,
        "source_review_outcome_id": source.get("review_outcome_id"),
        "source_approval_intent_id": source_approval_intent_id,
    }
    return "approval-token-intent-dry-run-" + _hash_payload(payload)


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
    "MEMORY_APPROVAL_TOKEN_ISSUANCE_DRY_RUN_VERSION",
    "SOURCE_REVIEW_GATE_VERSION",
    "TOKEN_KIND",
    "SOURCE_REQUIRED_KEYS",
    "SOURCE_FALSE_WRITE_FLAGS",
    "TOKEN_NO_WRITE_FLAGS",
    "run_memory_approval_token_issuance_dry_run",
    "memory_approval_token_issuance_dry_run",
    "approval_token_issuance_dry_run_to_json",
]
