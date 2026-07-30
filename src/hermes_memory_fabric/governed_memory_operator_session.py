"""Deterministic in-memory onboarding and operator-session surface for R6.1.

This module prepares a replacement scored corpus, teaches four non-scored
practice examples, instruments one ordered scored session, and delegates all
scoring to the unchanged operator-evaluation engine.  It does not persist,
apply, promote, execute, create a proposal, or create Evidence.
"""

from __future__ import annotations

import math
import re
import time
from copy import deepcopy
from typing import Any, Mapping

from hermes_memory_fabric import governed_memory_operator_evaluation as _engine


GOVERNED_MEMORY_OPERATOR_SESSION_VERSION = "0.1"
RUNTIME_SURFACE = "governed_memory_operator_session"
PRACTICE_COUNT = 4
SCORED_TRIAL_COUNT = 12

ACTION_EVENT_TYPES = (
    "GLOSSARY_OPENED",
    "GLOSSARY_CLOSED",
    "OUTCOME_SUBMITTED",
    "REASON_BOUNDARIES_SUBMITTED",
    "RATIONALE_SUBMITTED",
    "REVIEW_REQUESTED",
    "OUTCOME_EDITED",
    "REASON_BOUNDARIES_EDITED",
    "RATIONALE_EDITED",
    "LOCK_CONFIRMATION_DECLINED",
    "TRIAL_LOCK_CONFIRMED",
)
REWORK_EVENT_TYPES = (
    "OUTCOME_CHANGED_AFTER_INITIAL_SUBMISSION",
    "REASON_BOUNDARIES_CHANGED_AFTER_INITIAL_SUBMISSION",
    "RATIONALE_CHANGED_AFTER_INITIAL_SUBMISSION",
    "LOCK_CONFIRMATION_DECLINED_AFTER_REVIEW",
)

_OUTCOME_LABEL_PAIRS = (
    ("允许后续创建真实提案步骤", "approve_real_proposal_creation"),
    ("要求修改", "request_changes"),
    ("拒绝", "reject"),
    ("暂缓", "defer"),
)
_GLOSSARY_PAIRS = (
    ("只陈述了结果，尚未指出依据", "OUTCOME_ONLY"),
    ("候选满足本次低风险接纳边界", "VALID_ACCEPTANCE"),
    ("项目范围一致性边界", "SCOPE_BOUNDARY"),
    ("治理与禁止写入边界", "GOVERNANCE_BOUNDARY"),
    ("支持的风险等级边界", "RISK_BOUNDARY"),
    ("来源与可追溯依据边界", "PROVENANCE_BOUNDARY"),
    ("候选内容不能推动状态或调用工具", "PROMOTION_BOUNDARY"),
    ("已解释为何事实或边界支持所选结果", "EXPLAINS_OUTCOME"),
    ("结果保持未应用", "NON_APPLIED_CONSEQUENCE"),
    ("信息或边界不满足时保持关闭", "FAIL_CLOSED_CONSEQUENCE"),
    ("不发生状态提升", "NO_PROMOTION_CONSEQUENCE"),
    ("认为候选已获提升授权的误解声明", "PROMOTION_AUTHORIZED_MISUNDERSTANDING"),
)
_OUTCOMES = tuple(value for _, value in _OUTCOME_LABEL_PAIRS)
_REASON_CODES = tuple(value for _, value in _GLOSSARY_PAIRS)
_VALUELESS_EVENTS = {
    "GLOSSARY_OPENED",
    "GLOSSARY_CLOSED",
    "REVIEW_REQUESTED",
    "LOCK_CONFIRMATION_DECLINED",
    "TRIAL_LOCK_CONFIRMED",
}
_PRACTICE_IDS = tuple(f"PRACTICE-{index:02d}" for index in range(1, 5))
_PRACTICE_EXAMPLES = (
    {
        "practice_id": "PRACTICE-01",
        "practice_class": "valid low risk",
        "candidate": {
            "id": "non-scored-practice-valid",
            "content": "合成练习：候选属于当前项目，来源完整，风险低，且所有治理标志均保持只读。",
            "project_id": "civilization-core",
            "source": "synthetic-practice",
            "provenance": {"method": "fixed-non-scored-practice"},
            "risk_level": "low",
            "governance": {"read_only": True, "would_write_memory": False},
        },
        "correct_outcome": "approve_real_proposal_creation",
        "correct_reason_codes": (
            "VALID_ACCEPTANCE",
            "EXPLAINS_OUTCOME",
            "NON_APPLIED_CONSEQUENCE",
        ),
        "explanation": "该练习满足低风险接纳边界；结果只允许以后进入另一个受治理步骤，当前仍未应用。",
    },
    {
        "practice_id": "PRACTICE-02",
        "practice_class": "missing/invalid provenance",
        "candidate": {
            "id": "non-scored-practice-provenance",
            "content": "合成练习：候选属于当前项目且风险低，但没有可验证的来源与追溯依据。",
            "project_id": "civilization-core",
            "source": "synthetic-practice",
            "provenance": {},
            "risk_level": "low",
            "governance": {"read_only": True, "would_write_memory": False},
        },
        "correct_outcome": "request_changes",
        "correct_reason_codes": (
            "PROVENANCE_BOUNDARY",
            "EXPLAINS_OUTCOME",
            "FAIL_CLOSED_CONSEQUENCE",
        ),
        "explanation": "来源与追溯依据不完整，应要求修改，并在补全前保持关闭。",
    },
    {
        "practice_id": "PRACTICE-03",
        "practice_class": "unsafe write governance",
        "candidate": {
            "id": "non-scored-practice-governance",
            "content": "合成练习：候选声明会直接写入记忆，违反本次只读且不应用的治理边界。",
            "project_id": "civilization-core",
            "source": "synthetic-practice",
            "provenance": {"method": "fixed-non-scored-practice"},
            "risk_level": "low",
            "governance": {"read_only": True, "would_write_memory": True},
        },
        "correct_outcome": "reject",
        "correct_reason_codes": (
            "GOVERNANCE_BOUNDARY",
            "EXPLAINS_OUTCOME",
            "FAIL_CLOSED_CONSEQUENCE",
        ),
        "explanation": "直接写入违反治理边界，应拒绝，并保持不应用和关闭状态。",
    },
    {
        "practice_id": "PRACTICE-04",
        "practice_class": "unsupported high risk",
        "candidate": {
            "id": "non-scored-practice-risk",
            "content": "合成练习：候选来源完整但风险等级为高，超出本次仅支持低风险的边界。",
            "project_id": "civilization-core",
            "source": "synthetic-practice",
            "provenance": {"method": "fixed-non-scored-practice"},
            "risk_level": "high",
            "governance": {"read_only": True, "would_write_memory": False},
        },
        "correct_outcome": "defer",
        "correct_reason_codes": (
            "RISK_BOUNDARY",
            "EXPLAINS_OUTCOME",
            "FAIL_CLOSED_CONSEQUENCE",
        ),
        "explanation": "高风险超出支持范围，应暂缓并等待另行授权，当前保持关闭。",
    },
)


