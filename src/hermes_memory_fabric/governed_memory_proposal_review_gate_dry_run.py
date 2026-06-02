"""v2.5.0 governed memory proposal review-gate dry run."""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

from .governed_memory_proposal_pack_dry_run import (
    build_governed_memory_proposal_pack_dry_run,
)


GOVERNED_MEMORY_PROPOSAL_REVIEW_GATE_DRY_RUN_VERSION = "2.5.0"

APPROVABLE_TARGET_SURFACES = {
    "long_term_memory",
    "short_term_memory",
    "operation_ledger",
    "knowledge_surface",
}

KNOWN_TARGET_SURFACES = APPROVABLE_TARGET_SURFACES | {
    "rejected_do_not_persist",
    "risk_note",
}

KNOWN_STATUSES = {"proposed", "rejected", "risk_note"}

LOCKED_NON_DURABLE_REASONS = {
    "temporary_command_authorization",
    "api_key_or_secret",
    "raw_credentials",
    "docker_log_or_temp_path_or_pid",
    "one_off_temporary_state",
}

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


def run_governed_memory_proposal_review_gate_dry_run(proposal_path: str | Path) -> dict[str, Any]:
    """Classify a v2.4.0 proposal pack locally without executing any write path."""

    pack = build_governed_memory_proposal_pack_dry_run(proposal_path)
    entries = list(pack.get("entries") or [])
    decisions = [_decision_for_entry(entry) for entry in entries]
    deferred = [decision for decision in decisions if decision["review_decision"] == "defer_for_human_review"]
    approve_candidates = [
        decision for decision in decisions if decision["review_decision"] == "approve_candidate"
    ]
    reject_locked = [decision for decision in decisions if decision["review_decision"] == "reject_locked"]
    risk_note_only = [decision for decision in decisions if decision["review_decision"] == "risk_note_only"]
    review_gate_status = "blocked" if pack.get("pack_status") != "ready" or deferred else "ready"

    result = {
        "version": GOVERNED_MEMORY_PROPOSAL_REVIEW_GATE_DRY_RUN_VERSION,
        "review_gate_status": review_gate_status,
        "source_path": str(pack.get("source_path") or Path(proposal_path).expanduser().resolve().as_posix()),
        "source_sha256": str(pack.get("source_sha256") or ""),
        "pack_version": str(pack.get("version") or ""),
        "pack_status": str(pack.get("pack_status") or "blocked"),
        "entry_count": len(entries),
        "decision_count": len(decisions),
        "approve_candidate_count": len(approve_candidates),
        "reject_locked_count": len(reject_locked),
        "defer_for_human_review_count": len(deferred),
        "risk_note_only_count": len(risk_note_only),
        "decisions": decisions,
        "approve_candidates": approve_candidates,
        "reject_locked": reject_locked,
        "deferred": deferred,
        "risk_note_only": risk_note_only,
        **deepcopy(NO_WRITE_FLAGS),
        **deepcopy(NO_TOKEN_FLAGS),
        "safety_summary": _safety_summary(
            review_gate_status=review_gate_status,
            pack=pack,
            decisions=decisions,
            approve_candidates=approve_candidates,
            reject_locked=reject_locked,
            deferred=deferred,
            risk_note_only=risk_note_only,
        ),
    }
    return deepcopy(result)


def governed_memory_proposal_review_gate_to_json(result: Mapping[str, Any]) -> str:
    """Serialize a v2.5.0 governed memory proposal review-gate report deterministically."""

    return json.dumps(dict(result), sort_keys=True, indent=2, ensure_ascii=True) + "\n"


