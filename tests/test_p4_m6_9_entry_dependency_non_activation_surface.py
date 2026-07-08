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
from hermes_memory_fabric.p4_m6_9_entry_dependency_non_activation_surface import (
    BOUNDARY_PHRASE_LINES,
    FALSE_STATUS_FLAGS,
    MEMORY_LOOP_COMMAND,
    MEMORY_LOOP_COMMAND_INVOCATION,
    P4_M6_9_ENTRY_DEPENDENCY_NON_ACTIVATION_SURFACE_BOUNDARY,
    PRIOR_DEFINITION_LAYER_REFERENCE_CHAIN,
    STATUS_DIRECTION,
    TRUE_STATUS_FLAGS,
    P4M69EntryDependencyNonActivationSurfaceField,
    list_p4_m6_9_entry_dependency_non_activation_surface_fields,
    p4_m6_9_entry_dependency_non_activation_surface_field_ids,
    p4_m6_9_entry_dependency_non_activation_surface_report,
    p4_m6_9_entry_dependency_non_activation_surface_status_shape,
    render_p4_m6_9_entry_dependency_non_activation_surface_markdown,
    run_p4_m6_9_entry_dependency_non_activation_surface_command,
)


FIELD_IDS = tuple(
    line
    for line in """
p4_m6_9_stage
p4_m6_9_surface_id
p4_m6_9_direct_prior_reference
p4_m6_9_prior_reference_chain
p4_m6_9_entry_dependency_label_surface
p4_m6_9_dependency_non_activation_surface
p4_m6_9_dependency_non_resolution_surface
p4_m6_9_dependency_non_traversal_surface
p4_m6_9_dependency_non_expansion_surface
p4_m6_9_dependency_non_requirement_generation_surface
p4_m6_9_dependency_non_ordering_surface
p4_m6_9_dependency_non_ranking_surface
p4_m6_9_dependency_non_selection_surface
p4_m6_9_dependency_non_blocking_surface
p4_m6_9_dependency_non_routing_surface
p4_m6_9_dependency_non_execution_surface
p4_m6_9_readiness_non_evidence_surface
p4_m6_9_validation_non_input_surface
p4_m6_9_record_non_creation_surface
p4_m6_9_storage_non_persistence_surface
p4_m6_9_mutation_absence_surface
p4_m6_9_implementation_corridor_non_start_surface
p4_m6_9_operator_surface_guard
""".splitlines()
    if line
)

