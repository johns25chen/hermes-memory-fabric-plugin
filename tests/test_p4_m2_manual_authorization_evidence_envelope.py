from __future__ import annotations

import argparse
import io
import json
import tomllib
from pathlib import Path

from hermes_memory_fabric.p4_m0_subspace_operator import build_parser, run_operator_command
from hermes_memory_fabric.p4_m2_manual_authorization_evidence_envelope import (
    MANUAL_AUTHORIZATION_EVIDENCE_ENVELOPE_BOUNDARY,
    ManualAuthorizationEvidenceEnvelopeField,
    list_manual_authorization_evidence_envelope_fields,
    manual_authorization_evidence_envelope_as_dicts,
    manual_authorization_evidence_envelope_field_ids,
    manual_authorization_evidence_envelope_report,
    render_manual_authorization_evidence_envelope_markdown,
)


FIELD_IDS = (
    "authorization-evidence-envelope-id",
    "human-operator-reference",
    "human-authorization-intent-reference",
    "manual-decision-reference",
    "execution-surface-reference",
    "execution-contract-validation-matrix-reference",
    "authorization-scope-statement",
    "authorization-boundary-statement",
    "precondition-evidence-reference",
    "risk-acknowledgement-reference",
    "audit-trace-reference",
    "operator-confirmation-placeholder",
    "revocation-or-expiry-note",
    "authorization-semantics-disabled",
    "execution-semantics-disabled",
)

DATACLASS_FIELDS = {
    "field_order",
    "field_id",
    "field_name",
    "field_purpose",
    "required_evidence_signal",
    "trace_requirement",
    "prohibited_semantics",
    "blocking_signal",
    "future_authorization_note",
}

EXPECTED_MEMORY_LOOP_COMMANDS = {
    "checklist",
    "review-status",
    "recall-verification-status",
    "lifecycle-verification-status",
    "do-not-retry-verification-status",
    "source-provenance-verification-status",
    "decision-readiness-status",
    "manual-decision-preview",
    "governance-pack-export",
    "final-boundary-audit",
    "manual-execution-hardening",
    "execution-surface-contract",
    "execution-contract-validation-matrix",
    "manual-authorization-evidence-envelope",
    "human-confirmation-snapshot-contract",
    "execution-preconditions-snapshot-map",
    "execution-risk-acknowledgement-map",
    "execution-risk-acceptance-prohibition-map",
    "execution-risk-waiver-prohibition-map",
    "execution-decision-non-equivalence-map",
    "execution-decision-recommendation-prohibition-map",
    "execution-decision-default-denial-boundary-map",
    "execution-decision-silence-non-consent-map",
    "execution-decision-negative-evidence-non-override-map",
    "execution-decision-conflicting-evidence-isolation-map",
    "execution-decision-evidence-precedence-prohibition-map",
    "final-non-execution-boundary-audit",
    "p4-m2-closure-handoff-contract",
    "governed-transition-intake-boundary-contract",
    "governed-transition-intake-request-envelope-contract",
    "governed-transition-intake-evidence-reference-envelope-contract",
    "governed-transition-intake-declared-human-context-envelope-contract",
    "governed-transition-intake-target-phase-envelope-contract",
    "governed-transition-intake-declared-transition-reason-envelope-contract",
    "governed-transition-intake-declared-transition-constraint-envelope-contract",
        "governed-transition-intake-declared-transition-dependency-envelope-contract",
    "governed-transition-intake-declared-transition-impact-envelope-contract",
    "governed-transition-intake-declared-transition-risk-envelope-contract",
    "governed-transition-intake-declared-transition-assumption-envelope-contract",
    "governed-transition-intake-declared-transition-safeguard-envelope-contract",
    "governed-transition-intake-package-assembly-envelope-contract",
    "governed-transition-intake-final-non-validation-boundary-audit",
    "governed-transition-intake-closure-handoff-contract",
    "governed-transition-intake-phase-closure-review",
    "governed-transition-intake-final-phase-handoff-summary",
    "entry-gate-design-boundary-contract",
    "entry-gate-design-request-envelope-contract",
    "evidence-reference-envelope-contract",
    "declared-human-context-envelope-contract",
    "target-phase-envelope-contract",
}

TRUE_STATUS_FLAGS = (
    "p4_m2_started",
    "execution_surface_contract_definition_available",
    "execution_contract_validation_matrix_available",
    "manual_authorization_evidence_envelope_started",
    "manual_authorization_evidence_envelope_definition_only",
    "evidence_envelope_fields_defined",
    "trace_requirements_defined",
    "blocking_signal_rules_defined",
    "inspection_only",
)

