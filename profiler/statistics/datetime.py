from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(slots=True)
class DatetimeStats:
    """Statistical summary for a datetime column."""

    earliest: str
    latest: str
    date_range_days: int
    most_frequent: str | None
    most_frequent_count: int
    null_count: int


class DatetimeAnalyzer:
    """Computes statistics for datetime columns."""

    _FMT = "%Y-%m-%d %H:%M:%S"

    @staticmethod
    def analyze(series: pd.Series) -> DatetimeStats:
        """
        Analyzes a datetime pandas Series.
        Attempts to parse object columns as datetime if not already.
        """
        # Try to coerce to datetime if needed
        if not pd.api.types.is_datetime64_any_dtype(series):
            try:
                series = pd.to_datetime(series, errors="coerce")
            except Exception:
                pass

        clean = series.dropna()
        null_count = int(series.isna().sum())

        if clean.empty:
            return DatetimeStats(
                earliest="N/A",
                latest="N/A",
                date_range_days=0,
                most_frequent=None,
                most_frequent_count=0,
                null_count=null_count,
            )

        earliest = clean.min()
        latest = clean.max()
        date_range_days = (latest - earliest).days

        # Most frequent date (by date only, not time)
        date_counts = clean.dt.date.value_counts()
        most_frequent = str(date_counts.index[0]) if not date_counts.empty else None
        most_frequent_count = int(date_counts.iloc[0]) if not date_counts.empty else 0

        fmt = DatetimeAnalyzer._FMT

        return DatetimeStats(
            earliest=earliest.strftime(fmt),
            latest=latest.strftime(fmt),
            date_range_days=date_range_days,
            most_frequent=most_frequent,
            most_frequent_count=most_frequent_count,
            null_count=null_count,
        )

    @staticmethod
    def is_datetime(series: pd.Series) -> bool:
        """Returns True if the series is datetime typed."""
        return pd.api.types.is_datetime64_any_dtype(series)
