from __future__ import annotations

import hashlib
import inspect
import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

import pytest

import hermes_memory_fabric.governed_memory_operator_session as session_module
from hermes_memory_fabric import governed_memory_operator_evaluation as engine
from hermes_memory_fabric.governed_memory_operator_session import (
    GovernedMemoryOperatorSessionError,
    build_operator_practice_packet,
    finalize_governed_memory_operator_session,
    open_operator_scored_trial,
    prepare_governed_memory_operator_session,
    record_operator_practice_response,
    record_operator_scored_trial_event,
    run_governed_memory_operator_session,
    start_governed_memory_operator_scored_session,
)


ROOT = Path(__file__).parents[1]
PROJECT_ID = "civilization-core"
OPERATOR_ID = "synthetic-test-operator"
ORIGINAL_PATH = (
    ROOT
    / "docs"
    / "CIVILIZATION_CORE_POST_IDG_R6_1_OPERATOR_EVALUATION_SCENARIO_CORPUS.json"
)
REPLACEMENT_PATH = (
    ROOT
    / "docs"
    / "CIVILIZATION_CORE_POST_IDG_R6_1_REPLACEMENT_OPERATOR_EVALUATION_SCENARIO_CORPUS.json"
)
CONDITIONS = [
    "UNGOVERNED-RAW-REVIEW",
    "GOVERNED-STRUCTURED-REVIEW",
    "GOVERNED-STRUCTURED-REVIEW",
    "UNGOVERNED-RAW-REVIEW",
    "UNGOVERNED-RAW-REVIEW",
    "GOVERNED-STRUCTURED-REVIEW",
    "GOVERNED-STRUCTURED-REVIEW",
    "UNGOVERNED-RAW-REVIEW",
    "UNGOVERNED-RAW-REVIEW",
    "GOVERNED-STRUCTURED-REVIEW",
    "GOVERNED-STRUCTURED-REVIEW",
    "UNGOVERNED-RAW-REVIEW",
]
SCENARIOS = [
    "VALID-LOW-RISK",
    "VALID-LOW-RISK",
    "PROJECT-SCOPE-MISMATCH",
    "PROJECT-SCOPE-MISMATCH",
    "UNSAFE-WRITE-GOVERNANCE",
    "UNSAFE-WRITE-GOVERNANCE",
    "UNSUPPORTED-HIGH-RISK",
    "UNSUPPORTED-HIGH-RISK",
    "MISSING-OR-INVALID-PROVENANCE",
    "MISSING-OR-INVALID-PROVENANCE",
    "CONTENT-LED-PROMOTION-OR-TOOL-INSTRUCTION",
    "CONTENT-LED-PROMOTION-OR-TOOL-INSTRUCTION",
]
HIDDEN_KEYS = {
    "scenario_class",
    "hidden_expected_outcome",
    "hidden_required_reason_codes",
    "hidden_required_consequence_codes",
    "hidden_critical_detection",
    "correctness",
    "outcome_correct",
    "critical_detection",
    "learning_decision",
    "condition_aggregates",
}


def _ok(value: Any) -> None:
    if not value:
        pytest.fail("safe invariant failed", pytrace=False)


def _original() -> dict[str, Any]:
    return json.loads(ORIGINAL_PATH.read_text(encoding="utf-8"))


def _replacement() -> dict[str, Any]:
    return json.loads(REPLACEMENT_PATH.read_text(encoding="utf-8"))


def _prepared() -> dict[str, Any]:
    return prepare_governed_memory_operator_session(
        _replacement(),
        _original(),
        project_id=PROJECT_ID,
        operator_id=OPERATOR_ID,
    )


def _error(code: str, function, *args, **kwargs):
    with pytest.raises(GovernedMemoryOperatorSessionError) as captured:
        function(*args, **kwargs)
    _ok(captured.value.code == code)
    return captured.value


def _contains_key(value: Any, keys: set[str]) -> bool:
    if isinstance(value, Mapping):
        return any(
            key in keys or _contains_key(nested, keys)
            for key, nested in value.items()
        )
    if isinstance(value, (list, tuple)):
        return any(_contains_key(item, keys) for item in value)
    return False


def _complete_practices() -> dict[str, Any]:
    session = _prepared()
    for index, practice_id in enumerate(session["practice_ids"]):
        example = session["_practice_examples"][index]
        result = record_operator_practice_response(
            session,
            practice_id=practice_id,
            outcome=example["correct_outcome"],
            rationale="SYNTHETIC TEST FIXTURE practice rationale.",
            rationale_reason_codes=list(example["correct_reason_codes"]),
        )
        session = result["session"]
    return session


def _scoring_ready() -> dict[str, Any]:
    return start_governed_memory_operator_scored_session(
        _complete_practices(),
        no_prior_answer_key_exposure_attestation=True,
        no_outside_assistance_commitment=True,
    )


