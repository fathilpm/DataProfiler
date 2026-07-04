from pathlib import Path

import pandas as pd

from profiler.analyzers.duplicates import DuplicateAnalyzer
from profiler.analyzers.memory import MemoryAnalyzer
from profiler.analyzers.missing import MissingAnalyzer
from profiler.analyzers.preview import PreviewAnalyzer
from profiler.analyzers.schema import SchemaAnalyzer
from profiler.analyzers.shape import ShapeAnalyzer
from profiler.analyzers.unique import UniqueAnalyzer
from profiler.models.profile import ColumnProfile, DatasetProfile


class ProfilerEngine:
    """Runs all analyzers and builds a dataset profile."""

    @staticmethod
    def profile(df: pd.DataFrame, dataset_name: str) -> DatasetProfile:

        rows, columns = ShapeAnalyzer.analyze(df)

        duplicate_rows = DuplicateAnalyzer.analyze(df)

        memory_usage = MemoryAnalyzer.analyze(df)

        preview = PreviewAnalyzer.analyze(df)

        missing = MissingAnalyzer.analyze(df)

        unique = UniqueAnalyzer.analyze(df)

        schema = SchemaAnalyzer.analyze(df)

        column_profiles = []

        for column in df.columns:

            column_profiles.append(
                ColumnProfile(
                    name=column,
                    dtype=schema[column],
                    missing_count=missing[column],
                    missing_percentage=(missing[column] / rows) * 100 if rows else 0,
                    unique_count=unique[column],
                    memory_usage=int(df[column].memory_usage(deep=True)),
                )
            )

        return DatasetProfile(
            dataset_name=dataset_name,
            rows=rows,
            columns=columns,
            duplicate_rows=duplicate_rows,
            memory_usage=memory_usage,
            preview=preview,
            column_profiles=column_profiles,
        )