# SQL & Python Investigation Study Program

This portfolio documents a structured self-study program in SQL and Python, 
developed by a senior nuclear security professional and radiochemist with 20+ 
years of CBRN-E threat detection and national security experience. All projects 
are built around realistic AI misuse and CBRN-E threat detection scenarios — 
simulated AI model API logs, behavioral profiling of suspicious users, and 
automated investigation pipelines — with direct application to detecting 
AI-facilitated weapons development and threat actor activity.

The program is designed to complement deep domain expertise in radiological, 
nuclear, and chemical threat detection with the technical data analysis tools 
used in modern threat intelligence workflows.

## Program Overview

Six-month self-study program building skills in:
- Complex SQL for behavioral analysis and threat detection
- Python data pipelines for investigation automation
- Machine learning anomaly detection
- Network graph analysis
- End-to-end investigation reporting

## Key Capstone Projects

### Month 2 Capstone — End-to-End CBRN-E Detection Pipeline

A seven-step automated investigation pipeline applied to simulated AI model 
API logs. Designed to identify accounts exhibiting behavioral patterns 
consistent with CBRN-E threat actor activity, producing a prioritized 
investigation queue with supporting evidence summaries.

**Pipeline Architecture:**
1. Data ingestion via SQLAlchemy
2. Feature engineering — 5 behavioral signals
3. Rule-based detection layer
4. IsolationForest ML anomaly scoring
5. NetworkX network graph analysis
6. Composite priority ranking
7. CSV output and investigation brief

**Behavioral Scoring Schema v1.0**

Thresholds were informed by operational CBRN-E threat assessment experience 
— specifically, the behavioral patterns associated with actors conducting 
systematic reconnaissance for weapons-relevant technical information.

| Signal | Condition | Weight |
|--------|-----------|--------|
| Midnight activity ratio | >20% of queries after midnight | 20 pts |
| CBRN query percentage | >25% of queries flagged CBRN-relevant | 30 pts |
| Unknown country queries | Any queries from unrecognized countries | 20 pts |
| Response length anomaly | >1.5 std above mean (unusually detailed responses) | 15 pts |
| Network connectivity | Any shared IP with other flagged accounts | 15 pts |

### Month 1 Capstone — SQL and Python Behavioral Analysis

SQL and Python analysis of simulated AI model API logs. Produces a 
prioritized investigation queue identifying accounts flagged for high 
query volume, anomalous after-midnight activity, and rapid sequential 
querying patterns — behavioral indicators of systematic rather than 
casual AI use.

## Repository Structure

### SQL Files
| File | Description |
|------|-------------|
| `Task 1a.sql` | Month 1 capstone SQL queries |
| `capstone_queries.sql` | Month 1 investigation queries against capstone dataset |
| `month2_queries.sql` | Month 2 advanced SQL — window functions, CTEs, temporal analysis, string functions |

### Python Files
| File | Description |
|------|-------------|
| `hello.py` | Day 1 — variables, data types, f-strings |
| `day2.py` | Lists, dictionaries, loops, conditional logic |
| `day3.py` | Functions, CSV file handling, keyword detection |
| `day4.py` | pandas pipeline — risk scoring and investigation queue |
| `day5.py` | Datetime handling and matplotlib visualization |
| `day6.py` | Complete investigation pipeline — 6-step modular design |
| `day7.py` | JSON handling and nested data extraction |
| `day8.py` | Regular expressions for log parsing and IP extraction |
| `week7.py` | pandas deep dive — merge, groupby, apply, datetime features |
| `week8.py` | Excel output with openpyxl, advanced visualization, investigation dashboard |
| `precapstone.py` | SQLAlchemy, IsolationForest, and NetworkX demonstrations |
| `capstone.py` | Month 1 capstone — pandas analysis of API logs |
| `month2_capstone.py` | Month 2 capstone — end-to-end detection pipeline |

### Data Files
| File | Description |
|------|-------------|
| `capstone_logs_clean.csv` | 1,000 simulated AI model API log entries (clean UTF-8) |
| `accounts.csv` | Small account dataset for early exercises |
| `api_logs.json` | Simulated JSON API log entries with nested metadata |

### Output Files
| File | Description |
|------|-------------|
| `investigation_report.xlsx` | Formatted Excel investigation report with embedded dashboard |
| `investigation_dashboard.png` | Multi-chart investigation visualization |
| `month2_investigation_queue.csv` | Prioritized investigation queue from Month 2 capstone |

## Technologies Used
- **SQL**: SQLite, complex queries, window functions, CTEs, temporal analysis, 
  recursive CTEs
- **Python**: pandas, numpy, scikit-learn, NetworkX, SQLAlchemy, matplotlib, 
  openpyxl, json, re
- **Tools**: DB Browser for SQLite, VS Code, Git, Jupyter

## Program Status
| Month | Focus | Status |
|-------|-------|--------|
| Month 1 | SQL foundations, Python basics, behavioral analysis | Complete |
| Month 2 | Advanced SQL, end-to-end detection pipeline, ML anomaly detection | Complete |
| Month 3 | Advanced Python, API interaction, expanded ML techniques | In progress |
| Months 4–6 | Network analysis, reporting automation, advanced investigation workflows | Planned |