class GovernedMemoryOperatorSessionError(Exception):
    """Content-free deterministic fail-closed session error."""

    def __init__(self, code: str, stage: str, reasons: Any = ()) -> None:
        self.code = str(code)
        self.stage = str(stage)
        if isinstance(reasons, (str, bytes, bytearray)):
            reasons = (str(reasons),)
        else:
            try:
                reasons = tuple(str(reason) for reason in reasons)
            except TypeError:
                reasons = (str(reasons),)
        self.reasons = reasons
        rendered = ",".join(self.reasons) if self.reasons else "none"
        super().__init__(
            f"governed_memory_operator_session_error:"
            f"code={self.code};stage={self.stage};reasons={rendered}"
        )


def prepare_governed_memory_operator_session(
    replacement_corpus,
    original_corpus,
    *,
    project_id,
    operator_id,
    preexposed_candidate_digests=(),
):
    """Validate and lock the replacement experiment entirely in memory."""

    replacement_snapshot = _mapping_copy(replacement_corpus, "replacement_corpus")
    original_snapshot = _mapping_copy(original_corpus, "original_corpus")
    replacement_evaluation = _prepare_engine(
        replacement_snapshot,
        project_id=project_id,
        operator_id=operator_id,
        stage="replacement_corpus",
    )
    original_evaluation = _prepare_engine(
        original_snapshot,
        project_id=project_id,
        operator_id=operator_id,
        stage="original_corpus",
    )

    replacement_candidates = [
        deepcopy(trial["candidate"]) for trial in replacement_snapshot["trials"]
    ]
    original_candidates = [
        deepcopy(trial["candidate"]) for trial in original_snapshot["trials"]
    ]
    replacement_digests = tuple(
        _engine._canonical_sha256(candidate) for candidate in replacement_candidates
    )
    original_digests = tuple(
        _engine._canonical_sha256(candidate) for candidate in original_candidates
    )
    exposed = _digest_set(preexposed_candidate_digests)

    if len(set(replacement_digests)) != SCORED_TRIAL_COUNT:
        _fail("replacement_candidate_digests_not_unique", "corpus_readiness")
    if set(replacement_digests) & set(original_digests):
        _fail("replacement_candidate_digest_overlap", "corpus_readiness")
    if set(replacement_digests) & exposed:
        _fail("replacement_candidate_preexposed", "operator_eligibility")

    _require_new_unique_values(
        replacement_candidates,
        original_candidates,
        key="id",
        code="replacement_candidate_ids_not_entirely_new",
    )
    _require_new_unique_values(
        replacement_candidates,
        original_candidates,
        key="source_id",
        code="replacement_source_ids_not_entirely_new",
    )
    _require_new_unique_values(
        replacement_candidates,
        original_candidates,
        key="content",
        code="replacement_candidate_contents_not_entirely_new",
    )
    replacement_fixtures = [
        _fixture_identity(candidate, strict=True) for candidate in replacement_candidates
    ]
    original_fixtures = [
        identity
        for candidate in original_candidates
        if (identity := _fixture_identity(candidate, strict=False)) is not None
    ]
    if (
        len(set(replacement_fixtures)) != SCORED_TRIAL_COUNT
        or set(replacement_fixtures) & set(original_fixtures)
    ):
        _fail("replacement_fixture_identities_not_entirely_new", "corpus_readiness")

    practice_digests = {
        _engine._canonical_sha256(example["candidate"])
        for example in _PRACTICE_EXAMPLES
    }
    if (
        len(practice_digests) != PRACTICE_COUNT
        or practice_digests & set(replacement_digests)
        or practice_digests & set(original_digests)
    ):
        _fail("practice_candidate_overlap", "practice")

    session = {
        "version": GOVERNED_MEMORY_OPERATOR_SESSION_VERSION,
        "runtime_surface": RUNTIME_SURFACE,
        "status": "practice_ready",
        "project_id": deepcopy(project_id),
        "operator_id": deepcopy(operator_id),
        "replacement_corpus_sha256": replacement_evaluation["corpus_sha256"],
        "original_corpus_sha256": original_evaluation["corpus_sha256"],
        "practice_ids": list(_PRACTICE_IDS),
        "scored_trial_ids": deepcopy(replacement_evaluation["trial_order"]),
        "practice_completion_records": [],
        "observations": [],
        "locked_trial_ids": [],
        "action_events": [],
        "rework_events": [],
        "human_timing": [],
        "system_timing": [],
        "evidence_document_authorized": False,
        "evidence_document_created": False,
        "continuation_authorized": False,
        "non_applied": True,
        "non_persisted": True,
        "_evaluation": replacement_evaluation,
        "_replacement_candidate_digests": list(replacement_digests),
        "_original_candidate_digests": list(original_digests),
        "_practice_examples": deepcopy(_PRACTICE_EXAMPLES),
        "_locked_observations": [],
        "_current_trial": None,
        "_eligibility_attestations": None,
        "_rule_lock_sha256": _rule_lock_sha256(),
    }
    return _seal(session)


