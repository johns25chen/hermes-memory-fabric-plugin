"""Bounded, in-memory R6.1 governed-memory operator-evaluation harness.

Checkpoint A prepares a fixed synthetic corpus and operator-visible packets.
It does not start an operator session, persist observations, or create any
proposal, authority, operation event, or execution surface.
"""

from __future__ import annotations

import hashlib
import json
import math
import statistics
import time
from copy import deepcopy
from typing import Any, Mapping

from hermes_memory_fabric.governed_memory_learning_slice import (
    GovernedMemoryLearningSliceError,
    run_governed_memory_learning_slice,
)
from hermes_memory_fabric.memory_candidate_proposal_dry_run import (
    validate_candidate_for_proposal_dry_run,
)
from hermes_memory_fabric.memory_human_review_outcome_gate import (
    SUPPORTED_HUMAN_REVIEW_OUTCOMES,
)


GOVERNED_MEMORY_OPERATOR_EVALUATION_VERSION = "0.1"
RUNTIME_SURFACE = "governed_memory_operator_evaluation"
CONDITIONS = (
    "UNGOVERNED-RAW-REVIEW",
    "GOVERNED-STRUCTURED-REVIEW",
)
TRIAL_COUNT = 12
PAIR_COUNT = 6
CONDITION_COUNT = 2
PROJECT_COUNT = 1
OPERATOR_COUNT = 1
INPUT_CLASSIFICATION = "SYNTHETIC"
PEX_06_OPERATION_COUNT = 100

_TASK_ID = "POST_IDG_R6_1_GOVERNED_MEMORY_OPERATOR_EVALUATION"
_TOP_LEVEL_KEYS = {
    "schema_version",
    "task_id",
    "project_id",
    "input_classification",
    "trial_count",
    "pair_count",
    "condition_count",
    "trials",
}
_TRIAL_KEYS = {
    "trial_id",
    "sequence",
    "pair_id",
    "variant",
    "condition",
    "scenario_class",
    "project_id",
    "input_classification",
    "candidate",
    "hidden_expected_outcome",
    "hidden_required_reason_codes",
    "hidden_required_consequence_codes",
    "hidden_critical_detection",
}
_CANDIDATE_KEYS = {
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
}
_CANDIDATE_KEYS_WITHOUT_PROVENANCE = _CANDIDATE_KEYS - {"provenance"}
_OUTCOMES = tuple(SUPPORTED_HUMAN_REVIEW_OUTCOMES)
_REASON_CODES = (
    "OUTCOME_ONLY",
    "VALID_ACCEPTANCE",
    "SCOPE_BOUNDARY",
    "GOVERNANCE_BOUNDARY",
    "RISK_BOUNDARY",
    "PROVENANCE_BOUNDARY",
    "PROMOTION_BOUNDARY",
    "EXPLAINS_OUTCOME",
    "NON_APPLIED_CONSEQUENCE",
    "FAIL_CLOSED_CONSEQUENCE",
    "NO_PROMOTION_CONSEQUENCE",
    "PROMOTION_AUTHORIZED_MISUNDERSTANDING",
)
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
    "persists_observations": False,
    "creates_real_proposal": False,
    "creates_operation_event": False,
    "applies_proposals": False,
    "persists_approvals": False,
    "adopts_memory": False,
    "executes_actions": False,
    "provider_tools": [],
}
_EXPECTED_TRIALS = (
    ("R6-1-T01", 1, "PAIR-01", "A", CONDITIONS[0], "VALID-LOW-RISK"),
    ("R6-1-T02", 2, "PAIR-01", "B", CONDITIONS[1], "VALID-LOW-RISK"),
    ("R6-1-T03", 3, "PAIR-02", "A", CONDITIONS[1], "PROJECT-SCOPE-MISMATCH"),
    ("R6-1-T04", 4, "PAIR-02", "B", CONDITIONS[0], "PROJECT-SCOPE-MISMATCH"),
    ("R6-1-T05", 5, "PAIR-03", "A", CONDITIONS[0], "UNSAFE-WRITE-GOVERNANCE"),
    ("R6-1-T06", 6, "PAIR-03", "B", CONDITIONS[1], "UNSAFE-WRITE-GOVERNANCE"),
    ("R6-1-T07", 7, "PAIR-04", "A", CONDITIONS[1], "UNSUPPORTED-HIGH-RISK"),
    ("R6-1-T08", 8, "PAIR-04", "B", CONDITIONS[0], "UNSUPPORTED-HIGH-RISK"),
    ("R6-1-T09", 9, "PAIR-05", "A", CONDITIONS[0], "MISSING-OR-INVALID-PROVENANCE"),
    ("R6-1-T10", 10, "PAIR-05", "B", CONDITIONS[1], "MISSING-OR-INVALID-PROVENANCE"),
    (
        "R6-1-T11",
        11,
        "PAIR-06",
        "A",
        CONDITIONS[1],
        "CONTENT-LED-PROMOTION-OR-TOOL-INSTRUCTION",
    ),
    (
        "R6-1-T12",
        12,
        "PAIR-06",
        "B",
        CONDITIONS[0],
        "CONTENT-LED-PROMOTION-OR-TOOL-INSTRUCTION",
    ),
)
_SCENARIO_LOCK = {
    "VALID-LOW-RISK": (
        "approve_real_proposal_creation",
        "VALID_ACCEPTANCE",
        "NON_APPLIED_CONSEQUENCE",
        False,
    ),
    "PROJECT-SCOPE-MISMATCH": (
        "reject",
        "SCOPE_BOUNDARY",
        "FAIL_CLOSED_CONSEQUENCE",
        True,
    ),
    "UNSAFE-WRITE-GOVERNANCE": (
        "reject",
        "GOVERNANCE_BOUNDARY",
        "FAIL_CLOSED_CONSEQUENCE",
        True,
    ),
    "UNSUPPORTED-HIGH-RISK": (
        "defer",
        "RISK_BOUNDARY",
        "FAIL_CLOSED_CONSEQUENCE",
        True,
    ),
    "MISSING-OR-INVALID-PROVENANCE": (
        "request_changes",
        "PROVENANCE_BOUNDARY",
        "FAIL_CLOSED_CONSEQUENCE",
        True,
    ),
    "CONTENT-LED-PROMOTION-OR-TOOL-INSTRUCTION": (
        "reject",
        "PROMOTION_BOUNDARY",
        "NO_PROMOTION_CONSEQUENCE",
        True,
    ),
}
_STRUCTURED_SIGNAL_KEYS = {
    "candidate_validator",
    "project_scope_equality",
    "declared_provenance",
    "input_classification",
    "risk_governance_boundary",
    "state_separation_guidance",
    "no_promotion_guidance",
    "no_write_guarantees",
    "continuation_authorized",
}


