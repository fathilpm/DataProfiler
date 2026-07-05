from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(slots=True)
class BooleanStats:
    """Statistical summary for a boolean column."""

    true_count: int
    false_count: int
    true_pct: float
    false_pct: float
    null_count: int


class BooleanAnalyzer:
    """Computes statistics for boolean columns."""

    @staticmethod
    def analyze(series: pd.Series) -> BooleanStats:
        """
        Analyzes a boolean pandas Series.
        NaN values are tracked separately.
        """
        null_count = int(series.isna().sum())
        clean = series.dropna()
        total = len(clean)

        if total == 0:
            return BooleanStats(
                true_count=0,
                false_count=0,
                true_pct=0.0,
                false_pct=0.0,
                null_count=null_count,
            )

        true_count = int(clean.sum())
        false_count = total - true_count

        return BooleanStats(
            true_count=true_count,
            false_count=false_count,
            true_pct=round((true_count / total) * 100, 2),
            false_pct=round((false_count / total) * 100, 2),
            null_count=null_count,
        )

    @staticmethod
    def is_boolean(series: pd.Series) -> bool:
        """Returns True if the series holds boolean data."""
        return pd.api.types.is_bool_dtype(series)
