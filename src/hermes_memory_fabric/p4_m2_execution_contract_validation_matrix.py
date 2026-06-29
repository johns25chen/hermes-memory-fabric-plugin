from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Sequence

from .p4_m2_execution_surface_contract_definition import (
    execution_surface_contract_field_ids,
)


P4_M2_2_PACKAGE_VERSION = "6.16.0"

EXECUTION_CONTRACT_VALIDATION_MATRIX_BOUNDARY = (
    "P4-M2.2 execution contract validation matrix only. "
    "Read-only validation matrix definition only. Inspection-only. "
    "Not P4-M3. P4-M2 hardening remains active. "
    "P4-M2.1 execution surface contract definition remains the source field contract. "
    "Live contract validation is disabled. Input validation is disabled. "
    "Record validation is disabled. Validation verdicts are disabled. "
    "Readiness verdicts are disabled. Actual decision execution is disabled. "
    "Automatic decision execution is disabled. Manual execution command is disabled. "
    "Execute command is disabled. Approval is disabled. Rejection is disabled. "
    "It does not recommend a decision. It does not rank decisions. "
    "It does not automatically determine readiness. "
    "It does not emit an automatic readiness verdict. "
    "It does not make decisions. It does not execute decisions. "
    "It does not approve memory. It does not reject memory. "
    "It does not approve proposals. It does not reject proposals. "
    "It does not write memory. It does not create memory records. "
    "It does not update memory records. It does not delete memory records. "
    "It does not mutate proposal records. It does not mutate lifecycle records. "
    "It does not mutate do-not-retry guard state. "
    "It does not mutate retry policy. It does not fetch sources. "
    "It does not browse the web. It does not call external APIs. "
    "It does not call connectors. It does not create API/MCP/connector behavior. "
    "It does not automatically trust a source. It does not write provenance. "
    "It does not mutate source/provenance/evidence/citation records. "
    "It does not inject memory into agents. It does not bulk import memory. "
    "It does not auto-ingest chat history. It does not auto-ingest files. "
    "It does not auto-ingest external systems. It does not call agents. "
    "It does not grant authorization semantics. "
    "It does not grant execution semantics. It does not start P4-M3. "
    "It does not start P4-M4. It does not start P4-M5. "
    "It does not start v7. It does not productize."
)


@dataclass(frozen=True)
class ExecutionContractValidationMatrixRow:
    row_order: int
    field_id: str
    validation_dimension: str
    required_presence_signal: str
    schema_closure_signal: str
    trace_completeness_signal: str
    prohibited_semantics: str
    blocking_signal: str
    future_validation_note: str


