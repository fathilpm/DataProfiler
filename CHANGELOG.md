# Changelog

All notable changes to this project will be documented in this file.

The format follows Keep a Changelog principles.

---

# [0.1.1] - In Development

## Added

### Core Architecture

- Dataset domain model
- DataSource domain model
- DatasetProfile model
- ColumnProfile model
- Profiler Engine

### Readers

- CSV Reader
- Excel Reader
- Reader Factory

### Analysis

- Dataset dimensions
- Duplicate row detection
- Memory usage analysis
- Missing value analysis
- Dataset completeness analysis
- Column profiling

### Reporting

- Console Reporter
- Human-readable memory formatter

---

## Changed

- Refactored architecture to use Dataset instead of raw DataFrame
- Separated reporting from profiling engine
- Improved modular project structure

---

## Removed

- Sample value display from column summary
- Dataset preview from console output

---

# [0.1.0] - Initial Release

## Added

- Initial repository structure
- Python project setup
- Logging
- CSV support
- Excel support
- Initial profiler engine