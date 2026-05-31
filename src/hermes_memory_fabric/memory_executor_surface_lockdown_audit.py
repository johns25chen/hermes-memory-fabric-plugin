"""v1.6 source-only audit for executor-adjacent write surfaces.

The audit is intentionally static. It reads repository source files with
``Path.read_text`` and parses Python syntax with ``ast`` instead of importing
the modules being audited.
"""

from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any, Iterable, Mapping


MEMORY_EXECUTOR_SURFACE_LOCKDOWN_AUDIT_VERSION = "1.6.0"

FORBIDDEN_MODULE_FILENAMES = ("memory_human_approval_token_real_write_executor.py",)
FORBIDDEN_TEST_FILENAMES = ("test_memory_human_approval_token_real_write_executor.py",)
FORBIDDEN_WRITE_PROPOSAL_CALLS = {
    "memory_fabric_bridge.create_memory_write_proposal",
    "create_memory_write_proposal",
}

REQUIRED_NO_WRITE_FLAGS = (
    "invokes_real_token_write_executor",
    "implements_real_token_write_executor",
    "issues_real_approval_tokens",
    "writes_operation_ledger",
    "writes_token_files",
    "writes_approval_audit",
    "applies_proposals",
)

V15_REQUIRED_FALSE_FLAGS = (
    "created_real_proposal",
    "writes_proposal_files",
    "writes_operation_ledger",
    "writes_memory",
    "writes_graph",
    "writes_config",
    "writes_sqlite",
    "writes_token_files",
    "writes_approval_audit",
    "applies_proposals",
)

TARGET_KEYWORDS = (
    "approval",
    "token",
    "executor",
    "write_lock",
    "ledger",
)

WRITE_MODE_CHARS = frozenset({"w", "a", "x", "+"})
SQLITE_WRITE_PREFIXES = (
    "insert",
    "update",
    "delete",
    "replace",
    "create",
    "drop",
    "alter",
    "vacuum",
    "attach",
    "detach",
)
LEDGER_WRITE_CALL_NAMES = {
    "append_operation_ledger",
    "append_operation_ledger_event",
    "append_ledger",
    "append_ledger_event",
    "create_operation_event",
    "record_operation_ledger",
    "record_operation_ledger_event",
    "write_operation_ledger",
    "write_operation_ledger_event",
}


def audit_executor_surface_lockdown(repo_root: str | Path = ".") -> dict[str, Any]:
    """Return a deterministic read-only audit report for the repository."""

    root = Path(repo_root).expanduser().resolve(strict=False)
    source_files, skipped_files = _discover_python_files(root)
    source_by_rel = _read_source_files(root, source_files)

    forbidden_files_present = _forbidden_files_present(source_files)
    forbidden_calls = _find_forbidden_calls(source_by_rel)
    provider_tools, provider_exposure = _provider_tools_status(source_by_rel)
    forbidden_write_surfaces = _find_forbidden_write_surfaces(root, source_by_rel)
    missing_no_write_flags = _missing_no_write_flags(source_by_rel)
    v15_boundary = _v15_boundary_status(source_by_rel)

    failure_lists = (
        forbidden_files_present,
        forbidden_calls,
        provider_exposure,
        forbidden_write_surfaces,
        missing_no_write_flags,
        v15_boundary["errors"],
    )
    audit_passed = all(not failures for failures in failure_lists)

    return {
        "version": MEMORY_EXECUTOR_SURFACE_LOCKDOWN_AUDIT_VERSION,
        "dry_run": True,
        "audit_status": "pass" if audit_passed else "fail",
        "provider_tools": provider_tools,
        "scanned_files": sorted(source_by_rel),
        "skipped_files": skipped_files,
        "forbidden_files_present": forbidden_files_present,
        "forbidden_calls": forbidden_calls,
        "forbidden_write_surfaces": forbidden_write_surfaces,
        "required_no_write_flags": list(REQUIRED_NO_WRITE_FLAGS),
        "missing_no_write_flags": missing_no_write_flags,
        "v15_boundary_status": v15_boundary["status"],
        "safety_summary": {
            "audit": "memory_executor_surface_lockdown_audit",
            "version": MEMORY_EXECUTOR_SURFACE_LOCKDOWN_AUDIT_VERSION,
            "read_only_static_source_audit": True,
            "imports_audited_modules": False,
            "writes_hermes_home": False,
            "writes_proposal_files": False,
            "writes_operation_ledger": False,
            "writes_token_files": False,
            "writes_approval_audit": False,
            "applies_proposals": False,
            "creates_real_executor": False,
            "creates_approval_tokens": False,
            "provider_tool_exposure_detected": bool(provider_exposure),
            "provider_exposure": provider_exposure,
            "target_group_counts": _target_group_counts(source_by_rel),
            "v15_boundary_errors": v15_boundary["errors"],
        },
    }