REQUIRED_BOUNDARY_PHRASES = tuple(
    line
    for line in """
Entry Dependency Non-Activation Surface
static entry dependency label surface
dependency-non-activation-surface-only
dependency-non-resolution-surface-only
dependency-non-traversal-surface-only
dependency-non-expansion-surface-only
dependency-non-requirement-generation-surface-only
dependency-non-ordering-surface-only
dependency-non-selection-surface-only
dependency-non-routing-surface-only
dependency-non-execution-surface-only
definition-only
declaration-only
read-only
inspection-only
no dependency activation
no dependency resolution
no dependency graph traversal
no dependency chain expansion
no dependency requirement inference
no dependency requirement generation
no dependency ordering
no dependency ranking
no dependency selection
no required dependency choice
no dependency blocking
no dependency unblocking
no dependency routing
no dependency execution
no readiness evidence
no validation input
no record creation
no storage
no persistence
no mutation
no implementation corridor start
no API
no MCP
no Connector
no Agent
no network
no OAuth
no credential
no secret inspection
no v7
no productization
no UI
no Operator Console
""".splitlines()
    if line
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


def test_command_exists_as_static_memory_loop_declaration() -> None:
    assert MEMORY_LOOP_COMMAND == "p4-m6-9-entry-dependency-non-activation-surface"
    assert (
        MEMORY_LOOP_COMMAND_INVOCATION
        == "memory-loop p4-m6-9-entry-dependency-non-activation-surface"
    )
    assert (
        P4_M6_9_ENTRY_DEPENDENCY_NON_ACTIVATION_SURFACE_BOUNDARY["command"]
        == MEMORY_LOOP_COMMAND_INVOCATION
    )


def test_status_shape_includes_23_required_semantic_field_ids() -> None:
    fields = list_p4_m6_9_entry_dependency_non_activation_surface_fields()
    assert len(fields) == 23
    assert p4_m6_9_entry_dependency_non_activation_surface_field_ids() == FIELD_IDS
    assert tuple(p4_m6_9_entry_dependency_non_activation_surface_status_shape()) == FIELD_IDS
    assert all(isinstance(field, P4M69EntryDependencyNonActivationSurfaceField) for field in fields)
    assert set(dataclasses.asdict(fields[0])) == {
        "field_order",
        "field_id",
        "field_name",
        "field_purpose",
        "p4_m6_9_entry_dependency_non_activation_surface_category",
        "p4_m6_9_entry_dependency_non_activation_surface_semantics_disabled",
    }


def test_direct_prior_reference_points_to_p4_m6_8() -> None:
    report = p4_m6_9_entry_dependency_non_activation_surface_report()
    assert (
        report["direct_prior_reference"]
        == "P4-M6.8 Entry Ambiguity Non-Inference Surface"
    )
    assert (
        report["status_shape"]["p4_m6_9_direct_prior_reference"]
        == "P4-M6.8 Entry Ambiguity Non-Inference Surface"
    )


def test_prior_reference_chain_is_preserved() -> None:
    assert PRIOR_DEFINITION_LAYER_REFERENCE_CHAIN == (
        "P4-M6.8 Entry Ambiguity Non-Inference Surface",
        "P4-M6.7 Entry Conflict Non-Resolution Surface",
        "P4-M6.6 Entry Exception Non-Override Surface",
        "P4-M6.5 Entry Escalation Non-Routing Surface",
        "P4-M6.4 Entry Rejection Non-Execution Surface",
        "P4-M6.3 Entry Deferral Non-Execution Surface",
        "P4-M6.2 Entry Acceptance Non-Evidence Surface",
        "P4-M6.1 Entry Preconditions Definition Surface",
        "P4-M6.0 Next Corridor Entry Boundary Contract",
        "P4-M5.6 Final Closure Handoff / Next Corridor Non-Start Index",
        "P4-M5.5 Readiness Audit Closure / Non-Start Boundary Seal",
        "P4-M5.4 API / MCP / Connector Cross-Surface Alignment Map",
        "P4-M5.3 Connector Readiness Audit Surface Map",
        "P4-M5.2 MCP Readiness Audit Surface Map",
        "P4-M5.1 API Readiness Audit Surface Map",
        "P4-M5.0 API / MCP / Connector Readiness Audit Boundary Contract",
    )
    assert (
        p4_m6_9_entry_dependency_non_activation_surface_status_shape()[
            "p4_m6_9_prior_reference_chain"
        ]
        == PRIOR_DEFINITION_LAYER_REFERENCE_CHAIN
    )


def test_required_boundary_phrases_are_present() -> None:
    phrase_text = "\n".join(BOUNDARY_PHRASE_LINES)
    rendered = render_p4_m6_9_entry_dependency_non_activation_surface_markdown()
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in phrase_text
        assert phrase in rendered
    for direction in STATUS_DIRECTION:
        assert direction in rendered


def test_true_flags_count_is_157() -> None:
    report = p4_m6_9_entry_dependency_non_activation_surface_report()
    assert len(TRUE_STATUS_FLAGS) == 157
    assert report["true_flags"] == 157


def test_false_flags_count_is_302() -> None:
    report = p4_m6_9_entry_dependency_non_activation_surface_report()
    assert len(FALSE_STATUS_FLAGS) == 302
    assert report["false_flags"] == 302


def test_strict_boolean_key_set_is_stable() -> None:
    report = p4_m6_9_entry_dependency_non_activation_surface_report()
    expected = set(TRUE_STATUS_FLAGS) | set(FALSE_STATUS_FLAGS)
    assert set(report["status_booleans"]) == expected
    assert all(report["status_booleans"][key] is True for key in TRUE_STATUS_FLAGS)
    assert all(report["status_booleans"][key] is False for key in FALSE_STATUS_FLAGS)


def test_command_renderer_is_read_only() -> None:
    markdown = run_p4_m6_9_entry_dependency_non_activation_surface_command()
    parsed = json.loads(
        run_p4_m6_9_entry_dependency_non_activation_surface_command(output_format="json")
    )
    assert "Entry Dependency Non-Activation Surface" in markdown
    assert parsed["command"] == MEMORY_LOOP_COMMAND_INVOCATION
    assert parsed["mode"] == "read-only declaration-only definition-only inspection-only"
    assert parsed["true_flags"] == 157
    assert parsed["false_flags"] == 302


def test_command_renderer_does_not_create_subspace_memory_in_fresh_temp_workspace(
    tmp_path: Path,
) -> None:
    workspace = tmp_path / "fresh-workspace"
    workspace.mkdir()
    output = run_p4_m6_9_entry_dependency_non_activation_surface_command(
        workspace_root=workspace
    )
    assert "read-only" in output
    assert not (workspace / ".local" / "subspace_memory").exists()


def test_operator_markdown_command_is_read_only_and_pre_store(
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
            "p4-m6-9-entry-dependency-non-activation-surface",
            "--workspace-root",
            str(tmp_path),
        ]
    )

    assert code == 0
    assert payload == {}
    assert stderr == ""
    assert stdout.startswith("# P4-M6.9 Entry Dependency Non-Activation Surface\n")
    for phrase in (
        "Entry Dependency Non-Activation Surface",
        "static entry dependency label surface",
        "dependency-non-activation-surface-only",
        "dependency-non-resolution-surface-only",
        "no dependency activation",
        "no dependency routing",
        "no dependency execution",
        "no storage",
        "no mutation",
    ):
        assert phrase in stdout
    assert not (tmp_path / ".local" / "subspace_memory").exists()


