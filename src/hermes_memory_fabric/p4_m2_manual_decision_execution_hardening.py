from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Sequence


P4_M2_0_PACKAGE_VERSION = "6.16.0"

MANUAL_EXECUTION_HARDENING_BOUNDARY = (
    "P4-M2.0 manual decision execution hardening only. "
    "P4-M2.0 is hardening contract only and read-only status surface only. "
    "P4-M2 hardening has started. Actual decision execution is disabled. "
    "Automatic decision execution is disabled. Manual execution command is disabled. "
    "Execute command is disabled. It does not recommend a decision. "
    "It does not rank decisions. It does not automatically determine readiness. "
    "It does not emit an automatic readiness verdict. It does not make decisions. "
    "It does not execute decisions. It does not approve memory. "
    "It does not reject memory. It does not approve proposals. "
    "It does not reject proposals. It does not write memory. "
    "It does not create memory records. It does not update memory records. "
    "It does not delete memory records. It does not mutate proposal records. "
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
class ManualExecutionHardeningRequirement:
    requirement_order: int
    requirement_id: str
    requirement_name: str
    hardening_purpose: str
    required_human_input: str
    required_precondition: str
    prohibited_automation: str
    audit_signal: str
    blocking_signal: str


_MANUAL_EXECUTION_HARDENING_REQUIREMENTS: tuple[
    ManualExecutionHardeningRequirement,
    ...,
] = (
    ManualExecutionHardeningRequirement(
        requirement_order=1,
        requirement_id="explicit-human-authorization-required",
        requirement_name="Explicit human authorization required",
        hardening_purpose="Require later manual execution paths to depend on explicit human authorization.",
        required_human_input="A human must provide explicit authorization in a later P4-M2.x path.",
        required_precondition="A later execution path must define the exact human authorization input before execution can be considered.",
        prohibited_automation="No automatic, inferred, checklist-derived, report-derived, or readiness-derived authorization.",
        audit_signal="Audit material must show the explicit human authorization input required by the later path.",
        blocking_signal="Missing explicit human authorization input or any inferred authorization blocks later execution consideration.",
    ),
    ManualExecutionHardeningRequirement(
        requirement_order=2,
        requirement_id="manual-decision-reference-required",
        requirement_name="Manual decision reference required",
        hardening_purpose="Require a later path to reference a human-selected decision or preview item.",
        required_human_input="A human must select the specific decision or preview item for any later path.",
        required_precondition="The selected item must be identified before any later manual execution path can be considered.",
        prohibited_automation="No automatic decision selection, preview selection, ranking selection, or inferred item reference.",
        audit_signal="Audit material must show the human-selected item reference required by the later path.",
        blocking_signal="Missing human-selected item reference or automatic item selection blocks later execution consideration.",
    ),
    ManualExecutionHardeningRequirement(
        requirement_order=3,
        requirement_id="execution-intent-must-be-explicit",
        requirement_name="Execution intent must be explicit",
        hardening_purpose="Separate inspect and preview behavior from any later execute intent.",
        required_human_input="A human must explicitly express execution intent in a later P4-M2.x path.",
        required_precondition="The later path must distinguish inspect, preview, and execute modes before execution can be considered.",
        prohibited_automation="No implicit execute intent from inspection, preview, status, report, or checklist output.",
        audit_signal="Audit material must show that execute intent is separate from inspect and preview output.",
        blocking_signal="Any ambiguity between inspect, preview, and execute intent blocks later execution consideration.",
    ),
    ManualExecutionHardeningRequirement(
        requirement_order=4,
        requirement_id="no-automatic-recommendation",
        requirement_name="No automatic recommendation",
        hardening_purpose="Prevent automatic recommendations from becoming execution input.",
        required_human_input="A human must not be replaced by automatic recommendation output.",
        required_precondition="Any later path must exclude automatic recommendations from execution input.",
        prohibited_automation="No decision recommendation, recommendation-derived selection, or recommendation-derived execution input.",
        audit_signal="Audit material must show that recommendation behavior is absent from execution input.",
        blocking_signal="Any automatic recommendation used as execution input blocks later execution consideration.",
    ),
    ManualExecutionHardeningRequirement(
        requirement_order=5,
        requirement_id="no-automatic-readiness-verdict",
        requirement_name="No automatic readiness verdict",
        hardening_purpose="Prevent automatic readiness verdicts from authorizing execution.",
        required_human_input="A human must not be replaced by an automatic readiness verdict.",
        required_precondition="Any later path must keep readiness inspection separate from authorization.",
        prohibited_automation="No automatic readiness verdict, mark-ready behavior, or readiness-derived authorization.",
        audit_signal="Audit material must show that no readiness verdict grants authorization or execution.",
        blocking_signal="Any automatic readiness verdict used for authorization blocks later execution consideration.",
    ),
    ManualExecutionHardeningRequirement(
        requirement_order=6,
        requirement_id="no-implicit-approval",
        requirement_name="No implicit approval",
        hardening_purpose="Prevent status, checklist, or report output from implying approval.",
        required_human_input="A human approval must not be inferred from any read-only output.",
        required_precondition="Any later path must require explicit approval semantics if approval is ever considered.",
        prohibited_automation="No inferred approval from status, checklist, report, preview, export, or audit output.",
        audit_signal="Audit material must show that read-only output does not approve memory or proposals.",
        blocking_signal="Any inferred approval blocks later execution consideration.",
    ),
    ManualExecutionHardeningRequirement(
        requirement_order=7,
        requirement_id="no-implicit-rejection",
        requirement_name="No implicit rejection",
        hardening_purpose="Prevent status, checklist, or report output from implying rejection.",
        required_human_input="A human rejection must not be inferred from any read-only output.",
        required_precondition="Any later path must require explicit rejection semantics if rejection is ever considered.",
        prohibited_automation="No inferred rejection from status, checklist, report, preview, export, or audit output.",
        audit_signal="Audit material must show that read-only output does not reject memory or proposals.",
        blocking_signal="Any inferred rejection blocks later execution consideration.",
    ),
    ManualExecutionHardeningRequirement(
        requirement_order=8,
        requirement_id="no-memory-write-in-p4-m2-0",
        requirement_name="No memory write in P4-M2.0",
        hardening_purpose="Keep P4-M2.0 contract/status output memory-write-free.",
        required_human_input="No human input in P4-M2.0 may write memory.",
        required_precondition="P4-M2.0 must remain a read-only status surface.",
        prohibited_automation="No memory write, memory creation, memory update, memory deletion, import, ingest, or injection.",
        audit_signal="Audit material must show memory write flags disabled and no storage created.",
        blocking_signal="Any P4-M2.0 memory write or memory record mutation violates the contract.",
    ),
    ManualExecutionHardeningRequirement(
        requirement_order=9,
        requirement_id="no-proposal-mutation-in-p4-m2-0",
        requirement_name="No proposal mutation in P4-M2.0",
        hardening_purpose="Keep P4-M2.0 contract/status output proposal-mutation-free.",
        required_human_input="No human input in P4-M2.0 may mutate proposals.",
        required_precondition="P4-M2.0 must not approve, reject, update, or mutate proposal records.",
        prohibited_automation="No proposal approval, rejection, update, mutation, lifecycle transition, or inferred proposal action.",
        audit_signal="Audit material must show proposal mutation flags disabled and no proposal files created.",
        blocking_signal="Any P4-M2.0 proposal mutation violates the contract.",
    ),
    ManualExecutionHardeningRequirement(
        requirement_order=10,
        requirement_id="no-lifecycle-mutation-in-p4-m2-0",
        requirement_name="No lifecycle mutation in P4-M2.0",
        hardening_purpose="Keep P4-M2.0 contract/status output lifecycle-mutation-free.",
        required_human_input="No human input in P4-M2.0 may mutate lifecycle state.",
        required_precondition="P4-M2.0 must not set, update, or mutate lifecycle records.",
        prohibited_automation="No lifecycle state mutation, lifecycle update, stale/archive/cleanup/delete behavior, or lifecycle-derived execution.",
        audit_signal="Audit material must show lifecycle mutation flags disabled and no lifecycle files created.",
        blocking_signal="Any P4-M2.0 lifecycle mutation violates the contract.",
    ),
    ManualExecutionHardeningRequirement(
        requirement_order=11,
        requirement_id="no-source-provenance-mutation-in-p4-m2-0",
        requirement_name="No source or provenance mutation in P4-M2.0",
        hardening_purpose="Keep P4-M2.0 contract/status output source and provenance mutation free.",
        required_human_input="No human input in P4-M2.0 may fetch, trust, write, or mutate sources or provenance.",
        required_precondition="P4-M2.0 must not touch source, provenance, evidence, or citation records.",
        prohibited_automation="No source fetch, browse, lookup, verification, trust, provenance write, or source/provenance/evidence/citation mutation.",
        audit_signal="Audit material must show source/provenance mutation flags disabled and no source/provenance files created.",
        blocking_signal="Any P4-M2.0 source, provenance, evidence, or citation mutation violates the contract.",
    ),
    ManualExecutionHardeningRequirement(
        requirement_order=12,
        requirement_id="no-api-mcp-connector-execution",
        requirement_name="No API, MCP, or connector execution",
        hardening_purpose="Prevent API, MCP, and connector behavior from executing decisions.",
        required_human_input="No human input in P4-M2.0 may trigger API, MCP, connector, or execution behavior.",
        required_precondition="P4-M2.0 must not add API, MCP, connector, or execution behavior.",
        prohibited_automation="No API, MCP, connector, external call, source call, decision execution, or connector-backed execution.",
        audit_signal="Audit material must show API/MCP/connector behavior disabled.",
        blocking_signal="Any API, MCP, connector, or execution behavior violates the contract.",
    ),
    ManualExecutionHardeningRequirement(
        requirement_order=13,
        requirement_id="no-agent-auto-call",
        requirement_name="No agent automatic call",
        hardening_purpose="Prevent product code from automatically calling agents.",
        required_human_input="No human input in P4-M2.0 may trigger automatic agent calls.",
        required_precondition="P4-M2.0 must not call Codex, Hermes, ChatGPT, or any agent from product code.",
        prohibited_automation="No automatic agent call, memory injection into agents, Codex call, Hermes call, ChatGPT call, or agent-mediated execution.",
        audit_signal="Audit material must show agent calls and memory injection disabled.",
        blocking_signal="Any automatic agent call or memory injection violates the contract.",
    ),
    ManualExecutionHardeningRequirement(
        requirement_order=14,
        requirement_id="audit-trail-required-for-future-execution",
        requirement_name="Audit trail required for future execution",
        hardening_purpose="Require any later manual execution path to be audit-traceable.",
        required_human_input="A human must be able to inspect the audit trail required by a later path.",
        required_precondition="A later path must define audit signals before manual execution can be considered.",
        prohibited_automation="No untraceable execution, hidden execution, implicit authorization, or mutation without audit material.",
        audit_signal="Audit material must identify the future trace requirements without writing P4-M2.0 state.",
        blocking_signal="Missing audit trace requirements block later execution consideration.",
    ),
    ManualExecutionHardeningRequirement(
        requirement_order=15,
        requirement_id="p4-m2-hardening-not-execution",
        requirement_name="P4-M2 hardening is not execution",
        hardening_purpose="State that P4-M2.0 starts hardening only, not actual decision execution.",
        required_human_input="A human-authorized route selected P4-M2.x hardening, not P4-M2.0 execution.",
        required_precondition="P4-M2.0 must remain a read-only contract/status surface only.",
        prohibited_automation="No actual execution, automatic execution, manual execution command, execute command, authorization semantics, or execution semantics.",
        audit_signal="Audit material must show hardening started and all execution semantics disabled.",
        blocking_signal="Any actual execution, command creation, authorization semantics, or execution semantics violates the contract.",
    ),
)


def list_manual_execution_hardening_requirements() -> tuple[
    ManualExecutionHardeningRequirement,
    ...,
]:
    return _MANUAL_EXECUTION_HARDENING_REQUIREMENTS


def manual_execution_hardening_requirement_ids() -> tuple[str, ...]:
    return tuple(
        requirement.requirement_id
        for requirement in list_manual_execution_hardening_requirements()
    )


def render_manual_execution_hardening_markdown(
    requirements: Sequence[ManualExecutionHardeningRequirement] | None = None,
) -> str:
    requirement_values = (
        tuple(requirements)
        if requirements is not None
        else list_manual_execution_hardening_requirements()
    )
    status = manual_execution_hardening_report()
    lines = [
        "# P4-M2.0 Manual Decision Execution Hardening",
        "",
        "P4-M2.0 manual decision execution hardening boundary.",
        "",
        "Hardening contract only.",
        "",
        "Read-only status surface only.",
        "",
        "P4-M2 hardening has started.",
        "",
        "Actual decision execution is disabled.",
        "",
        "Automatic decision execution is disabled.",
        "",
        "Manual execution command is disabled.",
        "",
        "Execute command is disabled.",
        "",
        "No decision recommendation is performed by this hardening contract.",
        "",
        "No decision ranking is performed by this hardening contract.",
        "",
        "No automatic readiness verdict is performed by this hardening contract.",
        "",
        "No decision execution is performed by this hardening contract.",
        "",
        "No approval or rejection is performed by this hardening contract.",
        "",
        "No memory writing is performed by this hardening contract.",
        "",
        "No proposal mutation is performed by this hardening contract.",
        "",
        "No lifecycle mutation is performed by this hardening contract.",
        "",
        "No do-not-retry mutation is performed by this hardening contract.",
        "",
        "No source/provenance mutation is performed by this hardening contract.",
        "",
        "No API/MCP/connector behavior is performed by this hardening contract.",
        "",
        "No authorization semantics are granted by this hardening contract.",
        "",
        "No execution semantics are granted by this hardening contract.",
        "",
        MANUAL_EXECUTION_HARDENING_BOUNDARY,
        "",
        "## Status Report",
        "",
    ]
    for key, value in status.items():
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Hardening Requirements", ""])
    for requirement in requirement_values:
        lines.extend(
            [
                f"### {requirement.requirement_order}. {requirement.requirement_id}",
                "",
                f"- Requirement name: {requirement.requirement_name}",
                f"- Hardening purpose: {requirement.hardening_purpose}",
                f"- Required human input: {requirement.required_human_input}",
                f"- Required precondition: {requirement.required_precondition}",
                f"- Prohibited automation: {requirement.prohibited_automation}",
                f"- Audit signal: {requirement.audit_signal}",
                f"- Blocking signal: {requirement.blocking_signal}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def manual_execution_hardening_as_dicts(
    requirements: Sequence[ManualExecutionHardeningRequirement] | None = None,
) -> tuple[dict[str, object], ...]:
    requirement_values = (
        tuple(requirements)
        if requirements is not None
        else list_manual_execution_hardening_requirements()
    )
    return tuple(asdict(requirement) for requirement in requirement_values)


def manual_execution_hardening_report() -> dict[str, object]:
    return {
        "phase": "P4-M2.0",
        "feature": "Manual Decision Execution Hardening",
        "mode": "read-only",
        "hardening_requirement_count": len(_MANUAL_EXECUTION_HARDENING_REQUIREMENTS),
        "p4_m2_started": True,
        "manual_decision_execution_hardening_started": True,
        "manual_execution_contract_only": True,
        "actual_decision_execution_enabled": False,
        "automatic_decision_execution_enabled": False,
        "manual_execution_command_enabled": False,
        "execute_command_enabled": False,
        "approval_enabled": False,
        "rejection_enabled": False,
        "automatic_decision_recommendation_enabled": False,
        "decision_ranking_enabled": False,
        "automatic_readiness_verdict_enabled": False,
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
        "authorization_semantics_granted": False,
        "execution_semantics_granted": False,
        "package_version": P4_M2_0_PACKAGE_VERSION,
        "boundary": MANUAL_EXECUTION_HARDENING_BOUNDARY,
    }
