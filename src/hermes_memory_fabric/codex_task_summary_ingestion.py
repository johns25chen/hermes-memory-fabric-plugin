"""Dry-run Codex task summary ingestion for Memory Fabric candidates."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable, Mapping, TextIO


CODEX_TASK_SUMMARY_INGESTION_VERSION = "1.3.0"
DEFAULT_PROJECT_ID = "hermes-memory-fabric"
DEFAULT_SOURCE = "codex-task-summary"
DEFAULT_CREATED_AT = "1970-01-01T00:00:00Z"

SECTION_ALIASES = {
    "goal": (
        "goal",
        "goals",
        "purpose",
        "goal purpose",
        "goal / purpose",
        "objective",
        "objectives",
    ),
    "changed_files": (
        "included",
        "changed files",
        "included files",
        "included changed files",
        "included / changed files",
        "files",
        "file changes",
    ),
    "validation": (
        "validation",
        "verification",
        "validated",
        "tests",
        "test",
        "smoke",
    ),
    "boundary": (
        "boundary",
        "boundaries",
        "safety boundary",
        "limitations",
        "constraints",
        "scope boundary",
    ),
    "commit": ("commit", "commits", "commit sha"),
    "pr": ("pr", "pull request", "pull requests"),
    "version": ("version", "release", "release version"),
    "result": ("result", "results", "outcome", "status"),
}

CAPABILITY_SECTION_KEYS = ("goal", "result", "changed_files", "version")
RELEASE_SECTION_KEYS = ("commit", "pr")
REQUIRED_GOVERNANCE = {
    "read_only": True,
    "proposal_governed": True,
    "dry_run": True,
    "would_write_memory": False,
    "would_modify_config": False,
    "would_write_graph": False,
    "writes_proposal_files": False,
    "writes_operation_ledger": False,
    "writes_token_files": False,
    "writes_approval_audit": False,
    "invokes_real_token_write_executor": False,
    "implements_real_token_write_executor": False,
    "exposes_provider_tools": False,
}

HIGH_RISK_PATTERNS = (
    re.compile(r"\bauth(?:entication|orization)?\b", re.IGNORECASE),
    re.compile(r"\btokens?\b", re.IGNORECASE),
    re.compile(r"\bcredentials?\b", re.IGNORECASE),
    re.compile(r"\bwrit(?:e|es|ing|ten)\b", re.IGNORECASE),
    re.compile(r"\bwrote\b", re.IGNORECASE),
    re.compile(r"\bapprov(?:al|als|e|es|ed|ing)\b", re.IGNORECASE),
    re.compile(r"\bexecutors?\b", re.IGNORECASE),
    re.compile(r"\bdelet(?:e|es|ed|ing|ion|ions)\b", re.IGNORECASE),
    re.compile(r"\bmigrat(?:e|es|ed|ing|ion|ions)\b", re.IGNORECASE),
)

_HEADING_MARKDOWN_RE = re.compile(r"^\s{0,3}#{1,6}\s+")
_BOLD_WRAPPER_RE = re.compile(r"^\*{1,2}(.+?)\*{1,2}$")
_SPACE_RE = re.compile(r"\s+")
_HEADING_WORD_RE = re.compile(r"[^a-z0-9/ ]+")
_SLUG_RE = re.compile(r"[^a-z0-9]+")


def parse_codex_task_summary(text: Any) -> dict[str, Any]:
    """Parse recognized structured Codex summary sections without side effects."""

    raw_text = "" if text is None else str(text)
    sections: list[dict[str, Any]] = []
    current: dict[str, Any] | None = None

    for line_number, raw_line in enumerate(raw_text.splitlines(), start=1):
        heading = _match_section_heading(raw_line)
        if heading is not None:
            if current is not None:
                sections.append(_finalize_section(current))
            key, heading_text, inline_content = heading
            current = {
                "key": key,
                "heading": heading_text,
                "lines": [],
                "line_start": line_number,
                "line_end": line_number,
            }
            if inline_content:
                current["lines"].append(inline_content)
            continue

        if current is not None:
            current["lines"].append(raw_line.rstrip())
            current["line_end"] = line_number

    if current is not None:
        sections.append(_finalize_section(current))

    section_map: dict[str, list[dict[str, Any]]] = {}
    for section in sections:
        section_map.setdefault(section["key"], []).append(deepcopy(section))

    return {
        "input_sha256": _sha256_text(raw_text),
        "sections": sections,
        "section_map": section_map,
    }


def parse_codex_task_summary_sections(text: Any) -> list[dict[str, Any]]:
    """Return parsed section records for callers that only need sections."""

    return deepcopy(list(parse_codex_task_summary(text)["sections"]))


def generate_codex_task_summary_candidates(
    text: Any,
    *,
    project_id: str = DEFAULT_PROJECT_ID,
    source: str = DEFAULT_SOURCE,
    created_at: str = DEFAULT_CREATED_AT,
) -> list[dict[str, Any]]:
    """Generate deterministic dry-run candidate records from a Codex summary."""

    raw_text = "" if text is None else str(text)
    parsed = parse_codex_task_summary(raw_text)
    clean_project_id = _clean_text(project_id) or DEFAULT_PROJECT_ID
    clean_source = _clean_text(source) or DEFAULT_SOURCE
    clean_created_at = _clean_text(created_at) or DEFAULT_CREATED_AT
    candidates: list[dict[str, Any]] = []

    capability_sections = _sections_for_keys(parsed["sections"], CAPABILITY_SECTION_KEYS)
    if capability_sections:
        candidates.append(
            _candidate(
                kind="capability",
                sections=capability_sections,
                project_id=clean_project_id,
                source=clean_source,
                created_at=clean_created_at,
                input_sha256=parsed["input_sha256"],
            )
        )

    validation_sections = _sections_for_keys(parsed["sections"], ("validation",))
    if validation_sections:
        candidates.append(
            _candidate(
                kind="validation",
                sections=validation_sections,
                project_id=clean_project_id,
                source=clean_source,
                created_at=clean_created_at,
                input_sha256=parsed["input_sha256"],
            )
        )

    boundary_sections = _sections_for_keys(parsed["sections"], ("boundary",))
    if boundary_sections:
        candidates.append(
            _candidate(
                kind="boundary",
                sections=boundary_sections,
                project_id=clean_project_id,
                source=clean_source,
                created_at=clean_created_at,
                input_sha256=parsed["input_sha256"],
            )
        )

    release_sections = _sections_for_keys(parsed["sections"], RELEASE_SECTION_KEYS)
    if release_sections:
        candidates.append(
            _candidate(
                kind="release_reference",
                sections=release_sections,
                project_id=clean_project_id,
                source=clean_source,
                created_at=clean_created_at,
                input_sha256=parsed["input_sha256"],
            )
        )

    return deepcopy(candidates)


def ingest_codex_task_summary_dry_run(
    text: Any,
    *,
    project_id: str = DEFAULT_PROJECT_ID,
    source: str = DEFAULT_SOURCE,
    created_at: str = DEFAULT_CREATED_AT,
) -> list[dict[str, Any]]:
    """Alias for the v1.3.0 dry-run ingestion entry point."""

    return generate_codex_task_summary_candidates(
        text,
        project_id=project_id,
        source=source,
        created_at=created_at,
    )


def candidates_to_jsonl(candidates: Iterable[Mapping[str, Any]]) -> str:
    """Serialize candidates as deterministic JSONL."""

    lines = [
        json.dumps(dict(candidate), sort_keys=True, separators=(",", ":"))
        for candidate in candidates
        if isinstance(candidate, Mapping)
    ]
    return "\n".join(lines) + ("\n" if lines else "")


def write_candidates_jsonl(candidates: Iterable[Mapping[str, Any]], output_path: Any) -> Path:
    """Write JSONL only to the explicit output path supplied by the caller."""

    path = Path(output_path)
    path.write_text(candidates_to_jsonl(candidates), encoding="utf-8")
    return path


def detect_codex_task_summary_risk_level(text: Any) -> str:
    """Return high when explicit high-risk terms appear, otherwise low."""

    value = "" if text is None else str(text)
    return "high" if any(pattern.search(value) for pattern in HIGH_RISK_PATTERNS) else "low"


def summarize_candidate_batch(candidates: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    """Return a compact deterministic summary of a candidate batch."""

    candidate_list = [dict(candidate) for candidate in candidates if isinstance(candidate, Mapping)]
    kinds = Counter(_candidate_kind(candidate) for candidate in candidate_list)
    risks = Counter(str(candidate.get("risk_level") or "") for candidate in candidate_list)
    return {
        "candidate_count": len(candidate_list),
        "kinds": {key: kinds[key] for key in sorted(kinds)},
        "risk_levels": {key: risks[key] for key in sorted(risks)},
        "dry_run": all(
            isinstance(candidate.get("governance"), Mapping)
            and candidate["governance"].get("dry_run") is True
            for candidate in candidate_list
        ),
    }


def cli_main(
    argv: list[str] | None = None,
    *,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
) -> int:
    """Run the dry-run ingestion CLI."""

    out = stdout if stdout is not None else sys.stdout
    err = stderr if stderr is not None else sys.stderr
    parser = argparse.ArgumentParser(description="Dry-run ingest a Codex task summary into Memory Fabric JSONL.")
    parser.add_argument("--input", required=True, help="Path to a structured Codex task summary text file.")
    parser.add_argument("--output", help="Optional explicit output JSONL path. Defaults to stdout.")
    parser.add_argument("--project-id", default=DEFAULT_PROJECT_ID)
    parser.add_argument("--source", default=DEFAULT_SOURCE)
    parser.add_argument("--print-summary", action="store_true")
    args = parser.parse_args(argv)

    input_text = Path(args.input).read_text(encoding="utf-8")
    candidates = generate_codex_task_summary_candidates(
        input_text,
        project_id=args.project_id,
        source=args.source,
    )
    if args.output:
        write_candidates_jsonl(candidates, args.output)
    else:
        out.write(candidates_to_jsonl(candidates))

    if args.print_summary:
        summary = summarize_candidate_batch(candidates)
        err.write("codex_task_summary_ingestion_summary=")
        err.write(json.dumps(summary, sort_keys=True, separators=(",", ":")))
        err.write("\n")

    return 0


def _match_section_heading(line: str) -> tuple[str, str, str] | None:
    stripped = line.strip()
    if not stripped:
        return None

    candidate = _HEADING_MARKDOWN_RE.sub("", stripped).strip()
    bold_match = _BOLD_WRAPPER_RE.match(candidate)
    if bold_match:
        candidate = bold_match.group(1).strip()

    heading_text = candidate
    inline_content = ""
    if ":" in candidate:
        possible_heading, possible_inline = candidate.split(":", 1)
        if possible_heading.strip():
            heading_text = possible_heading.strip()
            inline_content = possible_inline.strip()

    normalized = _normalize_heading(heading_text)
    for key, aliases in SECTION_ALIASES.items():
        normalized_aliases = {_normalize_heading(alias) for alias in aliases}
        if normalized in normalized_aliases:
            return key, heading_text.strip(), inline_content
    return None


def _finalize_section(section: Mapping[str, Any]) -> dict[str, Any]:
    lines = [str(line).rstrip() for line in section.get("lines", [])]
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    content = "\n".join(lines).strip()
    return {
        "key": str(section.get("key") or ""),
        "heading": str(section.get("heading") or ""),
        "content": content,
        "line_start": int(section.get("line_start") or 0),
        "line_end": int(section.get("line_end") or section.get("line_start") or 0),
    }


def _sections_for_keys(sections: Iterable[Mapping[str, Any]], keys: Iterable[str]) -> list[dict[str, Any]]:
    key_set = set(keys)
    selected: list[dict[str, Any]] = []
    for section in sections:
        if section.get("key") in key_set and _clean_text(section.get("content")):
            selected.append(deepcopy(dict(section)))
    return selected


def _candidate(
    *,
    kind: str,
    sections: list[dict[str, Any]],
    project_id: str,
    source: str,
    created_at: str,
    input_sha256: str,
) -> dict[str, Any]:
    content = "\n\n".join(_section_block(section) for section in sections if _section_block(section))
    candidate_id = _candidate_id(
        source=source,
        project_id=project_id,
        kind=kind,
        content=content,
    )
    section_keys = [str(section.get("key") or "") for section in sections]
    provenance = {
        "ingestion": "codex_task_summary_dry_run",
        "version": CODEX_TASK_SUMMARY_INGESTION_VERSION,
        "source": source,
        "input_sha256": input_sha256,
        "sections": [
            {
                "key": section.get("key"),
                "heading": section.get("heading"),
                "line_start": section.get("line_start"),
                "line_end": section.get("line_end"),
            }
            for section in sections
        ],
    }
    return {
        "id": candidate_id,
        "content": content,
        "project_id": project_id,
        "entity_ids": [project_id],
        "source": source,
        "source_id": candidate_id,
        "provenance": provenance,
        "risk_level": detect_codex_task_summary_risk_level(content),
        "governance": dict(REQUIRED_GOVERNANCE),
        "created_at": created_at,
        "tags": _candidate_tags(kind, section_keys),
    }


def _candidate_id(*, source: str, project_id: str, kind: str, content: str) -> str:
    payload = json.dumps(
        {
            "content": content,
            "kind": kind,
            "project_id": project_id,
            "source": source,
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    digest = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]
    return f"{_slug(source)}:{_slug(project_id)}:{_slug(kind)}:{digest}"


def _candidate_tags(kind: str, section_keys: Iterable[str]) -> list[str]:
    tags = ["codex-task-summary", "dry-run", kind]
    tags.extend(f"section:{key}" for key in section_keys if key)
    if kind == "validation":
        tags.append("validation-evidence")
    if kind == "boundary":
        tags.append("boundary-limitation")
    return _dedupe(tags)


def _candidate_kind(candidate: Mapping[str, Any]) -> str:
    tags = [str(tag) for tag in candidate.get("tags", []) if str(tag)]
    for known in ("capability", "validation", "boundary", "release_reference"):
        if known in tags:
            return known
    return "unknown"


def _section_block(section: Mapping[str, Any]) -> str:
    heading = _clean_text(section.get("heading"))
    content = _clean_text(section.get("content"))
    if heading and content:
        return f"{heading}\n{content}"
    return content or heading


def _normalize_heading(value: Any) -> str:
    text = str(value).strip().lower()
    text = text.replace("&", " and ")
    text = _HEADING_WORD_RE.sub(" ", text.replace("/", " / "))
    text = _SPACE_RE.sub(" ", text).strip()
    text = text.replace(" / ", " ")
    return _SPACE_RE.sub(" ", text).strip()


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _slug(value: str) -> str:
    text = _SLUG_RE.sub("-", str(value).strip().lower()).strip("-")
    return text or "unknown"


def _clean_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _dedupe(values: Iterable[str]) -> list[str]:
    deduped: list[str] = []
    seen: set[str] = set()
    for value in values:
        text = str(value)
        if text and text not in seen:
            seen.add(text)
            deduped.append(text)
    return deduped


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(cli_main())
