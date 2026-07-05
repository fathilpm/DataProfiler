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


class CorrelationMatrix:
    """Generates a correlation heatmap for numeric columns."""

    @staticmethod
    def generate(
        df: pd.DataFrame,
        output_path: Path = Path("reports/charts/correlation.html"),
        title: str = "Correlation Matrix",
        method: str = "pearson",
    ) -> Path:
        """
        Generates a heatmap of pairwise correlations between numeric columns.

        Parameters
        ----------
        df : pd.DataFrame
            The dataset.
        output_path : Path
            Where to save the HTML chart.
        title : str
            Chart title.
        method : str
            Correlation method: 'pearson', 'spearman', or 'kendall'.

        Returns
        -------
        Path
            Path to the saved HTML chart.
        """
        _check_plotly()

        numeric_df = df.select_dtypes(include="number")
        if numeric_df.shape[1] < 2:
            raise ValueError(
                "At least 2 numeric columns are required for a correlation matrix."
            )

        corr = numeric_df.corr(method=method).round(3)
        cols = list(corr.columns)

        fig = go.Figure(
            go.Heatmap(
                z=corr.values,
                x=cols,
                y=cols,
                colorscale="RdBu",
                zmid=0,
                text=corr.values.round(2),
                texttemplate="%{text}",
                hovertemplate="%{x} vs %{y}: %{z:.3f}<extra></extra>",
            )
        )

        fig.update_layout(
            title=title,
            template="plotly_dark",
            plot_bgcolor="#1e1e2e",
            paper_bgcolor="#1e1e2e",
        )

        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        fig.write_html(str(output_path))
        return output_path