DISABLED_STATUS_FLAGS = (
    "authorization_enabled",
    "authorization_command_enabled",
    "live_authorization_validation_enabled",
    "live_contract_validation_enabled",
    "input_validation_enabled",
    "record_validation_enabled",
    "validation_verdict_enabled",
    "readiness_verdict_enabled",
    "actual_decision_execution_enabled",
    "automatic_decision_execution_enabled",
    "manual_execution_command_enabled",
    "execute_command_enabled",
    "approval_enabled",
    "rejection_enabled",
    "automatic_decision_recommendation_enabled",
    "decision_ranking_enabled",
    "automatic_readiness_verdict_enabled",
    "authorization_semantics_granted",
    "execution_semantics_granted",
    "memory_write_enabled",
    "memory_record_mutation_enabled",
    "proposal_mutation_enabled",
    "lifecycle_mutation_enabled",
    "do_not_retry_guard_mutation_enabled",
    "retry_policy_mutation_enabled",
    "source_fetching_enabled",
    "source_provenance_mutation_enabled",
    "provenance_write_enabled",
    "memory_injection_enabled",
    "bulk_import_enabled",
    "auto_ingest_enabled",
    "agent_call_enabled",
    "api_mcp_connector_enabled",
    "p4_m3_started",
    "p4_m4_started",
    "p4_m5_started",
    "v7_started",
    "productization_started",
)

PROHIBITED_MEMORY_LOOP_COMMANDS = {
    "authorize",
    "authorization",
    "authorize-decision",
    "decision-authorization",
    "grant-authorization",
    "revoke-authorization",
    "approve",
    "reject",
    "approve-all",
    "reject-all",
    "approve-proposal",
    "reject-proposal",
    "approve-memory",
    "reject-memory",
    "decide",
    "decision",
    "execute-decision",
    "decision-execute",
    "manual-execute",
    "execute-manual-decision",
    "recommend-decision",
    "decision-recommendation",
    "rank-decision",
    "readiness-verdict",
    "automatic-readiness",
    "validation-verdict",
    "validate-contract",
    "validate-authorization-envelope",
    "validate-execution-contract",
    "live-authorization-validation",
    "live-validation",
    "input-validation",
    "record-validation",
    "mark-ready",
    "mark-not-ready",
    "write-memory",
    "create-memory",
    "update-memory",
    "delete-memory",
    "mutate-proposal",
    "update-proposal",
    "lifecycle-set",
    "lifecycle-update",
    "lifecycle-mutate",
    "do-not-retry",
    "mark-do-not-retry",
    "guard-set",
    "guard-update",
    "retry-policy-set",
    "retry-policy-update",
    "fetch-source",
    "source-fetch",
    "lookup-source",
    "source-lookup",
    "browse-source",
    "web-fetch",
    "web-search",
    "verify-source",
    "trust-source",
    "score-source",
    "write-provenance",
    "provenance-write",
    "mutate-source",
    "mutate-provenance",
    "mutate-evidence",
    "mutate-citation",
    "archive",
    "stale",
    "cleanup",
    "delete",
    "import",
    "bulk-import",
    "ingest",
    "auto-ingest",
    "auto-approve",
    "auto-reject",
    "inject",
    "inject-memory",
    "call-agent",
    "execute",
    "deploy",
    "API",
    "MCP",
    "connector",
    "start-p4-m3",
    "start-p4-m4",
    "start-p4-m5",
    "start-v7",
    "productize",
}


def test_envelope_field_order_and_ids_are_deterministic():
    assert [
        field.field_order
        for field in list_manual_authorization_evidence_envelope_fields()
    ] == list(range(1, 16))
    assert manual_authorization_evidence_envelope_field_ids() == FIELD_IDS
    assert (
        manual_authorization_evidence_envelope_field_ids()
        == manual_authorization_evidence_envelope_field_ids()
    )


def test_envelope_has_exactly_15_fields():
    assert len(list_manual_authorization_evidence_envelope_fields()) == 15


def test_every_field_has_required_non_empty_values():
    for field in list_manual_authorization_evidence_envelope_fields():
        assert field.field_name.strip()
        assert field.field_purpose.strip()
        assert field.required_evidence_signal.strip()
        assert field.trace_requirement.strip()
        assert field.prohibited_semantics.strip()
        assert field.blocking_signal.strip()
        assert field.future_authorization_note.strip()


def test_markdown_render_contains_all_15_field_ids():
    markdown = render_manual_authorization_evidence_envelope_markdown()

    for field_id in FIELD_IDS:
        assert field_id in markdown


