from dataclasses import dataclass, field

from profiler.analyzers.completeness import CompletenessResult


@dataclass(slots=True)
class ColumnProfile:
    """Stores profiling information for a single column."""

    name: str
    dtype: str

    nullable: bool

    missing_count: int
    missing_percentage: float

    unique_count: int
    unique_percentage: float

    memory_usage: int


@dataclass(slots=True)
class DatasetProfile:
    """Stores profiling information for an entire dataset."""

    dataset_name: str

    rows: int
    columns: int

    duplicate_rows: int

    memory_usage: int

    completeness: CompletenessResult

    column_profiles: list[ColumnProfile] = field(default_factory=list)