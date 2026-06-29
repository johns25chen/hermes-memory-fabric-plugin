from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Sequence


P4_M2_1_PACKAGE_VERSION = "6.16.0"

EXECUTION_SURFACE_CONTRACT_BOUNDARY = (
    "P4-M2.1 execution surface contract definition only. "
    "Read-only contract/schema/trace field definition only. "
    "Inspection-only. Not P4-M3. P4-M2 hardening remains active. "
    "Actual decision execution is disabled. "
    "Automatic decision execution is disabled. "
    "Manual execution command is disabled. Execute command is disabled. "
    "Approval is disabled. Rejection is disabled. "
    "It does not recommend a decision. It does not rank decisions. "
    "It does not automatically determine readiness. "
    "It does not emit an automatic readiness verdict. "
    "It does not make decisions. It does not execute decisions. "
    "It does not approve memory. It does not reject memory. "
    "It does not approve proposals. It does not reject proposals. "
    "It does not write memory. It does not create memory records. "
    "It does not update memory records. It does not delete memory records. "
    "It does not mutate proposal records. "
    "It does not mutate lifecycle records. "
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
class ExecutionSurfaceContractField:
    field_order: int
    field_id: str
    field_name: str
    field_purpose: str
    required_description: str
    inspection_signal: str
    prohibited_semantics: str
    blocking_signal: str


_EXECUTION_SURFACE_CONTRACT_FIELDS: tuple[ExecutionSurfaceContractField, ...] = (
    ExecutionSurfaceContractField(
        field_order=1,
        field_id="execution-surface-id",
        field_name="Execution surface identifier",
        field_purpose="Identify a future controlled execution surface without creating execution behavior.",
        required_description="A unique future execution surface identifier for inspection only.",
        inspection_signal="The identifier is present, stable, and not used as an execution command.",
        prohibited_semantics="No execution, authorization, approval, rejection, mutation, or readiness semantics may derive from this identifier.",
        blocking_signal="Missing identifier or identifier-derived execution semantics block later consideration.",
    ),
    ExecutionSurfaceContractField(
        field_order=2,
        field_id="human-authorization-reference",
        field_name="Human authorization reference",
        field_purpose="Describe where explicit human authorization would be referenced later without granting authorization now.",
        required_description="A reference to explicit human authorization, but not authorization itself.",
        inspection_signal="The reference is descriptive and does not approve, reject, or execute anything.",
        prohibited_semantics="No inferred authorization, implicit approval, or authorization grant.",
        blocking_signal="Missing reference or any authorization semantics blocks later consideration.",
    ),
    ExecutionSurfaceContractField(
        field_order=3,
        field_id="manual-decision-reference",
        field_name="Manual decision reference",
        field_purpose="Describe the future human-selected manual decision or preview item without selecting or executing it.",
        required_description="A reference to a human-selected manual decision or preview item.",
        inspection_signal="The reference field exists and remains separate from recommendation, ranking, readiness, and execution.",
        prohibited_semantics="No automatic decision selection, recommendation, ranking, approval, rejection, or execution.",
        blocking_signal="Missing manual reference or automatic selection semantics block later consideration.",
    ),
    ExecutionSurfaceContractField(
        field_order=4,
        field_id="execution-intent-declaration",
        field_name="Execution intent declaration",
        field_purpose="Define where a later path would describe intent while P4-M2.1 remains inspection-only.",
        required_description="An explicit intent description field, still inspection-only in P4-M2.1.",
        inspection_signal="Intent is described as contract text only and cannot trigger execution.",
        prohibited_semantics="No execute intent, manual execution command, execute command, or automatic execution.",
        blocking_signal="Ambiguous intent or any intent-triggered execution semantics block later consideration.",
    ),
    ExecutionSurfaceContractField(
        field_order=5,
        field_id="target-record-reference",
        field_name="Target record reference",
        field_purpose="Describe the future target record reference without reading or mutating records.",
        required_description="A reference to the target record, but no mutation.",
        inspection_signal="The target field is descriptive and produces no record writes or state changes.",
        prohibited_semantics="No memory, proposal, lifecycle, do-not-retry, retry, source, provenance, evidence, or citation mutation.",
        blocking_signal="Missing target reference or any target-record mutation blocks later consideration.",
    ),
    ExecutionSurfaceContractField(
        field_order=6,
        field_id="allowed-operation-envelope",
        field_name="Allowed operation envelope",
        field_purpose="Describe the future operation envelope required for inspection before any later path is considered.",
        required_description="A future operation envelope description, without execution.",
        inspection_signal="The envelope is visible as schema text only and cannot invoke operations.",
        prohibited_semantics="No operation execution, connector call, API/MCP behavior, write, import, ingest, or injection.",
        blocking_signal="Undefined operation envelope or executable behavior blocks later consideration.",
    ),
    ExecutionSurfaceContractField(
        field_order=7,
        field_id="precondition-evidence",
        field_name="Precondition evidence",
        field_purpose="Describe future precondition evidence required for later consideration without fetching or writing evidence.",
        required_description="A description of preconditions required for later consideration.",
        inspection_signal="Precondition fields are visible and do not fetch sources or write provenance.",
        prohibited_semantics="No source fetching, browsing, external API call, source trust, evidence write, citation write, or provenance write.",
        blocking_signal="Missing precondition description or evidence/source/provenance mutation blocks later consideration.",
    ),
    ExecutionSurfaceContractField(
        field_order=8,
        field_id="risk-and-blocking-signals",
        field_name="Risk and blocking signals",
        field_purpose="Define the future risk and blocker description fields without producing automatic readiness verdicts.",
        required_description="A description of risks and blockers.",
        inspection_signal="Risk and blocker text is visible and does not determine readiness.",
        prohibited_semantics="No automatic readiness verdict, decision ranking, decision recommendation, approval, rejection, or execution.",
        blocking_signal="Missing blocker description or automatic readiness semantics block later consideration.",
    ),
    ExecutionSurfaceContractField(
        field_order=9,
        field_id="audit-trace-id",
        field_name="Audit trace identifier",
        field_purpose="Describe a future audit trace reference field without writing audit or provenance records.",
        required_description="A future audit trace reference field.",
        inspection_signal="The trace field is present as contract text only and writes no audit state.",
        prohibited_semantics="No audit write, provenance write, source mutation, evidence mutation, citation mutation, or execution trace mutation.",
        blocking_signal="Missing trace field or trace/provenance state mutation blocks later consideration.",
    ),
    ExecutionSurfaceContractField(
        field_order=10,
        field_id="operator-confirmation-placeholder",
        field_name="Operator confirmation placeholder",
        field_purpose="Reserve a placeholder for later human confirmation without confirmation semantics in P4-M2.1.",
        required_description="A placeholder for later human confirmation, with no confirmation semantics in P4-M2.1.",
        inspection_signal="The placeholder is visible and explicitly non-confirming.",
        prohibited_semantics="No approval, rejection, authorization, confirmation, execute command, or manual execution command.",
        blocking_signal="Missing placeholder boundary or any confirmation semantics block later consideration.",
    ),
    ExecutionSurfaceContractField(
        field_order=11,
        field_id="execution-preview-output",
        field_name="Execution preview output",
        field_purpose="Describe a future preview output field while keeping P4-M2.1 inspection-only.",
        required_description="A future preview output field, inspection-only.",
        inspection_signal="Preview output is described without creating preview state or execution state.",
        prohibited_semantics="No execution, approval, rejection, readiness verdict, memory write, proposal mutation, or preview-state mutation.",
        blocking_signal="Preview output that becomes execution input or writes state blocks later consideration.",
    ),
    ExecutionSurfaceContractField(
        field_order=12,
        field_id="rollback-consideration",
        field_name="Rollback consideration",
        field_purpose="Describe future rollback considerations without adding rollback commands or mutation behavior.",
        required_description="A future rollback consideration field, no rollback command.",
        inspection_signal="Rollback text is visible and cannot revert, cleanup, archive, stale, or delete records.",
        prohibited_semantics="No rollback command, cleanup, archive, stale, delete, lifecycle mutation, or record mutation.",
        blocking_signal="Rollback-command behavior or lifecycle mutation blocks later consideration.",
    ),
    ExecutionSurfaceContractField(
        field_order=13,
        field_id="side-effect-boundary",
        field_name="Side-effect boundary",
        field_purpose="Describe side-effect boundaries while guaranteeing P4-M2.1 produces no side effects.",
        required_description="A side-effect boundary description, with no side effects.",
        inspection_signal="The boundary states writes, mutation, external calls, agent calls, imports, ingests, and injections remain disabled.",
        prohibited_semantics="No write, mutation, external call, connector call, agent call, import, ingest, injection, deployment, or productization.",
        blocking_signal="Any side effect or missing side-effect boundary blocks later consideration.",
    ),
    ExecutionSurfaceContractField(
        field_order=14,
        field_id="external-system-boundary",
        field_name="External system boundary",
        field_purpose="Describe external system limits without calling external systems or connectors.",
        required_description="An external system boundary description, with no external calls.",
        inspection_signal="The boundary states API, MCP, connector, web, source, and agent calls remain disabled.",
        prohibited_semantics="No API call, MCP behavior, connector behavior, web browse, source fetch, external system call, or agent call.",
        blocking_signal="Any external system behavior or connector behavior blocks later consideration.",
    ),
    ExecutionSurfaceContractField(
        field_order=15,
        field_id="authorization-semantics-disabled",
        field_name="Authorization semantics disabled",
        field_purpose="State that P4-M2.1 grants no authorization semantics.",
        required_description="A statement that P4-M2.1 grants no authorization semantics.",
        inspection_signal="The disabled authorization status is explicit in the status report and boundary.",
        prohibited_semantics="No authorization grant, approval, rejection, confirmation, or human authorization fulfillment.",
        blocking_signal="Any authorization semantics block later consideration.",
    ),
    ExecutionSurfaceContractField(
        field_order=16,
        field_id="execution-semantics-disabled",
        field_name="Execution semantics disabled",
        field_purpose="State that P4-M2.1 grants no execution semantics.",
        required_description="A statement that P4-M2.1 grants no execution semantics.",
        inspection_signal="The disabled execution status is explicit in the status report and boundary.",
        prohibited_semantics="No actual execution, automatic execution, manual execution command, execute command, deployment, or productization.",
        blocking_signal="Any execution semantics block later consideration.",
    ),
)


def list_execution_surface_contract_fields() -> tuple[
    ExecutionSurfaceContractField,
    ...,
]:
    return _EXECUTION_SURFACE_CONTRACT_FIELDS


def execution_surface_contract_field_ids() -> tuple[str, ...]:
    return tuple(field.field_id for field in list_execution_surface_contract_fields())


def render_execution_surface_contract_markdown(
    fields: Sequence[ExecutionSurfaceContractField] | None = None,
) -> str:
    field_values = (
        tuple(fields)
        if fields is not None
        else list_execution_surface_contract_fields()
    )
    status = execution_surface_contract_report()
    lines = [
        "# P4-M2.1 Execution Surface Contract Definition",
        "",
        "P4-M2.1 execution surface contract definition only.",
        "",
        "Read-only contract/schema/trace field definition only.",
        "",
        "Inspection-only.",
        "",
        "Not P4-M3.",
        "",
        "P4-M2 hardening remains active.",
        "",
        "Actual decision execution is disabled.",
        "",
        "Automatic decision execution is disabled.",
        "",
        "Manual execution command is disabled.",
        "",
        "Execute command is disabled.",
        "",
        "No authorization semantics are granted by this contract definition.",
        "",
        "No execution semantics are granted by this contract definition.",
        "",
        "No memory writing is performed by this contract definition.",
        "",
        "No mutation is performed by this contract definition.",
        "",
        "No API/MCP/connector behavior is performed by this contract definition.",
        "",
        "No agent call is performed by this contract definition.",
        "",
        EXECUTION_SURFACE_CONTRACT_BOUNDARY,
        "",
        "## Status Report",
        "",
    ]
    for key, value in status.items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Contract Fields", ""])
    for field in field_values:
        lines.extend(
            [
                f"### {field.field_order}. {field.field_id}",
                "",
                f"- Field name: {field.field_name}",
                f"- Field purpose: {field.field_purpose}",
                f"- Required description: {field.required_description}",
                f"- Inspection signal: {field.inspection_signal}",
                f"- Prohibited semantics: {field.prohibited_semantics}",
                f"- Blocking signal: {field.blocking_signal}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def execution_surface_contract_as_dicts(
    fields: Sequence[ExecutionSurfaceContractField] | None = None,
) -> tuple[dict[str, object], ...]:
    field_values = (
        tuple(fields)
        if fields is not None
        else list_execution_surface_contract_fields()
    )
    return tuple(asdict(field) for field in field_values)


def execution_surface_contract_report() -> dict[str, object]:
    return {
        "phase": "P4-M2.1",
        "feature": "Execution Surface Contract Definition",
        "mode": "read-only",
        "contract_field_count": len(_EXECUTION_SURFACE_CONTRACT_FIELDS),
        "p4_m2_started": True,
        "execution_surface_contract_definition_started": True,
        "execution_surface_contract_only": True,
        "schema_definition_only": True,
        "trace_field_definition_only": True,
        "inspection_only": True,
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
        "package_version": P4_M2_1_PACKAGE_VERSION,
        "boundary": EXECUTION_SURFACE_CONTRACT_BOUNDARY,
    }
