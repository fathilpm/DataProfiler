from __future__ import annotations

from pathlib import Path

import pandas as pd

try:
    import plotly.figure_factory as ff
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


class DistributionPlot:
    """Generates KDE distribution plots for numeric columns."""

    @staticmethod
    def generate(
        df: pd.DataFrame,
        columns: list[str] | None = None,
        output_path: Path = Path("reports/charts/distribution.html"),
        title: str = "Value Distributions",
    ) -> Path:
        """
        Generates overlaid KDE distribution curves for numeric columns.

        Parameters
        ----------
        df : pd.DataFrame
            The dataset.
        columns : list[str], optional
            Columns to plot. Defaults to all numeric columns.
        output_path : Path
            Where to save the HTML file.
        title : str
            Chart title.

        Returns
        -------
        Path
            Path to saved HTML chart.
        """
        _check_plotly()

        numeric_cols = columns or list(
            df.select_dtypes(include="number").columns
        )

        colors = [
            "#6366f1", "#f43f5e", "#10b981", "#f59e0b",
            "#3b82f6", "#8b5cf6", "#ec4899",
        ]

        fig = go.Figure()

        for i, col in enumerate(numeric_cols):
            series = df[col].dropna()
            if len(series) < 2:
                continue

            try:
                hist_data = [series.tolist()]
                group_labels = [col]
                kde_fig = ff.create_distplot(
                    hist_data,
                    group_labels,
                    show_hist=False,
                    show_rug=False,
                    colors=[colors[i % len(colors)]],
                )
                for trace in kde_fig.data:
                    trace.name = col
                    fig.add_trace(trace)
            except Exception:
                # Fall back to histogram if KDE fails (e.g. constant column)
                fig.add_trace(
                    go.Histogram(
                        x=series,
                        name=col,
                        marker_color=colors[i % len(colors)],
                        histnorm="probability density",
                        opacity=0.6,
                    )
                )

        fig.update_layout(
            title=title,
            xaxis_title="Value",
            yaxis_title="Density",
            template="plotly_dark",
            plot_bgcolor="#1e1e2e",
            paper_bgcolor="#1e1e2e",
        )

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig.write_html(str(output_path))
        return output_path
