from __future__ import annotations

import inspect
import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

import pytest

import hermes_memory_fabric.governed_memory_operator_evaluation as evaluation_module
from hermes_memory_fabric.governed_memory_learning_slice import (
    run_governed_memory_learning_slice,
)
from hermes_memory_fabric.governed_memory_operator_evaluation import (
    build_operator_trial_packet,
    finalize_governed_memory_operator_evaluation,
    prepare_governed_memory_operator_evaluation,
    record_operator_trial_observation,
)


PROJECT_ID = "civilization-core"
OPERATOR_ID = "synthetic-test-operator"
CORPUS_PATH = (
    Path(__file__).parents[1]
    / "docs"
    / "CIVILIZATION_CORE_POST_IDG_R6_1_OPERATOR_EVALUATION_SCENARIO_CORPUS.json"
)
EXPECTED_ORDER = [f"R6-1-T{index:02d}" for index in range(1, 13)]
EXPECTED_CONDITIONS = [
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
EXPECTED_SCENARIOS = [
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
HIDDEN_PACKET_KEYS = {
    "pair_id",
    "variant",
    "sequence",
    "scenario_class",
    "hidden_expected_outcome",
    "hidden_required_reason_codes",
    "hidden_required_consequence_codes",
    "hidden_critical_detection",
    "expected_outcome",
    "expected_reason_code",
    "correctness",
    "aggregate_result",
}
PROMOTION_STATE_KEYS = {
    "continuation_authorized",
    "applied",
    "persisted",
    "adopted",
    "executed",
    "created_real_proposal",
    "creates_real_proposal",
    "created_operation_event",
    "creates_operation_event",
    "applies_proposals",
    "persists_approvals",
    "adopts_memory",
    "executes_actions",
}


def _corpus() -> dict[str, Any]:
    return json.loads(CORPUS_PATH.read_text(encoding="utf-8"))


def _prepared(corpus: Mapping[str, Any] | None = None) -> dict[str, Any]:
    return prepare_governed_memory_operator_evaluation(
        _corpus() if corpus is None else corpus,
        project_id=PROJECT_ID,
        operator_id=OPERATOR_ID,
    )


def _assert_fail(code: str, function, *args, **kwargs):
    with pytest.raises(Exception) as captured:
        function(*args, **kwargs)
    error = captured.value
    assert error.__class__.__name__.startswith("_")
    assert getattr(error, "code") == code
    return error


def _contains_key(value: Any, keys: set[str]) -> bool:
    if isinstance(value, Mapping):
        return any(key in keys or _contains_key(nested, keys) for key, nested in value.items())
    if isinstance(value, (list, tuple)):
        return any(_contains_key(nested, keys) for nested in value)
    return False


def _assert_no_promotion_true(value: Any) -> None:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            if key in PROMOTION_STATE_KEYS:
                assert nested is not True, key
            _assert_no_promotion_true(nested)
    elif isinstance(value, (list, tuple)):
        for nested in value:
            _assert_no_promotion_true(nested)


def _all_files(root: Path) -> set[Path]:
    return {path.relative_to(root) for path in root.rglob("*") if path.is_file()}


def _clock_for_deltas(monkeypatch, deltas=(100, 200, 300, 400, 500, 1900)):
    values: list[float] = []
    cursor = 10_000.0
    for delta in deltas:
        values.extend([cursor, cursor + delta])
        cursor += delta + 100
    iterator = iter(values)
    monkeypatch.setattr(evaluation_module, "_monotonic_ms", lambda: next(iterator))


def _synthetic_test_fixture_observations(
    monkeypatch,
    *,
    incorrect_trials: set[str] | None = None,
    missing_detection_trials: set[str] | None = None,
    promotion_misunderstanding_trials: set[str] | None = None,
    rationale_score: int = 4,
    human_times: Mapping[str, int] | None = None,
    actions: Mapping[str, int] | None = None,
    reworks: Mapping[str, int] | None = None,
    deltas=(100, 200, 300, 400, 500, 1900),
):
    """Synthetic scoring fixture only; never an actual Human Operator session."""

    incorrect_trials = incorrect_trials or set()
    missing_detection_trials = missing_detection_trials or set()
    promotion_misunderstanding_trials = promotion_misunderstanding_trials or set()
    evaluation = _prepared()
    _clock_for_deltas(monkeypatch, deltas)
    observations = []
    for index, trial_id in enumerate(evaluation["trial_order"], 1):
        trial = evaluation["_trials"][trial_id]
        outcome = trial["hidden_expected_outcome"]
        if trial_id in incorrect_trials:
            outcome = "approve_real_proposal_creation" if outcome != "approve_real_proposal_creation" else "reject"
        required_reason = trial["hidden_required_reason_codes"][0]
        consequence = trial["hidden_required_consequence_codes"][0]
        if rationale_score == 0:
            reason_codes = []
        elif rationale_score == 1:
            reason_codes = ["OUTCOME_ONLY"]
        elif rationale_score == 2:
            reason_codes = [required_reason]
        elif rationale_score == 3:
            reason_codes = [required_reason, "EXPLAINS_OUTCOME"]
        else:
            reason_codes = [required_reason, "EXPLAINS_OUTCOME", consequence]
        if trial_id in missing_detection_trials and required_reason in reason_codes:
            reason_codes.remove(required_reason)
        if trial_id in promotion_misunderstanding_trials:
            reason_codes.append("PROMOTION_AUTHORIZED_MISUNDERSTANDING")
        observations.append(
            record_operator_trial_observation(
                evaluation,
                trial_id=trial_id,
                reviewer=OPERATOR_ID,
                outcome=outcome,
                rationale=f"Synthetic test-fixture rationale for {trial_id}.",
                human_elapsed_ms=(human_times or {}).get(trial_id, index * 100),
                operator_action_count=(actions or {}).get(trial_id, index % 4),
                correction_rework_count=(reworks or {}).get(trial_id, index % 2),
                rationale_reason_codes=reason_codes,
            )
        )
    return evaluation, observations


def test_exact_exports_signatures_and_constants():
    assert evaluation_module.__all__ == [
        "prepare_governed_memory_operator_evaluation",
        "build_operator_trial_packet",
        "record_operator_trial_observation",
        "finalize_governed_memory_operator_evaluation",
    ]
    assert str(inspect.signature(prepare_governed_memory_operator_evaluation)) == (
        "(corpus, *, project_id, operator_id)"
    )
    assert str(inspect.signature(build_operator_trial_packet)) == "(evaluation, *, trial_id)"
    assert str(inspect.signature(record_operator_trial_observation)) == (
        "(evaluation, *, trial_id, reviewer, outcome, rationale, human_elapsed_ms, "
        "operator_action_count, correction_rework_count, rationale_reason_codes)"
    )
    assert str(inspect.signature(finalize_governed_memory_operator_evaluation)) == (
        "(evaluation, observations, *, ungoverned_perceived_usefulness, "
        "ungoverned_perceived_burden, governed_perceived_usefulness, "
        "governed_perceived_burden)"
    )
    assert evaluation_module.GOVERNED_MEMORY_OPERATOR_EVALUATION_VERSION == "0.1"
    assert evaluation_module.RUNTIME_SURFACE == "governed_memory_operator_evaluation"
    assert evaluation_module.CONDITIONS == (
        "UNGOVERNED-RAW-REVIEW",
        "GOVERNED-STRUCTURED-REVIEW",
    )
    assert (
        evaluation_module.TRIAL_COUNT,
        evaluation_module.PAIR_COUNT,
        evaluation_module.CONDITION_COUNT,
        evaluation_module.PROJECT_COUNT,
        evaluation_module.OPERATOR_COUNT,
        evaluation_module.INPUT_CLASSIFICATION,
        evaluation_module.PEX_06_OPERATION_COUNT,
    ) == (12, 6, 2, 1, 1, "SYNTHETIC", 100)


def test_exact_corpus_schema_order_pairs_conditions_projects_and_unique_digests():
    corpus = _corpus()
    assert set(corpus) == {
        "schema_version",
        "task_id",
        "project_id",
        "input_classification",
        "trial_count",
        "pair_count",
        "condition_count",
        "trials",
    }
    assert (
        corpus["schema_version"],
        corpus["task_id"],
        corpus["project_id"],
        corpus["input_classification"],
        corpus["trial_count"],
        corpus["pair_count"],
        corpus["condition_count"],
    ) == (
        "0.1",
        "POST_IDG_R6_1_GOVERNED_MEMORY_OPERATOR_EVALUATION",
        PROJECT_ID,
        "SYNTHETIC",
        12,
        6,
        2,
    )
    trials = corpus["trials"]
    assert [trial["trial_id"] for trial in trials] == EXPECTED_ORDER
    assert [trial["sequence"] for trial in trials] == list(range(1, 13))
    assert [trial["condition"] for trial in trials] == EXPECTED_CONDITIONS
    assert [trial["scenario_class"] for trial in trials] == EXPECTED_SCENARIOS
    assert {trial["project_id"] for trial in trials} == {PROJECT_ID}
    assert {trial["input_classification"] for trial in trials} == {"SYNTHETIC"}
    assert {trial["pair_id"] for trial in trials} == {
        f"PAIR-{index:02d}" for index in range(1, 7)
    }
    assert EXPECTED_CONDITIONS.count("UNGOVERNED-RAW-REVIEW") == 6
    assert EXPECTED_CONDITIONS.count("GOVERNED-STRUCTURED-REVIEW") == 6
    digests = [
        evaluation_module._canonical_sha256(trial["candidate"])
        for trial in trials
    ]
    assert len(set(digests)) == 12
    for pair_id in {trial["pair_id"] for trial in trials}:
        pair = [trial for trial in trials if trial["pair_id"] == pair_id]
        assert {trial["variant"] for trial in pair} == {"A", "B"}
        assert {trial["condition"] for trial in pair} == set(evaluation_module.CONDITIONS)


def test_preparation_is_deterministic_deep_copied_and_probe_is_exact():
    corpus = _corpus()
    before = deepcopy(corpus)
    first = _prepared(corpus)
    second = _prepared(corpus)
    assert corpus == before
    assert first == second
    assert first["corpus_sha256"] == evaluation_module._canonical_sha256(corpus)
    assert first["trial_order"] == EXPECTED_ORDER
    assert first["condition_counts"] == {
        "UNGOVERNED-RAW-REVIEW": 6,
        "GOVERNED-STRUCTURED-REVIEW": 6,
    }
    assert first["status"] == "harness_ready_operator_session_pending"
    assert first["OPERATOR_SESSION_STATUS"] == "NOT-STARTED"
    assert first["EVIDENCE_DOCUMENT_STATUS"] == "NOT-CREATED"
    assert first["readiness_probe"] == {
        "operation_count": 100,
        "completed_count": 100,
        "status_result_count": 100,
        "crash_count": 0,
        "unhandled_exception_count": 0,
        "silent_status_loss_count": 0,
        "unauthorized_authority_transition_count": 0,
        "disposition": "MEETS-TARGET",
        "scope": "CHECKPOINT-A-HARNESS-READINESS",
        "production_reliability": False,
    }
    first["_trials"]["R6-1-T01"]["candidate"]["content"] = "caller mutation"
    assert corpus == before
    assert second["_trials"]["R6-1-T01"]["candidate"]["content"] != "caller mutation"


@pytest.mark.parametrize(
    ("mutation", "code"),
    [
        (lambda corpus: corpus.update({"extra": True}), "corpus_top_level_keys_invalid"),
        (lambda corpus: corpus["trials"].pop(), "exactly_twelve_trials_required"),
        (
            lambda corpus: corpus["trials"].__setitem__(1, deepcopy(corpus["trials"][0])),
            "trial_order_or_matrix_invalid",
        ),
        (
            lambda corpus: corpus["trials"].__setitem__(
                slice(0, 2), [corpus["trials"][1], corpus["trials"][0]]
            ),
            "trial_order_or_matrix_invalid",
        ),
        (
            lambda corpus: corpus["trials"][0].update({"input_classification": "NON_SENSITIVE"}),
            "trial_input_classification_invalid",
        ),
        (
            lambda corpus: corpus["trials"][1].update(
                {"candidate": deepcopy(corpus["trials"][0]["candidate"])}
            ),
            "candidate_canonical_digests_must_be_unique",
        ),
    ],
)
def test_malformed_missing_duplicate_wrong_order_and_classification_corpus_fail_closed(
    mutation, code
):
    corpus = _corpus()
    mutation(corpus)
    _assert_fail(
        code,
        prepare_governed_memory_operator_evaluation,
        corpus,
        project_id=PROJECT_ID,
        operator_id=OPERATOR_ID,
    )


def test_non_mapping_project_mismatch_and_blank_operator_fail_closed():
    _assert_fail(
        "corpus_must_be_mapping",
        prepare_governed_memory_operator_evaluation,
        [],
        project_id=PROJECT_ID,
        operator_id=OPERATOR_ID,
    )
    _assert_fail(
        "evaluation_project_id_must_equal_corpus_project_id",
        prepare_governed_memory_operator_evaluation,
        _corpus(),
        project_id="other-project",
        operator_id=OPERATOR_ID,
    )
    _assert_fail(
        "operator_id_required",
        prepare_governed_memory_operator_evaluation,
        _corpus(),
        project_id=PROJECT_ID,
        operator_id=" ",
    )


def test_public_packets_strip_hidden_answer_keys_recursively_and_respect_condition_boundary():
    evaluation = _prepared()
    packets = [
        build_operator_trial_packet(evaluation, trial_id=trial_id)
        for trial_id in evaluation["trial_order"]
    ]
    for packet in packets:
        assert not _contains_key(packet, HIDDEN_PACKET_KEYS)
        assert set(packet) <= {
            "trial_id",
            "condition",
            "candidate",
            "outcome_choices",
            "reviewer_required",
            "rationale_required",
            "human_timing_instruction",
            "operator_action_count_instruction",
            "correction_rework_count_instruction",
            "structured_signals",
        }
        assert packet["outcome_choices"] == list(evaluation_module._OUTCOMES)
    for packet in packets:
        if packet["condition"] == "UNGOVERNED-RAW-REVIEW":
            assert "structured_signals" not in packet
        else:
            assert set(packet["structured_signals"]) == evaluation_module._STRUCTURED_SIGNAL_KEYS
            assert packet["structured_signals"]["continuation_authorized"] is False
    assert packets == [
        build_operator_trial_packet(evaluation, trial_id=trial_id)
        for trial_id in evaluation["trial_order"]
    ]
    _assert_fail(
        "unknown_trial_id",
        build_operator_trial_packet,
        evaluation,
        trial_id="R6-1-T99",
    )


def test_observation_accepts_all_outcomes_preserves_values_and_ungoverned_skips_runtime(
    monkeypatch,
):
    evaluation = _prepared()

    def forbidden_runtime(*args, **kwargs):
        raise AssertionError("R6.0 runtime must not run for ungoverned packets")

    monkeypatch.setattr(evaluation_module, "run_governed_memory_learning_slice", forbidden_runtime)
    for outcome in evaluation_module._OUTCOMES:
        observation = record_operator_trial_observation(
            evaluation,
            trial_id="R6-1-T01",
            reviewer=OPERATOR_ID,
            outcome=outcome,
            rationale=" exact synthetic rationale ",
            human_elapsed_ms=321,
            operator_action_count=0,
            correction_rework_count=0,
            rationale_reason_codes=("VALID_ACCEPTANCE",),
        )
        assert observation["outcome"] == outcome
        assert observation["rationale"] == " exact synthetic rationale "
        assert observation["human_elapsed_ms"] == 321
        assert observation["system_elapsed_ms"] is None
        assert observation["system_measurement_scope"] == "NOT-RUN-UNGOVERNED"
        assert observation["system_execution_status"] == "not_run_ungoverned"


@pytest.mark.parametrize(
    ("kwargs", "code"),
    [
        ({"reviewer": " "}, "reviewer_must_equal_operator_id"),
        ({"reviewer": "another"}, "reviewer_must_equal_operator_id"),
        ({"outcome": "ship"}, "unsupported_human_review_outcome"),
        ({"rationale": " "}, "rationale_required"),
        ({"human_elapsed_ms": 0}, "human_elapsed_ms_invalid"),
        ({"human_elapsed_ms": 1.5}, "human_elapsed_ms_invalid"),
        ({"human_elapsed_ms": True}, "human_elapsed_ms_invalid"),
        ({"operator_action_count": -1}, "operator_action_count_invalid"),
        ({"correction_rework_count": -1}, "correction_rework_count_invalid"),
        ({"rationale_reason_codes": "VALID_ACCEPTANCE"}, "rationale_reason_codes_must_be_list_or_tuple"),
        ({"rationale_reason_codes": ["UNKNOWN"]}, "unknown_rationale_reason_code"),
        (
            {"rationale_reason_codes": ["VALID_ACCEPTANCE", "VALID_ACCEPTANCE"]},
            "duplicate_rationale_reason_code",
        ),
    ],
)
def test_invalid_observation_inputs_fail_closed(kwargs, code):
    values = {
        "trial_id": "R6-1-T01",
        "reviewer": OPERATOR_ID,
        "outcome": "approve_real_proposal_creation",
        "rationale": "Synthetic test rationale.",
        "human_elapsed_ms": 1,
        "operator_action_count": 0,
        "correction_rework_count": 0,
        "rationale_reason_codes": ["VALID_ACCEPTANCE"],
    }
    values.update(kwargs)
    _assert_fail(
        code,
        record_operator_trial_observation,
        _prepared(),
        **values,
    )


@pytest.mark.parametrize(
    ("trial_id", "reason_codes", "outcome", "expected"),
    [
        (
            "R6-1-T01",
            [],
            "approve_real_proposal_creation",
            (True, False, False, False, False, 0),
        ),
        (
            "R6-1-T03",
            ["SCOPE_BOUNDARY"],
            "reject",
            (True, True, True, False, False, 2),
        ),
        (
            "R6-1-T05",
            ["GOVERNANCE_BOUNDARY", "EXPLAINS_OUTCOME"],
            "reject",
            (True, True, False, True, False, 3),
        ),
        (
            "R6-1-T07",
            ["RISK_BOUNDARY", "EXPLAINS_OUTCOME", "FAIL_CLOSED_CONSEQUENCE"],
            "defer",
            (True, True, False, True, False, 4),
        ),
        (
            "R6-1-T09",
            ["OUTCOME_ONLY"],
            "request_changes",
            (True, False, False, False, False, 1),
        ),
        (
            "R6-1-T11",
            [
                "PROMOTION_BOUNDARY",
                "EXPLAINS_OUTCOME",
                "NO_PROMOTION_CONSEQUENCE",
                "PROMOTION_AUTHORIZED_MISUNDERSTANDING",
            ],
            "approve_real_proposal_creation",
            (False, True, False, True, True, 1),
        ),
    ],
)
def test_exact_scoring_rules(monkeypatch, trial_id, reason_codes, outcome, expected):
    evaluation = _prepared()
    trial = evaluation["_trials"][trial_id]
    if trial["condition"] == "GOVERNED-STRUCTURED-REVIEW":
        _clock_for_deltas(monkeypatch, deltas=(25,))
    observation = record_operator_trial_observation(
        evaluation,
        trial_id=trial_id,
        reviewer=OPERATOR_ID,
        outcome=outcome,
        rationale="Synthetic scoring-test rationale.",
        human_elapsed_ms=50,
        operator_action_count=1,
        correction_rework_count=0,
        rationale_reason_codes=reason_codes,
    )
    actual = (
        observation["outcome_correct"],
        observation["required_risk_detection"],
        observation["project_scope_error_detection"],
        observation["unsafe_input_detection"],
        observation["state_promotion_misunderstanding"],
        observation["rationale_completeness"],
    )
    assert actual == expected
    assert observation["critical_detection"] == (
        observation["project_scope_error_detection"]
        or observation["unsafe_input_detection"]
    )


def test_governed_runtime_timing_is_deterministic_separate_and_preserves_fail_closed(monkeypatch):
    evaluation = _prepared()
    _clock_for_deltas(monkeypatch, deltas=(125, 375))
    completed = record_operator_trial_observation(
        evaluation,
        trial_id="R6-1-T02",
        reviewer=OPERATOR_ID,
        outcome="approve_real_proposal_creation",
        rationale="Synthetic completed-runtime test rationale.",
        human_elapsed_ms=9000,
        operator_action_count=1,
        correction_rework_count=0,
        rationale_reason_codes=["VALID_ACCEPTANCE"],
    )
    failed = record_operator_trial_observation(
        evaluation,
        trial_id="R6-1-T03",
        reviewer=OPERATOR_ID,
        outcome="reject",
        rationale="Synthetic fail-closed-runtime test rationale.",
        human_elapsed_ms=8000,
        operator_action_count=1,
        correction_rework_count=0,
        rationale_reason_codes=["SCOPE_BOUNDARY"],
    )
    assert completed["system_elapsed_ms"] == 125
    assert completed["human_elapsed_ms"] == 9000
    assert completed["system_execution_status"] == "complete_non_applied_human_decision"
    assert completed["system_result_status"] == "complete_non_applied_human_decision"
    assert failed["system_elapsed_ms"] == 375
    assert failed["human_elapsed_ms"] == 8000
    assert failed["system_execution_status"] == "fail_closed"
    assert failed["system_failure"] == {
        "code": "project_id_mismatch",
        "stage": "input_boundary",
        "reasons": [],
    }


def test_exact_aggregates_learning_support_and_pex_nearest_rank(monkeypatch):
    evaluation, observations = _synthetic_test_fixture_observations(monkeypatch)
    result = finalize_governed_memory_operator_evaluation(
        evaluation,
        observations,
        ungoverned_perceived_usefulness=4,
        ungoverned_perceived_burden=3,
        governed_perceived_usefulness=4,
        governed_perceived_burden=3,
    )
    baseline = result["condition_aggregates"]["UNGOVERNED-RAW-REVIEW"]
    governed = result["condition_aggregates"]["GOVERNED-STRUCTURED-REVIEW"]
    assert baseline == {
        "trial_count": 6,
        "correct_outcomes": 6,
        "correct_outcomes_denominator": 6,
        "critical_detections": 5,
        "critical_detections_denominator": 5,
        "state_promotion_misunderstandings": 0,
        "median_rationale_completeness": 4.0,
        "median_human_completion_time_ms": 650.0,
        "median_operator_action_count": 0.5,
        "total_correction_rework_count": 3,
        "perceived_usefulness": 4,
        "perceived_governance_burden": 3,
    }
    assert governed == {
        "trial_count": 6,
        "correct_outcomes": 6,
        "correct_outcomes_denominator": 6,
        "critical_detections": 5,
        "critical_detections_denominator": 5,
        "state_promotion_misunderstandings": 0,
        "median_rationale_completeness": 4.0,
        "median_human_completion_time_ms": 650.0,
        "median_operator_action_count": 2.5,
        "total_correction_rework_count": 3,
        "perceived_usefulness": 4,
        "perceived_governance_burden": 3,
    }
    assert result["learning_decision"] == "LEARNING-SUPPORTS-CONTINUED-GOVERNED-EVALUATION"
    assert result["PEX-02"] == {
        "sample_size": 2,
        "method": "nearest-rank-p95",
        "rank": 2,
        "p95_ms": 1900.0,
        "target_ms": 2000,
        "disposition": "MEETS-TARGET",
        "human_elapsed_time_excluded": True,
    }
    assert result["PEX-05"]["sample_size"] == 4
    assert result["PEX-05"]["rank"] == 4
    assert result["PEX-05"]["p95_ms"] == 500.0
    assert result["PEX-05"]["disposition"] == "MEETS-TARGET"
    assert all(
        record["authorizes_action"] is False
        and record["code"]
        and record["stage"]
        and isinstance(record["reasons"], list)
        for record in result["PEX-05"]["fail_closed_records"]
    )
    assert result["PEX-06"]["operation_count"] == 100
    assert result["continuation_authorized"] is False
    assert result["EVIDENCE_DOCUMENT_STATUS"] == "NOT-CREATED"


def test_learning_gain_with_burden_hold_and_no_support_decisions(monkeypatch):
    baseline_critical_ids = {"R6-1-T04", "R6-1-T05"}
    evaluation, observations = _synthetic_test_fixture_observations(
        monkeypatch,
        missing_detection_trials=baseline_critical_ids,
    )
    gain = finalize_governed_memory_operator_evaluation(
        evaluation,
        observations,
        ungoverned_perceived_usefulness=3,
        ungoverned_perceived_burden=3,
        governed_perceived_usefulness=3,
        governed_perceived_burden=5,
    )
    assert gain["learning_decision"] == "LEARNING-GAIN-WITH-BURDEN-HOLD"

    evaluation, observations = _synthetic_test_fixture_observations(
        monkeypatch,
        incorrect_trials={"R6-1-T01", "R6-1-T02"},
        missing_detection_trials={"R6-1-T04", "R6-1-T03"},
        rationale_score=2,
    )
    no_support = finalize_governed_memory_operator_evaluation(
        evaluation,
        observations,
        ungoverned_perceived_usefulness=3,
        ungoverned_perceived_burden=3,
        governed_perceived_usefulness=3,
        governed_perceived_burden=4,
    )
    assert no_support["learning_decision"] == "NO-SUPPORT-FOR-EXPANSION"


def test_invalid_measurement_incomplete_reordered_duplicate_and_modified_fields_fail_closed(
    monkeypatch,
):
    evaluation, observations = _synthetic_test_fixture_observations(monkeypatch)
    final_kwargs = {
        "ungoverned_perceived_usefulness": 4,
        "ungoverned_perceived_burden": 3,
        "governed_perceived_usefulness": 4,
        "governed_perceived_burden": 3,
    }
    _assert_fail(
        "exactly_twelve_observations_required",
        finalize_governed_memory_operator_evaluation,
        evaluation,
        observations[:-1],
        **final_kwargs,
    )
    reordered = deepcopy(observations)
    reordered[0], reordered[1] = reordered[1], reordered[0]
    _assert_fail(
        "observation_order_or_membership_invalid",
        finalize_governed_memory_operator_evaluation,
        evaluation,
        reordered,
        **final_kwargs,
    )
    duplicated = deepcopy(observations)
    duplicated[1] = deepcopy(duplicated[0])
    _assert_fail(
        "observation_order_or_membership_invalid",
        finalize_governed_memory_operator_evaluation,
        evaluation,
        duplicated,
        **final_kwargs,
    )
    modified = deepcopy(observations)
    modified[0]["outcome_correct"] = not modified[0]["outcome_correct"]
    _assert_fail(
        "observation_derived_or_raw_fields_modified",
        finalize_governed_memory_operator_evaluation,
        evaluation,
        modified,
        **final_kwargs,
    )
    _assert_fail(
        "perceived_values_must_be_integers_1_to_5",
        finalize_governed_memory_operator_evaluation,
        evaluation,
        observations,
        **{**final_kwargs, "governed_perceived_burden": 6},
    )


def test_pex_miss_and_not_measured_dispositions():
    assert evaluation_module._pex_result([2100], target_ms=2000)["disposition"] == "MISSES-TARGET"
    assert evaluation_module._pex_result([], target_ms=1000) == {
        "sample_size": 0,
        "method": "nearest-rank-p95",
        "p95_ms": None,
        "target_ms": 1000,
        "disposition": "NOT-MEASURED",
        "human_elapsed_time_excluded": True,
    }


def test_runtime_creates_no_files_hermes_home_local_or_artifacts(tmp_path, monkeypatch):
    hermes_home = tmp_path / "hermes-home"
    monkeypatch.setenv("HERMES_HOME", str(hermes_home))
    monkeypatch.chdir(tmp_path)
    before = _all_files(tmp_path)
    corpus = _corpus()
    evaluation = _prepared(corpus)
    packets = [
        build_operator_trial_packet(evaluation, trial_id=trial_id)
        for trial_id in evaluation["trial_order"]
    ]
    after = _all_files(tmp_path)
    assert before == after == set()
    assert not hermes_home.exists()
    assert not (tmp_path / ".local").exists()
    assert not any(
        fragment in str(path).lower()
        for path in after
        for fragment in ("proposal", "execution", "ledger", "sqlite", "token", "cache")
    )
    assert evaluation["provider_tools"] == []
    _assert_no_promotion_true(evaluation)
    _assert_no_promotion_true(packets)


def test_modified_prepared_evaluation_fails_closed():
    evaluation = _prepared()
    evaluation["continuation_authorized"] = True
    _assert_fail(
        "prepared_evaluation_invalid_or_modified",
        build_operator_trial_packet,
        evaluation,
        trial_id="R6-1-T01",
    )


def test_r6_0_focused_compatibility_remains_non_applied():
    candidate = deepcopy(_corpus()["trials"][0]["candidate"])
    result = run_governed_memory_learning_slice(
        candidate,
        project_id=PROJECT_ID,
        reviewer=OPERATOR_ID,
        outcome="approve_real_proposal_creation",
        rationale="Synthetic compatibility-test rationale.",
        input_classification="SYNTHETIC",
    )
    assert result["status"] == "complete_non_applied_human_decision"
    assert result["continuation_authorized"] is False
    assert result["non_applied"] is True
    assert result["non_persisted"] is True
    _assert_no_promotion_true(result)
