# DataProfiler

A modular and extensible Python application for profiling datasets before analysis or machine learning.

DataProfiler helps data analysts, data engineers, and data scientists quickly understand the structure, quality, and characteristics of a dataset before beginning any downstream work.

> **Project Status:** 🚧 Active Development

---

# Features

## Currently Implemented

### Data Loading
- CSV file support
- Excel (.xlsx) file support
- Reader Factory for automatic file type detection
- Extensible reader architecture

### Dataset Profiling
- Dataset dimensions (rows and columns)
- Dataset memory usage
- Duplicate row detection
- Missing value analysis
- Dataset completeness analysis

### Column Profiling
- Column name
- Data type
- Nullable detection
- Missing value count
- Missing percentage
- Unique value count
- Unique percentage
- Memory usage per column

### Architecture
- Modular project structure
- Domain-driven models (`Dataset`, `DataSource`, `DatasetProfile`)
- Profiling engine
- Console reporting
- Logging support

---

# Example Output

```text
============================================================
                       DATA PROFILER
============================================================

Dataset        : sample.csv
Rows           : 5
Columns        : 3
Memory Usage   : 520 B
Duplicate Rows : 0

DATASET HEALTH
------------------------------------------------------------
Total Cells    : 15
Filled Cells   : 15
Missing Cells  : 0
Completeness   : 100.00%

COLUMN SUMMARY
------------------------------------------------------------
Column              Type        Nullable    Missing    Unique    Memory
------------------------------------------------------------
id                  int64       No          0          5         172 B
name                string      No          0          5         440 B
age                 int64       No          0          5         172 B
```

---

# Project Structure

```
DataProfiler/
│
├── app/
│
├── profiler/
│   ├── analyzers/
│   ├── engine/
│   ├── models/
│   ├── readers/
│   ├── report/
│   ├── utils/
│   ├── config/
│   └── exceptions/
│
├── examples/
├── tests/
├── docs/
├── reports/
├── assets/
│
├── requirements.txt
├── pyproject.toml
├── README.md
└── LICENSE
```

---

# Current Architecture

```
Reader
   │
   ▼
Dataset
 ├── DataFrame
 └── DataSource
        │
        ▼
Profiler Engine
        │
        ▼
Dataset Profile
        │
        ▼
Console Reporter
```

---

# Technology Stack

- Python
- Pandas
- OpenPyXL
- Logging
- Dataclasses
- Git
- GitHub

---

# Roadmap

## Version 0.2

- Improved console tables
- Table formatter
- Better datatype detection
- Human-readable reports

## Version 0.3

Statistics Module

- Mean
- Median
- Standard Deviation
- Variance
- Quartiles
- Distribution Analysis

## Version 0.4

Data Quality Module

- Primary Key Detection
- Duplicate Key Detection
- Constant Columns
- Mixed Datatype Detection
- High Cardinality Detection
- Outlier Detection

## Version 0.5

Relationship Detection

- Candidate Foreign Keys
- Relationship Detection
- Entity Relationship Diagram

## Version 0.6

Visualization

- Missing Value Charts
- Histograms
- Correlation Matrix
- Distribution Plots

## Version 0.7

Exporters

- HTML Reports
- Markdown Reports
- PDF Reports
- JSON Export

## Version 0.8

Streamlit Application

- Drag-and-drop upload
- Interactive dashboard
- Report download
- Visualization interface

## Version 1.0

Production Release

- Documentation
- Unit Tests
- CI/CD
- Performance Improvements
- Package Release

---

# Design Principles

DataProfiler follows a modular architecture.

- Readers load datasets.
- The Profiling Engine coordinates analysis.
- Analyzers inspect specific aspects of the dataset.
- Models store profiling results.
- Reporters generate output.

This separation keeps the project maintainable and makes it easy to add new data sources, analyzers, and reporting formats.

---

# Contributing

Contributions, suggestions, and feature requests are welcome.

Future contribution guidelines will be added as the project matures.

---

# License

This project is licensed under the MIT License.