def build_operator_practice_packet(
    session,
    *,
    practice_id,
):
    """Return the next fixed non-scored practice packet without feedback."""

    checked = _require_session(session)
    expected_index = len(checked["practice_completion_records"])
    if checked["status"] != "practice_ready":
        _fail("practice_phase_not_open", "practice")
    if expected_index >= PRACTICE_COUNT or practice_id != _PRACTICE_IDS[expected_index]:
        _fail("practice_order_invalid", "practice")
    example = checked["_practice_examples"][expected_index]
    packet = {
        "practice_id": example["practice_id"],
        "phase": "NON-SCORED-PRACTICE",
        "candidate": deepcopy(example["candidate"]),
        "outcome_choices": _outcome_choices(),
        "reason_glossary": _reason_glossary(),
        "rationale_required": True,
        "scored": False,
        "feedback_available": False,
    }
    return deepcopy(packet)


def record_operator_practice_response(
    session,
    *,
    practice_id,
    outcome,
    rationale,
    rationale_reason_codes,
):
    """Record one sequential practice response and then reveal fixed feedback."""

    checked = _require_session(session)
    expected_index = len(checked["practice_completion_records"])
    if checked["status"] != "practice_ready":
        _fail("practice_phase_not_open", "practice")
    if expected_index >= PRACTICE_COUNT or practice_id != _PRACTICE_IDS[expected_index]:
        _fail("practice_order_invalid", "practice")
    _require_outcome(outcome, "practice")
    _require_rationale(rationale, "practice")
    codes = _require_reason_codes(rationale_reason_codes, "practice")
    example = checked["_practice_examples"][expected_index]
    checked["practice_completion_records"].append(
        {
            "practice_id": practice_id,
            "phase": "NON-SCORED-PRACTICE",
            "completed": True,
            "scored": False,
        }
    )
    feedback = {
        "practice_id": practice_id,
        "phase": "NON-SCORED-PRACTICE",
        "submitted_outcome": outcome,
        "submitted_rationale": rationale,
        "submitted_reason_codes": codes,
        "correct_outcome": example["correct_outcome"],
        "correct_reason_codes": list(example["correct_reason_codes"]),
        "correct": outcome == example["correct_outcome"],
        "explanation": example["explanation"],
        "scored": False,
        "feedback_available": True,
    }
    if len(checked["practice_completion_records"]) == PRACTICE_COUNT:
        checked["status"] = "eligibility_attestation_required"
    return {"session": _seal(checked), "feedback": deepcopy(feedback)}


def start_governed_memory_operator_scored_session(
    session,
    *,
    no_prior_answer_key_exposure_attestation,
    no_outside_assistance_commitment,
):
    """Open scoring only after practice and exact eligibility attestations."""

    checked = _require_session(session)
    if (
        checked["status"] != "eligibility_attestation_required"
        or len(checked["practice_completion_records"]) != PRACTICE_COUNT
    ):
        _fail("practice_not_complete", "operator_eligibility")
    if no_prior_answer_key_exposure_attestation is not True:
        _fail("no_prior_answer_key_exposure_attestation_required", "operator_eligibility")
    if no_outside_assistance_commitment is not True:
        _fail("no_outside_assistance_commitment_required", "operator_eligibility")
    checked["_eligibility_attestations"] = {
        "no_prior_answer_key_exposure_attestation": True,
        "no_outside_assistance_commitment": True,
    }
    checked["status"] = "scored_session_ready"
    return _seal(checked)


def open_operator_scored_trial(
    session,
    *,
    trial_id,
    monotonic_ms,
):
    """Open only the next exact scored trial and start human timing."""

    checked = _require_session(session)
    _require_timestamp(monotonic_ms, "trial_open")
    if checked["status"] not in {"scored_session_ready", "scored_session_in_progress"}:
        _fail("scored_session_not_ready", "trial_open")
    if checked["_eligibility_attestations"] != {
        "no_prior_answer_key_exposure_attestation": True,
        "no_outside_assistance_commitment": True,
    }:
        _fail("operator_eligibility_invalid", "trial_open")
    if checked["_current_trial"] is not None:
        _fail("current_trial_already_open", "trial_open")
    next_index = len(checked["locked_trial_ids"])
    if next_index >= SCORED_TRIAL_COUNT or trial_id != checked["scored_trial_ids"][next_index]:
        _fail("scored_trial_order_invalid", "trial_open")
    try:
        packet = _engine.build_operator_trial_packet(
            checked["_evaluation"],
            trial_id=trial_id,
        )
    except Exception:
        _fail("existing_packet_builder_rejected_trial", "trial_open")
    view = _safe_scored_view(packet)
    checked["_current_trial"] = {
        "trial_id": trial_id,
        "opened_monotonic_ms": monotonic_ms,
        "last_monotonic_ms": monotonic_ms,
        "phase": "editing",
        "glossary_open": False,
        "outcome": None,
        "rationale_reason_codes": None,
        "rationale": None,
        "view": deepcopy(view),
        "action_events": [],
        "rework_events": [],
        "review_snapshot": None,
    }
    checked["status"] = "scored_session_in_progress"
    return {"session": _seal(checked), "view": deepcopy(view)}


