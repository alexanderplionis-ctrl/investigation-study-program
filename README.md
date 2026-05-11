# SQL & Python Investigation Study Program

CBRN-E behavioral detection portfolio applied to simulated API log data, with relevance to AI misuse investigation workflows.

## Capstone Artifact: End-to-End Behavioral Detection Pipeline

The Month 2 capstone (`month2_capstone.py`) is a seven-step automated investigation pipeline that ingests simulated API logs, computes behavioral risk signals, scores activity using rule-based logic and machine learning anomaly detection, performs network graph analysis, and produces a prioritized investigation queue.

**Pipeline steps:**

1. Data ingestion via SQLAlchemy
2. Feature engineering across five behavioral signals
3. Rule-based detection layer
4. IsolationForest ML anomaly scoring
5. NetworkX network graph analysis
6. Composite priority ranking
7. CSV output and investigation brief

### Behavioral Scoring Schema v1.0

The pipeline computes five behavioral risk signals against simulated API log entries. Each signal carries a weighted point value contributing to a composite priority score:

| Signal | Trigger Condition | Points |
| --- | --- | --- |
| Midnight activity ratio | >20% of activity during off-hours | 20 |
| CBRN query percentage | >25% of queries flagged as CBRN-related | 30 |
| Unknown country queries | Any presence of unattributable origin | 20 |
| Response length anomaly | >1.5 standard deviations from baseline | 15 |
| Network connectivity | Any shared IP across accounts | 15 |

The composite score drives prioritization in the investigation queue output.

## About This Portfolio

This repository documents a structured six-month self-study program building applied SQL and Python skills for CBRN-E behavioral detection and investigative data analysis. The program was developed to complement two decades of operational CBRN-E threat investigation experience with hands-on technical tooling for AI-era threat detection workflows. Months 1 and 2 are complete with capstone projects delivered; Months 3–6 are in progress.

For broader professional context: scholar.google.com/citations?user=I5Q1SqwAAAAJ

## Program Status

* Month 1: Complete (capstone delivered)
* Month 2: Complete (capstone delivered)
* Months 3–6: In progress

## Repository Structure

### SQL

| File | Description |
| --- | --- |
| `Task 1a.sql` | Month 1 capstone SQL queries |
| `capstone_queries.sql` | Month 1 investigation queries against capstone dataset |
| `month2_queries.sql` | Month 2 advanced SQL: window functions, CTEs, temporal analysis, string functions |

### Python

| File | Description |
| --- | --- |
| `month2_capstone.py` | **Month 2 capstone**: end-to-end detection pipeline |
| `capstone.py` | Month 1 capstone: pandas analysis of API logs |
| `precapstone.py` | SQLAlchemy, IsolationForest, and NetworkX foundational exercises |
| `week8.py` | Excel output with openpyxl, advanced visualization, investigation dashboard |
| `week7.py` | pandas deep dive: merge, groupby, apply, datetime features |
| `day8.py` | Regular expressions for log parsing and IP extraction |
| `day7.py` | JSON handling and nested data extraction |
| `day6.py` | Modular investigation pipeline (six-step design) |
| `day5.py` | Datetime handling and matplotlib visualization |
| `day4.py` | pandas pipeline: risk scoring and investigation queue |
| `day3.py` | Functions, CSV file handling, keyword detection |
| `day2.py` | Lists, dictionaries, loops, conditional logic |
| `hello.py` | Day 1: variables, data types, f-strings |

### Data

| File | Description |
| --- | --- |
| `capstone_logs_clean.csv` | 1,000 simulated API log entries (clean UTF-8) |
| `accounts.csv` | Small account dataset for early exercises |
| `api_logs.json` | Simulated JSON API log entries with nested metadata |

### Outputs

| File | Description |
| --- | --- |
| `investigation_report.xlsx` | Formatted Excel investigation report with embedded dashboard |
| `investigation_dashboard.png` | Multi-chart investigation visualization |
| `month2_investigation_queue.csv` | Prioritized investigation queue from Month 2 capstone |

## Technologies

**SQL**: SQLite, complex queries, window functions, CTEs, temporal analysis, recursive CTEs

**Python**: pandas, numpy, scikit-learn, NetworkX, SQLAlchemy, matplotlib, openpyxl, json, re

**Tools**: DB Browser for SQLite, VS Code, Git, Jupyter

## Notes

This is a working-knowledge portfolio built on simulated data. It is not production code, and the simulated log datasets (1,000 rows) are several orders of magnitude smaller than what production threat investigation systems work with. The intent is to demonstrate applied investigative reasoning and the construction of end-to-end detection pipelines using techniques relevant to behavioral threat detection workflows.
