from __future__ import annotations

import argparse
import json
import sys
from contextlib import redirect_stderr
from dataclasses import asdict
from pathlib import Path
from typing import Any, TextIO

from .p4_m0_subspace_memory import VALID_LIFECYCLE_STATES
from .p4_m0_subspace_project_seed import (
    get_project_memory_seed,
    list_project_memory_seeds,
    render_project_memory_seed_pack,
)
from .p4_m0_subspace_seed_approval_runbook import (
    SEED_APPROVAL_RUNBOOK_BOUNDARY,
    render_seed_approval_runbook_markdown,
    seed_approval_runbook_as_dicts,
)
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
    recall.add_argument("--include-stale", action="store_true")
    recall.add_argument("--include-archived", action="store_true")

    lifecycle = subparsers.add_parser("lifecycle")
    _add_workspace_root(lifecycle)
    lifecycle.add_argument("--memory-id", required=True)
    lifecycle.add_argument("--state", choices=VALID_LIFECYCLE_STATES, required=True)
    lifecycle.add_argument("--actor", required=True)
    lifecycle.add_argument("--reason")

    do_not_retry = subparsers.add_parser("do-not-retry")
    do_not_retry_subparsers = do_not_retry.add_subparsers(dest="do_not_retry_command", required=True)

    do_not_retry_set = do_not_retry_subparsers.add_parser("set")
    _add_workspace_root(do_not_retry_set)
    do_not_retry_set.add_argument("--memory-id", required=True)
    do_not_retry_set.add_argument("--reason", required=True)
    do_not_retry_set.add_argument("--actor", required=True)
    do_not_retry_set.add_argument("--alternative")

    do_not_retry_clear = do_not_retry_subparsers.add_parser("clear")
    _add_workspace_root(do_not_retry_clear)
    do_not_retry_clear.add_argument("--memory-id", required=True)
    do_not_retry_clear.add_argument("--actor", required=True)
    do_not_retry_clear.add_argument("--reason")

    project_seed = subparsers.add_parser("project-seed")
    project_seed_subparsers = project_seed.add_subparsers(dest="project_seed_command", required=True)

    project_seed_list = project_seed_subparsers.add_parser("list")
    _add_workspace_root(project_seed_list)

    project_seed_show = project_seed_subparsers.add_parser("show")
    _add_workspace_root(project_seed_show)
    project_seed_show.add_argument("--seed-id", required=True)

    project_seed_pack = project_seed_subparsers.add_parser("pack")
    _add_workspace_root(project_seed_pack)

    project_seed_approval_runbook = project_seed_subparsers.add_parser("approval-runbook")
    _add_workspace_root(project_seed_approval_runbook)
    project_seed_approval_runbook.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
    )

    project_seed_propose = project_seed_subparsers.add_parser("propose")
    _add_workspace_root(project_seed_propose)
    project_seed_propose.add_argument("--seed-id", required=True)
    project_seed_propose.add_argument("--actor", required=True)

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

    if isinstance(payload, str):
        out.write(payload)
    else:
        _write_json(out, payload)
    return 0


def main(argv: list[str] | None = None) -> int:
    return run_operator_command(sys.argv[1:] if argv is None else argv)


