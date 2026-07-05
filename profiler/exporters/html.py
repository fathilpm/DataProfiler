from __future__ import annotations

from pathlib import Path

from profiler.models.profile import ColumnProfile, DatasetProfile
from profiler.utils.size_formatter import SizeFormatter


_CSS = """
:root {
  --bg: #0f0f1a;
  --surface: #1a1a2e;
  --surface2: #16213e;
  --accent: #6366f1;
  --accent2: #8b5cf6;
  --success: #10b981;
  --warning: #f59e0b;
  --danger: #f43f5e;
  --text: #e2e8f0;
  --text-muted: #94a3b8;
  --border: #2d2d50;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  background: var(--bg);
  color: var(--text);
  font-family: 'Inter', -apple-system, sans-serif;
  padding: 2rem;
  line-height: 1.6;
}

h1 {
  background: linear-gradient(135deg, var(--accent), var(--accent2));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-size: 2rem;
  margin-bottom: 0.25rem;
}

h2 {
  color: var(--accent);
  font-size: 1.1rem;
  margin: 2rem 0 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  border-bottom: 1px solid var(--border);
  padding-bottom: 0.4rem;
}

h3 {
  color: var(--text);
  font-size: 0.95rem;
  margin: 1rem 0 0.4rem;
}

.subtitle {
  color: var(--text-muted);
  font-size: 0.85rem;
  margin-bottom: 2rem;
}

.cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 1rem;
}

.card-label {
  font-size: 0.72rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.card-value {
  font-size: 1.4rem;
  font-weight: 700;
  color: var(--accent);
  margin-top: 0.25rem;
}

.score-badge {
  display: inline-block;
  background: linear-gradient(135deg, var(--accent), var(--accent2));
  border-radius: 8px;
  padding: 0.5rem 1.2rem;
  font-size: 1.6rem;
  font-weight: 800;
  color: white;
  margin-right: 1rem;
}

.grade-badge {
  display: inline-block;
  border: 2px solid var(--accent);
  border-radius: 8px;
  padding: 0.3rem 0.8rem;
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--accent);
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.85rem;
  margin-bottom: 1rem;
}

thead th {
  background: var(--surface2);
  color: var(--text-muted);
  font-weight: 600;
  text-align: left;
  padding: 0.6rem 0.8rem;
  border-bottom: 1px solid var(--border);
  text-transform: uppercase;
  font-size: 0.72rem;
  letter-spacing: 0.06em;
}

tbody tr:hover { background: var(--surface); }

tbody td {
  padding: 0.55rem 0.8rem;
  border-bottom: 1px solid var(--border);
  color: var(--text);
}

.tag {
  display: inline-block;
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 0.1rem 0.4rem;
  font-size: 0.75rem;
  color: var(--accent);
}

.warning-box {
  background: rgba(245, 158, 11, 0.08);
  border-left: 3px solid var(--warning);
  border-radius: 6px;
  padding: 0.75rem 1rem;
  margin: 0.4rem 0;
  font-size: 0.85rem;
  color: var(--warning);
}

.rec-box {
  background: rgba(99, 102, 241, 0.08);
  border-left: 3px solid var(--accent);
  border-radius: 6px;
  padding: 0.75rem 1rem;
  margin: 0.4rem 0;
  font-size: 0.85rem;
  color: var(--text);
}

footer {
  margin-top: 3rem;
  color: var(--text-muted);
  font-size: 0.75rem;
  border-top: 1px solid var(--border);
  padding-top: 1rem;
}
"""


