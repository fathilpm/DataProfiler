import pandas as pd
from profiler.preprocessing.base import Transformer
from profiler.preprocessing.imputers import SimpleImputer
from profiler.preprocessing.cleaners import ColumnDropper
from profiler.preprocessing.outliers import OutlierCapper
from profiler.preprocessing.encoders import OneHotEncoder

class AutoPreprocessor(Transformer):
    def __init__(self, missing_threshold=0.95, onehot_threshold=10, outlier_factor=1.5):
        """
        AutoPreprocessor:
        1. Drops columns with high missing rates (>95%) and constant columns.
        2. Imputes missing values (median for numeric, mode for categorical).
        3. Caps outliers on numeric columns using IQR.
        4. One-Hot encodes low-cardinality categorical columns.
        """
        self.missing_threshold = missing_threshold
        self.onehot_threshold = onehot_threshold
        self.outlier_factor = outlier_factor
        self._transformers = []

    def fit(self, df: pd.DataFrame) -> 'Transformer':
        self._transformers = []
        
        # 1. Identify columns to drop
        cols_to_drop = []
        for col in df.columns:
            missing_pct = df[col].isnull().mean()
            if missing_pct >= self.missing_threshold:
                cols_to_drop.append(col)
            elif df[col].nunique() <= 1:
                if col not in cols_to_drop:
                    cols_to_drop.append(col)
        
        if cols_to_drop:
            dropper = ColumnDropper(columns=cols_to_drop)
            dropper.fit(df)
            self._transformers.append(dropper)
            
        df_temp = df.drop(columns=cols_to_drop)
        
        # 2. Impute missing values
        for col in df_temp.columns:
            if df_temp[col].isnull().any():
                if pd.api.types.is_numeric_dtype(df_temp[col]) and not pd.api.types.is_bool_dtype(df_temp[col]):
                    imputer = SimpleImputer(column=col, strategy='median')
                else:
                    imputer = SimpleImputer(column=col, strategy='mode')
                imputer.fit(df_temp)
                self._transformers.append(imputer)
                df_temp = imputer.transform(df_temp)
                
        # 3. Cap Outliers and Encode
        # Note: encoding changes column names, so we do capping first
        for col in df_temp.columns:
            if pd.api.types.is_numeric_dtype(df_temp[col]) and not pd.api.types.is_bool_dtype(df_temp[col]):
                capper = OutlierCapper(column=col, factor=self.outlier_factor)
                capper.fit(df_temp)
                self._transformers.append(capper)
                df_temp = capper.transform(df_temp)
            else:
                # If categorical and low cardinality, One-Hot Encode
                if df_temp[col].nunique() < self.onehot_threshold:
                    encoder = OneHotEncoder(column=col)
                    encoder.fit(df_temp)
                    self._transformers.append(encoder)
                    df_temp = encoder.transform(df_temp)
                
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df_out = df.copy()
        for transformer in self._transformers:
            df_out = transformer.transform(df_out)
        return df_out
