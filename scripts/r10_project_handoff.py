#!/usr/bin/env python3
"""Build one read-only, source-linked active-context packet from explicit local files."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import sys
import tempfile
from pathlib import Path
from typing import Any, Iterable, Mapping

from hermes_memory_fabric import MemoryFabricProvider
from hermes_memory_fabric.candidate_jsonl_source import DEFAULT_CANDIDATE_JSONL_MAX_BYTES


RESULT_FILENAME = "project-handoff-context.json"
DIAGNOSTIC_FILENAME = "project-handoff-diagnostics.json"
DEFAULT_MAX_SEGMENT_CHARS = 1600
DEFAULT_MEMORY_LIMIT = 8
DEFAULT_CONTEXT_BUDGET_CHARS = 8000
_PROVIDER_ID = "r10-local-project-handoff"
_SOURCE_DESCRIPTOR = {
    "provider_id": _PROVIDER_ID,
    "source_class": "LOCAL_CALLER",
    "source_instance": "local:r10-project-handoff",
}
_PROVIDER_REGISTRY = {
    _PROVIDER_ID: {
        "enabled": True,
        "source_classes": ["LOCAL_CALLER"],
        "capabilities": ["READ_CANDIDATE"],
        "review_only": False,
        "trusted_ingestion": True,
    }
}


class HandoffInputError(ValueError):
    """An explicit local handoff input does not meet this CLI's read boundary."""


class HandoffDeliveryError(RuntimeError):
    """The Provider packet or output could not be delivered safely."""


def _positive_int(value: str) -> int:
    try:
        result = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be an integer") from exc
    if result <= 0:
        raise argparse.ArgumentTypeError("must be greater than zero")
    return result


def _non_negative_int(value: str) -> int:
    try:
        result = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be an integer") from exc
    if result < 0:
        raise argparse.ArgumentTypeError("must not be negative")
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Read only explicitly listed local text files, then use MemoryFabricProvider "
            "to return source-linked active context."
        )
    )
    parser.add_argument("--source-file", action="append", required=True, help="Explicit UTF-8 regular file; repeatable.")
    parser.add_argument("--question", required=True, help="Question used for Provider retrieval and ranking.")
    parser.add_argument("--project", required=True, help="Exact Provider project scope.")
    parser.add_argument("--workspace", required=True, help="Exact logical absolute workspace scope; it grants no filesystem access.")
    parser.add_argument("--namespace", required=True, help="Exact Provider namespace scope.")
    parser.add_argument("--output-dir", required=True, help="Existing non-symlink directory for handoff result files.")
    parser.add_argument(
        "--confirm-local-context-use",
        action="store_true",
        help="Confirm this explicit candidate set may be read and used for this invocation only.",
    )
    parser.add_argument("--max-source-bytes", type=_positive_int, default=DEFAULT_CANDIDATE_JSONL_MAX_BYTES)
    parser.add_argument("--max-segment-chars", type=_positive_int, default=DEFAULT_MAX_SEGMENT_CHARS)
    parser.add_argument("--memory-limit", type=_positive_int, default=DEFAULT_MEMORY_LIMIT)
    parser.add_argument("--context-budget-chars", type=_non_negative_int, default=DEFAULT_CONTEXT_BUDGET_CHARS)
    parser.add_argument(
        "--caller-risk-level",
        required=True,
        choices=("low", "medium", "high", "critical"),
        help="Explicit caller classification only; it is not an independent risk review.",
    )
    parser.add_argument(
        "--write-diagnostics",
        action="store_true",
        help="Also write the full packet and unselected input candidates to a separate diagnostic file.",
    )
    return parser


def _absolute_path(value: str) -> Path:
    return Path(os.path.abspath(os.fspath(value)))


def _reject_symlink_components(target: Path) -> None:
    current = Path(target.anchor)
    for component in target.parts[1:]:
        current /= component
        try:
            mode = os.lstat(current).st_mode
        except FileNotFoundError:
            continue
        except OSError as exc:
            raise HandoffInputError(f"path_unavailable:{target}") from exc
        if stat.S_ISLNK(mode):
            raise HandoffInputError(f"symlink_not_allowed:{target}")


