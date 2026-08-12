from __future__ import annotations

import io
import json
import traceback
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest

import hermes_memory_fabric.p4_m0_subspace_operator as operator_module
import hermes_memory_fabric.r7_project_continuity_control_surface as surface_module
from hermes_memory_fabric.p4_m0_subspace_operator import run_operator_command
from hermes_memory_fabric.r7_project_continuity_control_surface import (
    R7ProjectContinuityControlSurfaceError,
    run_r7_project_continuity_control_surface,
    validate_correction_record,
    validate_revocation_record,
)


PROJECT_ID = "CIVILIZATION-CORE"
OPERATOR = "FOUNDER-OPERATOR"
LARGE_INTEGER_FIXTURE = 10**400


def _candidate() -> dict[str, Any]:
    return {
        "id": "cc-r7-candidate-1",
        "content": (
            "Civilization Core project continuity candidate memory with "
            "declared evidence."
        ),
        "project_id": PROJECT_ID,
        "entity_ids": [PROJECT_ID],
        "source": "declared-test-input",
        "source_id": "cc-r7-source-1",
        "provenance": {
            "kind": "declared-operator-input",
            "reference": "cc-r7-source-1",
        },
        "risk_level": "low",
        "governance": {
            "dry_run": True,
            "read_only": True,
            "proposal_governed": True,
        },
        "created_at": "2026-08-10T00:00:00Z",
        "tags": ["project-continuity"],
    }


def _kwargs(**overrides: Any) -> dict[str, Any]:
    values = {
        "query": "Civilization Core project continuity",
        "project_id": PROJECT_ID,
        "operator": OPERATOR,
        "outcome": "defer",
        "rationale": "Founder-operator defers durable adoption.",
        "corrected_outcome": "request_changes",
        "correction_rationale": (
            "Superseding non-applied outcome corrects the review disposition."
        ),
        "revocation_rationale": (
            "Terminal read-only revocation of the corrected outcome."
        ),
        "input_classification": "SYNTHETIC",
        "confirm_human_review": True,
        "confirm_scope_check": True,
        "confirm_correction": True,
        "confirm_revocation": True,
        "confirm_no_apply": True,
    }
    values.update(overrides)
    return values


def _real_use_result_snapshot(
    *,
    baseline_available: bool = True,
) -> dict[str, Any]:
    snapshot = {
        "task_completed": True,
        "state_traceable": True,
        "human_correction_count": 1,
        "recovery_time_seconds": 600.0,
        "governance_burden_worthwhile": True,
        "baseline_available": baseline_available,
    }
    if baseline_available:
        snapshot.update(
            {
                "baseline_human_correction_count": 3,
                "baseline_recovery_time_seconds": 900.0,
            }
        )
    return snapshot


def _run(candidate: dict[str, Any] | None = None, **overrides: Any) -> dict[str, Any]:
    return run_r7_project_continuity_control_surface(
        _candidate() if candidate is None else candidate,
        **_kwargs(**overrides),
    )


def _cli_argv(
    workspace: Path,
    *,
    candidate_json: str | None = None,
    real_use_result_json: str | None = None,
) -> list[str]:
    values = _kwargs()
    argv = [
        "continuity",
        "--workspace-root",
        str(workspace),
        "--project-id",
        PROJECT_ID,
        "--operator",
        OPERATOR,
        "--query",
        values["query"],
        "--candidate-json",
        candidate_json
        if candidate_json is not None
        else json.dumps(_candidate(), sort_keys=True, separators=(",", ":")),
    ]
    if real_use_result_json is not None:
        argv.extend(["--real-use-result-json", real_use_result_json])
    argv.extend(
        [
        "--outcome",
        values["outcome"],
        "--rationale",
        values["rationale"],
        "--corrected-outcome",
        values["corrected_outcome"],
        "--correction-rationale",
        values["correction_rationale"],
        "--revocation-rationale",
        values["revocation_rationale"],
        "--input-classification",
        values["input_classification"],
        "--confirm-human-review",
        "--confirm-scope-check",
        "--confirm-correction",
        "--confirm-revocation",
        "--confirm-no-apply",
        ]
    )
    return argv


