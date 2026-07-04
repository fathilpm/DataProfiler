import pandas as pd


class DuplicateAnalyzer:
    """Analyzes duplicate rows."""

    @staticmethod
    def analyze(df: pd.DataFrame) -> int:
        return int(df.duplicated().sum())