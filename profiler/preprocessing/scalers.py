import pandas as pd
import numpy as np
from profiler.preprocessing.base import Transformer

class MinMaxScaler(Transformer):
    def __init__(self, column: str):
        self.column = column
        self.min_val = None
        self.max_val = None

    def fit(self, df: pd.DataFrame) -> 'Transformer':
        if pd.api.types.is_numeric_dtype(df[self.column]) and not pd.api.types.is_bool_dtype(df[self.column]):
            self.min_val = df[self.column].min()
            self.max_val = df[self.column].max()
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df_out = df.copy()
        if self.min_val is not None and self.max_val is not None and self.max_val > self.min_val:
            df_out[self.column] = (df_out[self.column] - self.min_val) / (self.max_val - self.min_val)
        return df_out

class StandardScaler(Transformer):
    def __init__(self, column: str):
        self.column = column
        self.mean_val = None
        self.std_val = None

    def fit(self, df: pd.DataFrame) -> 'Transformer':
        if pd.api.types.is_numeric_dtype(df[self.column]) and not pd.api.types.is_bool_dtype(df[self.column]):
            self.mean_val = df[self.column].mean()
            self.std_val = df[self.column].std()
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df_out = df.copy()
        if self.mean_val is not None and self.std_val is not None and self.std_val > 0:
            df_out[self.column] = (df_out[self.column] - self.mean_val) / self.std_val
        return df_out

class RobustScaler(Transformer):
    def __init__(self, column: str):
        self.column = column
        self.median_val = None
        self.iqr_val = None

    def fit(self, df: pd.DataFrame) -> 'Transformer':
        if pd.api.types.is_numeric_dtype(df[self.column]) and not pd.api.types.is_bool_dtype(df[self.column]):
            self.median_val = df[self.column].median()
            q1 = df[self.column].quantile(0.25)
            q3 = df[self.column].quantile(0.75)
            self.iqr_val = q3 - q1
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df_out = df.copy()
        if self.median_val is not None and self.iqr_val is not None and self.iqr_val > 0:
            df_out[self.column] = (df_out[self.column] - self.median_val) / self.iqr_val
        return df_out
