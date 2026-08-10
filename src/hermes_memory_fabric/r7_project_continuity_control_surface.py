"""Bounded R7 project-continuity workflow for CIVILIZATION-CORE."""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from typing import Any, Mapping

from hermes_memory_fabric.governed_memory_learning_slice import (
    ALLOWED_INPUT_CLASSIFICATIONS,
    TERMINAL_ARTIFACT,
    run_governed_memory_learning_slice,
)
from hermes_memory_fabric.memory_human_review_outcome_gate import (
    SUPPORTED_HUMAN_REVIEW_OUTCOMES,
    validate_human_review_outcome_candidate,
)
from hermes_memory_fabric.provider import MemoryFabricProvider


R7_PROJECT_CONTINUITY_CONTROL_SURFACE_VERSION = "0.1"
R7_PROJECT_ID = "CIVILIZATION-CORE"
R7_OPERATOR = "FOUNDER-OPERATOR"

_RUNTIME_SURFACE = "r7_project_continuity_control_surface"
_WORKFLOW = (
    "candidate-memory",
    "evidence",
    "human-review",
    "scope-check",
    "correct",
    "revoke",
)
_CORRECTION_RECORD_TYPE = "project_continuity_correction"
_REVOCATION_RECORD_TYPE = "project_continuity_revocation"


class R7ProjectContinuityControlSurfaceError(ValueError):
    """Stable fail-closed error that never renders candidate content."""

    def __init__(
        self,
        code: str,
        stage: str,
        reasons: tuple[str, ...] | list[str] = (),
    ) -> None:
        self.code = str(code)
        self.stage = str(stage)
        self.reasons = tuple(str(reason) for reason in reasons)
        reason_text = ",".join(self.reasons) if self.reasons else "none"
        super().__init__(
            "r7_project_continuity_control_surface_error:"
            f"code={self.code};stage={self.stage};reasons={reason_text}"
        )