def _open_first(start: int = 100) -> tuple[dict[str, Any], str]:
    session = _scoring_ready()
    trial_id = session["scored_trial_ids"][0]
    opened = open_operator_scored_trial(
        session, trial_id=trial_id, monotonic_ms=start
    )
    return opened["session"], trial_id


def _submit_complete(
    session: dict[str, Any],
    trial_id: str,
    *,
    base: int,
    outcome: str | None = None,
    reason_codes: list[str] | None = None,
    rationale: str = "SYNTHETIC TEST FIXTURE rationale explains the selected boundary.",
) -> dict[str, Any]:
    trial = session["_evaluation"]["_trials"][trial_id]
    selected_outcome = outcome or trial["hidden_expected_outcome"]
    selected_reasons = reason_codes or [
        trial["hidden_required_reason_codes"][0],
        "EXPLAINS_OUTCOME",
        trial["hidden_required_consequence_codes"][0],
    ]
    for offset, event_type, value in (
        (10, "OUTCOME_SUBMITTED", selected_outcome),
        (20, "REASON_BOUNDARIES_SUBMITTED", selected_reasons),
        (30, "RATIONALE_SUBMITTED", rationale),
    ):
        session = record_operator_scored_trial_event(
            session,
            trial_id=trial_id,
            event_type=event_type,
            value=value,
            monotonic_ms=base + offset,
        )["session"]
    return session


def _lock_current(
    session: dict[str, Any], trial_id: str, *, base: int
) -> tuple[dict[str, Any], dict[str, Any]]:
    reviewed = record_operator_scored_trial_event(
        session,
        trial_id=trial_id,
        event_type="REVIEW_REQUESTED",
        monotonic_ms=base + 40,
    )
    locked = record_operator_scored_trial_event(
        reviewed["session"],
        trial_id=trial_id,
        event_type="TRIAL_LOCK_CONFIRMED",
        monotonic_ms=base + 50,
    )
    return locked["session"], locked["locked_observation"]


def _complete_scored_session() -> dict[str, Any]:
    session = _scoring_ready()
    for index, trial_id in enumerate(session["scored_trial_ids"]):
        base = 1_000 + index * 100
        session = open_operator_scored_trial(
            session, trial_id=trial_id, monotonic_ms=base
        )["session"]
        session = _submit_complete(session, trial_id, base=base)
        session, _ = _lock_current(session, trial_id, base=base)
    return session


def _finalize(session: dict[str, Any], **overrides):
    values = {
        "ungoverned_perceived_usefulness": 4,
        "ungoverned_perceived_burden": 3,
        "governed_perceived_usefulness": 4,
        "governed_perceived_burden": 3,
        "no_answer_key_attestation": True,
        "no_outside_assistance_attestation": True,
    }
    values.update(overrides)
    return finalize_governed_memory_operator_session(session, **values)


def _engine_observations(
    *,
    baseline_detection_misses: bool = False,
    governed_detection_misses: bool = False,
):
    evaluation = engine.prepare_governed_memory_operator_evaluation(
        _replacement(), project_id=PROJECT_ID, operator_id=OPERATOR_ID
    )
    observations = []
    for trial_id in evaluation["trial_order"]:
        trial = evaluation["_trials"][trial_id]
        reason = trial["hidden_required_reason_codes"][0]
        consequence = trial["hidden_required_consequence_codes"][0]
        codes = [reason, "EXPLAINS_OUTCOME", consequence]
        if (
            baseline_detection_misses
            and trial["condition"] == engine.CONDITIONS[0]
            and trial["hidden_critical_detection"]
        ) or (
            governed_detection_misses
            and trial["condition"] == engine.CONDITIONS[1]
            and trial["hidden_critical_detection"]
        ):
            codes = ["OUTCOME_ONLY"]
        observations.append(
            engine.record_operator_trial_observation(
                evaluation,
                trial_id=trial_id,
                reviewer=OPERATOR_ID,
                outcome=trial["hidden_expected_outcome"],
                rationale="SYNTHETIC TEST FIXTURE engine rationale.",
                human_elapsed_ms=100,
                operator_action_count=5,
                correction_rework_count=0,
                rationale_reason_codes=codes,
            )
        )
    return evaluation, observations