_EXECUTION_CONTRACT_VALIDATION_MATRIX_ROWS: tuple[
    ExecutionContractValidationMatrixRow,
    ...,
] = (
    ExecutionContractValidationMatrixRow(
        row_order=1,
        field_id="execution-surface-id",
        validation_dimension="Identifier presence and non-execution boundary.",
        required_presence_signal="The matrix row requires a visible execution surface identifier field signal.",
        schema_closure_signal="The identifier field remains a closed P4-M2.1 contract field, not an extensible command namespace.",
        trace_completeness_signal="Future trace review would need to reference the identifier without deriving execution state.",
        prohibited_semantics="No execution, authorization, approval, rejection, mutation, or readiness semantics may derive from the identifier.",
        blocking_signal="Missing identifier signal or identifier-derived execution semantics would block later consideration.",
        future_validation_note="A later human-authorized path may inspect this signal against records, but P4-M2.2 does not validate records.",
    ),
    ExecutionContractValidationMatrixRow(
        row_order=2,
        field_id="human-authorization-reference",
        validation_dimension="Human authorization reference presence without authorization grant.",
        required_presence_signal="The matrix row requires a visible human authorization reference field signal.",
        schema_closure_signal="The reference remains descriptive and cannot become an authorization grant.",
        trace_completeness_signal="Future trace review would need explicit human authorization evidence before any later path is considered.",
        prohibited_semantics="No inferred authorization, implicit approval, rejection, confirmation, or authorization fulfillment.",
        blocking_signal="Missing human authorization reference signal or any authorization semantics would block later consideration.",
        future_validation_note="A later path may define how a human authorization record is inspected, but P4-M2.2 grants none.",
    ),
    ExecutionContractValidationMatrixRow(
        row_order=3,
        field_id="manual-decision-reference",
        validation_dimension="Manual decision reference presence without decision selection.",
        required_presence_signal="The matrix row requires a visible manual decision reference field signal.",
        schema_closure_signal="The reference remains separate from recommendation, ranking, readiness, approval, rejection, and execution.",
        trace_completeness_signal="Future trace review would need a human-selected decision reference before later execution consideration.",
        prohibited_semantics="No automatic decision selection, recommendation, ranking, approval, rejection, or execution.",
        blocking_signal="Missing manual decision reference signal or automatic selection semantics would block later consideration.",
        future_validation_note="A later path may inspect a human-selected reference, but P4-M2.2 selects and validates none.",
    ),
    ExecutionContractValidationMatrixRow(
        row_order=4,
        field_id="execution-intent-declaration",
        validation_dimension="Execution intent declaration presence without executable intent.",
        required_presence_signal="The matrix row requires a visible execution intent declaration field signal.",
        schema_closure_signal="Intent remains contract text only and cannot trigger execution behavior.",
        trace_completeness_signal="Future trace review would need a separate explicit intent signal before any later execution path.",
        prohibited_semantics="No execute intent, manual execution command, execute command, actual execution, or automatic execution.",
        blocking_signal="Missing intent declaration signal or intent-triggered execution semantics would block later consideration.",
        future_validation_note="A later human-authorized path may validate intent wording, but P4-M2.2 emits no validation verdict.",
    ),
    ExecutionContractValidationMatrixRow(
        row_order=5,
        field_id="target-record-reference",
        validation_dimension="Target record reference presence without record access or mutation.",
        required_presence_signal="The matrix row requires a visible target record reference field signal.",
        schema_closure_signal="The target reference remains descriptive and cannot read, validate, or mutate records.",
        trace_completeness_signal="Future trace review would need a target reference that stays linked to audit material.",
        prohibited_semantics="No memory, proposal, lifecycle, do-not-retry, retry, source, provenance, evidence, or citation mutation.",
        blocking_signal="Missing target record reference signal or any target-record mutation would block later consideration.",
        future_validation_note="A later path may inspect real targets, but P4-M2.2 performs no record validation.",
    ),
    ExecutionContractValidationMatrixRow(
        row_order=6,
        field_id="allowed-operation-envelope",
        validation_dimension="Allowed operation envelope presence without operation invocation.",
        required_presence_signal="The matrix row requires a visible allowed operation envelope field signal.",
        schema_closure_signal="The envelope remains schema text only and cannot invoke operations or connectors.",
        trace_completeness_signal="Future trace review would need the operation envelope to be linked to explicit audit boundaries.",
        prohibited_semantics="No operation execution, connector call, API/MCP behavior, write, import, ingest, or injection.",
        blocking_signal="Missing operation envelope signal or executable operation behavior would block later consideration.",
        future_validation_note="A later path may validate envelope compliance, but P4-M2.2 defines rows only.",
    ),
    ExecutionContractValidationMatrixRow(
        row_order=7,
        field_id="precondition-evidence",
        validation_dimension="Precondition evidence presence without source fetching or evidence writing.",
        required_presence_signal="The matrix row requires a visible precondition evidence field signal.",
        schema_closure_signal="Precondition evidence remains descriptive and cannot fetch, trust, write, or mutate evidence.",
        trace_completeness_signal="Future trace review would need precondition evidence references without hidden source activity.",
        prohibited_semantics="No source fetching, browsing, external API call, source trust, evidence write, citation write, or provenance write.",
        blocking_signal="Missing precondition evidence signal or evidence/source/provenance mutation would block later consideration.",
        future_validation_note="A later path may inspect evidence, but P4-M2.2 does not fetch sources or write provenance.",
    ),
    ExecutionContractValidationMatrixRow(
        row_order=8,
        field_id="risk-and-blocking-signals",
        validation_dimension="Risk and blocking signal presence without verdict generation.",
        required_presence_signal="The matrix row requires visible risk and blocking signal field text.",
        schema_closure_signal="Risk and blocker fields remain descriptive and cannot determine readiness.",
        trace_completeness_signal="Future trace review would need risk and blocker text preserved for human inspection.",
        prohibited_semantics="No automatic readiness verdict, validation verdict, decision ranking, decision recommendation, approval, rejection, or execution.",
        blocking_signal="Missing risk/blocker signal or automatic readiness semantics would block later consideration.",
        future_validation_note="A later path may validate blockers, but P4-M2.2 emits no readiness or validation verdict.",
    ),
    ExecutionContractValidationMatrixRow(
        row_order=9,
        field_id="audit-trace-id",
        validation_dimension="Audit trace identifier presence without audit or provenance writes.",
        required_presence_signal="The matrix row requires a visible audit trace identifier field signal.",
        schema_closure_signal="The audit trace field remains a contract reference and cannot write audit or provenance state.",
        trace_completeness_signal="Future trace review would need a stable audit trace reference for human inspection.",
        prohibited_semantics="No audit write, provenance write, source mutation, evidence mutation, citation mutation, or execution trace mutation.",
        blocking_signal="Missing audit trace identifier signal or trace/provenance mutation would block later consideration.",
        future_validation_note="A later path may compare trace identifiers, but P4-M2.2 writes no trace state.",
    ),
    ExecutionContractValidationMatrixRow(
        row_order=10,
        field_id="operator-confirmation-placeholder",
        validation_dimension="Operator confirmation placeholder presence without confirmation semantics.",
        required_presence_signal="The matrix row requires a visible operator confirmation placeholder field signal.",
        schema_closure_signal="The placeholder remains non-confirming and cannot approve, reject, authorize, or execute.",
        trace_completeness_signal="Future trace review would need explicit operator confirmation separate from this placeholder.",
        prohibited_semantics="No approval, rejection, authorization, confirmation, execute command, or manual execution command.",
        blocking_signal="Missing placeholder signal or any confirmation semantics would block later consideration.",
        future_validation_note="A later path may define confirmation evidence, but P4-M2.2 does not confirm anything.",
    ),
    ExecutionContractValidationMatrixRow(
        row_order=11,
        field_id="execution-preview-output",
        validation_dimension="Execution preview output presence without preview or execution state mutation.",
        required_presence_signal="The matrix row requires a visible execution preview output field signal.",
        schema_closure_signal="Preview output remains descriptive and cannot become execution input or state.",
        trace_completeness_signal="Future trace review would need preview output linked to audit material without mutation.",
        prohibited_semantics="No execution, approval, rejection, readiness verdict, validation verdict, memory write, proposal mutation, or preview-state mutation.",
        blocking_signal="Preview output that becomes execution input or writes state would block later consideration.",
        future_validation_note="A later path may validate preview output, but P4-M2.2 does not validate live previews.",
    ),
    ExecutionContractValidationMatrixRow(
        row_order=12,
        field_id="rollback-consideration",
        validation_dimension="Rollback consideration presence without rollback command behavior.",
        required_presence_signal="The matrix row requires a visible rollback consideration field signal.",
        schema_closure_signal="Rollback consideration remains text only and cannot revert, cleanup, archive, stale, or delete records.",
        trace_completeness_signal="Future trace review would need rollback considerations preserved for human inspection.",
        prohibited_semantics="No rollback command, cleanup, archive, stale, delete, lifecycle mutation, or record mutation.",
        blocking_signal="Rollback-command behavior or lifecycle mutation would block later consideration.",
        future_validation_note="A later path may inspect rollback sufficiency, but P4-M2.2 performs no rollback validation.",
    ),
    ExecutionContractValidationMatrixRow(
        row_order=13,
        field_id="side-effect-boundary",
        validation_dimension="Side-effect boundary presence with side effects disabled.",
        required_presence_signal="The matrix row requires a visible side-effect boundary field signal.",
        schema_closure_signal="The side-effect boundary must remain closed to writes, mutation, external calls, imports, ingests, and injections.",
        trace_completeness_signal="Future trace review would need explicit side-effect boundaries before later execution consideration.",
        prohibited_semantics="No write, mutation, external call, connector call, agent call, import, ingest, injection, deployment, or productization.",
        blocking_signal="Any side effect or missing side-effect boundary signal would block later consideration.",
        future_validation_note="A later path may validate side-effect controls, but P4-M2.2 has no side effects.",
    ),
    ExecutionContractValidationMatrixRow(
        row_order=14,
        field_id="external-system-boundary",
        validation_dimension="External system boundary presence with external behavior disabled.",
        required_presence_signal="The matrix row requires a visible external system boundary field signal.",
        schema_closure_signal="The external boundary must remain closed to API, MCP, connector, web, source, and agent calls.",
        trace_completeness_signal="Future trace review would need external-system boundaries preserved for human inspection.",
        prohibited_semantics="No API call, MCP behavior, connector behavior, web browse, source fetch, external system call, or agent call.",
        blocking_signal="Any external system behavior or connector behavior would block later consideration.",
        future_validation_note="A later path may inspect external readiness, but P4-M2.2 creates no API/MCP/connector behavior.",
    ),
    ExecutionContractValidationMatrixRow(
        row_order=15,
        field_id="authorization-semantics-disabled",
        validation_dimension="Authorization semantics disabled signal remains explicit.",
        required_presence_signal="The matrix row requires a visible authorization-semantics-disabled field signal.",
        schema_closure_signal="Disabled authorization status remains closed and cannot become a grant.",
        trace_completeness_signal="Future trace review would need authorization-disabled status preserved in reports and boundaries.",
        prohibited_semantics="No authorization grant, approval, rejection, confirmation, or human authorization fulfillment.",
        blocking_signal="Any authorization semantics would block later consideration.",
        future_validation_note="A later path may define authorization checks, but P4-M2.2 grants no authorization semantics.",
    ),
    ExecutionContractValidationMatrixRow(
        row_order=16,
        field_id="execution-semantics-disabled",
        validation_dimension="Execution semantics disabled signal remains explicit.",
        required_presence_signal="The matrix row requires a visible execution-semantics-disabled field signal.",
        schema_closure_signal="Disabled execution status remains closed and cannot become execution behavior.",
        trace_completeness_signal="Future trace review would need execution-disabled status preserved in reports and boundaries.",
        prohibited_semantics="No actual execution, automatic execution, manual execution command, execute command, deployment, or productization.",
        blocking_signal="Any execution semantics would block later consideration.",
        future_validation_note="A later path may define execution checks, but P4-M2.2 grants no execution semantics.",
    ),
)


