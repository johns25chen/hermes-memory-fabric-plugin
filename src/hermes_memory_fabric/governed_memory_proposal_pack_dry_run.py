"""v2.4.0 governed memory proposal pack dry-run builder."""

from __future__ import annotations

import hashlib
import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping


GOVERNED_MEMORY_PROPOSAL_PACK_DRY_RUN_VERSION = "2.4.0"

REQUIRED_SECTION_SLUGS = (
    "long_term_memory_candidates",
    "short_term_memory_candidates",
    "operation_ledger_candidates",
    "knowledge_surface_candidates",
    "do_not_persist",
    "risk_notes",
)

SECTION_TITLES = {
    "long_term_memory_candidates": "Long-Term Memory Candidates",
    "short_term_memory_candidates": "Short-Term Memory Candidates",
    "operation_ledger_candidates": "Operation Ledger Candidates",
    "knowledge_surface_candidates": "Knowledge Surface Candidates",
    "do_not_persist": "Do Not Persist",
    "risk_notes": "Risk Notes",
}

SECTION_TARGETS = {
    "long_term_memory_candidates": "long_term_memory",
    "short_term_memory_candidates": "short_term_memory",
    "operation_ledger_candidates": "operation_ledger",
    "knowledge_surface_candidates": "knowledge_surface",
    "do_not_persist": "rejected_do_not_persist",
    "risk_notes": "risk_note",
}

NO_WRITE_FLAGS = {
    "writes_memory": False,
    "writes_graph": False,
    "writes_operation_ledger": False,
    "writes_config": False,
    "writes_sqlite": False,
    "invokes_real_executor": False,
    "provider_tools": [],
}

REAL_SURFACE_FALSE_FLAGS = {
    "creates_real_memory_write_proposal": False,
    "creates_real_operation_ledger_entry": False,
    "modifies_hermes_agent": False,
    "no_network_surface": True,
}

NON_DURABLE_PATTERNS = (
    ("temporary_command_authorization", re.compile(r"\btemporary\b.*\b(command|authorization|approval)", re.I)),
    ("one_off_temporary_state", re.compile(r"\b(one[- ]off|temporary|current task state|unfinished work)\b", re.I)),
    ("api_key_or_secret", re.compile(r"\b(api key|api keys|secret|secrets|credential|credentials|password)\b", re.I)),
    ("docker_log_or_temp_path_or_pid", re.compile(r"\b(docker logs?|docker layer|/private/tmp|temporary pids?|pid\b|ports?)\b", re.I)),
    ("raw_credentials", re.compile(r"\b(raw credential|plaintext api key|durable secret|authentication password)\b", re.I)),
)


def build_governed_memory_proposal_pack_dry_run(proposal_path: str | Path) -> dict[str, Any]:
    """Build a deterministic governed proposal pack without writing any memory surface."""

    path = Path(proposal_path).expanduser().resolve()
    text = path.read_text(encoding="utf-8")
    source_sha256 = hashlib.sha256(text.encode("utf-8")).hexdigest()
    section_map = _parse_section_map(text)
    sections_present = [slug for slug in REQUIRED_SECTION_SLUGS if slug in section_map]
    missing_sections = [slug for slug in REQUIRED_SECTION_SLUGS if slug not in section_map]

    entries: list[dict[str, Any]] = []
    for section_slug in REQUIRED_SECTION_SLUGS:
        section_text = section_map.get(section_slug, "")
        for index, entry in enumerate(_entries_for_section(section_slug, section_text), start=1):
            entries.append(_build_entry(section_slug, index, entry, source_sha256))

    proposed_entries = [entry for entry in entries if entry["status"] == "proposed"]
    rejected_entries = [
        entry for entry in entries if entry["status"] == "rejected" or entry["must_not_become_durable_memory"]
    ]
    risk_notes = [entry for entry in entries if entry["status"] == "risk_note"]
    pack_status = "ready" if not missing_sections else "blocked"

    result = {
        "version": GOVERNED_MEMORY_PROPOSAL_PACK_DRY_RUN_VERSION,
        "pack_status": pack_status,
        "source_path": path.as_posix(),
        "source_sha256": source_sha256,
        "entry_count": len(entries),
        "proposed_count": len(proposed_entries),
        "rejected_count": len([entry for entry in entries if entry["status"] == "rejected"]),
        "risk_note_count": len(risk_notes),
        "sections_present": sections_present,
        "missing_sections": missing_sections,
        "entries": entries,
        "rejected_entries": rejected_entries,
        "risk_notes": risk_notes,
        **deepcopy(NO_WRITE_FLAGS),
        **deepcopy(REAL_SURFACE_FALSE_FLAGS),
        "safety_summary": _safety_summary(entries, missing_sections, pack_status),
    }
    return deepcopy(result)


def governed_memory_proposal_pack_to_json(result: Mapping[str, Any]) -> str:
    """Serialize a v2.4.0 governed memory proposal pack report deterministically."""

    return json.dumps(dict(result), sort_keys=True, indent=2, ensure_ascii=True) + "\n"