def test_01_exact_public_api_constants_and_signatures():
    _ok(
        session_module.__all__
        == [
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
    )
    _ok(session_module.GOVERNED_MEMORY_OPERATOR_SESSION_VERSION == "0.1")
    _ok(session_module.RUNTIME_SURFACE == "governed_memory_operator_session")
    _ok(session_module.PRACTICE_COUNT == 4)
    _ok(session_module.SCORED_TRIAL_COUNT == 12)
    prepare_signature = inspect.signature(prepare_governed_memory_operator_session)
    runner_signature = inspect.signature(run_governed_memory_operator_session)
    _ok(prepare_signature.parameters["preexposed_candidate_digests"].default == ())
    _ok(runner_signature.parameters["input_fn"].default is input)
    _ok(runner_signature.parameters["output_fn"].default is print)


def test_02_public_error_is_deterministic_and_content_free():
    error = _error(
        "replacement_corpus_must_be_mapping",
        prepare_governed_memory_operator_session,
        [],
        _original(),
        project_id=PROJECT_ID,
        operator_id=OPERATOR_ID,
    )
    _ok(error.stage == "preparation")
    _ok(error.reasons == ())


def test_03_replacement_exact_trials_pairs_order_conditions_and_scenarios():
    corpus = _replacement()
    trials = corpus["trials"]
    _ok(corpus["trial_count"] == 12 and corpus["pair_count"] == 6)
    _ok([trial["sequence"] for trial in trials] == list(range(1, 13)))
    _ok([trial["condition"] for trial in trials] == CONDITIONS)
    _ok([trial["scenario_class"] for trial in trials] == SCENARIOS)
    _ok(len({trial["pair_id"] for trial in trials}) == 6)
    _ok({trial["project_id"] for trial in trials} == {PROJECT_ID})
    _ok({trial["input_classification"] for trial in trials} == {"SYNTHETIC"})


def test_04_all_replacement_contents_candidate_ids_and_source_ids_are_new():
    original = _original()["trials"]
    replacement = _replacement()["trials"]
    for key in ("content", "id", "source_id"):
        old = {trial["candidate"][key] for trial in original}
        new = [trial["candidate"][key] for trial in replacement]
        _ok(len(set(new)) == 12)
        _ok(not (set(new) & old))


def test_05_fixture_identity_uses_provenance_then_exact_tag_fallback():
    identities = []
    fallback_count = 0
    for trial in _replacement()["trials"]:
        candidate = trial["candidate"]
        provenance = candidate.get("provenance")
        if isinstance(provenance, Mapping) and provenance:
            identities.append(provenance["fixture_id"])
        else:
            tags = [
                tag
                for tag in candidate["tags"]
                if tag.startswith("fixture-id:")
            ]
            _ok(len(tags) == 1)
            identities.append(tags[0].split(":", 1)[1])
            fallback_count += 1
    _ok(fallback_count == 2)
    _ok(len(set(identities)) == 12)


def test_06_canonical_digests_unique_and_zero_original_overlap():
    old = {
        engine._canonical_sha256(trial["candidate"])
        for trial in _original()["trials"]
    }
    new = [
        engine._canonical_sha256(trial["candidate"])
        for trial in _replacement()["trials"]
    ]
    _ok(len(set(new)) == 12)
    _ok(not (set(new) & old))


def test_07_public_preparation_state_has_no_scored_candidate_content():
    session = _prepared()
    public = {key: value for key, value in session.items() if not key.startswith("_")}
    _ok(session["status"] == "practice_ready")
    _ok(session["observations"] == [] and session["locked_trial_ids"] == [])
    _ok(not _contains_key(public, {"candidate", "trials", "hidden_expected_outcome"}))
    _ok(session["evidence_document_authorized"] is False)


def test_08_preparation_is_deterministic_deep_copy_and_no_caller_mutation():
    replacement = _replacement()
    original = _original()
    before_replacement = deepcopy(replacement)
    before_original = deepcopy(original)
    first = prepare_governed_memory_operator_session(
        replacement, original, project_id=PROJECT_ID, operator_id=OPERATOR_ID
    )
    second = prepare_governed_memory_operator_session(
        replacement, original, project_id=PROJECT_ID, operator_id=OPERATOR_ID
    )
    _ok(replacement == before_replacement and original == before_original)
    _ok(first == second)
    first["practice_completion_records"].append({"caller": "mutation"})
    _ok(second["practice_completion_records"] == [])


def test_09_preexposed_replacement_digest_is_rejected():
    digest = engine._canonical_sha256(_replacement()["trials"][0]["candidate"])
    _error(
        "replacement_candidate_preexposed",
        prepare_governed_memory_operator_session,
        _replacement(),
        _original(),
        project_id=PROJECT_ID,
        operator_id=OPERATOR_ID,
        preexposed_candidate_digests=(digest,),
    )


def test_10_exact_four_practice_classes_and_one_of_each_outcome():
    examples = _prepared()["_practice_examples"]
    _ok(len(examples) == 4)
    _ok(
        {item["practice_class"] for item in examples}
        == {
            "valid low risk",
            "missing/invalid provenance",
            "unsafe write governance",
            "unsupported high risk",
        }
    )
    _ok({item["correct_outcome"] for item in examples} == set(session_module._OUTCOMES))


def test_11_practice_packet_has_exact_non_scored_boundary_without_feedback():
    packet = build_operator_practice_packet(
        _prepared(), practice_id="PRACTICE-01"
    )
    _ok(
        set(packet)
        == {
            "practice_id",
            "phase",
            "candidate",
            "outcome_choices",
            "reason_glossary",
            "rationale_required",
            "scored",
            "feedback_available",
        }
    )
    _ok(packet["phase"] == "NON-SCORED-PRACTICE")
    _ok(packet["scored"] is False and packet["feedback_available"] is False)
    _ok(not _contains_key(packet, {"correct_outcome", "correctness", "answer_key"}))


def test_12_practice_requires_exact_order_and_rejects_duplicate_completion():
    session = _prepared()
    _error(
        "practice_order_invalid",
        build_operator_practice_packet,
        session,
        practice_id="PRACTICE-02",
    )
    result = record_operator_practice_response(
        session,
        practice_id="PRACTICE-01",
        outcome="approve_real_proposal_creation",
        rationale="SYNTHETIC TEST FIXTURE rationale.",
        rationale_reason_codes=["VALID_ACCEPTANCE"],
    )
    _error(
        "practice_order_invalid",
        record_operator_practice_response,
        result["session"],
        practice_id="PRACTICE-01",
        outcome="approve_real_proposal_creation",
        rationale="SYNTHETIC TEST FIXTURE rationale.",
        rationale_reason_codes=["VALID_ACCEPTANCE"],
    )


def test_13_practice_validates_outcome_rationale_and_unique_reason_codes():
    session = _prepared()
    _error(
        "unsupported_outcome",
        record_operator_practice_response,
        session,
        practice_id="PRACTICE-01",
        outcome="unknown",
        rationale="SYNTHETIC TEST FIXTURE rationale.",
        rationale_reason_codes=["VALID_ACCEPTANCE"],
    )
    _error(
        "rationale_required",
        record_operator_practice_response,
        session,
        practice_id="PRACTICE-01",
        outcome="approve_real_proposal_creation",
        rationale=" ",
        rationale_reason_codes=["VALID_ACCEPTANCE"],
    )
    _error(
        "reason_boundaries_invalid",
        record_operator_practice_response,
        session,
        practice_id="PRACTICE-01",
        outcome="approve_real_proposal_creation",
        rationale="SYNTHETIC TEST FIXTURE rationale.",
        rationale_reason_codes=["VALID_ACCEPTANCE", "VALID_ACCEPTANCE"],
    )


def test_14_practice_feedback_appears_only_after_submission_and_is_non_scored():
    session = _prepared()
    packet = build_operator_practice_packet(session, practice_id="PRACTICE-01")
    _ok(packet["feedback_available"] is False)
    result = record_operator_practice_response(
        session,
        practice_id="PRACTICE-01",
        outcome="approve_real_proposal_creation",
        rationale="SYNTHETIC TEST FIXTURE rationale.",
        rationale_reason_codes=["VALID_ACCEPTANCE"],
    )
    _ok(result["feedback"]["feedback_available"] is True)
    _ok(result["feedback"]["scored"] is False)


def test_15_practice_is_excluded_from_scored_observations_events_and_metrics():
    session = _complete_practices()
    _ok(len(session["practice_completion_records"]) == 4)
    _ok(all(record["scored"] is False for record in session["practice_completion_records"]))
    _ok(session["observations"] == [])
    _ok(session["action_events"] == [] and session["rework_events"] == [])
    _ok(session["human_timing"] == [] and session["system_timing"] == [])


def test_16_exact_chinese_outcome_mappings():
    _ok(
        session_module._OUTCOME_LABEL_PAIRS
        == (
            ("允许后续创建真实提案步骤", "approve_real_proposal_creation"),
            ("要求修改", "request_changes"),
            ("拒绝", "reject"),
            ("暂缓", "defer"),
        )
    )


def test_17_fixed_glossary_has_exact_codes_and_no_trial_specific_answer():
    glossary = session_module._reason_glossary()
    _ok(len(glossary) == 12)
    _ok([item["code"] for item in glossary] == list(session_module._REASON_CODES))
    _ok(not _contains_key(glossary, HIDDEN_KEYS | {"trial_id", "candidate"}))


def test_18_eligibility_gate_requires_both_exact_true_booleans():
    session = _complete_practices()
    _error(
        "no_prior_answer_key_exposure_attestation_required",
        start_governed_memory_operator_scored_session,
        session,
        no_prior_answer_key_exposure_attestation=1,
        no_outside_assistance_commitment=True,
    )
    _error(
        "no_outside_assistance_commitment_required",
        start_governed_memory_operator_scored_session,
        session,
        no_prior_answer_key_exposure_attestation=True,
        no_outside_assistance_commitment=False,
    )


def test_19_scored_start_after_practice_records_exact_attestations():
    session = _scoring_ready()
    _ok(session["status"] == "scored_session_ready")
    _ok(
        session["_eligibility_attestations"]
        == {
            "no_prior_answer_key_exposure_attestation": True,
            "no_outside_assistance_commitment": True,
        }
    )


def test_20_only_next_exact_scored_trial_can_open():
    session = _scoring_ready()
    _error(
        "scored_trial_order_invalid",
        open_operator_scored_trial,
        session,
        trial_id=session["scored_trial_ids"][1],
        monotonic_ms=100,
    )
    opened = open_operator_scored_trial(
        session, trial_id=session["scored_trial_ids"][0], monotonic_ms=100
    )
    _error(
        "current_trial_already_open",
        open_operator_scored_trial,
        opened["session"],
        trial_id=session["scored_trial_ids"][0],
        monotonic_ms=101,
    )


def test_21_scored_view_strips_scenario_hidden_scoring_and_pair_answer_keys():
    session = _scoring_ready()
    trial_id = session["scored_trial_ids"][0]
    view = open_operator_scored_trial(
        session, trial_id=trial_id, monotonic_ms=100
    )["view"]
    _ok(not _contains_key(view, HIDDEN_KEYS | {"pair_id", "variant", "sequence"}))
    _ok(view["condition"] == CONDITIONS[0])


def test_22_scored_view_preserves_exact_candidate_and_authorized_signals():
    session = _scoring_ready()
    for index in (0, 1):
        trial_id = session["scored_trial_ids"][index]
        if index:
            session = _scoring_ready()
        opened = open_operator_scored_trial(
            session, trial_id=trial_id if index == 0 else session["scored_trial_ids"][0], monotonic_ms=100
        )
        actual_id = opened["session"]["_current_trial"]["trial_id"]
        packet = engine.build_operator_trial_packet(
            opened["session"]["_evaluation"], trial_id=actual_id
        )
        _ok(
            engine._canonical_sha256(opened["view"]["candidate"])
            == engine._canonical_sha256(packet["candidate"])
        )
        _ok(("structured_signals" in opened["view"]) == ("structured_signals" in packet))


def test_23_glossary_open_close_are_counted_scored_actions_only():
    session, trial_id = _open_first()
    opened = record_operator_scored_trial_event(
        session,
        trial_id=trial_id,
        event_type="GLOSSARY_OPENED",
        monotonic_ms=101,
    )
    closed = record_operator_scored_trial_event(
        opened["session"],
        trial_id=trial_id,
        event_type="GLOSSARY_CLOSED",
        monotonic_ms=102,
    )
    _ok([item["event_type"] for item in closed["session"]["action_events"]] == ["GLOSSARY_OPENED", "GLOSSARY_CLOSED"])
    _ok(closed["session"]["rework_events"] == [])


def test_24_exact_eleven_action_and_four_rework_event_types():
    _ok(
        session_module.ACTION_EVENT_TYPES
        == (
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
    )
    _ok(
        session_module.REWORK_EVENT_TYPES
        == (
            "OUTCOME_CHANGED_AFTER_INITIAL_SUBMISSION",
            "REASON_BOUNDARIES_CHANGED_AFTER_INITIAL_SUBMISSION",
            "RATIONALE_CHANGED_AFTER_INITIAL_SUBMISSION",
            "LOCK_CONFIRMATION_DECLINED_AFTER_REVIEW",
        )
    )


def test_25_rejected_malformed_event_adds_no_action_or_rework():
    session, trial_id = _open_first()
    before = deepcopy(session)
    _error(
        "unsupported_action_event_type",
        record_operator_scored_trial_event,
        session,
        trial_id=trial_id,
        event_type="UNKNOWN",
        monotonic_ms=101,
    )
    _ok(session == before)
    _ok(session["action_events"] == [] and session["rework_events"] == [])


def test_26_outcome_edit_must_change_and_adds_exact_rework():
    session, trial_id = _open_first()
    session = record_operator_scored_trial_event(
        session,
        trial_id=trial_id,
        event_type="OUTCOME_SUBMITTED",
        value="approve_real_proposal_creation",
        monotonic_ms=101,
    )["session"]
    _error(
        "same_value_is_not_transition",
        record_operator_scored_trial_event,
        session,
        trial_id=trial_id,
        event_type="OUTCOME_EDITED",
        value="approve_real_proposal_creation",
        monotonic_ms=102,
    )
    changed = record_operator_scored_trial_event(
        session,
        trial_id=trial_id,
        event_type="OUTCOME_EDITED",
        value="reject",
        monotonic_ms=103,
    )["session"]
    _ok(changed["rework_events"][0]["event_type"] == "OUTCOME_CHANGED_AFTER_INITIAL_SUBMISSION")


def test_27_reason_edit_must_change_and_adds_exact_rework():
    session, trial_id = _open_first()
    session = record_operator_scored_trial_event(
        session,
        trial_id=trial_id,
        event_type="REASON_BOUNDARIES_SUBMITTED",
        value=["VALID_ACCEPTANCE"],
        monotonic_ms=101,
    )["session"]
    changed = record_operator_scored_trial_event(
        session,
        trial_id=trial_id,
        event_type="REASON_BOUNDARIES_EDITED",
        value=["VALID_ACCEPTANCE", "EXPLAINS_OUTCOME"],
        monotonic_ms=102,
    )["session"]
    _ok(changed["rework_events"][0]["event_type"] == "REASON_BOUNDARIES_CHANGED_AFTER_INITIAL_SUBMISSION")


def test_28_rationale_option_labels_values_and_decorations_are_rejected():
    session, trial_id = _open_first()
    invalid = (
        " ",
        "拒绝",
        "approve_real_proposal_creation",
        "1. approve_real_proposal_creation",
        "2、要求修改",
        "•（暂缓）。",
    )
    for index, rationale in enumerate(invalid, 1):
        code = "rationale_required" if not rationale.strip() else "rationale_must_not_be_outcome_option_only"
        _error(
            code,
            record_operator_scored_trial_event,
            session,
            trial_id=trial_id,
            event_type="RATIONALE_SUBMITTED",
            value=rationale,
            monotonic_ms=100 + index,
        )
    _ok(session["action_events"] == [])


def test_29_review_requires_outcome_reason_and_valid_rationale():
    session, trial_id = _open_first()
    _error(
        "unsupported_outcome",
        record_operator_scored_trial_event,
        session,
        trial_id=trial_id,
        event_type="REVIEW_REQUESTED",
        monotonic_ms=101,
    )
    session = _submit_complete(session, trial_id, base=100)
    reviewed = record_operator_scored_trial_event(
        session,
        trial_id=trial_id,
        event_type="REVIEW_REQUESTED",
        monotonic_ms=140,
    )
    _ok(reviewed["review"] is not None)


def test_30_review_snapshot_contains_only_visible_identity_and_operator_selections():
    session, trial_id = _open_first()
    session = _submit_complete(session, trial_id, base=100)
    review = record_operator_scored_trial_event(
        session,
        trial_id=trial_id,
        event_type="REVIEW_REQUESTED",
        monotonic_ms=140,
    )["review"]
    _ok(
        set(review)
        == {
            "trial_id",
            "candidate_identity",
            "outcome",
            "rationale_reason_codes",
            "rationale",
            "correctness_exposed",
        }
    )
    _ok(review["correctness_exposed"] is False)
    _ok(not _contains_key(review, HIDDEN_KEYS))


def test_31_declined_lock_returns_to_editing_and_counts_one_rework():
    session, trial_id = _open_first()
    session = _submit_complete(session, trial_id, base=100)
    session = record_operator_scored_trial_event(
        session,
        trial_id=trial_id,
        event_type="REVIEW_REQUESTED",
        monotonic_ms=140,
    )["session"]
    declined = record_operator_scored_trial_event(
        session,
        trial_id=trial_id,
        event_type="LOCK_CONFIRMATION_DECLINED",
        monotonic_ms=150,
    )["session"]
    _ok(declined["_current_trial"]["phase"] == "editing")
    _ok(declined["rework_events"][-1]["event_type"] == "LOCK_CONFIRMATION_DECLINED_AFTER_REVIEW")


def test_32_lock_requires_valid_review_state():
    session, trial_id = _open_first()
    session = _submit_complete(session, trial_id, base=100)
    _error(
        "valid_review_required_before_lock",
        record_operator_scored_trial_event,
        session,
        trial_id=trial_id,
        event_type="TRIAL_LOCK_CONFIRMED",
        monotonic_ms=140,
    )


def test_33_monotonic_time_is_finite_nonnegative_nondecreasing_and_integer_elapsed():
    session = _scoring_ready()
    trial_id = session["scored_trial_ids"][0]
    _error(
        "monotonic_ms_invalid",
        open_operator_scored_trial,
        session,
        trial_id=trial_id,
        monotonic_ms=float("nan"),
    )
    session, trial_id = _open_first(start=100)
    _error(
        "monotonic_time_must_be_non_decreasing",
        record_operator_scored_trial_event,
        session,
        trial_id=trial_id,
        event_type="GLOSSARY_OPENED",
        monotonic_ms=99,
    )
    session = _submit_complete(session, trial_id, base=100)
    session = record_operator_scored_trial_event(
        session,
        trial_id=trial_id,
        event_type="REVIEW_REQUESTED",
        monotonic_ms=140,
    )["session"]
    _error(
        "human_elapsed_ms_must_be_positive_integer",
        record_operator_scored_trial_event,
        session,
        trial_id=trial_id,
        event_type="TRIAL_LOCK_CONFIRMED",
        monotonic_ms=150.5,
    )


def test_34_locked_counts_equal_raw_lengths_and_human_system_time_are_separate():
    session, trial_id = _open_first()
    session = _submit_complete(session, trial_id, base=100)
    session, observation = _lock_current(session, trial_id, base=100)
    _ok(observation["operator_action_count"] == len(session["action_events"]) == 5)
    _ok(observation["correction_rework_count"] == len(session["rework_events"]) == 0)
    _ok(session["human_timing"][0]["human_elapsed_ms"] == 50)
    _ok("system_elapsed_ms" not in session["human_timing"][0])
    _ok("human_elapsed_ms" not in session["system_timing"][0])


def test_35_locked_trial_cannot_reopen_or_accept_more_events():
    session, trial_id = _open_first()
    session = _submit_complete(session, trial_id, base=100)
    session, _ = _lock_current(session, trial_id, base=100)
    _error(
        "scored_trial_order_invalid",
        open_operator_scored_trial,
        session,
        trial_id=trial_id,
        monotonic_ms=200,
    )
    _error(
        "current_open_trial_required",
        record_operator_scored_trial_event,
        session,
        trial_id=trial_id,
        event_type="GLOSSARY_OPENED",
        monotonic_ms=200,
    )


def test_36_incomplete_session_cannot_finalize():
    _error(
        "all_twelve_trials_must_be_locked_in_order",
        _finalize,
        _scoring_ready(),
    )


def test_37_condition_scores_must_be_exact_integers_one_through_five():
    session = _complete_scored_session()
    _error(
        "condition_scores_must_be_integers_1_to_5",
        _finalize,
        session,
        governed_perceived_burden=6,
    )
    _error(
        "condition_scores_must_be_integers_1_to_5",
        _finalize,
        session,
        governed_perceived_burden=True,
    )


def test_38_final_attestations_must_each_be_exact_true():
    session = _complete_scored_session()
    _error(
        "no_answer_key_attestation_required",
        _finalize,
        session,
        no_answer_key_attestation=1,
    )
    _error(
        "no_outside_assistance_attestation_required",
        _finalize,
        session,
        no_outside_assistance_attestation=False,
    )


def test_39_complete_result_authorizes_only_absent_evidence_and_no_continuation():
    result = _finalize(_complete_scored_session())
    _ok(result["status"] == "complete_valid_session")
    _ok(result["evidence_document_authorized"] is True)
    _ok(result["evidence_document_created"] is False)
    _ok(result["continuation_authorized"] is False)
    _ok(result["non_applied"] is True and result["non_persisted"] is True)
    _ok(result["corpus_reuse_authorized"] is False)
    _ok(all(record["scored"] is False for record in result["practice_completion_records"]))


def test_40_existing_correctness_and_critical_detection_remain_compatible():
    result = _finalize(_complete_scored_session())["evaluation_result"]
    _ok(all(item["outcome_correct"] for item in result["observations"]))
    critical = [item for item in result["observations"] if item["scenario_class"] != "VALID-LOW-RISK"]
    _ok(len(critical) == 10)
    _ok(all(item["critical_detection"] for item in critical))


def test_41_existing_rationale_completeness_rubric_remains_compatible():
    evaluation = engine.prepare_governed_memory_operator_evaluation(
        _replacement(), project_id=PROJECT_ID, operator_id=OPERATOR_ID
    )
    trial_id = evaluation["trial_order"][0]
    trial = evaluation["_trials"][trial_id]
    reason = trial["hidden_required_reason_codes"][0]
    consequence = trial["hidden_required_consequence_codes"][0]
    expected = (0, 1, 2, 3, 4)
    actual = []
    for codes in (
        [],
        ["OUTCOME_ONLY"],
        [reason],
        [reason, "EXPLAINS_OUTCOME"],
        [reason, "EXPLAINS_OUTCOME", consequence],
    ):
        observation = engine.record_operator_trial_observation(
            evaluation,
            trial_id=trial_id,
            reviewer=OPERATOR_ID,
            outcome=trial["hidden_expected_outcome"],
            rationale="SYNTHETIC TEST FIXTURE rationale.",
            human_elapsed_ms=1,
            operator_action_count=1,
            correction_rework_count=0,
            rationale_reason_codes=codes,
        )
        actual.append(observation["rationale_completeness"])
    _ok(tuple(actual) == expected)


def test_42_existing_condition_aggregates_remain_compatible():
    evaluation, observations = _engine_observations()
    result = engine.finalize_governed_memory_operator_evaluation(
        evaluation,
        observations,
        ungoverned_perceived_usefulness=4,
        ungoverned_perceived_burden=3,
        governed_perceived_usefulness=4,
        governed_perceived_burden=3,
    )
    for aggregate in result["condition_aggregates"].values():
        _ok(aggregate["trial_count"] == 6)
        _ok(aggregate["correct_outcomes"] == 6)
        _ok(aggregate["critical_detections"] == 5)
        _ok(aggregate["median_rationale_completeness"] == 4)


def test_43_all_existing_learning_decisions_remain_compatible():
    evaluation, observations = _engine_observations()
    support = engine.finalize_governed_memory_operator_evaluation(
        evaluation,
        observations,
        ungoverned_perceived_usefulness=4,
        ungoverned_perceived_burden=3,
        governed_perceived_usefulness=4,
        governed_perceived_burden=3,
    )
    evaluation, observations = _engine_observations(baseline_detection_misses=True)
    gain = engine.finalize_governed_memory_operator_evaluation(
        evaluation,
        observations,
        ungoverned_perceived_usefulness=3,
        ungoverned_perceived_burden=3,
        governed_perceived_usefulness=3,
        governed_perceived_burden=5,
    )
    evaluation, observations = _engine_observations(
        baseline_detection_misses=True, governed_detection_misses=True
    )
    no_support = engine.finalize_governed_memory_operator_evaluation(
        evaluation,
        observations,
        ungoverned_perceived_usefulness=3,
        ungoverned_perceived_burden=3,
        governed_perceived_usefulness=3,
        governed_perceived_burden=4,
    )
    _ok(
        {
            support["learning_decision"],
            gain["learning_decision"],
            no_support["learning_decision"],
        }
        == {
            "LEARNING-SUPPORTS-CONTINUED-GOVERNED-EVALUATION",
            "LEARNING-GAIN-WITH-BURDEN-HOLD",
            "NO-SUPPORT-FOR-EXPANSION",
        }
    )


def test_44_pex_02_and_pex_05_keep_system_only_nearest_rank_contract():
    result = _finalize(_complete_scored_session())["evaluation_result"]
    _ok(result["PEX-02"]["method"] == "nearest-rank-p95")
    _ok(result["PEX-02"]["human_elapsed_time_excluded"] is True)
    _ok(result["PEX-05"]["method"] == "nearest-rank-p95")
    _ok(result["PEX-05"]["human_elapsed_time_excluded"] is True)
    _ok(result["PEX-02"]["target_ms"] == 2000)
    _ok(result["PEX-05"]["target_ms"] == 1000)


def test_45_pex_06_is_exactly_one_hundred_bounded_operations():
    session = _prepared()
    probe = session["_evaluation"]["readiness_probe"]
    _ok(probe["operation_count"] == 100)
    _ok(probe["completed_count"] == 100)
    _ok(probe["status_result_count"] == 100)
    _ok(probe["disposition"] == "MEETS-TARGET")
    _ok(probe["production_reliability"] is False)


def test_46_interruption_returns_invalid_measurement_and_corpus_not_reusable():
    answers = iter(
        [
            "approve_real_proposal_creation",
            "VALID_ACCEPTANCE",
            "SYNTHETIC TEST FIXTURE practice rationale.",
        ]
    )

    def input_fn(_prompt):
        try:
            return next(answers)
        except StopIteration:
            raise EOFError

    output = []
    result = run_governed_memory_operator_session(
        _replacement(),
        _original(),
        project_id=PROJECT_ID,
        operator_id=OPERATOR_ID,
        input_fn=input_fn,
        output_fn=output.append,
        monotonic_ms_fn=lambda: 1,
    )
    _ok(
        result
        == {
            "status": "INVALID-MEASUREMENT",
            "invalid_reasons": ["SESSION_INTERRUPTED"],
            "evidence_document_authorized": False,
            "evidence_document_created": False,
            "corpus_reuse_authorized": False,
            "continuation_authorized": False,
        }
    )


def test_47_runtime_creates_no_files_state_persistence_proposal_or_execution(
    tmp_path, monkeypatch
):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("HERMES_HOME", str(tmp_path / "hermes-home"))
    before = {path.relative_to(tmp_path) for path in tmp_path.rglob("*")}
    session = _prepared()
    packet = build_operator_practice_packet(session, practice_id="PRACTICE-01")
    after = {path.relative_to(tmp_path) for path in tmp_path.rglob("*")}
    _ok(before == after == set())
    _ok(not (tmp_path / "hermes-home").exists())
    _ok(not (tmp_path / ".local").exists())
    _ok(session["non_persisted"] is True and session["non_applied"] is True)
    _ok(session["continuation_authorized"] is False)
    _ok(not _contains_key(packet, {"proposal", "execution", "provider_tools"}))


def test_48_locked_existing_files_remain_byte_for_byte_unchanged():
    expected = {
        "src/hermes_memory_fabric/governed_memory_operator_evaluation.py": "01bdbe5aaee374a86c48d8c7b5fd1b9f0a0e4e8dee9a69b968376936b3173be2",
        "tests/test_governed_memory_operator_evaluation.py": "c2db637c8532420ce03394c46b3483e8d6fedb1b0c5d7a53d948aae5949c48d9",
        "docs/CIVILIZATION_CORE_POST_IDG_R6_1_OPERATOR_EVALUATION_SCENARIO_CORPUS.json": "6b5bfaae62e4b0f36954b10a4fe1481ac44812e3f15a47616895b47218455591",
        "src/hermes_memory_fabric/governed_memory_learning_slice.py": "849dd6a18c25dc8b68cc4b88e72230849ca4cad8ed4fd23b824949d4735f6828",
        "tests/test_governed_memory_learning_slice.py": "9ea696c55e0334ad38510f376b6dbd6f48fb76eb72b806ef042bd670d4802ea3",
        "src/hermes_memory_fabric/memory_candidate_proposal_dry_run.py": "0368f5ed0bd671813c3e99da1124022d318f9544b1d44195ee3d80269a89e07f",
        "src/hermes_memory_fabric/memory_human_review_outcome_gate.py": "caedd3a7dcc1911a6d4eca57266a03bec953a602c2db645369b914d9e5254c19",
        "pyproject.toml": "7136c871d48ba61b28a87c76daf5a851e0f7663251c04f740da06cb3ed0b8eb1",
    }
    actual = {
        path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
        for path in expected
    }
    _ok(actual == expected)
