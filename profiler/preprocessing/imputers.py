import pandas as pd
from profiler.preprocessing.base import Transformer

class SimpleImputer(Transformer):
    def __init__(self, column: str, strategy: str = 'mean', fill_value=None):
        self.column = column
        self.strategy = strategy
        self.fill_value = fill_value
        self._computed_value = None

    def fit(self, df: pd.DataFrame) -> 'Transformer':
        if self.strategy == 'mean':
            self._computed_value = df[self.column].mean()
        elif self.strategy == 'median':
            self._computed_value = df[self.column].median()
        elif self.strategy == 'mode':
            mode_series = df[self.column].mode()
            self._computed_value = mode_series.iloc[0] if not mode_series.empty else None
        elif self.strategy == 'constant':
            self._computed_value = self.fill_value
        else:
            raise ValueError(f"Unknown strategy: {self.strategy}")
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df_out = df.copy()
        if self._computed_value is not None:
            df_out[self.column] = df_out[self.column].fillna(self._computed_value)
        return df_out
