from __future__ import annotations

from pathlib import Path

import pandas as pd

from profiler.models.dataset import Dataset
from profiler.models.datasource import DataSource
from profiler.readers.base_reader import BaseReader


class ExcelReader(BaseReader):
    """Reader for Excel files."""

    def read(self, file_path: Path) -> Dataset:
        dataframe = pd.read_excel(file_path)

        source = DataSource(
            name=file_path.name,
            source_type="excel",
            location=str(file_path.resolve()),
        )

        return Dataset(
            dataframe=dataframe,
            source=source,
        )