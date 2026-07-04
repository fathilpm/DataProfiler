import pandas as pd


class ShapeAnalyzer:
    """Analyzes dataset dimensions."""

    @staticmethod
    def analyze(df: pd.DataFrame) -> tuple[int, int]:
        return df.shape