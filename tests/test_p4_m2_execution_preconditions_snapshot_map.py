from __future__ import annotations

import argparse
import io
import json
import tomllib
from pathlib import Path

from hermes_memory_fabric.p4_m0_subspace_operator import build_parser, run_operator_command
from hermes_memory_fabric.p4_m2_execution_preconditions_snapshot_map import (
    EXECUTION_PRECONDITIONS_SNAPSHOT_MAP_BOUNDARY,
    ExecutionPreconditionsSnapshotMapField,
    execution_preconditions_snapshot_map_as_dicts,
    execution_preconditions_snapshot_map_field_ids,
    execution_preconditions_snapshot_map_report,
    list_execution_preconditions_snapshot_map_fields,
    render_execution_preconditions_snapshot_map_markdown,
)


FIELD_IDS = (
    "execution-preconditions-snapshot-map-id",
    "execution-surface-reference",
    "execution-contract-validation-matrix-reference",
    "manual-authorization-evidence-envelope-reference",
    "human-confirmation-snapshot-reference",
    "manual-decision-reference",
    "operator-reference",
    "precondition-category",
    "precondition-snapshot-signal",
    "precondition-evidence-reference",
    "risk-blocking-signal",
    "dependency-boundary-signal",
    "revocation-or-expiry-signal",
    "audit-trace-reference",
    "precondition-semantics-disabled",
    "validation-semantics-disabled",
    "execution-semantics-disabled",
)

DATACLASS_FIELDS = {
    "field_order",
    "field_id",
    "field_name",
    "field_purpose",
    "snapshot_signal",
    "evidence_boundary",
    "prohibited_semantics",
    "blocking_boundary",
    "future_precondition_note",
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
}

PREVIOUS_P4_M2_4_READ_ONLY_COMMANDS = EXPECTED_MEMORY_LOOP_COMMANDS - {
    "execution-preconditions-snapshot-map",
    "execution-risk-acknowledgement-map",
    "execution-risk-acceptance-prohibition-map",
    "execution-risk-waiver-prohibition-map",
    "execution-decision-non-equivalence-map",
    "execution-decision-recommendation-prohibition-map",
    "execution-decision-default-denial-boundary-map",
}

BOUNDARY_PHRASES = (
    "P4-M2.5",
    "Execution Preconditions Snapshot Map",
    "Definition-only",
    "Inspection-only",
    "Read-only",
    "No execution",
    "No confirmation",
    "No authorization",
    "No approval",
    "No rejection",
    "No memory mutation",
    "No memory record creation",
    "No memory record update",
    "No memory record deletion",
    "No proposal mutation",
    "No lifecycle mutation",
    "No retry policy mutation",
    "No source fetching",
    "No provenance writing",
    "No evidence mutation",
    "No citation mutation",
    "No live confirmation validation",
    "No live authorization validation",
    "No live contract validation",
    "No input validation",
    "No record validation",
    "No validation verdict",
    "No readiness verdict",
    "No automatic readiness verdict",
    "No decision recommendation",
    "No decision ranking",
    "No confirmation semantics",
    "No authorization semantics",
    "No execution semantics",
    "No API",
    "No MCP",
    "No connector",
    "No agent call",
    "No Codex/Hermes/ChatGPT product-code auto-call",
    "No P4-M3",
    "No P4-M4",
    "No P4-M5",
    "No v7",
    "No productization",
    "No UI",
    "No Operator Console",
    "No MVP",
    "No deploy",
    "No full Memory Graph",
)

TRUE_STATUS_FLAGS = (
    "definition_only",
    "inspection_only",
    "p4_m2_started",
    "execution_surface_contract_definition_available",
    "execution_contract_validation_matrix_available",
    "manual_authorization_evidence_envelope_available",
    "human_confirmation_snapshot_contract_available",
    "execution_preconditions_snapshot_map_started",
    "execution_preconditions_snapshot_map_definition_only",
    "snapshot_map_fields_defined",
    "precondition_snapshot_structure_defined",
)

