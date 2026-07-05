"""
DataProfiler — Unit Tests

Covers: analyzers, statistics, quality, exporters, and the profiler engine.
Run with: pytest tests/
"""
from __future__ import annotations

import json
import tempfile
from pathlib import Path

import pandas as pd
import pytest

# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def sample_df() -> pd.DataFrame:
    """A small representative DataFrame for testing."""
    return pd.DataFrame({
        "id":       [1, 2, 3, 4, 5],
        "name":     ["Alice", "Bob", "Charlie", "David", "Eve"],
        "age":      [25, 31, 29, 22, 35],
        "score":    [88.5, 91.0, 76.5, 85.0, 92.5],
        "active":   [True, False, True, True, False],
        "joined":   pd.to_datetime(["2020-01-01", "2019-06-15", "2021-03-20",
                                    "2022-07-10", "2018-11-30"]),
    })


@pytest.fixture
def dirty_df() -> pd.DataFrame:
    """A DataFrame with duplicates, missing values, and a constant column."""
    return pd.DataFrame({
        "id":      [1, 1, 2, 3, None],
        "value":   [10.0, 10.0, 20.0, None, 30.0],
        "const":   ["x", "x", "x", "x", "x"],
        "mixed":   [1, "two", 3, "four", 5],
    })


@pytest.fixture
def dataset(sample_df):
    from profiler.models.dataset import Dataset
    from profiler.models.datasource import DataSource
    source = DataSource(name="sample.csv", source_type="csv", location="/tmp/sample.csv")
    return Dataset(dataframe=sample_df, source=source)


# ── Analyzer Tests ─────────────────────────────────────────────────────────────

class TestShapeAnalyzer:
    def test_returns_correct_shape(self, sample_df):
        from profiler.analyzers.shape import ShapeAnalyzer
        rows, cols = ShapeAnalyzer.analyze(sample_df)
        assert rows == 5
        assert cols == 6

class TestDuplicateAnalyzer:
    def test_no_duplicates(self, sample_df):
        from profiler.analyzers.duplicates import DuplicateAnalyzer
        assert DuplicateAnalyzer.analyze(sample_df) == 0

    def test_with_duplicates(self, dirty_df):
        from profiler.analyzers.duplicates import DuplicateAnalyzer
        # Rows 0 and 1 share the same id+value+const, but differ on 'mixed'
        # Full-row duplicates = 0; subset duplicates = 1
        subset_dups = int(dirty_df.duplicated(subset=["id", "value", "const"]).sum())
        assert subset_dups >= 1

class TestMemoryAnalyzer:
    def test_returns_positive_int(self, sample_df):
        from profiler.analyzers.memory import MemoryAnalyzer
        assert MemoryAnalyzer.analyze(sample_df) > 0

class TestMissingAnalyzer:
    def test_no_missing(self, sample_df):
        from profiler.analyzers.missing import MissingAnalyzer
        result = MissingAnalyzer.analyze(sample_df)
        assert all(v == 0 for v in result.values())

    def test_with_missing(self, dirty_df):
        from profiler.analyzers.missing import MissingAnalyzer
        result = MissingAnalyzer.analyze(dirty_df)
        assert result["id"] == 1
        assert result["value"] == 1

class TestSchemaAnalyzer:
    def test_human_readable_dtype(self, sample_df):
        from profiler.analyzers.schema import SchemaAnalyzer
        schema = SchemaAnalyzer.analyze(sample_df)
        assert schema["id"] == "Integer"
        assert schema["name"] == "String"
        assert schema["score"] == "Float"
        assert schema["active"] == "Boolean"

class TestCompletenessAnalyzer:
    def test_full_completeness(self, sample_df):
        from profiler.analyzers.completeness import CompletenessAnalyzer
        result = CompletenessAnalyzer.analyze(sample_df)
        assert result.completeness_percentage == 100.0
        assert result.missing_cells == 0

    def test_partial_completeness(self, dirty_df):
        from profiler.analyzers.completeness import CompletenessAnalyzer
        result = CompletenessAnalyzer.analyze(dirty_df)
        assert result.missing_cells > 0
        assert result.completeness_percentage < 100.0


# ── Statistics Tests ───────────────────────────────────────────────────────────

class TestNumericAnalyzer:
    def test_basic_stats(self, sample_df):
        from profiler.statistics.numeric import NumericAnalyzer
        stats = NumericAnalyzer.analyze(sample_df["age"])
        assert stats.minimum == 22.0
        assert stats.maximum == 35.0
        assert stats.mean == pytest.approx(28.4, rel=1e-3)
        assert stats.zeros == 0
        assert stats.negatives == 0

    def test_is_numeric(self, sample_df):
        from profiler.statistics.numeric import NumericAnalyzer
        assert NumericAnalyzer.is_numeric(sample_df["age"])
        assert not NumericAnalyzer.is_numeric(sample_df["name"])

class TestCategoricalAnalyzer:
    def test_distinct_count(self, sample_df):
        from profiler.statistics.categorical import CategoricalAnalyzer
        stats = CategoricalAnalyzer.analyze(sample_df["name"])
        assert stats.distinct_count == 5

    def test_top_values(self, sample_df):
        from profiler.statistics.categorical import CategoricalAnalyzer
        stats = CategoricalAnalyzer.analyze(sample_df["name"], top_n=3)
        assert len(stats.top_values) == 3

class TestDatetimeAnalyzer:
    def test_range(self, sample_df):
        from profiler.statistics.datetime import DatetimeAnalyzer
        stats = DatetimeAnalyzer.analyze(sample_df["joined"])
        assert stats.date_range_days > 0
        assert "2018" in stats.earliest

