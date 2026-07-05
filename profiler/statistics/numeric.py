from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(slots=True)
class NumericStats:
    """Statistical summary for a numeric column."""

    mean: float
    median: float
    mode: float | None
    std: float
    variance: float
    minimum: float
    maximum: float
    q1: float
    q3: float
    iqr: float
    skewness: float
    kurtosis: float
    zeros: int
    negatives: int


class NumericAnalyzer:
    """Computes descriptive statistics for numeric columns."""

    @staticmethod
    def analyze(series: pd.Series) -> NumericStats:
        """
        Analyzes a numeric pandas Series and returns a NumericStats result.
        NaN values are ignored in all calculations.
        """
        clean = series.dropna()

        if clean.empty:
            return NumericStats(
                mean=0.0, median=0.0, mode=None, std=0.0, variance=0.0,
                minimum=0.0, maximum=0.0, q1=0.0, q3=0.0, iqr=0.0,
                skewness=0.0, kurtosis=0.0, zeros=0, negatives=0,
            )

        q1 = float(clean.quantile(0.25))
        q3 = float(clean.quantile(0.75))

        mode_series = clean.mode()
        mode = float(mode_series.iloc[0]) if not mode_series.empty else None

        return NumericStats(
            mean=round(float(clean.mean()), 6),
            median=round(float(clean.median()), 6),
            mode=round(mode, 6) if mode is not None else None,
            std=round(float(clean.std()), 6),
            variance=round(float(clean.var()), 6),
            minimum=float(clean.min()),
            maximum=float(clean.max()),
            q1=round(q1, 6),
            q3=round(q3, 6),
            iqr=round(q3 - q1, 6),
            skewness=round(float(clean.skew()), 6),
            kurtosis=round(float(clean.kurt()), 6),
            zeros=int((clean == 0).sum()),
            negatives=int((clean < 0).sum()),
        )

    @staticmethod
    def is_numeric(series: pd.Series) -> bool:
        """Returns True if the series holds numeric data."""
        return pd.api.types.is_numeric_dtype(series)
