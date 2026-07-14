# DataProfiler Roadmap

This document outlines the planned development roadmap for DataProfiler.

The roadmap may evolve as the project grows.

---

# Version 0.1.x – Foundation ✅

## Project Setup
- [x] Repository structure
- [x] Git & GitHub setup
- [x] Virtual environment
- [x] Requirements management

## Data Readers
- [x] CSV Reader
- [x] Excel Reader
- [x] Reader Factory

## Core Architecture
- [x] Dataset model
- [x] DataSource model
- [x] DatasetProfile model
- [x] Profiler Engine

## Current Analysis
- [x] Dataset dimensions
- [x] Memory usage
- [x] Duplicate row detection
- [x] Missing value analysis
- [x] Dataset completeness
- [x] Column summary

## Reporting
- [x] Console Reporter

---

# Version 0.2 – Enhanced Profiling ✅

## Console Improvements
- [x] Dynamic table formatter
- [x] Better console formatting
- [x] Improved datatype display
- [x] Human-readable memory formatting

## Column Profiling
- [ ] Column order
- [ ] Nullability improvements
- [ ] Better schema summary

---

# Version 0.3 – Statistical Analysis ✅

## Numeric Statistics
- [x] Mean
- [x] Median
- [x] Mode
- [x] Standard Deviation
- [x] Variance
- [x] Minimum
- [x] Maximum
- [x] Quartiles

## Categorical Statistics
- [x] Most frequent values
- [x] Least frequent values
- [x] Cardinality analysis

## Datetime Statistics
- [x] Earliest date
- [x] Latest date
- [x] Date range

---

# Version 0.4 – Data Quality ✅

## Quality Checks
- [x] Primary Key Detection
- [x] Duplicate Key Detection
- [x] Constant Columns
- [x] High Cardinality Detection
- [x] Mixed Datatype Detection
- [ ] Leading/Trailing Whitespace Detection
- [ ] Invalid Values Detection

## Dataset Health
- [x] Health Score
- [x] Warnings
- [x] Recommendations

---

# Version 0.5 – Relationship Analysis

## Multi-file Profiling
- [ ] Multiple dataset support
- [ ] Relationship detection
- [ ] Candidate foreign keys
- [ ] Join suggestions
- [ ] Entity Relationship Diagram (ERD)

---

# Version 0.6 – Visualization ✅

## Charts
- [x] Missing value visualization
- [x] Histograms
- [x] Correlation Matrix
- [x] Boxplots
- [x] Distribution plots

---

# Version 0.7 – Report Export ✅

## Export Formats
- [x] HTML
- [x] Markdown
- [x] PDF
- [x] JSON

---

# Version 0.8 – Streamlit Application ✅

## Web Interface
- [x] Drag-and-drop upload
- [x] Interactive dashboard
- [x] Dataset explorer
- [ ] Visualization dashboard
- [x] Report downloads

---

# Version 0.9 – Preprocessing & AI Copilot ✅

## Data Transformation Pipeline
- [x] Cleaners (ColumnDropper, RowDropperNA, TypeConverter)
- [x] Imputers (Mean, Median, Mode, Constant imputation)
- [x] Scalers (Min-Max, Standard, Robust scaling)
- [x] Encoders (One-Hot, Label encoding)
- [x] Outliers (IQR Capper)
- [x] Automated Preprocessing Pipeline

## AI Assistant
- [x] Google Gemini AI Copilot Integration (gemini-1.5-flash)
- [x] Chat history and interactive user queries
- [x] Pre-defined quick recommendations

---

# Version 1.0 – Production Release

## Release Goals
- [x] Complete documentation (Roadmap, Changelog, README)
- [x] Unit tests (Full test suite of 41 tests passing)
- [ ] Integration tests
- [ ] GitHub Actions
- [ ] Code coverage
- [ ] Packaging
- [ ] Stable API
- [ ] Public release