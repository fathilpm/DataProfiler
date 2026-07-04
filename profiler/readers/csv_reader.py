from pathlib import Path

import pandas as pd

from profiler.readers.base_reader import BaseReader
from profiler.utils.logger import get_logger


logger = get_logger(__name__)


class CSVReader(BaseReader):
    """Reader for CSV files."""

    def read(self, file_path: Path) -> pd.DataFrame:
        logger.info(f"Reading CSV file: {file_path}")

        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"File not found: {file_path}")

        if file_path.suffix.lower() != ".csv":
            logger.error(f"Invalid CSV extension: {file_path.suffix}")
            raise ValueError(f"Invalid file type: {file_path.suffix}")

        try:
            dataframe = pd.read_csv(file_path)

            logger.info(
                f"Successfully loaded CSV with {len(dataframe)} rows."
            )

            return dataframe

        except Exception as e:
            logger.exception("Error reading CSV file.")
            raise RuntimeError(f"Failed to read CSV file: {e}") from e