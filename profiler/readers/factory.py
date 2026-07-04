from pathlib import Path

from profiler.readers.base_reader import BaseReader
from profiler.readers.csv_reader import CSVReader
from profiler.readers.excel_reader import ExcelReader


class ReaderFactory:
    """Factory for creating dataset readers."""

    _READERS = {
        ".csv": CSVReader,
        ".xlsx": ExcelReader,
        ".xls": ExcelReader,
    }

    @classmethod
    def get_reader(cls, file_path: str | Path) -> BaseReader:
        path = Path(file_path)
        extension = path.suffix.lower()

        reader_class = cls._READERS.get(extension)

        if reader_class is None:
            supported = ", ".join(cls._READERS.keys())
            raise ValueError(
                f"Unsupported file format: '{extension}'. "
                f"Supported formats: {supported}"
            )

        return reader_class()