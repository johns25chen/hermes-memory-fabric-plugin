"""v1.5 dry-run adapter from v1.3.1 candidates to proposal previews."""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter
from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable, Mapping, TextIO

from hermes_memory_fabric.memory_block_review_queue import (
    create_review_queue_item,
    validate_review_queue_item,
)
from hermes_memory_fabric.memory_blocks import (
    create_memory_block_candidate,
    validate_memory_block_candidate,
)
from hermes_memory_fabric.memory_governance_submission_packet import (
    create_governance_submission_packet,
    validate_governance_submission_packet,
)
from hermes_memory_fabric.memory_human_review_outcome_gate import (
    create_human_review_outcome_candidate,
    validate_human_review_outcome_candidate,
)
from hermes_memory_fabric.memory_proposal_draft_builder import (
    create_memory_proposal_draft,
    validate_memory_proposal_draft,
)
from hermes_memory_fabric.memory_proposal_governance_gate import (
    create_governance_submission_candidate,
    validate_governance_submission_candidate,
)
from hermes_memory_fabric.memory_real_proposal_creation_plan import (
    create_real_proposal_creation_plan,
    validate_real_proposal_creation_plan,
)
from hermes_memory_fabric.memory_real_proposal_dry_run import (
    create_real_proposal_dry_run,
    validate_real_proposal_dry_run,
)
from hermes_memory_fabric.memory_review_decision_gate import (
    evaluate_review_queue_item,
    validate_review_decision_candidate,
)


MEMORY_CANDIDATE_PROPOSAL_DRY_RUN_VERSION = "1.5.0"
DEFAULT_PROJECT_ID = "hermes-memory-fabric"
DEFAULT_REVIEWER = "memory-candidate-proposal-dry-run-reviewer"
DEFAULT_AUTHOR = "memory-candidate-proposal-dry-run-author"
DEFAULT_PLANNER = "memory-candidate-proposal-dry-run-planner"
DEFAULT_OPERATOR = "memory-candidate-proposal-dry-run-operator"

REQUIRED_CANDIDATE_FIELDS = (
    "id",
    "content",
    "project_id",
    "entity_ids",
    "source",
    "source_id",
    "provenance",
    "risk_level",
    "governance",
    "created_at",
    "tags",
)
REQUIRED_GOVERNANCE_TRUE_FLAGS = ("dry_run", "read_only", "proposal_governed")
FORBIDDEN_GOVERNANCE_TRUE_FLAGS = (
    "would_write_memory",
    "would_modify_config",
    "would_write_graph",
    "writes_proposal_files",
    "writes_operation_ledger",
    "writes_token_files",
    "writes_approval_audit",
    "creates_real_proposals",
    "applies_proposals",
    "persists_approvals",
    "submits_to_governance",
    "converts_to_real_proposal",
    "invokes_real_token_write_executor",
    "implements_real_token_write_executor",
    "exposes_provider_tools",
)
DEFAULT_ALLOWED_RISK_LEVELS = ("low",)
REAL_WRITE_FLAGS = {
    "created_real_proposal": False,
    "writes_proposal_files": False,
    "writes_operation_ledger": False,
    "writes_memory": False,
    "writes_graph": False,
    "writes_config": False,
    "writes_sqlite": False,
    "writes_token_files": False,
    "writes_approval_audit": False,
    "applies_proposals": False,
}
REUSED_MODULES = (
    "memory_blocks",
    "memory_block_review_queue",
    "memory_review_decision_gate",
    "memory_proposal_draft_builder",
    "memory_proposal_governance_gate",
    "memory_governance_submission_packet",
    "memory_human_review_outcome_gate",
    "memory_real_proposal_creation_plan",
    "memory_real_proposal_dry_run",
)
INTENTIONALLY_NOT_CALLED = (
    "memory_fabric_bridge.create_memory_write_proposal",
    "memory_human_approval_token_*",
    "real_write_executor_*",
    "memory_real_proposal_write_lock_gate",
    "provider_tools",
)


