"""Synthetic protocol tests only; never real-user or pilot evidence."""
from __future__ import annotations

import hashlib
import io
import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path

import pytest

from hermes_memory_fabric import p4_m0_subspace_operator as cli
from hermes_memory_fabric import r7_project_continuity_control_surface as surface
from hermes_memory_fabric import r8_security_governance as security

OPERATION = "R10_ORDINARY_HANDOFF_RECORD_VALIDATION"
SCOPE = {"project": "CIVILIZATION-CORE", "workspace": "/workspace/r7-project-continuity", "namespace": "r7-value-signal"}
SECRET = "SYNTHETIC-CONTENT-MUST-NOT-LEAK-81726"


def record():
    return {
        "scope": dict(SCOPE), "input_classification": "SYNTHETIC",
        "candidate": {
            "id": "synthetic-handoff-1", "content": SECRET,
            "project_id": "CIVILIZATION-CORE", "entity_ids": ["CIVILIZATION-CORE"],
            "source": "synthetic-test", "source_id": "synthetic-source-1",
            "provenance": {"kind": "synthetic-test", "reference": SECRET},
            "risk_level": "low", "created_at": "2026-09-21T00:00:00Z", "tags": ["synthetic"],
            "governance": {"dry_run": True, "read_only": True, "proposal_governed": True},
        },
        "human_review": {"status": "NOT_PROVIDED"},
        "correction": {"status": "NOT_OCCURRED"}, "revocation": {"status": "NOT_OCCURRED"},
        "measurement": {"status": "NOT_MEASURED"}, "value_evaluation": {"status": "NOT_PROVIDED"},
    }


def event_record(correction=False, revocation=False):
    value = record()
    value["human_review"] = {"status": "PROVIDED", "outcome": "defer", "rationale": SECRET}
    if correction:
        value["correction"] = {"status": "OCCURRED", "corrected_outcome": "request_changes", "rationale": SECRET}
    if revocation:
        value["revocation"] = {
            "status": "OCCURRED", "target": "CORRECTION" if correction else "HUMAN_REVIEW",
            "target_candidate_id": "synthetic-handoff-1", "rationale": SECRET,
        }
    return value


def digest(value):
    # Independently specified protocol serialization, not a production validator oracle.
    raw = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)
    return hashlib.sha256(raw.encode()).hexdigest()


def envelope(value, *, workspace=SCOPE["workspace"], project="CIVILIZATION-CORE", operator="FOUNDER-OPERATOR", confirm=True):
    payload = {
        "operation": OPERATION, "project_id": project, "operator": operator,
        "workspace": workspace, "record": value, "confirm_ordinary_handoff": confirm,
    }
    result = {
        "schema_name": "GOVERNED-MEMORY-SECURITY-DECISION-ENVELOPE", "version": "1.4",
        "operation": OPERATION, "request_reference": "r8-request:0123456789abcdef0123456789abcdef",
        "payload_binding_sha256": digest(payload), "project_id": "CIVILIZATION-CORE",
        "namespace": "R7_PROJECT_CONTINUITY", "workspace": workspace,
        "operator_role": "FOUNDER-OPERATOR", "requested_effect": "READ_ONLY_NON_PERSISTENT_TERMINAL_ASSESSMENT",
        "security_classification": value["input_classification"], "security_classification_source": "CALLER_DECLARATION",
        "source_trust": "LOCAL_CALLER_PROVIDED", "source_lineage_class": "CALLER_SUBMISSION",
        "human_decision": "APPROVE_READ_ONLY_EXECUTION",
    }
    attest(result)
    return result


def attest(value):
    value["authority_attestation"] = {
        **{k: v for k, v in value.items() if k != "authority_attestation"},
        "attestation_type": "CALLER_AUTHORITY_ATTESTATION", "attestation_version": value["version"], "attested": True,
    }


def argv(value, env=None, *, workspace=SCOPE["workspace"], project="CIVILIZATION-CORE", operator="FOUNDER-OPERATOR", confirm=True):
    env = envelope(value, workspace=workspace, project=project, operator=operator, confirm=confirm) if env is None else env
    return ["ordinary-handoff", "--workspace-root", workspace, "--project-id", project, "--operator", operator,
            "--record-json", json.dumps(value), "--security-envelope-json", json.dumps(env)] + (["--confirm-ordinary-handoff"] if confirm else [])