def _run_cli(
    workspace: Path,
    *,
    candidate_json: str | None = None,
    real_use_result_json: str | None = None,
) -> tuple[int, str, str]:
    stdout = io.StringIO()
    stderr = io.StringIO()
    exit_code = run_operator_command(
        _cli_argv(
            workspace,
            candidate_json=candidate_json,
            real_use_result_json=real_use_result_json,
        ),
        stdout=stdout,
        stderr=stderr,
    )
    return exit_code, stdout.getvalue(), stderr.getvalue()


def test_value_signal_with_baseline_uses_real_governed_chain():
    snapshot = _real_use_result_snapshot()

    result = _run(real_use_result_snapshot=snapshot)

    assert result["real_use_result_snapshot"] == snapshot
    assert result["value_signal_assessment"] == {
        "assessment_status": "validated",
        "baseline_available": True,
        "task_completion": True,
        "state_traceability": True,
        "reduced_human_correction": True,
        "shortened_recovery_time": True,
        "governance_burden_worthwhile": True,
        "benefit_inference_allowed": False,
    }
    assert result["active_context_validation"] == {"valid": True, "errors": []}
    governed = result["governed_memory_learning_slice"]
    assert governed["terminal_artifact"] == "human_review_outcome_candidate"
    assert result["correction_record"]["supersedes_outcome_id"] == governed[
        "human_review_outcome_candidate"
    ]["outcome_id"]
    assert result["revocation_record"]["outcome_lineage"][1]["record_id"] == (
        result["correction_record"]["correction_id"]
    )
    assert result["terminal"] is True
    assert result["non_applied"] is True
    assert result["non_persisted"] is True
    assert result["continuation_authorized"] is False


def test_value_signal_without_baseline_is_deterministic_non_comparative():
    snapshot = _real_use_result_snapshot(baseline_available=False)
    snapshot["recovery_time_seconds"] = LARGE_INTEGER_FIXTURE

    first = _run(real_use_result_snapshot=snapshot)
    second = _run(real_use_result_snapshot=snapshot)

    expected = {
        "assessment_status": "baseline-unavailable",
        "baseline_available": False,
        "task_completion": True,
        "state_traceability": True,
        "reduced_human_correction": None,
        "shortened_recovery_time": None,
        "governance_burden_worthwhile": True,
        "benefit_inference_allowed": False,
    }
    assert first["real_use_result_snapshot"] == snapshot
    assert second["real_use_result_snapshot"] == snapshot
    assert first["value_signal_assessment"] == expected
    assert second["value_signal_assessment"] == expected


def test_baseline_unavailable_is_not_validation_failure():
    result = _run(
        real_use_result_snapshot=_real_use_result_snapshot(
            baseline_available=False
        )
    )
    assert result["value_signal_assessment"]["assessment_status"] == (
        "baseline-unavailable"
    )
    without_snapshot = _run()
    assert "real_use_result_snapshot" not in without_snapshot
    assert "value_signal_assessment" not in without_snapshot

    invalid = _real_use_result_snapshot()
    invalid.pop("baseline_recovery_time_seconds")
    with pytest.raises(R7ProjectContinuityControlSurfaceError) as captured:
        _run(real_use_result_snapshot=invalid)
    assert captured.value.code == "real-use-result-snapshot-invalid"
    assert captured.value.stage == "value-signal-validation"
    assert captured.value.reasons == ("field-set-invalid",)

    invalid_candidate = _candidate()
    invalid_candidate["project_id"] = "another-project"
    with pytest.raises(R7ProjectContinuityControlSurfaceError) as candidate_only:
        _run(invalid_candidate)
    with pytest.raises(R7ProjectContinuityControlSurfaceError) as dual_invalid:
        _run(invalid_candidate, real_use_result_snapshot=invalid)
    assert (
        dual_invalid.value.code,
        dual_invalid.value.stage,
        dual_invalid.value.reasons,
    ) == (
        candidate_only.value.code,
        candidate_only.value.stage,
        candidate_only.value.reasons,
    )

    with pytest.raises(R7ProjectContinuityControlSurfaceError) as no_apply:
        _run(confirm_no_apply=False, real_use_result_snapshot=invalid)
    assert no_apply.value.code == "confirm_no_apply_required"
    assert no_apply.value.stage == "no-apply"
    assert no_apply.value.reasons == ()


