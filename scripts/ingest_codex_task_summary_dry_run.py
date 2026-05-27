#!/usr/bin/env python3
"""CLI wrapper for v1.3.0 Codex task summary ingestion dry-run."""

from __future__ import annotations

from hermes_memory_fabric.codex_task_summary_ingestion import cli_main


if __name__ == "__main__":
    raise SystemExit(cli_main())