def _read_utf8_regular_file(value: str, *, max_bytes: int) -> tuple[Path, str, str]:
    target = _absolute_path(value)
    _reject_symlink_components(target)
    try:
        expected = os.lstat(target)
    except FileNotFoundError as exc:
        raise HandoffInputError(f"source_file_missing:{target}") from exc
    except OSError as exc:
        raise HandoffInputError(f"source_file_unreadable:{target}") from exc
    if not stat.S_ISREG(expected.st_mode):
        raise HandoffInputError(f"source_file_not_regular:{target}")
    if expected.st_size > max_bytes:
        raise HandoffInputError(f"source_file_exceeds_max_bytes:{target}")
    flags = os.O_RDONLY | getattr(os, "O_NONBLOCK", 0) | getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(target, flags)
    except FileNotFoundError as exc:
        raise HandoffInputError(f"source_file_missing:{target}") from exc
    except OSError as exc:
        raise HandoffInputError(f"source_file_unreadable:{target}") from exc
    try:
        details = os.fstat(descriptor)
        if not stat.S_ISREG(details.st_mode):
            raise HandoffInputError(f"source_file_not_regular:{target}")
        if (details.st_dev, details.st_ino) != (expected.st_dev, expected.st_ino):
            raise HandoffInputError(f"source_file_replaced_before_open:{target}")
        if details.st_size > max_bytes:
            raise HandoffInputError(f"source_file_exceeds_max_bytes:{target}")
        with os.fdopen(descriptor, "rb") as stream:
            descriptor = -1
            raw = stream.read(max_bytes + 1)
    finally:
        if descriptor >= 0:
            os.close(descriptor)
    if len(raw) > max_bytes:
        raise HandoffInputError(f"source_file_exceeds_max_bytes:{target}")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise HandoffInputError(f"source_file_not_utf8:{target}") from exc
    if not text:
        raise HandoffInputError(f"source_file_empty:{target}")
    return target, text, hashlib.sha256(raw).hexdigest()


def _segments(text: str, maximum_chars: int) -> Iterable[tuple[str, int, int, int, int]]:
    """Yield exact, consecutive source slices with one-based line and offset ranges."""
    pending = ""
    pending_start_line = 1
    pending_start_offset = 0
    offset = 0
    for line_number, line in enumerate(text.splitlines(keepends=True), start=1):
        if len(line) > maximum_chars:
            if pending:
                yield pending, pending_start_line, line_number - 1, pending_start_offset, offset
                pending = ""
            for position in range(0, len(line), maximum_chars):
                piece = line[position : position + maximum_chars]
                yield piece, line_number, line_number, offset + position, offset + position + len(piece)
        elif pending and len(pending) + len(line) > maximum_chars:
            yield pending, pending_start_line, line_number - 1, pending_start_offset, offset
            pending = line
            pending_start_line = line_number
            pending_start_offset = offset
        else:
            if not pending:
                pending_start_line = line_number
                pending_start_offset = offset
            pending += line
        offset += len(line)
    if pending:
        yield pending, pending_start_line, len(text.splitlines()), pending_start_offset, len(text)


def _source_identity(target: Path, digest: str) -> str:
    return hashlib.sha256(f"{target}\0{digest}".encode("utf-8")).hexdigest()


def _build_candidates(
    source_files: Iterable[str], *, project: str, max_bytes: int,
    max_segment_chars: int, caller_risk_level: str,
) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    seen_sources: set[str] = set()
    for value in source_files:
        normalized = _absolute_path(value)
        if str(normalized) in seen_sources:
            raise HandoffInputError(f"source_file_duplicate:{normalized}")
        seen_sources.add(str(normalized))
        target, text, digest = _read_utf8_regular_file(value, max_bytes=max_bytes)
        identity = _source_identity(target, digest)
        for content, line_start, line_end, char_start, char_end in _segments(text, max_segment_chars):
            source_id = f"local-file:{identity}:chars:{char_start}-{char_end}"
            candidates.append(
                {
                    "id": f"r10-file-{identity[:16]}-{char_start:012x}-{char_end:012x}",
                    "content": content,
                    "project_id": project,
                    "entity_ids": [project],
                    "source": "local-authorized-file",
                    "source_id": source_id,
                    "provenance": {
                        "file_path": str(target),
                        "file_sha256": digest,
                        "line_start": line_start,
                        "line_end": line_end,
                        "char_start": char_start,
                        "char_end": char_end,
                    },
                    "risk_level": caller_risk_level,
                    "governance": {
                        "dry_run": True,
                        "read_only": True,
                        "proposal_governed": True,
                        "would_write_memory": False,
                        "would_modify_config": False,
                        "would_write_graph": False,
                    },
                }
            )
    return candidates


def _output_paths(value: str, *, write_diagnostics: bool) -> tuple[Path, Path | None]:
    directory = _absolute_path(value)
    _reject_symlink_components(directory)
    try:
        if not directory.is_dir():
            raise HandoffInputError(f"output_dir_not_directory:{directory}")
    except OSError as exc:
        raise HandoffInputError(f"output_dir_unavailable:{directory}") from exc
    result = directory / RESULT_FILENAME
    diagnostic = directory / DIAGNOSTIC_FILENAME if write_diagnostics else None
    for target in (result, diagnostic):
        if target is not None and target.exists():
            raise HandoffInputError(f"output_result_already_exists:{target}")
    return result, diagnostic