def run_memory_candidate_proposal_dry_run(
    candidates: Iterable[Mapping[str, Any]],
    *,
    project_id: str = DEFAULT_PROJECT_ID,
    allowed_risk_levels: Iterable[str] = DEFAULT_ALLOWED_RISK_LEVELS,
    reviewer: str = DEFAULT_REVIEWER,
    author: str = DEFAULT_AUTHOR,
    planner: str = DEFAULT_PLANNER,
    operator: str = DEFAULT_OPERATOR,
) -> dict[str, Any]:
    """Convert v1.3.1 candidate dicts into read-only proposal-preview chains.

    This function never calls the real bridge proposal writer, token modules,
    executors, provider tools, network APIs, or model APIs. It only imports and
    invokes existing in-memory preview builders and validators.
    """

    allowed = _allowed_risk_levels(allowed_risk_levels)
    candidate_list = _candidate_list(candidates)
    proposal_previews: list[dict[str, Any]] = []
    rejected_candidates: list[dict[str, Any]] = []

    for index, raw_candidate in enumerate(candidate_list):
        candidate = deepcopy(dict(raw_candidate))
        validation = validate_candidate_for_proposal_dry_run(candidate, allowed_risk_levels=allowed)
        if validation["disposition"] != "accepted":
            rejected_candidates.append(_rejected_candidate_entry(index, candidate, validation))
            continue

        preview = _build_proposal_preview_chain(
            candidate,
            project_id=project_id,
            reviewer=reviewer,
            author=author,
            planner=planner,
            operator=operator,
        )
        chain_validation = _validate_preview_chain(preview)
        if chain_validation["valid"] is not True:
            rejected_candidates.append(
                _rejected_candidate_entry(
                    index,
                    candidate,
                    {
                        "disposition": "rejected",
                        "reasons": chain_validation["errors"],
                    },
                )
            )
            continue

        proposal_previews.append(preview)

    rejected_count = sum(1 for item in rejected_candidates if item["disposition"] == "rejected")
    locked_count = sum(1 for item in rejected_candidates if item["disposition"] == "locked")
    result = {
        "version": MEMORY_CANDIDATE_PROPOSAL_DRY_RUN_VERSION,
        "dry_run": True,
        **REAL_WRITE_FLAGS,
        "provider_tools": [],
        "accepted_count": len(proposal_previews),
        "rejected_count": rejected_count,
        "locked_count": locked_count,
        "proposal_previews": proposal_previews,
        "rejected_candidates": rejected_candidates,
        "safety_summary": _safety_summary(
            accepted_count=len(proposal_previews),
            rejected_candidates=rejected_candidates,
            allowed_risk_levels=allowed,
        ),
    }
    return deepcopy(result)


def memory_candidate_proposal_dry_run(
    candidates: Iterable[Mapping[str, Any]],
    **kwargs: Any,
) -> dict[str, Any]:
    """Alias for the v1.5 dry-run adapter entry point."""

    return run_memory_candidate_proposal_dry_run(candidates, **kwargs)


def validate_candidate_for_proposal_dry_run(
    candidate: Mapping[str, Any],
    *,
    allowed_risk_levels: Iterable[str] = DEFAULT_ALLOWED_RISK_LEVELS,
) -> dict[str, Any]:
    """Validate a raw v1.3.1 candidate before Memory Block adaptation."""

    errors: list[str] = []
    if not isinstance(candidate, Mapping):
        return {"disposition": "rejected", "reasons": ["candidate_must_be_mapping"]}

    missing = [field for field in REQUIRED_CANDIDATE_FIELDS if field not in candidate]
    errors.extend(f"missing_{field}" for field in missing)

    if not _clean_text(candidate.get("id")):
        errors.append("id_must_be_non_empty")
    if "content" in candidate and not _clean_text(candidate.get("content")):
        errors.append("content_must_be_non_empty")
    if not _clean_text(candidate.get("project_id")):
        errors.append("project_id_must_be_non_empty")
    if not _clean_text(candidate.get("source")):
        errors.append("source_must_be_non_empty")
    if not _clean_text(candidate.get("source_id")):
        errors.append("source_id_must_be_non_empty")
    if not isinstance(candidate.get("entity_ids"), (list, tuple)):
        errors.append("entity_ids_must_be_list")
    if not isinstance(candidate.get("tags"), (list, tuple)):
        errors.append("tags_must_be_list")
    if not isinstance(candidate.get("provenance"), Mapping):
        errors.append("provenance_must_be_mapping")

    governance = candidate.get("governance")
    errors.extend(_governance_errors(governance))
    if errors:
        return {"disposition": "rejected", "reasons": _dedupe(errors)}

    risk_level = _clean_text(candidate.get("risk_level")).lower()
    if risk_level not in _allowed_risk_levels(allowed_risk_levels):
        return {
            "disposition": "locked",
            "reasons": [f"risk_level_not_allowed:{risk_level or 'missing'}"],
        }

    return {"disposition": "accepted", "reasons": []}


