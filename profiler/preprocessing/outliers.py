import pandas as pd
import numpy as np
from profiler.preprocessing.base import Transformer

class OutlierCapper(Transformer):
    def __init__(self, column: str, factor: float = 1.5):
        self.column = column
        self.factor = factor
        self.lower_bound = None
        self.upper_bound = None

    def fit(self, df: pd.DataFrame) -> 'Transformer':
        if pd.api.types.is_numeric_dtype(df[self.column]) and not pd.api.types.is_bool_dtype(df[self.column]):
            q1 = df[self.column].quantile(0.25)
            q3 = df[self.column].quantile(0.75)
            iqr = q3 - q1
            self.lower_bound = q1 - (self.factor * iqr)
            self.upper_bound = q3 + (self.factor * iqr)
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df_out = df.copy()
        if self.lower_bound is not None and self.upper_bound is not None:
            df_out[self.column] = df_out[self.column].clip(lower=self.lower_bound, upper=self.upper_bound)
        return df_out
