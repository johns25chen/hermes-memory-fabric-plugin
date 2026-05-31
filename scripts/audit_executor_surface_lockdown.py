#!/usr/bin/env python3
"""CLI wrapper for v1.6 Executor Surface Lockdown Audit."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import TextIO

from hermes_memory_fabric.memory_executor_surface_lockdown_audit import (
    audit_executor_surface_lockdown,
    report_to_json,
)


def cli_main(
    argv: list[str] | None = None,
    *,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
) -> int:
    out = stdout if stdout is not None else sys.stdout
    err = stderr if stderr is not None else sys.stderr
    parser = argparse.ArgumentParser(description="Audit executor-adjacent Memory Fabric write surfaces.")
    parser.add_argument("--repo-root", default=".", help="Repository root to audit. Defaults to cwd.")
    parser.add_argument("--output", help="Optional explicit JSON output path. Defaults to stdout.")
    parser.add_argument("--print-summary", action="store_true")
    args = parser.parse_args(argv)

    report = audit_executor_surface_lockdown(args.repo_root)
    rendered = report_to_json(report)

    if args.output:
        output_path = Path(args.output)
        if _is_under_hermes_home(output_path):
            err.write("executor_surface_lockdown_audit_error=refusing_output_under_hermes_home\n")
            return 2
        output_path.write_text(rendered, encoding="utf-8")
    else:
        out.write(rendered)

    if args.print_summary:
        summary = {
            "version": report["version"],
            "audit_status": report["audit_status"],
            "provider_tools": report["provider_tools"],
            "forbidden_files_present": len(report["forbidden_files_present"]),
            "forbidden_calls": len(report["forbidden_calls"]),
            "forbidden_write_surfaces": len(report["forbidden_write_surfaces"]),
            "missing_no_write_flags": len(report["missing_no_write_flags"]),
            "v15_boundary_status": report["v15_boundary_status"],
        }
        err.write("executor_surface_lockdown_audit_summary=")
        err.write(json.dumps(summary, sort_keys=True, separators=(",", ":")))
        err.write("\n")

    return 0


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
