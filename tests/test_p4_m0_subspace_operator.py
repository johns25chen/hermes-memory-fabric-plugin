from __future__ import annotations

import io
import json
import tomllib
from pathlib import Path

from hermes_memory_fabric.p4_m0_subspace_operator import run_operator_command
from hermes_memory_fabric.p4_m0_subspace_workspace import create_workspace_subspace_memory_store


def _run(argv: list[str]) -> tuple[int, dict[str, object], str]:
    stdout = io.StringIO()
    stderr = io.StringIO()

    exit_code = run_operator_command(argv, stdout=stdout, stderr=stderr)

    payload = json.loads(stdout.getvalue()) if stdout.getvalue() else {}
    return exit_code, payload, stderr.getvalue()


def test_propose_command_creates_pending_proposal_json_output_and_audit_event(tmp_path):
    exit_code, payload, stderr = _run(
        [
            "propose",
            "--workspace-root",
            str(tmp_path),
            "--project",
            "hermes-memory-fabric",
            "--namespace",
            "operator",
            "--content",
            "Manual operator propose creates a pending proposal.",
            "--source",
            "unit-test",
            "--tag",
            "manual",
            "--confidence",
            "0.9",
        ]
    )

    assert exit_code == 0
    assert stderr == ""
    assert payload["status"] == "pending"
    assert payload["project"] == "hermes-memory-fabric"
    assert payload["namespace"] == "operator"
    assert payload["storage_root"] == str(tmp_path / ".local" / "subspace_memory")
    store = create_workspace_subspace_memory_store(tmp_path)
    assert [event.event_type for event in store.list_audit_events()] == ["proposal_created"]


def test_approve_command_creates_approved_memory_json_output(tmp_path):
    proposal_id = _propose(tmp_path, content="Approve command creates approved memory.")

    exit_code, payload, stderr = _run(
        [
            "approve",
            "--workspace-root",
            str(tmp_path),
            "--proposal-id",
            proposal_id,
            "--approver",
            "human",
            "--note",
            "approved locally",
        ]
    )

    assert exit_code == 0
    assert stderr == ""
    assert payload["status"] == "approved"
    assert payload["proposal_id"] == proposal_id
    assert isinstance(payload["memory_id"], str)
    assert payload["storage_root"] == str(tmp_path / ".local" / "subspace_memory")


def test_reject_command_rejects_proposal_and_rejected_content_is_not_recalled(tmp_path):
    proposal_id = _propose(tmp_path, content="Rejected operator content must not be recalled.")

    exit_code, payload, stderr = _run(
        [
            "reject",
            "--workspace-root",
            str(tmp_path),
            "--proposal-id",
            proposal_id,
            "--reviewer",
            "human",
            "--reason",
            "not suitable",
        ]
    )
    recall_code, recall_payload, recall_stderr = _run(
        [
            "recall",
            "--workspace-root",
            str(tmp_path),
            "--query",
            "rejected operator",
            "--project",
            "hermes-memory-fabric",
            "--namespace",
            "operator",
        ]
    )

    assert exit_code == 0
    assert stderr == ""
    assert payload["status"] == "rejected"
    assert payload["reason"] == "not suitable"
    assert recall_code == 0
    assert recall_stderr == ""
    assert recall_payload["count"] == 0
    assert recall_payload["results"] == []


def test_recall_command_returns_approved_memory_with_deterministic_json_output(tmp_path):
    proposal_id = _propose(tmp_path, content="Deterministic recall returns approved operator memory.")
    _run(
        [
            "approve",
            "--workspace-root",
            str(tmp_path),
            "--proposal-id",
            proposal_id,
            "--approver",
            "human",
        ]
    )

    exit_code, payload, stderr = _run(
        [
            "recall",
            "--workspace-root",
            str(tmp_path),
            "--query",
            "deterministic approved",
            "--project",
            "hermes-memory-fabric",
            "--namespace",
            "operator",
            "--limit",
            "5",
        ]
    )

    assert exit_code == 0
    assert stderr == ""
    assert payload["query"] == "deterministic approved"
    assert payload["count"] == 1
    assert payload["storage_root"] == str(tmp_path / ".local" / "subspace_memory")
    assert payload["results"] == [
        {
            "content": "Deterministic recall returns approved operator memory.",
            "matched_terms": ["deterministic", "approved"],
            "memory_id": payload["results"][0]["memory_id"],
            "namespace": "operator",
            "project": "hermes-memory-fabric",
            "score": 2,
            "source": "operator-test",
        }
    ]


