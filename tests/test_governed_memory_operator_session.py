from __future__ import annotations

import hashlib
import json
import re
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
EVIDENCE_RELATIVE = Path(
    "docs/CIVILIZATION_CORE_POST_IDG_R6_1_REPLACEMENT_OPERATOR_EVALUATION_EVIDENCE.md"
)


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


def test_exact_surface_plan_practice_and_fixed_chinese_semantics(monkeypatch):
    expected_raw_sha = hashlib.sha256(NEW_CORPUS.read_bytes()).hexdigest()
    canonical_json_sha = hashlib.sha256(
        json.dumps(corpus(), ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode()
    ).hexdigest()
    assert expected_raw_sha == "76574906ab6c989c0159d88b64c961f16b78a1dfd5b1dc347c0b62ccf34dcf77"
    assert canonical_json_sha != expected_raw_sha
    assert session_module.__all__ == ["governed_memory_operator_session"]
    session = make_session()
    first = session.plan()
    second = make_session().plan()
    assert first == second
    assert first["runtime_surface"] == "governed_memory_operator_session"
    assert first["practice_count"] == 4
    assert first["scored_trial_count"] == 12
    assert first["matched_pair_count"] == 6
    assert first["corpus_sha256"] == expected_raw_sha
    supplied = corpus()
    prepared_corpora = []
    prepare = session_module.prepare_governed_memory_operator_evaluation

    def capture_prepared_corpus(value, **kwargs):
        prepared_corpora.append(value)
        return prepare(value, **kwargs)

    monkeypatch.setattr(
        session_module, "prepare_governed_memory_operator_evaluation", capture_prepared_corpus
    )
    equal_session = governed_memory_operator_session(
        supplied,
        project_id="civilization-core",
        operator_id="synthetic-test-operator",
    )
    assert equal_session.plan()["corpus_sha256"] == expected_raw_sha
    assert prepared_corpora[-1] == supplied
    assert prepared_corpora[-1] is not supplied

    different = deepcopy(supplied)
    different["trials"][0]["candidate"]["content"] += " 内容不同但结构仍有效。"
    assert_error(
        "corpus_mismatch",
        lambda: governed_memory_operator_session(
            different,
            project_id="civilization-core",
            operator_id="synthetic-test-operator",
        ),
    )

    class ForgedDigestCorpus(dict):
        _raw_sha256 = "0" * 64

    forged_equal = ForgedDigestCorpus(supplied)
    forged_session = governed_memory_operator_session(
        forged_equal,
        project_id="civilization-core",
        operator_id="synthetic-test-operator",
    )
    assert forged_session.plan()["corpus_sha256"] == expected_raw_sha
    assert type(prepared_corpora[-1]) is dict
    forged_different = ForgedDigestCorpus(different)
    assert_error(
        "corpus_mismatch",
        lambda: governed_memory_operator_session(
            forged_different,
            project_id="civilization-core",
            operator_id="synthetic-test-operator",
        ),
    )
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


def test_replacement_corpus_exact_matrix_and_new_identities():
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
    assert len(digests) == 12
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


def terminal_inputs(*, reject_first_lock=False, open_glossary=False):
    values = ["yes"] * 4
    for outcome in (
        "approve_real_proposal_creation", "request_changes", "reject", "defer"
    ):
        values.extend((outcome, "OUTCOME_ONLY", "独立完成的合成练习理由。"))
    for index in range(12):
        values.append("yes" if open_glossary and index == 0 else "no")
        if open_glossary and index == 0:
            values.append("yes")
        values.extend(("defer", "OUTCOME_ONLY", f"第{index + 1}项独立人工理由。", "yes"))
        if reject_first_lock and index == 0:
            values.append("no")
            values.extend(
                ("no", "reject", "GOVERNANCE_BOUNDARY", "编辑后的独立人工理由。", "yes")
            )
        values.append("yes")
    values.extend(("4", "2", "5", "3", "yes", "yes"))
    return values


def run_terminal(values, *, argv=None, cwd=None):
    outputs = []
    iterator = iter(values)
    tick = iter(float(value) for value in range(1000, 5000, 100)).__next__
    if cwd is None:
        return_code = session_module.main(
            argv or ["--operator-id", "opaque-human-operator"],
            input_fn=lambda _prompt: next(iterator),
            output_fn=outputs.append,
            clock=tick,
            corpus_loader=corpus,
        )
    else:
        old_cwd = Path.cwd()
        try:
            __import__("os").chdir(cwd)
            return_code = session_module.main(
                argv or ["--operator-id", "opaque-human-operator"],
                input_fn=lambda _prompt: next(iterator),
                output_fn=outputs.append,
                clock=tick,
                corpus_loader=corpus,
            )
        finally:
            __import__("os").chdir(old_cwd)
    return return_code, outputs


def test_preflight_exact_output_and_no_exposure():
    expected_raw_sha = hashlib.sha256(NEW_CORPUS.read_bytes()).hexdigest()
    expected_plan = make_session().plan()
    return_code, outputs = run_terminal([], argv=["--preflight"])
    assert return_code == 0
    assert outputs == [
        "RUNTIME_SURFACE=governed_memory_operator_session",
        "STATUS=HARNESS-READY-OPERATOR-SESSION-PENDING",
        "PROJECT_ID=civilization-core",
        "INPUT_CLASSIFICATION=SYNTHETIC",
        "PRACTICE_COUNT=4",
        "SCORED_TRIAL_COUNT=12",
        "MATCHED_PAIR_COUNT=6",
        f"CORPUS_SHA256={expected_raw_sha}",
        "EVIDENCE_DOCUMENT_STATUS=NOT-CREATED",
        "ACTUAL_HUMAN_OPERATOR_SESSION_STATUS=NOT-STARTED",
        "CONTINUATION_AUTHORIZED=FALSE",
        "IN_MEMORY_ONLY=TRUE",
        "PROVIDER_TOOL_COUNT=0",
    ]
    rendered = "\n".join(outputs)
    corpus_sha256_lines = [
        line for line in outputs if line.startswith("CORPUS_SHA256=")
    ]
    assert len(corpus_sha256_lines) == 1
    corpus_sha256 = corpus_sha256_lines[0].removeprefix("CORPUS_SHA256=")
    assert corpus_sha256 == expected_raw_sha
    assert expected_plan["corpus_sha256"] == expected_raw_sha
    assert re.fullmatch(r"[0-9a-f]{64}", corpus_sha256)
    assert len(expected_plan["corpus_sha256"]) == 64
    assert expected_plan["corpus_sha256"] == expected_plan["corpus_sha256"].lower()
    assert "candidate" not in rendered.lower()
    assert "hidden_" not in rendered.lower()
    assert "correct" not in rendered.lower()


def test_eligibility_rejection_precedes_corpus_loading_and_exposure():
    outputs = []
    loaded = []
    return_code = session_module.main(
        ["--operator-id", "opaque-human-operator"],
        input_fn=lambda _prompt: "no",
        output_fn=outputs.append,
        corpus_loader=lambda: loaded.append(True),
    )
    assert return_code != 0
    assert outputs == []
    assert loaded == []


@pytest.mark.parametrize("failure", [EOFError(), KeyboardInterrupt()])
def test_terminal_eof_and_interrupt_fail_closed_without_result(failure):
    outputs = []

    def fail(_prompt):
        raise failure

    return_code = session_module.main(
        ["--operator-id", "opaque-human-operator"],
        input_fn=fail,
        output_fn=outputs.append,
        corpus_loader=corpus,
    )
    assert return_code != 0
    assert not any(line.startswith("SESSION_RESULT_JSON=") for line in outputs)


def test_complete_terminal_flow_glossary_edit_declined_lock_and_final_payload():
    return_code, outputs = run_terminal(
        terminal_inputs(reject_first_lock=True, open_glossary=True)
    )
    assert return_code == 0
    assert sum(line.startswith("PRACTICE_PACKET=") for line in outputs) == 4
    assert sum(line.startswith("PRACTICE_FEEDBACK=") for line in outputs) == 4
    assert sum(line.startswith("SCORED_PACKET=") for line in outputs) == 12
    assert sum(line.startswith("GLOSSARY=") for line in outputs) == 1
    markers = [line for line in outputs if line.startswith("SESSION_RESULT_JSON=")]
    assert len(markers) == 1
    assert outputs[-1] == markers[0]
    marker_suffix = outputs[-1].removeprefix("SESSION_RESULT_JSON=")
    payload = json.loads(marker_suffix)
    assert json.dumps(
        payload, sort_keys=True, ensure_ascii=False, separators=(",", ":")
    ) == marker_suffix
    result = payload["result"]
    observations = result["observations"]
    assert [item["trial_id"] for item in observations] == [f"R6-1-T{i:02d}" for i in range(1, 13)]
    assert result["status"] == "complete_in_memory_non_authoritative_measurement"
    assert result["OPERATOR_SESSION_STATUS"] == "COMPLETE-IN-MEMORY-INPUT-SUPPLIED"
    assert payload["evidence_document_status"] == "NOT-CREATED"
    assert payload["continuation_authorized"] is False
    assert payload["non_persisted"] is True
    assert observations[0]["correction_rework_count"] == 4
    rendered = markers[0]
    for forbidden in (
        "hidden_expected_outcome", "hidden_required_reason_codes",
        "hidden_required_consequence_codes", "hidden_critical_detection",
    ):
        assert forbidden not in rendered
    pending = [payload]
    keys = set()
    while pending:
        item = pending.pop()
        if isinstance(item, dict):
            keys.update(item)
            pending.extend(item.values())
        elif isinstance(item, list):
            pending.extend(item)
    assert "candidate" not in keys
    assert "content" not in keys


def test_terminal_and_preflight_create_no_files_and_preserve_evidence_sentinel(tmp_path):
    empty = tmp_path / "empty"
    empty.mkdir()
    assert run_terminal([], argv=["--preflight"], cwd=empty)[0] == 0
    assert run_terminal(terminal_inputs(), cwd=empty)[0] == 0
    assert list(empty.rglob("*")) == []

    workspace = tmp_path / "sentinel-workspace"
    evidence = workspace / EVIDENCE_RELATIVE
    evidence.parent.mkdir(parents=True)
    sentinel = b"future-checkpoint-b-evidence-sentinel\x00\xff"
    evidence.write_bytes(sentinel)
    before = {path.relative_to(workspace) for path in workspace.rglob("*") if path.is_file()}
    assert run_terminal([], argv=["--preflight"], cwd=workspace)[0] == 0
    assert run_terminal(terminal_inputs(), cwd=workspace)[0] == 0
    after = {path.relative_to(workspace) for path in workspace.rglob("*") if path.is_file()}
    assert after == before == {EVIDENCE_RELATIVE}
    assert evidence.read_bytes() == sentinel