def report_to_json(report: Mapping[str, Any]) -> str:
    """Serialize an audit report deterministically."""

    return json.dumps(dict(report), sort_keys=True, indent=2, ensure_ascii=True) + "\n"


def _discover_python_files(root: Path) -> tuple[list[str], list[str]]:
    files: list[str] = []
    skipped: list[str] = []
    search_roots = (
        root / "src" / "hermes_memory_fabric",
        root / "tests",
        root / "scripts",
    )
    for search_root in search_roots:
        if not search_root.exists():
            continue
        for path in sorted(search_root.rglob("*.py")):
            rel = _relative_path(root, path)
            if "__pycache__" in path.parts:
                skipped.append(rel)
                continue
            files.append(rel)
    return sorted(set(files)), sorted(set(skipped))


def _read_source_files(root: Path, rel_paths: Iterable[str]) -> dict[str, str]:
    source_by_rel: dict[str, str] = {}
    for rel in rel_paths:
        path = root / rel
        try:
            source_by_rel[rel] = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            source_by_rel[rel] = path.read_text(encoding="utf-8", errors="replace")
    return source_by_rel


def _forbidden_files_present(source_files: Iterable[str]) -> list[str]:
    forbidden: list[str] = []
    for rel in source_files:
        name = Path(rel).name
        if name in FORBIDDEN_MODULE_FILENAMES or name in FORBIDDEN_TEST_FILENAMES:
            forbidden.append(rel)
    return sorted(forbidden)