@pytest.mark.parametrize(
    ("mutation", "expected_reasons"),
    [
        ("missing", ("field-set-invalid",)),
        ("unknown", ("field-set-invalid",)),
        ("boolean", ("task-completed-invalid",)),
        (
            "numeric",
            (
                "human-correction-count-invalid",
                "recovery-time-seconds-invalid",
                "baseline-human-correction-count-invalid",
                "baseline-recovery-time-seconds-invalid",
            ),
        ),
    ],
)
def test_real_use_snapshot_schema_rejections_are_stable_and_sanitized(
    mutation: str,
    expected_reasons: tuple[str, ...],
    tmp_path: Path,
    monkeypatch,
):
    deepcopy_calls = 0

    class DeepcopyTrap:
        def __deepcopy__(self, memo: dict[int, Any]) -> Any:
            nonlocal deepcopy_calls
            deepcopy_calls += 1
            raise AssertionError("unvalidated snapshot value was deep-copied")

    snapshot = _real_use_result_snapshot()
    if mutation == "missing":
        snapshot.pop("task_completed")
    elif mutation == "unknown":
        snapshot["governance_burden_seconds"] = 17
    elif mutation == "boolean":
        snapshot["task_completed"] = DeepcopyTrap()
    else:
        snapshot["human_correction_count"] = -1
        snapshot["recovery_time_seconds"] = "invalid-sensitive-value"
        snapshot["baseline_human_correction_count"] = -2
        snapshot["baseline_recovery_time_seconds"] = -3.0
    before = dict(snapshot)
    candidate = _candidate()
    candidate["content"] = "snapshot-candidate-content-must-not-leak"
    calls = {
        "provider": 0,
        "governed": 0,
        "correction_validation": 0,
        "revocation_validation": 0,
    }

    def unexpected_provider(*args: Any, **kwargs: Any) -> Any:
        calls["provider"] += 1
        raise AssertionError("provider called for invalid snapshot")

    def unexpected_governed(*args: Any, **kwargs: Any) -> Any:
        calls["governed"] += 1
        raise AssertionError("governed chain called for invalid snapshot")

    def unexpected_correction_validation(*args: Any, **kwargs: Any) -> Any:
        calls["correction_validation"] += 1
        raise AssertionError("correction validation called for invalid snapshot")

    def unexpected_revocation_validation(*args: Any, **kwargs: Any) -> Any:
        calls["revocation_validation"] += 1
        raise AssertionError("revocation validation called for invalid snapshot")

    monkeypatch.setattr(
        surface_module.MemoryFabricProvider,
        "build_active_context",
        unexpected_provider,
    )
    monkeypatch.setattr(
        surface_module,
        "run_governed_memory_learning_slice",
        unexpected_governed,
    )
    monkeypatch.setattr(
        surface_module,
        "validate_correction_record",
        unexpected_correction_validation,
    )
    monkeypatch.setattr(
        surface_module,
        "validate_revocation_record",
        unexpected_revocation_validation,
    )

    with pytest.raises(R7ProjectContinuityControlSurfaceError) as captured:
        _run(candidate, real_use_result_snapshot=snapshot)

    error = captured.value
    assert error.code == "real-use-result-snapshot-invalid"
    assert error.stage == "value-signal-validation"
    assert error.reasons == expected_reasons
    assert snapshot == before
    assert deepcopy_calls == 0
    assert calls == {
        "provider": 0,
        "governed": 0,
        "correction_validation": 0,
        "revocation_validation": 0,
    }
    assert error.__context__ is None
    assert error.__cause__ is None
    rendered = str(error)
    assert "governance_burden_seconds" not in rendered
    assert "invalid-sensitive-value" not in rendered
    assert candidate["content"] not in rendered
    formatted_traceback = "".join(
        traceback.format_exception(type(error), error, error.__traceback__)
    )
    assert "AssertionError" not in formatted_traceback
    assert "unvalidated snapshot value was deep-copied" not in formatted_traceback
    assert candidate["content"] not in formatted_traceback

    workspace = tmp_path / "fresh-workspace"
    workspace.mkdir()
    cli_snapshot = dict(snapshot)
    if mutation == "boolean":
        cli_snapshot["task_completed"] = 1
    exit_code, stdout, stderr = _run_cli(
        workspace,
        candidate_json=json.dumps(candidate, separators=(",", ":")),
        real_use_result_json=json.dumps(cli_snapshot, separators=(",", ":")),
    )
    assert exit_code == 1
    assert stdout == ""
    assert stderr == f"{error}\n"
    assert "governance_burden_seconds" not in stderr
    assert "invalid-sensitive-value" not in stderr
    assert candidate["content"] not in stderr
    assert deepcopy_calls == 0
    assert calls == {
        "provider": 0,
        "governed": 0,
        "correction_validation": 0,
        "revocation_validation": 0,
    }
    assert list(workspace.iterdir()) == []


