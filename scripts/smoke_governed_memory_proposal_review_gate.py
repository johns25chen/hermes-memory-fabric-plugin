#!/usr/bin/env python3
"""Smoke test for governed memory proposal review gate."""

from __future__ import annotations

from pathlib import Path
import sys

REPO_SRC = Path(__file__).resolve().parents[1] / "src"
if REPO_SRC.is_dir():
    sys.path.insert(0, str(REPO_SRC))

from hermes_memory_fabric.governed_memory_proposal_review_gate import (  # noqa: E402
    build_governed_memory_proposal_review_gate,
)


def _valid_proposal_report() -> dict[str, object]:
    return {
        "version": "2.10.0",
        "status": "proposal_ready",
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
        "civilization_core_layer_mapping": {
            "primary_layer": "星辰记忆",
            "supporting_layers": ["星域记忆", "星穹记忆", "星界记忆"],
            "direction": "星界闭环证据 -> 星辰候选记忆提案",
        },
        "candidate_memories": [
            {
                "candidate_id": "star-memory-smoke-candidate",
                "memory_layer": "星辰记忆",
                "title": "Smoke candidate",
                "summary": "Structurally complete candidate memory for review gate smoke coverage.",
                "evidence_basis": {"source": "smoke", "categories": [{"category": "local", "present": True}]},
                "scope": "Smoke-test candidate only.",
                "risks": ["candidate_must_not_be_treated_as_durable_memory"],
                "required_review": ["human_operator_review"],
            }
        ],
    }


EXPECTED_RESULT = {
    "status": "review_ready",
    "read_only": True,
    "read_only_memory": True,
    "would_mutate_memory": False,
    "writes_files": False,
    "invokes_openclaw": False,
    "would_call_github_api": False,
    "would_write_durable_memory": False,
    "would_mutate_memory_graph": False,
    "would_create_operation_ledger_entry": False,
    "would_create_approval_request": False,
    "authorization_granted": False,
    "review_gate_authorized": False,
    "approval_request_authorized": False,
    "memory_write_authorized": False,
    "openclaw_execution_authorized": False,
}


def main() -> int:
    try:
        result = build_governed_memory_proposal_review_gate(_valid_proposal_report())
        for key, expected in EXPECTED_RESULT.items():
            if result.get(key) != expected:
                print(f"governed_memory_proposal_review_gate=failed {key}", file=sys.stderr)
                return 1
        layer_mapping = result.get("civilization_core_layer_mapping", {})
        if layer_mapping.get("primary_layer") != "星穹记忆":
            print("governed_memory_proposal_review_gate=failed primary_layer", file=sys.stderr)
            return 1
        if not result.get("accepted_candidate_ids"):
            print("governed_memory_proposal_review_gate=failed accepted_candidate_ids", file=sys.stderr)
            return 1
        if result.get("blocked_candidate_ids") != []:
            print("governed_memory_proposal_review_gate=failed blocked_candidate_ids", file=sys.stderr)
            return 1
    except Exception as exc:
        print(f"governed_memory_proposal_review_gate=failed {type(exc).__name__}", file=sys.stderr)
        return 1

    print("governed_memory_proposal_review_gate=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