def record_operator_scored_trial_event(
    session,
    *,
    trial_id,
    event_type,
    value=None,
    monotonic_ms,
):
    """Apply one accepted current-trial transition and instrument it."""

    checked = _require_session(session)
    current = checked["_current_trial"]
    if not isinstance(current, Mapping) or trial_id != current.get("trial_id"):
        _fail("current_open_trial_required", "scored_event")
    if event_type not in ACTION_EVENT_TYPES:
        _fail("unsupported_action_event_type", "scored_event")
    _require_timestamp(monotonic_ms, "scored_event")
    if monotonic_ms < current["last_monotonic_ms"]:
        _fail("monotonic_time_must_be_non_decreasing", "scored_event")
    if event_type in _VALUELESS_EVENTS and value is not None:
        _fail("event_value_must_be_absent", "scored_event")

    review = None
    locked_observation = None
    rework_type = None

    if event_type == "GLOSSARY_OPENED":
        if current["glossary_open"] is True:
            _fail("glossary_already_open", "scored_event")
        current["glossary_open"] = True
    elif event_type == "GLOSSARY_CLOSED":
        if current["glossary_open"] is not True:
            _fail("glossary_not_open", "scored_event")
        current["glossary_open"] = False
    elif event_type in {"OUTCOME_SUBMITTED", "OUTCOME_EDITED"}:
        if current["phase"] != "editing":
            _fail("trial_not_editable", "scored_event")
        _require_outcome(value, "scored_event")
        if event_type == "OUTCOME_SUBMITTED":
            if current["outcome"] is not None:
                _fail("outcome_already_submitted", "scored_event")
        else:
            if current["outcome"] is None:
                _fail("initial_outcome_required", "scored_event")
            if value == current["outcome"]:
                _fail("same_value_is_not_transition", "scored_event")
            rework_type = "OUTCOME_CHANGED_AFTER_INITIAL_SUBMISSION"
        current["outcome"] = value
    elif event_type in {
        "REASON_BOUNDARIES_SUBMITTED",
        "REASON_BOUNDARIES_EDITED",
    }:
        if current["phase"] != "editing":
            _fail("trial_not_editable", "scored_event")
        codes = _require_reason_codes(value, "scored_event")
        if event_type == "REASON_BOUNDARIES_SUBMITTED":
            if current["rationale_reason_codes"] is not None:
                _fail("reason_boundaries_already_submitted", "scored_event")
        else:
            if current["rationale_reason_codes"] is None:
                _fail("initial_reason_boundaries_required", "scored_event")
            if codes == current["rationale_reason_codes"]:
                _fail("same_value_is_not_transition", "scored_event")
            rework_type = "REASON_BOUNDARIES_CHANGED_AFTER_INITIAL_SUBMISSION"
        current["rationale_reason_codes"] = codes
    elif event_type in {"RATIONALE_SUBMITTED", "RATIONALE_EDITED"}:
        if current["phase"] != "editing":
            _fail("trial_not_editable", "scored_event")
        _require_rationale(value, "scored_event")
        if event_type == "RATIONALE_SUBMITTED":
            if current["rationale"] is not None:
                _fail("rationale_already_submitted", "scored_event")
        else:
            if current["rationale"] is None:
                _fail("initial_rationale_required", "scored_event")
            if value == current["rationale"]:
                _fail("same_value_is_not_transition", "scored_event")
            rework_type = "RATIONALE_CHANGED_AFTER_INITIAL_SUBMISSION"
        current["rationale"] = value
    elif event_type == "REVIEW_REQUESTED":
        if current["phase"] != "editing" or current["glossary_open"] is True:
            _fail("trial_not_ready_for_review", "scored_event")
        _require_complete_current_trial(current)
        review = _review_snapshot(current)
        current["phase"] = "reviewed"
        current["review_snapshot"] = deepcopy(review)
    elif event_type == "LOCK_CONFIRMATION_DECLINED":
        if current["phase"] != "reviewed" or current["glossary_open"] is True:
            _fail("valid_review_required_before_decline", "scored_event")
        current["phase"] = "editing"
        current["review_snapshot"] = None
        rework_type = "LOCK_CONFIRMATION_DECLINED_AFTER_REVIEW"
    elif event_type == "TRIAL_LOCK_CONFIRMED":
        if current["phase"] != "reviewed" or current["glossary_open"] is True:
            _fail("valid_review_required_before_lock", "scored_event")
        _require_complete_current_trial(current)
        elapsed = monotonic_ms - current["opened_monotonic_ms"]
        if elapsed <= 0 or not float(elapsed).is_integer():
            _fail("human_elapsed_ms_must_be_positive_integer", "trial_lock")

    action_event = {
        "trial_id": trial_id,
        "event_type": event_type,
        "monotonic_ms": monotonic_ms,
    }
    current["action_events"].append(deepcopy(action_event))
    checked["action_events"].append(deepcopy(action_event))
    if rework_type is not None:
        rework_event = {
            "trial_id": trial_id,
            "event_type": rework_type,
            "monotonic_ms": monotonic_ms,
        }
        current["rework_events"].append(deepcopy(rework_event))
        checked["rework_events"].append(deepcopy(rework_event))
    current["last_monotonic_ms"] = monotonic_ms

    if event_type == "TRIAL_LOCK_CONFIRMED":
        human_elapsed_ms = int(monotonic_ms - current["opened_monotonic_ms"])
        try:
            full_observation = _engine.record_operator_trial_observation(
                checked["_evaluation"],
                trial_id=trial_id,
                reviewer=checked["operator_id"],
                outcome=current["outcome"],
                rationale=current["rationale"],
                human_elapsed_ms=human_elapsed_ms,
                operator_action_count=len(current["action_events"]),
                correction_rework_count=len(current["rework_events"]),
                rationale_reason_codes=current["rationale_reason_codes"],
            )
        except Exception:
            _fail("existing_observation_recorder_rejected_input", "trial_lock")
        checked["_locked_observations"].append(deepcopy(full_observation))
        locked_observation = _safe_locked_observation(full_observation)
        checked["observations"].append(deepcopy(locked_observation))
        checked["locked_trial_ids"].append(trial_id)
        checked["human_timing"].append(
            {"trial_id": trial_id, "human_elapsed_ms": human_elapsed_ms}
        )
        checked["system_timing"].append(
            {
                "trial_id": trial_id,
                "system_measurement_scope": full_observation["system_measurement_scope"],
                "system_elapsed_ms": full_observation["system_elapsed_ms"],
            }
        )
        checked["_current_trial"] = None
        checked["status"] = (
            "finalization_ready"
            if len(checked["locked_trial_ids"]) == SCORED_TRIAL_COUNT
            else "scored_session_in_progress"
        )

    return {
        "session": _seal(checked),
        "review": deepcopy(review),
        "locked_observation": deepcopy(locked_observation),
    }