DISABLED_STATUS_FLAGS = (
    "execution_enabled",
    "confirmation_enabled",
    "authorization_enabled",
    "approval_enabled",
    "rejection_enabled",
    "memory_mutation_enabled",
    "memory_record_creation_enabled",
    "memory_record_update_enabled",
    "memory_record_deletion_enabled",
    "proposal_mutation_enabled",
    "lifecycle_mutation_enabled",
    "retry_policy_mutation_enabled",
    "source_fetching_enabled",
    "provenance_writing_enabled",
    "evidence_mutation_enabled",
    "citation_mutation_enabled",
    "live_confirmation_validation_enabled",
    "live_authorization_validation_enabled",
    "live_contract_validation_enabled",
    "input_validation_enabled",
    "record_validation_enabled",
    "validation_verdict_enabled",
    "readiness_verdict_enabled",
    "automatic_readiness_verdict_enabled",
    "decision_recommendation_enabled",
    "decision_ranking_enabled",
    "confirmation_semantics_granted",
    "authorization_semantics_granted",
    "execution_semantics_granted",
    "api_enabled",
    "mcp_enabled",
    "connector_enabled",
    "agent_call_enabled",
    "codex_hermes_chatgpt_product_code_auto_call_enabled",
    "p4_m3_started",
    "p4_m4_started",
    "p4_m5_started",
    "v7_started",
    "productization_started",
    "ui_started",
    "operator_console_started",
    "mvp_started",
    "deploy_started",
    "full_memory_graph_started",
)

PROHIBITED_MEMORY_LOOP_COMMANDS = {
    "confirm",
    "confirmation",
    "authorize",
    "authorization",
    "approve",
    "reject",
    "execute",
    "execute-decision",
    "manual-execute",
    "recommend-decision",
    "rank-decision",
    "readiness-verdict",
    "validation-verdict",
    "validate-contract",
    "validate-confirmation-snapshot",
    "validate-authorization-envelope",
    "live-confirmation-validation",
    "live-authorization-validation",
    "live-validation",
    "input-validation",
    "record-validation",
    "write-memory",
    "create-memory",
    "update-memory",
    "delete-memory",
    "mutate-proposal",
    "lifecycle-mutate",
    "retry-policy-update",
    "fetch-source",
    "source-fetch",
    "write-provenance",
    "mutate-evidence",
    "mutate-citation",
    "call-agent",
    "API",
    "MCP",
    "connector",
    "start-p4-m3",
    "start-p4-m4",
    "start-p4-m5",
    "start-v7",
    "productize",
    "operator-console",
    "ui",
    "deploy",
}


def test_snapshot_map_field_order_count_and_ids_are_stable():
    fields = list_execution_preconditions_snapshot_map_fields()

    assert [field.field_order for field in fields] == list(range(1, 18))
    assert len(fields) == 17
    assert execution_preconditions_snapshot_map_field_ids() == FIELD_IDS
    assert execution_preconditions_snapshot_map_field_ids() == FIELD_IDS


def test_every_snapshot_map_field_has_required_non_empty_values():
    for field in list_execution_preconditions_snapshot_map_fields():
        assert field.field_name.strip()
        assert field.field_purpose.strip()
        assert field.snapshot_signal.strip()
        assert field.evidence_boundary.strip()
        assert field.prohibited_semantics.strip()
        assert field.blocking_boundary.strip()
        assert field.future_precondition_note.strip()


def test_markdown_output_is_stable_and_contains_required_boundaries():
    first = render_execution_preconditions_snapshot_map_markdown()
    second = render_execution_preconditions_snapshot_map_markdown()

    assert first == second
    assert first.startswith("# P4-M2.5 Execution Preconditions Snapshot Map\n")
    assert EXECUTION_PRECONDITIONS_SNAPSHOT_MAP_BOUNDARY in first
    for field_id in FIELD_IDS:
        assert field_id in first
    for phrase in BOUNDARY_PHRASES:
        assert phrase in first