def list_execution_contract_validation_matrix_rows() -> tuple[
    ExecutionContractValidationMatrixRow,
    ...,
]:
    return _EXECUTION_CONTRACT_VALIDATION_MATRIX_ROWS


def execution_contract_validation_matrix_field_ids() -> tuple[str, ...]:
    return tuple(
        row.field_id
        for row in list_execution_contract_validation_matrix_rows()
    )


def render_execution_contract_validation_matrix_markdown(
    rows: Sequence[ExecutionContractValidationMatrixRow] | None = None,
) -> str:
    row_values = (
        tuple(rows)
        if rows is not None
        else list_execution_contract_validation_matrix_rows()
    )
    status = execution_contract_validation_matrix_report()
    lines = [
        "# P4-M2.2 Execution Contract Validation Matrix",
        "",
        "P4-M2.2 execution contract validation matrix only.",
        "",
        "Read-only validation matrix definition only.",
        "",
        "Inspection-only.",
        "",
        "Not P4-M3.",
        "",
        "P4-M2 hardening remains active.",
        "",
        "P4-M2.1 execution surface contract definition remains the source field contract.",
        "",
        "Live contract validation is disabled.",
        "",
        "Input validation is disabled.",
        "",
        "Record validation is disabled.",
        "",
        "Validation verdicts are disabled.",
        "",
        "Readiness verdicts are disabled.",
        "",
        "Actual decision execution is disabled.",
        "",
        "Automatic decision execution is disabled.",
        "",
        "Manual execution command is disabled.",
        "",
        "Execute command is disabled.",
        "",
        "No authorization semantics are granted by this validation matrix.",
        "",
        "No execution semantics are granted by this validation matrix.",
        "",
        "No memory writing is performed by this validation matrix.",
        "",
        "No mutation is performed by this validation matrix.",
        "",
        "No API/MCP/connector behavior is performed by this validation matrix.",
        "",
        "No agent call is performed by this validation matrix.",
        "",
        EXECUTION_CONTRACT_VALIDATION_MATRIX_BOUNDARY,
        "",
        "## Status Report",
        "",
    ]
    for key, value in status.items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Validation Matrix Rows", ""])
    for row in row_values:
        lines.extend(
            [
                f"### {row.row_order}. {row.field_id}",
                "",
                f"- Validation dimension: {row.validation_dimension}",
                f"- Required presence signal: {row.required_presence_signal}",
                f"- Schema closure signal: {row.schema_closure_signal}",
                f"- Trace completeness signal: {row.trace_completeness_signal}",
                f"- Prohibited semantics: {row.prohibited_semantics}",
                f"- Blocking signal: {row.blocking_signal}",
                f"- Future validation note: {row.future_validation_note}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def execution_contract_validation_matrix_as_dicts(
    rows: Sequence[ExecutionContractValidationMatrixRow] | None = None,
) -> tuple[dict[str, object], ...]:
    row_values = (
        tuple(rows)
        if rows is not None
        else list_execution_contract_validation_matrix_rows()
    )
    return tuple(asdict(row) for row in row_values)


def execution_contract_validation_matrix_report() -> dict[str, object]:
    return {
        "phase": "P4-M2.2",
        "feature": "Execution Contract Validation Matrix",
        "mode": "read-only",
        "matrix_row_count": len(_EXECUTION_CONTRACT_VALIDATION_MATRIX_ROWS),
        "p4_m2_started": True,
        "execution_surface_contract_definition_available": True,
        "execution_contract_validation_matrix_started": True,
        "validation_matrix_definition_only": True,
        "schema_validation_rules_defined": True,
        "trace_completeness_rules_defined": True,
        "blocking_signal_rules_defined": True,
        "inspection_only": True,
        "live_contract_validation_enabled": False,
        "input_validation_enabled": False,
        "record_validation_enabled": False,
        "validation_verdict_enabled": False,
        "readiness_verdict_enabled": False,
        "actual_decision_execution_enabled": False,
        "automatic_decision_execution_enabled": False,
        "manual_execution_command_enabled": False,
        "execute_command_enabled": False,
        "approval_enabled": False,
        "rejection_enabled": False,
        "automatic_decision_recommendation_enabled": False,
        "decision_ranking_enabled": False,
        "automatic_readiness_verdict_enabled": False,
        "authorization_semantics_granted": False,
        "execution_semantics_granted": False,
        "memory_write_enabled": False,
        "memory_record_mutation_enabled": False,
        "proposal_mutation_enabled": False,
        "lifecycle_mutation_enabled": False,
        "do_not_retry_guard_mutation_enabled": False,
        "retry_policy_mutation_enabled": False,
        "source_fetching_enabled": False,
        "source_provenance_mutation_enabled": False,
        "provenance_write_enabled": False,
        "memory_injection_enabled": False,
        "bulk_import_enabled": False,
        "auto_ingest_enabled": False,
        "agent_call_enabled": False,
        "api_mcp_connector_enabled": False,
        "p4_m3_started": False,
        "p4_m4_started": False,
        "p4_m5_started": False,
        "v7_started": False,
        "productization_started": False,
        "package_version": P4_M2_2_PACKAGE_VERSION,
        "boundary": EXECUTION_CONTRACT_VALIDATION_MATRIX_BOUNDARY,
    }


_P4_M2_1_FIELD_IDS = execution_surface_contract_field_ids()
if execution_contract_validation_matrix_field_ids() != _P4_M2_1_FIELD_IDS:
    raise RuntimeError("execution_contract_validation_matrix_field_ids_mismatch")
