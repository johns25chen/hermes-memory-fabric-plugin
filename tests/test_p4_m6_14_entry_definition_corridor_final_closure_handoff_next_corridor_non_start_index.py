from __future__ import annotations

import argparse
import dataclasses
import io
import json
from pathlib import Path

import hermes_memory_fabric.p4_m0_subspace_operator as operator
from hermes_memory_fabric.p4_m0_subspace_operator import (
    build_parser,
    run_operator_command,
)
from hermes_memory_fabric.p4_m6_13_entry_definition_corridor_closure_review import (
    FALSE_STATUS_FLAGS as P4_M6_13_FALSE_STATUS_FLAGS,
    TRUE_STATUS_FLAGS as P4_M6_13_TRUE_STATUS_FLAGS,
)
from hermes_memory_fabric.p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index import (
    BOUNDARY_PHRASE_LINES,
    FALSE_STATUS_FLAGS,
    MEMORY_LOOP_COMMAND,
    MEMORY_LOOP_COMMAND_INVOCATION,
    P4_M5_PRE_CORRIDOR_REFERENCE_CHAIN,
    P4_M6_14_ENTRY_DEFINITION_CORRIDOR_FINAL_CLOSURE_HANDOFF_NEXT_CORRIDOR_NON_START_INDEX_BOUNDARY,
    P4_M6_14_FALSE_STATUS_FLAGS,
    P4_M6_14_TRUE_STATUS_FLAGS,
    P4_M6_CORRIDOR_REFERENCE_CHAIN,
    PRIOR_DEFINITION_LAYER_REFERENCE_CHAIN,
    STATUS_DIRECTION,
    TRUE_STATUS_FLAGS,
    P4M614EntryDefinitionCorridorFinalClosureHandoffNextCorridorNonStartIndexField,
    list_p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_fields,
    p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_field_ids,
    p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_report,
    p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_status_shape,
    render_p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_markdown,
    run_p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_command,
)


FIELD_IDS = tuple(
    line
    for line in """
p4_m6_14_stage
p4_m6_14_surface_id
p4_m6_14_direct_prior_reference
p4_m6_14_prior_reference_chain
p4_m6_14_closed_corridor_scope
p4_m6_14_final_closure_handoff_index
p4_m6_14_corridor_closed_declaration_index
p4_m6_14_closure_review_reference_index
p4_m6_14_corridor_lineage_index
p4_m6_14_operator_alignment_index
p4_m6_14_documentation_alignment_index
p4_m6_14_status_shape_alignment_index
p4_m6_14_final_closure_non_verdict_index
p4_m6_14_final_closure_non_approval_index
p4_m6_14_final_closure_non_authorization_index
p4_m6_14_final_closure_non_confirmation_index
p4_m6_14_entry_non_validation_index
p4_m6_14_readiness_non_determination_index
p4_m6_14_routing_non_execution_index
p4_m6_14_record_non_creation_index
p4_m6_14_storage_non_persistence_index
p4_m6_14_mutation_absence_index
p4_m6_14_next_corridor_and_v7_non_start_operator_guard
""".splitlines()
    if line
)

REQUIRED_BOUNDARY_PHRASES = tuple(
    line
    for line in """
P4-M6.14
Entry Definition Corridor Final Closure Handoff
Next Corridor Non-Start Index
P4-M6.14 Entry Definition Corridor Final Closure Handoff / Next Corridor Non-Start Index
static entry definition corridor final closure handoff and next corridor non-start index
final-closure-handoff-index-only
corridor-closed-declaration-index-only
closure-review-reference-index-only
corridor-lineage-index-only
operator-alignment-index-only
documentation-alignment-index-only
status-shape-alignment-index-only
next-corridor-non-start-index-only
operator-guard-index-only
definition-only
declaration-only
read-only
inspection-only
static declared index rows only
P4-M6 corridor closed
handoff declaration only
P4-M6.13 closure review remains the direct prior reference
no repeated closure review
no live repository inspection
no live workspace inspection
no validation
no inference
no scoring
no verdict
no readiness determination
no approval
no authorization
no confirmation
no acceptance
no rejection
no deferral
no escalation
no override
no resolution
no safeguard activation
no safeguard enforcement
no prioritization
no selection
no recommendation
no entry blocking
no entry unblocking
no routing
no execution
no record creation
no storage
no persistence
no mutation
no next corridor start
no P4-M7.0 start
no API
no MCP
no Connector
no Agent
no network
no OAuth
no credential inspection
no secret inspection
no v7
no productization
no UI
no Operator Console
""".splitlines()
    if line
)