def test_json_output_is_stable_and_contains_required_boundaries(tmp_path):
    args = [
        "memory-loop",
        "execution-preconditions-snapshot-map",
        "--workspace-root",
        str(tmp_path),
        "--format",
        "json",
    ]
    first_code, first_payload, first_stderr, first_stdout = _run_operator(args)
    second_code, second_payload, second_stderr, second_stdout = _run_operator(args)

    assert first_code == 0
    assert second_code == 0
    assert first_stderr == ""
    assert second_stderr == ""
    assert first_stdout == second_stdout
    assert first_payload == second_payload
    assert first_payload["boundary"] == EXECUTION_PRECONDITIONS_SNAPSHOT_MAP_BOUNDARY
    assert first_payload["count"] == 17
    assert first_payload["status"] == execution_preconditions_snapshot_map_report()
    assert [item["field_id"] for item in first_payload["fields"]] == list(FIELD_IDS)
    assert set(first_payload["fields"][0]) == DATACLASS_FIELDS
    for phrase in BOUNDARY_PHRASES:
        assert phrase in first_stdout
    assert not (tmp_path / ".local").exists()


def test_dict_conversion_and_status_report_are_deterministic():
    first_fields = execution_preconditions_snapshot_map_as_dicts()
    second_fields = execution_preconditions_snapshot_map_as_dicts()
    first_status = execution_preconditions_snapshot_map_report()
    second_status = execution_preconditions_snapshot_map_report()

    assert first_fields == second_fields
    assert [field["field_id"] for field in first_fields] == list(FIELD_IDS)
    assert first_status == second_status
    assert first_status["phase"] == "P4-M2.5"
    assert first_status["feature"] == "Execution Preconditions Snapshot Map"
    assert first_status["mode"] == "read-only"
    assert first_status["snapshot_map_field_count"] == 17
    assert first_status["boundary"] == EXECUTION_PRECONDITIONS_SNAPSHOT_MAP_BOUNDARY


def test_status_report_locks_true_and_disabled_flags():
    status = execution_preconditions_snapshot_map_report()

    for flag in TRUE_STATUS_FLAGS:
        assert status[flag] is True
    for flag in DISABLED_STATUS_FLAGS:
        assert status[flag] is False


