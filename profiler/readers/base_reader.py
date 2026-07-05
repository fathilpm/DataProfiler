from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from profiler.models.dataset import Dataset


class BaseReader(ABC):
    """
    Abstract base class for all dataset readers.
    """

    @abstractmethod
    def read(self, file_path: Path) -> Dataset:
        """
        Read a file and return it as a Dataset.
        """
        pass