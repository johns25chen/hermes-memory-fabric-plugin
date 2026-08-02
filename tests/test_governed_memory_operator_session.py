from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from pathlib import Path

import pytest

import hermes_memory_fabric.governed_memory_operator_evaluation as engine
import hermes_memory_fabric.governed_memory_operator_session as session_module
from hermes_memory_fabric.governed_memory_operator_session import (
    governed_memory_operator_session,
)


ROOT = Path(__file__).parents[1]
NEW_CORPUS = ROOT / "docs/CIVILIZATION_CORE_POST_IDG_R6_1_REPLACEMENT_OPERATOR_EVALUATION_SCENARIO_CORPUS.json"
ORIGINAL_CORPUS = ROOT / "docs/CIVILIZATION_CORE_POST_IDG_R6_1_OPERATOR_EVALUATION_SCENARIO_CORPUS.json"
EVIDENCE = ROOT / "docs/CIVILIZATION_CORE_POST_IDG_R6_1_REPLACEMENT_OPERATOR_EVALUATION_EVIDENCE.md"


def corpus():
    return json.loads(NEW_CORPUS.read_text(encoding="utf-8"))


def make_session(clock=None):
    return governed_memory_operator_session(
        corpus(),
        project_id="civilization-core",
        operator_id="synthetic-test-operator",
        clock=clock or iter([1000.0, 1400.0]).__next__,
    )


def complete_practice(session):
    for outcome in (
        "approve_real_proposal_creation",
        "request_changes",
        "reject",
        "defer",
    ):
        feedback = session.submit_practice(
            outcome=outcome,
            reason_codes=["OUTCOME_ONLY"],
            rationale="这是明确提交的合成练习理由。",
        )
        assert feedback["classification"] == "NON-SCORED-PRACTICE"
        assert feedback["scored"] is False


def assert_error(code, call):
    with pytest.raises(Exception) as captured:
        call()
    assert captured.value.code == code


def test_exact_surface_plan_practice_and_fixed_chinese_semantics():
    assert session_module.__all__ == ["governed_memory_operator_session"]
    session = make_session()
    first = session.plan()
    second = make_session().plan()
    assert first == second
    assert first["runtime_surface"] == "governed_memory_operator_session"
    assert first["practice_count"] == 4
    assert first["scored_trial_count"] == 12
    assert first["matched_pair_count"] == 6
    assert first["input_classification"] == "SYNTHETIC"
    assert first["evidence_document_status"] == "NOT-CREATED"
    assert tuple(value for _, value, _ in first["outcome_choices"]) == (
        "approve_real_proposal_creation", "request_changes", "reject", "defer"
    )
    assert dict(first["glossary"]) == dict(session_module.GLOSSARY)
    assert len(session_module.PRACTICE_EXAMPLES) == 4
    assert {item["correct_outcome"] for item in session_module.PRACTICE_EXAMPLES} == {
        "approve_real_proposal_creation", "request_changes", "reject", "defer"
    }
    packet = session.practice_packet()
    assert packet["feedback"] is None
    complete_practice(session)
    assert_error("practice_complete", session.practice_packet)


def test_replacement_corpus_exact_matrix_new_identities_and_opaque_original_digest_overlap():
    value = corpus()
    prepared = engine.prepare_governed_memory_operator_evaluation(
        value, project_id="civilization-core", operator_id="synthetic-test-operator"
    )
    assert len(value["trials"]) == 12
    assert len({trial["pair_id"] for trial in value["trials"]}) == 6
    assert {trial["input_classification"] for trial in value["trials"]} == {"SYNTHETIC"}
    assert [trial["condition"] for trial in value["trials"]] == [
        "UNGOVERNED-RAW-REVIEW", "GOVERNED-STRUCTURED-REVIEW",
        "GOVERNED-STRUCTURED-REVIEW", "UNGOVERNED-RAW-REVIEW",
        "UNGOVERNED-RAW-REVIEW", "GOVERNED-STRUCTURED-REVIEW",
        "GOVERNED-STRUCTURED-REVIEW", "UNGOVERNED-RAW-REVIEW",
        "UNGOVERNED-RAW-REVIEW", "GOVERNED-STRUCTURED-REVIEW",
        "GOVERNED-STRUCTURED-REVIEW", "UNGOVERNED-RAW-REVIEW",
    ]
    candidates = [trial["candidate"] for trial in value["trials"]]
    digests = {engine._canonical_sha256(candidate) for candidate in candidates}
    original = json.loads(ORIGINAL_CORPUS.read_text(encoding="utf-8"))
    original_digests = {
        engine._canonical_sha256(trial["candidate"]) for trial in original["trials"]
    }
    assert len(digests) == 12
    assert len(digests & original_digests) == 0
    identities = {
        next(tag for tag in candidate["tags"] if tag.startswith("fixture:v3-sealed-"))
        for candidate in candidates
    }
    assert len(identities) == 12
    for field in ("id", "content", "source_id"):
        assert len({hashlib.sha256(candidate[field].encode()).hexdigest() for candidate in candidates}) == 12
    assert prepared["readiness_probe"]["disposition"] == "MEETS-TARGET"


