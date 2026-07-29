"""Bounded, in-memory governed-memory learning slice.

The public runtime in this module composes existing candidate builders through
an explicit human-review outcome and stops.  It never applies, persists, or
continues a recommendation.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from hermes_memory_fabric.memory_block_review_queue import (
    create_review_queue_item,
    validate_review_queue_item,
)
from hermes_memory_fabric.memory_blocks import validate_memory_block_candidate
from hermes_memory_fabric.memory_candidate_proposal_dry_run import (
    candidate_to_memory_block_candidate,
    validate_candidate_for_proposal_dry_run,
)
from hermes_memory_fabric.memory_governance_submission_packet import (
    create_governance_submission_packet,
    validate_governance_submission_packet,
)
from hermes_memory_fabric.memory_human_review_outcome_gate import (
    SUPPORTED_HUMAN_REVIEW_OUTCOMES,
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
from hermes_memory_fabric.memory_review_decision_gate import (
    evaluate_review_queue_item,
    validate_review_decision_candidate,
)


GOVERNED_MEMORY_LEARNING_SLICE_VERSION = "0.1"
ALLOWED_INPUT_CLASSIFICATIONS = ("SYNTHETIC", "NON_SENSITIVE")
TERMINAL_ARTIFACT = "human_review_outcome_candidate"

_RUNTIME_SURFACE = "governed_memory_learning_slice"
_NO_WRITE_GUARANTEES = {
    "writes_memory": False,
    "writes_graph": False,
    "writes_sqlite": False,
    "writes_proposal_files": False,
    "writes_operation_ledger": False,
    "writes_approval_audit": False,
    "writes_token_files": False,
    "writes_config": False,
    "writes_cache": False,
    "creates_real_proposal": False,
    "creates_operation_event": False,
    "applies_proposals": False,
    "persists_approvals": False,
    "adopts_memory": False,
    "executes_actions": False,
    "provider_tools": [],
}


class GovernedMemoryLearningSliceError(Exception):
    """Deterministic fail-closed error with content-free rendering."""

    def __init__(self, code: str, stage: str, reasons: tuple[str, ...] | list[str] = ()) -> None:
        self.code = str(code)
        self.stage = str(stage)
        self.reasons = tuple(str(reason) for reason in reasons)
        rendered_reasons = ",".join(self.reasons) if self.reasons else "none"
        super().__init__(
            f"governed_memory_learning_slice_error:"
            f"code={self.code};stage={self.stage};reasons={rendered_reasons}"
        )


def run_governed_memory_learning_slice(
    candidate: Mapping[str, Any],
    *,
    project_id: str,
    reviewer: str,
    outcome: str,
    rationale: str,
    input_classification: str,
) -> dict[str, Any]:
    """Build and validate the bounded learning slice without side effects."""

    if not isinstance(candidate, Mapping):
        _fail("candidate_must_be_mapping", "input_boundary")

    candidate_snapshot = deepcopy(dict(candidate))
    if not _non_blank(project_id):
        _fail("project_id_required", "input_boundary")

    candidate_project_id = candidate_snapshot.get("project_id")
    if not _non_blank(candidate_project_id):
        _fail("candidate_project_id_required", "input_boundary")
    if candidate_project_id != project_id:
        _fail("project_id_mismatch", "input_boundary")

    if not _non_blank(reviewer):
        _fail("reviewer_required", "input_boundary")
    if outcome is None or not _non_blank(outcome):
        _fail("outcome_required", "input_boundary")
    if outcome not in SUPPORTED_HUMAN_REVIEW_OUTCOMES:
        _fail("unsupported_human_review_outcome", "input_boundary")
    if not _non_blank(rationale):
        _fail("rationale_required", "input_boundary")
    if input_classification not in ALLOWED_INPUT_CLASSIFICATIONS:
        _fail("unsupported_input_classification", "input_boundary")

    provenance = candidate_snapshot.get("provenance")
    if not isinstance(provenance, Mapping) or not provenance:
        _fail("declared_provenance_required", "input_boundary")

    candidate_validation = deepcopy(
        validate_candidate_for_proposal_dry_run(candidate_snapshot)
    )
    if candidate_validation.get("disposition") != "accepted":
        _fail(
            "candidate_not_accepted",
            "candidate",
            candidate_validation.get("reasons", ()),
        )

    memory_block_candidate = candidate_to_memory_block_candidate(
        candidate_snapshot,
        project_id=project_id,
    )
    memory_block_validation = _validate_intermediate(
        "memory_block_candidate",
        validate_memory_block_candidate(memory_block_candidate),
    )

    review_queue_item = create_review_queue_item(
        memory_block_candidate,
        reason="Accepted bounded learning-slice candidate requires explicit review.",
        reviewer=reviewer,
    )
    review_queue_validation = _validate_intermediate(
        "review_queue_item",
        validate_review_queue_item(review_queue_item),
    )

    review_decision_candidate = evaluate_review_queue_item(
        review_queue_item,
        reviewer=reviewer,
    )
    review_decision_validation = _validate_intermediate(
        "review_decision_candidate",
        validate_review_decision_candidate(review_decision_candidate),
    )

    proposal_draft = create_memory_proposal_draft(
        review_decision_candidate,
        author=reviewer,
    )
    proposal_draft_validation = _validate_intermediate(
        "proposal_draft",
        validate_memory_proposal_draft(proposal_draft),
    )

    governance_submission_candidate = create_governance_submission_candidate(
        proposal_draft,
        reviewer=reviewer,
    )
    governance_submission_validation = _validate_intermediate(
        "governance_submission_candidate",
        validate_governance_submission_candidate(governance_submission_candidate),
    )

    governance_submission_packet = create_governance_submission_packet(
        governance_submission_candidate,
        reviewer=reviewer,
    )
    governance_packet_validation = _validate_intermediate(
        "governance_submission_packet",
        validate_governance_submission_packet(governance_submission_packet),
    )

    human_review_outcome_candidate = create_human_review_outcome_candidate(
        governance_submission_packet,
        reviewer=reviewer,
        outcome=outcome,
        rationale=rationale,
    )
    human_outcome_validation = _validate_intermediate(
        "human_review_outcome_candidate",
        validate_human_review_outcome_candidate(human_review_outcome_candidate),
    )

    result = {
        "version": GOVERNED_MEMORY_LEARNING_SLICE_VERSION,
        "runtime_surface": _RUNTIME_SURFACE,
        "mode": "implementation_to_learn",
        "status": "complete_non_applied_human_decision",
        "terminal_artifact": TERMINAL_ARTIFACT,
        "boundary_reached": True,
        "continuation_authorized": False,
        "project_id": project_id,
        "input_classification": input_classification,
        "reviewer": reviewer,
        "outcome": outcome,
        "rationale": rationale,
        "declared_source": deepcopy(candidate_snapshot.get("source")),
        "declared_source_id": deepcopy(candidate_snapshot.get("source_id")),
        "declared_provenance": deepcopy(provenance),
        "candidate_snapshot": deepcopy(candidate_snapshot),
        "candidate_validation": deepcopy(candidate_validation),
        "memory_block_candidate": deepcopy(memory_block_candidate),
        "review_queue_item": deepcopy(review_queue_item),
        "review_decision_candidate": deepcopy(review_decision_candidate),
        "proposal_draft": deepcopy(proposal_draft),
        "governance_submission_candidate": deepcopy(governance_submission_candidate),
        "governance_submission_packet": deepcopy(governance_submission_packet),
        "human_review_outcome_candidate": deepcopy(human_review_outcome_candidate),
        "validations": {
            "candidate": deepcopy(candidate_validation),
            "memory_block_candidate": memory_block_validation,
            "review_queue_item": review_queue_validation,
            "review_decision_candidate": review_decision_validation,
            "proposal_draft": proposal_draft_validation,
            "governance_submission_candidate": governance_submission_validation,
            "governance_submission_packet": governance_packet_validation,
            "human_review_outcome_candidate": human_outcome_validation,
        },
        "non_authoritative": True,
        "non_applied": True,
        "non_persisted": True,
        "no_write_guarantees": deepcopy(_NO_WRITE_GUARANTEES),
    }
    return deepcopy(result)


def _validate_intermediate(stage: str, validation: Mapping[str, Any]) -> dict[str, Any]:
    copied = deepcopy(dict(validation)) if isinstance(validation, Mapping) else {}
    if copied != {"valid": True, "errors": []}:
        reasons = copied.get("errors", ()) if copied else ("validator_result_not_mapping",)
        _fail("invalid_intermediate_artifact", stage, reasons)
    return copied


def _non_blank(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _fail(code: str, stage: str, reasons: Any = ()) -> None:
    if isinstance(reasons, (str, bytes, bytearray)):
        stable_reasons = (str(reasons),)
    else:
        try:
            stable_reasons = tuple(str(reason) for reason in reasons)
        except TypeError:
            stable_reasons = (str(reasons),)
    raise GovernedMemoryLearningSliceError(code, stage, stable_reasons)


__all__ = [
    "GovernedMemoryLearningSliceError",
    "GOVERNED_MEMORY_LEARNING_SLICE_VERSION",
    "ALLOWED_INPUT_CLASSIFICATIONS",
    "TERMINAL_ARTIFACT",
    "run_governed_memory_learning_slice",
]
