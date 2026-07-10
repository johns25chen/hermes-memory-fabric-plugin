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
from hermes_memory_fabric.p4_m6_12_entry_safeguard_non_activation_surface import (
    FALSE_STATUS_FLAGS as P4_M6_12_FALSE_STATUS_FLAGS,
    TRUE_STATUS_FLAGS as P4_M6_12_TRUE_STATUS_FLAGS,
)
from hermes_memory_fabric.p4_m6_13_entry_definition_corridor_closure_review import (
    BOUNDARY_PHRASE_LINES,
    FALSE_STATUS_FLAGS,
    MEMORY_LOOP_COMMAND,
    MEMORY_LOOP_COMMAND_INVOCATION,
    P4_M5_PRE_CORRIDOR_REFERENCE_CHAIN,
    P4_M6_13_ENTRY_DEFINITION_CORRIDOR_CLOSURE_REVIEW_BOUNDARY,
    P4_M6_13_FALSE_STATUS_FLAGS,
    P4_M6_13_TRUE_STATUS_FLAGS,
    P4_M6_CORRIDOR_REFERENCE_CHAIN,
    PRIOR_DEFINITION_LAYER_REFERENCE_CHAIN,
    STATUS_DIRECTION,
    TRUE_STATUS_FLAGS,
    P4M613EntryDefinitionCorridorClosureReviewField,
    list_p4_m6_13_entry_definition_corridor_closure_review_fields,
    p4_m6_13_entry_definition_corridor_closure_review_field_ids,
    p4_m6_13_entry_definition_corridor_closure_review_report,
    p4_m6_13_entry_definition_corridor_closure_review_status_shape,
    render_p4_m6_13_entry_definition_corridor_closure_review_markdown,
    run_p4_m6_13_entry_definition_corridor_closure_review_command,
)


FIELD_IDS = tuple(
    line
    for line in """
p4_m6_13_stage
p4_m6_13_surface_id
p4_m6_13_direct_prior_reference
p4_m6_13_prior_reference_chain
p4_m6_13_corridor_scope
p4_m6_13_entry_definition_inventory_review_surface
p4_m6_13_lineage_alignment_review_surface
p4_m6_13_operator_alignment_review_surface
p4_m6_13_documentation_alignment_review_surface
p4_m6_13_status_shape_alignment_review_surface
p4_m6_13_closure_non_verdict_surface
p4_m6_13_closure_non_approval_surface
p4_m6_13_closure_non_authorization_surface
p4_m6_13_closure_non_confirmation_surface
p4_m6_13_entry_non_validation_surface
p4_m6_13_readiness_non_determination_surface
p4_m6_13_routing_non_execution_surface
p4_m6_13_record_non_creation_surface
p4_m6_13_storage_non_persistence_surface
p4_m6_13_mutation_absence_surface
p4_m6_13_next_corridor_non_start_surface
p4_m6_13_v7_non_start_surface
p4_m6_13_operator_surface_guard
""".splitlines()
    if line
)

