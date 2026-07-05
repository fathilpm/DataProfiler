from __future__ import annotations

import pandas as pd


class DuplicateKeyDetector:
    """Detects duplicate key combinations across column subsets."""

    @staticmethod
    def detect(df: pd.DataFrame, columns: list[str] | None = None) -> int:
        """
        Counts duplicate rows across the given column subset.

        If columns is None, checks all columns (equivalent to full row duplicates).
        Returns the number of duplicate records found.
        """
        subset = columns if columns else list(df.columns)
        return int(df.duplicated(subset=subset).sum())

    @staticmethod
    def find_constant_columns(df: pd.DataFrame) -> list[str]:
        """
        Returns a list of column names that contain only a single distinct value
        (constant columns are useless for analysis).
        """
        return [
            col for col in df.columns
            if df[col].dropna().nunique() <= 1
        ]

    @staticmethod
    def find_high_cardinality(
        df: pd.DataFrame,
        threshold: float = 0.9,
    ) -> list[str]:
        """
        Returns columns where the ratio of unique values to total rows
        exceeds the threshold. High-cardinality columns may be IDs or
        candidate foreign keys.
        """
        n_rows = len(df)
        if n_rows == 0:
            return []

        return [
            col for col in df.columns
            if df[col].nunique() / n_rows >= threshold
        ]
