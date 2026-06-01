#!/usr/bin/env python3
"""CLI wrapper for v2.0 Token Authority Boundary Contract Dry Run."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import TextIO

from hermes_memory_fabric.memory_token_authority_boundary_contract_dry_run import (
    run_memory_token_authority_boundary_contract_dry_run,
    token_authority_boundary_contract_dry_run_to_json,
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
        description="Dry-run a v1.9 token issuance candidate into a v2.0 authority boundary contract."
    )
    parser.add_argument("--input", required=True, help="Path to v1.9 token issuance dry-run JSON.")
    parser.add_argument(
        "--scope",
        action="append",
        dest="scopes",
        help="Repeatable authority scope. Defaults to memory_proposal_apply_preview_only.",
    )
    parser.add_argument("--expiry-seconds", type=int, default=900)
    parser.add_argument(
        "--revocation-required",
        default=True,
        action=argparse.BooleanOptionalAction,
        help="Require a future revocation boundary. Defaults to true.",
    )
    parser.add_argument(
        "--audit-required",
        default=True,
        action=argparse.BooleanOptionalAction,
        help="Require a future audit boundary. Defaults to true.",
    )
    parser.add_argument("--output", help="Optional explicit output JSON path. Defaults to stdout.")
    parser.add_argument("--print-summary", action="store_true")
    args = parser.parse_args(argv)

    try:
        token_issuance = json.loads(Path(args.input).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        err.write(f"token_authority_boundary_contract_dry_run_error={exc}\n")
        return 2
    if not isinstance(token_issuance, dict):
        err.write("token_authority_boundary_contract_dry_run_error=input_must_be_json_object\n")
        return 2

    result = run_memory_token_authority_boundary_contract_dry_run(
        token_issuance,
        authority_scope=args.scopes,
        expiry_seconds=args.expiry_seconds,
        revocation_required=args.revocation_required,
        audit_required=args.audit_required,
    )
    rendered = token_authority_boundary_contract_dry_run_to_json(result)

    if args.output:
        output_path = Path(args.output)
        if _is_under_forbidden_hermes_home(output_path):
            err.write(
                "token_authority_boundary_contract_dry_run_error=refusing_output_under_hermes_home\n"
            )
            return 2
        output_path.write_text(rendered, encoding="utf-8")
    else:
        out.write(rendered)

    if args.print_summary:
        err.write("token_authority_boundary_contract_dry_run_summary=")
        err.write(json.dumps(_cli_summary(result), sort_keys=True, separators=(",", ":")))
        err.write("\n")

    return 0


def _cli_summary(result: dict[str, object]) -> dict[str, object]:
    return {
        "version": result.get("version"),
        "dry_run": result.get("dry_run"),
        "authority_contract_status": result.get("authority_contract_status"),
        "authority_contract_id": result.get("authority_contract_id"),
        "source_token_issuance_version": result.get("source_token_issuance_version"),
        "source_token_issuance_status": result.get("source_token_issuance_status"),
        "required_next_step": result.get("required_next_step"),
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
