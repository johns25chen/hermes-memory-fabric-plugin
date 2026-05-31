#!/usr/bin/env python3
"""CLI wrapper for v1.7 Approval Intent Dry Run."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import TextIO

from hermes_memory_fabric.memory_approval_intent_dry_run import (
    approval_intent_dry_run_to_json,
    run_memory_approval_intent_dry_run,
)


def cli_main(
    argv: list[str] | None = None,
    *,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
) -> int:
    out = stdout if stdout is not None else sys.stdout
    err = stderr if stderr is not None else sys.stderr
    parser = argparse.ArgumentParser(description="Dry-run a v1.5 proposal preview into approval intent.")
    parser.add_argument("--input", required=True, help="Path to v1.5 proposal dry-run preview JSON.")
    parser.add_argument("--repo-root", default=".", help="Repository root for the v1.6 audit gate.")
    parser.add_argument("--output", help="Optional explicit output JSON path. Defaults to stdout.")
    parser.add_argument("--print-summary", action="store_true")
    args = parser.parse_args(argv)

    try:
        source_preview = json.loads(Path(args.input).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        err.write(f"approval_intent_dry_run_error={exc}\n")
        return 2
    if not isinstance(source_preview, dict):
        err.write("approval_intent_dry_run_error=input_must_be_json_object\n")
        return 2

    result = run_memory_approval_intent_dry_run(source_preview, repo_root=args.repo_root)
    rendered = approval_intent_dry_run_to_json(result)

    if args.output:
        output_path = Path(args.output)
        if _is_under_hermes_home(output_path):
            err.write("approval_intent_dry_run_error=refusing_output_under_hermes_home\n")
            return 2
        output_path.write_text(rendered, encoding="utf-8")
    else:
        out.write(rendered)

    if args.print_summary:
        err.write("approval_intent_dry_run_summary=")
        err.write(json.dumps(_cli_summary(result), sort_keys=True, separators=(",", ":")))
        err.write("\n")

    return 0


def _cli_summary(result: dict[str, object]) -> dict[str, object]:
    return {
        "version": result.get("version"),
        "dry_run": result.get("dry_run"),
        "approval_intent_status": result.get("approval_intent_status"),
        "approval_intent_id": result.get("approval_intent_id"),
        "source_preview_version": result.get("source_preview_version"),
        "source_accepted_count": result.get("source_accepted_count"),
        "human_review_required": result.get("human_review_required"),
        "approval_token_issued": result.get("approval_token_issued"),
        "creates_real_proposal": result.get("creates_real_proposal"),
        "writes_operation_ledger": result.get("writes_operation_ledger"),
        "writes_memory": result.get("writes_memory"),
        "invokes_real_executor": result.get("invokes_real_executor"),
        "provider_tools": result.get("provider_tools"),
    }


def _is_under_hermes_home(path: Path) -> bool:
    hermes_home = Path(os.environ.get("HERMES_HOME", str(Path.home() / ".hermes")))
    try:
        resolved_path = path.expanduser().resolve(strict=False)
        resolved_home = hermes_home.expanduser().resolve(strict=False)
        return resolved_path == resolved_home or resolved_home in resolved_path.parents
    except OSError:
        return False


if __name__ == "__main__":
    raise SystemExit(cli_main())
