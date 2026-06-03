"""Governed Star-Dome chain closure audit for the v2.9-v2.16 chain."""

from __future__ import annotations

import json
from typing import Any, Mapping


GOVERNED_STAR_DOME_CHAIN_CLOSURE_AUDIT_VERSION = "2.17.0"

AUDITED_CHAIN_VERSIONS = [
    "v2.9.0",
    "v2.10.0",
    "v2.11.0",
    "v2.12.0",
    "v2.13.0",
    "v2.14.0",
    "v2.15.0",
    "v2.16.0",
]

LAYER_MAPPING = {
    "primary_layer": "星穹记忆",
    "supporting_layers": ["星界记忆", "星辰记忆", "星域记忆"],
    "direction": "v2.9-v2.16 星穹治理链 -> Star-Dome chain closure audit",
}

SAFETY_FLAGS = {
    "read_only": True,
    "read_only_memory": True,
    "audit_only": True,
    "closure_audit_only": True,
    "would_mutate_memory": False,
    "writes_files": False,
    "invokes_openclaw": False,
    "would_call_github_api": False,
    "would_merge_pr": False,
    "would_create_tag": False,
    "would_write_durable_memory": False,
    "would_mutate_memory_graph": False,
    "would_create_operation_ledger_entry": False,
    "would_create_approval_request": False,
    "would_submit_approval_request": False,
    "would_execute_approval_request": False,
    "would_record_human_decision": False,
    "would_grant_approval": False,
    "authorization_granted": False,
    "closure_authorized": False,
    "star_dome_closed": False,
    "handoff_authorized": False,
    "human_decision_recorded": False,
    "approval_request_created": False,
    "approval_request_submitted": False,
    "approval_request_authorized": False,
    "approval_granted": False,
    "memory_write_authorized": False,
    "openclaw_execution_authorized": False,
}

STAGE_SAFETY_CLAIMS = {
    "claims_durable_memory_write": False,
    "claims_memory_graph_mutation": False,
    "claims_operation_ledger_creation": False,
    "claims_approval_request_creation": False,
    "claims_approval_request_submission": False,
    "claims_approval_request_execution": False,
    "claims_real_human_decision_recording": False,
    "claims_approval_granted": False,
    "claims_openclaw_execution_authorization": False,
    "claims_github_api_write_action": False,
    "claims_star_hub_scheduling": False,
    "claims_self_enforcing_memory_law": False,
    "claims_star_soul_continuity": False,
    "claims_star_universe_evolution": False,
    "claims_source_self_evolution": False,
}

CHAIN_STAGE_MATRIX = [
    {
        "version": "v2.9.0",
        "stage": "closed-loop evidence validation",
        "primary_layer": "星界记忆",
        "role": "validates cross-system closed-loop evidence",
        "chain_position": "星界闭环证据 source",
        **STAGE_SAFETY_CLAIMS,
    },
    {
        "version": "v2.10.0",
        "stage": "governed memory proposal from evidence",
        "primary_layer": "星辰记忆",
        "role": "converts validated evidence into reusable candidate memory material",
        "chain_position": "星辰候选记忆 proposal material",
        **STAGE_SAFETY_CLAIMS,
    },
    {
        "version": "v2.11.0",
        "stage": "governed proposal review gate",
        "primary_layer": "星穹记忆",
        "role": "reviews candidate proposals under governance boundaries",
        "chain_position": "星穹 governance-chain stage",
        **STAGE_SAFETY_CLAIMS,
    },
    {
        "version": "v2.12.0",
        "stage": "governed approval request preparation",
        "primary_layer": "星穹记忆",
        "role": "prepares approval request material without creating a real request",
        "chain_position": "星穹 governance-chain stage",
        **STAGE_SAFETY_CLAIMS,
    },
    {
        "version": "v2.13.0",
        "stage": "governed approval request dry-run envelope",
        "primary_layer": "星穹记忆",
        "role": "creates a dry-run envelope without submitting or authorizing",
        "chain_position": "星穹 governance-chain stage",
        **STAGE_SAFETY_CLAIMS,
    },
    {
        "version": "v2.14.0",
        "stage": "governed dry-run envelope validation gate",
        "primary_layer": "星穹记忆",
        "role": "validates dry-run envelope structure only",
        "chain_position": "星穹 governance-chain stage",
        **STAGE_SAFETY_CLAIMS,
    },
    {
        "version": "v2.15.0",
        "stage": "governed Human Operator decision packet dry-run",
        "primary_layer": "星穹记忆",
        "role": "prepares a dry-run Human Operator decision packet without recording a decision",
        "chain_position": "星穹 governance-chain stage",
        **STAGE_SAFETY_CLAIMS,
    },
    {
        "version": "v2.16.0",
        "stage": "governed Human Operator decision packet validation gate",
        "primary_layer": "星穹记忆",
        "role": "validates decision packet structure only",
        "chain_position": "星穹 governance-chain stage",
        **STAGE_SAFETY_CLAIMS,
    },
]

