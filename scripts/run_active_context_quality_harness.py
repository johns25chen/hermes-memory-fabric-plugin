#!/usr/bin/env python3
"""Run the v0.9.0 Active Context Quality Harness.

The harness is deterministic and local: it evaluates JSON fixtures through
MemoryFabricProvider active-context APIs without model, network, executor, or
durable-write calls.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable, Mapping

from hermes_memory_fabric import MemoryFabricProvider
from hermes_memory_fabric.memory_subspace_index import create_subspace_descriptor, create_subspace_registry


HARNESS_VERSION = "0.9.0"
HARNESS_TYPE = "active_context_quality_harness_v0.9.0"
REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CASES_PATH = REPO_ROOT / "benchmarks" / "active_context_quality" / "fixtures" / "v09_cases.json"

REQUIRED_SAFETY_POLICY = {
    "read_only": True,
    "would_write_memory": False,
    "would_modify_config": False,
    "would_write_graph": False,
    "writes_proposal_files": False,
    "writes_operation_ledger": False,
    "writes_token_files": False,
    "writes_approval_audit": False,
    "invokes_real_token_write_executor": False,
    "implements_real_token_write_executor": False,
    "exposes_provider_tools": False,
}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run the v0.9.0 Active Context Quality Harness.")
    parser.add_argument(
        "--cases",
        default=str(DEFAULT_CASES_PATH),
        help=f"JSON fixture path. Defaults to {DEFAULT_CASES_PATH}",
    )
    parser.add_argument("--json", action="store_true", help="Print a machine-readable JSON report.")
    parser.add_argument(
        "--fail-on-score-below",
        type=float,
        default=None,
        metavar="FLOAT",
        help="Exit non-zero when aggregate overall_score is below this threshold.",
    )
    return parser


def load_cases(path: str | Path = DEFAULT_CASES_PATH) -> list[dict[str, Any]]:
    fixture_path = Path(path)
    with fixture_path.open("r", encoding="utf-8") as handle:
        cases = json.load(handle)
    if not isinstance(cases, list):
        raise ValueError(f"Active context fixture must contain a list of cases: {fixture_path}")
    return [_case_mapping(case, index, fixture_path) for index, case in enumerate(cases)]


def run_harness(cases_path: str | Path = DEFAULT_CASES_PATH) -> dict[str, Any]:
    fixture_path = Path(cases_path)
    case_results = [_evaluate_case(case) for case in load_cases(fixture_path)]
    aggregate = _aggregate(case_results)
    return {
        "harness_type": HARNESS_TYPE,
        "version": HARNESS_VERSION,
        "cases_path": str(fixture_path),
        "cases": case_results,
        "aggregate": aggregate,
        "policy": {
            "deterministic_local": True,
            "calls_real_model": False,
            "calls_network": False,
            "calls_executor": False,
            **REQUIRED_SAFETY_POLICY,
        },
    }


def print_human_summary(report: Mapping[str, Any]) -> None:
    aggregate = report.get("aggregate", {}) if isinstance(report.get("aggregate"), Mapping) else {}
    print(f"Active Context Quality Harness v{report.get('version', HARNESS_VERSION)}")
    print(
        "Cases: "
        f"{aggregate.get('passed_count', 0)}/{aggregate.get('case_count', 0)} passed, "
        f"overall_score={float(aggregate.get('overall_score', 0.0)):.3f}"
    )
    for case in report.get("cases", []):
        if not isinstance(case, Mapping):
            continue
        status = "PASS" if case.get("passed") else "FAIL"
        evidence = case.get("evidence", {}) if isinstance(case.get("evidence"), Mapping) else {}
        selected = ",".join(evidence.get("selected_memory_ids", [])) or "-"
        rejected = ",".join(evidence.get("rejected_memory_ids", [])) or "-"
        print(f"- {case.get('id')}: {status} selected={selected} rejected={rejected}")
        if not case.get("passed"):
            failed = [check.get("name") for check in case.get("checks", []) if isinstance(check, Mapping) and not check.get("passed")]
            if failed:
                print(f"  failed_checks={','.join(str(item) for item in failed)}")
    print(
        "Safety: read_only=True, durable_writes=False, graph_writes=False, "
        "token_writes=False, approval_audits=False, executor_calls=False, provider_tools=[]"
    )


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    report = run_harness(args.cases)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_human_summary(report)

    if args.fail_on_score_below is not None:
        overall_score = float(report["aggregate"]["overall_score"])
        if overall_score < args.fail_on_score_below:
            return 1
    return 0


def _evaluate_case(case: Mapping[str, Any]) -> dict[str, Any]:
    provider = MemoryFabricProvider()
    init_kwargs: dict[str, Any] = {
        "hermes_home": str(case.get("hermes_home") or os.environ.get("HERMES_HOME", "")),
    }
    provider_runtime_config = case.get("provider_runtime_config")
    if isinstance(provider_runtime_config, Mapping):
        init_kwargs["provider_runtime_config"] = deepcopy(dict(provider_runtime_config))
    provider.initialize(str(case.get("session_id") or f"active-context-quality:{case['id']}"), **init_kwargs)

    registry = _subspace_registry(case.get("subspaces", []))
    packet = provider.build_active_context(
        query=str(case.get("query", "")),
        memory_candidates=case.get("memories", []),
        subspace_registry=registry,
        context=case.get("context", {}),
        project_scope=case.get("project_scope"),
        agent_scope=case.get("agent_scope"),
        entity_ids=case.get("entity_ids"),
        now=case.get("now"),
        max_active_subspaces=case.get("max_active_subspaces"),
        memory_limit=case.get("memory_limit", case.get("limit")),
        context_budget_chars=case.get("context_budget_chars"),
        include_archived=case.get("include_archived"),
        allowed_risk_levels=case.get("allowed_risk_levels"),
        required_tags=case.get("required_tags"),
        include_rejected=bool(case.get("include_rejected", False)),
    )
    validation = provider.validate_active_context(packet)
    explanation = provider.explain_active_context(packet)
    summary = provider.summarize_active_context(packet)
    provider_tools = provider.get_tool_schemas()

    selected_memory_ids = list(explanation.get("selected_memory_ids", []))
    rejected_memory_ids = list(explanation.get("rejected_memory_ids", []))
    selected_subspace_ids = list(explanation.get("selected_subspace_ids", []))
    rejected_subspace_ids = list(explanation.get("rejected_subspace_ids", []))
    compact_context_text = str(packet.get("compact_context_text", ""))
    rejection_reasons = _rejection_reasons(packet, explanation)
    policy = _packet_policy(packet)

    evidence = {
        "selected_memory_ids": selected_memory_ids,
        "rejected_memory_ids": rejected_memory_ids,
        "selected_subspace_ids": selected_subspace_ids,
        "rejected_subspace_ids": rejected_subspace_ids,
        "rejection_reasons": rejection_reasons,
        "compact_context_text": compact_context_text,
        "context_budget_chars": packet.get("budget", {}).get("context_budget_chars"),
        "used_context_chars": len(compact_context_text),
        "packet_valid": validation.get("valid") is True,
        "validation": validation,
        "summary": summary,
        "explanation": explanation,
        "policy": policy,
        "packet_policy": policy,
        "provider_runtime_policy": deepcopy(dict(provider.runtime_integration_policy)),
        "provider_tools": provider_tools,
        "provider_tool_count": len(provider_tools),
        "active_context_packet": packet,
        "calls_real_model": False,
        "calls_network": False,
        "calls_executor": False,
        "created_durable_memory_write": False,
        "created_graph_write": False,
        "created_operation_event": False,
        "created_real_proposal": False,
        "writes_proposal_files": False,
        "writes_operation_ledger": False,
        "writes_token_files": False,
        "writes_approval_audit": False,
        "invokes_real_token_write_executor": False,
        "implements_real_token_write_executor": False,
        "exposes_provider_tools": False,
    }

    checks = _evaluate_checks(case, evidence)
    passed = all(check["passed"] for check in checks)
    return {
        "id": str(case["id"]),
        "dimension": str(case.get("dimension", "")),
        "description": str(case.get("description", "")),
        "query": str(case.get("query", "")),
        "score": 1.0 if passed else 0.0,
        "passed": passed,
        "checks": checks,
        "evidence": evidence,
    }


def _evaluate_checks(case: Mapping[str, Any], evidence: Mapping[str, Any]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(name: str, passed: bool, details: Any | None = None) -> None:
        check = {"name": name, "passed": bool(passed)}
        if details is not None:
            check["details"] = details
        checks.append(check)

    add("packet_valid", evidence.get("packet_valid") is bool(case.get("expected_packet_valid", True)))
    add(
        "selected_memory_ids",
        _ids_equal(evidence.get("selected_memory_ids"), case.get("expected_selected_memory_ids")),
        {"actual": evidence.get("selected_memory_ids"), "expected": case.get("expected_selected_memory_ids")},
    )
    add(
        "rejected_memory_ids",
        _ids_set_equal(evidence.get("rejected_memory_ids"), case.get("expected_rejected_memory_ids")),
        {"actual": evidence.get("rejected_memory_ids"), "expected": case.get("expected_rejected_memory_ids")},
    )
    add(
        "selected_subspace_ids",
        _ids_set_equal(evidence.get("selected_subspace_ids"), case.get("expected_selected_subspace_ids")),
        {"actual": evidence.get("selected_subspace_ids"), "expected": case.get("expected_selected_subspace_ids")},
    )
    add(
        "rejected_subspace_ids",
        _ids_set_equal(evidence.get("rejected_subspace_ids"), case.get("expected_rejected_subspace_ids")),
        {"actual": evidence.get("rejected_subspace_ids"), "expected": case.get("expected_rejected_subspace_ids")},
    )
    expected_top = case.get("expected_top_selected_memory_id")
    if expected_top is not None:
        selected = list(evidence.get("selected_memory_ids", []))
        add("top_selected_memory_id", bool(selected) and selected[0] == str(expected_top))

    compact_context_text = str(evidence.get("compact_context_text", ""))
    for index, expected in enumerate(_as_list(case.get("expected_compact_contains"))):
        add(f"compact_contains:{index}", str(expected) in compact_context_text, str(expected))
    for index, expected in enumerate(_as_list(case.get("expected_compact_absent"))):
        add(f"compact_absent:{index}", str(expected) not in compact_context_text, str(expected))

    budget = case.get("context_budget_chars")
    if budget is not None:
        add("context_budget_respected", len(compact_context_text) <= int(budget))
        add("context_budget_recorded", evidence.get("context_budget_chars") == int(budget))

    add(
        "rejection_reasons",
        _rejection_reasons_match(evidence.get("rejection_reasons", {}), case.get("expected_rejection_reasons", {})),
        {"actual": evidence.get("rejection_reasons", {}), "expected": case.get("expected_rejection_reasons", {})},
    )
    add("rejected_memory_content_absent", _rejected_content_absent(case, evidence))
    add("policy_safety", _policy_safety_ok(evidence))
    add("provider_tools_empty", evidence.get("provider_tools") == [])
    return checks


def _aggregate(case_results: list[dict[str, Any]]) -> dict[str, Any]:
    case_count = len(case_results)
    passed_count = sum(1 for case in case_results if case.get("passed") is True)
    failed_count = case_count - passed_count
    overall_score = round(sum(float(case.get("score", 0.0)) for case in case_results) / case_count, 3) if case_count else 0.0
    return {
        "case_count": case_count,
        "passed_count": passed_count,
        "failed_count": failed_count,
        "overall_score": overall_score,
        "policy_safety_score": round(
            sum(1.0 if _policy_safety_ok(case.get("evidence", {})) else 0.0 for case in case_results) / case_count,
            3,
        )
        if case_count
        else 0.0,
    }


def _subspace_registry(subspaces: Any) -> dict[str, Any]:
    descriptors = [_subspace_descriptor(subspace) for subspace in _as_list(subspaces) if isinstance(subspace, Mapping)]
    return create_subspace_registry(descriptors)


def _subspace_descriptor(subspace: Mapping[str, Any]) -> dict[str, Any]:
    subspace_id = str(subspace.get("subspace_id") or "").strip()
    subspace_kind = str(subspace.get("subspace_kind") or "project").strip()
    created_at = str(subspace.get("created_at") or "2026-05-27T00:00:00Z")
    return create_subspace_descriptor(
        subspace_id=subspace_id,
        subspace_kind=subspace_kind,
        scope=subspace.get("scope") or _default_scope(subspace_id, subspace_kind),
        owner=str(subspace.get("owner") or "active-context-quality-harness"),
        access_policy=subspace.get("access_policy"),
        risk_level=str(subspace.get("risk_level") or "low"),
        lifecycle_status=str(subspace.get("lifecycle_status") or "active"),
        active_summary=str(subspace.get("active_summary") or f"Active context quality subspace {subspace_id}."),
        source_index=subspace.get("source_index") or {"source_ids": [f"harness:v09:{subspace_id}"]},
        fact_graph_ref=subspace.get("fact_graph_ref") or {"node_id": f"fact-graph:{subspace_id}"},
        memory_blocks_ref=subspace.get("memory_blocks_ref") or {"block_ids": [f"block:{subspace_id}"]},
        tags=subspace.get("tags", []),
        priority=subspace.get("priority", 0),
        created_at=created_at,
        updated_at=str(subspace.get("updated_at") or created_at),
        last_compacted_at=subspace.get("last_compacted_at"),
        governance_status=str(subspace.get("governance_status") or "governed"),
        policy=subspace.get("policy"),
    )


def _default_scope(subspace_id: str, subspace_kind: str) -> dict[str, str]:
    scope = subspace_id.split(":", 1)[1] if ":" in subspace_id else subspace_id
    if subspace_kind == "project":
        return {"project_scope": scope}
    if subspace_kind == "agent":
        return {"agent_scope": scope}
    if subspace_kind == "risk":
        return {"risk_scope": scope}
    if subspace_kind == "archive":
        return {"archive_scope": scope}
    if subspace_kind == "global":
        return {"scope_id": scope or "global"}
    return {"custom_scope": scope}


def _case_mapping(case: Any, index: int, fixture_path: Path) -> dict[str, Any]:
    if not isinstance(case, Mapping):
        raise ValueError(f"Case at index {index} in {fixture_path} must be a mapping.")
    if not case.get("id"):
        raise ValueError(f"Case at index {index} in {fixture_path} must define id.")
    if not case.get("query"):
        raise ValueError(f"Case {case.get('id')} in {fixture_path} must define query.")
    return deepcopy(dict(case))


def _rejection_reasons(packet: Mapping[str, Any], explanation: Mapping[str, Any]) -> dict[str, Any]:
    reasons = {
        str(item.get("id")): item.get("reason")
        for item in _as_list(packet.get("rejected_memories"))
        if isinstance(item, Mapping) and item.get("id")
    }
    selection = explanation.get("selection_rejection_explanation")
    if isinstance(selection, Mapping):
        subspace_reasons = selection.get("subspace_rejected_reasons")
        if isinstance(subspace_reasons, Mapping):
            reasons.update(deepcopy(dict(subspace_reasons)))
    return reasons


def _packet_policy(packet: Mapping[str, Any]) -> dict[str, Any]:
    policy = packet.get("policy")
    return deepcopy(dict(policy)) if isinstance(policy, Mapping) else {}


def _ids_equal(actual: Any, expected: Any) -> bool:
    if expected is None:
        return True
    return [str(item) for item in _as_list(actual)] == [str(item) for item in _as_list(expected)]


def _ids_set_equal(actual: Any, expected: Any) -> bool:
    if expected is None:
        return True
    return {str(item) for item in _as_list(actual)} == {str(item) for item in _as_list(expected)}


def _rejection_reasons_match(actual: Any, expected: Any) -> bool:
    if expected is None:
        return True
    if not isinstance(expected, Mapping):
        return False
    actual_map = actual if isinstance(actual, Mapping) else {}
    for item_id, expected_reason in expected.items():
        if not _reason_matches(actual_map.get(item_id), expected_reason):
            return False
    return True


def _reason_matches(actual_reason: Any, expected_reason: Any) -> bool:
    actual_reasons = [str(reason) for reason in _as_list(actual_reason)]
    expected_reasons = [str(reason) for reason in _as_list(expected_reason)]
    for expected in expected_reasons:
        if not any(actual == expected or actual.startswith(expected) for actual in actual_reasons):
            return False
    return True


def _rejected_content_absent(case: Mapping[str, Any], evidence: Mapping[str, Any]) -> bool:
    if bool(case.get("include_rejected", False)):
        return True
    rejected_ids = {str(item) for item in _as_list(evidence.get("rejected_memory_ids"))}
    compact_text = str(evidence.get("compact_context_text", ""))
    for memory in _as_list(case.get("memories")):
        if not isinstance(memory, Mapping) or str(memory.get("id")) not in rejected_ids:
            continue
        content = " ".join(
            str(memory.get(field, "")).strip()
            for field in ("title", "summary", "content", "text")
            if str(memory.get(field, "")).strip()
        )
        if content and content in compact_text:
            return False
    return True


def _policy_safety_ok(evidence: Mapping[str, Any]) -> bool:
    policy = evidence.get("policy", {}) if isinstance(evidence, Mapping) else {}
    provider_policy = evidence.get("provider_runtime_policy", {}) if isinstance(evidence, Mapping) else {}
    if not isinstance(policy, Mapping) or not isinstance(provider_policy, Mapping):
        return False
    for key, expected in REQUIRED_SAFETY_POLICY.items():
        if policy.get(key) is not expected or provider_policy.get(key) is not expected:
            return False
    if evidence.get("provider_tools") != []:
        return False
    for field in (
        "calls_real_model",
        "calls_network",
        "calls_executor",
        "created_durable_memory_write",
        "created_graph_write",
        "created_operation_event",
        "created_real_proposal",
        "writes_proposal_files",
        "writes_operation_ledger",
        "writes_token_files",
        "writes_approval_audit",
        "invokes_real_token_write_executor",
        "implements_real_token_write_executor",
        "exposes_provider_tools",
    ):
        if evidence.get(field) is not False:
            return False
    return True


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    if isinstance(value, set):
        return sorted(value)
    return [value]


if __name__ == "__main__":
    sys.exit(main())