def run_r7_project_continuity_control_surface(
    candidate: Mapping[str, Any],
    *,
    query: str,
    project_id: str,
    operator: str,
    outcome: str,
    rationale: str,
    corrected_outcome: str,
    correction_rationale: str,
    revocation_rationale: str,
    input_classification: str,
    confirm_human_review: bool,
    confirm_scope_check: bool,
    confirm_correction: bool,
    confirm_revocation: bool,
    confirm_no_apply: bool,
) -> dict[str, Any]:
    """Run one explicit candidate through the terminal non-applied workflow."""

    candidate_snapshot = _validate_and_copy_inputs(
        candidate,
        query=query,
        project_id=project_id,
        operator=operator,
        outcome=outcome,
        rationale=rationale,
        corrected_outcome=corrected_outcome,
        correction_rationale=correction_rationale,
        revocation_rationale=revocation_rationale,
        input_classification=input_classification,
    )
    _require_confirmation(confirm_no_apply, "confirm_no_apply", "no-apply")

    provider = MemoryFabricProvider()
    active_context_packet = provider.build_active_context(
        query=query,
        memory_candidates=[deepcopy(candidate_snapshot)],
        project_scope=R7_PROJECT_ID,
        entity_ids=[R7_PROJECT_ID],
        memory_limit=1,
    )
    active_context_validation = deepcopy(
        provider.validate_active_context(active_context_packet)
    )
    if active_context_validation != {"valid": True, "errors": []}:
        _fail(
            "active_context_packet_invalid",
            "evidence",
            active_context_validation.get("errors", ()),
        )
    _validate_selected_candidate(active_context_packet, candidate_snapshot["id"])

    _require_confirmation(
        confirm_human_review,
        "confirm_human_review",
        "human-review",
    )
    governed_slice = run_governed_memory_learning_slice(
        deepcopy(candidate_snapshot),
        project_id=R7_PROJECT_ID,
        reviewer=R7_OPERATOR,
        outcome=outcome,
        rationale=rationale,
        input_classification=input_classification,
    )
    _validate_governed_slice(governed_slice)

    _require_confirmation(
        confirm_scope_check,
        "confirm_scope_check",
        "scope-check",
    )
    if active_context_packet.get("project_scope") != R7_PROJECT_ID:
        _fail("project_scope_mismatch", "scope-check")

    _require_confirmation(
        confirm_correction,
        "confirm_correction",
        "correct",
    )
    correction_record = create_correction_record(
        governed_slice["human_review_outcome_candidate"],
        project_id=R7_PROJECT_ID,
        operator=R7_OPERATOR,
        corrected_outcome=corrected_outcome,
        rationale=correction_rationale,
    )
    correction_validation = validate_correction_record(correction_record)
    if correction_validation != {"valid": True, "errors": []}:
        _fail(
            "correction_record_invalid",
            "correct",
            correction_validation.get("errors", ()),
        )

    _require_confirmation(
        confirm_revocation,
        "confirm_revocation",
        "revoke",
    )
    revocation_record = create_revocation_record(
        correction_record,
        rationale=revocation_rationale,
    )
    revocation_validation = validate_revocation_record(revocation_record)
    if revocation_validation != {"valid": True, "errors": []}:
        _fail(
            "revocation_record_invalid",
            "revoke",
            revocation_validation.get("errors", ()),
        )

    result = {
        "version": R7_PROJECT_CONTINUITY_CONTROL_SURFACE_VERSION,
        "runtime_surface": _RUNTIME_SURFACE,
        "status": "complete-terminal-non-applied-revocation",
        "project_id": R7_PROJECT_ID,
        "operator": R7_OPERATOR,
        "workflow": list(_WORKFLOW),
        "candidate_snapshot": deepcopy(candidate_snapshot),
        "active_context_packet": deepcopy(active_context_packet),
        "active_context_validation": deepcopy(active_context_validation),
        "governed_memory_learning_slice": deepcopy(governed_slice),
        "correction_record": deepcopy(correction_record),
        "correction_validation": deepcopy(correction_validation),
        "revocation_record": deepcopy(revocation_record),
        "revocation_validation": deepcopy(revocation_validation),
        "confirmation_snapshot": {
            "confirm_human_review": True,
            "confirm_scope_check": True,
            "confirm_correction": True,
            "confirm_revocation": True,
            "confirm_no_apply": True,
        },
        "terminal": True,
        "non_authoritative": True,
        "non_applied": True,
        "non_persisted": True,
        "continuation_authorized": False,
        "automatic_collection": False,
        "automatic_write": False,
        "automatic_approval": False,
        "automatic_adoption": False,
        "automatic_execution": False,
        "automatic_continuation": False,
    }
    return deepcopy(result)


def create_correction_record(
    human_review_outcome: Mapping[str, Any],
    *,
    project_id: str,
    operator: str,
    corrected_outcome: str,
    rationale: str,
) -> dict[str, Any]:
    """Create one deterministic superseding outcome record in memory."""

    if not isinstance(human_review_outcome, Mapping):
        _fail("human_review_outcome_must_be_mapping", "correct")
    source = deepcopy(dict(human_review_outcome))
    source_validation = validate_human_review_outcome_candidate(source)
    if source_validation != {"valid": True, "errors": []}:
        _fail(
            "human_review_outcome_invalid",
            "correct",
            source_validation.get("errors", ()),
        )
    if project_id != R7_PROJECT_ID or source.get("project_scope") != R7_PROJECT_ID:
        _fail("project_id_must_be_civilization_core", "correct")
    if operator != R7_OPERATOR or source.get("reviewer") != R7_OPERATOR:
        _fail("operator_must_be_founder_operator", "correct")
    prior_outcome = source.get("outcome")
    if prior_outcome not in SUPPORTED_HUMAN_REVIEW_OUTCOMES:
        _fail("unsupported_prior_outcome", "correct")
    if corrected_outcome not in SUPPORTED_HUMAN_REVIEW_OUTCOMES:
        _fail("unsupported_corrected_outcome", "correct")
    if corrected_outcome == prior_outcome:
        _fail("corrected_outcome_must_differ", "correct")
    if not _non_blank(source.get("outcome_id")):
        _fail("superseded_outcome_id_required", "correct")
    if not _non_blank(rationale):
        _fail("correction_rationale_required", "correct")

    record = {
        "version": R7_PROJECT_CONTINUITY_CONTROL_SURFACE_VERSION,
        "record_type": _CORRECTION_RECORD_TYPE,
        "correction_id": None,
        "project_id": R7_PROJECT_ID,
        "operator": R7_OPERATOR,
        "supersedes_outcome_id": source["outcome_id"],
        "prior_outcome": prior_outcome,
        "corrected_outcome": corrected_outcome,
        "rationale": rationale,
        "terminal": False,
        "non_authoritative": True,
        "non_applied": True,
        "non_persisted": True,
        "continuation_authorized": False,
    }
    record["correction_id"] = _correction_id(record)
    validation = validate_correction_record(record)
    if validation != {"valid": True, "errors": []}:
        _fail("correction_record_invalid", "correct", validation["errors"])
    return deepcopy(record)