P4_M6_CHAIN = (
    "P4-M6.13 Entry Definition Corridor Closure Review",
    "P4-M6.12 Entry Safeguard Non-Activation Surface",
    "P4-M6.11 Entry Risk Non-Mitigation Surface",
    "P4-M6.10 Entry Constraint Non-Enforcement Surface",
    "P4-M6.9 Entry Dependency Non-Activation Surface",
    "P4-M6.8 Entry Ambiguity Non-Inference Surface",
    "P4-M6.7 Entry Conflict Non-Resolution Surface",
    "P4-M6.6 Entry Exception Non-Override Surface",
    "P4-M6.5 Entry Escalation Non-Routing Surface",
    "P4-M6.4 Entry Rejection Non-Execution Surface",
    "P4-M6.3 Entry Deferral Non-Execution Surface",
    "P4-M6.2 Entry Acceptance Non-Evidence Surface",
    "P4-M6.1 Entry Preconditions Definition Surface",
    "P4-M6.0 Next Corridor Entry Boundary Contract",
)

P4_M5_CHAIN = (
    "P4-M5.6 Final Closure Handoff / Next Corridor Non-Start Index",
    "P4-M5.5 Readiness Audit Closure / Non-Start Boundary Seal",
    "P4-M5.4 API / MCP / Connector Cross-Surface Alignment Map",
    "P4-M5.3 Connector Readiness Audit Surface Map",
    "P4-M5.2 MCP Readiness Audit Surface Map",
    "P4-M5.1 API Readiness Audit Surface Map",
    "P4-M5.0 API / MCP / Connector Readiness Audit Boundary Contract",
)


def _run_operator(argv: list[str]) -> tuple[int, object, str, str]:
    stdout = io.StringIO()
    stderr = io.StringIO()
    code = run_operator_command(argv, stdout=stdout, stderr=stderr)
    output = stdout.getvalue()
    try:
        payload = json.loads(output)
    except json.JSONDecodeError:
        payload = {}
    return code, payload, stderr.getvalue(), output


def _memory_loop_subcommands(parser: argparse.ArgumentParser) -> set[str]:
    command_action = next(
        action
        for action in parser._actions
        if isinstance(action, argparse._SubParsersAction)
    )
    memory_loop_parser = command_action.choices["memory-loop"]
    memory_loop_action = next(
        action
        for action in memory_loop_parser._actions
        if isinstance(action, argparse._SubParsersAction)
    )
    return set(memory_loop_action.choices)


def test_static_command_declaration_exists() -> None:
    assert (
        MEMORY_LOOP_COMMAND
        == "p4-m6-14-entry-definition-corridor-final-closure-handoff-next-corridor-non-start-index"
    )
    assert MEMORY_LOOP_COMMAND_INVOCATION == f"memory-loop {MEMORY_LOOP_COMMAND}"
    assert (
        P4_M6_14_ENTRY_DEFINITION_CORRIDOR_FINAL_CLOSURE_HANDOFF_NEXT_CORRIDOR_NON_START_INDEX_BOUNDARY[
            "command"
        ]
        == MEMORY_LOOP_COMMAND_INVOCATION
    )


def test_actual_operator_parser_exposes_the_command() -> None:
    commands = _memory_loop_subcommands(build_parser())
    assert MEMORY_LOOP_COMMAND in commands
    assert "p4-m6-13-entry-definition-corridor-closure-review" in commands