def _col_stats_html(col: ColumnProfile) -> str:
    if col.numeric_stats:
        ns = col.numeric_stats
        return f"""
        <h3>{col.name} <span class="tag">{col.dtype}</span></h3>
        <table>
          <thead><tr><th>Statistic</th><th>Value</th><th>Statistic</th><th>Value</th></tr></thead>
          <tbody>
            <tr><td>Mean</td><td>{ns.mean}</td><td>Std Dev</td><td>{ns.std}</td></tr>
            <tr><td>Median</td><td>{ns.median}</td><td>Variance</td><td>{ns.variance}</td></tr>
            <tr><td>Mode</td><td>{ns.mode if ns.mode is not None else 'N/A'}</td><td>Skewness</td><td>{ns.skewness}</td></tr>
            <tr><td>Min</td><td>{ns.minimum}</td><td>Kurtosis</td><td>{ns.kurtosis}</td></tr>
            <tr><td>Max</td><td>{ns.maximum}</td><td>Zeros</td><td>{ns.zeros}</td></tr>
            <tr><td>Q1</td><td>{ns.q1}</td><td>Negatives</td><td>{ns.negatives}</td></tr>
            <tr><td>Q3</td><td>{ns.q3}</td><td>IQR</td><td>{ns.iqr}</td></tr>
          </tbody>
        </table>"""
    elif col.categorical_stats:
        cs = col.categorical_stats
        top_rows = "".join(
            f"<tr><td>{v}</td><td>{c}</td></tr>"
            for v, c in cs.top_values
        )
        return f"""
        <h3>{col.name} <span class="tag">{col.dtype}</span></h3>
        <table>
          <thead><tr><th>Statistic</th><th>Value</th></tr></thead>
          <tbody>
            <tr><td>Distinct Values</td><td>{cs.distinct_count}</td></tr>
            <tr><td>Most Frequent</td><td>{cs.most_frequent} ({cs.most_frequent_pct}%)</td></tr>
            <tr><td>Least Frequent</td><td>{cs.least_frequent} ({cs.least_frequent_pct}%)</td></tr>
          </tbody>
        </table>
        <h3>Top Values</h3>
        <table><thead><tr><th>Value</th><th>Count</th></tr></thead>
        <tbody>{top_rows}</tbody></table>"""
    elif col.datetime_stats:
        ds = col.datetime_stats
        return f"""
        <h3>{col.name} <span class="tag">{col.dtype}</span></h3>
        <table>
          <thead><tr><th>Statistic</th><th>Value</th></tr></thead>
          <tbody>
            <tr><td>Earliest</td><td>{ds.earliest}</td></tr>
            <tr><td>Latest</td><td>{ds.latest}</td></tr>
            <tr><td>Range (days)</td><td>{ds.date_range_days}</td></tr>
            <tr><td>Most Frequent Date</td><td>{ds.most_frequent}</td></tr>
          </tbody>
        </table>"""
    elif col.boolean_stats:
        bs = col.boolean_stats
        return f"""
        <h3>{col.name} <span class="tag">{col.dtype}</span></h3>
        <table>
          <thead><tr><th>Statistic</th><th>Value</th></tr></thead>
          <tbody>
            <tr><td>True</td><td>{bs.true_count} ({bs.true_pct}%)</td></tr>
            <tr><td>False</td><td>{bs.false_count} ({bs.false_pct}%)</td></tr>
            <tr><td>Null</td><td>{bs.null_count}</td></tr>
          </tbody>
        </table>"""
    return ""


