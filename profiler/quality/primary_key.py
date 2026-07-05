from __future__ import annotations

import pandas as pd


class PrimaryKeyDetector:
    """Detects candidate primary key columns in a dataset."""

    @staticmethod
    def detect(df: pd.DataFrame) -> list[str]:
        """
        Returns a list of column names that are candidate primary keys.

        A column is a candidate primary key if it:
        - Has no missing values
        - Has 100% unique values (no duplicates)
        """
        candidates = []
        n_rows = len(df)

        if n_rows == 0:
            return candidates

        for col in df.columns:
            series = df[col]
            has_no_nulls = series.isna().sum() == 0
            is_unique = series.nunique() == n_rows

            if has_no_nulls and is_unique:
                candidates.append(col)

        return candidates