def test_markdown_dispatch_works_and_is_default_format(tmp_path: Path) -> None:
    code, payload, stderr, stdout = _run_operator(
        ["memory-loop", MEMORY_LOOP_COMMAND, "--workspace-root", str(tmp_path)]
    )
    assert code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith(
        "# P4-M6.14 Entry Definition Corridor Final Closure Handoff / Next Corridor Non-Start Index\n"
    )
    assert "static declared index rows only" in stdout
    assert "no repeated closure review" in stdout
    assert not (tmp_path / ".local" / "subspace_memory").exists()


def test_json_dispatch_works(tmp_path: Path) -> None:
    code, output, stderr, stdout = _run_operator(
        [
            "memory-loop",
            MEMORY_LOOP_COMMAND,
            "--workspace-root",
            str(tmp_path),
            "--format",
            "json",
        ]
    )
    assert code == 0
    assert stderr == ""
    assert stdout.startswith("{")
    assert output["count"] == 23
    assert output["true_flags"] == 202
    assert output["false_flags"] == 447
    status = output["status"]
    assert status["stage"] == "P4-M6.14"
    assert status["surface"] == (
        "Entry Definition Corridor Final Closure Handoff / Next Corridor Non-Start Index"
    )
    assert status["mode"] == "read-only declaration-only definition-only inspection-only"
    assert len(status["status_shape"]) == 23
    assert set(status["status_shape"]) == set(FIELD_IDS)
    assert tuple(field["field_id"] for field in output["fields"]) == FIELD_IDS
    assert not (tmp_path / ".local" / "subspace_memory").exists()


def test_workspace_root_is_accepted_but_not_used_for_store_creation(
    monkeypatch, tmp_path: Path
) -> None:
    def fail_store_creation(*_args, **_kwargs):
        raise AssertionError("workspace store must not be created")

    monkeypatch.setattr(operator, "create_workspace_subspace_memory_store", fail_store_creation)
    code, payload, stderr, stdout = _run_operator(
        [
            "memory-loop",
            MEMORY_LOOP_COMMAND,
            "--workspace-root",
            str(tmp_path),
            "--format",
            "markdown",
        ]
    )
    assert code == 0
    assert payload == {}
    assert stderr == ""
    assert "read-only" in stdout
    assert not (tmp_path / ".local" / "subspace_memory").exists()


def test_renderer_does_not_scan_workspace_or_repository(tmp_path: Path) -> None:
    workspace = tmp_path / "fresh-workspace"
    workspace.mkdir()
    sentinel = workspace / "sentinel.txt"
    sentinel.write_text("must not be inspected", encoding="utf-8")
    markdown = run_p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_command(
        workspace_root=workspace
    )
    parsed = json.loads(
        run_p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_command(
            output_format="json",
            workspace_root=workspace,
        )
    )
    assert "must not be inspected" not in markdown
    assert "must not be inspected" not in json.dumps(parsed)
    assert parsed["command"] == MEMORY_LOOP_COMMAND_INVOCATION
    assert not (workspace / ".local" / "subspace_memory").exists()


def test_status_shape_contains_exactly_23_required_semantic_field_ids() -> None:
    fields = list_p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_fields()
    assert len(fields) == 23
    assert (
        p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_field_ids()
        == FIELD_IDS
    )
    assert (
        tuple(
            p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_status_shape()
        )
        == FIELD_IDS
    )
    assert all(
        isinstance(
            field,
            P4M614EntryDefinitionCorridorFinalClosureHandoffNextCorridorNonStartIndexField,
        )
        for field in fields
    )
    assert set(dataclasses.asdict(fields[0])) == {
        "field_order",
        "field_id",
        "field_name",
        "field_purpose",
        "p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_category",
        "p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_semantics_disabled",
    }


def test_direct_prior_reference_is_p4_m6_13() -> None:
    report = p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_report()
    assert report["direct_prior_reference"] == "P4-M6.13 Entry Definition Corridor Closure Review"
    assert (
        report["status_shape"]["p4_m6_14_direct_prior_reference"]
        == "P4-M6.13 Entry Definition Corridor Closure Review"
    )


