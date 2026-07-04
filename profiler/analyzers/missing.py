import pandas as pd


class MissingAnalyzer:
    """Analyzes missing values."""

    @staticmethod
    def analyze(df: pd.DataFrame) -> dict[str, int]:
        return df.isna().sum().to_dict()