def finalize_governed_memory_operator_session(
    session,
    *,
    ungoverned_perceived_usefulness,
    ungoverned_perceived_burden,
    governed_perceived_usefulness,
    governed_perceived_burden,
    no_answer_key_attestation,
    no_outside_assistance_attestation,
):
    """Finalize one complete valid in-memory session through the existing engine."""

    checked = _require_session(session)
    if (
        checked["status"] != "finalization_ready"
        or checked["_current_trial"] is not None
        or checked["locked_trial_ids"] != checked["scored_trial_ids"]
        or len(checked["_locked_observations"]) != SCORED_TRIAL_COUNT
        or len(checked["observations"]) != SCORED_TRIAL_COUNT
    ):
        _fail("all_twelve_trials_must_be_locked_in_order", "finalization")
    scores = (
        ungoverned_perceived_usefulness,
        ungoverned_perceived_burden,
        governed_perceived_usefulness,
        governed_perceived_burden,
    )
    if any(
        isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= 5
        for value in scores
    ):
        _fail("condition_scores_must_be_integers_1_to_5", "finalization")
    if no_answer_key_attestation is not True:
        _fail("no_answer_key_attestation_required", "finalization")
    if no_outside_assistance_attestation is not True:
        _fail("no_outside_assistance_attestation_required", "finalization")
    _validate_raw_record_integrity(checked)
    try:
        evaluation_result = _engine.finalize_governed_memory_operator_evaluation(
            checked["_evaluation"],
            checked["_locked_observations"],
            ungoverned_perceived_usefulness=ungoverned_perceived_usefulness,
            ungoverned_perceived_burden=ungoverned_perceived_burden,
            governed_perceived_usefulness=governed_perceived_usefulness,
            governed_perceived_burden=governed_perceived_burden,
        )
    except Exception:
        _fail("existing_evaluation_finalizer_rejected_session", "finalization")

    result = {
        "version": GOVERNED_MEMORY_OPERATOR_SESSION_VERSION,
        "status": "complete_valid_session",
        "runtime_surface": RUNTIME_SURFACE,
        "project_id": checked["project_id"],
        "operator_id": checked["operator_id"],
        "replacement_corpus_sha256": checked["replacement_corpus_sha256"],
        "original_corpus_sha256": checked["original_corpus_sha256"],
        "practice_completion_records": deepcopy(
            checked["practice_completion_records"]
        ),
        "locked_observations": deepcopy(checked["_locked_observations"]),
        "raw_ordered_action_events": deepcopy(checked["action_events"]),
        "raw_ordered_rework_events": deepcopy(checked["rework_events"]),
        "human_timing": deepcopy(checked["human_timing"]),
        "system_timing": deepcopy(checked["system_timing"]),
        "condition_perception_scores": {
            "UNGOVERNED-RAW-REVIEW": {
                "perceived_usefulness": ungoverned_perceived_usefulness,
                "perceived_governance_burden": ungoverned_perceived_burden,
            },
            "GOVERNED-STRUCTURED-REVIEW": {
                "perceived_usefulness": governed_perceived_usefulness,
                "perceived_governance_burden": governed_perceived_burden,
            },
        },
        "final_attestations": {
            "no_answer_key_attestation": True,
            "no_outside_assistance_attestation": True,
        },
        "evaluation_result": deepcopy(evaluation_result),
        "evidence_document_authorized": True,
        "evidence_document_created": False,
        "continuation_authorized": False,
        "non_applied": True,
        "non_persisted": True,
        "corpus_reuse_authorized": False,
    }
    return deepcopy(result)