def test_p4_m6_0_through_p4_m6_13_lineage_is_preserved() -> None:
    report = p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_report()
    assert P4_M6_CORRIDOR_REFERENCE_CHAIN == P4_M6_CHAIN
    assert report["p4_m6_corridor_reference_chain"] == P4_M6_CHAIN
    assert report["prior_reference_chain"][:14] == P4_M6_CHAIN


def test_pre_corridor_p4_m5_0_through_p4_m5_6_lineage_is_preserved() -> None:
    report = p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_report()
    assert P4_M5_PRE_CORRIDOR_REFERENCE_CHAIN == P4_M5_CHAIN
    assert PRIOR_DEFINITION_LAYER_REFERENCE_CHAIN == (*P4_M6_CHAIN, *P4_M5_CHAIN)
    assert report["p4_m5_pre_corridor_reference_chain"] == P4_M5_CHAIN
    assert report["prior_reference_chain"][14:] == P4_M5_CHAIN


def test_p4_m6_corridor_closed_is_declaration_only() -> None:
    report = p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_report()
    shape = report["status_shape"]
    assert "P4-M6 corridor closed" in shape["p4_m6_14_closed_corridor_scope"]
    assert "handoff declaration only" in shape["p4_m6_14_final_closure_handoff_index"]
    assert "corridor-closed-declaration-index-only" in shape["p4_m6_14_corridor_closed_declaration_index"]


def test_p4_m6_13_closure_review_is_referenced_but_not_repeated() -> None:
    rendered = render_p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_markdown()
    assert "P4-M6.13 closure review remains the direct prior reference" in rendered
    assert "no repeated closure review" in rendered
    assert "Entry Definition Corridor Closure Review" in rendered


def test_all_required_boundary_phrases_are_present() -> None:
    phrase_text = "\n".join(BOUNDARY_PHRASE_LINES)
    rendered = render_p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_markdown()
    docs = Path(
        "docs/CIVILIZATION_CORE_P4_M6_14_ENTRY_DEFINITION_CORRIDOR_FINAL_CLOSURE_HANDOFF_NEXT_CORRIDOR_NON_START_INDEX.md"
    ).read_text(encoding="utf-8")
    source = Path(
        "src/hermes_memory_fabric/p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index.py"
    ).read_text(encoding="utf-8")
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in phrase_text
        assert phrase in rendered
        assert phrase in docs
        assert phrase in source
    for direction in STATUS_DIRECTION:
        assert direction in rendered


def test_true_flags_count_is_202_and_stage_delta_is_9() -> None:
    report = p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_report()
    assert len(P4_M6_13_TRUE_STATUS_FLAGS) == 193
    assert len(P4_M6_14_TRUE_STATUS_FLAGS) == 9
    assert len(TRUE_STATUS_FLAGS) == 202
    assert report["true_flags"] == 202


def test_false_flags_count_is_447_and_stage_delta_is_29() -> None:
    report = p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_report()
    assert len(P4_M6_13_FALSE_STATUS_FLAGS) == 418
    assert len(P4_M6_14_FALSE_STATUS_FLAGS) == 29
    assert len(FALSE_STATUS_FLAGS) == 447
    assert report["false_flags"] == 447


def test_strict_cumulative_true_boolean_key_set_is_stable() -> None:
    report = p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_report()
    actual_true_keys = {
        key for key, value in report["status_booleans"].items() if value is True
    }
    assert actual_true_keys == set(TRUE_STATUS_FLAGS)
    assert set(P4_M6_14_TRUE_STATUS_FLAGS).issubset(actual_true_keys)


def test_strict_cumulative_false_boolean_key_set_is_stable() -> None:
    report = p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_report()
    actual_false_keys = {
        key for key, value in report["status_booleans"].items() if value is False
    }
    assert actual_false_keys == set(FALSE_STATUS_FLAGS)
    assert set(P4_M6_14_FALSE_STATUS_FLAGS).issubset(actual_false_keys)