REQUIRED_BOUNDARY_PHRASES = tuple(
    line
    for line in """
Entry Definition Corridor Closure Review
static entry definition corridor closure review surface
corridor-closure-review-surface-only
entry-definition-inventory-review-surface-only
lineage-alignment-review-surface-only
operator-alignment-review-surface-only
documentation-alignment-review-surface-only
status-shape-alignment-review-surface-only
closure-non-verdict-surface-only
next-corridor-non-start-surface-only
operator-guard-surface-only
definition-only
declaration-only
read-only
inspection-only
static declared review rows only
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
    assert MEMORY_LOOP_COMMAND == "p4-m6-13-entry-definition-corridor-closure-review"
    assert (
        MEMORY_LOOP_COMMAND_INVOCATION
        == "memory-loop p4-m6-13-entry-definition-corridor-closure-review"
    )
    assert (
        P4_M6_13_ENTRY_DEFINITION_CORRIDOR_CLOSURE_REVIEW_BOUNDARY["command"]
        == MEMORY_LOOP_COMMAND_INVOCATION
    )


def test_actual_operator_parser_exposes_the_command() -> None:
    commands = _memory_loop_subcommands(build_parser())

    assert "p4-m6-13-entry-definition-corridor-closure-review" in commands
    assert "p4-m6-12-entry-safeguard-non-activation-surface" in commands


def test_markdown_dispatch_works_and_is_default_format(tmp_path: Path) -> None:
    code, payload, stderr, stdout = _run_operator(
        [
            "memory-loop",
            "p4-m6-13-entry-definition-corridor-closure-review",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    assert code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith("# P4-M6.13 Entry Definition Corridor Closure Review\n")
    assert "static entry definition corridor closure review surface" in stdout
    assert "static declared review rows only" in stdout
    assert not (tmp_path / ".local" / "subspace_memory").exists()


def test_json_dispatch_works(tmp_path: Path) -> None:
    code, output, stderr, stdout = _run_operator(
        [
            "memory-loop",
            "p4-m6-13-entry-definition-corridor-closure-review",
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
    assert output["true_flags"] == 193
    assert output["false_flags"] == 418
    assert (
        output["boundary"]["command"]
        == P4_M6_13_ENTRY_DEFINITION_CORRIDOR_CLOSURE_REVIEW_BOUNDARY["command"]
    )
    assert tuple(field["field_id"] for field in output["fields"]) == FIELD_IDS
    status = output["status"]
    assert status["command"] == MEMORY_LOOP_COMMAND_INVOCATION
    assert status["stage"] == "P4-M6.13"
    assert status["surface"] == "Entry Definition Corridor Closure Review"
    assert status["mode"] == "read-only declaration-only definition-only inspection-only"
    assert set(status["status_shape"]) == set(FIELD_IDS)
    assert len(status["status_shape"]) == 23
    assert status["true_flags"] == 193
    assert status["false_flags"] == 418
    assert not (tmp_path / ".local" / "subspace_memory").exists()


def test_workspace_root_is_accepted_but_not_used_for_store_creation(
    monkeypatch, tmp_path: Path
) -> None:
    def fail_store_creation(*_args, **_kwargs):
        raise AssertionError("workspace store must not be created")

    monkeypatch.setattr(
        operator,
        "create_workspace_subspace_memory_store",
        fail_store_creation,
    )

    code, payload, stderr, stdout = _run_operator(
        [
            "memory-loop",
            "p4-m6-13-entry-definition-corridor-closure-review",
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

    markdown = run_p4_m6_13_entry_definition_corridor_closure_review_command(
        workspace_root=workspace
    )
    parsed = json.loads(
        run_p4_m6_13_entry_definition_corridor_closure_review_command(
            output_format="json",
            workspace_root=workspace,
        )
    )

    assert "must not be inspected" not in markdown
    assert "must not be inspected" not in json.dumps(parsed)
    assert parsed["command"] == MEMORY_LOOP_COMMAND_INVOCATION
    assert not (workspace / ".local" / "subspace_memory").exists()


def test_status_shape_contains_exactly_23_required_semantic_field_ids() -> None:
    fields = list_p4_m6_13_entry_definition_corridor_closure_review_fields()
    assert len(fields) == 23
    assert p4_m6_13_entry_definition_corridor_closure_review_field_ids() == FIELD_IDS
    assert tuple(p4_m6_13_entry_definition_corridor_closure_review_status_shape()) == FIELD_IDS
    assert all(
        isinstance(field, P4M613EntryDefinitionCorridorClosureReviewField)
        for field in fields
    )
    assert set(dataclasses.asdict(fields[0])) == {
        "field_order",
        "field_id",
        "field_name",
        "field_purpose",
        "p4_m6_13_entry_definition_corridor_closure_review_category",
        "p4_m6_13_entry_definition_corridor_closure_review_semantics_disabled",
    }


def test_direct_prior_reference_is_p4_m6_12() -> None:
    report = p4_m6_13_entry_definition_corridor_closure_review_report()
    assert (
        report["direct_prior_reference"]
        == "P4-M6.12 Entry Safeguard Non-Activation Surface"
    )
    assert (
        report["status_shape"]["p4_m6_13_direct_prior_reference"]
        == "P4-M6.12 Entry Safeguard Non-Activation Surface"
    )


def test_p4_m6_0_through_p4_m6_12_lineage_is_preserved() -> None:
    assert P4_M6_CORRIDOR_REFERENCE_CHAIN == P4_M6_CHAIN
    report = p4_m6_13_entry_definition_corridor_closure_review_report()
    assert report["p4_m6_corridor_reference_chain"] == P4_M6_CHAIN
    assert report["prior_reference_chain"][:13] == P4_M6_CHAIN


def test_pre_corridor_p4_m5_0_through_p4_m5_6_lineage_is_preserved() -> None:
    assert P4_M5_PRE_CORRIDOR_REFERENCE_CHAIN == P4_M5_CHAIN
    assert PRIOR_DEFINITION_LAYER_REFERENCE_CHAIN == (*P4_M6_CHAIN, *P4_M5_CHAIN)
    report = p4_m6_13_entry_definition_corridor_closure_review_report()
    assert report["p4_m5_pre_corridor_reference_chain"] == P4_M5_CHAIN
    assert report["prior_reference_chain"][13:] == P4_M5_CHAIN


def test_all_required_boundary_phrases_are_present() -> None:
    phrase_text = "\n".join(BOUNDARY_PHRASE_LINES)
    rendered = render_p4_m6_13_entry_definition_corridor_closure_review_markdown()
    docs = Path(
        "docs/CIVILIZATION_CORE_P4_M6_13_ENTRY_DEFINITION_CORRIDOR_CLOSURE_REVIEW.md"
    ).read_text(encoding="utf-8")
    source = Path(
        "src/hermes_memory_fabric/p4_m6_13_entry_definition_corridor_closure_review.py"
    ).read_text(encoding="utf-8")

    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in phrase_text
        assert phrase in rendered
        assert phrase in docs
        assert phrase in source
    for direction in STATUS_DIRECTION:
        assert direction in rendered


def test_true_flags_count_is_193_and_stage_delta_is_9() -> None:
    report = p4_m6_13_entry_definition_corridor_closure_review_report()
    assert len(P4_M6_12_TRUE_STATUS_FLAGS) == 184
    assert len(P4_M6_13_TRUE_STATUS_FLAGS) == 9
    assert len(TRUE_STATUS_FLAGS) == 193
    assert report["true_flags"] == 193


def test_false_flags_count_is_418_and_stage_delta_is_29() -> None:
    report = p4_m6_13_entry_definition_corridor_closure_review_report()
    assert len(P4_M6_12_FALSE_STATUS_FLAGS) == 389
    assert len(P4_M6_13_FALSE_STATUS_FLAGS) == 29
    assert len(FALSE_STATUS_FLAGS) == 418
    assert report["false_flags"] == 418


def test_strict_cumulative_true_boolean_key_set_is_stable() -> None:
    report = p4_m6_13_entry_definition_corridor_closure_review_report()
    actual_true_keys = {
        key for key, value in report["status_booleans"].items() if value is True
    }
    assert actual_true_keys == set(TRUE_STATUS_FLAGS)
    assert set(P4_M6_13_TRUE_STATUS_FLAGS).issubset(actual_true_keys)


def test_strict_cumulative_false_boolean_key_set_is_stable() -> None:
    report = p4_m6_13_entry_definition_corridor_closure_review_report()
    actual_false_keys = {
        key for key, value in report["status_booleans"].items() if value is False
    }
    assert actual_false_keys == set(FALSE_STATUS_FLAGS)
    assert set(P4_M6_13_FALSE_STATUS_FLAGS).issubset(actual_false_keys)


def test_no_validation_verdict_or_readiness_behavior_exists() -> None:
    booleans = p4_m6_13_entry_definition_corridor_closure_review_report()[
        "status_booleans"
    ]
    for key in (
        "p4_m6_13_live_validation_enabled",
        "p4_m6_13_inference_enabled",
        "p4_m6_13_scoring_enabled",
        "p4_m6_13_verdict_enabled",
        "p4_m6_13_readiness_determination_enabled",
        "p4_m6_13_approval_enabled",
        "p4_m6_13_authorization_enabled",
        "p4_m6_13_confirmation_enabled",
        "p4_m6_13_acceptance_enabled",
        "p4_m6_13_rejection_enabled",
        "p4_m6_13_deferral_enabled",
        "p4_m6_13_escalation_enabled",
        "p4_m6_13_override_enabled",
        "p4_m6_13_resolution_enabled",
    ):
        assert booleans[key] is False


def test_no_routing_execution_storage_or_mutation_behavior_exists() -> None:
    booleans = p4_m6_13_entry_definition_corridor_closure_review_report()[
        "status_booleans"
    ]
    for key in (
        "p4_m6_13_routing_enabled",
        "p4_m6_13_execution_enabled",
        "p4_m6_13_record_creation_enabled",
        "p4_m6_13_storage_enabled",
        "p4_m6_13_persistence_enabled",
        "p4_m6_13_mutation_enabled",
        "p4_m6_13_safeguard_activation_enabled",
        "p4_m6_13_safeguard_enforcement_enabled",
        "p4_m6_13_prioritization_enabled",
        "p4_m6_13_selection_enabled",
        "p4_m6_13_recommendation_enabled",
        "p4_m6_13_entry_blocking_enabled",
        "p4_m6_13_entry_unblocking_enabled",
    ):
        assert booleans[key] is False


def test_no_next_corridor_or_v7_start_behavior_exists() -> None:
    booleans = p4_m6_13_entry_definition_corridor_closure_review_report()[
        "status_booleans"
    ]
    assert booleans["p4_m6_13_next_corridor_start_enabled"] is False
    assert booleans["p4_m6_13_v7_start_enabled"] is False


def test_docs_match_the_declared_surface() -> None:
    docs = Path(
        "docs/CIVILIZATION_CORE_P4_M6_13_ENTRY_DEFINITION_CORRIDOR_CLOSURE_REVIEW.md"
    ).read_text(encoding="utf-8")
    assert "# P4-M6.13 Entry Definition Corridor Closure Review" in docs
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in docs
    for field_id in FIELD_IDS:
        assert field_id in docs
    assert "true_flags=193" in docs
    assert "false_flags=418" in docs


def test_operator_surface_remains_pre_store_and_read_only(
    monkeypatch, tmp_path: Path
) -> None:
    created_store = False

    def fail_store_creation(*_args, **_kwargs):
        nonlocal created_store
        created_store = True
        raise AssertionError("workspace store must not be created")

    monkeypatch.setattr(
        operator,
        "create_workspace_subspace_memory_store",
        fail_store_creation,
    )

    code, output, stderr, _stdout = _run_operator(
        [
            "memory-loop",
            "p4-m6-13-entry-definition-corridor-closure-review",
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
