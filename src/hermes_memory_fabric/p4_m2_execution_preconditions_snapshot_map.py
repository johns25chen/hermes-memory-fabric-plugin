from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Sequence

from .p4_m2_execution_contract_validation_matrix import (
    execution_contract_validation_matrix_field_ids,
)
from .p4_m2_execution_surface_contract_definition import (
    execution_surface_contract_field_ids,
)
from .p4_m2_human_confirmation_snapshot_contract import (
    human_confirmation_snapshot_contract_field_ids,
)
from .p4_m2_manual_authorization_evidence_envelope import (
    manual_authorization_evidence_envelope_field_ids,
)


P4_M2_5_PACKAGE_VERSION = "6.16.0"

EXECUTION_PRECONDITIONS_SNAPSHOT_MAP_BOUNDARY = (
    "P4-M2.5 execution preconditions snapshot map only. "
    "Execution Preconditions Snapshot Map definition-only. "
    "Read-only. Inspection-only. Definition-only. "
    "It defines a stable read-only structure for future manual execution precondition snapshots. "
    "It references P4-M2.1 execution surface contract definition, "
    "P4-M2.2 execution contract validation matrix, "
    "P4-M2.3 manual authorization evidence envelope, and "
    "P4-M2.4 human confirmation snapshot contract as definition layers only. "
    "No execution. No confirmation. No authorization. No approval. No rejection. "
    "No memory mutation. No memory record creation. No memory record update. "
    "No memory record deletion. No proposal mutation. No lifecycle mutation. "
    "No retry policy mutation. No source fetching. No provenance writing. "
    "No evidence mutation. No citation mutation. No live confirmation validation. "
    "No live authorization validation. No live contract validation. "
    "No input validation. No record validation. No validation verdict. "
    "No readiness verdict. No automatic readiness verdict. "
    "No decision recommendation. No decision ranking. "
    "No confirmation semantics. No authorization semantics. No execution semantics. "
    "No API. No MCP. No connector. No agent call. "
    "No Codex/Hermes/ChatGPT product-code auto-call. "
    "No P4-M3. No P4-M4. No P4-M5. No v7. No productization. "
    "No UI. No Operator Console. No MVP. No deploy. No full Memory Graph."
)


@dataclass(frozen=True)
class ExecutionPreconditionsSnapshotMapField:
    field_order: int
    field_id: str
    field_name: str
    field_purpose: str
    snapshot_signal: str
    evidence_boundary: str
    prohibited_semantics: str
    blocking_boundary: str
    future_precondition_note: str