def test_current_trial_edit_lock_events_monotonic_time_and_no_return():
    clock = iter([1000.0, 1650.0, 1651.0]).__next__
    session = make_session(clock)
    complete_practice(session)
    packet = session.start_next_trial()
    assert "scenario_class" not in json.dumps(packet, ensure_ascii=False)
    session.open_glossary()
    session.close_glossary()
    session.submit_outcome("request_changes")
    session.submit_reason_boundaries(["OUTCOME_ONLY"])
    assert_error(
        "rationale_must_not_duplicate_outcome_option",
        lambda: session.submit_rationale("要求修改", confirmed=True),
    )
    session.submit_rationale("我依据当前合成事实明确选择结果，且结果保持未应用。", confirmed=True)
    session.review()
    assert session.confirm_lock(False) is None
    session.submit_outcome("approve_real_proposal_creation")
    session.submit_reason_boundaries(
        ["VALID_ACCEPTANCE", "EXPLAINS_OUTCOME", "NON_APPLIED_CONSEQUENCE"]
    )
    session.submit_rationale("项目、来源、风险和治理边界均满足，但当前仍不创建或应用。", confirmed=True)
    review = session.review()
    assert review["lock_confirmation_required"] is True
    locked = session.confirm_lock(True)
    assert locked["human_elapsed_ms"] == 650
    assert locked["operator_action_count"] == len(locked["action_events"]) == 12
    assert locked["correction_rework_count"] == len(locked["rework_events"]) == 4
    assert set(locked["action_events"]) <= session_module.ACTION_EVENT_TYPES
    assert set(locked["rework_events"]) <= session_module.REWORK_EVENT_TYPES
    assert_error("no_current_unlocked_trial", session.current_packet)
    next_packet = session.start_next_trial()
    assert next_packet["trial_id"] == "R6-1-T02"


def test_blank_confirmation_incomplete_attestation_and_scores_fail_closed():
    session = make_session()
    assert_error("practice_incomplete", session.start_next_trial)
    complete_practice(session)
    session.start_next_trial()
    assert_error("current_trial_input_incomplete", session.review)
    session.submit_outcome("reject")
    session.submit_reason_boundaries(["GOVERNANCE_BOUNDARY"])
    assert_error(
        "rationale_confirmation_required",
        lambda: session.submit_rationale("明确的人工理由。", confirmed=False),
    )
    assert_error("scored_trials_incomplete", session.finalize)
    assert_error(
        "explicit_attestations_required",
        lambda: session.attest(no_answer_key_viewed=True, no_outside_assistance=False),
    )
    assert_error(
        "condition_scores_invalid",
        lambda: session.set_condition_scores(engine.CONDITIONS[0], usefulness=0, burden=5),
    )
    assert not EVIDENCE.exists()


def test_no_mutation_no_storage_network_model_proposal_execution_or_promotion(tmp_path, monkeypatch):
    before_files = {p.relative_to(tmp_path) for p in tmp_path.rglob("*") if p.is_file()}
    value = corpus()
    before = deepcopy(value)
    monkeypatch.chdir(tmp_path)
    session = governed_memory_operator_session(
        value,
        project_id="civilization-core",
        operator_id="synthetic-test-operator",
        clock=iter([1.0, 2.0]).__next__,
    )
    assert value == before
    plan = session.plan()
    assert plan["provider_tools"] == []
    assert plan["continuation_authorized"] is False
    assert plan["in_memory_only"] is True
    after_files = {p.relative_to(tmp_path) for p in tmp_path.rglob("*") if p.is_file()}
    assert after_files == before_files
    source = Path(session_module.__file__).read_text(encoding="utf-8")
    for token in (
        "requests", "urllib", "socket", "subprocess", "openai", "anthropic",
        "mcp", "connector", "memory_write_proposal", "apply_proposal",
    ):
        assert token not in source.lower()


def test_packet_preserves_engine_data_and_hides_answers():
    session = make_session()
    complete_practice(session)
    visible = session.start_next_trial()
    expected = engine.build_operator_trial_packet(
        session._evaluation, trial_id="R6-1-T01"
    )
    assert visible["packet"] == expected
    rendered = json.dumps(visible, ensure_ascii=False)
    for forbidden in (
        "hidden_expected_outcome", "hidden_required_reason_codes",
        "hidden_required_consequence_codes", "hidden_critical_detection",
        "scenario_class", "pair_id", "correctness", "aggregate_result",
    ):
        assert forbidden not in rendered


def test_operator_smoke_harness_ready_without_starting_human_session():
    session = make_session()
    plan = session.plan()
    assert plan["status"] == "HARNESS-READY-OPERATOR-SESSION-PENDING"
    assert plan["actual_human_operator_session_status"] == "NOT-STARTED"
    assert plan["evidence_document_status"] == "NOT-CREATED"
    assert not EVIDENCE.exists()