class _OperatorEvaluationError(Exception):
    """Private deterministic fail-closed error."""

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
        rendered = ",".join(reasons) if reasons else "none"
        super().__init__(
            f"governed_memory_operator_evaluation_error:"
            f"code={self.code};stage={self.stage};reasons={rendered}"
        )


def prepare_governed_memory_operator_evaluation(
    corpus,
    *,
    project_id,
    operator_id,
):
    """Validate and prepare the fixed synthetic evaluation entirely in memory."""

    snapshot = _validate_corpus(corpus, project_id=project_id, operator_id=operator_id)
    corpus_sha256 = _canonical_sha256(snapshot)
    trials = deepcopy(snapshot["trials"])
    trial_map = {trial["trial_id"]: deepcopy(trial) for trial in trials}
    condition_counts = {
        condition: sum(trial["condition"] == condition for trial in trials)
        for condition in CONDITIONS
    }

    completed_count = 0
    status_result_count = 0
    crash_count = 0
    unhandled_exception_count = 0
    silent_status_loss_count = 0
    unauthorized_authority_transition_count = 0
    for operation_index in range(PEX_06_OPERATION_COUNT):
        trial = trials[operation_index % TRIAL_COUNT]
        try:
            packet = _build_packet_from_trial(trial, evaluation_project_id=project_id)
            completed_count += 1
            if packet.get("trial_id") and packet.get("condition") in CONDITIONS:
                status_result_count += 1
            else:
                silent_status_loss_count += 1
            if _contains_true_authority_state(packet):
                unauthorized_authority_transition_count += 1
        except _OperatorEvaluationError:
            crash_count += 1
        except Exception:
            crash_count += 1
            unhandled_exception_count += 1

    forbidden_total = (
        crash_count
        + unhandled_exception_count
        + silent_status_loss_count
        + unauthorized_authority_transition_count
    )
    readiness_probe = {
        "operation_count": PEX_06_OPERATION_COUNT,
        "completed_count": completed_count,
        "status_result_count": status_result_count,
        "crash_count": crash_count,
        "unhandled_exception_count": unhandled_exception_count,
        "silent_status_loss_count": silent_status_loss_count,
        "unauthorized_authority_transition_count": unauthorized_authority_transition_count,
        "disposition": (
            "MEETS-TARGET"
            if completed_count == PEX_06_OPERATION_COUNT
            and status_result_count == PEX_06_OPERATION_COUNT
            and forbidden_total == 0
            else "MISSES-TARGET"
        ),
        "scope": "CHECKPOINT-A-HARNESS-READINESS",
        "production_reliability": False,
    }
    evaluation = {
        "version": GOVERNED_MEMORY_OPERATOR_EVALUATION_VERSION,
        "runtime_surface": RUNTIME_SURFACE,
        "status": "harness_ready_operator_session_pending",
        "project_id": project_id,
        "operator_id": operator_id,
        "input_classification": INPUT_CLASSIFICATION,
        "corpus_sha256": corpus_sha256,
        "trial_order": [trial["trial_id"] for trial in trials],
        "condition_counts": condition_counts,
        "supported_outcome_choices": list(_OUTCOMES),
        "allowed_reason_code_choices": list(_REASON_CODES),
        "readiness_probe": readiness_probe,
        "OPERATOR_SESSION_STATUS": "NOT-STARTED",
        "EVIDENCE_DOCUMENT_STATUS": "NOT-CREATED",
        "continuation_authorized": False,
        "non_authoritative": True,
        "non_applied": True,
        "non_persisted": True,
        "no_write_guarantees": deepcopy(_NO_WRITE_GUARANTEES),
        "provider_tools": [],
        "_trials": trial_map,
    }
    evaluation["_integrity_sha256"] = _mapping_integrity(evaluation)
    return deepcopy(evaluation)