def test_no_validation_verdict_readiness_approval_authorization_or_confirmation_behavior_exists() -> None:
    booleans = p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_report()["status_booleans"]
    for key in (
        "p4_m6_14_live_validation_enabled",
        "p4_m6_14_inference_enabled",
        "p4_m6_14_scoring_enabled",
        "p4_m6_14_verdict_enabled",
        "p4_m6_14_readiness_determination_enabled",
        "p4_m6_14_approval_enabled",
        "p4_m6_14_authorization_enabled",
        "p4_m6_14_confirmation_enabled",
        "p4_m6_14_acceptance_enabled",
        "p4_m6_14_rejection_enabled",
        "p4_m6_14_deferral_enabled",
        "p4_m6_14_escalation_enabled",
        "p4_m6_14_override_enabled",
        "p4_m6_14_resolution_enabled",
    ):
        assert booleans[key] is False


def test_no_routing_execution_storage_persistence_or_mutation_behavior_exists() -> None:
    booleans = p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_report()["status_booleans"]
    for key in (
        "p4_m6_14_routing_enabled",
        "p4_m6_14_execution_enabled",
        "p4_m6_14_record_creation_enabled",
        "p4_m6_14_storage_enabled",
        "p4_m6_14_persistence_enabled",
        "p4_m6_14_mutation_enabled",
        "p4_m6_14_safeguard_activation_enabled",
        "p4_m6_14_safeguard_enforcement_enabled",
        "p4_m6_14_prioritization_enabled",
        "p4_m6_14_selection_enabled",
        "p4_m6_14_recommendation_enabled",
        "p4_m6_14_entry_blocking_enabled",
        "p4_m6_14_entry_unblocking_enabled",
    ):
        assert booleans[key] is False


def test_no_next_corridor_p4_m7_or_v7_start_behavior_exists() -> None:
    report = p4_m6_14_entry_definition_corridor_final_closure_handoff_next_corridor_non_start_index_report()
    booleans = report["status_booleans"]
    assert booleans["p4_m6_14_next_corridor_start_enabled"] is False
    assert booleans["p4_m6_14_v7_start_enabled"] is False
    guard = report["status_shape"]["p4_m6_14_next_corridor_and_v7_non_start_operator_guard"]
    assert "no next corridor start" in guard
    assert "no P4-M7.0 start" in guard
    assert "no v7" in guard


def test_docs_match_the_declared_index_surface() -> None:
    docs = Path(
        "docs/CIVILIZATION_CORE_P4_M6_14_ENTRY_DEFINITION_CORRIDOR_FINAL_CLOSURE_HANDOFF_NEXT_CORRIDOR_NON_START_INDEX.md"
    ).read_text(encoding="utf-8")
    assert "# P4-M6.14 Entry Definition Corridor Final Closure Handoff / Next Corridor Non-Start Index" in docs
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in docs
    for field_id in FIELD_IDS:
        assert field_id in docs
    assert "true_flags=202" in docs
    assert "false_flags=447" in docs


def test_operator_surface_remains_pre_store_and_read_only(monkeypatch, tmp_path: Path) -> None:
    created_store = False

    def fail_store_creation(*_args, **_kwargs):
        nonlocal created_store
        created_store = True
        raise AssertionError("workspace store must not be created")

    monkeypatch.setattr(operator, "create_workspace_subspace_memory_store", fail_store_creation)
    code, output, stderr, _stdout = _run_operator(
        [
            "memory-loop",
            MEMORY_LOOP_COMMAND,
            "--workspace-root",
            str(tmp_path),
            "--format",
            "json",
        ]
    )
    assert code == 0
    assert stderr == ""
    assert created_store is False
    assert output["status"]["mode"] == "read-only declaration-only definition-only inspection-only"
    assert not (tmp_path / ".local" / "subspace_memory").exists()
