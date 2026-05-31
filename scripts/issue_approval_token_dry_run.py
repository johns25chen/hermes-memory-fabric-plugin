#!/usr/bin/env python3
"""CLI wrapper for v1.9 Approval Token Issuance Dry Run."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import TextIO

from hermes_memory_fabric.memory_approval_token_issuance_dry_run import (
    approval_token_issuance_dry_run_to_json,
    run_memory_approval_token_issuance_dry_run,
)


def cli_main(
    argv: list[str] | None = None,
    *,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
) -> int:
    out = stdout if stdout is not None else sys.stdout
    err = stderr if stderr is not None else sys.stderr
    parser = argparse.ArgumentParser(
        description="Dry-run a v1.8 approval-intent review outcome into a token issuance draft."
    )
    parser.add_argument("--input", required=True, help="Path to v1.8 review outcome dry-run JSON.")
    parser.add_argument("--issuer", default="manual-human-review", help="Issuer label for the draft.")
    parser.add_argument("--reason", default="", help="Optional issuance reason.")
    parser.add_argument("--output", help="Optional explicit output JSON path. Defaults to stdout.")
    parser.add_argument("--print-summary", action="store_true")
    args = parser.parse_args(argv)

    try:
        review_outcome = json.loads(Path(args.input).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        err.write(f"approval_token_issuance_dry_run_error={exc}\n")
        return 2
    if not isinstance(review_outcome, dict):
        err.write("approval_token_issuance_dry_run_error=input_must_be_json_object\n")
        return 2

    result = run_memory_approval_token_issuance_dry_run(
        review_outcome,
        issuer=args.issuer,
        issuance_reason=args.reason,
    )
    rendered = approval_token_issuance_dry_run_to_json(result)

    if args.output:
        output_path = Path(args.output)
        if _is_under_forbidden_hermes_home(output_path):
            err.write("approval_token_issuance_dry_run_error=refusing_output_under_hermes_home\n")
            return 2
        output_path.write_text(rendered, encoding="utf-8")
    else:
        out.write(rendered)

    if args.print_summary:
        err.write("approval_token_issuance_dry_run_summary=")
        err.write(json.dumps(_cli_summary(result), sort_keys=True, separators=(",", ":")))
        err.write("\n")

    return 0


def _cli_summary(result: dict[str, object]) -> dict[str, object]:
    return {
        "version": result.get("version"),
        "dry_run": result.get("dry_run"),
        "token_issuance_status": result.get("token_issuance_status"),
        "token_draft_id": result.get("token_draft_id"),
        "token_intent_id": result.get("token_intent_id"),
        "source_review_gate_version": result.get("source_review_gate_version"),
        "source_review_gate_status": result.get("source_review_gate_status"),
        "source_reviewer_decision": result.get("source_reviewer_decision"),
        "approval_token_issued": result.get("approval_token_issued"),
        "approval_token_id": result.get("approval_token_id"),
        "approval_token_value": result.get("approval_token_value"),
        "creates_usable_token": result.get("creates_usable_token"),
        "creates_real_proposal": result.get("creates_real_proposal"),
        "writes_operation_ledger": result.get("writes_operation_ledger"),
        "writes_memory": result.get("writes_memory"),
        "invokes_real_executor": result.get("invokes_real_executor"),
        "provider_tools": result.get("provider_tools"),
    }


def _is_under_forbidden_hermes_home(path: Path) -> bool:
    forbidden_roots = [
        Path(os.environ.get("HERMES_HOME", str(Path.home() / ".hermes"))),
        Path.home() / ".hermes",
    ]
    try:
        resolved_path = path.expanduser().resolve(strict=False)
    except OSError:
        return False
    for root in forbidden_roots:
        try:
            resolved_root = root.expanduser().resolve(strict=False)
        except OSError:
            continue
        if resolved_path == resolved_root or resolved_root in resolved_path.parents:
            return True
    return False


if __name__ == "__main__":
    raise SystemExit(cli_main())