def run_governed_memory_operator_session(
    replacement_corpus,
    original_corpus,
    *,
    project_id,
    operator_id,
    input_fn=input,
    output_fn=print,
    monotonic_ms_fn=None,
    preexposed_candidate_digests=(),
):
    """Run the fixed Chinese terminal flow without writing files."""

    clock = monotonic_ms_fn
    if clock is None:
        clock = lambda: time.monotonic_ns() / 1_000_000
    try:
        session = prepare_governed_memory_operator_session(
            replacement_corpus,
            original_corpus,
            project_id=project_id,
            operator_id=operator_id,
            preexposed_candidate_digests=preexposed_candidate_digests,
        )
        output_fn("本地受治理记忆评估：练习不计分，评分阶段不得查看答案或使用外部协助。")
        output_fn(_fixed_explanation())
        output_fn({"固定结果选项": _outcome_choices(), "固定术语表": _reason_glossary()})

        for practice_id in session["practice_ids"]:
            packet = build_operator_practice_packet(session, practice_id=practice_id)
            output_fn(packet)
            outcome = _terminal_outcome(input_fn, output_fn)
            codes = _terminal_reason_codes(input_fn)
            rationale = input_fn("请输入理由：")
            recorded = record_operator_practice_response(
                session,
                practice_id=practice_id,
                outcome=outcome,
                rationale=rationale,
                rationale_reason_codes=codes,
            )
            session = recorded["session"]
            output_fn(recorded["feedback"])

        eligible_answer_key = _terminal_yes(
            input_fn("确认此前未查看任何旧或替换评分答案材料（是/否）：")
        )
        eligible_assistance = _terminal_yes(
            input_fn("承诺评分阶段不使用任何外部试题协助（是/否）：")
        )
        session = start_governed_memory_operator_scored_session(
            session,
            no_prior_answer_key_exposure_attestation=eligible_answer_key,
            no_outside_assistance_commitment=eligible_assistance,
        )

        for trial_id in session["scored_trial_ids"]:
            opened = open_operator_scored_trial(
                session,
                trial_id=trial_id,
                monotonic_ms=clock(),
            )
            session = opened["session"]
            output_fn(opened["view"])
            session = _terminal_optional_glossary(
                session, trial_id, input_fn, output_fn, clock
            )
            outcome = _terminal_outcome(input_fn, output_fn)
            codes = _terminal_reason_codes(input_fn)
            rationale = input_fn("请输入独立理由：")
            session = record_operator_scored_trial_event(
                session,
                trial_id=trial_id,
                event_type="OUTCOME_SUBMITTED",
                value=outcome,
                monotonic_ms=clock(),
            )["session"]
            session = record_operator_scored_trial_event(
                session,
                trial_id=trial_id,
                event_type="REASON_BOUNDARIES_SUBMITTED",
                value=codes,
                monotonic_ms=clock(),
            )["session"]
            session = record_operator_scored_trial_event(
                session,
                trial_id=trial_id,
                event_type="RATIONALE_SUBMITTED",
                value=rationale,
                monotonic_ms=clock(),
            )["session"]

            while True:
                reviewed = record_operator_scored_trial_event(
                    session,
                    trial_id=trial_id,
                    event_type="REVIEW_REQUESTED",
                    monotonic_ms=clock(),
                )
                session = reviewed["session"]
                output_fn(reviewed["review"])
                if _terminal_yes(input_fn("确认锁定本题且不可返回（是/否）：")):
                    locked = record_operator_scored_trial_event(
                        session,
                        trial_id=trial_id,
                        event_type="TRIAL_LOCK_CONFIRMED",
                        monotonic_ms=clock(),
                    )
                    session = locked["session"]
                    break
                session = record_operator_scored_trial_event(
                    session,
                    trial_id=trial_id,
                    event_type="LOCK_CONFIRMATION_DECLINED",
                    monotonic_ms=clock(),
                )["session"]
                session = _terminal_optional_glossary(
                    session, trial_id, input_fn, output_fn, clock
                )
                new_outcome = _terminal_outcome(input_fn, output_fn)
                new_codes = _terminal_reason_codes(input_fn)
                new_rationale = input_fn("请重新输入独立理由：")
                current = session["_current_trial"]
                if new_outcome != current["outcome"]:
                    session = record_operator_scored_trial_event(
                        session,
                        trial_id=trial_id,
                        event_type="OUTCOME_EDITED",
                        value=new_outcome,
                        monotonic_ms=clock(),
                    )["session"]
                if new_codes != current["rationale_reason_codes"]:
                    session = record_operator_scored_trial_event(
                        session,
                        trial_id=trial_id,
                        event_type="REASON_BOUNDARIES_EDITED",
                        value=new_codes,
                        monotonic_ms=clock(),
                    )["session"]
                if new_rationale != current["rationale"]:
                    session = record_operator_scored_trial_event(
                        session,
                        trial_id=trial_id,
                        event_type="RATIONALE_EDITED",
                        value=new_rationale,
                        monotonic_ms=clock(),
                    )["session"]

        scores = [_terminal_score(input_fn) for _ in range(4)]
        no_answer_key = _terminal_yes(
            input_fn("最终确认评分期间未查看答案材料（是/否）：")
        )
        no_assistance = _terminal_yes(
            input_fn("最终确认评分期间未使用外部试题协助（是/否）：")
        )
        return finalize_governed_memory_operator_session(
            session,
            ungoverned_perceived_usefulness=scores[0],
            ungoverned_perceived_burden=scores[1],
            governed_perceived_usefulness=scores[2],
            governed_perceived_burden=scores[3],
            no_answer_key_attestation=no_answer_key,
            no_outside_assistance_attestation=no_assistance,
        )
    except (EOFError, KeyboardInterrupt):
        return {
            "status": "INVALID-MEASUREMENT",
            "invalid_reasons": ["SESSION_INTERRUPTED"],
            "evidence_document_authorized": False,
            "evidence_document_created": False,
            "corpus_reuse_authorized": False,
            "continuation_authorized": False,
        }


def _prepare_engine(corpus, *, project_id, operator_id, stage):
    try:
        return _engine.prepare_governed_memory_operator_evaluation(
            corpus,
            project_id=project_id,
            operator_id=operator_id,
        )
    except Exception:
        _fail("existing_engine_corpus_validation_failed", stage)


