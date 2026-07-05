from __future__ import annotations

import pandas as pd


# Mapping from pandas dtype names → human-readable display names
_DTYPE_MAP: dict[str, str] = {
    "int8": "Integer",
    "int16": "Integer",
    "int32": "Integer",
    "int64": "Integer",
    "uint8": "Integer",
    "uint16": "Integer",
    "uint32": "Integer",
    "uint64": "Integer",
    "float16": "Float",
    "float32": "Float",
    "float64": "Float",
    "bool": "Boolean",
    "boolean": "Boolean",
    "object": "String",
    "string": "String",
    "str": "String",       # pandas 3.x uses 'str' instead of 'object'
    "category": "Category",
}


def _resolve_dtype(series: pd.Series) -> str:
    """
    Returns a human-readable dtype label for a pandas Series.
    Checks for datetime, timedelta, and period types first,
    then falls back to the _DTYPE_MAP.
    """
    dtype_name = str(series.dtype)

    if dtype_name.startswith("datetime"):
        return "DateTime"
    if dtype_name.startswith("timedelta"):
        return "TimeDelta"
    if dtype_name.startswith("period"):
        return "Period"

    return _DTYPE_MAP.get(dtype_name, dtype_name.capitalize())


class SchemaAnalyzer:
    """Analyzes dataset schema and maps dtypes to human-readable names."""

    @staticmethod
    def analyze(df: pd.DataFrame) -> dict[str, str]:
        """
        Returns a mapping of column name → human-readable dtype label.
        """
        return {
            column: _resolve_dtype(df[column])
            for column in df.columns
        }

    @staticmethod
    def raw(df: pd.DataFrame) -> dict[str, str]:
        """
        Returns a mapping of column name → raw pandas dtype string.
        """
        return {
            column: str(dtype)
            for column, dtype in df.dtypes.items()
        }