@pytest.mark.parametrize("non_finite", [float("nan"), float("inf"), float("-inf")])
def test_real_use_snapshot_rejects_non_finite_api_and_cli(
    non_finite: float,
    tmp_path: Path,
):
    snapshot = _real_use_result_snapshot()
    snapshot["recovery_time_seconds"] = non_finite

    with pytest.raises(R7ProjectContinuityControlSurfaceError) as captured:
        _run(real_use_result_snapshot=snapshot)
    assert captured.value.code == "real-use-result-snapshot-invalid"
    assert captured.value.stage == "value-signal-validation"
    assert captured.value.reasons == ("recovery-time-seconds-invalid",)

    workspace = tmp_path / "fresh-workspace"
    workspace.mkdir()
    exit_code, stdout, stderr = _run_cli(
        workspace,
        real_use_result_json=json.dumps(snapshot, separators=(",", ":")),
    )
    assert exit_code == 1
    assert stdout == ""
    assert stderr == "real_use_result_json_non_finite_constant_not_allowed\n"
    assert list(workspace.iterdir()) == []


def test_real_use_snapshot_is_unchanged_deep_copied_and_repeatable():
    snapshot = _real_use_result_snapshot()
    before = deepcopy(snapshot)

    first = _run(real_use_result_snapshot=snapshot)
    second = _run(real_use_result_snapshot=snapshot)

    assert snapshot == before
    assert first == second
    assert first["real_use_result_snapshot"] is not snapshot
    first["real_use_result_snapshot"]["human_correction_count"] = 99
    assert snapshot == before
    assert second["real_use_result_snapshot"] == before


def test_continuity_cli_value_signal_single_json_and_zero_storage(
    tmp_path,
    monkeypatch,
):
    workspace = tmp_path / "fresh-workspace"
    workspace.mkdir()

    def forbidden_store(*args: Any, **kwargs: Any) -> Any:
        raise AssertionError("continuity route must not construct a persistent store")

    monkeypatch.setattr(
        operator_module,
        "create_workspace_subspace_memory_store",
        forbidden_store,
    )
    snapshot = _real_use_result_snapshot(baseline_available=False)
    snapshot["recovery_time_seconds"] = LARGE_INTEGER_FIXTURE
    snapshot_json = json.dumps(snapshot, sort_keys=True, separators=(",", ":"))

    exit_code, stdout, stderr = _run_cli(
        workspace,
        real_use_result_json=snapshot_json,
    )

    assert exit_code == 0
    assert stderr == ""
    assert stdout.endswith("\n")
    assert len(stdout.splitlines()) == 1
    payload = json.loads(stdout)
    assert payload["real_use_result_snapshot"] == snapshot
    assert payload["real_use_result_snapshot"]["recovery_time_seconds"] == (
        LARGE_INTEGER_FIXTURE
    )
    assert payload["value_signal_assessment"]["assessment_status"] == (
        "baseline-unavailable"
    )
    assert payload["value_signal_assessment"]["benefit_inference_allowed"] is False
    assert payload["terminal"] is True
    assert payload["non_persisted"] is True
    assert payload["continuation_authorized"] is False
    assert "formal_closure_eligible" not in payload
    assert list(workspace.iterdir()) == []

    for invalid_json_object in ("[]", "0", "null"):
        invalid_exit, invalid_stdout, invalid_stderr = _run_cli(
            workspace,
            real_use_result_json=invalid_json_object,
        )
        assert invalid_exit == 1
        assert invalid_stdout == ""
        assert invalid_stderr == "real_use_result_json_must_be_json_object\n"
        assert list(workspace.iterdir()) == []