def validate_correction_record(record: Mapping[str, Any]) -> dict[str, Any]:
    """Validate fixed scope, lineage, flags, and deterministic identity."""

    if not isinstance(record, Mapping):
        return {"valid": False, "errors": ["record_must_be_mapping"]}
    source = deepcopy(dict(record))
    errors: list[str] = []
    if source.get("version") != R7_PROJECT_CONTINUITY_CONTROL_SURFACE_VERSION:
        errors.append("version_must_be_0.1")
    if source.get("record_type") != _CORRECTION_RECORD_TYPE:
        errors.append("record_type_must_be_project_continuity_correction")
    if source.get("project_id") != R7_PROJECT_ID:
        errors.append("project_id_must_be_civilization_core")
    if source.get("operator") != R7_OPERATOR:
        errors.append("operator_must_be_founder_operator")
    if not _non_blank(source.get("supersedes_outcome_id")):
        errors.append("supersedes_outcome_id_required")
    if source.get("prior_outcome") not in SUPPORTED_HUMAN_REVIEW_OUTCOMES:
        errors.append("unsupported_prior_outcome")
    if source.get("corrected_outcome") not in SUPPORTED_HUMAN_REVIEW_OUTCOMES:
        errors.append("unsupported_corrected_outcome")
    if source.get("prior_outcome") == source.get("corrected_outcome"):
        errors.append("corrected_outcome_must_differ")
    if not _non_blank(source.get("rationale")):
        errors.append("rationale_required")
    if source.get("terminal") is not False:
        errors.append("terminal_must_be_false")
    _validate_non_applied_flags(source, errors)
    if source.get("correction_id") != _correction_id(source):
        errors.append("correction_id_mismatch")
    return {"valid": not errors, "errors": _dedupe(errors)}


def create_revocation_record(
    correction_record: Mapping[str, Any],
    *,
    rationale: str,
) -> dict[str, Any]:
    """Create the deterministic terminal revocation for one correction."""

    correction_validation = validate_correction_record(correction_record)
    if correction_validation != {"valid": True, "errors": []}:
        _fail(
            "correction_record_invalid",
            "revoke",
            correction_validation.get("errors", ()),
        )
    if not _non_blank(rationale):
        _fail("revocation_rationale_required", "revoke")
    correction = deepcopy(dict(correction_record))
    record = {
        "version": R7_PROJECT_CONTINUITY_CONTROL_SURFACE_VERSION,
        "record_type": _REVOCATION_RECORD_TYPE,
        "revocation_id": None,
        "project_id": R7_PROJECT_ID,
        "operator": R7_OPERATOR,
        "revokes_record_id": correction["correction_id"],
        "original_outcome_id": correction["supersedes_outcome_id"],
        "correction_id": correction["correction_id"],
        "prior_outcome": correction["prior_outcome"],
        "corrected_outcome": correction["corrected_outcome"],
        "outcome_lineage": [],
        "rationale": rationale,
        "terminal": True,
        "non_authoritative": True,
        "non_applied": True,
        "non_persisted": True,
        "continuation_authorized": False,
    }
    record["revocation_id"] = _revocation_id(record)
    record["outcome_lineage"] = _expected_outcome_lineage(record)
    validation = validate_revocation_record(record)
    if validation != {"valid": True, "errors": []}:
        _fail("revocation_record_invalid", "revoke", validation["errors"])
    return deepcopy(record)