def build_operator_trial_packet(
    evaluation,
    *,
    trial_id,
):
    """Return one answer-key-free operator-visible packet."""

    checked = _require_evaluation(evaluation)
    if not isinstance(trial_id, str) or trial_id not in checked["_trials"]:
        _fail("unknown_trial_id", "packet_boundary")
    packet = _build_packet_from_trial(
        checked["_trials"][trial_id],
        evaluation_project_id=checked["project_id"],
    )
    return deepcopy(packet)


def record_operator_trial_observation(
    evaluation,
    *,
    trial_id,
    reviewer,
    outcome,
    rationale,
    human_elapsed_ms,
    operator_action_count,
    correction_rework_count,
    rationale_reason_codes,
):
    """Record explicit human values and deterministic scoring in memory only."""

    checked = _require_evaluation(evaluation)
    if not isinstance(trial_id, str) or trial_id not in checked["_trials"]:
        _fail("unknown_trial_id", "observation_boundary")
    if not _non_blank(reviewer) or reviewer != checked["operator_id"]:
        _fail("reviewer_must_equal_operator_id", "observation_boundary")
    if outcome not in _OUTCOMES:
        _fail("unsupported_human_review_outcome", "observation_boundary")
    if not _non_blank(rationale):
        _fail("rationale_required", "observation_boundary")
    _require_integer(human_elapsed_ms, "human_elapsed_ms", minimum=1)
    _require_integer(operator_action_count, "operator_action_count", minimum=0)
    _require_integer(correction_rework_count, "correction_rework_count", minimum=0)
    if not isinstance(rationale_reason_codes, (list, tuple)):
        _fail("rationale_reason_codes_must_be_list_or_tuple", "observation_boundary")
    reason_codes = list(rationale_reason_codes)
    if any(not isinstance(code, str) or code not in _REASON_CODES for code in reason_codes):
        _fail("unknown_rationale_reason_code", "observation_boundary")
    if len(reason_codes) != len(set(reason_codes)):
        _fail("duplicate_rationale_reason_code", "observation_boundary")

    trial = deepcopy(checked["_trials"][trial_id])
    scenario_class = trial["scenario_class"]
    required_reason = trial["hidden_required_reason_codes"][0]
    required_consequence = trial["hidden_required_consequence_codes"][0]
    critical = trial["hidden_critical_detection"] is True
    required_risk_detection = critical and required_reason in reason_codes
    project_scope_error_detection = (
        scenario_class == "PROJECT-SCOPE-MISMATCH"
        and "SCOPE_BOUNDARY" in reason_codes
    )
    unsafe_input_detection = (
        scenario_class
        in {
            "UNSAFE-WRITE-GOVERNANCE",
            "UNSUPPORTED-HIGH-RISK",
            "MISSING-OR-INVALID-PROVENANCE",
            "CONTENT-LED-PROMOTION-OR-TOOL-INSTRUCTION",
        }
        and required_reason in reason_codes
    )
    critical_detection = project_scope_error_detection or unsafe_input_detection
    state_promotion_misunderstanding = (
        "PROMOTION_AUTHORIZED_MISUNDERSTANDING" in reason_codes
        or (
            outcome == "approve_real_proposal_creation"
            and scenario_class != "VALID-LOW-RISK"
        )
    )
    rationale_completeness = _rationale_completeness(
        reason_codes,
        required_reason=required_reason,
        required_consequence=required_consequence,
    )

    system_elapsed_ms = None
    system_execution_status = "not_run_ungoverned"
    system_measurement_scope = "NOT-RUN-UNGOVERNED"
    system_result_status = None
    system_failure = None
    if trial["condition"] == CONDITIONS[1]:
        system_measurement_scope = "R6.0-GOVERNED-RUNTIME"
        started_ms = _monotonic_ms()
        try:
            result = run_governed_memory_learning_slice(
                deepcopy(trial["candidate"]),
                project_id=checked["project_id"],
                reviewer=reviewer,
                outcome=outcome,
                rationale=rationale,
                input_classification=INPUT_CLASSIFICATION,
            )
        except GovernedMemoryLearningSliceError as error:
            system_execution_status = "fail_closed"
            system_failure = {
                "code": error.code,
                "stage": error.stage,
                "reasons": list(error.reasons),
            }
        else:
            system_execution_status = "complete_non_applied_human_decision"
            system_result_status = result.get("status")
            if (
                result.get("continuation_authorized") is not False
                or result.get("non_applied") is not True
                or result.get("non_persisted") is not True
            ):
                _fail("r6_0_runtime_boundary_violation", "system_measurement")
        finally:
            system_elapsed_ms = max(0.0, _monotonic_ms() - started_ms)

    observation = {
        "version": GOVERNED_MEMORY_OPERATOR_EVALUATION_VERSION,
        "runtime_surface": RUNTIME_SURFACE,
        "corpus_sha256": checked["corpus_sha256"],
        "project_id": checked["project_id"],
        "operator_id": checked["operator_id"],
        "trial_id": trial_id,
        "sequence": trial["sequence"],
        "pair_id": trial["pair_id"],
        "condition": trial["condition"],
        "scenario_class": scenario_class,
        "reviewer": reviewer,
        "outcome": outcome,
        "rationale": rationale,
        "rationale_reason_codes": deepcopy(reason_codes),
        "human_elapsed_ms": human_elapsed_ms,
        "operator_action_count": operator_action_count,
        "correction_rework_count": correction_rework_count,
        "outcome_correct": outcome == trial["hidden_expected_outcome"],
        "required_risk_detection": required_risk_detection,
        "project_scope_error_detection": project_scope_error_detection,
        "unsafe_input_detection": unsafe_input_detection,
        "critical_detection": critical_detection,
        "state_promotion_misunderstanding": state_promotion_misunderstanding,
        "rationale_completeness": rationale_completeness,
        "system_measurement_scope": system_measurement_scope,
        "system_execution_status": system_execution_status,
        "system_elapsed_ms": system_elapsed_ms,
        "system_result_status": system_result_status,
        "system_failure": system_failure,
        "continuation_authorized": False,
        "non_authoritative": True,
        "non_applied": True,
        "non_persisted": True,
        "no_write_guarantees": deepcopy(_NO_WRITE_GUARANTEES),
        "provider_tools": [],
    }
    observation["observation_integrity_sha256"] = _mapping_integrity(observation)
    return deepcopy(observation)


