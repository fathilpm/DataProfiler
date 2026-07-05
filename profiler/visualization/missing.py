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


class MissingValueChart:
    """Generates a bar chart of missing values per column."""

    @staticmethod
    def generate(
        df: pd.DataFrame,
        output_path: Path = Path("reports/charts/missing.html"),
        title: str = "Missing Values by Column",
    ) -> Path:
        """
        Generates a horizontal bar chart showing the percentage of
        missing values per column.

        Returns
        -------
        Path
            Path to the saved HTML chart.
        """
        _check_plotly()

        missing_pct = (df.isna().sum() / len(df) * 100).sort_values(ascending=True)
        columns = list(missing_pct.index)
        values = [round(v, 2) for v in missing_pct.values]

        colors = [
            "#6366f1" if v == 0 else "#f43f5e"
            for v in values
        ]

        fig = go.Figure(
            go.Bar(
                x=values,
                y=columns,
                orientation="h",
                marker_color=colors,
                text=[f"{v:.1f}%" for v in values],
                textposition="outside",
            )
        )

        fig.update_layout(
            title=title,
            xaxis_title="Missing %",
            yaxis_title="Column",
            xaxis=dict(range=[0, 110]),
            template="plotly_dark",
            plot_bgcolor="#1e1e2e",
            paper_bgcolor="#1e1e2e",
        )

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig.write_html(str(output_path))
        return output_path