def invoke(value, env=None, **kwargs):
    out, err = io.StringIO(), io.StringIO()
    code = cli.run_operator_command(argv(value, env, **kwargs), stdout=out, stderr=err)
    assert SECRET not in out.getvalue() + err.getvalue()
    return code, json.loads(out.getvalue()) if out.getvalue() else None, json.loads(err.getvalue()) if err.getvalue() else None


def test_ordinary_record_only_receipt_and_input_immutability(monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail("ordinary handoff must not compose context or fabricate review/events")
    monkeypatch.setattr(surface.MemoryFabricProvider, "build_active_context", forbidden)
    monkeypatch.setattr(surface, "run_governed_memory_learning_slice", forbidden)
    value = record()
    original = deepcopy(value)
    code, result, error = invoke(value)
    assert code == 0 and error is None and value == original
    assert result["status"] == "ordinary-handoff-record-accepted"
    assert result["record_accepted"] is True
    assert result["correction_status"] == result["revocation_status"] == "NOT_OCCURRED"
    assert result["measurement_status"] == "NOT_MEASURED"
    assert result["value_evaluation_status"] == "NOT_PROVIDED"
    assert result["security_decision"] == {"code": "security_policy_allowed", "disposition": "ALLOW"}
    assert result["sanitized_receipt"]["operation"] == OPERATION
    assert result["sanitized_receipt"]["version"] == "1.4"
    for name in ("candidate_use_authorized", "continuation_authorized", "benefit_inference_allowed", "automatic_collection", "automatic_write", "automatic_approval", "automatic_adoption", "automatic_execution", "automatic_continuation"):
        assert result[name] is False
    for name in ("non_authoritative", "non_applied", "non_persisted", "terminal"):
        assert result[name] is True
    assert not {"task_completed", "assessment", "worthwhile", "seconds", "candidate", "content", "query", "human_review", "correction_record", "revocation_record"} & result.keys()


@pytest.mark.parametrize("field", ["correction", "revocation"])
def test_unknown_is_not_not_occurred_or_candidate_permission(field):
    value = record()
    value[field] = {"status": "UNKNOWN"}
    code, result, error = invoke(value)
    assert code == 0 and error is None
    assert result[field + "_status"] == "UNKNOWN"
    assert result["candidate_use_authorized"] is False


@pytest.mark.parametrize("correct,revoke", [(True, False), (False, True), (True, True)])
def test_actual_declared_events_are_validated_without_forcing_other_event(correct, revoke, monkeypatch):
    calls = []
    real_correction, real_revocation = surface.create_correction_record, surface.create_revocation_record
    def correction(*a, **kw):
        calls.append("correction")
        return real_correction(*a, **kw)
    def revocation(*a, **kw):
        calls.append("revocation")
        return real_revocation(*a, **kw)
    monkeypatch.setattr(surface, "create_correction_record", correction)
    monkeypatch.setattr(surface, "create_revocation_record", revocation)
    code, result, error = invoke(event_record(correct, revoke))
    assert code == 0 and error is None
    assert result["correction_status"] == ("OCCURRED" if correct else "NOT_OCCURRED")
    assert result["revocation_status"] == ("OCCURRED" if revoke else "NOT_OCCURRED")
    assert calls == (["correction", "revocation"] if correct and revoke else ["correction"] if correct else [])
    assert result["candidate_use_authorized"] is False


@pytest.mark.parametrize("field,replacement", [
    ("correction", {"status": "NOT_OCCURRED", "rationale": SECRET}),
    ("correction", {"status": "UNKNOWN", "corrected_outcome": "defer"}),
    ("revocation", {"status": "UNKNOWN", "rationale": SECRET}),
    ("revocation", {"status": "NOT_OCCURRED", "target": "HUMAN_REVIEW"}),
    ("measurement", {"status": "NOT_MEASURED", "seconds": 0}),
    ("measurement", {"status": "NOT_MEASURED", "caller_observed": True}),
    ("measurement", {"status": "MEASURED", "seconds": -1, "caller_observed": True}),
    ("measurement", {"status": "MEASURED", "seconds": True, "caller_observed": True}),
    ("measurement", {"status": "MEASURED", "seconds": 10, "caller_observed": False}),
    ("measurement", {"status": "MEASURED", "seconds": 10}),
    ("value_evaluation", {"status": "NOT_PROVIDED", "worthwhile": False}),
    ("value_evaluation", {"status": "PROVIDED", "worthwhile": 1}),
    ("value_evaluation", {"status": "PROVIDED"}),
    ("human_review", {"status": "NOT_PROVIDED", "outcome": "defer"}),
    ("human_review", {"status": "PROVIDED", "outcome": "defer"}),
    ("correction", {"status": "NOT_PROVIDED"}), ("revocation", {"status": None}),
])
def test_contradictory_or_missing_fields_rejected(field, replacement):
    value = record()
    value[field] = replacement
    assert invoke(value) == (1, None, {"code": "handoff_record_rejected", "disposition": "BLOCK"})


@pytest.mark.parametrize("field,key", [
    ("human_review", "outcome"), ("human_review", "rationale"),
    ("correction", "corrected_outcome"), ("correction", "rationale"),
    ("revocation", "target"), ("revocation", "target_candidate_id"), ("revocation", "rationale"),
])
def test_occurred_events_require_every_fact(field, key):
    value = event_record(True, True)
    del value[field][key]
    assert invoke(value)[0] == 1


@pytest.mark.parametrize("field,key,bad", [
    ("correction", "corrected_outcome", "defer"), ("correction", "corrected_outcome", "unsupported"),
    ("correction", "rationale", " "), ("human_review", "rationale", ""),
    ("human_review", "outcome", "unsupported"), ("revocation", "rationale", ""),
    ("revocation", "target", "HUMAN_REVIEW"), ("revocation", "target_candidate_id", "another-candidate"),
])
def test_event_facts_cannot_bypass_existing_constraints(field, key, bad):
    value = event_record(True, True)
    value[field][key] = bad
    assert invoke(value)[0] == 1


def test_events_need_review_and_unambiguous_lineage():
    value = event_record(True, False)
    value["human_review"] = {"status": "NOT_PROVIDED"}
    assert invoke(value)[0] == 1
    value = event_record(False, True)
    value["human_review"] = {"status": "NOT_PROVIDED"}
    assert invoke(value)[0] == 1
    value = event_record(False, True)
    value["correction"] = {"status": "UNKNOWN"}
    assert invoke(value)[0] == 1


@pytest.mark.parametrize("seconds,worthwhile", [(0, False), (12.5, True)])
def test_actual_measurement_and_evaluation_are_not_inferred_value(seconds, worthwhile):
    value = record()
    value["measurement"] = {"status": "MEASURED", "seconds": seconds, "caller_observed": True}
    value["value_evaluation"] = {"status": "PROVIDED", "worthwhile": worthwhile}
    code, result, error = invoke(value)
    assert code == 0 and error is None
    assert result["measurement_status"] == "MEASURED" and result["value_evaluation_status"] == "PROVIDED"
    assert result["benefit_inference_allowed"] is False
    assert "worthwhile" not in result and "task_completed" not in result


@pytest.mark.parametrize("field", ["project", "workspace", "namespace"])
def test_record_scope_mismatch_rejected(field):
    value = record()
    value["scope"][field] = "wrong"
    assert invoke(value)[0] == 1


@pytest.mark.parametrize("key", ["project_id", "project", "workspace", "namespace"])
def test_candidate_scope_mismatch_rejected(key):
    value = record()
    value["candidate"][key] = "wrong"
    assert invoke(value)[0] == 1


@pytest.mark.parametrize("key,bad", [("risk_level", "high"), ("provenance", {}), ("content", ""), ("id", "invalid id")])
def test_rejected_candidate_never_reaches_event_processing(key, bad, monkeypatch):
    def forbidden(*a, **kw):
        pytest.fail("rejected candidate entered event processing")
    monkeypatch.setattr(surface, "run_governed_memory_learning_slice", forbidden)
    value = event_record(True, True)
    value["candidate"][key] = bad
    assert invoke(value)[0] == 1


@pytest.mark.parametrize("field,bad,expected", [
    ("operation", "R7_PROJECT_CONTINUITY", 2), ("version", "1.3", 2),
    ("namespace", "other", 2), ("project_id", "other", 2), ("operator_role", "other", 2),
    ("workspace", "/other", 2), ("human_decision", "DENY_EXECUTION", 2),
    ("human_decision", "REQUEST_REVIEW", 3),
])
def test_security_gate_stops_before_downstream(field, bad, expected, monkeypatch):
    value = record()
    env = envelope(value)
    env[field] = bad
    attest(env)
    def forbidden(*a, **kw):
        pytest.fail("security denial entered downstream")
    monkeypatch.setattr(cli, "run_ordinary_handoff_record", forbidden)
    code, result, error = invoke(value, env)
    assert code == expected and result is None
    assert error["disposition"] == ("REVIEW" if expected == 3 else "BLOCK")


@pytest.mark.parametrize("classification,trust,lineage,expected", [
    ("SENSITIVE", "LOCAL_CALLER_PROVIDED", "CALLER_SUBMISSION", 2),
    ("NON_SENSITIVE", "UNKNOWN", "UNKNOWN", 2),
    ("NON_SENSITIVE", "LOCAL_PROVIDER_DERIVED", "LOCAL_PROVIDER_OUTPUT", 3),
    ("NON_SENSITIVE", "EXTERNAL_FEDERATED", "EXTERNAL_FEDERATED_INPUT", 3),
])
def test_security_source_or_classification_rejection(classification, trust, lineage, expected, monkeypatch):
    value = record()
    value["input_classification"] = classification
    env = envelope(value)
    env.update(source_trust=trust, source_lineage_class=lineage)
    attest(env)
    def forbidden(*a, **kw):
        pytest.fail("source/classification denied but reached downstream")
    monkeypatch.setattr(cli, "run_ordinary_handoff_record", forbidden)
    assert invoke(value, env)[0] == expected


@pytest.mark.parametrize("mutation", ["content", "scope", "event", "measurement", "evaluation", "authority", "no-authority"])
def test_binding_and_authority_cannot_be_reused_for_changed_input(mutation):
    value = record()
    env = envelope(value)
    if mutation == "content": value["candidate"]["content"] = "changed synthetic"
    elif mutation == "scope": value["scope"]["namespace"] = "other"
    elif mutation == "event": value["correction"]["status"] = "UNKNOWN"
    elif mutation == "measurement": value["measurement"] = {"status": "MEASURED", "seconds": 0, "caller_observed": True}
    elif mutation == "evaluation": value["value_evaluation"] = {"status": "PROVIDED", "worthwhile": False}
    elif mutation == "authority": env["authority_attestation"]["attested"] = False
    else: del env["authority_attestation"]
    code, result, error = invoke(value, env)
    assert code == 2 and result is None and error["disposition"] == "BLOCK"


def test_confirmation_and_cli_scope_are_not_optional():
    assert invoke(record(), confirm=False)[0] == 1
    assert invoke(record(), workspace="/different")[0] == 1
    assert invoke(record(), project="different")[0] == 2
    assert invoke(record(), operator="different")[0] == 2


def test_real_federation_review_never_reaches_event_processing(monkeypatch):
    original = surface._r7_admission_config
    def external(project):
        scope, registry, descriptor = original(project)
        descriptor["source_class"] = "EXTERNAL_FEDERATED_CANDIDATE"
        registry[descriptor["provider_id"]]["source_classes"] = ["EXTERNAL_FEDERATED_CANDIDATE"]
        registry[descriptor["provider_id"]]["review_only"] = True
        return scope, registry, descriptor
    monkeypatch.setattr(surface, "_r7_admission_config", external)
    def forbidden(*a, **kw):
        pytest.fail("federation REVIEW entered event processing")
    monkeypatch.setattr(surface, "run_governed_memory_learning_slice", forbidden)
    assert invoke(event_record(True, True)) == (3, None, {"code": "handoff_candidate_review", "disposition": "REVIEW"})


def test_mixed_cli_arguments_and_invalid_json_do_not_leak():
    value = record()
    for extra in (["--outcome", SECRET], ["--real-use-observation-json", SECRET], ["--record-json", '{"x":NaN}'], ["--record-json", '{"x":1,"x":2}']):
        out, err = io.StringIO(), io.StringIO()
        assert cli.run_operator_command(argv(value) + extra, stdout=out, stderr=err) == 2
        assert out.getvalue() == "" and SECRET not in err.getvalue()


def test_real_cli_subprocess_uses_entrypoint_and_writes_nothing(tmp_path):
    repo = Path(__file__).resolve().parents[1]
    empty = tmp_path / "isolated"
    empty.mkdir()
    value = record()
    process = subprocess.run(
        [sys.executable, "-m", "hermes_memory_fabric.p4_m0_subspace_operator", *argv(value)],
        cwd=empty, env={"PYTHONPATH": str(repo / "src"), "PYTHONDONTWRITEBYTECODE": "1", "PYTHONNOUSERSITE": "1"},
        capture_output=True, text=True, timeout=30,
    )
    assert process.returncode == 0 and process.stderr == ""
    result = json.loads(process.stdout)
    assert result["status"] == "ordinary-handoff-record-accepted"
    assert result["candidate_use_authorized"] is False
    assert SECRET not in process.stdout and list(empty.iterdir()) == []


def test_no_write_or_network_calls_during_full_event_validation(monkeypatch):
    import builtins
    import os
    import socket

    def forbidden(*a, **kw):
        pytest.fail("handoff attempted filesystem access or network")
    with monkeypatch.context() as guard:
        guard.setattr(builtins, "open", forbidden)
        guard.setattr(io, "open", forbidden)
        guard.setattr(os, "open", forbidden)
        guard.setattr(socket.socket, "connect", forbidden)
        guard.setattr(socket, "create_connection", forbidden)
        assert invoke(event_record(True, True))[0] == 0


@pytest.mark.parametrize("field,bad", [
    ("candidate_use_authorized", True), ("non_persisted", False),
    ("automatic_write", True), ("correction_status", SECRET),
    ("revocation_status", None), ("record_accepted", 1),
    ("status", "complete-terminal-non-applied-revocation"),
])
def test_projection_fails_closed_on_unsafe_downstream_result(field, bad):
    value = record()
    args = {"project_id": "CIVILIZATION-CORE", "operator": "FOUNDER-OPERATOR",
            "workspace_root": SCOPE["workspace"], "confirm_ordinary_handoff": True}
    decision = security.evaluate_security_envelope(
        envelope(value), selected_operation=OPERATION,
        payload=security.build_handoff_payload(args, value), input_classification="SYNTHETIC",
    )
    actual = surface.run_ordinary_handoff_record(value, project_id="CIVILIZATION-CORE", operator="FOUNDER-OPERATOR", workspace=SCOPE["workspace"], confirm_ordinary_handoff=True)
    actual[field] = bad
    with pytest.raises(security.R8StructuralError, match="handoff_result_invalid"):
        security.minimized_operator_projection(decision, actual, selected_operation=OPERATION)


def test_projection_ignores_content_and_legacy_business_claims():
    value = record()
    args = {"project_id": "CIVILIZATION-CORE", "operator": "FOUNDER-OPERATOR",
            "workspace_root": SCOPE["workspace"], "confirm_ordinary_handoff": True}
    decision = security.evaluate_security_envelope(
        envelope(value), selected_operation=OPERATION,
        payload=security.build_handoff_payload(args, value), input_classification="SYNTHETIC",
    )
    actual = surface.run_ordinary_handoff_record(value, project_id="CIVILIZATION-CORE", operator="FOUNDER-OPERATOR", workspace=SCOPE["workspace"], confirm_ordinary_handoff=True)
    actual.update(candidate=SECRET, task_completed=True, value_signal_assessment={"worthwhile": True}, recovery_time_seconds=0)
    result = security.minimized_operator_projection(decision, actual, selected_operation=OPERATION)
    assert SECRET not in json.dumps(result)
    assert not {"candidate", "task_completed", "value_signal_assessment", "recovery_time_seconds"} & result.keys()