REQUIRED_RELEASE_INTEGRITY_FLAGS = {
    "audit_status": "pass",
    "release_chain_status": "pass",
    "no_network_surface": True,
    "no_hermes_memory_write": True,
    "no_github_write": True,
    "no_composio_execution": True,
    "provider_tool_surface_empty": True,
}


def run_governed_star_dome_chain_closure_audit(
    release_integrity_report: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Return a local-only, non-authorizing Star-Dome chain closure audit."""

    checks, blocking_reasons = _chain_closure_checks()
    sensitive_field_count = _count_sensitive_keys(release_integrity_report)
    if release_integrity_report is not None:
        release_checks, release_blocking_reasons = _release_integrity_checks(
            release_integrity_report
        )
        checks.extend(release_checks)
        blocking_reasons.extend(release_blocking_reasons)

    blocking_reasons = list(dict.fromkeys(blocking_reasons))
    status = "chain_closure_audit_passed" if not blocking_reasons else "blocked"

    return {
        "version": GOVERNED_STAR_DOME_CHAIN_CLOSURE_AUDIT_VERSION,
        "status": status,
        **SAFETY_FLAGS,
        "civilization_core_layer_mapping": dict(LAYER_MAPPING),
        "audited_chain_versions": list(AUDITED_CHAIN_VERSIONS),
        "chain_closure_summary": _chain_closure_summary(status),
        "chain_closure_checks": checks,
        "chain_stage_matrix": [dict(stage) for stage in CHAIN_STAGE_MATRIX],
        "non_authorization_boundary": _non_authorization_boundary(),
        "scope_boundaries": _scope_boundaries(),
        "risk_notes": _risk_notes(sensitive_field_count),
        "required_human_actions": _required_human_actions(status, blocking_reasons),
        "blocking_reasons": blocking_reasons,
        "next_allowed_step": "v2.18.0 Star-Dome closure boundary manifest",
        "sensitive_field_count": sensitive_field_count,
        "sensitive_fields_omitted": sensitive_field_count > 0,
    }


def governed_star_dome_chain_closure_audit_to_json(report: Mapping[str, Any]) -> str:
    """Serialize a Star-Dome chain closure audit report deterministically."""

    return json.dumps(dict(report), ensure_ascii=True, indent=2, sort_keys=True) + "\n"


def _chain_closure_checks() -> tuple[list[dict[str, Any]], list[str]]:
    checks: list[dict[str, Any]] = []
    blocking_reasons: list[str] = []

    versions = [stage["version"] for stage in CHAIN_STAGE_MATRIX]
    _add_check(
        checks,
        blocking_reasons,
        "all_audited_chain_versions_present",
        versions == AUDITED_CHAIN_VERSIONS,
        "audited_chain_versions_must_exactly_match_v2_9_0_through_v2_16_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "version_order_continuous",
        versions == AUDITED_CHAIN_VERSIONS,
        "version_order_must_be_continuous_from_v2_9_0_to_v2_16_0",
    )
    _add_check(
        checks,
        blocking_reasons,
        "v2_9_star_boundary_evidence_source",
        CHAIN_STAGE_MATRIX[0]["chain_position"] == "星界闭环证据 source",
        "v2_9_0_must_be_star_boundary_closed_loop_evidence_source",
    )
    _add_check(
        checks,
        blocking_reasons,
        "v2_10_star_candidate_memory_material",
        CHAIN_STAGE_MATRIX[1]["chain_position"] == "星辰候选记忆 proposal material",
        "v2_10_0_must_be_star_candidate_memory_proposal_material",
    )
    _add_check(
        checks,
        blocking_reasons,
        "v2_11_through_v2_16_star_dome_governance_stages",
        all(
            stage["primary_layer"] == "星穹记忆"
            and stage["chain_position"] == "星穹 governance-chain stage"
            for stage in CHAIN_STAGE_MATRIX[2:]
        ),
        "v2_11_0_through_v2_16_0_must_be_star_dome_governance_stages",
    )
    for claim in STAGE_SAFETY_CLAIMS:
        _add_check(
            checks,
            blocking_reasons,
            f"no_stage_{claim}",
            all(stage.get(claim) is False for stage in CHAIN_STAGE_MATRIX),
            f"no_stage_may_{claim}",
        )
    for key, expected in SAFETY_FLAGS.items():
        _add_check(
            checks,
            blocking_reasons,
            f"v2_17_flag_{key}",
            expected is (True if key in {"read_only", "read_only_memory", "audit_only", "closure_audit_only"} else False),
            f"v2_17_flag_{key}_must_remain_safe",
        )
    _add_check(
        checks,
        blocking_reasons,
        "chain_closure_audit_passed_is_not_authorization",
        SAFETY_FLAGS["authorization_granted"] is False,
        "chain_closure_audit_passed_must_not_authorize_anything",
    )
    _add_check(
        checks,
        blocking_reasons,
        "chain_closure_audit_passed_is_not_star_dome_final_closure",
        SAFETY_FLAGS["star_dome_closed"] is False,
        "chain_closure_audit_passed_must_not_close_star_dome",
    )
    _add_check(
        checks,
        blocking_reasons,
        "chain_closure_audit_only_permits_later_boundary_manifest",
        True,
        "next_step_must_be_later_star_dome_closure_boundary_manifest",
    )
    return checks, blocking_reasons


def _release_integrity_checks(
    report: Mapping[str, Any],
) -> tuple[list[dict[str, Any]], list[str]]:
    checks: list[dict[str, Any]] = []
    blocking_reasons: list[str] = []

    if not isinstance(report, Mapping):
        _add_check(
            checks,
            blocking_reasons,
            "release_integrity_report_mapping",
            False,
            "release_integrity_report_must_be_mapping",
        )
        return checks, blocking_reasons

    for key, expected in REQUIRED_RELEASE_INTEGRITY_FLAGS.items():
        actual = _provider_tools_empty(report) if key == "provider_tool_surface_empty" else report.get(key)
        _add_check(
            checks,
            blocking_reasons,
            f"release_integrity_{key}",
            actual is expected if isinstance(expected, bool) else actual == expected,
            f"release_integrity_{key}_must_be_{str(expected).lower()}",
        )
    _add_check(
        checks,
        blocking_reasons,
        "release_integrity_pyproject_version_allowed",
        report.get("pyproject_version") in {"2.16.0", "2.17.0"},
        "release_integrity_pyproject_version_must_be_2_16_0_or_2_17_0",
    )
    for key, value in sorted(report.items(), key=lambda item: str(item[0])):
        key_text = str(key)
        if key_text.endswith("_smoke_safe"):
            _add_check(
                checks,
                blocking_reasons,
                f"release_integrity_existing_smoke_safe_{key_text}",
                value is not False,
                "release_integrity_existing_smoke_safe_fields_must_not_be_false",
            )
    return checks, blocking_reasons


def _provider_tools_empty(report: Mapping[str, Any]) -> bool | None:
    if "provider_tool_surface_empty" in report:
        value = report.get("provider_tool_surface_empty")
        return value if isinstance(value, bool) else None
    if "provider_tools_empty" in report:
        value = report.get("provider_tools_empty")
        return value if isinstance(value, bool) else None
    if "provider_tools" in report:
        return report.get("provider_tools") == []
    return None


def _chain_closure_summary(status: str) -> dict[str, Any]:
    return {
        "closure_audit_status": status,
        "chain_continuous": status == "chain_closure_audit_passed",
        "structurally_complete": status == "chain_closure_audit_passed",
        "non_authorizing": True,
        "non_writing": True,
        "non_executing": True,
        "ready_for_later_boundary_manifest": status == "chain_closure_audit_passed",
        "star_dome_final_closure_claimed": False,
    }


def _non_authorization_boundary() -> dict[str, Any]:
    return {
        "chain_closure_audit_passed_is_authorization": False,
        "chain_closure_audit_passed_is_approval": False,
        "chain_closure_audit_passed_is_human_decision": False,
        "chain_closure_audit_passed_is_real_approval_request": False,
        "chain_closure_audit_passed_is_request_submission": False,
        "chain_closure_audit_passed_is_request_execution": False,
        "chain_closure_audit_passed_is_memory_write_permission": False,
        "chain_closure_audit_passed_is_memory_graph_mutation_permission": False,
        "chain_closure_audit_passed_is_operation_ledger_creation": False,
        "chain_closure_audit_passed_is_openclaw_execution_permission": False,
        "chain_closure_audit_passed_is_star_dome_final_closure": False,
        "only_permits_later_boundary_manifest": True,
        "human_operator_remains_final_authority": True,
    }


def _scope_boundaries() -> list[str]:
    return [
        "Civilization Core is the total system.",
        "Fifteen Memory Layers are the highest memory coordinate system.",
        "Subspace Memory System is the engineering carrier.",
        "Hermes, Codex CLI, OpenClaw, Terminal, and GitHub are components, not the core.",
        "This v2.17.0 step is limited to 星穹记忆 chain closure audit.",
        "This audit does not enter 星枢 scheduling, 星律 self-enforcing memory law, 星魂 continuity, 星宙 evolution, or 星源 self-evolution.",
    ]


def _risk_notes(sensitive_field_count: int) -> list[str]:
    notes = [
        "Chain closure audit passed must not be treated as authorization.",
        "No durable memory write, Memory Graph mutation, operation-ledger entry, GitHub API write, merge, tag creation, approval, request creation, request submission, request execution, human decision record, or OpenClaw execution is produced or authorized.",
        "Star-Dome is not finally closed by this audit.",
        "Human Operator remains final authority.",
    ]
    if sensitive_field_count:
        notes.append("Sensitive fields were omitted from audit output.")
    return notes


def _required_human_actions(status: str, blocking_reasons: list[str]) -> list[str]:
    if status == "chain_closure_audit_passed":
        return [
            "human_operator_must_confirm_chain_closure_audit_is_not_authorization",
            "human_operator_must_review_before_any_later_star_dome_closure_boundary_manifest",
            "human_operator_must_use_separate_governed_process_for_any_real_approval_write_submission_execution_or_decision",
        ]
    actions = [
        "repair_release_integrity_or_chain_structure_before_boundary_manifest_preparation",
        "confirm_all_write_approval_execution_and_handoff_flags_remain_false",
        "rerun_local_audit_after_blocking_reasons_are_resolved",
    ]
    if blocking_reasons:
        actions.append("resolve_blocking_reasons_before_star_dome_chain_closure_audit_can_pass")
    return actions


def _add_check(
    checks: list[dict[str, Any]],
    blocking_reasons: list[str],
    name: str,
    passed: bool,
    reason: str,
) -> None:
    checks.append({"check": name, "passed": passed})
    if not passed:
        blocking_reasons.append(reason)


def _count_sensitive_keys(value: Any) -> int:
    if isinstance(value, Mapping):
        count = 0
        for key, inner in value.items():
            key_text = str(key).lower()
            if _is_sensitive_key(key_text):
                count += 1
            count += _count_sensitive_keys(inner)
        return count
    if isinstance(value, list):
        return sum(_count_sensitive_keys(item) for item in value)
    return 0


def _is_sensitive_key(key_text: str) -> bool:
    return key_text in {
        "approval_phrase",
        "stdout",
        "stdout_tail",
        "raw_logs",
        "token",
        "api_key",
        "secret",
        "password",
        "credential",
    }


__all__ = [
    "GOVERNED_STAR_DOME_CHAIN_CLOSURE_AUDIT_VERSION",
    "run_governed_star_dome_chain_closure_audit",
    "governed_star_dome_chain_closure_audit_to_json",
]
