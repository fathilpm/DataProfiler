import pandas as pd
from profiler.preprocessing.base import Transformer

class ColumnDropper(Transformer):
    def __init__(self, columns: list[str]):
        self.columns = columns

    def fit(self, df: pd.DataFrame) -> 'Transformer':
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.drop(columns=self.columns, errors='ignore')

class RowDropperNA(Transformer):
    def __init__(self, column: str):
        self.column = column

    def fit(self, df: pd.DataFrame) -> 'Transformer':
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.dropna(subset=[self.column]).reset_index(drop=True)

class TypeConverter(Transformer):
    def __init__(self, column: str, target_type: str):
        self.column = column
        self.target_type = target_type

    def fit(self, df: pd.DataFrame) -> 'Transformer':
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df_out = df.copy()
        try:
            if self.target_type == 'numeric':
                df_out[self.column] = pd.to_numeric(df_out[self.column], errors='coerce')
            elif self.target_type == 'datetime':
                df_out[self.column] = pd.to_datetime(df_out[self.column], errors='coerce')
            elif self.target_type == 'string':
                df_out[self.column] = df_out[self.column].astype(str)
        except Exception:
            pass
        return df_out