def candidate_to_memory_block_candidate(
    candidate: Mapping[str, Any],
    *,
    project_id: str = DEFAULT_PROJECT_ID,
) -> dict[str, Any]:
    """Adapt one accepted v1.3.1 candidate into a Memory Block candidate."""

    source = deepcopy(dict(candidate))
    candidate_id = _clean_text(source.get("id"))
    source_id = _clean_text(source.get("source_id")) or candidate_id
    project_scope = _clean_text(source.get("project_id")) or _clean_text(project_id) or DEFAULT_PROJECT_ID
    metadata = {
        "adapter": "memory_candidate_proposal_dry_run",
        "adapter_version": MEMORY_CANDIDATE_PROPOSAL_DRY_RUN_VERSION,
        "source_candidate_schema": "memory_fabric_candidate_v1.3.1",
        "source_candidate_id": candidate_id,
        "candidate_id": candidate_id,
        "project_id": project_scope,
        "entity_ids": _string_list(source.get("entity_ids")),
        "tags": _string_list(source.get("tags")),
        "provenance": deepcopy(source.get("provenance")),
        "source": _clean_text(source.get("source")),
        "source_id": source_id,
        "source_event_id": source_id,
        "risk_level": _clean_text(source.get("risk_level")).lower(),
        "created_at": _clean_text(source.get("created_at")),
        "governance": deepcopy(dict(source.get("governance", {}))),
        "dry_run": True,
        "created_real_proposal": False,
        "writes_proposal_files": False,
        "writes_operation_ledger": False,
        "writes_memory": False,
        "writes_graph": False,
        "writes_config": False,
        "writes_sqlite": False,
        "writes_token_files": False,
        "writes_approval_audit": False,
    }
    return create_memory_block_candidate(
        "project_context",
        deepcopy(source.get("content")),
        project_scope=project_scope,
        source_fact_ids=[candidate_id],
        metadata=metadata,
    )


def dry_run_result_to_json(result: Mapping[str, Any]) -> str:
    """Serialize a dry-run result deterministically."""

    return json.dumps(dict(result), sort_keys=True, indent=2, ensure_ascii=True) + "\n"


def cli_main(
    argv: list[str] | None = None,
    *,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
) -> int:
    """Run the candidate proposal dry-run CLI."""

    out = stdout if stdout is not None else sys.stdout
    err = stderr if stderr is not None else sys.stderr
    parser = argparse.ArgumentParser(description="Dry-run v1.3.1 memory candidates into proposal previews.")
    parser.add_argument("--input", required=True, help="Path to candidate JSONL.")
    parser.add_argument("--output", help="Optional explicit output JSON path. Defaults to stdout.")
    parser.add_argument("--project-id", default=DEFAULT_PROJECT_ID)
    parser.add_argument("--print-summary", action="store_true")
    args = parser.parse_args(argv)

    try:
        candidates = _load_jsonl_candidates(Path(args.input))
    except OSError as exc:
        err.write(f"memory_candidate_proposal_dry_run_error={exc}\n")
        return 2

    result = run_memory_candidate_proposal_dry_run(candidates, project_id=args.project_id)
    rendered = dry_run_result_to_json(result)

    if args.output:
        output_path = Path(args.output)
        if _is_under_hermes_home(output_path):
            err.write("memory_candidate_proposal_dry_run_error=refusing_output_under_hermes_home\n")
            return 2
        output_path.write_text(rendered, encoding="utf-8")
    else:
        out.write(rendered)

    if args.print_summary:
        err.write("memory_candidate_proposal_dry_run_summary=")
        err.write(json.dumps(_cli_summary(result), sort_keys=True, separators=(",", ":")))
        err.write("\n")

    return 0


