from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from pathlib import Path
from typing import Any

from profiler.models.profile import DatasetProfile


def _serialize(obj: Any) -> Any:
    """Recursively converts dataclasses and special types to JSON-safe objects."""
    if is_dataclass(obj) and not isinstance(obj, type):
        return {k: _serialize(v) for k, v in asdict(obj).items()}
    if isinstance(obj, (list, tuple)):
        return [_serialize(i) for i in obj]
    if isinstance(obj, dict):
        return {k: _serialize(v) for k, v in obj.items()}
    return obj


class JSONExporter:
    """Serializes a DatasetProfile to a JSON file."""

    @staticmethod
    def export(profile: DatasetProfile, output_path: Path) -> Path:
        """
        Writes the full profile as a JSON file.

        Parameters
        ----------
        profile : DatasetProfile
            The profile to serialize.
        output_path : Path
            Destination file path (.json).

        Returns
        -------
        Path
            Path to the written file.
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        data = _serialize(profile)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)

        return output_path
