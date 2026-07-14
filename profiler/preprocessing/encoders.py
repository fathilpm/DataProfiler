import pandas as pd
from profiler.preprocessing.base import Transformer

class LabelEncoder(Transformer):
    def __init__(self, column: str):
        self.column = column
        self.mapping = {}

    def fit(self, df: pd.DataFrame) -> 'Transformer':
        unique_vals = df[self.column].dropna().unique()
        self.mapping = {val: i for i, val in enumerate(unique_vals)}
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df_out = df.copy()
        df_out[self.column] = df_out[self.column].map(self.mapping)
        return df_out

class OneHotEncoder(Transformer):
    def __init__(self, column: str):
        self.column = column
        self.categories = []

    def fit(self, df: pd.DataFrame) -> 'Transformer':
        self.categories = list(df[self.column].dropna().unique())
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df_out = df.copy()
        for cat in self.categories:
            col_name = f"{self.column}_{cat}"
            df_out[col_name] = (df_out[self.column] == cat).astype(int)
        df_out = df_out.drop(columns=[self.column])
        return df_out
