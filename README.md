# 📊 DataScope+ — Interactive Data Analyzer & Cleaner

**DataScope+** is an end-to-end interactive data exploration, cleaning, and visualization tool built with **Streamlit** and the Python data stack.
It enables analysts, data scientists, and researchers to upload raw datasets and quickly derive structure, quality insights, and visual understanding — without writing a single line of analysis code.

This project emphasizes **practical EDA**, **data quality inspection**, and **responsible visualization choices**, mirroring real-world analytical workflows used in industry.

---

## [Click to live WebApp](https://datascope-plus.streamlit.app)


---

### TL;DR (for the lazy)
**DataScope+** is a practical, analyst-focused data exploration and cleaning tool that reflects real-world workflows and sound statistical judgment.

## Note: Remember to be kind, i am still a novice but learning and some things may break or all of them. Just raise the issues. My contact info is on Bio


---

## Problem Statement

In real world data work, datasets are:

* messy
* incomplete
* inconsistent
* poorly documented

Most beginner and even intermediate analysts struggle not with modeling, but with:

* understanding dataset structure
* identifying missing values and duplicates
* detecting outliers
* choosing appropriate visualizations
* performing basic yet correct data cleaning

**DataScope+** addresses this gap by providing an **interactive, opinionated EDA tool** that enforces good analytical habits while remaining flexible.

---

## Core Objectives

* Rapid dataset inspection
* Transparent data quality diagnostics
* Controlled data cleaning strategies
* Visualization with guardrails
* Exportable cleaned data and charts
* Analyst-friendly UX with technical depth under the hood

---

## Supported File Types

Users can upload datasets in the following formats:

* **CSV** (`.csv`)
* **Excel** (`.xlsx`, `.xls`)

  * Sheet selection supported
* **Stata** (`.dta`)

---

## Features

### Dataset Preview

* View top and bottom rows immediately after upload
* Validate data integrity before analysis

### Dataset Summary & Insights

* Shape (rows × columns)
* Column data types
* Missing value counts
* Duplicate row detection
* Descriptive statistics for numerical columns

### Outlier Detection

* IQR-based outlier identification
* Column-wise reporting for numeric features

### Data Cleaning Engine

User-controlled missing value handling:

* **Auto**: statistical imputation
* **Zero**: numeric zero fill
* **Drop**: row removal

Cleaning is:

* non-destructive
* reversible
* previewable before export

### Visualization Suite

#### Seaborn (Static, Analytical)

* Line plots
* Bar plots
* Scatter plots
* Box plots
* Histograms
* Correlation heatmaps
* Pie charts

#### Plotly (Interactive)

* Scatter plots
* Line plots
* Bar plots
* Histograms
* Box plots
* Pie charts

The UI intentionally warns users when a chosen visualization is statistically inappropriate for the selected data.

### Export Capabilities

* Download cleaned dataset as CSV
* Download generated charts as PNG

---

## Project Walkthrough

1. Upload a dataset
2. Inspect previews and structure
3. Examine missing values, duplicates, and statistics
4. Review outlier reports
5. Choose a cleaning strategy
6. Preview cleaned data
7. Select columns for analysis
8. Generate appropriate visualizations
9. Export results

This mirrors a **professional EDA workflow** used in analytics teams.

---

## Tools & Technologies

* **Python 3.10+**
* **Streamlit**
* **Pandas**
* **NumPy**
* **Seaborn**
* **Matplotlib**
* **Plotly**
* **Apache Arrow (via Streamlit)**

---

## Known Warnings & Design Decisions

* Apache Arrow warnings may occur when rendering metadata objects (e.g., raw `dtype` objects).
  These are handled safely and do **not** affect correctness or deployment.
* Visualization warnings are intentional UX features, not errors.
* This tool prioritizes **EDA correctness** over “pretty but misleading” plots.

---

## Why This Project Matters for me

This project demonstrates:

* Understanding of real world data problems
* Strong EDA fundamentals
* UI/UX decisions grounded in statistics
* Safe data handling practices
* Ability to build production ready analytical tools
* Familiarity with modern Python data ecosystems

It reflects how analysts actually work not just how tutorials pretend they do. and working on the project was the most learning and blissful experience i have ever had.

---

## Potential Future Improvements

* Dataset profiling reports (Sweetviz / ydata-profiling integration)
* Automated feature type inference
* Advanced outlier diagnostics
* Caching for large datasets
* Multi-dataset comparison
* Role based UI (analyst vs stakeholder)
* Export to Parquet
* Lightweight ML diagnostics (optional), especially for feature importances

---

## Contribution & Issues

This project is actively evolving.

If you:

* encounter a bug
* observe incorrect behavior
* have a feature suggestion
* want to improve performance or UX

👉 **Please open an issue on GitHub** so it can be tracked and addressed properly.

---


## License

MIT License — free to use, modify, and build upon.

---


