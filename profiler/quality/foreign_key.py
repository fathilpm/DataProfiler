from __future__ import annotations

import pandas as pd


class ForeignKeyHint:
    """
    Heuristic hints about columns that may be foreign keys
    (within a single dataset context).
    """

    @staticmethod
    def detect(df: pd.DataFrame, primary_keys: list[str]) -> list[str]:
        """
        Returns a list of column names that appear to reference another
        column's values — i.e., their value set is a strict subset of
        a primary key column's value set.

        Excludes the primary key columns themselves.
        """
        hints: list[str] = []

        pk_value_sets = {
            pk: set(df[pk].dropna().astype(str))
            for pk in primary_keys
        }

        for col in df.columns:
            if col in primary_keys:
                continue

            col_values = set(df[col].dropna().astype(str))
            if not col_values:
                continue

            for pk, pk_values in pk_value_sets.items():
                if col_values <= pk_values and col != pk:
                    hints.append(col)
                    break

        return hints
