from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from profiler.analyzers.completeness import CompletenessResult

if TYPE_CHECKING:
    from profiler.statistics.numeric import NumericStats
    from profiler.statistics.categorical import CategoricalStats
    from profiler.statistics.datetime import DatetimeStats
    from profiler.statistics.boolean import BooleanStats
    from profiler.quality.scoring import QualityReport, HealthScore


@dataclass(slots=True)
class ColumnProfile:
    """Stores profiling information for a single column."""

    # Core
    name: str
    dtype: str           # human-readable type
    raw_dtype: str       # original pandas dtype string

    nullable: bool

    missing_count: int
    missing_percentage: float

    unique_count: int
    unique_percentage: float

    memory_usage: int

    # Statistics (one will be set depending on column type)
    numeric_stats: "NumericStats | None" = None
    categorical_stats: "CategoricalStats | None" = None
    datetime_stats: "DatetimeStats | None" = None
    boolean_stats: "BooleanStats | None" = None


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

    # Quality (v0.4)
    quality_report: "QualityReport | None" = None
    health_score: "HealthScore | None" = None