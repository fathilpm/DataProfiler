from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(slots=True)
class CompletenessResult:
    """Stores dataset completeness statistics."""

    total_cells: int
    filled_cells: int
    missing_cells: int
    completeness_percentage: float


class CompletenessAnalyzer:
    """Analyzes dataset completeness."""

    @staticmethod
    def analyze(df: pd.DataFrame) -> CompletenessResult:

        total_cells = df.shape[0] * df.shape[1]

        missing_cells = int(df.isna().sum().sum())

        filled_cells = total_cells - missing_cells

        completeness = (
            (filled_cells / total_cells) * 100
            if total_cells > 0
            else 0.0
        )

        return CompletenessResult(
            total_cells=total_cells,
            filled_cells=filled_cells,
            missing_cells=missing_cells,
            completeness_percentage=completeness,
        )