def _decision_for_entry(entry: Mapping[str, Any]) -> dict[str, Any]:
    source_status = str(entry.get("status") or "")
    source_target_surface = str(entry.get("target_surface") or "")
    entry_key = str(entry.get("entry_key") or "")
    proposal_id = str(entry.get("proposal_id") or "")
    must_not_become_durable_memory = bool(entry.get("must_not_become_durable_memory"))
    non_durable_reasons = [str(reason) for reason in entry.get("non_durable_reasons") or []]

    review_decision, review_reason = _classify_entry(
        source_status=source_status,
        source_target_surface=source_target_surface,
        must_not_become_durable_memory=must_not_become_durable_memory,
        non_durable_reasons=non_durable_reasons,
    )

    return {
        "decision_id": _decision_id(proposal_id, entry_key, source_status, source_target_surface),
        "proposal_id": proposal_id,
        "entry_key": entry_key,
        "source_status": source_status,
        "source_target_surface": source_target_surface,
        "review_decision": review_decision,
        "review_reason": review_reason,
        "target_surface": source_target_surface,
        "must_not_become_durable_memory": must_not_become_durable_memory,
        "non_durable_reasons": non_durable_reasons,
        "writes_memory": False,
        "writes_graph": False,
        "writes_operation_ledger": False,
        "issues_approval_token": False,
        "invokes_real_executor": False,
        "provider_tools": [],
    }


def _classify_entry(
    *,
    source_status: str,
    source_target_surface: str,
    must_not_become_durable_memory: bool,
    non_durable_reasons: list[str],
) -> tuple[str, str]:
    locked_reasons = sorted(set(non_durable_reasons).intersection(LOCKED_NON_DURABLE_REASONS))

    if source_status not in KNOWN_STATUSES:
        return "defer_for_human_review", "unknown_status_blocks_review_gate"
    if source_target_surface not in KNOWN_TARGET_SURFACES:
        return "defer_for_human_review", "unknown_target_surface_blocks_review_gate"
    if source_status == "risk_note":
        return "risk_note_only", "risk_note_is_observational_only"
    if source_status == "rejected":
        return "reject_locked", "source_pack_rejected_entry_is_locked"
    if must_not_become_durable_memory:
        return "reject_locked", "entry_marked_must_not_become_durable_memory"
    if locked_reasons:
        return "reject_locked", "entry_contains_locked_non_durable_reason"
    if source_target_surface in APPROVABLE_TARGET_SURFACES:
        return "approve_candidate", "proposed_entry_targets_governed_durable_surface"
    return "defer_for_human_review", "non_approvable_target_surface_requires_review"


def _decision_id(
    proposal_id: str,
    entry_key: str,
    source_status: str,
    source_target_surface: str,
) -> str:
    digest = hashlib.sha256(
        "\n".join(
            (
                GOVERNED_MEMORY_PROPOSAL_REVIEW_GATE_DRY_RUN_VERSION,
                proposal_id,
                entry_key,
                source_status,
                source_target_surface,
            )
        ).encode("utf-8")
    ).hexdigest()[:24]
    return f"gmprg-dry-run-{digest}"


def _safety_summary(
    *,
    review_gate_status: str,
    pack: Mapping[str, Any],
    decisions: list[dict[str, Any]],
    approve_candidates: list[dict[str, Any]],
    reject_locked: list[dict[str, Any]],
    deferred: list[dict[str, Any]],
    risk_note_only: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "adapter": "governed_memory_proposal_review_gate_dry_run",
        "version": GOVERNED_MEMORY_PROPOSAL_REVIEW_GATE_DRY_RUN_VERSION,
        "review_gate_status": review_gate_status,
        "dry_run_only": True,
        "consumes_pack_version": str(pack.get("version") or ""),
        "pack_status": str(pack.get("pack_status") or "blocked"),
        "local_file_parsing_only": True,
        "entry_count": len(decisions),
        "decision_count": len(decisions),
        "approve_candidate_count": len(approve_candidates),
        "reject_locked_count": len(reject_locked),
        "defer_for_human_review_count": len(deferred),
        "risk_note_only_count": len(risk_note_only),
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
    "GOVERNED_MEMORY_PROPOSAL_REVIEW_GATE_DRY_RUN_VERSION",
    "run_governed_memory_proposal_review_gate_dry_run",
    "governed_memory_proposal_review_gate_to_json",
]
