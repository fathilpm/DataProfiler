from dataclasses import dataclass, field
from typing import Any


@dataclass
class ColumnProfile:
    """Stores profiling information for a single column."""

    name: str
    dtype: str
    missing_count: int
    missing_percentage: float
    unique_count: int
    memory_usage: int


@dataclass
class DatasetProfile:
    """Stores profiling information for an entire dataset."""

    dataset_name: str

    rows: int
    columns: int

    duplicate_rows: int

    memory_usage: int

    preview: list[dict[str, Any]] = field(default_factory=list)

    column_profiles: list[ColumnProfile] = field(default_factory=list)