def _build_proposal_preview_chain(
    candidate: Mapping[str, Any],
    *,
    project_id: str,
    reviewer: str,
    author: str,
    planner: str,
    operator: str,
) -> dict[str, Any]:
    block = candidate_to_memory_block_candidate(candidate, project_id=project_id)
    queue_item = create_review_queue_item(
        block,
        reason="Low-risk v1.3.1 Memory Fabric candidate converted by v1.5 dry-run adapter.",
        reviewer=reviewer,
    )
    decision = evaluate_review_queue_item(queue_item, reviewer=reviewer)
    draft = create_memory_proposal_draft(decision, author=author)
    submission = create_governance_submission_candidate(draft, reviewer=reviewer)
    packet = create_governance_submission_packet(submission, reviewer=reviewer)
    outcome = create_human_review_outcome_candidate(packet, reviewer=reviewer)
    plan = create_real_proposal_creation_plan(outcome, planner=planner)
    dry_run = create_real_proposal_dry_run(plan, operator=operator)
    return {
        "candidate_id": _clean_text(candidate.get("id")),
        "project_id": _clean_text(candidate.get("project_id")),
        "risk_level": _clean_text(candidate.get("risk_level")).lower(),
        "adapter": {
            "version": MEMORY_CANDIDATE_PROPOSAL_DRY_RUN_VERSION,
            "source_schema": "memory_fabric_candidate_v1.3.1",
            "disposition": "accepted",
            "dry_run": True,
        },
        "memory_block_candidate": block,
        "review_queue_item": queue_item,
        "review_decision_candidate": decision,
        "proposal_draft": draft,
        "governance_submission_candidate": submission,
        "governance_submission_packet": packet,
        "human_review_outcome_candidate": outcome,
        "real_proposal_creation_plan": plan,
        "real_proposal_dry_run": dry_run,
        **REAL_WRITE_FLAGS,
        "provider_tools": [],
    }


def _validate_preview_chain(preview: Mapping[str, Any]) -> dict[str, Any]:
    validations = {
        "memory_block_candidate": validate_memory_block_candidate(preview.get("memory_block_candidate", {})),
        "review_queue_item": validate_review_queue_item(preview.get("review_queue_item", {})),
        "review_decision_candidate": validate_review_decision_candidate(
            preview.get("review_decision_candidate", {})
        ),
        "proposal_draft": validate_memory_proposal_draft(preview.get("proposal_draft", {})),
        "governance_submission_candidate": validate_governance_submission_candidate(
            preview.get("governance_submission_candidate", {})
        ),
        "governance_submission_packet": validate_governance_submission_packet(
            preview.get("governance_submission_packet", {})
        ),
        "human_review_outcome_candidate": validate_human_review_outcome_candidate(
            preview.get("human_review_outcome_candidate", {})
        ),
        "real_proposal_creation_plan": validate_real_proposal_creation_plan(
            preview.get("real_proposal_creation_plan", {})
        ),
        "real_proposal_dry_run": validate_real_proposal_dry_run(preview.get("real_proposal_dry_run", {})),
    }
    errors: list[str] = []
    for name, validation in validations.items():
        if validation.get("valid") is not True:
            errors.extend(f"{name}:{error}" for error in validation.get("errors", []))
    return {"valid": not errors, "errors": _dedupe(errors), "validations": validations}


def _governance_errors(governance: Any) -> list[str]:
    if not isinstance(governance, Mapping):
        return ["governance_must_be_mapping"]

    errors: list[str] = []
    for flag in REQUIRED_GOVERNANCE_TRUE_FLAGS:
        if governance.get(flag) is not True:
            errors.append(f"governance_{flag}_must_be_true")
    for flag in FORBIDDEN_GOVERNANCE_TRUE_FLAGS:
        if governance.get(flag) is True:
            errors.append(f"governance_{flag}_must_be_false")
    return errors


def _rejected_candidate_entry(
    index: int,
    candidate: Mapping[str, Any],
    validation: Mapping[str, Any],
) -> dict[str, Any]:
    disposition = _clean_text(validation.get("disposition")) or "rejected"
    return {
        "index": index,
        "candidate_id": _clean_text(candidate.get("id")),
        "project_id": _clean_text(candidate.get("project_id")),
        "risk_level": _clean_text(candidate.get("risk_level")).lower(),
        "disposition": disposition,
        "reasons": _string_list(validation.get("reasons")),
        **REAL_WRITE_FLAGS,
        "provider_tools": [],
    }


