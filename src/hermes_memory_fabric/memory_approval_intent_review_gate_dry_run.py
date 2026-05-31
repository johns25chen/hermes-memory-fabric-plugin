"""v1.8 dry-run review gate for v1.7 approval intent candidates."""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from typing import Any, Mapping


MEMORY_APPROVAL_INTENT_REVIEW_GATE_DRY_RUN_VERSION = "1.8.0"
SOURCE_APPROVAL_INTENT_VERSION = "1.7.0"
REVIEW_OUTCOME_KIND = "approval_intent_review_outcome_candidate"
SUPPORTED_REVIEWER_DECISIONS = ("approve", "request_changes", "reject")

SOURCE_REQUIRED_KEYS = (
    "version",
    "dry_run",
    "approval_intent_status",
    "approval_intent_id",
    "source_preview_version",
    "source_accepted_count",
    "source_locked_count",
    "source_rejected_count",
    "human_review_required",
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

REVIEW_NO_WRITE_FLAGS = {
    "approval_token_issued": False,
    "approval_token_id": None,
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

REQUIRED_NEXT_STEPS = {
    "approved": "manual_review_outcome_recorded_no_token_issued",
    "changes_requested": "return_to_approval_intent_source_for_revision",
    "rejected": "stop_no_token_no_write",
    "locked": "repair_source_approval_intent_or_review_decision",
}


def run_memory_approval_intent_review_gate_dry_run(
    approval_intent: Mapping[str, Any],
    reviewer_decision: str,
    reviewer_reason: str | None = None,
) -> dict[str, Any]:
    """Create a deterministic review outcome candidate from a v1.7 intent.

    The result is a review outcome candidate only. It never issues approval
    tokens, creates proposals, appends ledgers, invokes executors, or writes
    memory.
    """

    source = deepcopy(dict(approval_intent)) if isinstance(approval_intent, Mapping) else {}
    reason = "" if reviewer_reason is None else str(reviewer_reason)
    validation = _validate_source_approval_intent(source, reviewer_decision)
    status = _review_gate_status(validation, reviewer_decision)

    result = {
        "version": MEMORY_APPROVAL_INTENT_REVIEW_GATE_DRY_RUN_VERSION,
        "dry_run": True,
        "review_gate_status": status,
        "review_outcome_id": _review_outcome_id(
            source=source,
            reviewer_decision=reviewer_decision,
            reviewer_reason=reason,
        ),
        "review_outcome_kind": REVIEW_OUTCOME_KIND,
        "review_outcome_status": status,
        "reviewer_decision": reviewer_decision,
        "reviewer_reason": reason,
        "source_approval_intent_version": source.get("version"),
        "source_approval_intent_status": source.get("approval_intent_status"),
        "source_approval_intent_id": source.get("approval_intent_id"),
        "source_human_review_required": source.get("human_review_required"),
        "required_next_step": REQUIRED_NEXT_STEPS[status],
        **deepcopy(REVIEW_NO_WRITE_FLAGS),
        "safety_summary": _safety_summary(validation, status),
        "source_approval_intent_snapshot": source,
    }
    return deepcopy(result)


def memory_approval_intent_review_gate_dry_run(
    approval_intent: Mapping[str, Any],
    reviewer_decision: str,
    reviewer_reason: str | None = None,
) -> dict[str, Any]:
    """Alias for the v1.8 approval-intent review-gate dry-run entry point."""

    return run_memory_approval_intent_review_gate_dry_run(
        approval_intent,
        reviewer_decision,
        reviewer_reason,
    )


def approval_intent_review_gate_dry_run_to_json(result: Mapping[str, Any]) -> str:
    """Serialize a review-gate dry-run result deterministically."""

    return json.dumps(dict(result), sort_keys=True, indent=2, ensure_ascii=True) + "\n"


def _validate_source_approval_intent(
    source: Mapping[str, Any],
    reviewer_decision: str,
) -> dict[str, Any]:
    missing = [key for key in SOURCE_REQUIRED_KEYS if key not in source]
    errors = [f"missing_{key}" for key in missing]

    if source.get("version") != SOURCE_APPROVAL_INTENT_VERSION:
        errors.append("source_approval_intent_version_must_be_1.7.0")
    if source.get("dry_run") is not True:
        errors.append("source_approval_intent_dry_run_must_be_true")
    if source.get("approval_intent_status") != "ready":
        errors.append("source_approval_intent_status_must_be_ready")
    if source.get("human_review_required") is not True:
        errors.append("source_human_review_required_must_be_true")
    if source.get("approval_token_id") is not None:
        errors.append("source_approval_token_id_must_be_null")

    true_write_flags = [flag for flag in SOURCE_FALSE_WRITE_FLAGS if source.get(flag) is True]
    errors.extend(f"source_{flag}_must_be_false" for flag in true_write_flags)

    provider_tools = source.get("provider_tools")
    if provider_tools != []:
        errors.append("source_provider_tools_must_be_empty")

    if reviewer_decision not in SUPPORTED_REVIEWER_DECISIONS:
        errors.append("reviewer_decision_must_be_supported")

    return {
        "valid": not errors,
        "errors": _dedupe(errors),
        "missing_keys": missing,
        "true_write_flags": true_write_flags,
        "provider_tools": deepcopy(provider_tools),
        "reviewer_decision_supported": reviewer_decision in SUPPORTED_REVIEWER_DECISIONS,
    }


def _review_gate_status(validation: Mapping[str, Any], reviewer_decision: str) -> str:
    if validation.get("valid") is not True:
        return "locked"
    if reviewer_decision == "approve":
        return "approved"
    if reviewer_decision == "request_changes":
        return "changes_requested"
    if reviewer_decision == "reject":
        return "rejected"
    return "locked"


def _safety_summary(validation: Mapping[str, Any], status: str) -> dict[str, Any]:
    return {
        "adapter": "memory_approval_intent_review_gate_dry_run",
        "version": MEMORY_APPROVAL_INTENT_REVIEW_GATE_DRY_RUN_VERSION,
        "dry_run_only": True,
        "review_gate_status": status,
        "source_approval_intent_required_version": SOURCE_APPROVAL_INTENT_VERSION,
        "source_approval_intent_valid": validation.get("valid") is True,
        "source_approval_intent_errors": list(validation.get("errors", [])),
        "source_missing_keys": list(validation.get("missing_keys", [])),
        "source_true_write_flags": list(validation.get("true_write_flags", [])),
        "source_provider_tools": deepcopy(validation.get("provider_tools")),
        "reviewer_decision_supported": validation.get("reviewer_decision_supported") is True,
        "approval_token_issued": False,
        "approval_token_id": None,
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
        "create_memory_write_proposal_called": False,
        "approval_tokens_created": False,
        "operation_ledger_appended": False,
        "memory_written": False,
        "executor_invoked": False,
    }


def _review_outcome_id(
    *,
    source: Mapping[str, Any],
    reviewer_decision: str,
    reviewer_reason: str,
) -> str:
    payload = {
        "version": MEMORY_APPROVAL_INTENT_REVIEW_GATE_DRY_RUN_VERSION,
        "review_outcome_kind": REVIEW_OUTCOME_KIND,
        "reviewer_decision": reviewer_decision,
        "reviewer_reason": reviewer_reason,
        "source_approval_intent_id": source.get("approval_intent_id"),
        "source_approval_intent_status": source.get("approval_intent_status"),
        "source_preview_version": source.get("source_preview_version"),
        "source_accepted_count": source.get("source_accepted_count"),
        "source_locked_count": source.get("source_locked_count"),
        "source_rejected_count": source.get("source_rejected_count"),
    }
    rendered = json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return "approval-intent-review-outcome-dry-run-" + hashlib.sha256(
        rendered.encode("utf-8")
    ).hexdigest()[:32]


def _dedupe(values: list[str]) -> list[str]:
    deduped: list[str] = []
    seen: set[str] = set()
    for value in values:
        if value not in seen:
            seen.add(value)
            deduped.append(value)
    return deduped


__all__ = [
    "MEMORY_APPROVAL_INTENT_REVIEW_GATE_DRY_RUN_VERSION",
    "SOURCE_APPROVAL_INTENT_VERSION",
    "REVIEW_OUTCOME_KIND",
    "SUPPORTED_REVIEWER_DECISIONS",
    "SOURCE_REQUIRED_KEYS",
    "SOURCE_FALSE_WRITE_FLAGS",
    "REVIEW_NO_WRITE_FLAGS",
    "run_memory_approval_intent_review_gate_dry_run",
    "memory_approval_intent_review_gate_dry_run",
    "approval_intent_review_gate_dry_run_to_json",
]