def test_operator_json_command_returns_required_report(tmp_path: Path) -> None:
    code, output, stderr, stdout = _run_operator(
        [
            "memory-loop",
            "p4-m6-9-entry-dependency-non-activation-surface",
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
    assert output["true_flags"] == 157
    assert output["false_flags"] == 302
    assert (
        output["boundary"]["command"]
        == P4_M6_9_ENTRY_DEPENDENCY_NON_ACTIVATION_SURFACE_BOUNDARY["command"]
    )
    assert tuple(field["field_id"] for field in output["fields"]) == FIELD_IDS
    status = output["status"]
    assert status["command"] == MEMORY_LOOP_COMMAND_INVOCATION
    assert status["stage"] == "P4-M6.9"
    assert status["surface"] == "Entry Dependency Non-Activation Surface"
    assert status["mode"] == "read-only declaration-only definition-only inspection-only"
    assert set(status["status_shape"]) == set(FIELD_IDS)
    assert len(status["status_shape"]) == 23
    assert status["true_flags"] == 157
    assert status["false_flags"] == 302
    actual_true_keys = {
        key for key, value in status["status_booleans"].items() if value is True
    }
    actual_false_keys = {
        key for key, value in status["status_booleans"].items() if value is False
    }
    assert actual_true_keys == set(TRUE_STATUS_FLAGS)
    assert actual_false_keys == set(FALSE_STATUS_FLAGS)
    assert not (tmp_path / ".local" / "subspace_memory").exists()


def test_parser_exposes_p4_m6_9_memory_loop_command() -> None:
    commands = _memory_loop_subcommands(build_parser())

    assert "p4-m6-9-entry-dependency-non-activation-surface" in commands
    assert "p4-m6-8-entry-ambiguity-non-inference-surface" in commands


def test_no_routing_execution_storage_or_mutation_behavior_exists() -> None:
    booleans = p4_m6_9_entry_dependency_non_activation_surface_report()[
        "status_booleans"
    ]
    for key in (
        "p4_m6_9_dependency_activation_enabled",
        "p4_m6_9_dependency_resolution_enabled",
        "p4_m6_9_dependency_graph_traversal_enabled",
        "p4_m6_9_dependency_chain_expansion_enabled",
        "p4_m6_9_dependency_requirement_inference_enabled",
        "p4_m6_9_dependency_requirement_generation_enabled",
        "p4_m6_9_dependency_ordering_enabled",
        "p4_m6_9_dependency_ranking_enabled",
        "p4_m6_9_dependency_selection_enabled",
        "p4_m6_9_required_dependency_choice_enabled",
        "p4_m6_9_dependency_blocking_enabled",
        "p4_m6_9_dependency_unblocking_enabled",
        "p4_m6_9_dependency_routing_enabled",
        "p4_m6_9_dependency_execution_enabled",
        "p4_m6_9_storage_enabled",
        "p4_m6_9_persistence_enabled",
        "p4_m6_9_mutation_enabled",
        "p4_m6_9_api_call_enabled",
        "p4_m6_9_mcp_call_enabled",
        "p4_m6_9_connector_call_enabled",
        "p4_m6_9_agent_call_enabled",
        "p4_m6_9_network_enabled",
    ):
        assert booleans[key] is False


def test_docs_match_the_surface_boundary() -> None:
    docs = Path(
        "docs/CIVILIZATION_CORE_P4_M6_9_ENTRY_DEPENDENCY_NON_ACTIVATION_SURFACE.md"
    ).read_text(encoding="utf-8")
    assert "# P4-M6.9 Entry Dependency Non-Activation Surface" in docs
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        assert phrase in docs
    for field_id in FIELD_IDS:
        assert field_id in docs
    assert "true_flags=157" in docs
    assert "false_flags=302" in docs