def validate_revocation_record(record: Mapping[str, Any]) -> dict[str, Any]:
    """Validate terminal lineage, zero-application flags, and identity."""

    if not isinstance(record, Mapping):
        return {"valid": False, "errors": ["record_must_be_mapping"]}
    source = deepcopy(dict(record))
    errors: list[str] = []
    if source.get("version") != R7_PROJECT_CONTINUITY_CONTROL_SURFACE_VERSION:
        errors.append("version_must_be_0.1")
    if source.get("record_type") != _REVOCATION_RECORD_TYPE:
        errors.append("record_type_must_be_project_continuity_revocation")
    if source.get("project_id") != R7_PROJECT_ID:
        errors.append("project_id_must_be_civilization_core")
    if source.get("operator") != R7_OPERATOR:
        errors.append("operator_must_be_founder_operator")
    if not _non_blank(source.get("original_outcome_id")):
        errors.append("original_outcome_id_required")
    if not _non_blank(source.get("correction_id")):
        errors.append("correction_id_required")
    if source.get("revokes_record_id") != source.get("correction_id"):
        errors.append("revokes_record_id_must_equal_correction_id")
    if source.get("prior_outcome") not in SUPPORTED_HUMAN_REVIEW_OUTCOMES:
        errors.append("unsupported_prior_outcome")
    if source.get("corrected_outcome") not in SUPPORTED_HUMAN_REVIEW_OUTCOMES:
        errors.append("unsupported_corrected_outcome")
    if source.get("prior_outcome") == source.get("corrected_outcome"):
        errors.append("corrected_outcome_must_differ")
    if not _non_blank(source.get("rationale")):
        errors.append("rationale_required")
    if source.get("terminal") is not True:
        errors.append("terminal_must_be_true")
    _validate_non_applied_flags(source, errors)
    if source.get("revocation_id") != _revocation_id(source):
        errors.append("revocation_id_mismatch")
    if source.get("outcome_lineage") != _expected_outcome_lineage(source):
        errors.append("outcome_lineage_mismatch")
    return {"valid": not errors, "errors": _dedupe(errors)}


def _validate_and_copy_inputs(
    candidate: Mapping[str, Any],
    *,
    query: str,
    project_id: str,
    operator: str,
    outcome: str,
    rationale: str,
    corrected_outcome: str,
    correction_rationale: str,
    revocation_rationale: str,
    input_classification: str,
) -> dict[str, Any]:
    if not isinstance(candidate, Mapping):
        _fail("candidate_must_be_mapping", "input-boundary")
    snapshot = deepcopy(dict(candidate))
    if not _non_blank(query):
        _fail("query_required", "input-boundary")
    if project_id != R7_PROJECT_ID:
        _fail("project_id_must_be_civilization_core", "input-boundary")
    if operator != R7_OPERATOR:
        _fail("operator_must_be_founder_operator", "input-boundary")
    if snapshot.get("project_id") != R7_PROJECT_ID:
        _fail("candidate_project_id_must_be_civilization_core", "input-boundary")
    for field in ("id", "source", "source_id"):
        if not _non_blank(snapshot.get(field)):
            _fail(f"candidate_{field}_required", "input-boundary")
    provenance = snapshot.get("provenance")
    if not isinstance(provenance, Mapping) or not provenance:
        _fail("candidate_provenance_required", "input-boundary")
    if outcome not in SUPPORTED_HUMAN_REVIEW_OUTCOMES:
        _fail("unsupported_human_review_outcome", "input-boundary")
    if corrected_outcome not in SUPPORTED_HUMAN_REVIEW_OUTCOMES:
        _fail("unsupported_corrected_outcome", "input-boundary")
    if corrected_outcome == outcome:
        _fail("corrected_outcome_must_differ", "input-boundary")
    for field, value in (
        ("rationale", rationale),
        ("correction_rationale", correction_rationale),
        ("revocation_rationale", revocation_rationale),
    ):
        if not _non_blank(value):
            _fail(f"{field}_required", "input-boundary")
    if input_classification not in ALLOWED_INPUT_CLASSIFICATIONS:
        _fail("unsupported_input_classification", "input-boundary")
    return snapshot