_EXECUTION_PRECONDITIONS_SNAPSHOT_MAP_FIELDS: tuple[
    ExecutionPreconditionsSnapshotMapField,
    ...,
] = (
    ExecutionPreconditionsSnapshotMapField(
        field_order=1,
        field_id="execution-preconditions-snapshot-map-id",
        field_name="Execution Preconditions Snapshot Map Identifier",
        field_purpose="Names the inspection-only map without creating execution, confirmation, authorization, validation, or readiness state.",
        snapshot_signal="A stable map identifier signal must be visible for future manual precondition snapshot review.",
        evidence_boundary="The identifier is definition text only and does not create memory, proposal, lifecycle, source, provenance, evidence, or citation records.",
        prohibited_semantics="No execution, confirmation, authorization, approval, rejection, validation verdict, readiness verdict, mutation, or decision recommendation may derive from the identifier.",
        blocking_boundary="Identifier-derived execution, confirmation, authorization, validation, readiness, ranking, or mutation semantics remain out of scope.",
        future_precondition_note="A later human-governed path may compare a map identifier to records; P4-M2.5 validates no records.",
    ),
    ExecutionPreconditionsSnapshotMapField(
        field_order=2,
        field_id="execution-surface-reference",
        field_name="Execution Surface Reference",
        field_purpose="References the P4-M2.1 execution surface contract definition as read-only source context.",
        snapshot_signal="A visible P4-M2.1 execution surface reference signal must be present.",
        evidence_boundary="The reference preserves source context without modifying the execution surface contract or fetching sources.",
        prohibited_semantics="No execution-surface mutation, live contract validation, API, MCP, connector, agent call, execution, or product-code auto-call.",
        blocking_boundary="Missing reference or executable surface behavior remains outside P4-M2.5.",
        future_precondition_note="A later path may inspect the P4-M2.1 definition; P4-M2.5 runs no live contract validation.",
    ),
    ExecutionPreconditionsSnapshotMapField(
        field_order=3,
        field_id="execution-contract-validation-matrix-reference",
        field_name="Execution Contract Validation Matrix Reference",
        field_purpose="References the P4-M2.2 validation matrix definition without running validation.",
        snapshot_signal="A visible P4-M2.2 validation matrix reference signal must be present.",
        evidence_boundary="The reference preserves validation-matrix context without input validation, record validation, or verdict generation.",
        prohibited_semantics="No live contract validation, input validation, record validation, validation verdict, readiness verdict, or automatic readiness verdict.",
        blocking_boundary="Missing matrix reference or validation behavior remains outside P4-M2.5.",
        future_precondition_note="A later path may inspect matrix requirements; P4-M2.5 emits no validation verdict.",
    ),
    ExecutionPreconditionsSnapshotMapField(
        field_order=4,
        field_id="manual-authorization-evidence-envelope-reference",
        field_name="Manual Authorization Evidence Envelope Reference",
        field_purpose="References the P4-M2.3 evidence envelope definition without authorizing anything.",
        snapshot_signal="A visible P4-M2.3 manual authorization evidence envelope reference signal must be present.",
        evidence_boundary="The reference preserves evidence-envelope context without evidence mutation, source fetching, provenance writing, or citation mutation.",
        prohibited_semantics="No authorization, live authorization validation, approval, rejection, evidence mutation, provenance writing, citation mutation, or execution.",
        blocking_boundary="Missing envelope reference or authorization/evidence mutation behavior remains outside P4-M2.5.",
        future_precondition_note="A later path may inspect authorization evidence references; P4-M2.5 grants no authorization semantics.",
    ),
    ExecutionPreconditionsSnapshotMapField(
        field_order=5,
        field_id="human-confirmation-snapshot-reference",
        field_name="Human Confirmation Snapshot Reference",
        field_purpose="References the P4-M2.4 human confirmation snapshot contract without confirming anything.",
        snapshot_signal="A visible P4-M2.4 human confirmation snapshot reference signal must be present.",
        evidence_boundary="The reference preserves confirmation-snapshot context without live confirmation validation or confirmation state.",
        prohibited_semantics="No confirmation, live confirmation validation, authorization, approval, rejection, execution, or readiness verdict.",
        blocking_boundary="Missing confirmation snapshot reference or confirmation behavior remains outside P4-M2.5.",
        future_precondition_note="A later path may inspect human confirmation snapshots; P4-M2.5 grants no confirmation semantics.",
    ),
    ExecutionPreconditionsSnapshotMapField(
        field_order=6,
        field_id="manual-decision-reference",
        field_name="Manual Decision Reference",
        field_purpose="Links to a future manual decision reference without selecting, recommending, ranking, confirming, authorizing, or executing a decision.",
        snapshot_signal="A manual decision reference signal must be visible and non-ranking.",
        evidence_boundary="The reference remains descriptive and cannot mutate proposal, lifecycle, retry, memory, evidence, citation, or provenance state.",
        prohibited_semantics="No decision recommendation, decision ranking, approval, rejection, confirmation, authorization, readiness verdict, or execution.",
        blocking_boundary="Automatic selection, recommendation, ranking, readiness, or execution behavior remains outside P4-M2.5.",
        future_precondition_note="A later path may inspect a human-selected decision reference; P4-M2.5 selects none.",
    ),
    ExecutionPreconditionsSnapshotMapField(
        field_order=7,
        field_id="operator-reference",
        field_name="Operator Reference",
        field_purpose="Identifies a future operator reference required for snapshot inspection without confirming identity or authority.",
        snapshot_signal="An operator reference signal must be visible and separate from confirmation, authorization, approval, rejection, or execution.",
        evidence_boundary="The operator reference is definition text only and writes no operator, memory, proposal, audit, evidence, or provenance record.",
        prohibited_semantics="No operator confirmation, authorization, approval, rejection, execution, agent call, or product-code auto-call.",
        blocking_boundary="Operator-derived confirmation, authorization, or execution behavior remains outside P4-M2.5.",
        future_precondition_note="A later path may inspect operator evidence; P4-M2.5 confirms no operator authority.",
    ),
    ExecutionPreconditionsSnapshotMapField(
        field_order=8,
        field_id="precondition-category",
        field_name="Precondition Category",
        field_purpose="Defines a future precondition category label without validating, ranking, or scoring the category.",
        snapshot_signal="A precondition category signal must be visible for future human inspection.",
        evidence_boundary="The category label is closed definition text and does not fetch sources, write evidence, or mutate records.",
        prohibited_semantics="No input validation, record validation, readiness verdict, validation verdict, decision ranking, or automatic readiness verdict.",
        blocking_boundary="Category-derived validation, readiness, or recommendation behavior remains outside P4-M2.5.",
        future_precondition_note="A later path may define category checks; P4-M2.5 defines labels only.",
    ),
    ExecutionPreconditionsSnapshotMapField(
        field_order=9,
        field_id="precondition-snapshot-signal",
        field_name="Precondition Snapshot Signal",
        field_purpose="Defines the future snapshot signal for a precondition without treating the signal as validated evidence.",
        snapshot_signal="A precondition snapshot signal must be visible and read-only.",
        evidence_boundary="The signal is not live evidence, does not validate live input, and writes no evidence, citation, source, or provenance record.",
        prohibited_semantics="No live confirmation validation, live authorization validation, live contract validation, input validation, record validation, or validation verdict.",
        blocking_boundary="Signal-derived validation, readiness, confirmation, authorization, or execution behavior remains outside P4-M2.5.",
        future_precondition_note="A later path may inspect the signal against governed evidence; P4-M2.5 performs no inspection against records.",
    ),
    ExecutionPreconditionsSnapshotMapField(
        field_order=10,
        field_id="precondition-evidence-reference",
        field_name="Precondition Evidence Reference",
        field_purpose="References future precondition evidence without fetching, trusting, writing, validating, or mutating evidence.",
        snapshot_signal="A precondition evidence reference signal must be visible and non-verdict-bearing.",
        evidence_boundary="Evidence references remain textual and do not fetch sources, write provenance, mutate evidence, or mutate citations.",
        prohibited_semantics="No source fetching, source trust, provenance writing, evidence mutation, citation mutation, input validation, record validation, or readiness verdict.",
        blocking_boundary="Evidence reference mutation, source fetching, or verdict generation remains outside P4-M2.5.",
        future_precondition_note="A later path may inspect evidence references; P4-M2.5 fetches and writes none.",
    ),
    ExecutionPreconditionsSnapshotMapField(
        field_order=11,
        field_id="risk-blocking-signal",
        field_name="Risk Blocking Signal",
        field_purpose="Defines a future risk/blocker signal without making readiness decisions.",
        snapshot_signal="A risk-blocking signal must be visible and non-verdict-bearing.",
        evidence_boundary="Risk text remains definition-only and does not update proposal, lifecycle, retry, do-not-retry, memory, evidence, or provenance records.",
        prohibited_semantics="No validation verdict, readiness verdict, automatic readiness verdict, decision recommendation, decision ranking, approval, rejection, or execution.",
        blocking_boundary="Risk-derived readiness, ranking, recommendation, or mutation behavior remains outside P4-M2.5.",
        future_precondition_note="A later path may inspect blockers; P4-M2.5 determines no readiness.",
    ),
    ExecutionPreconditionsSnapshotMapField(
        field_order=12,
        field_id="dependency-boundary-signal",
        field_name="Dependency Boundary Signal",
        field_purpose="Defines future dependency boundary text without calling dependencies or external systems.",
        snapshot_signal="A dependency boundary signal must be visible.",
        evidence_boundary="Dependency boundary text cannot call APIs, MCP, connectors, agents, source fetchers, product code, or external systems.",
        prohibited_semantics="No API, MCP, connector, agent call, Codex/Hermes/ChatGPT product-code auto-call, source fetching, deploy, UI, or Operator Console.",
        blocking_boundary="Dependency calls or productized integration behavior remains outside P4-M2.5.",
        future_precondition_note="A later path may inspect dependency boundaries; P4-M2.5 invokes no dependency.",
    ),
    ExecutionPreconditionsSnapshotMapField(
        field_order=13,
        field_id="revocation-or-expiry-signal",
        field_name="Revocation Or Expiry Signal",
        field_purpose="Defines future revocation or expiry signals without lifecycle, retry, or do-not-retry mutation.",
        snapshot_signal="A revocation or expiry signal must be visible as definition text only.",
        evidence_boundary="The signal cannot archive, stale, cleanup, delete, update lifecycle, mutate retry policy, or mutate do-not-retry state.",
        prohibited_semantics="No lifecycle mutation, retry policy mutation, proposal mutation, memory record update, memory record deletion, approval, rejection, or execution.",
        blocking_boundary="Lifecycle, retry, revocation, expiry, or deletion mutation behavior remains outside P4-M2.5.",
        future_precondition_note="A later path may inspect expiry evidence; P4-M2.5 mutates no lifecycle or retry policy.",
    ),
    ExecutionPreconditionsSnapshotMapField(
        field_order=14,
        field_id="audit-trace-reference",
        field_name="Audit Trace Reference",
        field_purpose="References future audit trace material without writing audit, provenance, confirmation, authorization, validation, readiness, or execution state.",
        snapshot_signal="An audit trace reference signal must be visible and stable.",
        evidence_boundary="Audit references remain textual and do not write provenance, mutate evidence, mutate citations, or create memory records.",
        prohibited_semantics="No provenance writing, evidence mutation, citation mutation, memory record creation, validation verdict, readiness verdict, confirmation, authorization, or execution.",
        blocking_boundary="Trace-derived writes, verdicts, confirmation, authorization, or execution behavior remains outside P4-M2.5.",
        future_precondition_note="A later path may compare audit traces; P4-M2.5 writes no trace state.",
    ),
    ExecutionPreconditionsSnapshotMapField(
        field_order=15,
        field_id="precondition-semantics-disabled",
        field_name="Precondition Semantics Disabled",
        field_purpose="Makes explicit that precondition map fields do not become live precondition checks.",
        snapshot_signal="A precondition-semantics-disabled signal must be visible.",
        evidence_boundary="Disabled precondition semantics keep the map definition-only and prevent live checks, verdicts, mutation, or execution.",
        prohibited_semantics="No live precondition validation, input validation, record validation, validation verdict, readiness verdict, or automatic readiness verdict.",
        blocking_boundary="Any precondition semantics beyond read-only definition text remain outside P4-M2.5.",
        future_precondition_note="A later path may define governed checks; P4-M2.5 defines no checks.",
    ),
    ExecutionPreconditionsSnapshotMapField(
        field_order=16,
        field_id="validation-semantics-disabled",
        field_name="Validation Semantics Disabled",
        field_purpose="Makes explicit that the map performs no live, input, record, confirmation, authorization, or contract validation.",
        snapshot_signal="A validation-semantics-disabled signal must be visible.",
        evidence_boundary="Disabled validation semantics prevent validation records, validation verdicts, readiness verdicts, evidence writes, or citation mutation.",
        prohibited_semantics="No live confirmation validation, live authorization validation, live contract validation, input validation, record validation, validation verdict, or readiness verdict.",
        blocking_boundary="Any validation semantics remain outside P4-M2.5.",
        future_precondition_note="A later path may define governed validation; P4-M2.5 validates nothing.",
    ),
    ExecutionPreconditionsSnapshotMapField(
        field_order=17,
        field_id="execution-semantics-disabled",
        field_name="Execution Semantics Disabled",
        field_purpose="Makes explicit that the map grants no execution semantics.",
        snapshot_signal="An execution-semantics-disabled signal must be visible.",
        evidence_boundary="Disabled execution semantics prevent execution, commands, deployment, UI, Operator Console, MVP, productization, v7, and full Memory Graph behavior.",
        prohibited_semantics="No execution, confirmation, authorization, approval, rejection, decision recommendation, decision ranking, API, MCP, connector, agent call, P4-M3, P4-M4, P4-M5, v7, productization, UI, Operator Console, MVP, deploy, or full Memory Graph.",
        blocking_boundary="Any execution or productization semantics remain outside P4-M2.5.",
        future_precondition_note="A later path may define governed execution preconditions; P4-M2.5 executes nothing.",
    ),
)


