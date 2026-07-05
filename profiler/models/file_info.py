from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class FileInfo:
    """Stores metadata about the source file of a dataset."""

    name: str
    extension: str
    path: str
    size: int
    created: str
    modified: str