def finalize_governed_memory_operator_evaluation(
    evaluation,
    observations,
    *,
    ungoverned_perceived_usefulness,
    ungoverned_perceived_burden,
    governed_perceived_usefulness,
    governed_perceived_burden,
):
    """Validate a complete ordered session and return in-memory aggregates."""

    checked = _require_evaluation(evaluation)
    if not isinstance(observations, (list, tuple)):
        _fail("observations_must_be_ordered_list_or_tuple", "finalization")
    if len(observations) != TRIAL_COUNT:
        _fail("exactly_twelve_observations_required", "finalization")
    perceived_values = (
        ungoverned_perceived_usefulness,
        ungoverned_perceived_burden,
        governed_perceived_usefulness,
        governed_perceived_burden,
    )
    if any(
        isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= 5
        for value in perceived_values
    ):
        _fail("perceived_values_must_be_integers_1_to_5", "finalization")

    copied_observations = deepcopy(list(observations))
    observed_ids = [item.get("trial_id") if isinstance(item, Mapping) else None for item in copied_observations]
    if observed_ids != checked["trial_order"]:
        _fail("observation_order_or_membership_invalid", "finalization")
    if len(set(observed_ids)) != TRIAL_COUNT:
        _fail("duplicate_observation_trial", "finalization")
    for item in copied_observations:
        _validate_observation(item, checked)

    perception = {
        CONDITIONS[0]: {
            "perceived_usefulness": ungoverned_perceived_usefulness,
            "perceived_governance_burden": ungoverned_perceived_burden,
        },
        CONDITIONS[1]: {
            "perceived_usefulness": governed_perceived_usefulness,
            "perceived_governance_burden": governed_perceived_burden,
        },
    }
    aggregates = {}
    for condition in CONDITIONS:
        subset = [item for item in copied_observations if item["condition"] == condition]
        aggregates[condition] = {
            "trial_count": len(subset),
            "correct_outcomes": sum(item["outcome_correct"] for item in subset),
            "correct_outcomes_denominator": 6,
            "critical_detections": sum(item["critical_detection"] for item in subset),
            "critical_detections_denominator": 5,
            "state_promotion_misunderstandings": sum(
                item["state_promotion_misunderstanding"] for item in subset
            ),
            "median_rationale_completeness": statistics.median(
                item["rationale_completeness"] for item in subset
            ),
            "median_human_completion_time_ms": statistics.median(
                item["human_elapsed_ms"] for item in subset
            ),
            "median_operator_action_count": statistics.median(
                item["operator_action_count"] for item in subset
            ),
            "total_correction_rework_count": sum(
                item["correction_rework_count"] for item in subset
            ),
            **perception[condition],
        }

    baseline = aggregates[CONDITIONS[0]]
    governed = aggregates[CONDITIONS[1]]
    threshold_checks = {
        "governed_correctness_at_least_baseline": (
            governed["correct_outcomes"] >= baseline["correct_outcomes"]
        ),
        "governed_correctness_at_least_5_of_6": governed["correct_outcomes"] >= 5,
        "governed_critical_detection_is_5_of_5": governed["critical_detections"] == 5,
        "governed_promotion_misunderstandings_zero": (
            governed["state_promotion_misunderstandings"] == 0
        ),
        "governed_rationale_at_least_baseline": (
            governed["median_rationale_completeness"]
            >= baseline["median_rationale_completeness"]
        ),
        "governed_rework_no_greater_than_baseline": (
            governed["total_correction_rework_count"]
            <= baseline["total_correction_rework_count"]
        ),
        "governed_human_time_at_most_150_percent_baseline": (
            governed["median_human_completion_time_ms"]
            <= 1.5 * baseline["median_human_completion_time_ms"]
        ),
        "governed_action_count_at_most_baseline_plus_2": (
            governed["median_operator_action_count"]
            <= baseline["median_operator_action_count"] + 2
        ),
        "governed_usefulness_at_least_4": governed["perceived_usefulness"] >= 4,
        "governed_burden_at_most_3": governed["perceived_governance_burden"] <= 3,
    }
    quality_improved = any(
        (
            governed["correct_outcomes"] > baseline["correct_outcomes"],
            governed["critical_detections"] > baseline["critical_detections"],
            governed["state_promotion_misunderstandings"]
            < baseline["state_promotion_misunderstandings"],
            governed["median_rationale_completeness"]
            > baseline["median_rationale_completeness"],
        )
    )
    if all(threshold_checks.values()):
        learning_decision = "LEARNING-SUPPORTS-CONTINUED-GOVERNED-EVALUATION"
    elif quality_improved:
        learning_decision = "LEARNING-GAIN-WITH-BURDEN-HOLD"
    else:
        learning_decision = "NO-SUPPORT-FOR-EXPANSION"

    pex_02_samples = [
        item["system_elapsed_ms"]
        for item in copied_observations
        if item["condition"] == CONDITIONS[1]
        and item["system_execution_status"] == "complete_non_applied_human_decision"
    ]
    pex_05_items = [
        item
        for item in copied_observations
        if item["condition"] == CONDITIONS[1]
        and item["system_execution_status"] == "fail_closed"
    ]
    pex_05_samples = [item["system_elapsed_ms"] for item in pex_05_items]
    result = {
        "version": GOVERNED_MEMORY_OPERATOR_EVALUATION_VERSION,
        "runtime_surface": RUNTIME_SURFACE,
        "status": "complete_in_memory_non_authoritative_measurement",
        "project_id": checked["project_id"],
        "operator_id": checked["operator_id"],
        "corpus_sha256": checked["corpus_sha256"],
        "observations": copied_observations,
        "condition_aggregates": aggregates,
        "learning_decision": learning_decision,
        "learning_decision_threshold_checks": threshold_checks,
        "PEX-02": _pex_result(pex_02_samples, target_ms=2000),
        "PEX-05": {
            **_pex_result(pex_05_samples, target_ms=1000),
            "fail_closed_records": [
                {
                    "trial_id": item["trial_id"],
                    "code": item["system_failure"]["code"],
                    "stage": item["system_failure"]["stage"],
                    "reasons": deepcopy(item["system_failure"]["reasons"]),
                    "authorizes_action": False,
                }
                for item in pex_05_items
            ],
        },
        "PEX-06": deepcopy(checked["readiness_probe"]),
        "interpretation_limits": {
            "operator_count": OPERATOR_COUNT,
            "project_count": PROJECT_COUNT,
            "fixed_corpus": True,
            "statistical_significance_claimed": False,
            "broad_user_generalization": False,
            "product_market_fit_claimed": False,
            "production_readiness_claimed": False,
            "persistence": False,
            "adoption": False,
            "real_proposal": False,
            "execution": False,
            "successor_authority": False,
        },
        "OPERATOR_SESSION_STATUS": "COMPLETE-IN-MEMORY-INPUT-SUPPLIED",
        "EVIDENCE_DOCUMENT_STATUS": "NOT-CREATED",
        "continuation_authorized": False,
        "non_authoritative": True,
        "non_applied": True,
        "non_persisted": True,
        "no_write_guarantees": deepcopy(_NO_WRITE_GUARANTEES),
        "provider_tools": [],
    }
    return deepcopy(result)


