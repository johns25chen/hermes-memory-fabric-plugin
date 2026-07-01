from __future__ import annotations

import argparse
import io
import json
import tomllib
from pathlib import Path

from hermes_memory_fabric.p4_m0_subspace_operator import build_parser, run_operator_command
from hermes_memory_fabric.p4_m2_execution_surface_contract_definition import (
    EXECUTION_SURFACE_CONTRACT_BOUNDARY,
    ExecutionSurfaceContractField,
    execution_surface_contract_as_dicts,
    execution_surface_contract_field_ids,
    execution_surface_contract_report,
    list_execution_surface_contract_fields,
    render_execution_surface_contract_markdown,
)


FIELD_IDS = (
    "execution-surface-id",
    "human-authorization-reference",
    "manual-decision-reference",
    "execution-intent-declaration",
    "target-record-reference",
    "allowed-operation-envelope",
    "precondition-evidence",
    "risk-and-blocking-signals",
    "audit-trace-id",
    "operator-confirmation-placeholder",
    "execution-preview-output",
    "rollback-consideration",
    "side-effect-boundary",
    "external-system-boundary",
    "authorization-semantics-disabled",
    "execution-semantics-disabled",
)

DATACLASS_FIELDS = {
    "field_order",
    "field_id",
    "field_name",
    "field_purpose",
    "required_description",
    "inspection_signal",
    "prohibited_semantics",
    "blocking_signal",
}

