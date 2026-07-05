from __future__ import annotations

from pathlib import Path

from profiler.exporters.pdf import PDFExporter
from profiler.models.profile import DatasetProfile


class PDFReporter:
    """Writes a PDF report for a DatasetProfile."""

    def __init__(self, output_dir: str | Path = "reports") -> None:
        self.output_dir = Path(output_dir)

    def export(self, profile: DatasetProfile) -> Path:
        """Exports the profile as a PDF file and returns the path."""
        stem = Path(profile.dataset_name).stem
        output_path = self.output_dir / f"{stem}_report.pdf"
        return PDFExporter.export(profile, output_path)
