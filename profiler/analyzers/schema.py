import pandas as pd


class SchemaAnalyzer:
    """Analyzes dataset schema."""

    @staticmethod
    def analyze(df: pd.DataFrame) -> dict[str, str]:
        return {
            column: str(dtype)
            for column, dtype in df.dtypes.items()
        }