def _validate_selected_candidate(
    packet: Mapping[str, Any],
    candidate_id: str,
) -> None:
    selected = packet.get("selected_memories")
    if not isinstance(selected, list) or len(selected) != 1:
        _fail("selected_candidate_count_must_equal_one", "evidence")
    selected_candidate = selected[0]
    if not isinstance(selected_candidate, Mapping):
        _fail("selected_candidate_must_be_mapping", "evidence")
    if selected_candidate.get("id") != candidate_id:
        _fail("selected_candidate_id_mismatch", "evidence")
    if packet.get("project_scope") != R7_PROJECT_ID:
        _fail("project_scope_mismatch", "evidence")


def _validate_governed_slice(result: Mapping[str, Any]) -> None:
    if not isinstance(result, Mapping):
        _fail("governed_slice_must_be_mapping", "human-review")
    expected = {
        "terminal_artifact": TERMINAL_ARTIFACT,
        "continuation_authorized": False,
        "non_authoritative": True,
        "non_applied": True,
        "non_persisted": True,
    }
    errors = [
        f"{field}_mismatch"
        for field, value in expected.items()
        if result.get(field) is not value and result.get(field) != value
    ]
    if result.get("project_id") != R7_PROJECT_ID:
        errors.append("project_id_mismatch")
    if result.get("reviewer") != R7_OPERATOR:
        errors.append("reviewer_mismatch")
    if errors:
        _fail("governed_slice_boundary_invalid", "human-review", errors)


def _require_confirmation(value: bool, field: str, stage: str) -> None:
    if value is not True:
        _fail(f"{field}_required", stage)


def _validate_non_applied_flags(
    record: Mapping[str, Any],
    errors: list[str],
) -> None:
    for field in ("non_authoritative", "non_applied", "non_persisted"):
        if record.get(field) is not True:
            errors.append(f"{field}_must_be_true")
    if record.get("continuation_authorized") is not False:
        errors.append("continuation_authorized_must_be_false")


def _correction_id(record: Mapping[str, Any]) -> str:
    identity = {
        key: deepcopy(record.get(key))
        for key in (
            "version",
            "record_type",
            "project_id",
            "operator",
            "supersedes_outcome_id",
            "prior_outcome",
            "corrected_outcome",
            "rationale",
            "terminal",
            "non_authoritative",
            "non_applied",
            "non_persisted",
            "continuation_authorized",
        )
    }
    return f"r7-correction:v0.1:{_stable_digest(identity)}"


def _revocation_id(record: Mapping[str, Any]) -> str:
    identity = {
        key: deepcopy(record.get(key))
        for key in (
            "version",
            "record_type",
            "project_id",
            "operator",
            "revokes_record_id",
            "original_outcome_id",
            "correction_id",
            "prior_outcome",
            "corrected_outcome",
            "rationale",
            "terminal",
            "non_authoritative",
            "non_applied",
            "non_persisted",
            "continuation_authorized",
        )
    }
    return f"r7-revocation:v0.1:{_stable_digest(identity)}"


def _expected_outcome_lineage(record: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "stage": "human-review",
            "record_id": record.get("original_outcome_id"),
            "outcome": record.get("prior_outcome"),
        },
        {
            "stage": "correct",
            "record_id": record.get("correction_id"),
            "outcome": record.get("corrected_outcome"),
        },
        {
            "stage": "revoke",
            "record_id": record.get("revocation_id"),
            "outcome": "revoked",
        },
    ]


def _stable_digest(value: Mapping[str, Any]) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


def _non_blank(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _dedupe(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))


def _fail(code: str, stage: str, reasons: Any = ()) -> None:
    if isinstance(reasons, (str, bytes, bytearray)):
        stable_reasons = (str(reasons),)
    else:
        try:
            stable_reasons = tuple(str(reason) for reason in reasons)
        except TypeError:
            stable_reasons = (str(reasons),)
    raise R7ProjectContinuityControlSurfaceError(code, stage, stable_reasons)


__all__ = [
    "R7ProjectContinuityControlSurfaceError",
    "create_correction_record",
    "create_revocation_record",
    "run_r7_project_continuity_control_surface",
    "validate_correction_record",
    "validate_revocation_record",
]
