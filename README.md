# SQL & Python Investigation Study Program

A structured self-study portfolio developing SQL and Python proficiency 
for AI misuse investigation and CBRN-E threat detection workflows.

## Program Overview
Six-month self-study program building skills in:
- Complex SQL for behavioral analysis and threat detection
- Python data pipelines for investigation automation
- Machine learning anomaly detection
- Network graph analysis
- End-to-end investigation reporting

## Repository Structure

### SQL Files
| File | Description |
|------|-------------|
| `Task 1a.sql` | Month 1 capstone SQL queries |
| `capstone_queries.sql` | Month 1 investigation queries against capstone dataset |
| `month2_queries.sql` | Month 2 advanced SQL -- window functions, CTEs, temporal analysis, string functions |

### Python Files
| File | Description |
|------|-------------|
| `hello.py` | Day 1 -- variables, data types, f-strings |
| `day2.py` | Lists, dictionaries, loops, conditional logic |
| `day3.py` | Functions, CSV file handling, keyword detection |
| `day4.py` | pandas pipeline -- risk scoring and investigation queue |
| `day5.py` | Datetime handling and matplotlib visualization |
| `day6.py` | Complete investigation pipeline -- 6-step modular design |
| `day7.py` | JSON handling and nested data extraction |
| `day8.py` | Regular expressions for log parsing and IP extraction |
| `week7.py` | pandas deep dive -- merge, groupby, apply, datetime features |
| `week8.py` | Excel output with openpyxl, advanced visualization, investigation dashboard |
| `precapstone.py` | SQLAlchemy, IsolationForest, and NetworkX demonstrations |
| `capstone.py` | Month 1 capstone -- pandas analysis of API logs |
| `month2_capstone.py` | Month 2 capstone -- end-to-end detection pipeline |

### Data Files
| File | Description |
|------|-------------|
| `capstone_logs_clean.csv` | 1,000 simulated API log entries (clean UTF-8) |
| `accounts.csv` | Small account dataset for early exercises |
| `api_logs.json` | Simulated JSON API log entries with nested metadata |

### Output Files
| File | Description |
|------|-------------|
| `investigation_report.xlsx` | Formatted Excel investigation report with embedded dashboard |
| `investigation_dashboard.png` | Multi-chart investigation visualization |
| `month2_investigation_queue.csv` | Prioritized investigation queue from Month 2 capstone |

## Key Capstone Projects

### Month 1 Capstone
SQL and Python analysis of simulated API logs. Queries identify 
top users by volume, after-midnight activity, and rapid query 
sequences. Python pipeline filters and flags long-response queries.

### Month 2 Capstone -- End-to-End Detection Pipeline
Seven-step automated investigation pipeline:
1. Data ingestion via SQLAlchemy
2. Feature engineering -- 5 behavioral signals
3. Rule-based detection layer
4. IsolationForest ML anomaly scoring
5. NetworkX network graph analysis
6. Composite priority ranking
7. CSV output and investigation brief

**Behavioral Scoring Schema v1.0**
- Signal 1: Midnight activity ratio (>20% = flag, 20pts)
- Signal 2: CBRN query percentage (>25% = flag, 30pts)
- Signal 3: Unknown country queries (any = flag, 20pts)
- Signal 4: Response length anomaly (>1.5 std = flag, 15pts)
- Signal 5: Network connectivity (any shared IP = flag, 15pts)

## Technologies Used
- **SQL**: SQLite, complex queries, window functions, CTEs, 
  temporal analysis, recursive CTEs
- **Python**: pandas, numpy, scikit-learn, NetworkX, 
  SQLAlchemy, matplotlib, openpyxl, json, re
- **Tools**: DB Browser for SQLite, VS Code, Git, Jupyter

## Program Status
- Month 1: Complete
- Month 2: Complete  
- Months 3-6: In progress