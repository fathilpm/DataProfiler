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
from profiler.preprocessing import (
    SimpleImputer, ColumnDropper, TypeConverter, RowDropperNA,
    AutoPreprocessor, MinMaxScaler, StandardScaler, RobustScaler,
    OneHotEncoder, LabelEncoder, OutlierCapper
)
from profiler.utils.copilot import GeminiCopilot


# â”€â”€ Page config â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
st.set_page_config(
    page_title="DataProfiler",
    page_icon="ðŸ“Š",
    layout="wide",
    initial_sidebar_state="expanded",
)

# â”€â”€ Styles â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=Inter:wght@300;400;500;600;700&display=swap');

/* â”€â”€â”€ BASE TYPOGRAPHY & FONTS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

/* â”€â”€â”€ ANIMATED BACKGROUND â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
.stApp {
    background: #070a14 !important;
    color: #CBD5E1;
    min-height: 100vh;
}
.stApp::before {
    content: '';
    position: fixed;
    top: -30%;
    left: -20%;
    width: 700px;
    height: 700px;
    background: radial-gradient(circle, rgba(99,102,241,0.12) 0%, transparent 65%);
    pointer-events: none;
    z-index: 0;
    animation: orb1 12s ease-in-out infinite alternate;
}
.stApp::after {
    content: '';
    position: fixed;
    bottom: -20%;
    right: -10%;
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, rgba(139,92,246,0.10) 0%, transparent 65%);
    pointer-events: none;
    z-index: 0;
    animation: orb2 15s ease-in-out infinite alternate;
}
@keyframes orb1 {
    from { transform: translate(0, 0) scale(1);   }
    to   { transform: translate(80px, 60px) scale(1.15); }
}
@keyframes orb2 {
    from { transform: translate(0, 0) scale(1);   }
    to   { transform: translate(-60px, -40px) scale(1.1); }
}
.main { background: transparent !important; }
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 3rem !important;
    max-width: 1200px !important;
}

/* â”€â”€â”€ SIDEBAR â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0c0d1a 0%, #0a0b15 100%) !important;
    border-right: 1px solid rgba(99,102,241,0.10) !important;
    box-shadow: 4px 0 30px rgba(0,0,0,0.4) !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.5rem !important;
}
/* Sidebar image centering */
[data-testid="stSidebar"] [data-testid="stImage"] {
    display: flex;
    justify-content: center;
    margin-bottom: 0.5rem;
}
[data-testid="stSidebar"] [data-testid="stImage"] img {
    border-radius: 16px;
    box-shadow: 0 0 30px rgba(99,102,241,0.3);
    border: 1px solid rgba(99,102,241,0.2);
}
/* Sidebar section headers */
[data-testid="stSidebar"] h3 {
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    color: #6366f1 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12em !important;
    margin-top: 1.75rem !important;
    margin-bottom: 0.85rem !important;
    display: flex;
    align-items: center;
    gap: 6px;
}
[data-testid="stSidebar"] h3::before {
    content: '';
    display: inline-block;
    width: 18px;
    height: 2px;
    background: linear-gradient(90deg, #6366f1, #a78bfa);
    border-radius: 2px;
    flex-shrink: 0;
}
/* Caption */
[data-testid="stSidebar"] .stCaption {
    color: #374151 !important;
    font-size: 0.78rem !important;
}
/* Sidebar divider */
[data-testid="stSidebar"] hr {
    border-color: rgba(99,102,241,0.12) !important;
    margin: 1rem 0 !important;
}

/* â”€â”€â”€ FILE UPLOADER â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
[data-testid="stFileUploader"] {
    background: rgba(99,102,241,0.03) !important;
    border: 2px dashed rgba(99,102,241,0.22) !important;
    border-radius: 14px !important;
    transition: all 0.3s ease !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: rgba(99,102,241,0.55) !important;
    background: rgba(99,102,241,0.06) !important;
    box-shadow: 0 0 24px rgba(99,102,241,0.12) !important;
}
[data-testid="stFileUploader"] small,
[data-testid="stFileUploader"] span {
    color: #64748B !important;
}
[data-testid="stFileUploader"] [data-testid="stBaseButton-secondary"] {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 0.45rem 1.2rem !important;
    box-shadow: 0 4px 16px rgba(99,102,241,0.35) !important;
    transition: all 0.2s ease !important;
}
[data-testid="stFileUploader"] [data-testid="stBaseButton-secondary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 22px rgba(99,102,241,0.5) !important;
}

/* â”€â”€â”€ CHECKBOXES â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
div[data-testid="stCheckbox"] label {
    gap: 10px !important;
    align-items: center !important;
}
div[data-testid="stCheckbox"] label span {
    color: #94A3B8 !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.01em !important;
}
div[data-testid="stCheckbox"] div[role="checkbox"] {
    border: 2px solid rgba(99,102,241,0.3) !important;
    border-radius: 6px !important;
    background: rgba(99,102,241,0.04) !important;
    width: 18px !important;
    height: 18px !important;
    transition: all 0.2s ease !important;
}
div[data-testid="stCheckbox"] div[role="checkbox"][aria-checked="true"] {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
    border-color: transparent !important;
    box-shadow: 0 0 10px rgba(99,102,241,0.4) !important;
}

/* â”€â”€â”€ SLIDERS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
[data-testid="stSlider"] [data-testid="stThumbValue"] {
    color: #a78bfa !important;
    font-weight: 700 !important;
}
[data-testid="stSlider"] > div > div > div {
    background: linear-gradient(90deg, #6366f1, #8b5cf6) !important;
}

/* â”€â”€â”€ SELECT BOXES â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
div[data-baseweb="select"] > div {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(99,102,241,0.2) !important;
    border-radius: 10px !important;
    color: #E2E8F0 !important;
    transition: all 0.2s ease !important;
}
div[data-baseweb="select"] > div:hover {
    border-color: rgba(99,102,241,0.5) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.08) !important;
}
div[data-baseweb="select"] > div:focus-within {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
}

/* â”€â”€â”€ TEXT INPUTS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
div[data-baseweb="input"] input {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid rgba(99,102,241,0.2) !important;
    border-radius: 10px !important;
    color: #E2E8F0 !important;
    transition: all 0.2s ease !important;
}
div[data-baseweb="input"] input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
}

/* â”€â”€â”€ EXPANDERS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
details[data-testid="stExpander"] {
    background: rgba(255,255,255,0.02) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 12px !important;
    margin-bottom: 0.65rem !important;
    overflow: hidden !important;
    transition: border-color 0.2s ease !important;
}
details[data-testid="stExpander"]:hover {
    border-color: rgba(99,102,241,0.25) !important;
}
details[data-testid="stExpander"] summary {
    padding: 1rem 1.25rem !important;
    font-weight: 600 !important;
    color: #CBD5E1 !important;
    cursor: pointer !important;
}
details[data-testid="stExpander"][open] {
    border-color: rgba(99,102,241,0.3) !important;
    box-shadow: 0 0 20px rgba(99,102,241,0.06) !important;
}

/* â”€â”€â”€ HEADINGS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
h1, h2, h3, h4, h5 {
    font-family: 'Outfit', sans-serif !important;
    letter-spacing: -0.025em;
    color: #F1F5F9 !important;
}
h1 { font-weight: 900 !important; }
h2 { font-weight: 800 !important; }
h3 { font-weight: 700 !important; color: #E2E8F0 !important; }

/* â”€â”€â”€ GRADIENT HEADER â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
.gradient-header {
    background: linear-gradient(135deg, #c4b5fd 0%, #818cf8 45%, #60a5fa 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 900 !important;
    letter-spacing: -0.05em !important;
    line-height: 1.1 !important;
}

/* â”€â”€â”€ METRIC CARDS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
.metric-card {
    background: linear-gradient(145deg, rgba(15,16,28,0.9) 0%, rgba(20,21,36,0.7) 100%);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 1.4rem 1.5rem;
    text-align: left;
    transition: all 0.3s cubic-bezier(0.4,0,0.2,1);
    box-shadow: 0 4px 24px rgba(0,0,0,0.35), inset 0 1px 0 rgba(255,255,255,0.05);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    position: relative;
    overflow: hidden;
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(99,102,241,0.4), transparent);
}
.metric-card:hover {
    border-color: rgba(99,102,241,0.35);
    transform: translateY(-3px);
    box-shadow: 0 12px 40px rgba(99,102,241,0.18), inset 0 1px 0 rgba(255,255,255,0.07);
}
.metric-label {
    font-size: 0.72rem;
    color: #64748B;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.10em;
    margin-bottom: 0.5rem;
}
.metric-value {
    font-size: 2rem;
    font-weight: 800;
    color: #F1F5F9;
    letter-spacing: -0.04em;
    font-family: 'Outfit', sans-serif;
    line-height: 1;
}

/* â”€â”€â”€ HEALTH SCORE â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
.score-big {
    font-size: 5.5rem;
    font-weight: 900;
    line-height: 1;
    letter-spacing: -0.06em;
    font-family: 'Outfit', sans-serif;
    background: linear-gradient(135deg, #f1f5f9 0%, #818cf8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.grade-box {
    display: inline-block;
    border: 1px solid rgba(99,102,241,0.4);
    background: rgba(99,102,241,0.12);
    border-radius: 10px;
    padding: 0.35rem 0.9rem;
    font-size: 1rem;
    font-weight: 700;
    color: #a78bfa;
    margin-left: 0.75rem;
    vertical-align: super;
    box-shadow: 0 0 20px rgba(99,102,241,0.15);
    font-family: 'Outfit', sans-serif;
}

/* â”€â”€â”€ BUTTONS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
.stButton > button {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.6rem 1.5rem !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.01em !important;
    transition: all 0.2s cubic-bezier(0.4,0,0.2,1) !important;
    box-shadow: 0 4px 16px rgba(99,102,241,0.30) !important;
    position: relative !important;
    overflow: hidden !important;
}
.stButton > button::before {
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 100%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.12), transparent);
    transition: left 0.5s ease;
}
.stButton > button:hover::before { left: 100%; }
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(99,102,241,0.45) !important;
}
.stButton > button:active {
    transform: translateY(0px) !important;
    box-shadow: 0 2px 8px rgba(99,102,241,0.25) !important;
}

/* â”€â”€â”€ NAVIGATION RADIO (VIEW SWITCHER) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
div[data-testid="stHorizontalBlock"]:has(div.row-widget.stRadio) {
    background: rgba(10,11,20,0.8) !important;
    border-radius: 14px !important;
    padding: 5px !important;
    border: 1px solid rgba(99,102,241,0.12) !important;
    backdrop-filter: blur(10px) !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.3) !important;
}
div.row-widget.stRadio > div {
    background: transparent !important;
    padding: 0 !important;
    border: none !important;
    gap: 4px !important;
    box-shadow: none !important;
    display: flex !important;
}
div.row-widget.stRadio label {
    color: #64748B !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 9px 20px !important;
    border-radius: 10px !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
    letter-spacing: 0.01em !important;
}
div.row-widget.stRadio label:hover {
    color: #E2E8F0 !important;
    background: rgba(99,102,241,0.08) !important;
}
div.row-widget.stRadio div[data-checked="true"] {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
    border-radius: 10px !important;
    box-shadow: 0 4px 16px rgba(99,102,241,0.35) !important;
}
div.row-widget.stRadio div[data-checked="true"] label {
    color: #fff !important;
}

/* â”€â”€â”€ TABS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
div[data-baseweb="tab-list"] {
    background: rgba(10,11,20,0.85) !important;
    border-radius: 14px !important;
    padding: 5px !important;
    border: 1px solid rgba(99,102,241,0.10) !important;
    gap: 4px !important;
    margin-bottom: 2rem !important;
    backdrop-filter: blur(10px) !important;
}
div[data-baseweb="tab"] {
    color: #64748B !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    border: none !important;
    padding: 9px 18px !important;
    border-radius: 10px !important;
    transition: all 0.2s ease !important;
    background: transparent !important;
    letter-spacing: 0.01em !important;
}
div[data-baseweb="tab"]:hover {
    color: #E2E8F0 !important;
    background: rgba(99,102,241,0.08) !important;
}
div[data-baseweb="tab"][aria-selected="true"] {
    color: #fff !important;
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%) !important;
    box-shadow: 0 4px 16px rgba(99,102,241,0.30) !important;
}
div[role="tablist"] > div[style*="left"] { display: none !important; }

/* â”€â”€â”€ DATAFRAMES â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
[data-testid="stDataFrame"] {
    border-radius: 14px !important;
    border: 1px solid rgba(99,102,241,0.12) !important;
    overflow: hidden !important;
    box-shadow: 0 4px 24px rgba(0,0,0,0.25) !important;
}
[data-testid="stDataFrame"] thead tr th {
    background: rgba(99,102,241,0.08) !important;
    color: #94A3B8 !important;
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
    border-bottom: 1px solid rgba(99,102,241,0.15) !important;
}
[data-testid="stDataFrame"] tbody tr:hover td {
    background: rgba(99,102,241,0.05) !important;
}

/* â”€â”€â”€ ALERTS / INFO BOXES â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    border-left-width: 3px !important;
    backdrop-filter: blur(8px) !important;
}
div[data-testid="stAlert"][kind="info"] {
    background: rgba(59,130,246,0.07) !important;
    border-color: rgba(59,130,246,0.35) !important;
    color: #93C5FD !important;
}
div[data-testid="stAlert"][kind="success"] {
    background: rgba(16,185,129,0.07) !important;
    border-color: rgba(16,185,129,0.35) !important;
    color: #6EE7B7 !important;
}
div[data-testid="stAlert"][kind="warning"] {
    background: rgba(245,158,11,0.07) !important;
    border-color: rgba(245,158,11,0.35) !important;
    color: #FCD34D !important;
}
div[data-testid="stAlert"][kind="error"] {
    background: rgba(239,68,68,0.07) !important;
    border-color: rgba(239,68,68,0.35) !important;
    color: #FCA5A5 !important;
}

/* â”€â”€â”€ SPINNERS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
[data-testid="stSpinner"] > div {
    border-color: rgba(99,102,241,0.25) !important;
    border-top-color: #8b5cf6 !important;
}

/* â”€â”€â”€ WARNING / REC TAGS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
.warning-tag {
    background: rgba(245,158,11,0.08);
    border: 1px solid rgba(245,158,11,0.22);
    border-radius: 10px;
    padding: 0.8rem 1.1rem;
    margin: 0.5rem 0;
    color: #FCD34D;
    font-size: 0.88rem;
    font-weight: 500;
    display: flex;
    align-items: flex-start;
    gap: 8px;
}
.rec-tag {
    background: rgba(59,130,246,0.08);
    border: 1px solid rgba(59,130,246,0.22);
    border-radius: 10px;
    padding: 0.8rem 1.1rem;
    margin: 0.5rem 0;
    color: #93C5FD;
    font-size: 0.88rem;
    font-weight: 500;
    display: flex;
    align-items: flex-start;
    gap: 8px;
}

/* â”€â”€â”€ DIVIDERS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
hr {
    border: none !important;
    height: 1px !important;
    background: linear-gradient(90deg, transparent, rgba(99,102,241,0.15), transparent) !important;
    margin: 1.5rem 0 !important;
}

/* â”€â”€â”€ DOWNLOAD BUTTON â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
a[data-testid="stDownloadButton-Link"] button {
    background: rgba(99,102,241,0.10) !important;
    color: #a78bfa !important;
    border: 1px solid rgba(99,102,241,0.25) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
}
a[data-testid="stDownloadButton-Link"] button:hover {
    background: rgba(99,102,241,0.20) !important;
    border-color: rgba(99,102,241,0.5) !important;
    transform: translateY(-1px) !important;
}

/* â”€â”€â”€ SUBHEADERS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
h2[data-testid="stHeading"], h3[data-testid="stHeading"] {
    padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(99,102,241,0.12);
    margin-bottom: 1.25rem;
}

/* â”€â”€â”€ SCROLLBARS â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: rgba(99,102,241,0.25);
    border-radius: 999px;
}
::-webkit-scrollbar-thumb:hover {
    background: rgba(99,102,241,0.5);
}

/* â”€â”€â”€ SELECTION â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ */
::selection {
    background: rgba(99,102,241,0.35);
    color: #fff;
}
</style>
""", unsafe_allow_html=True)


# â”€â”€ Sidebar â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
_logo_path = Path(__file__).parent / "dataprofiler_logo.png"
with st.sidebar:
    if _logo_path.exists():
        st.image(str(_logo_path), width=160)
    else:
        st.markdown("""
        <div style='margin-bottom: 1.5rem; margin-top: 0.5rem;'>
            <h2 style='margin: 0; letter-spacing: -0.04em;'>DataProfiler.</h2>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("### Upload Dataset")
    uploaded = st.file_uploader("Drop a CSV or Excel file", type=["csv", "xlsx", "xls"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("### Analysis Options")
    run_stats = st.checkbox("Statistics", value=True)
    run_quality = st.checkbox("Data Quality", value=True)
    top_n = st.slider("Top N categorical values", 3, 20, 5, help="Controls how many distinct values to show in the Statistics tab.")
    preview_rows = st.slider("Preview rows", 5, 100, 20, help="Controls how many rows to show in the Data Preview table.")
    st.markdown("---")
    st.caption("DataProfiler - Dataset profiling tool.\nBuilt with Python & Streamlit.")

# ——— Main —————————————————————————————————————————————————————————
_hero_cols = st.columns([0.12, 1])
with _hero_cols[0]:
    if _logo_path.exists():
        st.image(str(_logo_path), width=90)
with _hero_cols[1]:
    st.markdown("""
        <h1 class='gradient-header' style='margin-top: 0.25rem; font-size: 2.75rem !important;'>DataProfiler.</h1>
        <p style='color: #94A3B8; font-size: 1.15rem; margin-bottom: 2.5rem; font-weight: 500;'>Advanced dataset profiling &amp; automated preprocessing.</p>
    """, unsafe_allow_html=True)

if not uploaded:
    st.info("ðŸ‘ˆ Upload a CSV or Excel file from the sidebar to get started.")
    st.stop()

@st.cache_data
def load_data(file_bytes: bytes, filename: str) -> pd.DataFrame:
    ext = Path(filename).suffix.lower()
    buf = io.BytesIO(file_bytes)
    if ext == ".csv":
        return pd.read_csv(buf)
    return pd.read_excel(buf)

if "current_file" not in st.session_state or st.session_state.current_file != uploaded.name:
    st.session_state.current_file = uploaded.name
    with st.spinner("Loading dataset..."):
        st.session_state.raw_data = load_data(uploaded.read(), uploaded.name)
        st.session_state.cleaned_data = st.session_state.raw_data.copy()

# â”€â”€ Helper â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
def render_profile(df: pd.DataFrame, filename: str):
    source = DataSource(name=filename, source_type=Path(filename).suffix.lstrip("."), location=filename)
    dataset = Dataset(dataframe=df, source=source)
    config = ProfileConfig(run_statistics=run_stats, run_quality=run_quality, top_n_values=top_n, run_visualization=False)
    
    with st.spinner("Profiling dataset..."):
        profile = ProfilerEngine.profile(dataset, config=config)

    tab_overview, tab_columns, tab_stats, tab_quality, tab_export = st.tabs([
        "📋 Overview", "🗂️ Columns", "📈 Statistics", "🔍 Quality", "📥 Export"
    ])

    with tab_overview:
        c = profile.completeness
        hs = profile.health_score
        cols = st.columns(6)
        metrics = [
            ("Rows", f"{profile.rows:,}"), ("Columns", str(profile.columns)),
            ("Memory", SizeFormatter.format(profile.memory_usage)), ("Duplicates", str(profile.duplicate_rows)),
            ("Completeness", f"{c.completeness_percentage:.1f}%"), ("Missing Cells", f"{c.missing_cells:,}")
        ]
        for col_ui, (label, value) in zip(cols, metrics):
            with col_ui:
                st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div></div>', unsafe_allow_html=True)

        if hs:
            st.markdown("---")
            st.markdown("### 🏥 Health Score")
            left, right = st.columns([1, 3])
            with left:
                st.markdown(f'<div class="score-big">{hs.score}</div><span class="grade-box">Grade {hs.grade}</span>', unsafe_allow_html=True)
            with right:
                breakdown_df = pd.DataFrame([(k.replace("_", " ").title(), f"-{v}") for k, v in hs.breakdown.items() if v > 0], columns=["Deduction Reason", "Points Deducted"])
                if not breakdown_df.empty:
                    st.dataframe(breakdown_df, use_container_width=True, hide_index=True)
                else:
                    st.success("No deductions â€” perfect score!")

        st.markdown("---")
        st.markdown(f"### ðŸ“„ Data Preview (First {preview_rows} Rows)")
        st.dataframe(df.head(preview_rows), use_container_width=True)

    with tab_columns:
        st.markdown("### 🗂️ Column Summary")
        rows = []
        for i, col in enumerate(profile.column_profiles, 1):
            rows.append({
                "#": i, "Column": col.name, "Type": col.dtype, "Raw Type": col.raw_dtype,
                "Nullable": "Yes" if col.nullable else "No", "Missing": f"{col.missing_count} ({col.missing_percentage:.1f}%)",
                "Unique": f"{col.unique_count} ({col.unique_percentage:.1f}%)", "Memory": SizeFormatter.format(col.memory_usage),
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    with tab_stats:
        if not run_stats:
            st.info("Statistics are disabled. Enable them in the sidebar.")
        else:
            st.markdown("### ðŸ“ˆ Column Statistics")
            for col in profile.column_profiles:
                with st.expander(f"**{col.name}** â€” {col.dtype}"):
                    if col.numeric_stats:
                        ns = col.numeric_stats
                        d = {"Mean": ns.mean, "Median": ns.median, "Mode": ns.mode, "Std Dev": ns.std, "Variance": ns.variance, "Min": ns.minimum, "Max": ns.maximum, "Q1": ns.q1, "Q3": ns.q3, "IQR": ns.iqr, "Skewness": ns.skewness, "Kurtosis": ns.kurtosis, "Zeros": ns.zeros, "Negatives": ns.negatives}
                        c1, c2 = st.columns(2)
                        items = list(d.items())
                        half = len(items) // 2
                        with c1: st.table(pd.DataFrame(items[:half], columns=["Stat", "Value"]))
                        with c2: st.table(pd.DataFrame(items[half:], columns=["Stat", "Value"]))
                    elif col.categorical_stats:
                        cs = col.categorical_stats
                        st.metric("Distinct Values", cs.distinct_count)
                        st.metric("Most Frequent", f"{cs.most_frequent} ({cs.most_frequent_pct}%)")
                        st.metric("Least Frequent", f"{cs.least_frequent} ({cs.least_frequent_pct}%)")
                        if cs.top_values:
                            st.markdown("**Top Values**")
                            st.dataframe(pd.DataFrame(cs.top_values, columns=["Value", "Count"]), hide_index=True)
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
                    for cc in qr.constant_columns: st.error(f"x {cc}")
                else: st.success("None")
            with c2:
                st.markdown("**High Cardinality Columns**")
                if qr.high_cardinality_columns:
                    for hc in qr.high_cardinality_columns: st.warning(f"!! {hc}")
                else: st.success("None")
                st.markdown("**Outlier Columns**")
                if qr.outlier_columns:
                    for oc in qr.outlier_columns: st.warning(f"!! {oc}")
                else: st.success("None")
            if qr.mixed_type_columns:
                st.markdown("**Mixed Type Columns**")
                for col_name, types in qr.mixed_type_columns.items(): st.error(f"âœ— {col_name}: {', '.join(types)}")
            st.markdown("---")
            st.markdown("### ⚠️ Warnings")
            if qr.warnings:
                for w in qr.warnings: st.markdown(f'<div class="warning-tag">âš  {w}</div>', unsafe_allow_html=True)
            else: st.success("No warnings!")
            st.markdown("### ðŸ’¡ Recommendations")
            if qr.recommendations:
                for r in qr.recommendations: st.markdown(f'<div class="rec-tag">â†’ {r}</div>', unsafe_allow_html=True)
            else: st.success("No recommendations â€” your dataset looks clean!")

    with tab_export:
        st.markdown("### ðŸ“¥ Download Reports")
        st.markdown("#### HTML Report")
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False) as tmp: html_path = Path(tmp.name)
        HTMLExporter.export(profile, html_path)
        st.download_button("â¬‡ Download HTML Report", data=html_path.read_bytes(), file_name=f"{Path(profile.dataset_name).stem}_report.html", mime="text/html")
        st.markdown("---")
        st.markdown("#### JSON Export")
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp: json_path = Path(tmp.name)
        JSONExporter.export(profile, json_path)
        st.download_button("â¬‡ Download JSON Export", data=json_path.read_bytes(), file_name=f"{Path(profile.dataset_name).stem}_report.json", mime="application/json")
        st.markdown("---")
        st.markdown("#### Markdown Report")
        with tempfile.NamedTemporaryFile(suffix=".md", delete=False, mode="w") as tmp: md_path = Path(tmp.name)
        MarkdownExporter.export(profile, md_path)
        st.download_button("â¬‡ Download Markdown Report", data=md_path.read_bytes(), file_name=f"{Path(profile.dataset_name).stem}_report.md", mime="text/markdown")
        st.markdown("---")
        st.markdown("#### PDF Report")
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp: pdf_path = Path(tmp.name)
        PDFExporter.export(profile, pdf_path)
        st.download_button("Download PDF Report", data=pdf_path.read_bytes(), file_name=f"{Path(profile.dataset_name).stem}_report.pdf", mime="application/pdf")

# â”€â”€ Navigation â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
mode = st.radio("Select View", ["🔍 Raw Data Profiler", "🛠️ Data Preprocessing"], horizontal=True)
st.markdown("---")

if mode == "🔍 Raw Data Profiler":
    st.subheader("Raw Data Profiler")
    render_profile(st.session_state.raw_data, uploaded.name)
else:
    st.subheader("Data Preprocessing")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("### 🛠️ Preprocessing Controls")
        
        st.markdown("#### Auto-Preprocess")
        if st.button("Run Auto-Preprocess", type="primary"):
            try:
                auto_transformer = AutoPreprocessor()
                st.session_state.cleaned_data = auto_transformer.fit_transform(st.session_state.cleaned_data)
                st.success("Successfully auto-preprocessed the dataset!")
                st.rerun()
            except Exception as e:
                st.error(f"Error auto-preprocessing: {e}")

        st.markdown("---")
        st.markdown("#### ðŸ”§ Manual Preprocessing")
        col_to_modify = st.selectbox("Select Column", options=st.session_state.cleaned_data.columns)
        operation = st.selectbox("Select Operation", options=[
            "Drop Column", "Drop Rows (Missing)", "Fill Missing (Mean)", "Fill Missing (Median)", 
            "Fill Missing (Mode)", "Fill Missing (Constant)", "Convert Type",
            "Scale (Min-Max)", "Scale (Standard)", "Scale (Robust)",
            "Encode (One-Hot)", "Encode (Label)", "Cap Outliers (IQR)"
        ])
        
        param_col = st.empty()
        fill_value = None
        target_type = None
        if operation == "Fill Missing (Constant)":
            fill_value = param_col.text_input("Constant Value")
        elif operation == "Convert Type":
            target_type = param_col.selectbox("Target Type", options=["numeric", "datetime", "string"])
            
        if st.button("Apply Transformation"):
            try:
                transformer = None
                if operation == "Drop Column": transformer = ColumnDropper(columns=[col_to_modify])
                elif operation == "Drop Rows (Missing)": transformer = RowDropperNA(column=col_to_modify)
                elif operation == "Fill Missing (Mean)": transformer = SimpleImputer(column=col_to_modify, strategy='mean')
                elif operation == "Fill Missing (Median)": transformer = SimpleImputer(column=col_to_modify, strategy='median')
                elif operation == "Fill Missing (Mode)": transformer = SimpleImputer(column=col_to_modify, strategy='mode')
                elif operation == "Fill Missing (Constant)": transformer = SimpleImputer(column=col_to_modify, strategy='constant', fill_value=fill_value)
                elif operation == "Convert Type": transformer = TypeConverter(column=col_to_modify, target_type=target_type)
                elif operation == "Scale (Min-Max)": transformer = MinMaxScaler(column=col_to_modify)
                elif operation == "Scale (Standard)": transformer = StandardScaler(column=col_to_modify)
                elif operation == "Scale (Robust)": transformer = RobustScaler(column=col_to_modify)
                elif operation == "Encode (One-Hot)": transformer = OneHotEncoder(column=col_to_modify)
                elif operation == "Encode (Label)": transformer = LabelEncoder(column=col_to_modify)
                elif operation == "Cap Outliers (IQR)": transformer = OutlierCapper(column=col_to_modify)
                    
                if transformer:
                    st.session_state.cleaned_data = transformer.fit_transform(st.session_state.cleaned_data)
                    st.success(f"Successfully applied {operation} to {col_to_modify}!")
                    st.rerun()
            except Exception as e:
                st.error(f"Error applying transformation: {e}")
                
        if st.button("ðŸ”„ Reset to Raw Data"):
            st.session_state.cleaned_data = st.session_state.raw_data.copy()
            st.rerun()
            
        st.markdown("---")
        csv_data = st.session_state.cleaned_data.to_csv(index=False).encode('utf-8')
        st.download_button(label="Download Cleaned Dataset (CSV)", data=csv_data, file_name="cleaned_dataset.csv", mime="text/csv")
        
    with col2:
        st.markdown("### Cleaned Data Profile")
        render_profile(st.session_state.cleaned_data, uploaded.name)