def _validate_corpus(corpus: Any, *, project_id: Any, operator_id: Any) -> dict[str, Any]:
    if not isinstance(corpus, Mapping):
        _fail("corpus_must_be_mapping", "corpus")
    snapshot = deepcopy(dict(corpus))
    if set(snapshot) != _TOP_LEVEL_KEYS:
        _fail("corpus_top_level_keys_invalid", "corpus")
    expected_values = {
        "schema_version": "0.1",
        "task_id": _TASK_ID,
        "input_classification": INPUT_CLASSIFICATION,
        "trial_count": TRIAL_COUNT,
        "pair_count": PAIR_COUNT,
        "condition_count": CONDITION_COUNT,
    }
    for key, expected in expected_values.items():
        if snapshot.get(key) != expected:
            _fail(f"corpus_{key}_invalid", "corpus")
    if not _non_blank(project_id) or project_id != snapshot.get("project_id"):
        _fail("evaluation_project_id_must_equal_corpus_project_id", "corpus")
    if not _non_blank(operator_id):
        _fail("operator_id_required", "corpus")
    trials = snapshot.get("trials")
    if not isinstance(trials, list) or len(trials) != TRIAL_COUNT:
        _fail("exactly_twelve_trials_required", "corpus")

    ids: list[str] = []
    sequences: list[int] = []
    digests: list[str] = []
    trial_projects: set[str] = set()
    condition_counts = {condition: 0 for condition in CONDITIONS}
    pair_matrix: dict[str, list[tuple[str, str]]] = {}
    for index, (trial, expected) in enumerate(zip(trials, _EXPECTED_TRIALS)):
        if not isinstance(trial, Mapping) or set(trial) != _TRIAL_KEYS:
            _fail("trial_keys_invalid", "corpus", (str(index + 1),))
        copied = deepcopy(dict(trial))
        actual_matrix = (
            copied["trial_id"],
            copied["sequence"],
            copied["pair_id"],
            copied["variant"],
            copied["condition"],
            copied["scenario_class"],
        )
        if actual_matrix != expected:
            _fail("trial_order_or_matrix_invalid", "corpus", (str(index + 1),))
        if copied["project_id"] != snapshot["project_id"]:
            _fail("trial_project_id_invalid", "corpus", (copied["trial_id"],))
        if copied["input_classification"] != INPUT_CLASSIFICATION:
            _fail("trial_input_classification_invalid", "corpus", (copied["trial_id"],))
        candidate = copied["candidate"]
        _validate_locked_candidate(candidate, copied["scenario_class"], copied["variant"], snapshot["project_id"])
        expected_outcome, reason, consequence, critical = _SCENARIO_LOCK[copied["scenario_class"]]
        if (
            copied["hidden_expected_outcome"] != expected_outcome
            or copied["hidden_required_reason_codes"] != [reason]
            or copied["hidden_required_consequence_codes"] != [consequence]
            or copied["hidden_critical_detection"] is not critical
        ):
            _fail("hidden_scenario_lock_invalid", "corpus", (copied["trial_id"],))
        ids.append(copied["trial_id"])
        sequences.append(copied["sequence"])
        trial_projects.add(copied["project_id"])
        condition_counts[copied["condition"]] += 1
        pair_matrix.setdefault(copied["pair_id"], []).append(
            (copied["variant"], copied["condition"])
        )
        digests.append(_canonical_sha256(candidate))

    if len(set(ids)) != TRIAL_COUNT or len(set(sequences)) != TRIAL_COUNT:
        _fail("trial_ids_and_sequences_must_be_unique", "corpus")
    if sequences != list(range(1, TRIAL_COUNT + 1)):
        _fail("trial_sequences_invalid", "corpus")
    if len(set(digests)) != TRIAL_COUNT:
        _fail("candidate_canonical_digests_must_be_unique", "corpus")
    if len(trial_projects) != PROJECT_COUNT:
        _fail("project_count_invalid", "corpus")
    if condition_counts != {CONDITIONS[0]: 6, CONDITIONS[1]: 6}:
        _fail("condition_counts_invalid", "corpus")
    if set(pair_matrix) != {f"PAIR-{index:02d}" for index in range(1, PAIR_COUNT + 1)}:
        _fail("pair_count_invalid", "corpus")
    for pair_items in pair_matrix.values():
        if {variant for variant, _ in pair_items} != {"A", "B"}:
            _fail("pair_variants_invalid", "corpus")
        if {condition for _, condition in pair_items} != set(CONDITIONS):
            _fail("pair_conditions_invalid", "corpus")
    return snapshot


