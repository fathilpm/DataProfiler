from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class DataSource:
    """
    Represents the origin of a dataset.
    """

    name: str
    source_type: str
    location: str

    metadata: dict[str, Any] = field(default_factory=dict)