from pathlib import Path

import pandas as pd

from profiler.readers.base_reader import BaseReader
from profiler.utils.logger import get_logger

logger = get_logger(__name__)


class ExcelReader(BaseReader):
    """Reader for Excel (.xlsx and .xls) files."""

    def read(self, file_path: Path) -> pd.DataFrame:
        logger.info(f"Reading Excel file: {file_path}")

        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"File not found: {file_path}")

        if file_path.suffix.lower() not in [".xlsx", ".xls"]:
            logger.error(f"Invalid Excel extension: {file_path.suffix}")
            raise ValueError(f"Invalid file type: {file_path.suffix}")

        try:
            dataframe = pd.read_excel(file_path)

            logger.info(
                f"Successfully loaded Excel file with {len(dataframe)} rows."
            )

            return dataframe

        except Exception as e:
            logger.exception("Error reading Excel file.")
            raise RuntimeError(f"Failed to read Excel file: {e}") from e