def _mapping_copy(value: Any, name: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        _fail(f"{name}_must_be_mapping", "preparation")
    return deepcopy(dict(value))


def _digest_set(value: Any) -> set[str]:
    if isinstance(value, (str, bytes, bytearray)):
        _fail("preexposed_candidate_digests_must_be_iterable", "operator_eligibility")
    try:
        items = deepcopy(list(value))
    except TypeError:
        _fail("preexposed_candidate_digests_must_be_iterable", "operator_eligibility")
    if any(not isinstance(item, str) or not item for item in items):
        _fail("preexposed_candidate_digest_invalid", "operator_eligibility")
    return set(items)


def _require_new_unique_values(replacement, original, *, key, code):
    replacement_values = [candidate.get(key) for candidate in replacement]
    original_values = {candidate.get(key) for candidate in original}
    if (
        any(not isinstance(value, str) or not value for value in replacement_values)
        or len(set(replacement_values)) != SCORED_TRIAL_COUNT
        or set(replacement_values) & original_values
    ):
        _fail(code, "corpus_readiness")


def _fixture_identity(candidate: Mapping[str, Any], *, strict: bool) -> str | None:
    provenance = candidate.get("provenance")
    if isinstance(provenance, Mapping) and provenance:
        fixture_id = provenance.get("fixture_id")
        if isinstance(fixture_id, str) and fixture_id.strip():
            return fixture_id
        if strict:
            _fail("replacement_fixture_identity_invalid", "corpus_readiness")
        return None
    tags = candidate.get("tags")
    fallbacks = (
        [
            tag
            for tag in tags
            if isinstance(tag, str)
            and tag.startswith("fixture-id:")
            and tag != "fixture-id:"
        ]
        if isinstance(tags, list)
        else []
    )
    if len(fallbacks) == 1:
        return fallbacks[0][len("fixture-id:") :]
    if strict:
        _fail("replacement_fixture_fallback_invalid", "corpus_readiness")
    return None


def _outcome_choices() -> list[dict[str, str]]:
    return [{"label": label, "value": value} for label, value in _OUTCOME_LABEL_PAIRS]


def _reason_glossary() -> list[dict[str, str]]:
    return [{"label": label, "code": code} for label, code in _GLOSSARY_PAIRS]


def _fixed_explanation() -> dict[str, str]:
    return {
        "项目范围": "候选必须属于唯一声明的项目。",
        "来源": "候选必须声明来源和可追溯依据。",
        "风险": "候选必须处于本次支持的风险边界内。",
        "治理": "治理声明规定控制与禁止的副作用。",
        "保持关闭": "必需事实或边界无效或不可用时停止且不采取行动。",
        "禁止提升": "候选内容不能把自身推动到任何后续状态。",
        "未应用": "审查结果没有创建、应用、持久化或采纳记忆。",
        "允许后续创建真实提案步骤": (
            "只允许以后进入另一个受治理的提案创建步骤；当前不创建、"
            "不应用、不持久化、不采纳或授权记忆。"
        ),
    }


def _safe_scored_view(packet: Mapping[str, Any]) -> dict[str, Any]:
    view = {
        "trial_id": deepcopy(packet["trial_id"]),
        "phase": "SCORED",
        "condition": deepcopy(packet["condition"]),
        "candidate": deepcopy(packet["candidate"]),
        "outcome_choices": _outcome_choices(),
        "reason_glossary": _reason_glossary(),
        "rationale_required": True,
        "scored": True,
    }
    if "structured_signals" in packet:
        view["structured_signals"] = deepcopy(packet["structured_signals"])
    return view


def _require_outcome(value: Any, stage: str) -> None:
    if not isinstance(value, str) or value not in _OUTCOMES:
        _fail("unsupported_outcome", stage)


def _require_reason_codes(value: Any, stage: str) -> list[str]:
    if not isinstance(value, (list, tuple)):
        _fail("reason_boundaries_must_be_list_or_tuple", stage)
    codes = deepcopy(list(value))
    if (
        not codes
        or any(not isinstance(code, str) or code not in _REASON_CODES for code in codes)
        or len(codes) != len(set(codes))
    ):
        _fail("reason_boundaries_invalid", stage)
    return codes


def _require_rationale(value: Any, stage: str) -> None:
    if not isinstance(value, str) or not value.strip():
        _fail("rationale_required", stage)
    text = value.strip()
    text = re.sub(r"^\s*\d+\s*[\.\、\)\]：:\-]*\s*", "", text)
    decoration = " \t\r\n.,，。:：;；!?！？-—–_*#·•●○()（）[]【】{}<>《》'\"“”‘’/\\|"
    text = text.strip(decoration)
    if text in {label for label, _ in _OUTCOME_LABEL_PAIRS} | set(_OUTCOMES):
        _fail("rationale_must_not_be_outcome_option_only", stage)


def _require_timestamp(value: Any, stage: str) -> None:
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
        or value < 0
    ):
        _fail("monotonic_ms_invalid", stage)


def _require_complete_current_trial(current: Mapping[str, Any]) -> None:
    _require_outcome(current.get("outcome"), "review")
    _require_reason_codes(current.get("rationale_reason_codes"), "review")
    _require_rationale(current.get("rationale"), "review")


def _review_snapshot(current: Mapping[str, Any]) -> dict[str, Any]:
    candidate = current["view"]["candidate"]
    return {
        "trial_id": current["trial_id"],
        "candidate_identity": {
            "id": deepcopy(candidate.get("id")),
            "source_id": deepcopy(candidate.get("source_id")),
        },
        "outcome": current["outcome"],
        "rationale_reason_codes": deepcopy(current["rationale_reason_codes"]),
        "rationale": current["rationale"],
        "correctness_exposed": False,
    }


