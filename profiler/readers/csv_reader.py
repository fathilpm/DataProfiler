from __future__ import annotations

from pathlib import Path

import pandas as pd

from profiler.models.dataset import Dataset
from profiler.models.datasource import DataSource
from profiler.readers.base_reader import BaseReader


class CSVReader(BaseReader):
    """Reader for CSV files."""

    def read(self, file_path: Path) -> Dataset:
        dataframe = pd.read_csv(file_path)

        source = DataSource(
            name=file_path.name,
            source_type="csv",
            location=str(file_path.resolve()),
        )

        return Dataset(
            dataframe=dataframe,
            source=source,
        )