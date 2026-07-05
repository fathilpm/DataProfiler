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


class HistogramChart:
    """Generates histogram charts for numeric columns."""

    @staticmethod
    def generate(
        series: pd.Series,
        output_path: Path,
        title: str | None = None,
    ) -> Path:
        """
        Saves an HTML histogram for the given numeric series.

        Parameters
        ----------
        series : pd.Series
            The numeric column data.
        output_path : Path
            Where to save the HTML file.
        title : str, optional
            Chart title. Defaults to series name.

        Returns
        -------
        Path
            The path where the chart was saved.
        """
        _check_plotly()

        chart_title = title or f"Distribution of {series.name}"

        fig = go.Figure(
            go.Histogram(
                x=series.dropna(),
                name=str(series.name),
                marker_color="#6366f1",
                opacity=0.85,
            )
        )
        fig.update_layout(
            title=chart_title,
            xaxis_title=str(series.name),
            yaxis_title="Count",
            template="plotly_dark",
            plot_bgcolor="#1e1e2e",
            paper_bgcolor="#1e1e2e",
        )

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig.write_html(str(output_path))
        return output_path
