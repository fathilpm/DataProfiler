import pandas as pd


class MemoryAnalyzer:
    """Analyzes dataset memory usage."""

    @staticmethod
    def analyze(df: pd.DataFrame) -> int:
        return int(df.memory_usage(deep=True).sum())