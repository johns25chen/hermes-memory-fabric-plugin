"""Governed memory proposal generation from closed-loop evidence."""

from __future__ import annotations

import json
from typing import Any, Mapping


GOVERNED_MEMORY_PROPOSAL_FROM_EVIDENCE_VERSION = "2.10.0"

SENSITIVE_EXACT_KEYS = {
    "approval_phrase",
    "stdout",
    "stdout_tail",
    "raw_logs",
}
SENSITIVE_KEY_FRAGMENTS = (
    "token",
    "secret",
    "password",
    "credential",
    "api_key",
    "apikey",
)

LAYER_MAPPING = {
    "primary_layer": "星辰记忆",
    "supporting_layers": ["星域记忆", "星穹记忆", "星界记忆"],
    "direction": "星界闭环证据 -> 星辰候选记忆提案",
}

SAFETY_FLAGS = {
    "read_only": True,
    "read_only_memory": True,
    "would_mutate_memory": False,
    "writes_files": False,
    "invokes_openclaw": False,
    "would_call_github_api": False,
    "would_merge_pr": False,
    "would_create_tag": False,
    "would_write_durable_memory": False,
    "would_mutate_memory_graph": False,
    "would_create_operation_ledger_entry": False,
    "authorization_granted": False,
    "memory_write_authorized": False,
    "openclaw_execution_authorized": False,
}


def build_governed_memory_proposal_from_evidence(
    evidence_validation: Mapping[str, Any],
) -> dict[str, Any]:
    """Convert validated closed-loop evidence into governed candidate material only."""

    if not isinstance(evidence_validation, Mapping):
        return _base_report(
            status="blocked",
            proposal_summary="Input must be a structured closed-loop evidence validation report.",
            candidate_memories=[],
            blocking_reasons=["evidence_validation_must_be_mapping"],
            required_review_actions=["provide_closed_loop_evidence_validation_report"],
            sensitive_field_count=0,
        )

    sensitive_field_count = _count_sensitive_keys(evidence_validation)
    validation_status = evidence_validation.get("status")
    if validation_status != "closed_loop_evidence_ready":
        return _base_report(
            status="blocked",
            proposal_summary=(
                "Closed-loop evidence is not ready; governed candidate memory proposal "
                "generation remains blocked."
            ),
            candidate_memories=[],
            blocking_reasons=_blocked_reasons(evidence_validation),
            required_review_actions=_blocked_review_actions(evidence_validation),
            sensitive_field_count=sensitive_field_count,
        )

    evidence_summary = _safe_evidence_summary(evidence_validation)
    candidate_memories = _build_candidate_memories(evidence_summary)
    return _base_report(
        status="proposal_ready",
        proposal_summary=(
            "Validated closed-loop evidence was converted into governed candidate memory "
            "proposal material for human review only."
        ),
        candidate_memories=candidate_memories,
        blocking_reasons=[],
        required_review_actions=[
            "human_operator_review_required_before_any_memory_write",
            "confirm_candidate_scope_before_durable_memory_proposal",
            "confirm_no_openclaw_execution_is_authorized_by_this_report",
        ],
        sensitive_field_count=sensitive_field_count,
    )


def governed_memory_proposal_from_evidence_to_json(report: Mapping[str, Any]) -> str:
    """Serialize a governed memory proposal report deterministically."""

    return json.dumps(dict(report), ensure_ascii=True, indent=2, sort_keys=True) + "\n"


def _base_report(
    *,
    status: str,
    proposal_summary: str,
    candidate_memories: list[dict[str, Any]],
    blocking_reasons: list[str],
    required_review_actions: list[str],
    sensitive_field_count: int,
) -> dict[str, Any]:
    return {
        "version": GOVERNED_MEMORY_PROPOSAL_FROM_EVIDENCE_VERSION,
        "status": status,
        **SAFETY_FLAGS,
        "civilization_core_layer_mapping": dict(LAYER_MAPPING),
        "proposal_summary": proposal_summary,
        "candidate_memories": candidate_memories,
        "scope_boundaries": [
            "Civilization Core is the total system; this report is only Subspace Memory System candidate material.",
            "Hermes, Codex CLI, OpenClaw, Terminal, and GitHub remain components, not the core.",
            "Proposal generation is not authorization, approval, execution scheduling, or durable memory write.",
            "Human Operator remains final authority.",
        ],
        "risk_notes": [
            "Do not treat closed-loop evidence conversion as memory write approval.",
            "Do not mutate Memory Graph or create operation-ledger entries from this report.",
            "Do not infer OpenClaw execution permission from proposal readiness.",
            "Sensitive fields, if present in input, were omitted from candidate material.",
        ],
        "required_review_actions": required_review_actions,
        "blocking_reasons": blocking_reasons,
        "sensitive_field_count": sensitive_field_count,
    }