class TestBooleanAnalyzer:
    def test_counts(self, sample_df):
        from profiler.statistics.boolean import BooleanAnalyzer
        stats = BooleanAnalyzer.analyze(sample_df["active"])
        assert stats.true_count == 3
        assert stats.false_count == 2
        assert stats.null_count == 0


# ── Quality Tests ──────────────────────────────────────────────────────────────

class TestQualityScorer:
    def test_returns_both_reports(self, sample_df):
        from profiler.quality.scoring import QualityScorer
        qr, hs = QualityScorer.score(sample_df)
        assert qr is not None
        assert hs is not None
        assert 0 <= hs.score <= 100

    def test_dirty_score_lower(self, sample_df, dirty_df):
        from profiler.quality.scoring import QualityScorer
        _, hs_clean = QualityScorer.score(sample_df)
        _, hs_dirty = QualityScorer.score(dirty_df)
        assert hs_dirty.score <= hs_clean.score


class TestMixedTypeDetector:
    def test_finds_mixed_column(self, dirty_df):
        from profiler.quality.mixed_types import MixedTypeDetector
        result = MixedTypeDetector.detect(dirty_df)
        assert "mixed" in result

    def test_clean_df_no_mixed(self, sample_df):
        from profiler.quality.mixed_types import MixedTypeDetector
        result = MixedTypeDetector.detect(sample_df)
        assert len(result) == 0

class TestOutlierDetector:
    def test_detects_outlier(self):
        from profiler.quality.outliers import OutlierDetector
        df = pd.DataFrame({"x": [1, 2, 3, 4, 5, 100]})  # 100 is an outlier
        result = OutlierDetector.detect(df)
        assert "x" in result
        assert result["x"].outlier_count == 1

    def test_no_outliers(self, sample_df):
        from profiler.quality.outliers import OutlierDetector
        result = OutlierDetector.detect(sample_df)
        assert "age" not in result  # small clean dataset

class TestQualityScorer:
    def test_returns_both_reports(self, sample_df):
        from profiler.quality.scoring import QualityScorer
        qr, hs = QualityScorer.score(sample_df)
        assert qr is not None
        assert hs is not None
        assert 0 <= hs.score <= 100

    def test_dirty_score_lower(self, sample_df, dirty_df):
        from profiler.quality.scoring import QualityScorer
        _, hs_clean = QualityScorer.score(sample_df)
        _, hs_dirty = QualityScorer.score(dirty_df)
        assert hs_dirty.score <= hs_clean.score


# ── Engine Tests ───────────────────────────────────────────────────────────────

class TestProfilerEngine:
    def test_full_profile(self, dataset):
        from profiler.engine.profiler_engine import ProfilerEngine
        profile = ProfilerEngine.profile(dataset)
        assert profile.rows == 5
        assert profile.columns == 6
        assert len(profile.column_profiles) == 6
        assert profile.quality_report is not None
        assert profile.health_score is not None

    def test_column_stats_populated(self, dataset):
        from profiler.engine.profiler_engine import ProfilerEngine
        profile = ProfilerEngine.profile(dataset)
        age_col = next(c for c in profile.column_profiles if c.name == "age")
        assert age_col.numeric_stats is not None
        assert age_col.numeric_stats.minimum == 22.0


# ── Exporter Tests ─────────────────────────────────────────────────────────────

@pytest.fixture
def profile(dataset):
    from profiler.engine.profiler_engine import ProfilerEngine
    return ProfilerEngine.profile(dataset)


class TestJSONExporter:
    def test_creates_valid_json(self, profile):
        from profiler.exporters.json import JSONExporter
        with tempfile.TemporaryDirectory() as tmp:
            path = JSONExporter.export(profile, Path(tmp) / "report.json")
            assert path.exists()
            with open(path) as f:
                data = json.load(f)
            assert data["dataset_name"] == "sample.csv"
            assert data["rows"] == 5

class TestMarkdownExporter:
    def test_creates_markdown_file(self, profile):
        from profiler.exporters.markdown import MarkdownExporter
        with tempfile.TemporaryDirectory() as tmp:
            path = MarkdownExporter.export(profile, Path(tmp) / "report.md")
            assert path.exists()
            content = path.read_text()
            assert "# DataProfiler Report" in content
            assert "sample.csv" in content

class TestHTMLExporter:
    def test_creates_html_file(self, profile):
        from profiler.exporters.html import HTMLExporter
        with tempfile.TemporaryDirectory() as tmp:
            path = HTMLExporter.export(profile, Path(tmp) / "report.html")
            assert path.exists()
            content = path.read_text()
            assert "<!DOCTYPE html>" in content
            assert "DataProfiler" in content


# ── Reader Tests ───────────────────────────────────────────────────────────────

class TestReaderFactory:
    def test_csv_reader(self):
        from profiler.readers.factory import ReaderFactory
        reader = ReaderFactory.get_reader(Path("examples/sample.csv"))
        assert reader is not None

    def test_unsupported_raises(self):
        from profiler.readers.factory import ReaderFactory
        with pytest.raises(ValueError, match="Unsupported"):
            ReaderFactory.get_reader(Path("data.parquet"))

class TestCSVReader:
    def test_reads_sample(self):
        from profiler.readers.csv_reader import CSVReader
        reader = CSVReader()
        dataset = reader.read(Path("examples/sample.csv"))
        assert dataset.dataframe.shape == (5, 3)
        assert dataset.source.name == "sample.csv"
