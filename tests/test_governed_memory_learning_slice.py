from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

import pytest

import hermes_memory_fabric.governed_memory_learning_slice as slice_module
from hermes_memory_fabric.governed_memory_learning_slice import (
    ALLOWED_INPUT_CLASSIFICATIONS,
    GOVERNED_MEMORY_LEARNING_SLICE_VERSION,
    TERMINAL_ARTIFACT,
    GovernedMemoryLearningSliceError,
    run_governed_memory_learning_slice,
)


PROJECT_ID = "civilization-core"
REVIEWER = "human-owner"
OUTCOME = "approve_real_proposal_creation"
RATIONALE = "Explicit bounded review outcome for a non-applied learning slice."

EXPECTED_TOP_LEVEL_KEYS = {
    "version",
    "runtime_surface",
    "mode",
    "status",
    "terminal_artifact",
    "boundary_reached",
    "continuation_authorized",
    "project_id",
    "input_classification",
    "reviewer",
    "outcome",
    "rationale",
    "declared_source",
    "declared_source_id",
    "declared_provenance",
    "candidate_snapshot",
    "candidate_validation",
    "memory_block_candidate",
    "review_queue_item",
    "review_decision_candidate",
    "proposal_draft",
    "governance_submission_candidate",
    "governance_submission_packet",
    "human_review_outcome_candidate",
    "validations",
    "non_authoritative",
    "non_applied",
    "non_persisted",
    "no_write_guarantees",
}

PROMOTION_KEYS = {
    "applied",
    "persisted",
    "adopted",
    "executed",
    "created_real_proposal",
    "created_operation_event",
    "persists_approvals",
    "applies_proposals",
    "adopts_memory",
    "executes_actions",
}


def _candidate() -> dict[str, Any]:
    return {
        "id": "candidate-001",
        "content": "Bounded synthetic project context.",
        "project_id": PROJECT_ID,
        "entity_ids": ["civilization-core"],
        "source": "synthetic-fixture",
        "source_id": "synthetic-fixture-001",
        "provenance": {
            "declared_by": "test-operator",
            "method": "synthetic",
        },
        "risk_level": "low",
        "governance": {
            "dry_run": True,
            "read_only": True,
            "proposal_governed": True,
            "would_write_memory": False,
            "would_modify_config": False,
            "would_write_graph": False,
        },
        "created_at": "2026-07-29T00:00:00Z",
        "tags": ["r6.0", "synthetic"],
    }


def _run(
    candidate: Mapping[str, Any] | None = None,
    *,
    project_id: str = PROJECT_ID,
    reviewer: str = REVIEWER,
    outcome: str = OUTCOME,
    rationale: str = RATIONALE,
    input_classification: str = "SYNTHETIC",
) -> dict[str, Any]:
    return run_governed_memory_learning_slice(
        _candidate() if candidate is None else candidate,
        project_id=project_id,
        reviewer=reviewer,
        outcome=outcome,
        rationale=rationale,
        input_classification=input_classification,
    )


def _assert_error(
    code: str,
    candidate: Any = None,
    **kwargs: Any,
) -> GovernedMemoryLearningSliceError:
    supplied = _candidate() if candidate is None else candidate
    with pytest.raises(GovernedMemoryLearningSliceError) as captured:
        _run(supplied, **kwargs)
    error = captured.value
    assert error.code == code
    assert isinstance(error.reasons, tuple)
    assert str(error) == str(error)
    return error


def _assert_no_promotion_true(value: Any) -> None:
    if isinstance(value, Mapping):
        for key, nested in value.items():
            is_promotion_key = (
                key in PROMOTION_KEYS
                or any(key.endswith(promotion_key) for promotion_key in PROMOTION_KEYS)
            )
            if key in {"non_applied", "non_persisted"}:
                is_promotion_key = False
            if is_promotion_key:
                assert nested is not True, key
            _assert_no_promotion_true(nested)
    elif isinstance(value, (list, tuple)):
        for nested in value:
            _assert_no_promotion_true(nested)


def _all_files(root: Path) -> set[Path]:
    return {
        path.relative_to(root)
        for path in root.rglob("*")
        if path.is_file()
    }