def _build_candidate_memories(evidence_summary: Mapping[str, Any]) -> list[dict[str, Any]]:
    candidates = [
        _candidate(
            candidate_id="star-memory-closed-loop-workflow-methodology",
            title="Closed-loop workflow methodology",
            summary=(
                "A natural-language task, Codex CLI implementation, controlled validation, "
                "ChatGPT review, human decision, and repository record formed a complete "
                "reviewable workflow pattern."
            ),
            evidence_basis=_evidence_basis(
                evidence_summary,
                ("natural_language_task", "codex_cli_implementation", "terminal_or_openclaw_validation"),
            ),
            scope="Methodology candidate for future human-reviewed closed-loop work.",
        ),
        _candidate(
            candidate_id="star-memory-role-and-boundary-mapping",
            title="Role and boundary mapping",
            summary=(
                "The evidence pattern keeps Civilization Core as the total system, the Fifteen "
                "Memory Layers as the highest memory coordinate system, and implementation "
                "surfaces as bounded components."
            ),
            evidence_basis=_evidence_basis(
                evidence_summary,
                ("natural_language_task", "chatgpt_review", "human_operator_decision"),
            ),
            scope="Boundary candidate for governance review only.",
        ),
        _candidate(
            candidate_id="star-memory-validation-evidence-pattern",
            title="Validation evidence pattern",
            summary=(
                "Controlled local validation evidence can support a candidate memory proposal "
                "when it remains read-only and does not authorize execution."
            ),
            evidence_basis=_evidence_basis(
                evidence_summary,
                ("terminal_or_openclaw_validation", "chatgpt_review"),
            ),
            scope="Validation pattern candidate for human review.",
        ),
    ]
    if _github_record_present(evidence_summary):
        candidates.append(
            _candidate(
                candidate_id="star-memory-release-or-pr-evidence-pattern",
                title="Release or PR evidence pattern",
                summary=(
                    "Repository record evidence was present as part of the closed-loop proof, "
                    "supporting a candidate release or PR evidence pattern without calling "
                    "GitHub APIs or creating tags."
                ),
                evidence_basis=_evidence_basis(evidence_summary, ("github_record",)),
                scope="Release or PR record pattern candidate for human review.",
            )
        )
    return candidates


def _candidate(
    *,
    candidate_id: str,
    title: str,
    summary: str,
    evidence_basis: dict[str, Any],
    scope: str,
) -> dict[str, Any]:
    return {
        "candidate_id": candidate_id,
        "memory_layer": "星辰记忆",
        "title": title,
        "summary": summary,
        "evidence_basis": evidence_basis,
        "scope": scope,
        "risks": [
            "candidate_must_not_be_treated_as_durable_memory",
            "candidate_must_not_authorize_openclaw_execution",
        ],
        "required_review": [
            "human_operator_review",
            "governance_boundary_review",
            "sensitive_output_absence_review",
        ],
    }


def _evidence_basis(evidence_summary: Mapping[str, Any], categories: tuple[str, ...]) -> dict[str, Any]:
    return {
        "source": "closed_loop_evidence_validation.evidence_summary",
        "categories": [
            {
                "category": category,
                "present": _section_present(evidence_summary, category),
                "true_flag_count": _safe_int(evidence_summary, category, "true_flag_count"),
                "non_empty_list_count": _safe_int(evidence_summary, category, "non_empty_list_count"),
                "non_empty_text_field_count": _safe_int(
                    evidence_summary,
                    category,
                    "non_empty_text_field_count",
                ),
            }
            for category in categories
        ],
    }


def _safe_evidence_summary(evidence_validation: Mapping[str, Any]) -> Mapping[str, Any]:
    evidence_summary = evidence_validation.get("evidence_summary")
    return evidence_summary if isinstance(evidence_summary, Mapping) else {}


def _github_record_present(evidence_summary: Mapping[str, Any]) -> bool:
    return _section_present(evidence_summary, "github_record")


def _section_present(evidence_summary: Mapping[str, Any], category: str) -> bool:
    section = evidence_summary.get(category)
    return isinstance(section, Mapping) and section.get("present") is True


def _safe_int(evidence_summary: Mapping[str, Any], category: str, key: str) -> int:
    section = evidence_summary.get(category)
    if not isinstance(section, Mapping):
        return 0
    value = section.get(key)
    return value if isinstance(value, int) and not isinstance(value, bool) else 0


def _blocked_reasons(evidence_validation: Mapping[str, Any]) -> list[str]:
    reasons = _safe_text_list(evidence_validation.get("blocking_reasons"))
    if not reasons:
        reasons = ["closed_loop_evidence_not_ready"]
    return reasons


def _blocked_review_actions(evidence_validation: Mapping[str, Any]) -> list[str]:
    actions = _safe_text_list(evidence_validation.get("required_actions"))
    if not actions:
        actions = ["complete_closed_loop_evidence_validation_before_proposal_generation"]
    actions.append("human_operator_review_required_no_authorization_granted")
    return list(dict.fromkeys(actions))


def _safe_text_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    safe_items: list[str] = []
    for item in value:
        if isinstance(item, str) and item.strip() and not _contains_sensitive_text(item):
            safe_items.append(item.strip())
    return safe_items


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


def _contains_sensitive_text(value: str) -> bool:
    lowered = value.lower()
    return _is_sensitive_key(lowered)


def _is_sensitive_key(key_text: str) -> bool:
    return key_text in SENSITIVE_EXACT_KEYS or any(
        fragment in key_text for fragment in SENSITIVE_KEY_FRAGMENTS
    )


__all__ = [
    "GOVERNED_MEMORY_PROPOSAL_FROM_EVIDENCE_VERSION",
    "build_governed_memory_proposal_from_evidence",
    "governed_memory_proposal_from_evidence_to_json",
]
