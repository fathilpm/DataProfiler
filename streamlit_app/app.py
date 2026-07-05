from __future__ import annotations

import sys
from pathlib import Path

# Ensure the project root is on sys.path so 'profiler' is importable
# regardless of where Streamlit is launched from.
sys.path.insert(0, str(Path(__file__).parent.parent))

import io
import tempfile
from pathlib import Path

try:
    import streamlit as st
    _ST = True
except ImportError:
    raise ImportError("Run: pip install streamlit")

import pandas as pd

from profiler.config.profile_config import ProfileConfig
from profiler.engine.profiler_engine import ProfilerEngine
from profiler.exporters.html import HTMLExporter
from profiler.exporters.json import JSONExporter
from profiler.exporters.markdown import MarkdownExporter
from profiler.exporters.pdf import PDFExporter
from profiler.models.dataset import Dataset
from profiler.models.datasource import DataSource
from profiler.utils.size_formatter import SizeFormatter


# ── Page config ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="DataProfiler",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Styles ────────────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.main { background: #0f0f1a; }

.stApp { background: #0f0f1a; }

[data-testid="stSidebar"] {
    background: #1a1a2e;
    border-right: 1px solid #2d2d50;
}

.metric-card {
    background: #1a1a2e;
    border: 1px solid #2d2d50;
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
}
.metric-label {
    font-size: 0.72rem;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.metric-value {
    font-size: 1.6rem;
    font-weight: 800;
    color: #6366f1;
    margin-top: 0.25rem;
}
.score-big {
    font-size: 3rem;
    font-weight: 900;
    background: linear-gradient(135deg, #6366f1, #8b5cf6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.grade-box {
    display: inline-block;
    border: 2px solid #6366f1;
    border-radius: 8px;
    padding: 0.2rem 0.8rem;
    font-size: 1.2rem;
    font-weight: 700;
    color: #6366f1;
    margin-left: 0.5rem;
}
.warning-tag {
    background: rgba(245,158,11,0.1);
    border-left: 3px solid #f59e0b;
    border-radius: 4px;
    padding: 0.5rem 0.75rem;
    margin: 0.25rem 0;
    color: #f59e0b;
    font-size: 0.85rem;
}
.rec-tag {
    background: rgba(99,102,241,0.08);
    border-left: 3px solid #6366f1;
    border-radius: 4px;
    padding: 0.5rem 0.75rem;
    margin: 0.25rem 0;
    color: #e2e8f0;
    font-size: 0.85rem;
}
</style>
""", unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("## 📊 DataProfiler")
    st.markdown("---")

    st.markdown("### Upload Dataset")
    uploaded = st.file_uploader(
        "Drop a CSV or Excel file",
        type=["csv", "xlsx", "xls"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown("### Analysis Options")

    run_stats = st.checkbox("Statistics", value=True)
    run_quality = st.checkbox("Data Quality", value=True)
    top_n = st.slider("Top N categorical values", 3, 20, 5, help="Controls how many distinct values to show in the Statistics tab for text/category columns.")
    preview_rows = st.slider("Preview rows", 5, 100, 20, help="Controls how many rows to show in the Data Preview table.")

    st.markdown("---")
    st.markdown("### About")
    st.caption("DataProfiler — Dataset profiling tool.\nBuilt with Python & Streamlit.")


# ── Main ─────────────────────────────────────────────────────────────────────

st.markdown("# 📊 DataProfiler")
st.markdown("*Upload a dataset to generate a full profile.*")

if not uploaded:
    st.info("👈 Upload a CSV or Excel file from the sidebar to get started.")
    st.stop()

# ── Load data ─────────────────────────────────────────────────────────────────

@st.cache_data
def load_data(file_bytes: bytes, filename: str) -> pd.DataFrame:
    ext = Path(filename).suffix.lower()
    buf = io.BytesIO(file_bytes)
    if ext == ".csv":
        return pd.read_csv(buf)
    return pd.read_excel(buf)


with st.spinner("Loading dataset..."):
    df = load_data(uploaded.read(), uploaded.name)

source = DataSource(
    name=uploaded.name,
    source_type=Path(uploaded.name).suffix.lstrip("."),
    location=uploaded.name,
)
dataset = Dataset(dataframe=df, source=source)

config = ProfileConfig(
    run_statistics=run_stats,
    run_quality=run_quality,
    top_n_values=top_n,
    run_visualization=False,
)

with st.spinner("Profiling dataset..."):
    profile = ProfilerEngine.profile(dataset, config=config)

# ── Tabs ─────────────────────────────────────────────────────────────────────

tab_overview, tab_columns, tab_stats, tab_quality, tab_export = st.tabs([
    "📋 Overview", "🗂️ Columns", "📈 Statistics", "🔍 Quality", "📥 Export"
])


# ── Tab: Overview ─────────────────────────────────────────────────────────────

with tab_overview:
    c = profile.completeness
    hs = profile.health_score

    cols = st.columns(6)
    metrics = [
        ("Rows", f"{profile.rows:,}"),
        ("Columns", str(profile.columns)),
        ("Memory", SizeFormatter.format(profile.memory_usage)),
        ("Duplicates", str(profile.duplicate_rows)),
        ("Completeness", f"{c.completeness_percentage:.1f}%"),
        ("Missing Cells", f"{c.missing_cells:,}"),
    ]
    for col_ui, (label, value) in zip(cols, metrics):
        with col_ui:
            st.markdown(
                f'<div class="metric-card">'
                f'<div class="metric-label">{label}</div>'
                f'<div class="metric-value">{value}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

    if hs:
        st.markdown("---")
        st.markdown("### 🏥 Health Score")
        left, right = st.columns([1, 3])
        with left:
            st.markdown(
                f'<div class="score-big">{hs.score}</div>'
                f'<span class="grade-box">Grade {hs.grade}</span>',
                unsafe_allow_html=True,
            )
        with right:
            breakdown_df = pd.DataFrame(
                [(k.replace("_", " ").title(), f"-{v}") for k, v in hs.breakdown.items() if v > 0],
                columns=["Deduction Reason", "Points Deducted"],
            )
            if not breakdown_df.empty:
                st.dataframe(breakdown_df, use_container_width=True, hide_index=True)
            else:
                st.success("No deductions — perfect score!")

    st.markdown("---")
    st.markdown(f"### 📄 Data Preview (First {preview_rows} Rows)")
    st.dataframe(df.head(preview_rows), use_container_width=True)


# ── Tab: Columns ─────────────────────────────────────────────────────────────

with tab_columns:
    st.markdown("### 🗂️ Column Summary")
    rows = []
    for i, col in enumerate(profile.column_profiles, 1):
        rows.append({
            "#": i,
            "Column": col.name,
            "Type": col.dtype,
            "Raw Type": col.raw_dtype,
            "Nullable": "Yes" if col.nullable else "No",
            "Missing": f"{col.missing_count} ({col.missing_percentage:.1f}%)",
            "Unique": f"{col.unique_count} ({col.unique_percentage:.1f}%)",
            "Memory": SizeFormatter.format(col.memory_usage),
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


# ── Tab: Statistics ───────────────────────────────────────────────────────────

with tab_stats:
    if not run_stats:
        st.info("Statistics are disabled. Enable them in the sidebar.")
    else:
        st.markdown("### 📈 Column Statistics")
        for col in profile.column_profiles:
            with st.expander(f"**{col.name}** — {col.dtype}"):
                if col.numeric_stats:
                    ns = col.numeric_stats
                    d = {
                        "Mean": ns.mean, "Median": ns.median,
                        "Mode": ns.mode, "Std Dev": ns.std,
                        "Variance": ns.variance, "Min": ns.minimum,
                        "Max": ns.maximum, "Q1": ns.q1, "Q3": ns.q3,
                        "IQR": ns.iqr, "Skewness": ns.skewness,
                        "Kurtosis": ns.kurtosis,
                        "Zeros": ns.zeros, "Negatives": ns.negatives,
                    }
                    c1, c2 = st.columns(2)
                    items = list(d.items())
                    half = len(items) // 2
                    with c1:
                        st.table(pd.DataFrame(items[:half], columns=["Stat", "Value"]))
                    with c2:
                        st.table(pd.DataFrame(items[half:], columns=["Stat", "Value"]))

                elif col.categorical_stats:
                    cs = col.categorical_stats
                    st.metric("Distinct Values", cs.distinct_count)
                    st.metric("Most Frequent", f"{cs.most_frequent} ({cs.most_frequent_pct}%)")
                    st.metric("Least Frequent", f"{cs.least_frequent} ({cs.least_frequent_pct}%)")
                    if cs.top_values:
                        st.markdown("**Top Values**")
                        st.dataframe(
                            pd.DataFrame(cs.top_values, columns=["Value", "Count"]),
                            hide_index=True,
                        )

                elif col.datetime_stats:
                    ds = col.datetime_stats
                    st.metric("Earliest", ds.earliest)
                    st.metric("Latest", ds.latest)
                    st.metric("Range (days)", ds.date_range_days)

                elif col.boolean_stats:
                    bs = col.boolean_stats
                    c1, c2, c3 = st.columns(3)
                    c1.metric("True", f"{bs.true_count} ({bs.true_pct}%)")
                    c2.metric("False", f"{bs.false_count} ({bs.false_pct}%)")
                    c3.metric("Null", bs.null_count)

                else:
                    st.caption("No statistics computed for this column type.")


# ── Tab: Quality ──────────────────────────────────────────────────────────────

with tab_quality:
    if not run_quality or not profile.quality_report:
        st.info("Quality analysis is disabled. Enable it in the sidebar.")
    else:
        qr = profile.quality_report

        st.markdown("### 🔍 Quality Findings")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Constant Columns**")
            if qr.constant_columns:
                for cc in qr.constant_columns:
                    st.error(f"x {cc}")
            else:
                st.success("None")

        with c2:
            st.markdown("**High Cardinality Columns**")
            if qr.high_cardinality_columns:
                for hc in qr.high_cardinality_columns:
                    st.warning(f"!! {hc}")
            else:
                st.success("None")

            st.markdown("**Outlier Columns**")
            if qr.outlier_columns:
                for oc in qr.outlier_columns:
                    st.warning(f"!! {oc}")
            else:
                st.success("None")

        if qr.mixed_type_columns:
            st.markdown("**Mixed Type Columns**")
            for col_name, types in qr.mixed_type_columns.items():
                st.error(f"✗ {col_name}: {', '.join(types)}")

        st.markdown("---")
        st.markdown("### ⚠️ Warnings")
        if qr.warnings:
            for w in qr.warnings:
                st.markdown(
                    f'<div class="warning-tag">⚠ {w}</div>',
                    unsafe_allow_html=True,
                )
        else:
            st.success("No warnings!")

        st.markdown("### 💡 Recommendations")
        if qr.recommendations:
            for r in qr.recommendations:
                st.markdown(
                    f'<div class="rec-tag">→ {r}</div>',
                    unsafe_allow_html=True,
                )
        else:
            st.success("No recommendations — your dataset looks clean!")


# ── Tab: Export ───────────────────────────────────────────────────────────────

with tab_export:
    st.markdown("### 📥 Download Reports")

    # HTML export
    st.markdown("#### HTML Report")
    with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as tmp:
        html_path = Path(tmp.name)
    HTMLExporter.export(profile, html_path)
    html_bytes = html_path.read_bytes()
    st.download_button(
        "⬇ Download HTML Report",
        data=html_bytes,
        file_name=f"{Path(profile.dataset_name).stem}_report.html",
        mime="text/html",
    )

    st.markdown("---")

    # JSON export
    st.markdown("#### JSON Export")
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
        json_path = Path(tmp.name)
    JSONExporter.export(profile, json_path)
    json_bytes = json_path.read_bytes()
    st.download_button(
        "⬇ Download JSON Export",
        data=json_bytes,
        file_name=f"{Path(profile.dataset_name).stem}_report.json",
        mime="application/json",
    )

    st.markdown("---")

    # Markdown export
    st.markdown("#### Markdown Report")
    with tempfile.NamedTemporaryFile(suffix=".md", delete=False, mode="w") as tmp:
        md_path = Path(tmp.name)
    MarkdownExporter.export(profile, md_path)
    md_bytes = md_path.read_bytes()
    st.download_button(
        "⬇ Download Markdown Report",
        data=md_bytes,
        file_name=f"{Path(profile.dataset_name).stem}_report.md",
        mime="text/markdown",
    )

    st.markdown("---")

    # PDF export
    st.markdown("#### PDF Report")
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        pdf_path = Path(tmp.name)
    PDFExporter.export(profile, pdf_path)
    pdf_bytes = pdf_path.read_bytes()
    st.download_button(
        "⬇ Download PDF Report",
        data=pdf_bytes,
        file_name=f"{Path(profile.dataset_name).stem}_report.pdf",
        mime="application/pdf",
    )
