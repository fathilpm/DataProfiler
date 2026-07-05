from __future__ import annotations

from profiler.analyzers.completeness import CompletenessAnalyzer
from profiler.analyzers.duplicates import DuplicateAnalyzer
from profiler.analyzers.memory import MemoryAnalyzer
from profiler.analyzers.missing import MissingAnalyzer
from profiler.analyzers.schema import SchemaAnalyzer
from profiler.analyzers.shape import ShapeAnalyzer
from profiler.analyzers.unique import UniqueAnalyzer

from profiler.statistics.boolean import BooleanAnalyzer
from profiler.statistics.categorical import CategoricalAnalyzer
from profiler.statistics.datetime import DatetimeAnalyzer
from profiler.statistics.numeric import NumericAnalyzer

from profiler.quality.scoring import QualityScorer

from profiler.config.profile_config import ProfileConfig
from profiler.models.dataset import Dataset
from profiler.models.profile import ColumnProfile, DatasetProfile


class ProfilerEngine:
    """Runs all analyzers and builds a dataset profile."""

    @staticmethod
    def profile(
        dataset: Dataset,
        config: ProfileConfig | None = None,
    ) -> DatasetProfile:
        """
        Profiles a dataset and returns a DatasetProfile.

        Parameters
        ----------
        dataset : Dataset
            The loaded dataset to profile.
        config : ProfileConfig, optional
            Controls which modules are executed. Defaults to ProfileConfig()
            which enables all standard modules.
        """
        if config is None:
            config = ProfileConfig()

        df = dataset.dataframe

        # ── Core ──────────────────────────────────────────────────────────
        rows, columns = ShapeAnalyzer.analyze(df)
        duplicate_rows = DuplicateAnalyzer.analyze(df)
        memory_usage = MemoryAnalyzer.analyze(df)
        missing = MissingAnalyzer.analyze(df)
        unique = UniqueAnalyzer.analyze(df)
        schema = SchemaAnalyzer.analyze(df)         # human-readable dtypes
        raw_schema = SchemaAnalyzer.raw(df)          # original pandas dtypes
        completeness = CompletenessAnalyzer.analyze(df)

        # ── Column Profiles ───────────────────────────────────────────────
        column_profiles: list[ColumnProfile] = []

        for column in df.columns:
            series = df[column]
            missing_count = missing[column]
            missing_pct = (missing_count / rows * 100) if rows else 0.0
            unique_count = unique[column]
            unique_pct = (unique_count / rows * 100) if rows else 0.0

            # --- Statistics (v0.3) ---
            numeric_stats = None
            categorical_stats = None
            datetime_stats = None
            boolean_stats = None

            if config.run_statistics:
                if BooleanAnalyzer.is_boolean(series):
                    boolean_stats = BooleanAnalyzer.analyze(series)
                elif NumericAnalyzer.is_numeric(series):
                    numeric_stats = NumericAnalyzer.analyze(series)
                elif DatetimeAnalyzer.is_datetime(series):
                    datetime_stats = DatetimeAnalyzer.analyze(series)
                elif CategoricalAnalyzer.is_categorical(series):
                    categorical_stats = CategoricalAnalyzer.analyze(
                        series, top_n=config.top_n_values
                    )

            column_profiles.append(
                ColumnProfile(
                    name=column,
                    dtype=schema[column],
                    raw_dtype=raw_schema[column],
                    nullable=missing_count > 0,
                    missing_count=missing_count,
                    missing_percentage=round(missing_pct, 2),
                    unique_count=unique_count,
                    unique_percentage=round(unique_pct, 2),
                    memory_usage=int(series.memory_usage(deep=True)),
                    numeric_stats=numeric_stats,
                    categorical_stats=categorical_stats,
                    datetime_stats=datetime_stats,
                    boolean_stats=boolean_stats,
                )
            )

        # ── Data Quality (v0.4) ───────────────────────────────────────────
        quality_report = None
        health_score = None

        if config.run_quality:
            quality_report, health_score = QualityScorer.score(
                df,
                iqr_multiplier=config.outlier_iqr_multiplier,
                high_cardinality_threshold=config.high_cardinality_threshold,
            )

        return DatasetProfile(
            dataset_name=dataset.source.name,
            rows=rows,
            columns=columns,
            duplicate_rows=duplicate_rows,
            memory_usage=memory_usage,
            completeness=completeness,
            column_profiles=column_profiles,
            quality_report=quality_report,
            health_score=health_score,
        )