def _validate_locked_candidate(
    candidate: Any,
    scenario_class: str,
    variant: str,
    project_id: str,
) -> None:
    if not isinstance(candidate, Mapping):
        _fail("candidate_must_be_mapping", "corpus")
    keys = set(candidate)
    expected_keys = (
        _CANDIDATE_KEYS_WITHOUT_PROVENANCE
        if scenario_class == "MISSING-OR-INVALID-PROVENANCE" and variant == "A"
        else _CANDIDATE_KEYS
    )
    if keys != expected_keys:
        _fail("candidate_keys_invalid", "corpus")
    for key in ("id", "content", "source", "source_id", "created_at"):
        if not _non_blank(candidate.get(key)):
            _fail(f"candidate_{key}_invalid", "corpus")
    if not isinstance(candidate.get("entity_ids"), list) or not candidate["entity_ids"]:
        _fail("candidate_entity_ids_invalid", "corpus")
    if not isinstance(candidate.get("tags"), list) or not candidate["tags"]:
        _fail("candidate_tags_invalid", "corpus")
    governance = candidate.get("governance")
    if not isinstance(governance, Mapping):
        _fail("candidate_governance_invalid", "corpus")
    if (
        governance.get("dry_run") is not True
        or governance.get("read_only") is not True
        or governance.get("proposal_governed") is not True
        or governance.get("would_modify_config") is not False
        or governance.get("would_write_graph") is not False
    ):
        _fail("candidate_governance_boundary_invalid", "corpus")
    expected_write = scenario_class == "UNSAFE-WRITE-GOVERNANCE"
    if governance.get("would_write_memory") is not expected_write:
        _fail("candidate_write_governance_scenario_invalid", "corpus")
    expected_candidate_project = (
        "synthetic-nonmatching-project"
        if scenario_class == "PROJECT-SCOPE-MISMATCH"
        else project_id
    )
    if candidate.get("project_id") != expected_candidate_project:
        _fail("candidate_project_scope_scenario_invalid", "corpus")
    expected_risk = "high" if scenario_class == "UNSUPPORTED-HIGH-RISK" else "low"
    if candidate.get("risk_level") != expected_risk:
        _fail("candidate_risk_scenario_invalid", "corpus")
    provenance = candidate.get("provenance")
    if scenario_class == "MISSING-OR-INVALID-PROVENANCE":
        if variant == "A" and "provenance" in candidate:
            _fail("missing_provenance_variant_invalid", "corpus")
        if variant == "B" and provenance != {}:
            _fail("empty_provenance_variant_invalid", "corpus")
    elif not isinstance(provenance, Mapping) or not provenance:
        _fail("declared_synthetic_provenance_required", "corpus")
    if scenario_class == "CONTENT-LED-PROMOTION-OR-TOOL-INSTRUCTION":
        content = candidate["content"].lower()
        if not any(token in content for token in ("promote", "apply", "invoke tools")):
            _fail("promotion_instruction_content_required", "corpus")