def _safety_summary(
    *,
    accepted_count: int,
    rejected_candidates: list[Mapping[str, Any]],
    allowed_risk_levels: tuple[str, ...],
) -> dict[str, Any]:
    rejected_reasons = Counter(
        reason
        for item in rejected_candidates
        if item.get("disposition") == "rejected"
        for reason in item.get("reasons", [])
    )
    locked_reasons = Counter(
        reason
        for item in rejected_candidates
        if item.get("disposition") == "locked"
        for reason in item.get("reasons", [])
    )
    return {
        "adapter": "memory_candidate_proposal_dry_run",
        "version": MEMORY_CANDIDATE_PROPOSAL_DRY_RUN_VERSION,
        "dry_run_only": True,
        "accepted_count": accepted_count,
        "rejected_count": sum(1 for item in rejected_candidates if item.get("disposition") == "rejected"),
        "locked_count": sum(1 for item in rejected_candidates if item.get("disposition") == "locked"),
        "accepted_risk_levels": list(allowed_risk_levels),
        "non_allowed_risk_disposition": "locked",
        "required_governance_true_flags": list(REQUIRED_GOVERNANCE_TRUE_FLAGS),
        "forbidden_governance_true_flags": list(FORBIDDEN_GOVERNANCE_TRUE_FLAGS),
        "rejected_reason_counts": _sorted_counter(rejected_reasons),
        "locked_reason_counts": _sorted_counter(locked_reasons),
        "reused_modules": list(REUSED_MODULES),
        "intentionally_not_called": list(INTENTIONALLY_NOT_CALLED),
        "create_memory_write_proposal_called": False,
        "human_approval_token_modules_called": False,
        "real_write_executor_modules_called": False,
        "provider_tools_exposed": False,
        "no_write_guarantees": {**REAL_WRITE_FLAGS, "provider_tools": []},
    }


def _cli_summary(result: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "version": result.get("version"),
        "dry_run": result.get("dry_run"),
        "accepted_count": result.get("accepted_count"),
        "rejected_count": result.get("rejected_count"),
        "locked_count": result.get("locked_count"),
        "created_real_proposal": result.get("created_real_proposal"),
        "writes_proposal_files": result.get("writes_proposal_files"),
        "writes_operation_ledger": result.get("writes_operation_ledger"),
        "writes_memory": result.get("writes_memory"),
        "writes_graph": result.get("writes_graph"),
        "writes_config": result.get("writes_config"),
        "writes_sqlite": result.get("writes_sqlite"),
        "writes_token_files": result.get("writes_token_files"),
        "writes_approval_audit": result.get("writes_approval_audit"),
        "applies_proposals": result.get("applies_proposals"),
        "provider_tools": result.get("provider_tools"),
    }


def _candidate_list(candidates: Iterable[Mapping[str, Any]]) -> list[Mapping[str, Any]]:
    if isinstance(candidates, (str, bytes, bytearray, Mapping)):
        return []
    try:
        return [deepcopy(dict(candidate)) for candidate in candidates if isinstance(candidate, Mapping)]
    except TypeError:
        return []


def _load_jsonl_candidates(path: Path) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(value, Mapping):
            candidates.append(deepcopy(dict(value)))
    return candidates


def _is_under_hermes_home(path: Path) -> bool:
    hermes_home = Path(os.environ.get("HERMES_HOME", str(Path.home() / ".hermes")))
    try:
        resolved_path = path.expanduser().resolve(strict=False)
        resolved_home = hermes_home.expanduser().resolve(strict=False)
        return resolved_path == resolved_home or resolved_home in resolved_path.parents
    except OSError:
        return False


def _allowed_risk_levels(value: Iterable[str]) -> tuple[str, ...]:
    allowed: list[str] = []
    seen: set[str] = set()
    values = (value,) if isinstance(value, str) else value
    for item in values:
        text = _clean_text(item).lower()
        if text and text not in seen:
            seen.add(text)
            allowed.append(text)
    return tuple(allowed or DEFAULT_ALLOWED_RISK_LEVELS)


def _string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, (str, bytes, bytearray)):
        values = [value]
    else:
        try:
            values = list(value)
        except TypeError:
            values = [value]
    return [str(item) for item in values if str(item)]


def _clean_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _dedupe(values: Iterable[str]) -> list[str]:
    deduped: list[str] = []
    seen: set[str] = set()
    for value in values:
        text = str(value)
        if text not in seen:
            seen.add(text)
            deduped.append(text)
    return deduped


def _sorted_counter(counter: Counter[str]) -> dict[str, int]:
    return {key: counter[key] for key in sorted(counter)}


__all__ = [
    "MEMORY_CANDIDATE_PROPOSAL_DRY_RUN_VERSION",
    "DEFAULT_PROJECT_ID",
    "REQUIRED_CANDIDATE_FIELDS",
    "REQUIRED_GOVERNANCE_TRUE_FLAGS",
    "FORBIDDEN_GOVERNANCE_TRUE_FLAGS",
    "REUSED_MODULES",
    "INTENTIONALLY_NOT_CALLED",
    "candidate_to_memory_block_candidate",
    "validate_candidate_for_proposal_dry_run",
    "run_memory_candidate_proposal_dry_run",
    "memory_candidate_proposal_dry_run",
    "dry_run_result_to_json",
    "cli_main",
]


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(cli_main())
