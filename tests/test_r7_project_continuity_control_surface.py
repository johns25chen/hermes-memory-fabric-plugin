from __future__ import annotations

import io
import json
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


def _run(candidate: dict[str, Any] | None = None, **overrides: Any) -> dict[str, Any]:
    return run_r7_project_continuity_control_surface(
        _candidate() if candidate is None else candidate,
        **_kwargs(**overrides),
    )


def _cli_argv(workspace: Path) -> list[str]:
    values = _kwargs()
    return [
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
        json.dumps(_candidate(), sort_keys=True, separators=(",", ":")),
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


def _run_cli(workspace: Path) -> tuple[int, str, str]:
    stdout = io.StringIO()
    stderr = io.StringIO()
    exit_code = run_operator_command(
        _cli_argv(workspace),
        stdout=stdout,
        stderr=stderr,
    )
    return exit_code, stdout.getvalue(), stderr.getvalue()


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