def test_civilization_core_only_and_single_candidate_workflow():
    result = _run()

    assert result["project_id"] == PROJECT_ID
    assert result["operator"] == OPERATOR
    assert result["workflow"] == [
        "candidate-memory",
        "evidence",
        "human-review",
        "scope-check",
        "correct",
        "revoke",
    ]
    assert len(result["active_context_packet"]["selected_memories"]) == 1
    assert (
        result["active_context_packet"]["selected_memories"][0]["id"]
        == _candidate()["id"]
    )

    with pytest.raises(R7ProjectContinuityControlSurfaceError):
        _run(project_id="another-project")
    with pytest.raises(R7ProjectContinuityControlSurfaceError):
        _run(operator="another-operator")
    wrong_project = _candidate()
    wrong_project["project_id"] = "another-project"
    with pytest.raises(R7ProjectContinuityControlSurfaceError):
        _run(wrong_project)


def test_provider_packet_and_governed_chain_are_reused(monkeypatch):
    calls: dict[str, Any] = {"provider": 0, "governed": 0}
    original_build = surface_module.MemoryFabricProvider.build_active_context
    original_governed = surface_module.run_governed_memory_learning_slice

    def tracked_build(self: Any, **kwargs: Any) -> dict[str, Any]:
        calls["provider"] += 1
        calls["provider_kwargs"] = deepcopy(kwargs)
        return original_build(self, **kwargs)

    def tracked_governed(candidate: Any, **kwargs: Any) -> dict[str, Any]:
        calls["governed"] += 1
        calls["governed_candidate"] = deepcopy(candidate)
        calls["governed_kwargs"] = deepcopy(kwargs)
        return original_governed(candidate, **kwargs)

    monkeypatch.setattr(
        surface_module.MemoryFabricProvider,
        "build_active_context",
        tracked_build,
    )
    monkeypatch.setattr(
        surface_module,
        "run_governed_memory_learning_slice",
        tracked_governed,
    )

    result = _run()

    assert calls["provider"] == 1
    assert calls["provider_kwargs"]["project_scope"] == PROJECT_ID
    assert calls["provider_kwargs"]["query"] == _kwargs()["query"]
    assert calls["provider_kwargs"]["memory_candidates"] == [_candidate()]
    assert result["active_context_validation"] == {"valid": True, "errors": []}
    assert calls["governed"] == 1
    assert calls["governed_candidate"] == _candidate()
    assert calls["governed_kwargs"] == {
        "project_id": PROJECT_ID,
        "reviewer": OPERATOR,
        "outcome": "defer",
        "rationale": _kwargs()["rationale"],
        "input_classification": "SYNTHETIC",
    }
    governed = result["governed_memory_learning_slice"]
    assert governed["terminal_artifact"] == "human_review_outcome_candidate"
    assert governed["continuation_authorized"] is False
    assert governed["non_authoritative"] is True
    assert governed["non_applied"] is True
    assert governed["non_persisted"] is True


def test_correction_record_supersedes_prior_outcome():
    result = _run()
    governed_outcome = result["governed_memory_learning_slice"][
        "human_review_outcome_candidate"
    ]
    correction = result["correction_record"]

    assert correction["supersedes_outcome_id"] == governed_outcome["outcome_id"]
    assert correction["prior_outcome"] == governed_outcome["outcome"] == "defer"
    assert correction["corrected_outcome"] == "request_changes"
    assert governed_outcome["outcome"] == "defer"
    assert validate_correction_record(correction) == {"valid": True, "errors": []}


def test_revocation_record_is_terminal_non_applied_and_traces_corrected_outcome():
    result = _run()
    correction = result["correction_record"]
    revocation = result["revocation_record"]

    assert revocation["revokes_record_id"] == correction["correction_id"]
    assert revocation["correction_id"] == correction["correction_id"]
    assert (
        revocation["original_outcome_id"]
        == correction["supersedes_outcome_id"]
    )
    assert [entry["stage"] for entry in revocation["outcome_lineage"]] == [
        "human-review",
        "correct",
        "revoke",
    ]
    assert revocation["outcome_lineage"][1]["outcome"] == "request_changes"
    assert revocation["terminal"] is True
    assert revocation["non_applied"] is True
    assert revocation["non_persisted"] is True
    assert revocation["continuation_authorized"] is False
    assert validate_revocation_record(revocation) == {"valid": True, "errors": []}