def _selected_source_mappings(packet: dict[str, Any], candidates: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = {candidate["id"]: candidate for candidate in candidates}
    selected = packet.get("selected_memories")
    items = packet.get("context_items")
    context = packet.get("compact_context_text")
    if not isinstance(selected, list) or not isinstance(items, list) or not isinstance(context, str):
        raise HandoffDeliveryError("invalid_context_structure")
    selected_ids = {item.get("id") for item in selected if isinstance(item, dict)}
    mappings: list[dict[str, Any]] = []
    rendered: list[str] = []
    seen: set[str] = set()
    for item in items:
        if not isinstance(item, dict) or item.get("item_type") != "memory":
            raise HandoffDeliveryError("unmapped_context_item")
        item_id = item.get("item_id")
        if not isinstance(item_id, str) or not item_id.startswith("memory:"):
            raise HandoffDeliveryError("invalid_context_item_id")
        candidate_id = item_id.removeprefix("memory:")
        candidate = by_id.get(candidate_id)
        item_text = item.get("text")
        if (candidate is None or candidate_id not in selected_ids or candidate_id in seen
                or item.get("source_id") != candidate["source_id"]
                or not isinstance(item_text, str) or not item_text.strip()
                or item_text != candidate["content"].strip()):
            raise HandoffDeliveryError("context_source_mismatch")
        seen.add(candidate_id)
        text = item_text.strip()
        if text.startswith("[REJECTED]"):
            rendered.append(f"[REJECTED MEMORY {candidate['source_id']}] {text.removeprefix('[REJECTED]').strip()}")
        else:
            rendered.append(f"[MEMORY {candidate['source_id']}] {text}")
        mappings.append({
            "candidate_id": candidate_id,
            "source_id": candidate["source_id"],
            "provenance": candidate["provenance"],
        })
    if "\n".join(rendered) != context:
        raise HandoffDeliveryError("context_render_mismatch")
    return mappings


def run(args: argparse.Namespace) -> int:
    question = args.question.strip()
    project = args.project.strip()
    workspace = args.workspace.strip()
    namespace = args.namespace.strip()
    if not all((question, project, workspace, namespace)):
        raise HandoffInputError("question_project_workspace_namespace_must_be_nonempty")
    if not workspace.startswith("/"):
        raise HandoffInputError("workspace_must_be_absolute_logical_scope")

    result_path, diagnostic_path = _output_paths(args.output_dir, write_diagnostics=args.write_diagnostics)
    candidates = _build_candidates(
        args.source_file,
        project=project,
        max_bytes=args.max_source_bytes,
        max_segment_chars=args.max_segment_chars,
        caller_risk_level=args.caller_risk_level,
    )
    provider = MemoryFabricProvider()
    packet = provider.build_active_context(
        query=question,
        memory_candidates=candidates,
        project_scope=project,
        entity_ids=[project],
        memory_limit=args.memory_limit,
        context_budget_chars=args.context_budget_chars,
        admission_scope={"project": project, "workspace": workspace, "namespace": namespace},
        provider_registry_snapshot=_PROVIDER_REGISTRY,
        candidate_source_descriptor=_SOURCE_DESCRIPTOR,
    )
    validation = provider.validate_active_context(packet)
    if validation != {"valid": True, "errors": []}:
        raise HandoffDeliveryError("invalid_provider_packet")
    mappings = _selected_source_mappings(packet, candidates)
    context = packet["compact_context_text"]
    if context and not mappings:
        raise HandoffDeliveryError("context_without_sources")
    result = {
        "result_type": "r10_local_project_handoff",
        "context": context,
        "source_mappings": mappings,
    }
    if diagnostic_path is not None:
        diagnostics = {
            "diagnostic_type": "r10_local_project_handoff_diagnostics",
            "read_scope": {
                "project": project,
                "workspace": workspace,
                "namespace": namespace,
                "confirmed_for_this_call_only": True,
                "caller_risk_level": args.caller_risk_level,
            },
            "input_candidates": candidates,
            "packet": packet,
            "diagnostics": {
                "packet_validation": validation,
                "packet_explanation": provider.explain_active_context(packet),
            },
        }
        _write_json(diagnostic_path, diagnostics)
    if not context:
        print("NO_CONTEXT")
        return 3
    _write_json(result_path, result)
    print(json.dumps({"result_path": str(result_path), "context_chars": len(result["context"])}, ensure_ascii=False))
    return 0


def _write_json(target: Path, value: Mapping[str, Any]) -> None:
    content = json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    descriptor, temporary_name = tempfile.mkstemp(prefix=".project-handoff-", dir=target.parent)
    temporary = Path(temporary_name)
    identity = os.fstat(descriptor)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(content)
        os.link(temporary, target)
    finally:
        try:
            current = os.lstat(temporary)
        except FileNotFoundError:
            pass
        else:
            if (current.st_dev, current.st_ino) == (identity.st_dev, identity.st_ino):
                os.unlink(temporary)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.confirm_local_context_use:
        parser.error("--confirm-local-context-use is required")
    try:
        return run(args)
    except HandoffInputError as exc:
        parser.error(str(exc))
    except Exception as exc:
        print(f"ERROR:{type(exc).__name__}:{exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
