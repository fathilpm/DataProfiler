from abc import ABC, abstractmethod
from pathlib import Path

import pandas as pd


class BaseReader(ABC):
    """
    Abstract base class for all dataset readers.
    """

    @abstractmethod
    def read(self, file_path: Path) -> pd.DataFrame:
        """
        Read a dataset and return it as a pandas DataFrame.
        """
        pass