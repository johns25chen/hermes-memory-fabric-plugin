"""v2.6.0 governed memory approval-request envelope dry run."""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

from .governed_memory_proposal_review_gate_dry_run import (
    run_governed_memory_proposal_review_gate_dry_run,
)


GOVERNED_MEMORY_APPROVAL_REQUEST_DRY_RUN_VERSION = "2.6.0"

NO_WRITE_FLAGS = {
    "writes_memory": False,
    "writes_graph": False,
    "writes_operation_ledger": False,
    "writes_config": False,
    "writes_sqlite": False,
    "invokes_real_executor": False,
    "provider_tools": [],
}

NO_TOKEN_FLAGS = {
    "creates_real_memory_write_proposal": False,
    "creates_real_operation_ledger_entry": False,
    "issues_approval_token": False,
    "approval_token_issued": False,
    "approval_token_value": None,
    "creates_usable_token": False,
    "modifies_hermes_agent": False,
    "no_network_surface": True,
}


def build_governed_memory_approval_request_dry_run(proposal_path: str | Path) -> dict[str, Any]:
    """Build deterministic approval-request envelopes from v2.5 approve candidates."""

    review_gate = run_governed_memory_proposal_review_gate_dry_run(proposal_path)
    approve_candidates = list(review_gate.get("approve_candidates") or [])
    blocked_decisions = [
        decision
        for decision in review_gate.get("decisions") or []
        if decision.get("review_decision") != "approve_candidate"
    ]
    approval_requests = [_approval_request_for_decision(decision) for decision in approve_candidates]
    approval_request_status = (
        "ready"
        if review_gate.get("review_gate_status") == "ready"
        and len(approval_requests) == int(review_gate.get("approve_candidate_count") or 0)
        else "blocked"
    )

    result = {
        "version": GOVERNED_MEMORY_APPROVAL_REQUEST_DRY_RUN_VERSION,
        "approval_request_status": approval_request_status,
        "source_path": str(review_gate.get("source_path") or Path(proposal_path).expanduser().resolve()),
        "source_sha256": str(review_gate.get("source_sha256") or ""),
        "review_gate_version": str(review_gate.get("version") or ""),
        "review_gate_status": str(review_gate.get("review_gate_status") or "blocked"),
        "decision_count": int(review_gate.get("decision_count") or 0),
        "approve_candidate_count": int(review_gate.get("approve_candidate_count") or 0),
        "approval_request_count": len(approval_requests),
        "blocked_decision_count": len(blocked_decisions),
        "approval_requests": approval_requests,
        "blocked_decisions": blocked_decisions,
        **deepcopy(NO_WRITE_FLAGS),
        **deepcopy(NO_TOKEN_FLAGS),
        "safety_summary": _safety_summary(
            approval_request_status=approval_request_status,
            review_gate=review_gate,
            approval_requests=approval_requests,
            blocked_decisions=blocked_decisions,
        ),
    }
    return deepcopy(result)


def governed_memory_approval_request_to_json(result: Mapping[str, Any]) -> str:
    """Serialize a v2.6.0 governed memory approval-request dry-run report."""

    return json.dumps(dict(result), sort_keys=True, indent=2, ensure_ascii=True) + "\n"


def _approval_request_for_decision(decision: Mapping[str, Any]) -> dict[str, Any]:
    proposal_id = str(decision.get("proposal_id") or "")
    decision_id = str(decision.get("decision_id") or "")
    entry_key = str(decision.get("entry_key") or "")
    target_surface = str(decision.get("target_surface") or "")
    review_reason = str(decision.get("review_reason") or "")

    return {
        "approval_request_id": _approval_request_id(
            proposal_id=proposal_id,
            decision_id=decision_id,
            entry_key=entry_key,
            target_surface=target_surface,
            review_reason=review_reason,
        ),
        "decision_id": decision_id,
        "proposal_id": proposal_id,
        "entry_key": entry_key,
        "target_surface": target_surface,
        "review_reason": review_reason,
        "request_status": "pending_human_approval",
        "requested_action": "authorize_future_memory_write_plan_candidate",
        "writes_memory": False,
        "writes_graph": False,
        "writes_operation_ledger": False,
        "issues_approval_token": False,
        "approval_token_issued": False,
        "approval_token_value": None,
        "creates_usable_token": False,
        "invokes_real_executor": False,
        "provider_tools": [],
    }


def _approval_request_id(
    *,
    proposal_id: str,
    decision_id: str,
    entry_key: str,
    target_surface: str,
    review_reason: str,
) -> str:
    digest = hashlib.sha256(
        "\n".join(
            (
                GOVERNED_MEMORY_APPROVAL_REQUEST_DRY_RUN_VERSION,
                proposal_id,
                decision_id,
                entry_key,
                target_surface,
                review_reason,
            )
        ).encode("utf-8")
    ).hexdigest()[:24]
    return f"gmar-dry-run-{digest}"


def _safety_summary(
    *,
    approval_request_status: str,
    review_gate: Mapping[str, Any],
    approval_requests: list[dict[str, Any]],
    blocked_decisions: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "adapter": "governed_memory_approval_request_dry_run",
        "version": GOVERNED_MEMORY_APPROVAL_REQUEST_DRY_RUN_VERSION,
        "approval_request_status": approval_request_status,
        "dry_run_only": True,
        "consumes_review_gate_version": str(review_gate.get("version") or ""),
        "review_gate_status": str(review_gate.get("review_gate_status") or "blocked"),
        "local_file_parsing_only": True,
        "decision_count": int(review_gate.get("decision_count") or 0),
        "approve_candidate_count": int(review_gate.get("approve_candidate_count") or 0),
        "approval_request_count": len(approval_requests),
        "blocked_decision_count": len(blocked_decisions),
        "writes_memory": False,
        "writes_graph": False,
        "writes_operation_ledger": False,
        "writes_config": False,
        "writes_sqlite": False,
        "invokes_real_executor": False,
        "provider_tools": [],
        "creates_real_memory_write_proposal": False,
        "creates_real_operation_ledger_entry": False,
        "issues_approval_token": False,
        "approval_token_issued": False,
        "approval_token_value": None,
        "creates_usable_token": False,
        "modifies_hermes_agent": False,
        "no_network_surface": True,
    }


__all__ = [
    "GOVERNED_MEMORY_APPROVAL_REQUEST_DRY_RUN_VERSION",
    "build_governed_memory_approval_request_dry_run",
    "governed_memory_approval_request_to_json",
]
