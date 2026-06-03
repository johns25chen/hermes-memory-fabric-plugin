"""Read-only Civilization Core closed-loop evidence validation."""

from __future__ import annotations

import json
from typing import Any, Mapping


CLOSED_LOOP_EVIDENCE_VALIDATION_VERSION = "2.9.0"

REQUIRED_EVIDENCE: dict[str, tuple[str, ...]] = {
    "natural_language_task": (
        "task_text",
        "task_boundary",
        "human_operator_confirmed_boundary",
    ),
    "codex_cli_implementation": (
        "codex_cli_used",
        "repository_inspected",
        "files_changed",
        "change_summary",
        "codex_did_not_commit",
    ),
    "terminal_or_openclaw_validation": (
        "validation_commands",
        "validation_passed",
        "controlled_validation_only",
        "no_real_world_execution",
        "no_openclaw_autonomous_execution",
    ),
    "chatgpt_review": (
        "diff_reviewed",
        "tests_reviewed",
        "governance_boundaries_reviewed",
        "no_sensitive_output_exposed",
    ),
    "human_operator_decision": (
        "merge_decision_by_human",
        "human_final_authority",
    ),
    "github_record": (
        "pr_recorded",
        "commit_recorded",
    ),
}

TRUE_FIELDS = {
    "human_operator_confirmed_boundary",
    "codex_cli_used",
    "repository_inspected",
    "codex_did_not_commit",
    "validation_passed",
    "controlled_validation_only",
    "no_real_world_execution",
    "no_openclaw_autonomous_execution",
    "diff_reviewed",
    "tests_reviewed",
    "governance_boundaries_reviewed",
    "no_sensitive_output_exposed",
    "merge_decision_by_human",
    "human_final_authority",
    "pr_recorded",
    "commit_recorded",
}

NON_EMPTY_STRING_FIELDS = {"task_text", "task_boundary", "change_summary"}
NON_EMPTY_LIST_FIELDS = {"files_changed", "validation_commands"}

SENSITIVE_EXACT_KEYS = {
    "approval_phrase",
    "stdout",
    "stdout_tail",
    "stderr",
}
SENSITIVE_KEY_FRAGMENTS = (
    "token",
    "secret",
    "password",
    "credential",
    "api_key",
    "apikey",
    "raw_log",
    "raw_logs",
)


def build_closed_loop_evidence_validation(evidence: Mapping[str, Any]) -> dict[str, Any]:
    """Validate closed-loop evidence completeness without authorizing execution."""

    missing_evidence: list[str] = []
    blocking_reasons: list[str] = []
    required_actions: list[str] = []

    if not isinstance(evidence, Mapping):
        return _base_report(
            status="blocked",
            evidence_summary={},
            missing_evidence=["evidence"],
            blocking_reasons=["evidence_must_be_mapping"],
            required_actions=["provide_structured_evidence_payload"],
            sensitive_field_count=0,
        )

    evidence_summary = _build_evidence_summary(evidence)
    sensitive_field_count = _count_sensitive_keys(evidence)

    for category, required_fields in REQUIRED_EVIDENCE.items():
        section = evidence.get(category)
        if not isinstance(section, Mapping):
            missing_evidence.append(category)
            continue
        for field_name in required_fields:
            if not _field_is_valid(section, field_name):
                missing_evidence.append(f"{category}.{field_name}")

    if _release_intended(evidence) and not _tag_recorded(evidence):
        missing_evidence.append("github_record.tag_recorded")
        blocking_reasons.append("release_tag_record_required_when_release_intended")
        required_actions.append("record_release_tag_or_mark_release_not_intended")

    if missing_evidence:
        blocking_reasons.append("required_evidence_missing_or_incomplete")
        required_actions.append("provide_missing_closed_loop_evidence")

    if sensitive_field_count:
        blocking_reasons.append("unsafe_sensitive_evidence_present")
        required_actions.append("remove_sensitive_raw_evidence_before_validation")

    status = "blocked" if blocking_reasons else "closed_loop_evidence_ready"
    if status == "closed_loop_evidence_ready":
        required_actions.append("human_operator_may_review_evidence_no_authorization_granted")

    return _base_report(
        status=status,
        evidence_summary=evidence_summary,
        missing_evidence=missing_evidence,
        blocking_reasons=blocking_reasons,
        required_actions=required_actions,
        sensitive_field_count=sensitive_field_count,
    )


def closed_loop_evidence_validation_to_json(report: Mapping[str, Any]) -> str:
    return json.dumps(dict(report), ensure_ascii=True, indent=2, sort_keys=True) + "\n"


def _field_is_valid(section: Mapping[str, Any], field_name: str) -> bool:
    value = section.get(field_name)
    if field_name in TRUE_FIELDS:
        return value is True
    if field_name in NON_EMPTY_STRING_FIELDS:
        return isinstance(value, str) and bool(value.strip())
    if field_name in NON_EMPTY_LIST_FIELDS:
        return isinstance(value, list) and bool(value)
    return value is not None


def _release_intended(evidence: Mapping[str, Any]) -> bool:
    github_record = evidence.get("github_record")
    if isinstance(github_record, Mapping) and github_record.get("release_intended") is True:
        return True
    return evidence.get("release_intended") is True


def _tag_recorded(evidence: Mapping[str, Any]) -> bool:
    github_record = evidence.get("github_record")
    return isinstance(github_record, Mapping) and github_record.get("tag_recorded") is True


def _build_evidence_summary(evidence: Mapping[str, Any]) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "categories_present": sorted(
            category for category in REQUIRED_EVIDENCE if isinstance(evidence.get(category), Mapping)
        ),
        "release_intended": _release_intended(evidence),
        "tag_recorded": _tag_recorded(evidence),
    }
    for category in REQUIRED_EVIDENCE:
        section = evidence.get(category)
        if isinstance(section, Mapping):
            summary[category] = _summarize_section(section)
        else:
            summary[category] = {"present": False}
    return summary


def _summarize_section(section: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "present": True,
        "true_flag_count": sum(1 for value in section.values() if value is True),
        "non_empty_list_count": sum(
            1 for value in section.values() if isinstance(value, list) and bool(value)
        ),
        "non_empty_text_field_count": sum(
            1 for value in section.values() if isinstance(value, str) and bool(value.strip())
        ),
    }


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
    return key_text in SENSITIVE_EXACT_KEYS or any(
        fragment in key_text for fragment in SENSITIVE_KEY_FRAGMENTS
    )


def _base_report(
    *,
    status: str,
    evidence_summary: dict[str, Any],
    missing_evidence: list[str],
    blocking_reasons: list[str],
    required_actions: list[str],
    sensitive_field_count: int,
) -> dict[str, Any]:
    return {
        "version": CLOSED_LOOP_EVIDENCE_VALIDATION_VERSION,
        "status": status,
        "read_only": True,
        "read_only_memory": True,
        "would_mutate_memory": False,
        "invokes_openclaw": False,
        "writes_files": False,
        "would_call_github_api": False,
        "would_merge_pr": False,
        "would_create_tag": False,
        "evidence_summary": evidence_summary,
        "missing_evidence": missing_evidence,
        "blocking_reasons": blocking_reasons,
        "required_actions": required_actions,
        "sensitive_field_count": sensitive_field_count,
        "authorization_granted": False,
        "openclaw_execution_authorized": False,
    }


__all__ = [
    "CLOSED_LOOP_EVIDENCE_VALIDATION_VERSION",
    "build_closed_loop_evidence_validation",
    "closed_loop_evidence_validation_to_json",
]