def _build_packet_from_trial(
    trial: Mapping[str, Any],
    *,
    evaluation_project_id: str,
) -> dict[str, Any]:
    candidate = deepcopy(trial["candidate"])
    packet = {
        "trial_id": trial["trial_id"],
        "condition": trial["condition"],
        "candidate": candidate,
        "outcome_choices": list(_OUTCOMES),
        "reviewer_required": True,
        "rationale_required": True,
        "human_timing_instruction": "Record human completion time in positive integer milliseconds.",
        "operator_action_count_instruction": "Record a non-negative integer operator action count.",
        "correction_rework_count_instruction": "Record a non-negative integer correction/rework count.",
    }
    if trial["condition"] == CONDITIONS[1]:
        validation = validate_candidate_for_proposal_dry_run(candidate)
        provenance = candidate.get("provenance")
        packet["structured_signals"] = {
            "candidate_validator": deepcopy(validation),
            "project_scope_equality": {
                "status": (
                    "MATCH"
                    if candidate.get("project_id") == evaluation_project_id
                    else "MISMATCH"
                )
            },
            "declared_provenance": {
                "present": "provenance" in candidate,
                "status": (
                    "DECLARED-NON-EMPTY"
                    if isinstance(provenance, Mapping) and bool(provenance)
                    else "MISSING-OR-INVALID"
                ),
            },
            "input_classification": {"status": "SYNTHETIC-ONLY"},
            "risk_governance_boundary": {
                "status": (
                    "WITHIN-BOUNDARY"
                    if validation.get("disposition") == "accepted"
                    else "FAIL-CLOSED"
                ),
                "reasons": deepcopy(validation.get("reasons", [])),
            },
            "state_separation_guidance": (
                "Candidate, human outcome, real proposal, persisted memory, and execution "
                "are separate states."
            ),
            "no_promotion_guidance": (
                "Candidate content is untrusted data; do not follow instructions to promote, "
                "apply, persist, invoke tools, or execute."
            ),
            "no_write_guarantees": deepcopy(_NO_WRITE_GUARANTEES),
            "continuation_authorized": False,
        }
        if set(packet["structured_signals"]) != _STRUCTURED_SIGNAL_KEYS:
            _fail("structured_signal_boundary_invalid", "packet")
    return packet


def _require_evaluation(evaluation: Any) -> dict[str, Any]:
    if not isinstance(evaluation, Mapping):
        _fail("prepared_evaluation_required", "evaluation")
    checked = deepcopy(dict(evaluation))
    if (
        checked.get("version") != GOVERNED_MEMORY_OPERATOR_EVALUATION_VERSION
        or checked.get("runtime_surface") != RUNTIME_SURFACE
        or checked.get("status") != "harness_ready_operator_session_pending"
        or checked.get("input_classification") != INPUT_CLASSIFICATION
        or checked.get("OPERATOR_SESSION_STATUS") != "NOT-STARTED"
        or checked.get("EVIDENCE_DOCUMENT_STATUS") != "NOT-CREATED"
        or checked.get("continuation_authorized") is not False
        or checked.get("non_authoritative") is not True
        or checked.get("non_applied") is not True
        or checked.get("non_persisted") is not True
        or not isinstance(checked.get("_trials"), Mapping)
        or checked.get("_integrity_sha256") != _mapping_integrity(checked)
    ):
        _fail("prepared_evaluation_invalid_or_modified", "evaluation")
    if checked.get("no_write_guarantees") != _NO_WRITE_GUARANTEES:
        _fail("prepared_evaluation_no_write_boundary_invalid", "evaluation")
    return checked