def test_markdown_render_contains_required_boundary_statements():
    markdown = render_manual_authorization_evidence_envelope_markdown()

    assert "P4-M2.3 manual authorization evidence envelope" in markdown
    assert "Read-only evidence envelope definition only" in markdown
    assert "Inspection-only" in markdown
    assert "Not P4-M3" in markdown
    assert "P4-M2.1 execution surface contract definition remains the source field contract" in markdown
    assert "P4-M2.2 execution contract validation matrix remains the source validation matrix definition" in markdown
    assert "Manual authorization evidence envelope does not authorize anything" in markdown
    assert "Authorization is disabled" in markdown
    assert "Authorization command is disabled" in markdown
    assert "Live authorization validation is disabled" in markdown
    assert "Live contract validation is disabled" in markdown
    assert "Input validation is disabled" in markdown
    assert "Record validation is disabled" in markdown
    assert "Validation verdicts are disabled" in markdown
    assert "Readiness verdicts are disabled" in markdown
    assert "Actual decision execution is disabled" in markdown
    assert "Automatic decision execution is disabled" in markdown
    assert "Manual execution command is disabled" in markdown
    assert "Execute command is disabled" in markdown
    assert "No authorization semantics are granted by this evidence envelope." in markdown
    assert "No execution semantics are granted by this evidence envelope." in markdown
    assert "No memory writing is performed by this evidence envelope." in markdown
    assert "No mutation is performed by this evidence envelope." in markdown
    assert "No API/MCP/connector behavior is performed by this evidence envelope." in markdown
    assert "No agent call is performed by this evidence envelope." in markdown


def test_dict_conversion_is_deterministic():
    first = manual_authorization_evidence_envelope_as_dicts()
    second = manual_authorization_evidence_envelope_as_dicts()

    assert first == second
    assert [item["field_id"] for item in first] == list(FIELD_IDS)
    assert set(first[0]) == DATACLASS_FIELDS


def test_status_report_is_deterministic():
    first = manual_authorization_evidence_envelope_report()
    second = manual_authorization_evidence_envelope_report()

    assert first == second
    assert first["phase"] == "P4-M2.3"
    assert first["feature"] == "Manual Authorization Evidence Envelope"
    assert first["mode"] == "read-only"
    assert first["envelope_field_count"] == 15
    assert first["boundary"] == MANUAL_AUTHORIZATION_EVIDENCE_ENVELOPE_BOUNDARY


def test_status_report_has_required_true_flags():
    status = manual_authorization_evidence_envelope_report()

    for flag in TRUE_STATUS_FLAGS:
        assert status[flag] is True


def test_status_report_has_all_disabled_flags_set_to_false():
    status = manual_authorization_evidence_envelope_report()

    for flag in DISABLED_STATUS_FLAGS:
        assert status[flag] is False


def test_status_report_package_version_is_6_16_0():
    assert manual_authorization_evidence_envelope_report()["package_version"] == "6.16.0"