def test_valid_synthetic_candidate_reaches_explicit_non_applied_human_outcome():
    result = _run()

    assert set(result) == EXPECTED_TOP_LEVEL_KEYS
    assert result["version"] == GOVERNED_MEMORY_LEARNING_SLICE_VERSION == "0.1"
    assert result["runtime_surface"] == "governed_memory_learning_slice"
    assert result["mode"] == "implementation_to_learn"
    assert result["status"] == "complete_non_applied_human_decision"
    assert result["terminal_artifact"] == TERMINAL_ARTIFACT == "human_review_outcome_candidate"
    assert result["boundary_reached"] is True
    assert result["continuation_authorized"] is False
    assert result["non_authoritative"] is True
    assert result["non_applied"] is True
    assert result["non_persisted"] is True
    human_outcome = result["human_review_outcome_candidate"]
    assert human_outcome["outcome"] == OUTCOME
    assert human_outcome["reviewer"] == REVIEWER
    assert human_outcome["rationale"] == RATIONALE


def test_non_sensitive_classification_is_accepted():
    result = _run(input_classification="NON_SENSITIVE")

    assert ALLOWED_INPUT_CLASSIFICATIONS == ("SYNTHETIC", "NON_SENSITIVE")
    assert result["input_classification"] == "NON_SENSITIVE"


def test_explicit_identity_scope_source_and_provenance_are_preserved():
    candidate = _candidate()
    result = _run(
        candidate,
        reviewer=" reviewer-with-spaces ",
        outcome="defer",
        rationale=" rationale preserved exactly ",
    )

    assert result["project_id"] == candidate["project_id"]
    assert result["reviewer"] == " reviewer-with-spaces "
    assert result["outcome"] == "defer"
    assert result["rationale"] == " rationale preserved exactly "
    assert result["declared_source"] == candidate["source"]
    assert result["declared_source_id"] == candidate["source_id"]
    assert result["declared_provenance"] == candidate["provenance"]
    assert result["memory_block_candidate"]["project_scope"] == candidate["project_id"]
    assert result["review_queue_item"]["reviewer"] == " reviewer-with-spaces "
    assert result["review_decision_candidate"]["reviewer"] == " reviewer-with-spaces "
    assert result["proposal_draft"]["author"] == " reviewer-with-spaces "
    assert result["governance_submission_candidate"]["reviewer"] == " reviewer-with-spaces "
    assert result["governance_submission_packet"]["reviewer"] == " reviewer-with-spaces "


def test_all_intermediate_validations_pass():
    validations = _run()["validations"]

    assert set(validations) == {
        "candidate",
        "memory_block_candidate",
        "review_queue_item",
        "review_decision_candidate",
        "proposal_draft",
        "governance_submission_candidate",
        "governance_submission_packet",
        "human_review_outcome_candidate",
    }
    assert validations["candidate"] == {"disposition": "accepted", "reasons": []}
    for name, validation in validations.items():
        if name != "candidate":
            assert validation == {"valid": True, "errors": []}


def test_identical_explicit_input_has_equal_output_and_deterministic_json():
    candidate = _candidate()

    first = _run(candidate)
    second = _run(candidate)

    assert first == second
    assert json.dumps(first, sort_keys=True, separators=(",", ":")) == json.dumps(
        second,
        sort_keys=True,
        separators=(",", ":"),
    )


def test_caller_candidate_is_not_mutated():
    candidate = _candidate()
    before = deepcopy(candidate)

    _run(candidate)

    assert candidate == before


def test_non_mapping_candidate_fails_closed_without_rendering_content():
    secret = "content-that-must-not-appear"
    error = _assert_error("candidate_must_be_mapping", [secret])

    assert error.stage == "input_boundary"
    assert secret not in str(error)


def test_blank_invocation_project_id_fails_closed():
    _assert_error("project_id_required", project_id=" \t")


def test_blank_candidate_project_id_fails_closed():
    candidate = _candidate()
    candidate["project_id"] = " "

    _assert_error("candidate_project_id_required", candidate)


def test_project_mismatch_fails_closed():
    _assert_error("project_id_mismatch", project_id="other-project")