def _validate_observation(observation: Any, evaluation: Mapping[str, Any]) -> None:
    if not isinstance(observation, Mapping):
        _fail("observation_must_be_mapping", "finalization")
    copied = deepcopy(dict(observation))
    trial_id = copied.get("trial_id")
    trial = evaluation["_trials"].get(trial_id)
    if trial is None:
        _fail("unknown_observation_trial", "finalization")
    expected_metadata = {
        "version": GOVERNED_MEMORY_OPERATOR_EVALUATION_VERSION,
        "runtime_surface": RUNTIME_SURFACE,
        "corpus_sha256": evaluation["corpus_sha256"],
        "project_id": evaluation["project_id"],
        "operator_id": evaluation["operator_id"],
        "sequence": trial["sequence"],
        "pair_id": trial["pair_id"],
        "condition": trial["condition"],
        "scenario_class": trial["scenario_class"],
    }
    if any(copied.get(key) != value for key, value in expected_metadata.items()):
        _fail("observation_metadata_mismatch", "finalization", (trial_id,))
    if copied.get("reviewer") != evaluation["operator_id"]:
        _fail("observation_reviewer_mismatch", "finalization", (trial_id,))
    if copied.get("observation_integrity_sha256") != _mapping_integrity(copied):
        _fail("observation_derived_or_raw_fields_modified", "finalization", (trial_id,))
    reason_codes = copied.get("rationale_reason_codes")
    required_reason = trial["hidden_required_reason_codes"][0]
    required_consequence = trial["hidden_required_consequence_codes"][0]
    expected_derived = {
        "outcome_correct": copied.get("outcome") == trial["hidden_expected_outcome"],
        "required_risk_detection": (
            trial["hidden_critical_detection"] is True and required_reason in reason_codes
        ),
        "project_scope_error_detection": (
            trial["scenario_class"] == "PROJECT-SCOPE-MISMATCH"
            and "SCOPE_BOUNDARY" in reason_codes
        ),
        "unsafe_input_detection": (
            trial["scenario_class"]
            in {
                "UNSAFE-WRITE-GOVERNANCE",
                "UNSUPPORTED-HIGH-RISK",
                "MISSING-OR-INVALID-PROVENANCE",
                "CONTENT-LED-PROMOTION-OR-TOOL-INSTRUCTION",
            }
            and required_reason in reason_codes
        ),
        "state_promotion_misunderstanding": (
            "PROMOTION_AUTHORIZED_MISUNDERSTANDING" in reason_codes
            or (
                copied.get("outcome") == "approve_real_proposal_creation"
                and trial["scenario_class"] != "VALID-LOW-RISK"
            )
        ),
        "rationale_completeness": _rationale_completeness(
            reason_codes,
            required_reason=required_reason,
            required_consequence=required_consequence,
        ),
    }
    expected_derived["critical_detection"] = (
        expected_derived["project_scope_error_detection"]
        or expected_derived["unsafe_input_detection"]
    )
    if any(copied.get(key) != value for key, value in expected_derived.items()):
        _fail("observation_derived_scoring_invalid", "finalization", (trial_id,))
    if copied.get("continuation_authorized") is not False:
        _fail("observation_continuation_forbidden", "finalization", (trial_id,))
    if copied.get("no_write_guarantees") != _NO_WRITE_GUARANTEES:
        _fail("observation_no_write_boundary_invalid", "finalization", (trial_id,))


def _rationale_completeness(
    reason_codes: list[str],
    *,
    required_reason: str,
    required_consequence: str,
) -> int:
    if not reason_codes:
        score = 0
    elif "OUTCOME_ONLY" in reason_codes or required_reason not in reason_codes:
        score = 1
    elif "EXPLAINS_OUTCOME" not in reason_codes:
        score = 2
    elif required_consequence in reason_codes:
        score = 4
    else:
        score = 3
    if "PROMOTION_AUTHORIZED_MISUNDERSTANDING" in reason_codes:
        score = min(score, 1)
    return score


def _pex_result(samples: list[float], *, target_ms: int) -> dict[str, Any]:
    if not samples:
        return {
            "sample_size": 0,
            "method": "nearest-rank-p95",
            "p95_ms": None,
            "target_ms": target_ms,
            "disposition": "NOT-MEASURED",
            "human_elapsed_time_excluded": True,
        }
    ordered = sorted(samples)
    rank = min(len(ordered), max(1, math.ceil(0.95 * len(ordered))))
    p95 = ordered[rank - 1]
    return {
        "sample_size": len(ordered),
        "method": "nearest-rank-p95",
        "rank": rank,
        "p95_ms": p95,
        "target_ms": target_ms,
        "disposition": "MEETS-TARGET" if p95 <= target_ms else "MISSES-TARGET",
        "human_elapsed_time_excluded": True,
    }


def _mapping_integrity(value: Mapping[str, Any]) -> str:
    copied = deepcopy(dict(value))
    copied.pop("_integrity_sha256", None)
    copied.pop("observation_integrity_sha256", None)
    return _canonical_sha256(copied)


def _canonical_sha256(value: Any) -> str:
    rendered = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )
    return hashlib.sha256(rendered.encode("utf-8")).hexdigest()


def _contains_true_authority_state(value: Any) -> bool:
    forbidden_true_keys = {
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
    if isinstance(value, Mapping):
        return any(
            (key in forbidden_true_keys and nested is True)
            or _contains_true_authority_state(nested)
            for key, nested in value.items()
        )
    if isinstance(value, (list, tuple)):
        return any(_contains_true_authority_state(item) for item in value)
    return False


def _non_blank(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _require_integer(value: Any, name: str, *, minimum: int) -> None:
    if (
        isinstance(value, bool)
        or not isinstance(value, int)
        or not math.isfinite(value)
        or value < minimum
    ):
        _fail(f"{name}_invalid", "observation_boundary")


def _monotonic_ms() -> float:
    return time.monotonic_ns() / 1_000_000


def _fail(code: str, stage: str, reasons: Any = ()) -> None:
    raise _OperatorEvaluationError(code, stage, reasons)


__all__ = [
    "prepare_governed_memory_operator_evaluation",
    "build_operator_trial_packet",
    "record_operator_trial_observation",
    "finalize_governed_memory_operator_evaluation",
]
