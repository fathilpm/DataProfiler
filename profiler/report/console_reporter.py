from __future__ import annotations

from profiler.models.profile import DatasetProfile
from profiler.report.formatter import Formatter
from profiler.utils.size_formatter import SizeFormatter


class ConsoleReporter:
    """Displays a dataset profile in the terminal."""

    def display(self, profile: DatasetProfile) -> None:

        print(Formatter.title("DATA PROFILER"))

        print(f"Dataset        : {profile.dataset_name}")
        print(f"Rows           : {profile.rows}")
        print(f"Columns        : {profile.columns}")
        print(f"Memory Usage   : {SizeFormatter.format(profile.memory_usage)}")
        print(f"Duplicate Rows : {profile.duplicate_rows}")

        print("\nDATASET HEALTH")
        print(Formatter.separator())

        print(f"Total Cells    : {profile.completeness.total_cells}")
        print(f"Filled Cells   : {profile.completeness.filled_cells}")
        print(f"Missing Cells  : {profile.completeness.missing_cells}")
        print(
            f"Completeness   : "
            f"{profile.completeness.completeness_percentage:.2f}%"
        )

        print("\nCOLUMN SUMMARY")
        print(Formatter.separator())

        header = (
            f"{'Column':<15}"
            f"{'Type':<10}"
            f"{'Nullable':<12}"
            f"{'Missing':<15}"
            f"{'Unique':<15}"
            f"{'Memory':<10}"
        )

        print(header)
        print(Formatter.separator())

        for column in profile.column_profiles:

            missing = (
                f"{column.missing_count} "
                f"({column.missing_percentage:.1f}%)"
            )

            unique = (
                f"{column.unique_count} "
                f"({column.unique_percentage:.1f}%)"
            )

            print(
                f"{column.name:<15}"
                f"{column.dtype:<10}"
                f"{'Yes' if column.nullable else 'No':<12}"
                f"{missing:<15}"
                f"{unique:<15}"
                f"{SizeFormatter.format(column.memory_usage):<10}"
            )

        print()