#!/usr/bin/env python3
"""Smoke test for closed-loop evidence validation."""

from __future__ import annotations

from pathlib import Path
import sys

REPO_SRC = Path(__file__).resolve().parents[1] / "src"
if REPO_SRC.is_dir():
    sys.path.insert(0, str(REPO_SRC))

from hermes_memory_fabric.closed_loop_evidence_validation import (  # noqa: E402
    build_closed_loop_evidence_validation,
)


def _valid_evidence() -> dict[str, object]:
    return {
        "natural_language_task": {
            "task_text": "Implement local closed-loop evidence validation.",
            "task_boundary": "Validate evidence completeness only.",
            "human_operator_confirmed_boundary": True,
        },
        "codex_cli_implementation": {
            "codex_cli_used": True,
            "repository_inspected": True,
            "files_changed": ["src/hermes_memory_fabric/closed_loop_evidence_validation.py"],
            "change_summary": "Added deterministic read-only validator.",
            "codex_did_not_commit": True,
        },
        "terminal_or_openclaw_validation": {
            "validation_commands": [".venv/bin/python -m pytest tests/test_closed_loop_evidence_validation.py -q"],
            "validation_passed": True,
            "controlled_validation_only": True,
            "no_real_world_execution": True,
            "no_openclaw_autonomous_execution": True,
        },
        "chatgpt_review": {
            "diff_reviewed": True,
            "tests_reviewed": True,
            "governance_boundaries_reviewed": True,
            "no_sensitive_output_exposed": True,
        },
        "human_operator_decision": {
            "merge_decision_by_human": True,
            "human_final_authority": True,
        },
        "github_record": {
            "pr_recorded": True,
            "commit_recorded": True,
            "release_intended": False,
        },
    }


EXPECTED_RESULT = {
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
}


def main() -> int:
    try:
        result = build_closed_loop_evidence_validation(_valid_evidence())
        for key, expected in EXPECTED_RESULT.items():
            if result.get(key) != expected:
                print(f"closed_loop_evidence_validation=failed {key}", file=sys.stderr)
                return 1
    except Exception as exc:
        print(f"closed_loop_evidence_validation=failed {type(exc).__name__}", file=sys.stderr)
        return 1

    print("closed_loop_evidence_validation=passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