def _add_workspace_root(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--workspace-root", default=".")


def _run_parsed_command(args: argparse.Namespace) -> dict[str, Any] | str:
    if args.command == "propose":
        store = create_workspace_subspace_memory_store(Path(args.workspace_root))
        storage_root = str(store.storage_root)
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
        store = create_workspace_subspace_memory_store(Path(args.workspace_root))
        storage_root = str(store.storage_root)
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
        store = create_workspace_subspace_memory_store(Path(args.workspace_root))
        storage_root = str(store.storage_root)
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
        store = create_workspace_subspace_memory_store(Path(args.workspace_root))
        storage_root = str(store.storage_root)
        _validate_positive_limit(args.limit)
        results = store.recall(
            args.query,
            project=args.project,
            namespace=args.namespace,
            limit=args.limit,
            include_stale=args.include_stale,
            include_archived=args.include_archived,
        )
        return {
            "query": args.query,
            "count": len(results),
            "results": [asdict(result) for result in results],
            "storage_root": storage_root,
        }

    if args.command == "lifecycle":
        store = create_workspace_subspace_memory_store(Path(args.workspace_root))
        storage_root = str(store.storage_root)
        memory = store.set_memory_lifecycle(
            args.memory_id,
            args.state,
            actor=args.actor,
            reason=args.reason,
        )
        previous_lifecycle = _latest_lifecycle_audit_previous(store, memory.id)
        return {
            "memory_id": memory.id,
            "lifecycle": memory.lifecycle,
            "previous_lifecycle": previous_lifecycle,
            "status": memory.status,
            "storage_root": storage_root,
        }

    if args.command == "do-not-retry":
        store = create_workspace_subspace_memory_store(Path(args.workspace_root))
        storage_root = str(store.storage_root)
        if args.do_not_retry_command == "set":
            memory = store.set_do_not_retry(
                args.memory_id,
                reason=args.reason,
                actor=args.actor,
                alternative=args.alternative,
            )
            return {
                "memory_id": memory.id,
                "status": memory.status,
                "do_not_retry": asdict(memory.do_not_retry) if memory.do_not_retry is not None else None,
                "storage_root": storage_root,
            }

        if args.do_not_retry_command == "clear":
            memory = store.clear_do_not_retry(
                args.memory_id,
                actor=args.actor,
                reason=args.reason,
            )
            previous = _latest_do_not_retry_clear_previous(store, memory.id)
            return {
                "memory_id": memory.id,
                "status": memory.status,
                "do_not_retry": None,
                "previous_do_not_retry": previous,
                "storage_root": storage_root,
            }

        raise ValueError(f"unsupported_do_not_retry_command:{args.do_not_retry_command}")

    if args.command == "project-seed":
        if args.project_seed_command == "list":
            seeds = list_project_memory_seeds()
            return {
                "count": len(seeds),
                "seeds": [_seed_summary(seed) for seed in seeds],
            }

        if args.project_seed_command == "show":
            seed = get_project_memory_seed(args.seed_id)
            return _seed_detail(seed)

        if args.project_seed_command == "pack":
            return render_project_memory_seed_pack()

        if args.project_seed_command == "approval-runbook":
            if args.format == "markdown":
                return render_seed_approval_runbook_markdown()
            if args.format == "json":
                entries = seed_approval_runbook_as_dicts()
                return {
                    "boundary": SEED_APPROVAL_RUNBOOK_BOUNDARY,
                    "count": len(entries),
                    "entries": list(entries),
                }
            raise ValueError(f"unsupported_project_seed_approval_runbook_format:{args.format}")

        if args.project_seed_command == "propose":
            seed = get_project_memory_seed(args.seed_id)
            actor = _required_text(args.actor, "actor")
            store = create_workspace_subspace_memory_store(Path(args.workspace_root))
            proposal = store.propose_memory(
                project=seed.project,
                namespace=seed.namespace,
                content=seed.content,
                source=f"{seed.source}:proposed-by:{actor}",
                tags=seed.tags,
                confidence=seed.confidence,
            )
            return {
                "seed_id": seed.seed_id,
                "proposal_id": proposal.id,
                "status": proposal.status,
                "project": proposal.project,
                "namespace": proposal.namespace,
                "storage_root": str(store.storage_root),
                "requires_human_approval": True,
            }

        raise ValueError(f"unsupported_project_seed_command:{args.project_seed_command}")

    if args.command == "audit":
        store = create_workspace_subspace_memory_store(Path(args.workspace_root))
        storage_root = str(store.storage_root)
        _validate_positive_limit(args.limit)
        events = store.list_audit_events()
        limited_events = events[-args.limit :]
        return {
            "count": len(limited_events),
            "events": [asdict(event) for event in limited_events],
            "storage_root": storage_root,
        }

    raise ValueError(f"unsupported_command:{args.command}")


def _seed_summary(seed: Any) -> dict[str, Any]:
    return {
        "seed_id": seed.seed_id,
        "project": seed.project,
        "namespace": seed.namespace,
        "source": seed.source,
        "tags": list(seed.tags),
        "confidence": seed.confidence,
    }


def _seed_detail(seed: Any) -> dict[str, Any]:
    return {
        **_seed_summary(seed),
        "content": seed.content,
    }


def _latest_lifecycle_audit_previous(store: Any, memory_id: str) -> str:
    for event in reversed(store.list_audit_events()):
        if event.event_type == "memory_lifecycle_updated" and event.target_id == memory_id:
            return str(event.detail["previous_lifecycle"])
    raise ValueError("memory_lifecycle_audit_not_found")


def _latest_do_not_retry_clear_previous(store: Any, memory_id: str) -> dict[str, Any] | None:
    for event in reversed(store.list_audit_events()):
        if event.event_type == "memory_do_not_retry_cleared" and event.target_id == memory_id:
            previous = event.detail["previous_do_not_retry"]
            if previous is None:
                return None
            return dict(previous)
    raise ValueError("memory_do_not_retry_clear_audit_not_found")


def _validate_positive_limit(limit: int) -> None:
    if limit < 1:
        raise ValueError("limit_must_be_positive")


def _required_text(value: object, field: str) -> str:
    cleaned = str(value or "").strip()
    if not cleaned:
        raise ValueError(f"{field}_must_be_non_empty")
    return cleaned


def _write_json(stdout: TextIO, payload: dict[str, Any]) -> None:
    json.dump(payload, stdout, ensure_ascii=False, sort_keys=True)
    stdout.write("\n")


if __name__ == "__main__":
    raise SystemExit(main())