def _parse_section_map(text: str) -> dict[str, str]:
    headings = list(re.finditer(r"^##\s+(.+?)\s*$", text, flags=re.MULTILINE))
    section_map: dict[str, str] = {}
    for index, heading in enumerate(headings):
        title = heading.group(1).strip()
        slug = _section_slug(title)
        if slug not in REQUIRED_SECTION_SLUGS:
            continue
        start = heading.end()
        end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
        section_map[slug] = text[start:end].strip()
    return section_map


def _entries_for_section(section_slug: str, section_text: str) -> list[dict[str, str]]:
    if not section_text.strip():
        return []
    subheadings = list(re.finditer(r"^###\s+(.+?)\s*$", section_text, flags=re.MULTILINE))
    if not subheadings:
        return [{"entry_key": section_slug, "content": section_text.strip()}]

    entries: list[dict[str, str]] = []
    for index, heading in enumerate(subheadings):
        title = heading.group(1).strip()
        start = heading.end()
        end = subheadings[index + 1].start() if index + 1 < len(subheadings) else len(section_text)
        content = section_text[start:end].strip()
        if content:
            entries.append({"entry_key": _entry_key(title), "content": content})
    return entries


def _build_entry(
    section_slug: str,
    section_index: int,
    raw_entry: Mapping[str, str],
    source_sha256: str,
) -> dict[str, Any]:
    entry_key = raw_entry["entry_key"]
    content = raw_entry["content"].strip()
    reasons = _non_durable_reasons(section_slug, entry_key, content)
    target_surface = SECTION_TARGETS[section_slug]
    status = _entry_status(section_slug, reasons)
    if status == "rejected":
        target_surface = "rejected_do_not_persist"

    proposal_id = _proposal_id(
        section_slug=section_slug,
        section_index=section_index,
        entry_key=entry_key,
        content=content,
        source_sha256=source_sha256,
    )
    return {
        "proposal_id": proposal_id,
        "entry_key": entry_key,
        "section": section_slug,
        "section_title": SECTION_TITLES[section_slug],
        "section_index": section_index,
        "target_surface": target_surface,
        "status": status,
        "content": content,
        "must_not_become_durable_memory": bool(reasons) or section_slug == "do_not_persist",
        "non_durable_reasons": reasons,
        **deepcopy(NO_WRITE_FLAGS),
    }


def _entry_status(section_slug: str, non_durable_reasons: list[str]) -> str:
    if section_slug == "risk_notes":
        return "risk_note"
    if section_slug == "do_not_persist" or non_durable_reasons:
        return "rejected"
    return "proposed"


def _non_durable_reasons(section_slug: str, entry_key: str, content: str) -> list[str]:
    haystack = f"{entry_key}\n{content}"
    if section_slug == "do_not_persist" or section_slug == "risk_notes":
        return _dedupe(reason for reason, pattern in NON_DURABLE_PATTERNS if pattern.search(haystack))
    if entry_key == "temporary_command_authorizations":
        return ["temporary_command_authorization"]
    return []


def _proposal_id(
    *,
    section_slug: str,
    section_index: int,
    entry_key: str,
    content: str,
    source_sha256: str,
) -> str:
    digest = hashlib.sha256(
        "\n".join(
            (
                GOVERNED_MEMORY_PROPOSAL_PACK_DRY_RUN_VERSION,
                source_sha256,
                section_slug,
                str(section_index),
                entry_key,
                content,
            )
        ).encode("utf-8")
    ).hexdigest()[:24]
    return f"gmpp-dry-run-{digest}"


def _section_slug(title: str) -> str:
    return _entry_key(title.replace("&", " and "))


def _entry_key(title: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", title.strip().lower())
    return slug.strip("_")


def _dedupe(values: Any) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        clean = str(value).strip()
        if clean and clean not in seen:
            seen.add(clean)
            result.append(clean)
    return result


def _safety_summary(
    entries: list[dict[str, Any]],
    missing_sections: list[str],
    pack_status: str,
) -> dict[str, Any]:
    rejected = [entry for entry in entries if entry["status"] == "rejected"]
    risk_notes = [entry for entry in entries if entry["status"] == "risk_note"]
    return {
        "adapter": "governed_memory_proposal_pack_dry_run",
        "version": GOVERNED_MEMORY_PROPOSAL_PACK_DRY_RUN_VERSION,
        "dry_run_only": True,
        "pack_status": pack_status,
        "local_file_parsing_only": True,
        "missing_sections": list(missing_sections),
        "entry_count": len(entries),
        "proposed_count": len([entry for entry in entries if entry["status"] == "proposed"]),
        "rejected_count": len(rejected),
        "risk_note_count": len(risk_notes),
        "rejected_entry_keys": [entry["entry_key"] for entry in rejected],
        "risk_note_entry_keys": [entry["entry_key"] for entry in risk_notes],
        "writes_memory": False,
        "writes_graph": False,
        "writes_operation_ledger": False,
        "writes_config": False,
        "writes_sqlite": False,
        "invokes_real_executor": False,
        "provider_tools": [],
        "creates_real_memory_write_proposal": False,
        "creates_real_operation_ledger_entry": False,
        "modifies_hermes_agent": False,
        "no_network_surface": True,
    }


__all__ = [
    "GOVERNED_MEMORY_PROPOSAL_PACK_DRY_RUN_VERSION",
    "build_governed_memory_proposal_pack_dry_run",
    "governed_memory_proposal_pack_to_json",
]
