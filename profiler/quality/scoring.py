from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd

from profiler.quality.duplicates import DuplicateKeyDetector
from profiler.quality.mixed_types import MixedTypeDetector
from profiler.quality.outliers import OutlierDetector


@dataclass(slots=True)
class QualityReport:
    """Stores all data quality findings for a dataset."""

    # Column-level checks
    constant_columns: list[str]
    high_cardinality_columns: list[str]
    mixed_type_columns: dict[str, list[str]]  # col -> [types]
    outlier_columns: list[str]                # cols with outliers

    # Dataset-level checks
    duplicate_rows: int
    total_rows: int

    # Warnings and recommendations
    warnings: list[str] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)


@dataclass(slots=True)
class HealthScore:
    """Overall dataset health score (0-100)."""

    score: float
    grade: str
    breakdown: dict[str, float]  # component -> deduction


class QualityScorer:
    """
    Computes a full QualityReport and HealthScore for a dataset.
    """

    @staticmethod
    def score(
        df: pd.DataFrame,
        iqr_multiplier: float = 1.5,
        high_cardinality_threshold: float = 0.9,
    ) -> tuple[QualityReport, HealthScore]:

        # --- Run all quality checks ---
        constant_cols = DuplicateKeyDetector.find_constant_columns(df)
        high_cardinality = DuplicateKeyDetector.find_high_cardinality(
            df, threshold=high_cardinality_threshold
        )
        mixed_types = MixedTypeDetector.detect(df)
        outlier_results = OutlierDetector.detect(df, iqr_multiplier=iqr_multiplier)
        outlier_columns = list(outlier_results.keys())
        duplicate_rows = int(df.duplicated().sum())
        total_rows = len(df)

        # --- Build warnings + recommendations ---
        warnings: list[str] = []
        recommendations: list[str] = []

        if duplicate_rows > 0:
            warnings.append(
                f"{duplicate_rows} duplicate row(s) detected."
            )
            recommendations.append(
                "Consider deduplicating rows before analysis."
            )

        if constant_cols:
            joined = ", ".join(constant_cols)
            warnings.append(
                f"Constant column(s) with a single value: {joined}."
            )
            recommendations.append(
                "Remove constant columns — they carry no information."
            )

        if mixed_types:
            for col, types in mixed_types.items():
                warnings.append(
                    f"Column '{col}' has mixed types: {', '.join(types)}."
                )
            recommendations.append(
                "Standardize mixed-type columns before analysis."
            )

        if outlier_columns:
            joined = ", ".join(outlier_columns)
            warnings.append(f"Outliers detected in column(s): {joined}.")
            recommendations.append(
                "Investigate outliers — they may be errors or rare events."
            )

        # --- Health score computation ---
        deductions: dict[str, float] = {}

        # Missing values deduction (up to -30)
        total_cells = df.shape[0] * df.shape[1]
        if total_cells > 0:
            missing_pct = df.isna().sum().sum() / total_cells
            deductions["missing_values"] = round(min(missing_pct * 100, 30), 2)

        # Duplicate rows deduction (up to -20)
        if total_rows > 0:
            dup_pct = duplicate_rows / total_rows
            deductions["duplicate_rows"] = round(min(dup_pct * 100, 20), 2)

        # Constant columns deduction (up to -15)
        deductions["constant_columns"] = min(len(constant_cols) * 5, 15)

        # Mixed types deduction (up to -20)
        deductions["mixed_types"] = min(len(mixed_types) * 5, 20)

        # Outliers deduction (up to -15)
        deductions["outliers"] = min(len(outlier_columns) * 3, 15)

        total_deduction = sum(deductions.values())
        score = max(0.0, round(100.0 - total_deduction, 1))

        if score >= 90:
            grade = "A"
        elif score >= 75:
            grade = "B"
        elif score >= 60:
            grade = "C"
        elif score >= 40:
            grade = "D"
        else:
            grade = "F"

        quality_report = QualityReport(
            constant_columns=constant_cols,
            high_cardinality_columns=high_cardinality,
            mixed_type_columns=mixed_types,
            outlier_columns=outlier_columns,
            duplicate_rows=duplicate_rows,
            total_rows=total_rows,
            warnings=warnings,
            recommendations=recommendations,
        )

        health_score = HealthScore(
            score=score,
            grade=grade,
            breakdown=deductions,
        )

        return quality_report, health_score
