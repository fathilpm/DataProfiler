from __future__ import annotations

from pathlib import Path

import pandas as pd

try:
    import plotly.graph_objects as go
    _PLOTLY_AVAILABLE = True
except ImportError:
    _PLOTLY_AVAILABLE = False


def _check_plotly() -> None:
    if not _PLOTLY_AVAILABLE:
        raise ImportError(
            "plotly is required for visualization. "
            "Install it with: pip install plotly"
        )


class BoxplotChart:
    """Generates boxplot charts for numeric columns."""

    @staticmethod
    def generate(
        df: pd.DataFrame,
        columns: list[str] | None = None,
        output_path: Path = Path("reports/charts/boxplot.html"),
        title: str = "Boxplot Distribution",
    ) -> Path:
        """
        Generates a combined boxplot for all (or selected) numeric columns.

        Parameters
        ----------
        df : pd.DataFrame
            The full dataset.
        columns : list[str], optional
            Columns to plot. Defaults to all numeric columns.
        output_path : Path
            Where to save the HTML chart.
        title : str
            Chart title.

        Returns
        -------
        Path
            Path to the saved chart.
        """
        _check_plotly()

        numeric_cols = columns or list(
            df.select_dtypes(include="number").columns
        )

        fig = go.Figure()
        colors = [
            "#6366f1", "#f43f5e", "#10b981", "#f59e0b",
            "#3b82f6", "#8b5cf6", "#ec4899",
        ]
        for i, col in enumerate(numeric_cols):
            fig.add_trace(
                go.Box(
                    y=df[col].dropna(),
                    name=col,
                    marker_color=colors[i % len(colors)],
                    boxmean=True,
                )
            )

        fig.update_layout(
            title=title,
            yaxis_title="Value",
            template="plotly_dark",
            plot_bgcolor="#1e1e2e",
            paper_bgcolor="#1e1e2e",
        )

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig.write_html(str(output_path))
        return output_path
