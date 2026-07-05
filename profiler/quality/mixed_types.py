from __future__ import annotations

import pandas as pd


class MixedTypeDetector:
    """Detects columns that contain mixed Python types within object columns."""

    @staticmethod
    def detect(df: pd.DataFrame) -> dict[str, list[str]]:
        """
        Returns a mapping of column name → list of detected Python type names
        for columns that contain more than one distinct non-null type.

        Only examines object-dtype columns, since typed columns
        (int, float, etc.) cannot contain mixed types by definition.
        """
        results: dict[str, list[str]] = {}

        for col in df.columns:
            series = df[col]

            if str(series.dtype) != "object":
                continue

            clean = series.dropna()
            if clean.empty:
                continue

            types_found = set(type(v).__name__ for v in clean)

            if len(types_found) > 1:
                results[col] = sorted(types_found)

        return results
