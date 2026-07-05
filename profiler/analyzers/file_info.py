from __future__ import annotations

from datetime import datetime
from pathlib import Path

from profiler.models.file_info import FileInfo


class FileInfoAnalyzer:
    """Analyzes dataset file metadata."""

    @staticmethod
    def analyze(file_path: Path) -> FileInfo:
        stat = file_path.stat()

        return FileInfo(
            name=file_path.name,
            extension=file_path.suffix.lower(),
            path=str(file_path.resolve()),
            size=stat.st_size,
            created=datetime.fromtimestamp(stat.st_ctime).strftime(
                "%d %b %Y %H:%M"
            ),
            modified=datetime.fromtimestamp(stat.st_mtime).strftime(
                "%d %b %Y %H:%M"
            ),
        )