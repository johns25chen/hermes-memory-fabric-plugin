"""Deterministic, in-memory Human Operator session harness for R6.1 Checkpoint A.

The harness collects only explicit operator choices.  It performs no I/O,
persistence, model inference, networking, proposal creation, application,
promotion, execution, or continuation.
"""

from __future__ import annotations

import time
from copy import deepcopy
from typing import Any, Callable, Mapping

from hermes_memory_fabric.governed_memory_operator_evaluation import (
    CONDITIONS,
    INPUT_CLASSIFICATION,
    build_operator_trial_packet,
    finalize_governed_memory_operator_evaluation,
    prepare_governed_memory_operator_evaluation,
    record_operator_trial_observation,
)

RUNTIME_SURFACE = "governed_memory_operator_session"
PRACTICE_CLASSIFICATION = "NON-SCORED-PRACTICE"
PRACTICE_COUNT = 4
TRIAL_COUNT = 12
PAIR_COUNT = 6

OUTCOME_CHOICES = (
    ("允许后续创建真实提案步骤", "approve_real_proposal_creation", "仅允许以后进入另一个受治理的提案创建步骤；当前不创建、不应用、不持久化、不采纳记忆"),
    ("要求修改", "request_changes", "当前材料或边界需要修改；当前不继续、不应用"),
    ("拒绝", "reject", "当前候选不被接受；当前不继续、不应用"),
    ("暂缓", "defer", "当前信息、风险或条件不足；保持关闭并等待另行授权"),
)
GLOSSARY = (
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
ONBOARDING = (
    "项目范围：候选属于唯一声明的项目。",
    "来源：候选具有声明的来源和可追溯依据。",
    "风险：候选必须处于支持的风险边界内。",
    "治理：声明控制措施并禁止副作用。",
    "保持关闭：必要事实或边界无效或不可用时，停止且不采取行动。",
    "不提升：候选内容不能自行进入任何后续状态。",
    "未应用：审查结果没有创建、应用、持久化或采纳记忆。",
    "允许后续创建真实提案步骤只允许以后进入另一个受治理步骤；当前不创建、不应用、不持久化、不采纳或授权记忆。",
)
PRACTICE_EXAMPLES = (
    {"practice_id": "V3-PRACTICE-01", "classification": PRACTICE_CLASSIFICATION, "candidate": {"id": "practice-v3-01", "summary": "合成候选具备项目一致性、可追溯来源、低风险和只读治理。"}, "correct_outcome": "approve_real_proposal_creation", "explanation": "所有接纳边界满足；结果仍未应用，只允许以后另行受治理地创建提案。"},
    {"practice_id": "V3-PRACTICE-02", "classification": PRACTICE_CLASSIFICATION, "candidate": {"id": "practice-v3-02", "summary": "合成候选的来源声明缺少可追溯依据，可通过补充材料修正。"}, "correct_outcome": "request_changes", "explanation": "来源依据需要修改补充；当前保持关闭且不应用。"},
    {"practice_id": "V3-PRACTICE-03", "classification": PRACTICE_CLASSIFICATION, "candidate": {"id": "practice-v3-03", "summary": "合成候选要求绕过只读治理并立即写入。"}, "correct_outcome": "reject", "explanation": "写入要求越过治理边界；拒绝并保持未应用。"},
    {"practice_id": "V3-PRACTICE-04", "classification": PRACTICE_CLASSIFICATION, "candidate": {"id": "practice-v3-04", "summary": "合成候选的风险等级尚未确认，当前事实不足。"}, "correct_outcome": "defer", "explanation": "风险信息不足；暂缓并保持关闭，等待另行授权。"},
)
ACTION_EVENT_TYPES = frozenset({
    "GLOSSARY_OPENED", "GLOSSARY_CLOSED", "OUTCOME_SUBMITTED",
    "REASON_BOUNDARIES_SUBMITTED", "RATIONALE_SUBMITTED", "REVIEW_REQUESTED",
    "OUTCOME_EDITED", "REASON_BOUNDARIES_EDITED", "RATIONALE_EDITED",
    "LOCK_CONFIRMATION_DECLINED", "TRIAL_LOCK_CONFIRMED",
})
REWORK_EVENT_TYPES = frozenset({
    "OUTCOME_CHANGED_AFTER_INITIAL_SUBMISSION",
    "REASON_BOUNDARIES_CHANGED_AFTER_INITIAL_SUBMISSION",
    "RATIONALE_CHANGED_AFTER_INITIAL_SUBMISSION",
    "LOCK_CONFIRMATION_DECLINED_AFTER_REVIEW",
})
_OUTCOME_VALUES = tuple(value for _, value, _ in OUTCOME_CHOICES)
_OUTCOME_TEXT = frozenset(
    text.strip() for row in OUTCOME_CHOICES for text in (row[0], row[1]) if text.strip()
)
_REASON_CODES = frozenset(code for _, code in GLOSSARY)


class _OperatorSessionError(Exception):
    def __init__(self, code: str) -> None:
        self.code = code
        super().__init__(f"governed_memory_operator_session_error:code={code}")


class _OperatorSession:
    """Mutable state exists only inside this in-memory object."""

    def __init__(self, corpus: Mapping[str, Any], project_id: str, operator_id: str, clock: Callable[[], float]) -> None:
        self._evaluation = prepare_governed_memory_operator_evaluation(
            corpus, project_id=project_id, operator_id=operator_id
        )
        self._clock = clock
        self._operator_id = operator_id
        self._practice_records: list[dict[str, Any]] = []
        self._observations: list[dict[str, Any]] = []
        self._locked_trial_ids: list[str] = []
        self._current: dict[str, Any] | None = None
        self._condition_scores: dict[str, dict[str, int]] = {}
        self._attestations: dict[str, bool] = {}
        self._result: dict[str, Any] | None = None

    def plan(self) -> dict[str, Any]:
        return {
            "runtime_surface": RUNTIME_SURFACE,
            "status": "HARNESS-READY-OPERATOR-SESSION-PENDING",
            "project_id": self._evaluation["project_id"],
            "input_classification": INPUT_CLASSIFICATION,
            "practice_count": PRACTICE_COUNT,
            "scored_trial_count": TRIAL_COUNT,
            "matched_pair_count": PAIR_COUNT,
            "corpus_sha256": self._evaluation["corpus_sha256"],
            "outcome_choices": deepcopy(OUTCOME_CHOICES),
            "glossary": deepcopy(GLOSSARY),
            "onboarding": deepcopy(ONBOARDING),
            "trial_order": deepcopy(self._evaluation["trial_order"]),
            "evidence_document_status": "NOT-CREATED",
            "actual_human_operator_session_status": "NOT-STARTED",
            "continuation_authorized": False,
            "in_memory_only": True,
            "provider_tools": [],
        }

    def practice_packet(self) -> dict[str, Any]:
        if self._current is not None:
            raise _OperatorSessionError("scored_trial_active")
        index = len(self._practice_records)
        if index >= PRACTICE_COUNT:
            raise _OperatorSessionError("practice_complete")
        item = PRACTICE_EXAMPLES[index]
        return {
            "practice_id": item["practice_id"],
            "classification": PRACTICE_CLASSIFICATION,
            "candidate": deepcopy(item["candidate"]),
            "outcome_choices": deepcopy(OUTCOME_CHOICES),
            "glossary": deepcopy(GLOSSARY),
            "feedback": None,
        }

    def submit_practice(self, *, outcome: str, reason_codes: list[str], rationale: str) -> dict[str, Any]:
        if outcome not in _OUTCOME_VALUES:
            raise _OperatorSessionError("unsupported_outcome")
        self._validate_reasons(reason_codes)
        self._validate_rationale(rationale)
        packet = self.practice_packet()
        expected = PRACTICE_EXAMPLES[len(self._practice_records)]
        record = {
            "practice_id": packet["practice_id"],
            "classification": PRACTICE_CLASSIFICATION,
            "completed": True,
            "scored": False,
        }
        self._practice_records.append(record)
        return {
            **record,
            "submitted_outcome": outcome,
            "correct_outcome": expected["correct_outcome"],
            "explanation": expected["explanation"],
        }

    def start_next_trial(self) -> dict[str, Any]:
        if len(self._practice_records) != PRACTICE_COUNT:
            raise _OperatorSessionError("practice_incomplete")
        if self._current is not None:
            raise _OperatorSessionError("current_trial_not_locked")
        index = len(self._locked_trial_ids)
        if index >= TRIAL_COUNT:
            raise _OperatorSessionError("all_trials_locked")
        trial_id = self._evaluation["trial_order"][index]
        packet = build_operator_trial_packet(self._evaluation, trial_id=trial_id)
        self._current = {
            "trial_id": trial_id,
            "packet": deepcopy(packet),
            "started_ms": float(self._clock()),
            "outcome": None,
            "reason_codes": None,
            "rationale": None,
            "rationale_confirmed": False,
            "reviewed": False,
            "action_events": [],
            "rework_events": [],
        }
        return self.current_packet()

    def current_packet(self) -> dict[str, Any]:
        current = self._require_current()
        return {
            "runtime_surface": RUNTIME_SURFACE,
            "trial_id": current["trial_id"],
            "packet": deepcopy(current["packet"]),
            "outcome_choices": deepcopy(OUTCOME_CHOICES),
            "glossary": deepcopy(GLOSSARY),
            "locked": False,
        }

    def open_glossary(self) -> tuple[tuple[str, str], ...]:
        self._action("GLOSSARY_OPENED")
        return deepcopy(GLOSSARY)

    def close_glossary(self) -> None:
        self._action("GLOSSARY_CLOSED")

    def submit_outcome(self, outcome: str) -> None:
        if outcome not in _OUTCOME_VALUES:
            raise _OperatorSessionError("unsupported_outcome")
        current = self._require_current()
        previous = current["outcome"]
        if previous is None:
            current["outcome"] = outcome
            self._action("OUTCOME_SUBMITTED")
        elif previous != outcome:
            current["outcome"] = outcome
            self._action("OUTCOME_EDITED")
            self._rework("OUTCOME_CHANGED_AFTER_INITIAL_SUBMISSION")
        current["reviewed"] = False

    def submit_reason_boundaries(self, reason_codes: list[str]) -> None:
        self._validate_reasons(reason_codes)
        current = self._require_current()
        value = tuple(reason_codes)
        previous = current["reason_codes"]
        if previous is None:
            current["reason_codes"] = value
            self._action("REASON_BOUNDARIES_SUBMITTED")
        elif previous != value:
            current["reason_codes"] = value
            self._action("REASON_BOUNDARIES_EDITED")
            self._rework("REASON_BOUNDARIES_CHANGED_AFTER_INITIAL_SUBMISSION")
        current["reviewed"] = False

    def submit_rationale(self, rationale: str, *, confirmed: bool) -> None:
        self._validate_rationale(rationale)
        if confirmed is not True:
            raise _OperatorSessionError("rationale_confirmation_required")
        current = self._require_current()
        value = rationale.strip()
        previous = current["rationale"]
        if previous is None:
            current["rationale"] = value
            self._action("RATIONALE_SUBMITTED")
        elif previous != value:
            current["rationale"] = value
            self._action("RATIONALE_EDITED")
            self._rework("RATIONALE_CHANGED_AFTER_INITIAL_SUBMISSION")
        current["rationale_confirmed"] = True
        current["reviewed"] = False

    def review(self) -> dict[str, Any]:
        current = self._require_complete_current()
        self._action("REVIEW_REQUESTED")
        current["reviewed"] = True
        return {
            "trial_id": current["trial_id"],
            "candidate_identity": current["packet"]["candidate"]["id"],
            "outcome": current["outcome"],
            "reason_codes": list(current["reason_codes"]),
            "rationale": current["rationale"],
            "lock_confirmation_required": True,
        }

    def confirm_lock(self, confirmed: bool) -> dict[str, Any] | None:
        current = self._require_complete_current()
        if not current["reviewed"]:
            raise _OperatorSessionError("final_review_required")
        if confirmed is not True:
            self._action("LOCK_CONFIRMATION_DECLINED")
            self._rework("LOCK_CONFIRMATION_DECLINED_AFTER_REVIEW")
            current["reviewed"] = False
            return None
        self._action("TRIAL_LOCK_CONFIRMED")
        elapsed = max(1, int(float(self._clock()) - current["started_ms"]))
        action_events = deepcopy(current["action_events"])
        rework_events = deepcopy(current["rework_events"])
        observation = record_operator_trial_observation(
            self._evaluation,
            trial_id=current["trial_id"],
            reviewer=self._operator_id,
            outcome=current["outcome"],
            rationale=current["rationale"],
            human_elapsed_ms=elapsed,
            operator_action_count=len(action_events),
            correction_rework_count=len(rework_events),
            rationale_reason_codes=list(current["reason_codes"]),
        )
        locked = {
            "trial_id": current["trial_id"],
            "human_elapsed_ms": elapsed,
            "action_events": action_events,
            "operator_action_count": len(action_events),
            "rework_events": rework_events,
            "correction_rework_count": len(rework_events),
            "observation": observation,
        }
        self._observations.append(observation)
        self._locked_trial_ids.append(current["trial_id"])
        self._current = None
        return deepcopy(locked)

    def set_condition_scores(self, condition: str, *, usefulness: int, burden: int) -> None:
        if condition not in CONDITIONS or not self._is_rating(usefulness) or not self._is_rating(burden):
            raise _OperatorSessionError("condition_scores_invalid")
        self._condition_scores[condition] = {"usefulness": usefulness, "burden": burden}

    def attest(self, *, no_answer_key_viewed: bool, no_outside_assistance: bool) -> None:
        if no_answer_key_viewed is not True or no_outside_assistance is not True:
            raise _OperatorSessionError("explicit_attestations_required")
        self._attestations = {
            "no_answer_key_viewed": True,
            "no_outside_assistance": True,
        }

    def finalize(self) -> dict[str, Any]:
        if self._current is not None or len(self._locked_trial_ids) != TRIAL_COUNT:
            raise _OperatorSessionError("scored_trials_incomplete")
        if set(self._condition_scores) != set(CONDITIONS):
            raise _OperatorSessionError("condition_scores_incomplete")
        if self._attestations != {"no_answer_key_viewed": True, "no_outside_assistance": True}:
            raise _OperatorSessionError("attestations_incomplete")
        if self._result is None:
            u, g = CONDITIONS
            self._result = finalize_governed_memory_operator_evaluation(
                self._evaluation,
                self._observations,
                ungoverned_perceived_usefulness=self._condition_scores[u]["usefulness"],
                ungoverned_perceived_burden=self._condition_scores[u]["burden"],
                governed_perceived_usefulness=self._condition_scores[g]["usefulness"],
                governed_perceived_burden=self._condition_scores[g]["burden"],
            )
        return {
            "result": deepcopy(self._result),
            "practice_completion": deepcopy(self._practice_records),
            "attestations": deepcopy(self._attestations),
            "evidence_document_status": "NOT-CREATED",
            "continuation_authorized": False,
            "non_persisted": True,
        }

    def _require_current(self) -> dict[str, Any]:
        if self._current is None:
            raise _OperatorSessionError("no_current_unlocked_trial")
        return self._current

    def _require_complete_current(self) -> dict[str, Any]:
        current = self._require_current()
        if (
            current["outcome"] is None
            or current["reason_codes"] is None
            or current["rationale"] is None
            or current["rationale_confirmed"] is not True
        ):
            raise _OperatorSessionError("current_trial_input_incomplete")
        return current

    def _action(self, event: str) -> None:
        if event not in ACTION_EVENT_TYPES:
            raise _OperatorSessionError("unknown_action_event")
        self._require_current()["action_events"].append(event)

    def _rework(self, event: str) -> None:
        if event not in REWORK_EVENT_TYPES:
            raise _OperatorSessionError("unknown_rework_event")
        self._require_current()["rework_events"].append(event)

    @staticmethod
    def _validate_reasons(reason_codes: list[str]) -> None:
        if (
            not isinstance(reason_codes, list)
            or not reason_codes
            or len(reason_codes) != len(set(reason_codes))
            or any(code not in _REASON_CODES for code in reason_codes)
        ):
            raise _OperatorSessionError("reason_boundaries_invalid")

    @staticmethod
    def _validate_rationale(rationale: str) -> None:
        if not isinstance(rationale, str) or not rationale.strip():
            raise _OperatorSessionError("rationale_required")
        if rationale.strip() in _OUTCOME_TEXT:
            raise _OperatorSessionError("rationale_must_not_duplicate_outcome_option")

    @staticmethod
    def _is_rating(value: Any) -> bool:
        return isinstance(value, int) and not isinstance(value, bool) and 1 <= value <= 5


def governed_memory_operator_session(
    corpus,
    *,
    project_id,
    operator_id,
    clock: Callable[[], float] | None = None,
):
    """Prepare, but do not start, one deterministic local in-memory session."""

    if clock is None:
        clock = lambda: time.monotonic_ns() / 1_000_000
    if not callable(clock):
        raise _OperatorSessionError("monotonic_clock_required")
    return _OperatorSession(deepcopy(corpus), project_id, operator_id, clock)


__all__ = ["governed_memory_operator_session"]