def test_operator_markdown_default_is_read_only_and_creates_no_local_storage(tmp_path):
    exit_code, payload, stderr, stdout = _run_operator(
        [
            "memory-loop",
            "execution-preconditions-snapshot-map",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith("# P4-M2.5 Execution Preconditions Snapshot Map\n")
    assert "## Status Report" in stdout
    assert EXECUTION_PRECONDITIONS_SNAPSHOT_MAP_BOUNDARY in stdout
    for phrase in BOUNDARY_PHRASES:
        assert phrase in stdout
    assert not (tmp_path / ".local").exists()


def test_operator_markdown_format_is_explicit_and_stable(tmp_path):
    args = [
        "memory-loop",
        "execution-preconditions-snapshot-map",
        "--workspace-root",
        str(tmp_path),
        "--format",
        "markdown",
    ]
    first_code, first_payload, first_stderr, first_stdout = _run_operator(args)
    second_code, second_payload, second_stderr, second_stdout = _run_operator(args)

    assert first_code == 0
    assert second_code == 0
    assert first_payload == {}
    assert second_payload == {}
    assert first_stderr == ""
    assert second_stderr == ""
    assert first_stdout == second_stdout
    assert first_stdout.startswith("# P4-M2.5 Execution Preconditions Snapshot Map\n")
    assert not (tmp_path / ".local").exists()


def test_command_does_not_instantiate_writable_store(monkeypatch, tmp_path):
    def fail_store_creation(*_args, **_kwargs):
        raise AssertionError("writable store must not be instantiated")

    monkeypatch.setattr(
        "hermes_memory_fabric.p4_m0_subspace_operator.create_workspace_subspace_memory_store",
        fail_store_creation,
    )

    markdown_code, _, markdown_stderr, markdown_stdout = _run_operator(
        [
            "memory-loop",
            "execution-preconditions-snapshot-map",
            "--workspace-root",
            str(tmp_path),
        ]
    )
    json_code, json_payload, json_stderr, _ = _run_operator(
        [
            "memory-loop",
            "execution-preconditions-snapshot-map",
            "--workspace-root",
            str(tmp_path),
            "--format",
            "json",
        ]
    )

    assert markdown_code == 0
    assert markdown_stderr == ""
    assert markdown_stdout.startswith("# P4-M2.5")
    assert json_code == 0
    assert json_stderr == ""
    assert json_payload["count"] == 17
    assert not (tmp_path / ".local").exists()


def test_command_creates_no_storage_files_or_state_changes(tmp_path):
    _run_operator(
        [
            "memory-loop",
            "execution-preconditions-snapshot-map",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    storage_root = tmp_path / ".local" / "subspace_memory"
    for filename in (
        "execution_preconditions_snapshot_map.jsonl",
        "confirmation.jsonl",
        "authorization.jsonl",
        "execution.jsonl",
        "approvals.jsonl",
        "rejections.jsonl",
        "validation.jsonl",
        "readiness.jsonl",
        "memories.jsonl",
        "proposals.jsonl",
        "lifecycle.jsonl",
        "retry_policy.jsonl",
        "sources.jsonl",
        "provenance.jsonl",
        "evidence.jsonl",
        "citations.jsonl",
        "audit.jsonl",
    ):
        assert not (storage_root / filename).exists()
    assert not (tmp_path / ".local").exists()


def test_read_only_allowlist_includes_new_command_and_preserves_previous_p4_m2_4_commands():
    commands = _memory_loop_commands()

    assert commands == EXPECTED_MEMORY_LOOP_COMMANDS
    assert "execution-preconditions-snapshot-map" in commands
    assert PREVIOUS_P4_M2_4_READ_ONLY_COMMANDS.issubset(commands)
    assert commands.isdisjoint(PROHIBITED_MEMORY_LOOP_COMMANDS)


def test_existing_p4_m1_0_through_p4_m2_4_memory_loop_commands_still_work(tmp_path):
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
        "manual-authorization-evidence-envelope": "# P4-M2.3 Manual Authorization Evidence Envelope\n",
        "human-confirmation-snapshot-contract": "# P4-M2.4 Human Confirmation Snapshot Contract\n",
    }

    for command, expected_prefix in expected_prefixes.items():
        exit_code, payload, stderr, stdout = _run_operator(
            ["memory-loop", command, "--workspace-root", str(tmp_path)]
        )
        assert exit_code == 0
        assert payload == {}
        assert stderr == ""
        assert stdout.startswith(expected_prefix)
        assert not (tmp_path / ".local").exists()


def test_package_version_lock_and_no_entry_point():
    with open("pyproject.toml", "rb") as handle:
        pyproject = tomllib.load(handle)

    assert pyproject["project"]["version"] == "6.16.0"
    assert "scripts" not in pyproject["project"]
    assert "gui-scripts" not in pyproject["project"]
    assert "console_scripts" not in pyproject["project"].get("entry-points", {})
    entry_points = json.dumps(pyproject["project"].get("entry-points", {}), sort_keys=True)
    assert "p4_m2_execution_preconditions_snapshot_map" not in entry_points
    assert "execution-preconditions-snapshot-map" not in entry_points


def test_no_uv_lock_is_created():
    assert not Path("uv.lock").exists()


def test_custom_markdown_render_accepts_read_only_fields():
    field = ExecutionPreconditionsSnapshotMapField(
        field_order=1,
        field_id="custom-execution-preconditions-snapshot-map",
        field_name="Custom Snapshot Map Field",
        field_purpose="Custom inspection-only purpose.",
        snapshot_signal="Custom snapshot signal is visible.",
        evidence_boundary="Custom evidence boundary is read-only.",
        prohibited_semantics="No execution, confirmation, authorization, validation, readiness, or mutation semantics.",
        blocking_boundary="Execution, confirmation, authorization, validation, readiness, or mutation behavior is introduced.",
        future_precondition_note="A later path may inspect this custom field.",
    )

    markdown = render_execution_preconditions_snapshot_map_markdown([field])

    assert "custom-execution-preconditions-snapshot-map" in markdown
    assert "Custom inspection-only purpose." in markdown


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
