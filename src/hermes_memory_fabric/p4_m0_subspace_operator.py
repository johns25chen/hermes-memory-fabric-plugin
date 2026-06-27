from __future__ import annotations

import argparse
import json
import sys
from contextlib import redirect_stderr
from dataclasses import asdict
from pathlib import Path
from typing import Any, TextIO

from .p4_m0_subspace_workspace import create_workspace_subspace_memory_store


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="p4-m0-subspace-operator",
        description="Manual local operator commands for the P4-M0 Subspace Memory store.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    propose = subparsers.add_parser("propose")
    _add_workspace_root(propose)
    propose.add_argument("--project", required=True)
    propose.add_argument("--namespace", required=True)
    propose.add_argument("--content", required=True)
    propose.add_argument("--source", default="local")
    propose.add_argument("--tag", action="append", default=[])
    propose.add_argument("--confidence", type=float, default=1.0)

    approve = subparsers.add_parser("approve")
    _add_workspace_root(approve)
    approve.add_argument("--proposal-id", required=True)
    approve.add_argument("--approver", required=True)
    approve.add_argument("--note")

    reject = subparsers.add_parser("reject")
    _add_workspace_root(reject)
    reject.add_argument("--proposal-id", required=True)
    reject.add_argument("--reviewer", required=True)
    reject.add_argument("--reason", required=True)

    recall = subparsers.add_parser("recall")
    _add_workspace_root(recall)
    recall.add_argument("--query", required=True)
    recall.add_argument("--project")
    recall.add_argument("--namespace")
    recall.add_argument("--limit", type=int, default=10)

    audit = subparsers.add_parser("audit")
    _add_workspace_root(audit)
    audit.add_argument("--limit", type=int, default=50)

    return parser


def run_operator_command(
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
        payload = _run_parsed_command(args)
    except SystemExit as exc:
        return int(exc.code) if isinstance(exc.code, int) else 2
    except (OSError, ValueError) as exc:
        err.write(f"{exc}\n")
        return 1

    _write_json(out, payload)
    return 0


def main(argv: list[str] | None = None) -> int:
    return run_operator_command(sys.argv[1:] if argv is None else argv)


def _add_workspace_root(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--workspace-root", default=".")


def _run_parsed_command(args: argparse.Namespace) -> dict[str, Any]:
    store = create_workspace_subspace_memory_store(Path(args.workspace_root))
    storage_root = str(store.storage_root)

    if args.command == "propose":
        proposal = store.propose_memory(
            project=args.project,
            namespace=args.namespace,
            content=args.content,
            source=args.source,
            tags=args.tag,
            confidence=args.confidence,
        )
        return {
            "proposal_id": proposal.id,
            "status": proposal.status,
            "project": proposal.project,
            "namespace": proposal.namespace,
            "storage_root": storage_root,
        }

    if args.command == "approve":
        memory = store.approve_proposal(
            args.proposal_id,
            approver=args.approver,
            note=args.note,
        )
        return {
            "memory_id": memory.id,
            "proposal_id": memory.proposal_id,
            "status": memory.status,
            "storage_root": storage_root,
        }

    if args.command == "reject":
        rejected = store.reject_proposal(
            args.proposal_id,
            reviewer=args.reviewer,
            reason=args.reason,
        )
        return {
            "proposal_id": rejected.id,
            "status": rejected.status,
            "reason": rejected.reason,
            "storage_root": storage_root,
        }

    if args.command == "recall":
        _validate_positive_limit(args.limit)
        results = store.recall(
            args.query,
            project=args.project,
            namespace=args.namespace,
            limit=args.limit,
        )
        return {
            "query": args.query,
            "count": len(results),
            "results": [asdict(result) for result in results],
            "storage_root": storage_root,
        }

    if args.command == "audit":
        _validate_positive_limit(args.limit)
        events = store.list_audit_events()
        limited_events = events[-args.limit :]
        return {
            "count": len(limited_events),
            "events": [asdict(event) for event in limited_events],
            "storage_root": storage_root,
        }

    raise ValueError(f"unsupported_command:{args.command}")


def _validate_positive_limit(limit: int) -> None:
    if limit < 1:
        raise ValueError("limit_must_be_positive")


def _write_json(stdout: TextIO, payload: dict[str, Any]) -> None:
    json.dump(payload, stdout, ensure_ascii=False, sort_keys=True)
    stdout.write("\n")


if __name__ == "__main__":
    raise SystemExit(main())
