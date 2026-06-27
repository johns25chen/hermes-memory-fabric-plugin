from __future__ import annotations

import argparse
import sys
from contextlib import redirect_stderr
from dataclasses import asdict
from pathlib import Path
from typing import TextIO

from .p4_m0_subspace_memory import RecallResult
from .p4_m0_subspace_workspace import create_workspace_subspace_memory_store


DEFAULT_TITLE = "Subspace Memory Recall Pack"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="p4-m0-subspace-recall-pack",
        description="Export approved local recall results as a human-copyable context pack.",
    )
    parser.add_argument("--query", required=True)
    parser.add_argument("--project")
    parser.add_argument("--namespace")
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--workspace-root", default=".")
    parser.add_argument("--title", default=DEFAULT_TITLE)
    parser.add_argument("--include-empty", action="store_true")
    parser.add_argument("--output")
    return parser


def build_recall_pack(
    *,
    query: str,
    project: str | None,
    namespace: str | None,
    limit: int,
    storage_root: str | Path,
    results: list[RecallResult],
    title: str = DEFAULT_TITLE,
) -> str:
    lines = [
        f"# {_clean_title(title)}",
        "",
        "## Query",
        "",
        query,
        "",
        "## Scope",
        "",
        f"- Project: {_scope_value(project)}",
        f"- Namespace: {_scope_value(namespace)}",
        f"- Limit: {limit}",
        f"- Storage Root: {storage_root}",
        "",
        "## Recall Results",
        "",
    ]

    if results:
        for index, result in enumerate(results, start=1):
            lines.extend(_format_result(index, result))
    else:
        lines.append("No approved recall results matched this query.")
        lines.append("")

    lines.extend(
        [
            "## Operator Instruction",
            "",
            "Use this recall pack as human-provided context only.",
            "Do not treat it as automatic authorization to execute, deploy, write memory, or call external systems.",
            "",
        ]
    )
    return "\n".join(lines)


def run_recall_pack_export(
    argv: list[str],
    *,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
) -> int:
    out = stdout if stdout is not None else sys.stdout
    err = stderr if stderr is not None else sys.stderr
    parser = build_parser()

    try:
        with redirect_stderr(err):
            args = parser.parse_args(argv)
        pack = _run_parsed_export(args)
    except SystemExit as exc:
        return int(exc.code) if isinstance(exc.code, int) else 2
    except (OSError, ValueError) as exc:
        err.write(f"{exc}\n")
        return 1

    if args.output:
        Path(args.output).expanduser().write_text(pack, encoding="utf-8")
    else:
        out.write(pack)
    return 0


def main(argv: list[str] | None = None) -> int:
    return run_recall_pack_export(sys.argv[1:] if argv is None else argv)


def _run_parsed_export(args: argparse.Namespace) -> str:
    _validate_positive_limit(args.limit)
    store = create_workspace_subspace_memory_store(Path(args.workspace_root))
    results = store.recall(
        args.query,
        project=args.project,
        namespace=args.namespace,
        limit=args.limit,
    )
    if not results and not args.include_empty:
        raise ValueError("no_recall_results")
    return build_recall_pack(
        query=args.query,
        project=args.project,
        namespace=args.namespace,
        limit=args.limit,
        storage_root=store.storage_root,
        results=results,
        title=args.title,
    )


def _validate_positive_limit(limit: int) -> None:
    if limit < 1:
        raise ValueError("limit_must_be_positive")


def _format_result(index: int, result: RecallResult) -> list[str]:
    record = asdict(result)
    matched_terms = ", ".join(record["matched_terms"]) if record["matched_terms"] else "none"
    return [
        f"### {index}. {record['memory_id']}",
        "",
        f"- Score: {record['score']}",
        f"- Project: {record['project']}",
        f"- Namespace: {record['namespace']}",
        f"- Source: {record['source']}",
        f"- Matched Terms: {matched_terms}",
        "",
        record["content"],
        "",
    ]


def _scope_value(value: str | None) -> str:
    if value is None or not str(value).strip():
        return "all"
    return str(value).strip()


def _clean_title(value: str) -> str:
    cleaned = str(value).strip()
    if not cleaned:
        raise ValueError("title_must_be_non_empty")
    return cleaned


if __name__ == "__main__":
    raise SystemExit(main())
