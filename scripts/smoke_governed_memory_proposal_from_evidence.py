#!/usr/bin/env python3
"""Smoke test for governed memory proposal generation from evidence."""

from __future__ import annotations

from pathlib import Path
import sys

REPO_SRC = Path(__file__).resolve().parents[1] / "src"
if REPO_SRC.is_dir():
    sys.path.insert(0, str(REPO_SRC))

from hermes_memory_fabric.governed_memory_proposal_from_evidence import (  # noqa: E402
    build_governed_memory_proposal_from_evidence,
)


def _valid_evidence_validation() -> dict[str, object]:
    return {
        "version": "2.9.0",
        "status": "closed_loop_evidence_ready",
        "read_only": True,
        "read_only_memory": True,
        "would_mutate_memory": False,
        "invokes_openclaw": False,
        "writes_files": False,
        "would_call_github_api": False,
        "would_merge_pr": False,
        "would_create_tag": False,
        "authorization_granted": False,
        "openclaw_execution_authorized": False,
        "evidence_summary": {
            "categories_present": [
                "natural_language_task",
                "codex_cli_implementation",
                "terminal_or_openclaw_validation",
                "chatgpt_review",
                "human_operator_decision",
                "github_record",
            ],
            "natural_language_task": {
                "present": True,
                "true_flag_count": 1,
                "non_empty_list_count": 0,
                "non_empty_text_field_count": 2,
            },
            "codex_cli_implementation": {
                "present": True,
                "true_flag_count": 3,
                "non_empty_list_count": 1,
                "non_empty_text_field_count": 1,
            },
            "terminal_or_openclaw_validation": {
                "present": True,
                "true_flag_count": 4,
                "non_empty_list_count": 1,
                "non_empty_text_field_count": 0,
            },
            "chatgpt_review": {
                "present": True,
                "true_flag_count": 4,
                "non_empty_list_count": 0,
                "non_empty_text_field_count": 0,
            },
            "human_operator_decision": {
                "present": True,
                "true_flag_count": 2,
                "non_empty_list_count": 0,
                "non_empty_text_field_count": 0,
            },
            "github_record": {
                "present": True,
                "true_flag_count": 2,
                "non_empty_list_count": 0,
                "non_empty_text_field_count": 0,
            },
        },
        "missing_evidence": [],
        "blocking_reasons": [],
        "required_actions": ["human_operator_may_review_evidence_no_authorization_granted"],
    }


EXPECTED_RESULT = {
    "status": "proposal_ready",
    "read_only": True,
    "read_only_memory": True,
    "would_mutate_memory": False,
    "writes_files": False,
    "invokes_openclaw": False,
    "would_call_github_api": False,
    "would_write_durable_memory": False,
    "would_mutate_memory_graph": False,
    "would_create_operation_ledger_entry": False,
    "authorization_granted": False,
    "memory_write_authorized": False,
    "openclaw_execution_authorized": False,
}


def main() -> int:
    try:
        result = build_governed_memory_proposal_from_evidence(_valid_evidence_validation())
        for key, expected in EXPECTED_RESULT.items():
            if result.get(key) != expected:
                print(f"governed_memory_proposal_from_evidence=failed {key}", file=sys.stderr)
                return 1
        layer_mapping = result.get("civilization_core_layer_mapping", {})
        if layer_mapping.get("primary_layer") != "星辰记忆":
            print("governed_memory_proposal_from_evidence=failed primary_layer", file=sys.stderr)
            return 1
        if not result.get("candidate_memories"):
            print("governed_memory_proposal_from_evidence=failed candidate_memories", file=sys.stderr)
            return 1
    except Exception as exc:
        print(f"governed_memory_proposal_from_evidence=failed {type(exc).__name__}", file=sys.stderr)
        return 1

    print("governed_memory_proposal_from_evidence=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
