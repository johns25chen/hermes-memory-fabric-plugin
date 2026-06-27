from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .p4_m0_subspace_memory import SubspaceMemoryStore


DEFAULT_WORKSPACE_SUBSPACE_MEMORY_DIR = ".local/subspace_memory"


@dataclass(frozen=True)
class WorkspaceSubspaceMemoryConfig:
    workspace_root: Path
    storage_dir: str | Path = DEFAULT_WORKSPACE_SUBSPACE_MEMORY_DIR

    @property
    def storage_root(self) -> Path:
        return resolve_workspace_subspace_memory_root(
            self.workspace_root,
            storage_dir=self.storage_dir,
        )


def resolve_workspace_subspace_memory_root(
    workspace_root: str | Path,
    storage_dir: str | Path = DEFAULT_WORKSPACE_SUBSPACE_MEMORY_DIR,
) -> Path:
    if workspace_root is None:
        raise ValueError("workspace_root_must_be_explicit")

    workspace = Path(workspace_root).expanduser().resolve(strict=False)
    if not workspace.exists():
        raise ValueError("workspace_root_must_exist")
    if not workspace.is_dir():
        raise ValueError("workspace_root_must_be_directory")

    storage_path = Path(storage_dir)
    if storage_path.is_absolute():
        raise ValueError("storage_dir_must_be_relative")
    if any(part == ".." for part in storage_path.parts):
        raise ValueError("storage_dir_must_not_escape_workspace")

    resolved = (workspace / storage_path).resolve(strict=False)
    try:
        resolved.relative_to(workspace)
    except ValueError as exc:
        raise ValueError("storage_dir_must_stay_inside_workspace") from exc
    return resolved


def create_workspace_subspace_memory_store(
    workspace_root: str | Path,
    storage_dir: str | Path = DEFAULT_WORKSPACE_SUBSPACE_MEMORY_DIR,
) -> SubspaceMemoryStore:
    return SubspaceMemoryStore(
        resolve_workspace_subspace_memory_root(
            workspace_root,
            storage_dir=storage_dir,
        )
    )