def test_operator_memory_loop_manual_authorization_evidence_envelope_returns_markdown(
    tmp_path,
):
    exit_code, payload, stderr, stdout = _run_operator(
        [
            "memory-loop",
            "manual-authorization-evidence-envelope",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith("# P4-M2.3 Manual Authorization Evidence Envelope\n")
    assert "## Status Report" in stdout
    assert MANUAL_AUTHORIZATION_EVIDENCE_ENVELOPE_BOUNDARY in stdout
    for field_id in FIELD_IDS:
        assert field_id in stdout
    assert "P4-M2.3 manual authorization evidence envelope only." in stdout
    assert "Read-only evidence envelope definition only." in stdout
    assert "Inspection-only." in stdout
    assert "Not P4-M3." in stdout
    assert "P4-M2.1 execution surface contract definition remains the source field contract." in stdout
    assert "P4-M2.2 execution contract validation matrix remains the source validation matrix definition." in stdout
    assert "Manual authorization evidence envelope does not authorize anything." in stdout
    assert "Authorization is disabled." in stdout
    assert "Authorization command is disabled." in stdout
    assert "Live authorization validation is disabled." in stdout
    assert "Live contract validation is disabled." in stdout
    assert "Input validation is disabled." in stdout
    assert "Record validation is disabled." in stdout
    assert "Validation verdicts are disabled." in stdout
    assert "Readiness verdicts are disabled." in stdout
    assert "Actual decision execution is disabled." in stdout
    assert "Automatic decision execution is disabled." in stdout
    assert "Manual execution command is disabled." in stdout
    assert "Execute command is disabled." in stdout
    assert "No authorization semantics are granted by this evidence envelope." in stdout
    assert "No execution semantics are granted by this evidence envelope." in stdout
    assert "No memory writing is performed by this evidence envelope." in stdout
    assert "No mutation is performed by this evidence envelope." in stdout
    assert "No API/MCP/connector behavior is performed by this evidence envelope." in stdout
    assert "No agent call is performed by this evidence envelope." in stdout
    assert not (tmp_path / ".local").exists()


def test_operator_memory_loop_manual_authorization_evidence_envelope_format_markdown_returns_markdown(
    tmp_path,
):
    exit_code, payload, stderr, stdout = _run_operator(
        [
            "memory-loop",
            "manual-authorization-evidence-envelope",
            "--workspace-root",
            str(tmp_path),
            "--format",
            "markdown",
        ]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith("# P4-M2.3 Manual Authorization Evidence Envelope\n")


def test_operator_memory_loop_manual_authorization_evidence_envelope_format_json_returns_deterministic_json(
    tmp_path,
):
    args = [
        "memory-loop",
        "manual-authorization-evidence-envelope",
        "--workspace-root",
        str(tmp_path),
        "--format",
        "json",
    ]
    exit_code, payload, stderr, stdout = _run_operator(args)
    second_code, second_payload, second_stderr, second_stdout = _run_operator(args)

    assert exit_code == 0
    assert stderr == ""
    assert second_code == 0
    assert second_stderr == ""
    assert stdout == second_stdout
    assert payload == second_payload
    assert payload["boundary"] == MANUAL_AUTHORIZATION_EVIDENCE_ENVELOPE_BOUNDARY
    assert payload["count"] == 15
    assert payload["status"] == manual_authorization_evidence_envelope_report()
    assert [item["field_id"] for item in payload["fields"]] == list(FIELD_IDS)
    assert set(payload["fields"][0]) == DATACLASS_FIELDS
    assert not (tmp_path / ".local").exists()


def test_operator_manual_authorization_evidence_envelope_command_is_read_only_and_creates_no_local_storage(
    tmp_path,
):
    markdown_code, _, markdown_stderr, _ = _run_operator(
        [
            "memory-loop",
            "manual-authorization-evidence-envelope",
            "--workspace-root",
            str(tmp_path),
        ]
    )
    json_code, _, json_stderr, _ = _run_operator(
        [
            "memory-loop",
            "manual-authorization-evidence-envelope",
            "--workspace-root",
            str(tmp_path),
            "--format",
            "json",
        ]
    )

    assert markdown_code == 0
    assert markdown_stderr == ""
    assert json_code == 0
    assert json_stderr == ""
    assert not (tmp_path / ".local").exists()


def test_operator_manual_authorization_evidence_envelope_command_creates_no_proposals(
    tmp_path,
):
    _run_operator(
        [
            "memory-loop",
            "manual-authorization-evidence-envelope",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    assert not (tmp_path / ".local" / "subspace_memory" / "proposals.jsonl").exists()


def test_operator_manual_authorization_evidence_envelope_command_creates_no_approved_memories(
    tmp_path,
):
    _run_operator(
        [
            "memory-loop",
            "manual-authorization-evidence-envelope",
            "--workspace-root",
            str(tmp_path),
            "--format",
            "json",
        ]
    )

    assert not (tmp_path / ".local" / "subspace_memory" / "memories.jsonl").exists()


def test_operator_manual_authorization_evidence_envelope_command_creates_no_boundary_or_state_changes(
    tmp_path,
):
    _run_operator(
        [
            "memory-loop",
            "manual-authorization-evidence-envelope",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    storage_root = tmp_path / ".local" / "subspace_memory"
    for filename in (
        "authorization.jsonl",
        "execution.jsonl",
        "approvals.jsonl",
        "rejections.jsonl",
        "validation.jsonl",
        "readiness.jsonl",
        "previews.jsonl",
        "governance_pack.jsonl",
        "final_boundary_audit.jsonl",
        "manual_execution_hardening.jsonl",
        "execution_surface_contract.jsonl",
        "execution_contract_validation_matrix.jsonl",
        "manual_authorization_evidence_envelope.jsonl",
        "closure.jsonl",
        "memories.jsonl",
        "proposals.jsonl",
        "lifecycle.jsonl",
        "do_not_retry.jsonl",
        "sources.jsonl",
        "provenance.jsonl",
        "evidence.jsonl",
        "citations.jsonl",
        "audit.jsonl",
    ):
        assert not (storage_root / filename).exists()
    assert not (tmp_path / ".local").exists()


def test_no_prohibited_memory_loop_write_import_agent_api_mcp_connector_authorization_decision_recommendation_readiness_validation_mutation_p4_m3_p4_m4_p4_m5_v7_productization_commands_are_exposed():
    commands = _memory_loop_commands()

    assert commands == EXPECTED_MEMORY_LOOP_COMMANDS
    assert commands.isdisjoint(PROHIBITED_MEMORY_LOOP_COMMANDS)


def test_existing_p4_m1_0_through_p4_m2_2_memory_loop_commands_still_work(tmp_path):
    expected_prefixes = {
        "checklist": "# P4-M1.0 Human-Gated Memory Loop Checklist\n",
        "review-status": "# P4-M1.1 Human-Gated Proposal Review Status\n",
        "recall-verification-status": "# P4-M1.2 Human-Gated Recall Verification Status\n",
        "lifecycle-verification-status": "# P4-M1.3 Human-Gated Lifecycle Verification Status\n",
        "do-not-retry-verification-status": "# P4-M1.4 Human-Gated Do-Not-Retry Verification Status\n",
        "source-provenance-verification-status": "# P4-M1.5 Source / Provenance Verification Status\n",
        "decision-readiness-status": "# P4-M1.6 Decision Readiness Status\n",
        "manual-decision-preview": "# P4-M1.7 Manual Decision Preview\n",
        "governance-pack-export": "# P4-M1.8 Governance Pack Export\n",
        "final-boundary-audit": "# P4-M1.9 Final Boundary Audit / Closure\n",
        "manual-execution-hardening": "# P4-M2.0 Manual Decision Execution Hardening\n",
        "execution-surface-contract": "# P4-M2.1 Execution Surface Contract Definition\n",
        "execution-contract-validation-matrix": "# P4-M2.2 Execution Contract Validation Matrix\n",
    }

    for command, expected_prefix in expected_prefixes.items():
        _assert_existing_command_still_works(tmp_path, command, expected_prefix)


def test_package_version_remains_6_16_0():
    with open("pyproject.toml", "rb") as handle:
        pyproject = tomllib.load(handle)

    assert pyproject["project"]["version"] == "6.16.0"


def test_no_uv_lock_is_created():
    assert not Path("uv.lock").exists()


def test_no_pyproject_entry_point_is_added_for_manual_authorization_evidence_envelope():
    with open("pyproject.toml", "rb") as handle:
        pyproject = tomllib.load(handle)

    assert "scripts" not in pyproject["project"]
    assert "gui-scripts" not in pyproject["project"]
    assert "console_scripts" not in pyproject["project"].get("entry-points", {})
    entry_points = json.dumps(pyproject["project"].get("entry-points", {}), sort_keys=True)
    assert "p4_m2_manual_authorization_evidence_envelope" not in entry_points
    assert "manual-authorization-evidence-envelope" not in entry_points


def test_custom_markdown_render_accepts_read_only_fields():
    field = ManualAuthorizationEvidenceEnvelopeField(
        field_order=1,
        field_id="custom-manual-authorization-evidence-envelope",
        field_name="Custom Envelope Field",
        field_purpose="Custom inspection-only purpose.",
        required_evidence_signal="Custom evidence signal is visible.",
        trace_requirement="Custom trace requirement is visible.",
        prohibited_semantics="No authorization or execution semantics.",
        blocking_signal="Authorization or execution behavior is introduced.",
        future_authorization_note="A later path may inspect this custom field.",
    )

    markdown = render_manual_authorization_evidence_envelope_markdown([field])

    assert "custom-manual-authorization-evidence-envelope" in markdown
    assert "Custom inspection-only purpose." in markdown


def _assert_existing_command_still_works(
    tmp_path: Path,
    command: str,
    expected_prefix: str,
) -> None:
    exit_code, payload, stderr, stdout = _run_operator(
        ["memory-loop", command, "--workspace-root", str(tmp_path)]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith(expected_prefix)
    assert not (tmp_path / ".local").exists()


def _run_operator(argv: list[str]) -> tuple[int, dict[str, object], str, str]:
    stdout = io.StringIO()
    stderr = io.StringIO()

    exit_code = run_operator_command(argv, stdout=stdout, stderr=stderr)

    stdout_value = stdout.getvalue()
    payload = json.loads(stdout_value) if stdout_value.startswith("{") else {}
    return exit_code, payload, stderr.getvalue(), stdout_value


def _memory_loop_commands() -> set[str]:
    parser = build_parser()
    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            memory_loop_parser = action.choices["memory-loop"]
            break
    else:
        raise AssertionError("memory-loop parser not found")

    for action in memory_loop_parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            return set(action.choices)
    raise AssertionError("memory-loop subcommands not found")