DISABLED_STATUS_FLAGS = (
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

PROHIBITED_MEMORY_LOOP_COMMANDS = {
    "authorize",
    "authorization",
    "authorize-decision",
    "decision-authorization",
    "grant-authorization",
    "revoke-authorization",
    "validate-authorization-envelope",
    "live-authorization-validation",
    "decide",
    "decision",
    "execute-decision",
    "decision-execute",
    "manual-execute",
    "execute-manual-decision",
    "approve",
    "reject",
    "approve-all",
    "reject-all",
    "approve-proposal",
    "reject-proposal",
    "approve-memory",
    "reject-memory",
    "recommend-decision",
    "decision-recommendation",
    "rank-decision",
    "readiness-verdict",
    "automatic-readiness",
    "validation-verdict",
    "validate-contract",
    "validate-execution-contract",
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


def test_execution_surface_contract_field_order_is_deterministic():
    assert [
        field.field_order
        for field in list_execution_surface_contract_fields()
    ] == list(range(1, 17))
    assert execution_surface_contract_field_ids() == FIELD_IDS
    assert execution_surface_contract_field_ids() == execution_surface_contract_field_ids()


def test_execution_surface_contract_has_exactly_16_fields():
    assert len(list_execution_surface_contract_fields()) == 16


def test_field_ids_match_required_field_ids():
    assert execution_surface_contract_field_ids() == FIELD_IDS


def test_every_field_has_required_non_empty_values():
    for field in list_execution_surface_contract_fields():
        assert field.field_name.strip()
        assert field.field_purpose.strip()
        assert field.required_description.strip()
        assert field.inspection_signal.strip()
        assert field.prohibited_semantics.strip()
        assert field.blocking_signal.strip()


def test_markdown_render_contains_all_16_field_ids():
    markdown = render_execution_surface_contract_markdown()

    for field_id in FIELD_IDS:
        assert field_id in markdown


def test_markdown_render_contains_required_boundary_statements():
    markdown = render_execution_surface_contract_markdown()

    assert "P4-M2.1 execution surface contract definition" in markdown
    assert "Read-only contract/schema/trace field definition only" in markdown
    assert "Inspection-only" in markdown
    assert "Not P4-M3" in markdown
    assert "Actual decision execution is disabled" in markdown
    assert "Automatic decision execution is disabled" in markdown
    assert "Manual execution command is disabled" in markdown
    assert "Execute command is disabled" in markdown
    assert "No authorization semantics are granted by this contract definition." in markdown
    assert "No execution semantics are granted by this contract definition." in markdown
    assert "No memory writing is performed by this contract definition." in markdown
    assert "No mutation is performed by this contract definition." in markdown
    assert "No API/MCP/connector behavior is performed by this contract definition." in markdown
    assert "No agent call is performed by this contract definition." in markdown


def test_dict_conversion_is_deterministic():
    first = execution_surface_contract_as_dicts()
    second = execution_surface_contract_as_dicts()

    assert first == second
    assert [item["field_id"] for item in first] == list(FIELD_IDS)
    assert set(first[0]) == DATACLASS_FIELDS


def test_status_report_is_deterministic():
    first = execution_surface_contract_report()
    second = execution_surface_contract_report()

    assert first == second
    assert first["phase"] == "P4-M2.1"
    assert first["feature"] == "Execution Surface Contract Definition"
    assert first["mode"] == "read-only"
    assert first["contract_field_count"] == 16
    assert first["boundary"] == EXECUTION_SURFACE_CONTRACT_BOUNDARY


def test_status_report_has_required_true_flags():
    status = execution_surface_contract_report()

    assert status["p4_m2_started"] is True
    assert status["execution_surface_contract_definition_started"] is True
    assert status["execution_surface_contract_only"] is True
    assert status["schema_definition_only"] is True
    assert status["trace_field_definition_only"] is True
    assert status["inspection_only"] is True


def test_status_report_has_required_execution_and_semantic_flags_disabled():
    status = execution_surface_contract_report()

    assert status["actual_decision_execution_enabled"] is False
    assert status["automatic_decision_execution_enabled"] is False
    assert status["manual_execution_command_enabled"] is False
    assert status["execute_command_enabled"] is False
    assert status["authorization_semantics_granted"] is False
    assert status["execution_semantics_granted"] is False


def test_status_report_has_all_disabled_flags_set_to_false():
    status = execution_surface_contract_report()

    for flag in DISABLED_STATUS_FLAGS:
        assert status[flag] is False


def test_status_report_package_version_is_6_16_0():
    assert execution_surface_contract_report()["package_version"] == "6.16.0"


def test_operator_memory_loop_execution_surface_contract_returns_markdown(tmp_path):
    exit_code, payload, stderr, stdout = _run_operator(
        ["memory-loop", "execution-surface-contract", "--workspace-root", str(tmp_path)]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith("# P4-M2.1 Execution Surface Contract Definition\n")
    assert "## Status Report" in stdout
    assert EXECUTION_SURFACE_CONTRACT_BOUNDARY in stdout
    for field_id in FIELD_IDS:
        assert field_id in stdout
    assert "P4-M2.1 execution surface contract definition only." in stdout
    assert "Read-only contract/schema/trace field definition only." in stdout
    assert "Inspection-only." in stdout
    assert "Not P4-M3." in stdout
    assert "Actual decision execution is disabled." in stdout
    assert "Automatic decision execution is disabled." in stdout
    assert "Manual execution command is disabled." in stdout
    assert "Execute command is disabled." in stdout
    assert "No authorization semantics are granted by this contract definition." in stdout
    assert "No execution semantics are granted by this contract definition." in stdout
    assert "No memory writing is performed by this contract definition." in stdout
    assert "No mutation is performed by this contract definition." in stdout
    assert "No API/MCP/connector behavior is performed by this contract definition." in stdout
    assert "No agent call is performed by this contract definition." in stdout
    assert not (tmp_path / ".local").exists()


def test_operator_memory_loop_execution_surface_contract_format_markdown_returns_markdown(
    tmp_path,
):
    exit_code, payload, stderr, stdout = _run_operator(
        [
            "memory-loop",
            "execution-surface-contract",
            "--workspace-root",
            str(tmp_path),
            "--format",
            "markdown",
        ]
    )

    assert exit_code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith("# P4-M2.1 Execution Surface Contract Definition\n")


def test_operator_memory_loop_execution_surface_contract_format_json_returns_deterministic_json(
    tmp_path,
):
    args = [
        "memory-loop",
        "execution-surface-contract",
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
    assert payload["boundary"] == EXECUTION_SURFACE_CONTRACT_BOUNDARY
    assert payload["count"] == 16
    assert payload["status"] == execution_surface_contract_report()
    assert [item["field_id"] for item in payload["fields"]] == list(FIELD_IDS)
    assert set(payload["fields"][0]) == DATACLASS_FIELDS
    assert not (tmp_path / ".local").exists()


def test_operator_execution_surface_contract_command_is_read_only_and_creates_no_local_storage(
    tmp_path,
):
    markdown_code, _, markdown_stderr, _ = _run_operator(
        ["memory-loop", "execution-surface-contract", "--workspace-root", str(tmp_path)]
    )
    json_code, _, json_stderr, _ = _run_operator(
        [
            "memory-loop",
            "execution-surface-contract",
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


def test_operator_execution_surface_contract_command_creates_no_proposals(tmp_path):
    _run_operator(
        ["memory-loop", "execution-surface-contract", "--workspace-root", str(tmp_path)]
    )

    assert not (tmp_path / ".local" / "subspace_memory" / "proposals.jsonl").exists()


def test_operator_execution_surface_contract_command_creates_no_approved_memories(
    tmp_path,
):
    _run_operator(
        [
            "memory-loop",
            "execution-surface-contract",
            "--workspace-root",
            str(tmp_path),
            "--format",
            "json",
        ]
    )

    assert not (tmp_path / ".local" / "subspace_memory" / "memories.jsonl").exists()


def test_operator_execution_surface_contract_command_creates_no_boundary_or_state_changes(
    tmp_path,
):
    _run_operator(
        ["memory-loop", "execution-surface-contract", "--workspace-root", str(tmp_path)]
    )

    storage_root = tmp_path / ".local" / "subspace_memory"
    assert not (storage_root / "decisions.jsonl").exists()
    assert not (storage_root / "execution.jsonl").exists()
    assert not (storage_root / "approvals.jsonl").exists()
    assert not (storage_root / "rejections.jsonl").exists()
    assert not (storage_root / "readiness.jsonl").exists()
    assert not (storage_root / "previews.jsonl").exists()
    assert not (storage_root / "governance_pack.jsonl").exists()
    assert not (storage_root / "final_boundary_audit.jsonl").exists()
    assert not (storage_root / "manual_execution_hardening.jsonl").exists()
    assert not (storage_root / "execution_surface_contract.jsonl").exists()
    assert not (storage_root / "closure.jsonl").exists()
    assert not (storage_root / "memories.jsonl").exists()
    assert not (storage_root / "proposals.jsonl").exists()
    assert not (storage_root / "lifecycle.jsonl").exists()
    assert not (storage_root / "do_not_retry.jsonl").exists()
    assert not (storage_root / "sources.jsonl").exists()
    assert not (storage_root / "provenance.jsonl").exists()
    assert not (storage_root / "evidence.jsonl").exists()
    assert not (storage_root / "citations.jsonl").exists()
    assert not (storage_root / "audit.jsonl").exists()
    assert not (tmp_path / ".local").exists()


def test_no_prohibited_memory_loop_write_import_agent_api_mcp_connector_decision_recommendation_readiness_mutation_p4_m3_p4_m4_p4_m5_v7_productization_commands_are_exposed():
    commands = _memory_loop_commands()

    assert commands == EXPECTED_MEMORY_LOOP_COMMANDS
    assert commands.isdisjoint(PROHIBITED_MEMORY_LOOP_COMMANDS)


def test_existing_p4_m1_0_memory_loop_checklist_still_works(tmp_path):
    _assert_existing_command_still_works(
        tmp_path,
        "checklist",
        "# P4-M1.0 Human-Gated Memory Loop Checklist\n",
    )


def test_existing_p4_m1_1_memory_loop_review_status_still_works(tmp_path):
    _assert_existing_command_still_works(
        tmp_path,
        "review-status",
        "# P4-M1.1 Human-Gated Proposal Review Status\n",
    )


def test_existing_p4_m1_2_memory_loop_recall_verification_status_still_works(
    tmp_path,
):
    _assert_existing_command_still_works(
        tmp_path,
        "recall-verification-status",
        "# P4-M1.2 Human-Gated Recall Verification Status\n",
    )


def test_existing_p4_m1_3_memory_loop_lifecycle_verification_status_still_works(
    tmp_path,
):
    _assert_existing_command_still_works(
        tmp_path,
        "lifecycle-verification-status",
        "# P4-M1.3 Human-Gated Lifecycle Verification Status\n",
    )


def test_existing_p4_m1_4_memory_loop_do_not_retry_verification_status_still_works(
    tmp_path,
):
    _assert_existing_command_still_works(
        tmp_path,
        "do-not-retry-verification-status",
        "# P4-M1.4 Human-Gated Do-Not-Retry Verification Status\n",
    )


def test_existing_p4_m1_5_memory_loop_source_provenance_verification_status_still_works(
    tmp_path,
):
    _assert_existing_command_still_works(
        tmp_path,
        "source-provenance-verification-status",
        "# P4-M1.5 Source / Provenance Verification Status\n",
    )


def test_existing_p4_m1_6_memory_loop_decision_readiness_status_still_works(
    tmp_path,
):
    _assert_existing_command_still_works(
        tmp_path,
        "decision-readiness-status",
        "# P4-M1.6 Decision Readiness Status\n",
    )


def test_existing_p4_m1_7_memory_loop_manual_decision_preview_still_works(
    tmp_path,
):
    _assert_existing_command_still_works(
        tmp_path,
        "manual-decision-preview",
        "# P4-M1.7 Manual Decision Preview\n",
    )


def test_existing_p4_m1_8_memory_loop_governance_pack_export_still_works(
    tmp_path,
):
    _assert_existing_command_still_works(
        tmp_path,
        "governance-pack-export",
        "# P4-M1.8 Governance Pack Export\n",
    )


def test_existing_p4_m1_9_memory_loop_final_boundary_audit_still_works(
    tmp_path,
):
    _assert_existing_command_still_works(
        tmp_path,
        "final-boundary-audit",
        "# P4-M1.9 Final Boundary Audit / Closure\n",
    )


def test_existing_p4_m2_0_memory_loop_manual_execution_hardening_still_works(
    tmp_path,
):
    _assert_existing_command_still_works(
        tmp_path,
        "manual-execution-hardening",
        "# P4-M2.0 Manual Decision Execution Hardening\n",
    )


def test_package_version_remains_6_16_0():
    with open("pyproject.toml", "rb") as handle:
        pyproject = tomllib.load(handle)

    assert pyproject["project"]["version"] == "6.16.0"


def test_no_uv_lock_is_created():
    assert not Path("uv.lock").exists()


def test_no_pyproject_entry_point_is_added_for_execution_surface_contract():
    with open("pyproject.toml", "rb") as handle:
        pyproject = tomllib.load(handle)

    assert "scripts" not in pyproject["project"]
    assert "gui-scripts" not in pyproject["project"]
    assert "console_scripts" not in pyproject["project"].get("entry-points", {})
    entry_points = json.dumps(pyproject["project"].get("entry-points", {}), sort_keys=True)
    assert "p4_m2_execution_surface_contract_definition" not in entry_points
    assert "execution-surface-contract" not in entry_points


def test_custom_markdown_render_accepts_read_only_fields():
    field = ExecutionSurfaceContractField(
        field_order=1,
        field_id="custom-execution-surface-contract",
        field_name="Custom execution surface contract",
        field_purpose="Keep the custom contract field read-only.",
        required_description="A custom contract field description.",
        inspection_signal="Custom field text is visible.",
        prohibited_semantics="No execution semantics.",
        blocking_signal="Execution behavior is introduced.",
    )

    markdown = render_execution_surface_contract_markdown([field])

    assert "custom-execution-surface-contract" in markdown
    assert "Keep the custom contract field read-only." in markdown


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