class HTMLExporter:
    """Exports a DatasetProfile to a styled HTML report file."""

    @staticmethod
    def export(profile: DatasetProfile, output_path: Path) -> Path:
        """
        Writes a full dark-themed HTML report.

        Parameters
        ----------
        profile : DatasetProfile
            The profile to render.
        output_path : Path
            Destination .html file.

        Returns
        -------
        Path
            Path to the written file.
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        c = profile.completeness

        # Column summary rows
        col_rows = ""
        for i, col in enumerate(profile.column_profiles, 1):
            missing = f"{col.missing_count} ({col.missing_percentage:.1f}%)"
            unique = f"{col.unique_count} ({col.unique_percentage:.1f}%)"
            nullable = "Yes" if col.nullable else "No"
            col_rows += f"""
            <tr>
              <td>{i}</td>
              <td><strong>{col.name}</strong></td>
              <td><span class="tag">{col.dtype}</span></td>
              <td>{nullable}</td>
              <td>{missing}</td>
              <td>{unique}</td>
              <td>{SizeFormatter.format(col.memory_usage)}</td>
            </tr>"""

        # Statistics section
        stats_html = ""
        has_stats = any(
            col.numeric_stats or col.categorical_stats
            or col.datetime_stats or col.boolean_stats
            for col in profile.column_profiles
        )
        if has_stats:
            stats_content = "".join(
                _col_stats_html(col) for col in profile.column_profiles
                if col.numeric_stats or col.categorical_stats
                or col.datetime_stats or col.boolean_stats
            )
            stats_html = f"<h2>Column Statistics</h2>{stats_content}"

        # Health score
        score_html = ""
        if profile.health_score:
            hs = profile.health_score
            score_html = f"""
            <h2>Health Score</h2>
            <span class="score-badge">{hs.score}</span>
            <span class="grade-badge">Grade {hs.grade}</span>
            <p style="color: var(--text-muted); margin-top: 0.5rem; font-size: 0.85rem;">
              Score out of 100 based on completeness, duplicates, data quality, and outlier checks.
            </p>"""

        # Quality report
        quality_html = ""
        if profile.quality_report:
            qr = profile.quality_report
            warnings_html = "".join(
                f'<div class="warning-box">⚠ {w}</div>' for w in qr.warnings
            ) or "<p style='color: var(--text-muted)'>No warnings.</p>"
            recs_html = "".join(
                f'<div class="rec-box">→ {r}</div>' for r in qr.recommendations
            ) or ""
            quality_html = f"""
            <h2>Data Quality</h2>
            <table>
              <thead><tr><th>Check</th><th>Result</th></tr></thead>
              <tbody>
                <tr><td>Constant Columns</td><td>{', '.join(qr.constant_columns) or 'None'}</td></tr>
                <tr><td>High Cardinality Columns</td><td>{', '.join(qr.high_cardinality_columns) or 'None'}</td></tr>
                <tr><td>Mixed Type Columns</td><td>{', '.join(qr.mixed_type_columns.keys()) or 'None'}</td></tr>
                <tr><td>Columns with Outliers</td><td>{', '.join(qr.outlier_columns) or 'None'}</td></tr>
                <tr><td>Duplicate Rows</td><td>{qr.duplicate_rows}</td></tr>
              </tbody>
            </table>
            <h3 style="margin: 1rem 0 0.5rem">Warnings</h3>
            {warnings_html}
            {recs_html}"""

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>DataProfiler Report — {profile.dataset_name}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>{_CSS}</style>
</head>
<body>
  <h1>DataProfiler Report</h1>
  <p class="subtitle">Dataset: <strong>{profile.dataset_name}</strong></p>

  <h2>Overview</h2>
  <div class="cards">
    <div class="card"><div class="card-label">Rows</div><div class="card-value">{profile.rows:,}</div></div>
    <div class="card"><div class="card-label">Columns</div><div class="card-value">{profile.columns}</div></div>
    <div class="card"><div class="card-label">Memory</div><div class="card-value">{SizeFormatter.format(profile.memory_usage)}</div></div>
    <div class="card"><div class="card-label">Duplicates</div><div class="card-value">{profile.duplicate_rows}</div></div>
    <div class="card"><div class="card-label">Completeness</div><div class="card-value">{c.completeness_percentage:.1f}%</div></div>
    <div class="card"><div class="card-label">Missing Cells</div><div class="card-value">{c.missing_cells:,}</div></div>
  </div>

  {score_html}

  <h2>Column Summary</h2>
  <table>
    <thead>
      <tr>
        <th>#</th><th>Column</th><th>Type</th><th>Nullable</th>
        <th>Missing</th><th>Unique</th><th>Memory</th>
      </tr>
    </thead>
    <tbody>{col_rows}</tbody>
  </table>

  {stats_html}
  {quality_html}

  <footer>Generated by <strong>DataProfiler</strong></footer>
</body>
</html>"""

        output_path.write_text(html, encoding="utf-8")
        return output_path
