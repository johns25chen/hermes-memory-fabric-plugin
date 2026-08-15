from __future__ import annotations

import io
import json
import tomllib
from pathlib import Path

import pytest

import hermes_memory_fabric.p4_m0_subspace_operator as operator_module
import hermes_memory_fabric.r7_project_continuity_control_surface as continuity_module
from hermes_memory_fabric.p4_m0_subspace_operator import run_operator_command
from hermes_memory_fabric.p4_m0_subspace_workspace import create_workspace_subspace_memory_store
from hermes_memory_fabric.r8_security_governance import (
    LEGACY_OPERATION,
    OBSERVATION_OPERATION,
    build_legacy_payload,
    build_observation_payload,
    canonical_payload_binding_sha256,
)


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
    memory_id = payload["results"][0]["memory_id"]
    assert payload["results"] == [
        {
            "content": "Deterministic recall returns approved operator memory.",
            "do_not_retry": None,
            "do_not_retry_warning": None,
            "matched_terms": ["deterministic", "approved"],
            "memory_id": memory_id,
            "namespace": "operator",
            "project": "hermes-memory-fabric",
            "score": 2,
            "source": "operator-test",
            "lifecycle": "active",
            "trace": {
                "explanation": "Matched 2 query terms: deterministic, approved.",
                "include_archived": False,
                "include_stale": False,
                "lifecycle": "active",
                "matched_terms": ["deterministic", "approved"],
                "memory_id": memory_id,
                "namespace": "operator",
                "project": "hermes-memory-fabric",
                "query": "deterministic approved",
                "query_terms": ["deterministic", "approved"],
                "rank": 1,
                "score": 2,
                "source": "operator-test",
            },
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


def _r8_candidate() -> dict[str, object]:
    return {
        "id": "cc-r8-candidate-1",
        "content": "R8 bounded synthetic continuity candidate.",
        "project_id": "CIVILIZATION-CORE",
        "entity_ids": ["CIVILIZATION-CORE"],
        "source": "declared-test-input",
        "source_id": "cc-r8-source-1",
        "provenance": {"kind": "declared-operator-input", "reference": "cc-r8-source-1"},
        "risk_level": "low",
        "governance": {"dry_run": True, "read_only": True, "proposal_governed": True},
        "created_at": "2026-08-15T00:00:00Z",
        "tags": ["project-continuity"],
    }


def _r8_legacy_args(
    workspace: Path, *, input_classification: str = "SYNTHETIC"
) -> tuple[list[str], dict[str, object]]:
    candidate = _r8_candidate()
    values: dict[str, object] = {
        "project_id": "CIVILIZATION-CORE",
        "operator": "FOUNDER-OPERATOR",
        "query": "R8 synthetic continuity",
        "outcome": "defer",
        "rationale": "Synthetic human review.",
        "corrected_outcome": "request_changes",
        "correction_rationale": "Synthetic correction.",
        "revocation_rationale": "Synthetic terminal revocation.",
        "input_classification": input_classification,
        "confirm_human_review": True,
        "confirm_scope_check": True,
        "confirm_correction": True,
        "confirm_revocation": True,
        "confirm_no_apply": True,
    }
    payload = build_legacy_payload(values, candidate, None)
    argv = [
        "continuity", "--workspace-root", str(workspace),
        "--project-id", str(values["project_id"]), "--operator", str(values["operator"]),
        "--query", str(values["query"]), "--candidate-json", json.dumps(candidate, separators=(",", ":")),
        "--outcome", str(values["outcome"]), "--rationale", str(values["rationale"]),
        "--corrected-outcome", str(values["corrected_outcome"]),
        "--correction-rationale", str(values["correction_rationale"]),
        "--revocation-rationale", str(values["revocation_rationale"]),
        "--input-classification", str(values["input_classification"]),
        "--confirm-human-review", "--confirm-scope-check", "--confirm-correction",
        "--confirm-revocation", "--confirm-no-apply",
    ]
    return argv, payload


def _r8_observation() -> dict[str, object]:
    return {
        "candidate": _r8_candidate(),
        "query": "R8 synthetic continuity",
        "input_classification": "SYNTHETIC",
        "human_review": {"outcome": "defer", "rationale": "Synthetic human review."},
        "correction": {"corrected_outcome": "request_changes", "rationale": "Synthetic correction."},
        "revocation": {"rationale": "Synthetic terminal revocation."},
        "measurement": {
            "human_correction_count": 0,
            "recovery_time_seconds": 10,
            "measurement_scope": "SYNTHETIC-COMMAND-INVOCATION-TO-TERMINAL",
            "caller_observed": True,
        },
        "governance_burden_worthwhile": True,
        "baseline": {"available": False},
    }


def _r8_envelope(
    payload: dict[str, object],
    *,
    operation: str,
    classification: str = "SYNTHETIC",
    source_trust: str = "LOCAL_CALLER_PROVIDED",
    source_lineage_class: str = "CALLER_SUBMISSION",
    human_decision: str = "APPROVE_READ_ONLY_EXECUTION",
) -> dict[str, object]:
    envelope: dict[str, object] = {
        "schema_name": "GOVERNED-MEMORY-SECURITY-DECISION-ENVELOPE",
        "version": "1.3",
        "operation": operation,
        "request_reference": "r8-request:fedcba9876543210fedcba9876543210",
        "payload_binding_sha256": canonical_payload_binding_sha256(payload),
        "project_id": "CIVILIZATION-CORE",
        "namespace": "R7_PROJECT_CONTINUITY",
        "operator_role": "FOUNDER-OPERATOR",
        "requested_effect": "READ_ONLY_NON_PERSISTENT_TERMINAL_ASSESSMENT",
        "security_classification": classification,
        "security_classification_source": "CALLER_DECLARATION",
        "source_trust": source_trust,
        "source_lineage_class": source_lineage_class,
        "human_decision": human_decision,
    }
    if operation == OBSERVATION_OPERATION:
        envelope["measurement_scope"] = "SYNTHETIC-COMMAND-INVOCATION-TO-TERMINAL"
        envelope["baseline_measurement_scope"] = None
    envelope["authority_attestation"] = {
        **{key: value for key, value in envelope.items() if key not in {"measurement_scope", "baseline_measurement_scope"}},
        "attestation_type": "CALLER_AUTHORITY_ATTESTATION",
        "attestation_version": "1.3",
        "attested": True,
    }
    return envelope


def _run_r8(argv: list[str]) -> tuple[int, str, str]:
    stdout = io.StringIO()
    stderr = io.StringIO()
    code = run_operator_command(argv, stdout=stdout, stderr=stderr)
    return code, stdout.getvalue(), stderr.getvalue()


def _replace_option(argv: list[str], option: str, value: str) -> None:
    argv[argv.index(option) + 1] = value


def _r8_observation_args(
    workspace: Path,
) -> tuple[list[str], dict[str, object], dict[str, object]]:
    observation = _r8_observation()
    values = {
        "project_id": "CIVILIZATION-CORE",
        "operator": "FOUNDER-OPERATOR",
        "confirm_real_use_observation": True,
    }
    payload = build_observation_payload(values, observation)
    argv = [
        "continuity",
        "--workspace-root",
        str(workspace),
        "--project-id",
        "CIVILIZATION-CORE",
        "--operator",
        "FOUNDER-OPERATOR",
        "--real-use-observation-json",
        json.dumps(observation, separators=(",", ":")),
        "--confirm-real-use-observation",
    ]
    return argv, observation, payload


def _install_r8_downstream_counters(monkeypatch) -> dict[str, int]:
    calls = {
        "provider": 0,
        "governed_memory": 0,
        "legacy": 0,
        "observation": 0,
    }
    monkeypatch.setattr(
        continuity_module,
        "MemoryFabricProvider",
        lambda: calls.__setitem__("provider", calls["provider"] + 1),
    )
    monkeypatch.setattr(
        continuity_module,
        "run_governed_memory_learning_slice",
        lambda *a, **k: calls.__setitem__(
            "governed_memory", calls["governed_memory"] + 1
        ),
    )
    monkeypatch.setattr(
        operator_module,
        "run_r7_project_continuity_control_surface",
        lambda *a, **k: calls.__setitem__("legacy", calls["legacy"] + 1),
    )
    monkeypatch.setattr(
        operator_module,
        "run_r7_real_use_observation",
        lambda *a, **k: calls.__setitem__(
            "observation", calls["observation"] + 1
        ),
    )
    return calls


def test_r8_legacy_continuity_operator_smoke_allows_minimized_output(tmp_path):
    workspace = tmp_path / "fresh"
    workspace.mkdir()
    argv, payload = _r8_legacy_args(workspace)
    argv.extend(["--security-envelope-json", json.dumps(_r8_envelope(payload, operation=LEGACY_OPERATION), separators=(",", ":"))])
    code, stdout, stderr = _run_r8(argv)
    assert code == 0, stderr
    result = json.loads(stdout)
    assert stderr == "" and len(stdout.splitlines()) == 1
    assert result["security_decision"]["disposition"] == "ALLOW"
    assert result["terminal"] is True and result["non_persisted"] is True
    assert "candidate" not in stdout and "query" not in stdout and "rationale" not in stdout
    assert payload["operation"] == LEGACY_OPERATION
    assert list(workspace.iterdir()) == []


def test_r8_operator_drops_malicious_common_downstream_values(tmp_path, monkeypatch):
    malicious = {
        "status": {"candidate": "secret"},
        "terminal": {"unknown_future_field": "secret"},
        "non_authoritative": {"query": "secret"},
        "non_applied": {"rationale": "secret"},
        "non_persisted": ["secret"],
        "continuation_authorized": "secret",
        "automatic_collection": {"payload_binding_sha256": "secret"},
        "automatic_write": 1,
        "automatic_approval": 0,
        "automatic_adoption": None,
        "automatic_execution": ["secret"],
        "automatic_continuation": {"unknown_future_field": "secret"},
    }
    mixed = {
        "status": "complete-terminal-non-applied-revocation",
        "terminal": True,
        "non_authoritative": False,
        "non_applied": {"candidate": "secret"},
        "non_persisted": ["query", "secret"],
        "continuation_authorized": "rationale",
        "automatic_collection": {"payload_binding_sha256": "secret"},
        "automatic_write": 1,
        "automatic_approval": 0,
        "automatic_adoption": None,
        "automatic_execution": ["digest", "secret"],
        "automatic_continuation": {"unknown_future_field": "secret"},
    }
    downstream_results = iter((malicious, mixed))
    monkeypatch.setattr(
        operator_module,
        "run_r7_project_continuity_control_surface",
        lambda *args, **kwargs: next(downstream_results),
    )

    hostile_workspace = tmp_path / "hostile-fresh"
    hostile_workspace.mkdir()
    hostile_argv, hostile_payload = _r8_legacy_args(hostile_workspace)
    hostile_argv.extend(
        [
            "--security-envelope-json",
            json.dumps(
                _r8_envelope(hostile_payload, operation=LEGACY_OPERATION),
                separators=(",", ":"),
            ),
        ]
    )
    hostile_code, hostile_stdout, hostile_stderr = _run_r8(hostile_argv)

    assert (
        hostile_code == 0
        and hostile_stderr == ""
        and len(hostile_stdout.splitlines()) == 1
    )
    hostile_result = json.loads(hostile_stdout)
    assert hostile_stdout == json.dumps(
        hostile_result, separators=(",", ":")
    ) + "\n"
    assert hostile_result["security_decision"]["disposition"] == "ALLOW"
    assert "sanitized_receipt" in hostile_result
    for field in malicious:
        assert field not in hostile_result
    for forbidden in (
        "candidate",
        "query",
        "rationale",
        "payload_binding_sha256",
        "digest",
        "secret",
        "unknown_future_field",
    ):
        assert forbidden not in hostile_stdout
    assert list(hostile_workspace.iterdir()) == []

    mixed_workspace = tmp_path / "mixed-fresh"
    mixed_workspace.mkdir()
    mixed_argv, mixed_payload = _r8_legacy_args(mixed_workspace)
    mixed_argv.extend(
        [
            "--security-envelope-json",
            json.dumps(
                _r8_envelope(mixed_payload, operation=LEGACY_OPERATION),
                separators=(",", ":"),
            ),
        ]
    )
    mixed_code, mixed_stdout, mixed_stderr = _run_r8(mixed_argv)

    assert (
        mixed_code == 0
        and mixed_stderr == ""
        and len(mixed_stdout.splitlines()) == 1
    )
    mixed_result = json.loads(mixed_stdout)
    assert mixed_stdout == json.dumps(mixed_result, separators=(",", ":")) + "\n"
    assert mixed_result["security_decision"]["disposition"] == "ALLOW"
    assert "sanitized_receipt" in mixed_result
    assert mixed_result["status"] == "complete-terminal-non-applied-revocation"
    assert mixed_result["terminal"] is True
    assert mixed_result["non_authoritative"] is False
    for field in (
        "non_applied",
        "non_persisted",
        "continuation_authorized",
        "automatic_collection",
        "automatic_write",
        "automatic_approval",
        "automatic_adoption",
        "automatic_execution",
        "automatic_continuation",
    ):
        assert field not in mixed_result
    for forbidden in (
        "candidate",
        "query",
        "rationale",
        "payload_binding_sha256",
        "digest",
        "secret",
        "unknown_future_field",
    ):
        assert forbidden not in mixed_stdout
    assert list(mixed_workspace.iterdir()) == []


def test_r8_real_use_observation_operator_smoke_preserves_sanitized_assessment(tmp_path):
    workspace = tmp_path / "fresh"
    workspace.mkdir()
    observation = _r8_observation()
    values = {"project_id": "CIVILIZATION-CORE", "operator": "FOUNDER-OPERATOR", "confirm_real_use_observation": True}
    payload = build_observation_payload(values, observation)
    envelope = _r8_envelope(payload, operation=OBSERVATION_OPERATION)
    argv = [
        "continuity", "--workspace-root", str(workspace), "--project-id", "CIVILIZATION-CORE",
        "--operator", "FOUNDER-OPERATOR", "--real-use-observation-json",
        json.dumps(observation, separators=(",", ":")), "--confirm-real-use-observation",
        "--security-envelope-json", json.dumps(envelope, separators=(",", ":")),
    ]
    code, stdout, stderr = _run_r8(argv)
    assert code == 0, stderr
    result = json.loads(stdout)
    assert stderr == "" and len(stdout.splitlines()) == 1
    assert result["security_decision"]["disposition"] == "ALLOW"
    assert result["assessment"]["assessment_status"] == "baseline-unavailable"
    assert result["benefit_inference_allowed"] is False
    assert result["measurement_scope"] == "SYNTHETIC-COMMAND-INVOCATION-TO-TERMINAL"
    assert result["baseline_measurement_scope"] is None
    assert "candidate" not in stdout and "query" not in stdout and "rationale" not in stdout
    assert list(workspace.iterdir()) == []


def test_r8_sensitive_operator_smoke_blocks_without_downstream(tmp_path, monkeypatch):
    workspace = tmp_path / "fresh"
    workspace.mkdir()
    calls = {"provider": 0, "governed_memory": 0, "legacy": 0, "observation": 0}
    monkeypatch.setattr(continuity_module, "MemoryFabricProvider", lambda: calls.__setitem__("provider", calls["provider"] + 1))
    monkeypatch.setattr(continuity_module, "run_governed_memory_learning_slice", lambda *a, **k: calls.__setitem__("governed_memory", calls["governed_memory"] + 1))
    monkeypatch.setattr(operator_module, "run_r7_project_continuity_control_surface", lambda *a, **k: calls.__setitem__("legacy", calls["legacy"] + 1))
    monkeypatch.setattr(operator_module, "run_r7_real_use_observation", lambda *a, **k: calls.__setitem__("observation", calls["observation"] + 1))
    argv, payload = _r8_legacy_args(workspace, input_classification="SENSITIVE")
    envelope = _r8_envelope(payload, operation=LEGACY_OPERATION, classification="SENSITIVE")
    assert payload["input_classification"] == "SENSITIVE"
    assert envelope["security_classification"] == "SENSITIVE"
    assert envelope["authority_attestation"]["security_classification"] == "SENSITIVE"
    assert envelope["payload_binding_sha256"] == canonical_payload_binding_sha256(payload)
    argv.extend(["--security-envelope-json", json.dumps(envelope, separators=(",", ":"))])
    code, stdout, stderr = _run_r8(argv)
    result = json.loads(stderr)
    assert code == 2 and stdout == "" and len(stderr.splitlines()) == 1
    assert result == {
        "code": "sensitive_classification_blocked",
        "disposition": "BLOCK",
        "receipt_id": result["receipt_id"],
    }
    for forbidden in ("payload", "digest", "candidate", "query", "rationale", envelope["payload_binding_sha256"]):
        assert str(forbidden) not in stderr
    assert calls == {"provider": 0, "governed_memory": 0, "legacy": 0, "observation": 0}
    assert list(workspace.iterdir()) == []


def test_r8_missing_envelope_operator_smoke_blocks_without_downstream(tmp_path, monkeypatch):
    workspace = tmp_path / "fresh"
    workspace.mkdir()
    calls = {"legacy": 0, "observation": 0}
    monkeypatch.setattr(operator_module, "run_r7_project_continuity_control_surface", lambda *a, **k: calls.__setitem__("legacy", calls["legacy"] + 1))
    monkeypatch.setattr(operator_module, "run_r7_real_use_observation", lambda *a, **k: calls.__setitem__("observation", calls["observation"] + 1))
    argv, _payload = _r8_legacy_args(workspace)
    code, stdout, stderr = _run_r8(argv)
    assert code == 2 and stdout == "" and len(stderr.splitlines()) == 1
    assert json.loads(stderr) == {"code": "security_envelope_json_missing_or_blank", "disposition": "BLOCK"}
    assert "receipt" not in stderr and calls == {"legacy": 0, "observation": 0}
    assert list(workspace.iterdir()) == []


@pytest.mark.parametrize(
    ("target", "expected_code"),
    [
        ("security_envelope", "security_envelope_json_duplicate_key"),
        ("candidate", "candidate_json_duplicate_key"),
        ("real_use_result", "real_use_result_json_duplicate_key"),
        ("real_use_observation", "real_use_observation_json_duplicate_key"),
    ],
)
def test_r8_operator_rejects_duplicate_keys_before_lossy_json_loading(
    tmp_path, target: str, expected_code: str
):
    workspace = tmp_path / "fresh"
    workspace.mkdir()
    duplicate = '{"evidence":"first","evidence":"lost"}'
    assert json.loads(duplicate) == {"evidence": "lost"}
    if target == "real_use_observation":
        argv, _observation, payload = _r8_observation_args(workspace)
        _replace_option(argv, "--real-use-observation-json", duplicate)
        envelope = _r8_envelope(payload, operation=OBSERVATION_OPERATION)
    else:
        argv, payload = _r8_legacy_args(workspace)
        envelope = _r8_envelope(payload, operation=LEGACY_OPERATION)
        if target == "candidate":
            _replace_option(argv, "--candidate-json", duplicate)
        elif target == "real_use_result":
            argv.extend(["--real-use-result-json", duplicate])
        else:
            envelope = duplicate
    envelope_json = (
        envelope
        if isinstance(envelope, str)
        else json.dumps(envelope, separators=(",", ":"))
    )
    argv.extend(["--security-envelope-json", envelope_json])

    code, stdout, stderr = _run_r8(argv)

    assert code == 2 and stdout == ""
    assert json.loads(stderr) == {
        "code": expected_code,
        "disposition": "BLOCK",
    }


@pytest.mark.parametrize(
    ("target", "raw", "suffix"),
    [
        ("security_envelope", "[]", "not_object"),
        ("security_envelope", '{"a":NaN}', "non_finite_number"),
        ("security_envelope", "{", "malformed"),
        ("candidate", "[]", "not_object"),
        ("candidate", '{"a":NaN}', "non_finite_number"),
        ("candidate", "{", "malformed"),
        ("real_use_result", "[]", "not_object"),
        ("real_use_result", '{"a":NaN}', "non_finite_number"),
        ("real_use_result", "{", "malformed"),
        ("real_use_observation", "[]", "not_object"),
        ("real_use_observation", '{"a":NaN}', "non_finite_number"),
        ("real_use_observation", "{", "malformed"),
    ],
)
def test_r8_all_operator_json_inputs_are_strict_objects(
    tmp_path, target: str, raw: str, suffix: str
):
    workspace = tmp_path / "fresh"
    workspace.mkdir()
    if target == "real_use_observation":
        argv, _observation, payload = _r8_observation_args(workspace)
        _replace_option(argv, "--real-use-observation-json", raw)
        envelope = _r8_envelope(payload, operation=OBSERVATION_OPERATION)
        field = "real_use_observation_json"
    else:
        argv, payload = _r8_legacy_args(workspace)
        envelope = _r8_envelope(payload, operation=LEGACY_OPERATION)
        if target == "candidate":
            _replace_option(argv, "--candidate-json", raw)
            field = "candidate_json"
        elif target == "real_use_result":
            argv.extend(["--real-use-result-json", raw])
            field = "real_use_result_json"
        else:
            field = "security_envelope_json"
            envelope = raw
    envelope_json = (
        envelope
        if isinstance(envelope, str)
        else json.dumps(envelope, separators=(",", ":"))
    )
    argv.extend(["--security-envelope-json", envelope_json])

    code, stdout, stderr = _run_r8(argv)

    assert code == 2 and stdout == ""
    assert json.loads(stderr) == {
        "code": f"{field}_{suffix}",
        "disposition": "BLOCK",
    }


def test_r8_empty_observation_selects_observation_route_then_blocks(tmp_path):
    workspace = tmp_path / "fresh"
    workspace.mkdir()
    values = {
        "project_id": "CIVILIZATION-CORE",
        "operator": "FOUNDER-OPERATOR",
        "confirm_real_use_observation": True,
    }
    payload = build_observation_payload(values, {})
    envelope = _r8_envelope(payload, operation=OBSERVATION_OPERATION)
    argv = [
        "continuity",
        "--workspace-root",
        str(workspace),
        "--project-id",
        "CIVILIZATION-CORE",
        "--operator",
        "FOUNDER-OPERATOR",
        "--real-use-observation-json",
        "{}",
        "--confirm-real-use-observation",
        "--security-envelope-json",
        json.dumps(envelope, separators=(",", ":")),
    ]

    code, stdout, stderr = _run_r8(argv)

    result = json.loads(stderr)
    assert code == 2 and stdout == ""
    assert result["disposition"] == "BLOCK"
    assert result["code"] == "security_classification_binding_mismatch"


def test_r8_confirmation_without_observation_is_route_argument_conflict(tmp_path):
    workspace = tmp_path / "fresh"
    workspace.mkdir()
    code, stdout, stderr = _run_r8(
        [
            "continuity",
            "--workspace-root",
            str(workspace),
            "--project-id",
            "CIVILIZATION-CORE",
            "--operator",
            "FOUNDER-OPERATOR",
            "--confirm-real-use-observation",
        ]
    )
    assert code == 2 and stdout == ""
    assert json.loads(stderr) == {
        "code": "route_argument_conflict",
        "disposition": "BLOCK",
    }


def test_r8_operation_must_match_actual_legacy_route(tmp_path):
    workspace = tmp_path / "fresh"
    workspace.mkdir()
    argv, payload = _r8_legacy_args(workspace)
    envelope = _r8_envelope(payload, operation=LEGACY_OPERATION)
    envelope["operation"] = OBSERVATION_OPERATION
    envelope["authority_attestation"]["operation"] = OBSERVATION_OPERATION
    argv.extend(
        [
            "--security-envelope-json",
            json.dumps(envelope, separators=(",", ":")),
        ]
    )
    code, stdout, stderr = _run_r8(argv)
    assert code == 2 and stdout == ""
    assert json.loads(stderr)["code"] == "operation_route_mismatch"


def test_r8_legacy_route_forbids_measurement_scope(tmp_path):
    workspace = tmp_path / "fresh"
    workspace.mkdir()
    argv, payload = _r8_legacy_args(workspace)
    envelope = _r8_envelope(payload, operation=LEGACY_OPERATION)
    envelope["measurement_scope"] = "SYNTHETIC-COMMAND-INVOCATION-TO-TERMINAL"
    argv.extend(
        [
            "--security-envelope-json",
            json.dumps(envelope, separators=(",", ":")),
        ]
    )
    code, stdout, stderr = _run_r8(argv)
    assert code == 2 and stdout == ""
    assert json.loads(stderr)["code"] == "route_field_set_mismatch"


@pytest.mark.parametrize(
    ("mutation", "expected_code"),
    [
        ("missing_baseline_scope", "security_envelope_missing_fields"),
        ("incorrect_baseline_scope", "baseline_measurement_scope_binding_mismatch"),
    ],
)
def test_r8_observation_route_binds_both_measurement_scopes(
    tmp_path, mutation: str, expected_code: str
):
    workspace = tmp_path / "fresh"
    workspace.mkdir()
    argv, _observation, payload = _r8_observation_args(workspace)
    envelope = _r8_envelope(payload, operation=OBSERVATION_OPERATION)
    if mutation == "missing_baseline_scope":
        del envelope["baseline_measurement_scope"]
    else:
        envelope["baseline_measurement_scope"] = (
            "SYNTHETIC-COMMAND-INVOCATION-TO-TERMINAL"
        )
    argv.extend(
        [
            "--security-envelope-json",
            json.dumps(envelope, separators=(",", ":")),
        ]
    )
    code, stdout, stderr = _run_r8(argv)
    assert code == 2 and stdout == ""
    assert json.loads(stderr)["code"] == expected_code


@pytest.mark.parametrize(
    ("classification", "trust", "lineage", "human", "exit_code", "expected_code"),
    [
        (
            "SYNTHETIC",
            "LOCAL_PROVIDER_DERIVED",
            "LOCAL_PROVIDER_OUTPUT",
            "APPROVE_READ_ONLY_EXECUTION",
            3,
            "provider_source_review_required",
        ),
        (
            "SYNTHETIC",
            "EXTERNAL_FEDERATED",
            "EXTERNAL_FEDERATED_INPUT",
            "APPROVE_READ_ONLY_EXECUTION",
            3,
            "federated_source_review_required",
        ),
        (
            "SYNTHETIC",
            "LOCAL_PROVIDER_DERIVED",
            "LOCAL_PROVIDER_OUTPUT",
            "DENY_EXECUTION",
            2,
            "human_execution_denied",
        ),
        (
            "SENSITIVE",
            "LOCAL_CALLER_PROVIDED",
            "CALLER_SUBMISSION",
            "APPROVE_READ_ONLY_EXECUTION",
            2,
            "sensitive_classification_blocked",
        ),
    ],
)
def test_r8_review_and_block_decisions_have_zero_downstream_calls(
    tmp_path,
    monkeypatch,
    classification: str,
    trust: str,
    lineage: str,
    human: str,
    exit_code: int,
    expected_code: str,
):
    workspace = tmp_path / "fresh"
    workspace.mkdir()
    calls = _install_r8_downstream_counters(monkeypatch)
    argv, payload = _r8_legacy_args(
        workspace, input_classification=classification
    )
    envelope = _r8_envelope(
        payload,
        operation=LEGACY_OPERATION,
        classification=classification,
        source_trust=trust,
        source_lineage_class=lineage,
        human_decision=human,
    )
    argv.extend(
        [
            "--security-envelope-json",
            json.dumps(envelope, separators=(",", ":")),
        ]
    )
    code, stdout, stderr = _run_r8(argv)
    assert code == exit_code and stdout == ""
    assert json.loads(stderr)["code"] == expected_code
    assert calls == {
        "provider": 0,
        "governed_memory": 0,
        "legacy": 0,
        "observation": 0,
    }


def test_r8_structural_block_has_zero_downstream_calls(tmp_path, monkeypatch):
    workspace = tmp_path / "fresh"
    workspace.mkdir()
    calls = _install_r8_downstream_counters(monkeypatch)
    argv, payload = _r8_legacy_args(workspace)
    _replace_option(argv, "--candidate-json", "{")
    envelope = _r8_envelope(payload, operation=LEGACY_OPERATION)
    argv.extend(
        [
            "--security-envelope-json",
            json.dumps(envelope, separators=(",", ":")),
        ]
    )
    code, stdout, stderr = _run_r8(argv)
    assert code == 2 and stdout == ""
    assert json.loads(stderr) == {
        "code": "candidate_json_malformed",
        "disposition": "BLOCK",
    }
    assert calls == {
        "provider": 0,
        "governed_memory": 0,
        "legacy": 0,
        "observation": 0,
    }


@pytest.mark.parametrize("route", ["legacy", "observation"])
def test_r8_downstream_exception_is_sanitized_without_leakage(
    tmp_path, monkeypatch, route: str
):
    workspace = tmp_path / "fresh"
    workspace.mkdir()
    leaked = "candidate query rationale secret traceback-marker"

    def fail(*args, **kwargs):
        raise RuntimeError(leaked)

    if route == "legacy":
        argv, payload = _r8_legacy_args(workspace)
        operation = LEGACY_OPERATION
        monkeypatch.setattr(
            operator_module, "run_r7_project_continuity_control_surface", fail
        )
    else:
        argv, _observation, payload = _r8_observation_args(workspace)
        operation = OBSERVATION_OPERATION
        monkeypatch.setattr(operator_module, "run_r7_real_use_observation", fail)
    envelope = _r8_envelope(payload, operation=operation)
    argv.extend(
        [
            "--security-envelope-json",
            json.dumps(envelope, separators=(",", ":")),
        ]
    )

    code, stdout, stderr = _run_r8(argv)

    assert code == 1 and stdout == ""
    assert json.loads(stderr) == {
        "code": "downstream_execution_failed",
        "disposition": "BLOCK",
    }
    lowered = stderr.lower()
    for forbidden in ("candidate", "query", "rationale", "secret", "traceback"):
        assert forbidden not in lowered
    assert leaked not in stderr