def list_execution_preconditions_snapshot_map_fields() -> tuple[
    ExecutionPreconditionsSnapshotMapField,
    ...,
]:
    return _EXECUTION_PRECONDITIONS_SNAPSHOT_MAP_FIELDS


def execution_preconditions_snapshot_map_field_ids() -> tuple[str, ...]:
    return tuple(
        field.field_id
        for field in list_execution_preconditions_snapshot_map_fields()
    )


def render_execution_preconditions_snapshot_map_markdown(
    fields: Sequence[ExecutionPreconditionsSnapshotMapField] | None = None,
) -> str:
    field_values = (
        tuple(fields)
        if fields is not None
        else list_execution_preconditions_snapshot_map_fields()
    )
    status = execution_preconditions_snapshot_map_report()
    lines = [
        "# P4-M2.5 Execution Preconditions Snapshot Map",
        "",
        "P4-M2.5 execution preconditions snapshot map only.",
        "",
        "Execution Preconditions Snapshot Map.",
        "",
        "Read-only.",
        "",
        "Inspection-only.",
        "",
        "Definition-only.",
        "",
        "P4-M2.1 Execution Surface Contract Definition remains a referenced definition layer.",
        "",
        "P4-M2.2 Execution Contract Validation Matrix remains a referenced definition layer.",
        "",
        "P4-M2.3 Manual Authorization Evidence Envelope remains a referenced definition layer.",
        "",
        "P4-M2.4 Human Confirmation Snapshot Contract remains a referenced definition layer.",
        "",
        "No execution.",
        "",
        "No confirmation.",
        "",
        "No authorization.",
        "",
        "No approval.",
        "",
        "No rejection.",
        "",
        "No memory mutation.",
        "",
        "No memory record creation.",
        "",
        "No memory record update.",
        "",
        "No memory record deletion.",
        "",
        "No proposal mutation.",
        "",
        "No lifecycle mutation.",
        "",
        "No retry policy mutation.",
        "",
        "No source fetching.",
        "",
        "No provenance writing.",
        "",
        "No evidence mutation.",
        "",
        "No citation mutation.",
        "",
        "No live confirmation validation.",
        "",
        "No live authorization validation.",
        "",
        "No live contract validation.",
        "",
        "No input validation.",
        "",
        "No record validation.",
        "",
        "No validation verdict.",
        "",
        "No readiness verdict.",
        "",
        "No automatic readiness verdict.",
        "",
        "No decision recommendation.",
        "",
        "No decision ranking.",
        "",
        "No confirmation semantics.",
        "",
        "No authorization semantics.",
        "",
        "No execution semantics.",
        "",
        "No API.",
        "",
        "No MCP.",
        "",
        "No connector.",
        "",
        "No agent call.",
        "",
        "No Codex/Hermes/ChatGPT product-code auto-call.",
        "",
        "No P4-M3.",
        "",
        "No P4-M4.",
        "",
        "No P4-M5.",
        "",
        "No v7.",
        "",
        "No productization.",
        "",
        "No UI.",
        "",
        "No Operator Console.",
        "",
        "No MVP.",
        "",
        "No deploy.",
        "",
        "No full Memory Graph.",
        "",
        EXECUTION_PRECONDITIONS_SNAPSHOT_MAP_BOUNDARY,
        "",
        "## Status Report",
        "",
    ]
    for key, value in status.items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Snapshot Map Fields", ""])
    for field in field_values:
        lines.extend(
            [
                f"### {field.field_order}. {field.field_id}",
                "",
                f"- Field name: {field.field_name}",
                f"- Field purpose: {field.field_purpose}",
                f"- Snapshot signal: {field.snapshot_signal}",
                f"- Evidence boundary: {field.evidence_boundary}",
                f"- Prohibited semantics: {field.prohibited_semantics}",
                f"- Blocking boundary: {field.blocking_boundary}",
                f"- Future precondition note: {field.future_precondition_note}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def execution_preconditions_snapshot_map_as_dicts(
    fields: Sequence[ExecutionPreconditionsSnapshotMapField] | None = None,
) -> tuple[dict[str, object], ...]:
    field_values = (
        tuple(fields)
        if fields is not None
        else list_execution_preconditions_snapshot_map_fields()
    )
    return tuple(asdict(field) for field in field_values)


def execution_preconditions_snapshot_map_report() -> dict[str, object]:
    return {
        "phase": "P4-M2.5",
        "feature": "Execution Preconditions Snapshot Map",
        "mode": "read-only",
        "definition_only": True,
        "inspection_only": True,
        "snapshot_map_field_count": len(_EXECUTION_PRECONDITIONS_SNAPSHOT_MAP_FIELDS),
        "p4_m2_started": True,
        "execution_surface_contract_definition_available": True,
        "execution_contract_validation_matrix_available": True,
        "manual_authorization_evidence_envelope_available": True,
        "human_confirmation_snapshot_contract_available": True,
        "execution_preconditions_snapshot_map_started": True,
        "execution_preconditions_snapshot_map_definition_only": True,
        "snapshot_map_fields_defined": True,
        "precondition_snapshot_structure_defined": True,
        "execution_enabled": False,
        "confirmation_enabled": False,
        "authorization_enabled": False,
        "approval_enabled": False,
        "rejection_enabled": False,
        "memory_mutation_enabled": False,
        "memory_record_creation_enabled": False,
        "memory_record_update_enabled": False,
        "memory_record_deletion_enabled": False,
        "proposal_mutation_enabled": False,
        "lifecycle_mutation_enabled": False,
        "retry_policy_mutation_enabled": False,
        "source_fetching_enabled": False,
        "provenance_writing_enabled": False,
        "evidence_mutation_enabled": False,
        "citation_mutation_enabled": False,
        "live_confirmation_validation_enabled": False,
        "live_authorization_validation_enabled": False,
        "live_contract_validation_enabled": False,
        "input_validation_enabled": False,
        "record_validation_enabled": False,
        "validation_verdict_enabled": False,
        "readiness_verdict_enabled": False,
        "automatic_readiness_verdict_enabled": False,
        "decision_recommendation_enabled": False,
        "decision_ranking_enabled": False,
        "confirmation_semantics_granted": False,
        "authorization_semantics_granted": False,
        "execution_semantics_granted": False,
        "api_enabled": False,
        "mcp_enabled": False,
        "connector_enabled": False,
        "agent_call_enabled": False,
        "codex_hermes_chatgpt_product_code_auto_call_enabled": False,
        "p4_m3_started": False,
        "p4_m4_started": False,
        "p4_m5_started": False,
        "v7_started": False,
        "productization_started": False,
        "ui_started": False,
        "operator_console_started": False,
        "mvp_started": False,
        "deploy_started": False,
        "full_memory_graph_started": False,
        "package_version": P4_M2_5_PACKAGE_VERSION,
        "boundary": EXECUTION_PRECONDITIONS_SNAPSHOT_MAP_BOUNDARY,
    }


if not execution_surface_contract_field_ids():
    raise RuntimeError("execution_surface_contract_definition_unavailable")

if not execution_contract_validation_matrix_field_ids():
    raise RuntimeError("execution_contract_validation_matrix_unavailable")

if not manual_authorization_evidence_envelope_field_ids():
    raise RuntimeError("manual_authorization_evidence_envelope_unavailable")

if not human_confirmation_snapshot_contract_field_ids():
    raise RuntimeError("human_confirmation_snapshot_contract_unavailable")
