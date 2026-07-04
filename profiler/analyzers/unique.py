import pandas as pd


class UniqueAnalyzer:
    """Analyzes unique values."""

    @staticmethod
    def analyze(df: pd.DataFrame) -> dict[str, int]:
        return df.nunique(dropna=False).to_dict()