def _safe_locked_observation(observation: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "trial_id": observation["trial_id"],
        "condition": observation["condition"],
        "reviewer": observation["reviewer"],
        "outcome": observation["outcome"],
        "rationale": observation["rationale"],
        "rationale_reason_codes": deepcopy(observation["rationale_reason_codes"]),
        "human_elapsed_ms": observation["human_elapsed_ms"],
        "operator_action_count": observation["operator_action_count"],
        "correction_rework_count": observation["correction_rework_count"],
        "locked": True,
        "correctness_exposed": False,
    }


def _validate_raw_record_integrity(session: Mapping[str, Any]) -> None:
    action_total = sum(item["operator_action_count"] for item in session["observations"])
    rework_total = sum(
        item["correction_rework_count"] for item in session["observations"]
    )
    if action_total != len(session["action_events"]):
        _fail("raw_action_event_count_mismatch", "finalization")
    if rework_total != len(session["rework_events"]):
        _fail("raw_rework_event_count_mismatch", "finalization")
    if any(
        event.get("event_type") not in ACTION_EVENT_TYPES
        for event in session["action_events"]
    ):
        _fail("raw_action_event_type_invalid", "finalization")
    if any(
        event.get("event_type") not in REWORK_EVENT_TYPES
        for event in session["rework_events"]
    ):
        _fail("raw_rework_event_type_invalid", "finalization")
    if (
        len(session["human_timing"]) != SCORED_TRIAL_COUNT
        or len(session["system_timing"]) != SCORED_TRIAL_COUNT
    ):
        _fail("timing_records_incomplete", "finalization")


def _rule_lock_sha256() -> str:
    return _engine._canonical_sha256(
        {
            "action_event_types": ACTION_EVENT_TYPES,
            "rework_event_types": REWORK_EVENT_TYPES,
            "outcome_labels": _OUTCOME_LABEL_PAIRS,
            "glossary": _GLOSSARY_PAIRS,
        }
    )


def _integrity_sha256(session: Mapping[str, Any]) -> str:
    copied = deepcopy(dict(session))
    copied.pop("_session_integrity_sha256", None)
    return _engine._canonical_sha256(copied)


def _seal(session: Mapping[str, Any]) -> dict[str, Any]:
    sealed = deepcopy(dict(session))
    sealed["_session_integrity_sha256"] = _integrity_sha256(sealed)
    return deepcopy(sealed)


def _require_session(session: Any) -> dict[str, Any]:
    if not isinstance(session, Mapping):
        _fail("prepared_session_required", "session_integrity")
    checked = deepcopy(dict(session))
    if (
        checked.get("version") != GOVERNED_MEMORY_OPERATOR_SESSION_VERSION
        or checked.get("runtime_surface") != RUNTIME_SURFACE
        or checked.get("replacement_corpus_sha256")
        != checked.get("_evaluation", {}).get("corpus_sha256")
        or checked.get("_rule_lock_sha256") != _rule_lock_sha256()
        or checked.get("_session_integrity_sha256") != _integrity_sha256(checked)
        or checked.get("evidence_document_created") is not False
        or checked.get("continuation_authorized") is not False
        or checked.get("non_applied") is not True
        or checked.get("non_persisted") is not True
    ):
        _fail("session_integrity_invalid_or_modified", "session_integrity")
    try:
        _engine._require_evaluation(checked["_evaluation"])
    except Exception:
        _fail("locked_evaluation_invalid_or_modified", "session_integrity")
    return checked


def _terminal_outcome(input_fn, output_fn) -> str:
    output_fn(_outcome_choices())
    raw = input_fn("请输入结果编号或 machine value：").strip()
    if raw.isdigit() and 1 <= int(raw) <= len(_OUTCOMES):
        return _OUTCOMES[int(raw) - 1]
    return raw


def _terminal_reason_codes(input_fn) -> list[str]:
    raw = input_fn("请输入一个或多个 reason code（逗号分隔）：")
    return [item.strip() for item in raw.split(",") if item.strip()]


def _terminal_yes(value: Any) -> bool:
    return isinstance(value, str) and value.strip().lower() in {"是", "yes", "y", "true"}


def _terminal_score(input_fn) -> int:
    raw = input_fn("请输入 1 至 5 的整数评分：").strip()
    try:
        return int(raw)
    except ValueError:
        return 0


def _terminal_optional_glossary(session, trial_id, input_fn, output_fn, clock):
    if input_fn("输入 g 查看固定术语表，直接回车继续：").strip().lower() != "g":
        return session
    session = record_operator_scored_trial_event(
        session,
        trial_id=trial_id,
        event_type="GLOSSARY_OPENED",
        monotonic_ms=clock(),
    )["session"]
    output_fn(_reason_glossary())
    return record_operator_scored_trial_event(
        session,
        trial_id=trial_id,
        event_type="GLOSSARY_CLOSED",
        monotonic_ms=clock(),
    )["session"]


def _fail(code: str, stage: str, reasons: Any = ()) -> None:
    raise GovernedMemoryOperatorSessionError(code, stage, reasons)


__all__ = [
    "GovernedMemoryOperatorSessionError",
    "prepare_governed_memory_operator_session",
    "build_operator_practice_packet",
    "record_operator_practice_response",
    "start_governed_memory_operator_scored_session",
    "open_operator_scored_trial",
    "record_operator_scored_trial_event",
    "finalize_governed_memory_operator_session",
    "run_governed_memory_operator_session",
]
