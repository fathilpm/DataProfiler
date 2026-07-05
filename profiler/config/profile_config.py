from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ProfileConfig:
    """
    Controls which analysis modules are executed by the profiler engine.

    All modules are enabled by default.
    """

    # Core (always on)
    run_shape: bool = True
    run_memory: bool = True
    run_duplicates: bool = True
    run_missing: bool = True
    run_schema: bool = True
    run_completeness: bool = True
    run_unique: bool = True

    # v0.3 — Statistics
    run_statistics: bool = True

    # v0.4 — Data Quality
    run_quality: bool = True

    # v0.5 — Relationships
    run_relationships: bool = False  # disabled by default (multi-file)

    # v0.6 — Visualization
    run_visualization: bool = True
    visualization_output_dir: str = "reports/charts"

    # v0.7 — Export
    export_html: bool = False
    export_json: bool = False
    export_markdown: bool = False
    export_pdf: bool = False
    export_output_dir: str = "reports"

    # Statistics options
    top_n_values: int = 5  # how many top/bottom categorical values to show

    # Quality options
    outlier_iqr_multiplier: float = 1.5
    high_cardinality_threshold: float = 0.9  # % unique to flag as high cardinality

    @classmethod
    def full(cls) -> "ProfileConfig":
        """Returns a config with all modules enabled including exports."""
        return cls(
            run_relationships=True,
            export_html=True,
            export_json=True,
            export_markdown=True,
        )

    @classmethod
    def minimal(cls) -> "ProfileConfig":
        """Returns a minimal config: core profiling only, no stats or quality."""
        return cls(
            run_statistics=False,
            run_quality=False,
            run_visualization=False,
        )
