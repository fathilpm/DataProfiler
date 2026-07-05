from __future__ import annotations

from profiler.models.profile import ColumnProfile, DatasetProfile
from profiler.report.formatter import Formatter
from profiler.utils.size_formatter import SizeFormatter


class ConsoleReporter:
    """Displays a full dataset profile in the terminal."""

    def display(self, profile: DatasetProfile) -> None:
        print(Formatter.title("DATA PROFILER"))

        # ── Overview ─────────────────────────────────────────────────────
        kv = Formatter.kv
        print(kv("Dataset", profile.dataset_name))
        print(kv("Rows", f"{profile.rows:,}"))
        print(kv("Columns", str(profile.columns)))
        print(kv("Memory Usage", SizeFormatter.format(profile.memory_usage)))
        print(kv("Duplicate Rows", str(profile.duplicate_rows)))

        # ── Health Score (v0.4) ───────────────────────────────────────────
        if profile.health_score is not None:
            hs = profile.health_score
            print(Formatter.section("Health Score"))
            print(kv("Score", f"{hs.score} / 100  (Grade: {hs.grade})"))

        # ── Dataset Completeness ──────────────────────────────────────────
        print(Formatter.section("Dataset Health"))
        c = profile.completeness
        print(kv("Total Cells", f"{c.total_cells:,}"))
        print(kv("Filled Cells", f"{c.filled_cells:,}"))
        print(kv("Missing Cells", f"{c.missing_cells:,}"))
        print(kv("Completeness", f"{c.completeness_percentage:.2f}%"))

        # ── Column Summary ────────────────────────────────────────────────
        print(Formatter.section("Column Summary"))

        headers = ["#", "Column", "Type", "Nullable", "Missing", "Unique", "Memory"]
        rows = []
        for i, col in enumerate(profile.column_profiles, start=1):
            missing = f"{col.missing_count} ({col.missing_percentage:.1f}%)"
            unique = f"{col.unique_count} ({col.unique_percentage:.1f}%)"
            rows.append([
                str(i),
                col.name,
                col.dtype,
                "Yes" if col.nullable else "No",
                missing,
                unique,
                SizeFormatter.format(col.memory_usage),
            ])

        print(Formatter.table(headers, rows))

        # ── Column Statistics (v0.3) ──────────────────────────────────────
        has_stats = any(
            col.numeric_stats or col.categorical_stats
            or col.datetime_stats or col.boolean_stats
            for col in profile.column_profiles
        )

        if has_stats:
            print(Formatter.section("Column Statistics"))
            for col in profile.column_profiles:
                self._display_column_stats(col)

        # ── Data Quality (v0.4) ───────────────────────────────────────────
        if profile.quality_report is not None:
            self._display_quality(profile)

        print()

    # ─────────────────────────────────────────────────────────────────────

    def _display_column_stats(self, col: ColumnProfile) -> None:
        kv = Formatter.kv
        sep = Formatter.separator()

        if col.numeric_stats:
            ns = col.numeric_stats
            print(f"\n  [{col.name}]  ({col.dtype})")
            print(f"  {sep}")
            print(f"  {kv('Mean', str(ns.mean))}")
            print(f"  {kv('Median', str(ns.median))}")
            print(f"  {kv('Mode', str(ns.mode) if ns.mode is not None else 'N/A')}")
            print(f"  {kv('Std Dev', str(ns.std))}")
            print(f"  {kv('Min', str(ns.minimum))}")
            print(f"  {kv('Max', str(ns.maximum))}")
            print(f"  {kv('Q1', str(ns.q1))}")
            print(f"  {kv('Q3', str(ns.q3))}")
            print(f"  {kv('IQR', str(ns.iqr))}")
            print(f"  {kv('Skewness', str(ns.skewness))}")
            print(f"  {kv('Kurtosis', str(ns.kurtosis))}")
            print(f"  {kv('Zeros', str(ns.zeros))}")
            print(f"  {kv('Negatives', str(ns.negatives))}")

        elif col.categorical_stats:
            cs = col.categorical_stats
            print(f"\n  [{col.name}]  ({col.dtype})")
            print(f"  {sep}")
            print(f"  {kv('Distinct Values', str(cs.distinct_count))}")
            print(f"  {kv('Most Frequent', f'{cs.most_frequent!r}  ({cs.most_frequent_count}x, {cs.most_frequent_pct}%)')}")
            print(f"  {kv('Least Frequent', f'{cs.least_frequent!r}  ({cs.least_frequent_count}x, {cs.least_frequent_pct}%)')}")
            if cs.top_values:
                print(f"  {'Top Values':}")
                for val, cnt in cs.top_values:
                    print(f"    {val!r:<30} {cnt:>6}x")

        elif col.datetime_stats:
            ds = col.datetime_stats
            print(f"\n  [{col.name}]  ({col.dtype})")
            print(f"  {sep}")
            print(f"  {kv('Earliest', ds.earliest)}")
            print(f"  {kv('Latest', ds.latest)}")
            print(f"  {kv('Range (days)', str(ds.date_range_days))}")
            print(f"  {kv('Most Frequent', str(ds.most_frequent))}")

        elif col.boolean_stats:
            bs = col.boolean_stats
            print(f"\n  [{col.name}]  ({col.dtype})")
            print(f"  {sep}")
            print(f"  {kv('True', f'{bs.true_count} ({bs.true_pct}%)')}")
            print(f"  {kv('False', f'{bs.false_count} ({bs.false_pct}%)')}")
            print(f"  {kv('Null', str(bs.null_count))}")

    def _display_quality(self, profile: DatasetProfile) -> None:
        qr = profile.quality_report
        kv = Formatter.kv

        print(Formatter.section("Data Quality"))

        if qr.constant_columns:
            print(kv("Constant Columns", ", ".join(qr.constant_columns)))

        if qr.high_cardinality_columns:
            print(kv("High Cardinality", ", ".join(qr.high_cardinality_columns)))

        if qr.mixed_type_columns:
            for col, types in qr.mixed_type_columns.items():
                print(kv(f"Mixed Types [{col}]", ", ".join(types)))

        if qr.outlier_columns:
            print(kv("Outlier Columns", ", ".join(qr.outlier_columns)))

        if not any([
            qr.constant_columns, qr.high_cardinality_columns,
            qr.mixed_type_columns, qr.outlier_columns,
            qr.duplicate_rows > 0,
        ]):
            print("  No issues detected.")

        if qr.warnings:
            print(f"\n  WARNINGS")
            for w in qr.warnings:
                print(f"  !! {w}")

        if qr.recommendations:
            print(f"\n  RECOMMENDATIONS")
            for r in qr.recommendations:
                print(f"  -> {r}")