def test_input_is_not_mutated():
    candidate = _candidate()
    before = deepcopy(candidate)

    result = _run(candidate)

    assert candidate == before
    result["candidate_snapshot"]["provenance"]["reference"] = "changed"
    assert candidate == before


def test_output_is_deterministic():
    first = _run()
    second = _run()

    assert first == second
    assert json.dumps(first, sort_keys=True, separators=(",", ":")) == json.dumps(
        second,
        sort_keys=True,
        separators=(",", ":"),
    )


@pytest.mark.parametrize(
    ("confirmation", "stage"),
    [
        ("confirm_human_review", "human-review"),
        ("confirm_scope_check", "scope-check"),
        ("confirm_correction", "correct"),
        ("confirm_revocation", "revoke"),
        ("confirm_no_apply", "no-apply"),
    ],
)
def test_each_required_confirmation_fails_closed(confirmation: str, stage: str):
    with pytest.raises(R7ProjectContinuityControlSurfaceError) as captured:
        _run(**{confirmation: False})

    assert captured.value.code == f"{confirmation}_required"
    assert captured.value.stage == stage


def test_no_automatic_collection_write_approval_adoption_execution_or_continuation():
    result = _run()

    for field in (
        "automatic_collection",
        "automatic_write",
        "automatic_approval",
        "automatic_adoption",
        "automatic_execution",
        "automatic_continuation",
        "continuation_authorized",
    ):
        assert result[field] is False
    assert result["terminal"] is True
    assert result["non_authoritative"] is True
    assert result["non_applied"] is True
    assert result["non_persisted"] is True
    guarantees = result["governed_memory_learning_slice"]["no_write_guarantees"]
    assert guarantees["writes_memory"] is False
    assert guarantees["writes_graph"] is False
    assert guarantees["writes_sqlite"] is False
    assert guarantees["applies_proposals"] is False
    assert guarantees["adopts_memory"] is False
    assert guarantees["executes_actions"] is False


def test_fresh_workspace_remains_empty(tmp_path):
    workspace = tmp_path / "fresh-workspace"
    workspace.mkdir()

    _run()
    assert list(workspace.iterdir()) == []

    exit_code, stdout, stderr = _run_cli(workspace)
    assert exit_code == 0
    assert stderr == ""
    assert json.loads(stdout)["status"] == (
        "complete-terminal-non-applied-revocation"
    )
    assert list(workspace.iterdir()) == []


def test_continuity_cli_route_writes_stdout_only(tmp_path):
    workspace = tmp_path / "fresh-workspace"
    workspace.mkdir()

    exit_code, stdout, stderr = _run_cli(workspace)

    assert exit_code == 0
    assert stderr == ""
    assert len(stdout.splitlines()) == 1
    payload = json.loads(stdout)
    assert payload["runtime_surface"] == "r7_project_continuity_control_surface"
    assert payload["revocation_record"]["terminal"] is True
    assert list(workspace.iterdir()) == []


def test_continuity_cli_does_not_construct_persistent_store(tmp_path, monkeypatch):
    workspace = tmp_path / "fresh-workspace"
    workspace.mkdir()

    def forbidden_store(*args: Any, **kwargs: Any) -> Any:
        raise AssertionError("continuity route must not construct a persistent store")

    monkeypatch.setattr(
        operator_module,
        "create_workspace_subspace_memory_store",
        forbidden_store,
    )

    exit_code, stdout, stderr = _run_cli(workspace)

    assert exit_code == 0
    assert stderr == ""
    assert json.loads(stdout)["terminal"] is True
    assert list(workspace.iterdir()) == []
    parsed_existing = operator_module.build_parser().parse_args(
        ["audit", "--workspace-root", str(workspace)]
    )
    assert parsed_existing.command == "audit"


