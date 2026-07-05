from __future__ import annotations


class ProfilerError(Exception):
    """Base exception for all DataProfiler errors."""


class UnsupportedFileFormatError(ProfilerError):
    """Raised when a file format is not supported by any reader."""

    def __init__(self, extension: str, supported: list[str]) -> None:
        supported_str = ", ".join(supported)
        super().__init__(
            f"Unsupported file format: '{extension}'. "
            f"Supported formats: {supported_str}"
        )
        self.extension = extension
        self.supported = supported


class EmptyDatasetError(ProfilerError):
    """Raised when an attempt is made to profile an empty dataset."""

    def __init__(self, name: str = "") -> None:
        msg = f"Dataset '{name}' is empty." if name else "Dataset is empty."
        super().__init__(msg)


class FileNotFoundError(ProfilerError):
    """Raised when the source file does not exist."""

    def __init__(self, path: str) -> None:
        super().__init__(f"File not found: '{path}'")
        self.path = path


class AnalysisError(ProfilerError):
    """Raised when an analyzer encounters an unexpected error."""

    def __init__(self, analyzer: str, reason: str) -> None:
        super().__init__(f"Analysis failed in '{analyzer}': {reason}")
        self.analyzer = analyzer
        self.reason = reason
