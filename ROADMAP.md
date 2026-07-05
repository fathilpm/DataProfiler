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

# Version 0.2 – Enhanced Profiling

## Console Improvements
- [ ] Dynamic table formatter
- [ ] Better console formatting
- [ ] Improved datatype display
- [ ] Human-readable memory formatting

## Column Profiling
- [ ] Column order
- [ ] Nullability improvements
- [ ] Better schema summary

---

# Version 0.3 – Statistical Analysis

## Numeric Statistics
- [ ] Mean
- [ ] Median
- [ ] Mode
- [ ] Standard Deviation
- [ ] Variance
- [ ] Minimum
- [ ] Maximum
- [ ] Quartiles

## Categorical Statistics
- [ ] Most frequent values
- [ ] Least frequent values
- [ ] Cardinality analysis

## Datetime Statistics
- [ ] Earliest date
- [ ] Latest date
- [ ] Date range

---

# Version 0.4 – Data Quality

## Quality Checks
- [ ] Primary Key Detection
- [ ] Duplicate Key Detection
- [ ] Constant Columns
- [ ] High Cardinality Detection
- [ ] Mixed Datatype Detection
- [ ] Leading/Trailing Whitespace Detection
- [ ] Invalid Values Detection

## Dataset Health
- [ ] Health Score
- [ ] Warnings
- [ ] Recommendations

---

# Version 0.5 – Relationship Analysis

## Multi-file Profiling
- [ ] Multiple dataset support
- [ ] Relationship detection
- [ ] Candidate foreign keys
- [ ] Join suggestions
- [ ] Entity Relationship Diagram (ERD)

---

# Version 0.6 – Visualization

## Charts
- [ ] Missing value visualization
- [ ] Histograms
- [ ] Correlation Matrix
- [ ] Boxplots
- [ ] Distribution plots

---

# Version 0.7 – Report Export

## Export Formats
- [ ] HTML
- [ ] Markdown
- [ ] PDF
- [ ] JSON

---

# Version 0.8 – Streamlit Application

## Web Interface
- [ ] Drag-and-drop upload
- [ ] Interactive dashboard
- [ ] Dataset explorer
- [ ] Visualization dashboard
- [ ] Report downloads

---

# Version 0.9 – Performance

## Optimization
- [ ] Chunk processing
- [ ] Large file support
- [ ] Parallel execution
- [ ] Performance benchmarking

---

# Version 1.0 – Production Release

## Release Goals

- [ ] Complete documentation
- [ ] Unit tests
- [ ] Integration tests
- [ ] GitHub Actions
- [ ] Code coverage
- [ ] Packaging
- [ ] Stable API
- [ ] Public release