def test_audit_command_returns_audit_events(tmp_path):
    proposal_id = _propose(tmp_path, content="Audit command lists events.")
    _run(
        [
            "approve",
            "--workspace-root",
            str(tmp_path),
            "--proposal-id",
            proposal_id,
            "--approver",
            "human",
        ]
    )

    exit_code, payload, stderr = _run(["audit", "--workspace-root", str(tmp_path)])

    assert exit_code == 0
    assert stderr == ""
    assert payload["count"] == 2
    assert [event["event_type"] for event in payload["events"]] == [
        "proposal_created",
        "proposal_approved",
    ]


def test_default_workspace_root_uses_local_subspace_memory(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    exit_code, payload, stderr = _run(
        [
            "propose",
            "--project",
            "hermes-memory-fabric",
            "--namespace",
            "operator",
            "--content",
            "Default workspace root uses local subspace memory.",
        ]
    )

    assert exit_code == 0
    assert stderr == ""
    assert payload["storage_root"] == str(tmp_path / ".local" / "subspace_memory")
    assert (tmp_path / ".local" / "subspace_memory" / "proposals.jsonl").exists()


def test_explicit_workspace_root_works(tmp_path):
    workspace = tmp_path / "workspace"
    workspace.mkdir()

    exit_code, payload, stderr = _run(
        [
            "propose",
            "--workspace-root",
            str(workspace),
            "--project",
            "hermes-memory-fabric",
            "--namespace",
            "operator",
            "--content",
            "Explicit workspace root is honored.",
        ]
    )

    assert exit_code == 0
    assert stderr == ""
    assert payload["storage_root"] == str(workspace / ".local" / "subspace_memory")
    assert (workspace / ".local" / "subspace_memory" / "proposals.jsonl").exists()


def test_recall_and_audit_commands_do_not_create_additional_memory_records(tmp_path):
    proposal_id = _propose(tmp_path, content="Read commands must not create memory records.")
    _run(
        [
            "approve",
            "--workspace-root",
            str(tmp_path),
            "--proposal-id",
            proposal_id,
            "--approver",
            "human",
        ]
    )
    memories_path = tmp_path / ".local" / "subspace_memory" / "memories.jsonl"
    before = memories_path.read_text(encoding="utf-8")

    recall_code, _, recall_stderr = _run(
        ["recall", "--workspace-root", str(tmp_path), "--query", "read commands"]
    )
    audit_code, _, audit_stderr = _run(["audit", "--workspace-root", str(tmp_path)])

    assert recall_code == 0
    assert recall_stderr == ""
    assert audit_code == 0
    assert audit_stderr == ""
    assert memories_path.read_text(encoding="utf-8") == before


def test_missing_required_args_return_non_zero_with_stderr(tmp_path):
    stdout = io.StringIO()
    stderr = io.StringIO()

    exit_code = run_operator_command(
        ["approve", "--workspace-root", str(tmp_path), "--proposal-id", "proposal:missing"],
        stdout=stdout,
        stderr=stderr,
    )

    assert exit_code != 0
    assert stdout.getvalue() == ""
    assert "the following arguments are required: --approver" in stderr.getvalue()


def test_package_version_remains_6_16_0():
    with open("pyproject.toml", "rb") as handle:
        pyproject = tomllib.load(handle)

    assert pyproject["project"]["version"] == "6.16.0"


def test_no_uv_lock_is_created():
    assert not Path("uv.lock").exists()


def test_no_pyproject_entry_point_is_added_for_operator():
    with open("pyproject.toml", "rb") as handle:
        pyproject = tomllib.load(handle)

    assert "scripts" not in pyproject["project"]
    assert "gui-scripts" not in pyproject["project"]
    assert "console_scripts" not in pyproject["project"].get("entry-points", {})
    entry_points = json.dumps(pyproject["project"].get("entry-points", {}), sort_keys=True)
    assert "p4_m0_subspace_operator" not in entry_points


def _propose(tmp_path: Path, *, content: str) -> str:
    exit_code, payload, stderr = _run(
        [
            "propose",
            "--workspace-root",
            str(tmp_path),
            "--project",
            "hermes-memory-fabric",
            "--namespace",
            "operator",
            "--content",
            content,
            "--source",
            "operator-test",
        ]
    )
    assert exit_code == 0
    assert stderr == ""
    return str(payload["proposal_id"])
