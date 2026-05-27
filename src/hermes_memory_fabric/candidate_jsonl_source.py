"""Read-only JSONL memory candidate source."""

from __future__ import annotations

import json
import os
from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable, Mapping
from urllib.parse import urlsplit


DEFAULT_CANDIDATE_JSONL_MAX_LINES = 1000
DEFAULT_CANDIDATE_JSONL_MAX_BYTES = 1_048_576
DEFAULT_CANDIDATE_JSONL_IGNORE_INVALID_LINES = True


def load_candidate_jsonl_source(
    path: Any,
    *,
    max_lines: Any = DEFAULT_CANDIDATE_JSONL_MAX_LINES,
    max_bytes: Any = DEFAULT_CANDIDATE_JSONL_MAX_BYTES,
    required_fields: Iterable[Any] | None = None,
    ignore_invalid_lines: bool = DEFAULT_CANDIDATE_JSONL_IGNORE_INVALID_LINES,
) -> list[dict[str, Any]]:
    """Load bounded memory candidates from an existing local JSONL file.

    The source is intentionally conservative: it rejects URLs and directories,
    reads at most the configured line/byte limits, parses one JSON object per
    non-blank line, and returns [] on any source-level failure.
    """

    candidate_path = _local_existing_file_path(path)
    if candidate_path is None:
        return []

    line_limit = _non_negative_int(max_lines, DEFAULT_CANDIDATE_JSONL_MAX_LINES)
    byte_limit = _non_negative_int(max_bytes, DEFAULT_CANDIDATE_JSONL_MAX_BYTES)
    if line_limit <= 0 or byte_limit <= 0:
        return []

    required = _required_fields(required_fields)
    candidates: list[dict[str, Any]] = []
    bytes_read = 0
    lines_read = 0

    try:
        source_size = candidate_path.stat().st_size
        with candidate_path.open("rb") as handle:
            while lines_read < line_limit and bytes_read < byte_limit:
                remaining = byte_limit - bytes_read
                raw_line = handle.readline(remaining)
                if raw_line == b"":
                    break

                bytes_read += len(raw_line)
                lines_read += 1

                is_partial_limit_line = (
                    bytes_read >= byte_limit
                    and source_size > bytes_read
                    and not raw_line.endswith((b"\n", b"\r"))
                )
                if is_partial_limit_line:
                    break

                candidate = _parse_candidate_line(
                    raw_line=raw_line,
                    required_fields=required,
                    ignore_invalid_lines=ignore_invalid_lines,
                )
                if candidate is _STRICT_INVALID:
                    return []
                if candidate is not None:
                    candidates.append(candidate)
    except OSError:
        return []

    return deepcopy(candidates)


_STRICT_INVALID = object()


def _parse_candidate_line(
    *,
    raw_line: bytes,
    required_fields: tuple[str, ...],
    ignore_invalid_lines: bool,
) -> dict[str, Any] | object | None:
    try:
        line = raw_line.decode("utf-8")
    except UnicodeDecodeError:
        return None if ignore_invalid_lines else _STRICT_INVALID

    if not line.strip():
        return None

    try:
        value = json.loads(line)
    except json.JSONDecodeError:
        return None if ignore_invalid_lines else _STRICT_INVALID

    if not isinstance(value, Mapping):
        return None if ignore_invalid_lines else _STRICT_INVALID

    candidate = deepcopy(dict(value))
    if any(field not in candidate for field in required_fields):
        return None if ignore_invalid_lines else _STRICT_INVALID

    return candidate


def _local_existing_file_path(path: Any) -> Path | None:
    text = _optional_text(path)
    if text is None or _looks_like_url(text):
        return None

    candidate_path = Path(os.path.expanduser(text))
    try:
        if not candidate_path.exists() or candidate_path.is_dir() or not candidate_path.is_file():
            return None
    except OSError:
        return None
    return candidate_path


def _looks_like_url(value: str) -> bool:
    parsed = urlsplit(value)
    return bool(parsed.scheme or parsed.netloc)


def _required_fields(value: Iterable[Any] | None) -> tuple[str, ...]:
    if value is None:
        return ()
    if isinstance(value, (str, bytes, bytearray)):
        values = [value]
    else:
        try:
            values = list(value)
        except TypeError:
            values = [value]
    required: list[str] = []
    seen: set[str] = set()
    for item in values:
        text = _optional_text(item)
        if text and text not in seen:
            seen.add(text)
            required.append(text)
    return tuple(required)


def _optional_text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _non_negative_int(value: Any, default: int) -> int:
    try:
        return max(0, int(value))
    except (TypeError, ValueError):
        return default