def test_governed_slice_rejection_is_translated_to_route_error(tmp_path):
    workspace = tmp_path / "fresh-workspace"
    workspace.mkdir()
    expected_stderr = (
        "r7_project_continuity_control_surface_error:"
        "code=governed_slice_rejected;stage=human-review;"
        "reasons=governed_slice_rejection_details_withheld\n"
    )

    governance_candidate = _candidate()
    governance_candidate["content"] = "candidate-content-must-not-leak"
    governance_candidate["governance"]["dry_run"] = False

    risk_level_sentinel = "r7-review-001-risk-sentinel-9f8a"
    injected_field = "injected_field=r7-review-001-must-not-appear"
    dynamic_risk_level = f"blocked-{risk_level_sentinel}\n{injected_field}"
    risk_candidate = _candidate()
    risk_candidate["content"] = "dynamic-candidate-content-must-not-leak"
    risk_candidate["risk_level"] = dynamic_risk_level

    scenarios = (
        (governance_candidate, (governance_candidate["content"],)),
        (
            risk_candidate,
            (
                risk_candidate["content"],
                risk_level_sentinel,
                injected_field,
                f"risk_level_not_allowed:{dynamic_risk_level}",
                "risk_level_not_allowed",
            ),
        ),
    )

    with pytest.raises(R7ProjectContinuityControlSurfaceError) as exc_info:
        _run(risk_candidate)

    error = exc_info.value
    assert error.code == "governed_slice_rejected"
    assert error.stage == "human-review"
    assert error.reasons == ("governed_slice_rejection_details_withheld",)
    assert error.__context__ is None
    assert error.__cause__ is None

    formatted_traceback = "".join(
        traceback.format_exception(type(error), error, error.__traceback__)
    )
    assert "GovernedMemoryLearningSliceError" not in formatted_traceback
    assert "governed_memory_learning_slice_error" not in formatted_traceback
    assert risk_level_sentinel not in formatted_traceback
    assert injected_field not in formatted_traceback
    assert risk_candidate["content"] not in formatted_traceback
    assert formatted_traceback.count(
        "r7_project_continuity_control_surface_error:"
    ) == 1
    assert str(error) in formatted_traceback

    for candidate, forbidden_fragments in scenarios:
        exit_code, stdout, stderr = _run_cli(
            workspace,
            candidate_json=json.dumps(candidate, sort_keys=True, separators=(",", ":")),
        )

        assert exit_code == 1
        assert stdout == ""
        assert stderr == expected_stderr
        assert "Traceback" not in stderr
        for forbidden_fragment in forbidden_fragments:
            assert forbidden_fragment not in stderr
        assert list(workspace.iterdir()) == []


def test_record_validators_reject_contradictory_affirmative_state_flags():
    result = _run()
    records_and_validators = (
        (result["correction_record"], validate_correction_record),
        (result["revocation_record"], validate_revocation_record),
    )
    contradictory_fields = (
        "authoritative",
        "applied",
        "persisted",
        "approved",
        "adopted",
        "executed",
        "created_real_proposal",
        "creates_real_proposal",
    )

    for original, validator in records_and_validators:
        original_snapshot = deepcopy(original)
        assert validator(original) == {"valid": True, "errors": []}

        for field in contradictory_fields:
            contradictory = deepcopy(original)
            contradictory[field] = True
            before_validation = deepcopy(contradictory)

            validation = validator(contradictory)

            assert validation["valid"] is False
            assert f"{field}_must_not_be_true" in validation["errors"]
            assert contradictory == before_validation

            non_contradictory = deepcopy(original)
            non_contradictory[field] = False
            assert validator(non_contradictory) == {"valid": True, "errors": []}
            assert non_contradictory.get("correction_id") == original.get(
                "correction_id"
            )
            assert non_contradictory.get("revocation_id") == original.get(
                "revocation_id"
            )
            assert non_contradictory.get("outcome_lineage") == original.get(
                "outcome_lineage"
            )

        assert original == original_snapshot


def test_continuity_cli_rejects_non_finite_json_constants(tmp_path):
    workspace = tmp_path / "fresh-workspace"
    workspace.mkdir()

    for non_finite in (float("nan"), float("inf"), float("-inf")):
        candidate = _candidate()
        candidate["content"] = "non-finite-candidate-content-must-not-leak"
        candidate["non_finite"] = non_finite
        candidate_json = json.dumps(candidate, sort_keys=True, separators=(",", ":"))

        exit_code, stdout, stderr = _run_cli(
            workspace,
            candidate_json=candidate_json,
        )

        assert exit_code == 1
        assert stdout == ""
        assert stderr == "candidate_json_non_finite_constant_not_allowed\n"
        assert "Traceback" not in stderr
        assert candidate["content"] not in stderr
        assert list(workspace.iterdir()) == []