def test_blank_reviewer_fails_closed():
    _assert_error("reviewer_required", reviewer="\n")


def test_missing_outcome_fails_closed():
    _assert_error("outcome_required", outcome=None)


def test_unsupported_outcome_fails_closed():
    _assert_error("unsupported_human_review_outcome", outcome="apply_now")


def test_blank_rationale_fails_closed():
    _assert_error("rationale_required", rationale="  ")


@pytest.mark.parametrize("classification", ["SENSITIVE", "", "synthetic"])
def test_unsupported_blank_and_lowercase_classifications_fail_closed(classification):
    _assert_error(
        "unsupported_input_classification",
        input_classification=classification,
    )


def test_empty_provenance_fails_closed():
    candidate = _candidate()
    candidate["provenance"] = {}

    _assert_error("declared_provenance_required", candidate)


def test_unsafe_governance_candidate_fails_closed_and_preserves_reasons():
    candidate = _candidate()
    candidate["governance"]["would_write_memory"] = True

    error = _assert_error("candidate_not_accepted", candidate)

    assert error.stage == "candidate"
    assert "governance_would_write_memory_must_be_false" in error.reasons


def test_unsupported_high_risk_candidate_fails_without_decision_output():
    candidate = _candidate()
    candidate["risk_level"] = "high"

    error = _assert_error("candidate_not_accepted", candidate)

    assert error.reasons == ("risk_level_not_allowed:high",)
    assert not hasattr(error, "human_review_outcome_candidate")


def test_forced_invalid_intermediate_fails_before_later_stage(monkeypatch):
    later_called = False

    def invalid_queue_validation(item):
        return {"valid": False, "errors": ["forced_invalid"]}

    def forbidden_later_call(item, reviewer=None):
        nonlocal later_called
        later_called = True
        raise AssertionError("later stage must not run")

    monkeypatch.setattr(slice_module, "validate_review_queue_item", invalid_queue_validation)
    monkeypatch.setattr(slice_module, "evaluate_review_queue_item", forbidden_later_call)

    error = _assert_error("invalid_intermediate_artifact")

    assert error.stage == "review_queue_item"
    assert error.reasons == ("forced_invalid",)
    assert later_called is False


def test_no_result_marks_promotion_state_true():
    _assert_no_promotion_true(_run())


def test_no_real_proposal_artifacts_appear():
    result = _run()

    assert "real_proposal_creation_plan" not in result
    assert "real_proposal_dry_run" not in result
    assert "adopted_memory" not in result
    assert "execution_result" not in result
    assert result["no_write_guarantees"] == {
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


def test_runtime_creates_no_files_or_hermes_home_state(tmp_path, monkeypatch):
    hermes_home = tmp_path / "hermes-home"
    monkeypatch.setenv("HERMES_HOME", str(hermes_home))
    monkeypatch.chdir(tmp_path)
    before = _all_files(tmp_path)

    result = _run()

    after = _all_files(tmp_path)
    assert before == after == set()
    assert not (tmp_path / ".local").exists()
    assert not hermes_home.exists()
    forbidden_fragments = {
        "memory",
        "graph",
        "sqlite",
        "proposal",
        "ledger",
        "approval",
        "audit",
        "token",
        "config",
        "cache",
        "migration",
        "tombstone",
    }
    assert not any(
        fragment in str(path).lower()
        for path in after
        for fragment in forbidden_fragments
    )
    _assert_no_promotion_true(result)


def test_exact_signature_rejects_extra_continuation_argument():
    with pytest.raises(TypeError):
        run_governed_memory_learning_slice(
            _candidate(),
            project_id=PROJECT_ID,
            reviewer=REVIEWER,
            outcome=OUTCOME,
            rationale=RATIONALE,
            input_classification="SYNTHETIC",
            continuation=True,
        )


def test_returned_output_mutations_do_not_mutate_caller_input():
    candidate = _candidate()
    before = deepcopy(candidate)
    result = _run(candidate)

    result["candidate_snapshot"]["provenance"]["method"] = "mutated"
    result["declared_provenance"]["declared_by"] = "mutated"
    result["memory_block_candidate"]["metadata"]["provenance"]["method"] = "mutated"

    assert candidate == before