def _find_forbidden_calls(source_by_rel: Mapping[str, str]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for rel, source in source_by_rel.items():
        tree = _parse_source(rel, source)
        if tree is None:
            continue
        lines = source.splitlines()
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            call_name = _call_name(node.func)
            if _is_forbidden_write_proposal_call(call_name):
                findings.append(
                    _finding(
                        rel,
                        node,
                        "memory_fabric_bridge.create_memory_write_proposal",
                        lines,
                    )
                )
    return _sorted_findings(findings)


def _provider_tools_status(source_by_rel: Mapping[str, str]) -> tuple[list[Any], list[dict[str, Any]]]:
    rel = "src/hermes_memory_fabric/provider.py"
    source = source_by_rel.get(rel)
    if source is None:
        return ["MemoryFabricProvider.get_tool_schemas"], [
            {"path": rel, "line": 0, "surface": "missing_provider_source", "snippet": ""}
        ]

    tree = _parse_source(rel, source)
    if tree is None:
        return ["MemoryFabricProvider.get_tool_schemas"], [
            {"path": rel, "line": 0, "surface": "provider_source_parse_error", "snippet": ""}
        ]

    lines = source.splitlines()
    provider_class = _find_class(tree, "MemoryFabricProvider")
    if provider_class is None:
        return ["MemoryFabricProvider"], [
            {"path": rel, "line": 0, "surface": "missing_memory_fabric_provider", "snippet": ""}
        ]

    method = _find_function(provider_class, "get_tool_schemas")
    if method is None:
        return ["MemoryFabricProvider.get_tool_schemas"], [
            {"path": rel, "line": provider_class.lineno, "surface": "missing_get_tool_schemas", "snippet": ""}
        ]

    returns = [node for node in ast.walk(method) if isinstance(node, ast.Return)]
    if not returns:
        return ["MemoryFabricProvider.get_tool_schemas"], [
            _finding(rel, method, "get_tool_schemas_without_static_empty_return", lines)
        ]

    exposure: list[dict[str, Any]] = []
    for node in returns:
        if not _is_empty_list_literal(node.value):
            exposure.append(_finding(rel, node, "provider_tool_schema_return_not_empty_list", lines))
    if exposure:
        return ["MemoryFabricProvider.get_tool_schemas"], _sorted_findings(exposure)
    return [], []


def _find_forbidden_write_surfaces(root: Path, source_by_rel: Mapping[str, str]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for rel, source in source_by_rel.items():
        if not _is_write_surface_target(rel):
            continue
        tree = _parse_source(rel, source)
        if tree is None:
            continue
        lines = source.splitlines()
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            surface = _write_surface_for_call(node)
            if surface is None:
                continue
            if _has_preview_only_test_coverage(root, rel, source):
                continue
            findings.append(_finding(rel, node, surface, lines))
    return _sorted_findings(findings)


def _missing_no_write_flags(source_by_rel: Mapping[str, str]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for rel, source in source_by_rel.items():
        if not _is_real_write_executor_planning_or_review_source(rel):
            continue
        flags = _false_flags_in_source(rel, source)
        missing = [flag for flag in REQUIRED_NO_WRITE_FLAGS if flag not in flags]
        if missing:
            findings.append({"path": rel, "missing_flags": missing})
    return sorted(findings, key=lambda item: item["path"])


def _v15_boundary_status(source_by_rel: Mapping[str, str]) -> dict[str, Any]:
    rel = "src/hermes_memory_fabric/memory_candidate_proposal_dry_run.py"
    source = source_by_rel.get(rel)
    errors: list[str] = []
    if source is None:
        return {"status": "fail", "errors": ["missing_memory_candidate_proposal_dry_run.py"]}

    flags = _false_flags_in_source(rel, source)
    for flag in V15_REQUIRED_FALSE_FLAGS:
        if flag not in flags:
            errors.append(f"missing_{flag}_false")
    if not _contains_provider_tools_empty_list(rel, source):
        errors.append("missing_provider_tools_empty_list")
    if _source_has_forbidden_call(rel, source):
        errors.append("calls_memory_fabric_bridge.create_memory_write_proposal")

    return {"status": "pass" if not errors else "fail", "errors": sorted(errors)}


def _target_group_counts(source_by_rel: Mapping[str, str]) -> dict[str, int]:
    counts = {
        "approval_modules": 0,
        "token_modules": 0,
        "executor_modules": 0,
        "write_lock_modules": 0,
        "ledger_modules": 0,
        "tool_wrapper_modules": 0,
    }
    for rel in source_by_rel:
        name = Path(rel).name
        if rel.startswith("src/hermes_memory_fabric/tools/"):
            counts["tool_wrapper_modules"] += 1
        if not rel.startswith("src/hermes_memory_fabric/"):
            continue
        if "approval" in name:
            counts["approval_modules"] += 1
        if "token" in name:
            counts["token_modules"] += 1
        if "executor" in name:
            counts["executor_modules"] += 1
        if "write_lock" in name:
            counts["write_lock_modules"] += 1
        if "ledger" in name:
            counts["ledger_modules"] += 1
    return counts


def _is_write_surface_target(rel: str) -> bool:
    if rel.startswith("src/hermes_memory_fabric/tools/"):
        return True
    if not rel.startswith("src/hermes_memory_fabric/"):
        return False
    name = Path(rel).name
    return any(keyword in name for keyword in TARGET_KEYWORDS)


def _is_real_write_executor_planning_or_review_source(rel: str) -> bool:
    if not rel.startswith("src/hermes_memory_fabric/"):
        return False
    name = Path(rel).name
    if name in FORBIDDEN_MODULE_FILENAMES:
        return False
    if "real_write_executor" not in name:
        return False
    return any(keyword in name for keyword in ("plan", "planning", "review", "contract", "dry_run"))


def _false_flags_in_source(rel: str, source: str) -> set[str]:
    tree = _parse_source(rel, source)
    if tree is None:
        return set()
    flags: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            for key, value in zip(node.keys, node.values):
                if isinstance(key, ast.Constant) and isinstance(key.value, str):
                    if key.value in REQUIRED_NO_WRITE_FLAGS + V15_REQUIRED_FALSE_FLAGS:
                        if _is_false_literal(value):
                            flags.add(key.value)
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            names = _assigned_names(node)
            value = node.value
            if value is not None and _is_false_literal(value):
                flags.update(name for name in names if name in REQUIRED_NO_WRITE_FLAGS + V15_REQUIRED_FALSE_FLAGS)
    return flags


def _contains_provider_tools_empty_list(rel: str, source: str) -> bool:
    tree = _parse_source(rel, source)
    if tree is None:
        return False
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        for key, value in zip(node.keys, node.values):
            if isinstance(key, ast.Constant) and key.value == "provider_tools":
                if _is_empty_list_literal(value):
                    return True
    return False


def _source_has_forbidden_call(rel: str, source: str) -> bool:
    tree = _parse_source(rel, source)
    if tree is None:
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and _is_forbidden_write_proposal_call(_call_name(node.func)):
            return True
    return False


def _is_forbidden_write_proposal_call(call_name: str) -> bool:
    return call_name in FORBIDDEN_WRITE_PROPOSAL_CALLS or call_name.endswith(
        ".create_memory_write_proposal"
    )


def _write_surface_for_call(node: ast.Call) -> str | None:
    call_name = _call_name(node.func)
    short_name = call_name.rsplit(".", 1)[-1]

    if call_name == "open" and _call_uses_write_mode(node):
        return "direct_open_write_mode"
    if short_name == "open" and _call_uses_write_mode(node):
        return "path_open_write_mode"
    if short_name == "write_text":
        return "path_write_text"
    if short_name == "write_bytes":
        return "path_write_bytes"
    if short_name in {"execute", "executemany", "executescript"} and _call_uses_sqlite_write(node):
        return "sqlite_write_statement"
    if short_name in LEDGER_WRITE_CALL_NAMES or call_name in LEDGER_WRITE_CALL_NAMES:
        return "operation_ledger_append"
    return None


def _call_uses_write_mode(node: ast.Call) -> bool:
    mode = None
    if len(node.args) >= 2:
        mode = _constant_string(node.args[1])
    for keyword in node.keywords:
        if keyword.arg == "mode":
            mode = _constant_string(keyword.value)
    return isinstance(mode, str) and any(char in mode for char in WRITE_MODE_CHARS)


def _call_uses_sqlite_write(node: ast.Call) -> bool:
    if not node.args:
        return False
    sql = _constant_string(node.args[0])
    if not isinstance(sql, str):
        return False
    normalized = sql.strip().lower()
    return normalized.startswith(SQLITE_WRITE_PREFIXES)


def _has_preview_only_test_coverage(root: Path, rel: str, source: str) -> bool:
    lowered = source.lower()
    if "preview-only" not in lowered and "preview only" not in lowered:
        return False
    module_name = Path(rel).stem
    candidate_tests = [
        root / "tests" / f"test_{module_name}.py",
        root / "tests" / "tools" / f"test_{module_name}.py",
    ]
    return any(path.exists() for path in candidate_tests)


def _parse_source(rel: str, source: str) -> ast.AST | None:
    try:
        return ast.parse(source, filename=rel)
    except SyntaxError:
        return None


def _find_class(tree: ast.AST, name: str) -> ast.ClassDef | None:
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == name:
            return node
    return None


def _find_function(class_node: ast.ClassDef, name: str) -> ast.FunctionDef | ast.AsyncFunctionDef | None:
    for node in class_node.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name:
            return node
    return None


def _assigned_names(node: ast.Assign | ast.AnnAssign) -> set[str]:
    targets = node.targets if isinstance(node, ast.Assign) else [node.target]
    names: set[str] = set()
    for target in targets:
        if isinstance(target, ast.Name):
            names.add(target.id)
    return names


def _call_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = _call_name(node.value)
        return f"{parent}.{node.attr}" if parent else node.attr
    return ""


def _constant_string(node: ast.AST) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None


def _is_false_literal(node: ast.AST) -> bool:
    return isinstance(node, ast.Constant) and node.value is False


def _is_empty_list_literal(node: ast.AST | None) -> bool:
    return isinstance(node, ast.List) and not node.elts


def _finding(rel: str, node: ast.AST, surface: str, lines: list[str]) -> dict[str, Any]:
    line = int(getattr(node, "lineno", 0) or 0)
    snippet = lines[line - 1].strip() if 0 < line <= len(lines) else ""
    return {"path": rel, "line": line, "surface": surface, "snippet": snippet}


def _sorted_findings(findings: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        [dict(finding) for finding in findings],
        key=lambda item: (
            str(item.get("path", "")),
            int(item.get("line", 0) or 0),
            str(item.get("surface", "")),
            str(item.get("snippet", "")),
        ),
    )


def _relative_path(root: Path, path: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()
