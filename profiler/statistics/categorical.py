from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd


@dataclass(slots=True)
class CategoricalStats:
    """Statistical summary for a categorical/string column."""

    distinct_count: int
    top_values: list[tuple[str, int]]    # [(value, count), ...]
    bottom_values: list[tuple[str, int]] # [(value, count), ...]
    most_frequent: str | None
    most_frequent_count: int
    most_frequent_pct: float
    least_frequent: str | None
    least_frequent_count: int
    least_frequent_pct: float


class CategoricalAnalyzer:
    """Computes statistics for categorical/string columns."""

    @staticmethod
    def analyze(series: pd.Series, top_n: int = 5) -> CategoricalStats:
        """
        Analyzes a categorical pandas Series.
        NaN values are excluded from frequency counts.
        """
        clean = series.dropna().astype(str)
        total = len(clean)

        if clean.empty:
            return CategoricalStats(
                distinct_count=0,
                top_values=[],
                bottom_values=[],
                most_frequent=None,
                most_frequent_count=0,
                most_frequent_pct=0.0,
                least_frequent=None,
                least_frequent_count=0,
                least_frequent_pct=0.0,
            )

        counts = clean.value_counts()
        distinct_count = len(counts)

        top_values = [
            (str(val), int(cnt))
            for val, cnt in counts.head(top_n).items()
        ]
        bottom_values = [
            (str(val), int(cnt))
            for val, cnt in counts.tail(top_n).items()
        ]

        most_frequent = str(counts.index[0])
        most_frequent_count = int(counts.iloc[0])
        most_frequent_pct = round((most_frequent_count / total) * 100, 2) if total else 0.0

        least_frequent = str(counts.index[-1])
        least_frequent_count = int(counts.iloc[-1])
        least_frequent_pct = round((least_frequent_count / total) * 100, 2) if total else 0.0

        return CategoricalStats(
            distinct_count=distinct_count,
            top_values=top_values,
            bottom_values=bottom_values,
            most_frequent=most_frequent,
            most_frequent_count=most_frequent_count,
            most_frequent_pct=most_frequent_pct,
            least_frequent=least_frequent,
            least_frequent_count=least_frequent_count,
            least_frequent_pct=least_frequent_pct,
        )

    @staticmethod
    def is_categorical(series: pd.Series) -> bool:
        """Returns True if the series holds string/object/category data."""
        dtype_name = str(series.dtype)
        return (
            pd.api.types.is_object_dtype(series)
            or pd.api.types.is_string_dtype(series)
            or dtype_name in ("object", "string", "category")
        )
