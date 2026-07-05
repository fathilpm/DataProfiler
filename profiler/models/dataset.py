from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from profiler.models.datasource import DataSource


@dataclass(slots=True)
class Dataset:
    """
    Represents a dataset loaded into DataProfiler.
    """

    dataframe: pd.DataFrame
    source: DataSource