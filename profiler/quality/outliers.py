from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(slots=True)
class OutlierResult:
    """IQR-based outlier detection result for a single numeric column."""

    column: str
    lower_bound: float
    upper_bound: float
    outlier_count: int
    outlier_pct: float
    outlier_indices: list[int]


class OutlierDetector:
    """Detects outliers in numeric columns using the IQR method."""

    @staticmethod
    def detect(
        df: pd.DataFrame,
        iqr_multiplier: float = 1.5,
    ) -> dict[str, OutlierResult]:
        """
        Runs IQR-based outlier detection on all numeric columns.

        A value is an outlier if it is below Q1 - k*IQR or above Q3 + k*IQR,
        where k is the iqr_multiplier (default 1.5).

        Returns a dict mapping column name → OutlierResult.
        Only columns with at least one outlier are included.
        """
        results: dict[str, OutlierResult] = {}

        for col in df.select_dtypes(include="number").columns:
            # Skip boolean columns or binary/one-hot encoded columns (<= 2 unique values)
            if pd.api.types.is_bool_dtype(df[col]) or df[col].nunique() <= 2:
                continue
                
            series = df[col].dropna()
            if series.empty:
                continue

            q1 = float(series.quantile(0.25))
            q3 = float(series.quantile(0.75))
            iqr = q3 - q1

            lower = q1 - iqr_multiplier * iqr
            upper = q3 + iqr_multiplier * iqr

            mask = (df[col] < lower) | (df[col] > upper)
            outlier_indices = list(df.index[mask.fillna(False)])
            outlier_count = len(outlier_indices)

            if outlier_count > 0:
                total = len(series)
                results[col] = OutlierResult(
                    column=col,
                    lower_bound=round(lower, 4),
                    upper_bound=round(upper, 4),
                    outlier_count=outlier_count,
                    outlier_pct=round((outlier_count / total) * 100, 2),
                    outlier_indices=outlier_indices,
                )

        return results
