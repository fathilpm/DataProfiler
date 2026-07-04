import pandas as pd


class PreviewAnalyzer:
    """Generates dataset preview."""

    @staticmethod
    def analyze(df: pd.DataFrame, rows: int = 5) -> list[dict]:
        return df.head(rows).to_dict(orient="records")