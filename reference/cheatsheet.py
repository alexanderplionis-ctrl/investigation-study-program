# =============================================================
# INVESTIGATION STUDY PROGRAM -- REFERENCE CHEATSHEET
# Covers: SQL patterns, Python, pandas, ML, NetworkX
# Last updated: Month 2 complete
# =============================================================

# ── IMPORTS ──────────────────────────────────────────────────
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import networkx as nx
import json
import re
import csv

# =============================================================
# SECTION 1: SQL REFERENCE
# =============================================================

# ── CLAUSE ORDER (mnemonic: Silly Frogs Wear Green Hats Outdoors)
# SELECT, FROM, WHERE, GROUP BY, HAVING, ORDER BY

# ── AGGREGATE FUNCTIONS ──────────────────────────────────────
# COUNT(*)                    -- count all rows
# COUNT(col)                  -- count non-null values
# COUNT(DISTINCT col)         -- count unique values
# SUM(col)                    -- sum of values
# AVG(col)                    -- average of values
# MAX(col)                    -- highest value
# MIN(col)                    -- lowest value
# ROUND(AVG(col), 1)          -- rounded to 1 decimal place
#
# AVG vs MAX -- know which one the question asks for:
# AVG(col) -- average across all rows in group
# MAX(col) -- single highest value in group
# Both can be used in HAVING and aliased in ORDER BY

# ── GROUP BY PATTERN ─────────────────────────────────────────
# SELECT col, COUNT(*) AS total
# FROM table
# GROUP BY col
# HAVING total > 100          -- filter on aggregated value
# ORDER BY total DESC

# ── WINDOW FUNCTIONS ─────────────────────────────────────────
# ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY timestamp DESC) AS rn
# RANK()       OVER (PARTITION BY user_id ORDER BY score DESC) AS rnk
# LAG(col)     OVER (PARTITION BY user_id ORDER BY timestamp) AS prev_val
# LEAD(col)    OVER (PARTITION BY user_id ORDER BY timestamp) AS next_val
# AVG(col)     OVER (PARTITION BY user_id) AS user_avg
#
# ORDER BY col DESC inside OVER --> rn=1 is HIGHEST value
# ORDER BY col ASC  inside OVER --> rn=1 is LOWEST value

# ── GET ONE ROW PER GROUP ────────────────────────────────────
# (most recent, highest, lowest -- use ROW_NUMBER)
#
# WITH ranked AS (
#     SELECT *, ROW_NUMBER() OVER (PARTITION BY user_id
#                                  ORDER BY timestamp DESC) AS rn
#     FROM table
# )
# SELECT * FROM ranked WHERE rn = 1;
#
# WHERE and ORDER BY always go in the OUTER SELECT, never inside CTE

# ── CTE PATTERNS ─────────────────────────────────────────────
# Single CTE:
# WITH cte_name AS (
#     SELECT ...
# )
# SELECT * FROM cte_name;
#
# Chained CTEs:
# WITH
# step1 AS (SELECT ...),
# step2 AS (SELECT ... FROM step1)
# SELECT * FROM step2;
#
# Recursive CTE:
# WITH RECURSIVE cte AS (
#     SELECT ...           -- anchor query (runs once)
#     UNION ALL
#     SELECT ... FROM cte  -- recursive step
#     WHERE depth < 5      -- stopping condition
# )

# ── DATETIME WITH STRFTIME (SQLite) ──────────────────────────
# STRFTIME('%H', timestamp)        -- hour as '00' to '23'
# STRFTIME('%Y-%m-%d', timestamp)  -- date as '2024-03-30'
# STRFTIME('%w', timestamp)        -- day of week 0=Sunday 6=Saturday
# STRFTIME('%m', timestamp)        -- month as '01' to '12'
#
# Nighttime filter (midnight to 3am):
# WHERE STRFTIME('%H', timestamp) BETWEEN '00' AND '03'
#
# Count distinct active days per user:
# COUNT(DISTINCT STRFTIME('%Y-%m-%d', timestamp)) AS active_days
#
# Count midnight queries per user:
# SUM(CASE WHEN STRFTIME('%H', timestamp) BETWEEN '00' AND '03'
#          THEN 1 ELSE 0 END) AS midnight_queries

# ── CASE WHEN PATTERNS ───────────────────────────────────────
# Simple classification:
# CASE WHEN col = 'value' THEN 'label'
#      WHEN col > 100     THEN 'high'
#      ELSE 'other'
# END AS category
#
# Conditional count (pivot table pattern):
# SUM(CASE WHEN category = 'Chemical' THEN 1 ELSE 0 END) AS chemical

# ── PIVOT TABLE PATTERN ──────────────────────────────────────
# SELECT user_id,
#        SUM(CASE WHEN cat = 'Chemical'   THEN 1 ELSE 0 END) AS chemical,
#        SUM(CASE WHEN cat = 'Biological' THEN 1 ELSE 0 END) AS biological,
#        COUNT(*) AS total
# FROM classified
# GROUP BY user_id
# ORDER BY (chemical + biological) DESC;

# ── JOIN PATTERNS ────────────────────────────────────────────
# INNER JOIN -- only matching rows:
# SELECT * FROM a JOIN b ON a.id = b.id

# LEFT JOIN -- all rows from left table:
# SELECT * FROM a LEFT JOIN b ON a.id = b.id

# Self join -- compare rows within same table:
# SELECT a.user_id, b.user_id
# FROM table a JOIN table b ON a.ip = b.ip
# WHERE a.user_id != b.user_id

# Basic JOIN with table aliases (cleaner syntax):
# SELECT c.col, p.col
# FROM table1 c JOIN table2 p ON c.id = p.id
# GROUP BY c.user_id
# ORDER BY total DESC;

# JOIN with aggregation and filtering:
# SELECT c.user_id,
#        COUNT(*) AS total,
#        SUM(CASE WHEN c.col = 'val' THEN 1 ELSE 0 END) AS count_val,
#        p.account_age_days
# FROM logs c
# JOIN profiles p ON c.user_id = p.user_id
# WHERE p.account_type = 'free'       -- filter on profile column
# GROUP BY c.user_id
# HAVING total > 100                  -- filter on aggregated value
# AND count_val >= 1                  -- multiple HAVING conditions
# ORDER BY total DESC;
#
# KEY RULES FOR JOINS:
# -- Use table aliases (c, p) to avoid ambiguous column names
# -- WHERE filters profile/lookup columns before grouping
# -- HAVING filters aggregated values after grouping
# -- Columns from joined table (p.*) don't need aggregating
# -- COUNT and SUM come from the main log table (c.*)

# ── SUBQUERY PATTERNS ────────────────────────────────────────
# Filter using subquery result:
# WHERE col IN (SELECT col FROM table WHERE condition)
#
# Get row matching max value per group:
# WHERE (user_id, timestamp) IN (
#     SELECT user_id, MAX(timestamp)
#     FROM table GROUP BY user_id
# )

# ── STRING FUNCTIONS ─────────────────────────────────────────
# LOWER(col)                    -- convert to lowercase
# LENGTH(col)                   -- character count
# INSTR(LOWER(col), 'keyword')  -- find position, 0 if not found
# SUBSTR(col, start, length)    -- extract substring
# REPLACE(col, 'old', 'new')    -- replace text
#
# CBRN keyword detection:
# INSTR(LOWER(query_text), 'synthesize') > 0

# ── TEMPORAL SQL ─────────────────────────────────────────────
# Time between consecutive queries in seconds:
# ROUND((JULIANDAY(timestamp) -
#        JULIANDAY(LAG(timestamp) OVER (PARTITION BY user_id
#                                       ORDER BY timestamp))) * 86400, 0)
#        AS seconds_since_last

# ── PERFORMANCE ──────────────────────────────────────────────
# Create index for faster queries on large tables:
# CREATE INDEX IF NOT EXISTS idx_country ON table(country);
#
# Check query execution plan:
# EXPLAIN QUERY PLAN SELECT ...;
# SCAN = slow (reads every row)
# SEARCH USING INDEX = fast (jumps to matching rows)

# =============================================================
# SECTION 2: SQLALCHEMY DATABASE CONNECTION
# =============================================================

engine = create_engine("sqlite:///database.db")

# Run SQL query and return DataFrame
df = pd.read_sql("SELECT * FROM table", engine)

# Parameterized query -- safe, prevents SQL injection
df = pd.read_sql(
    "SELECT * FROM logs WHERE user_id = :uid",
    engine,
    params={"uid": "USR_001"}
)

# =============================================================
# SECTION 3: PANDAS
# =============================================================

# ── LOADING DATA ─────────────────────────────────────────────
df = pd.read_csv("file.csv")
df = pd.read_csv("file.csv", encoding="latin-1")  # if UTF-8 fails

# Display settings
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

# ── BASIC EXPLORATION (always do these first) ────────────────
df.shape                    # (rows, columns)
df.columns.tolist()         # list of column names
df.head()                   # first 5 rows
df.dtypes                   # data types per column
df.describe()               # statistics for numeric columns
df.isnull().sum()           # count missing values per column
df["col"].nunique()         # count unique values
df["col"].value_counts()    # count occurrences of each value

# ── FILTERING ────────────────────────────────────────────────
df[df["column"] > value]
df[df["column"] == "text"]
df[df["column"].isna()]                          # find NULL/NaN rows
df[df["column"].notna()]                         # find non-NULL rows
df[(df["col1"] > val1) & (df["col2"] == val2)]  # AND
df[(df["col1"] > val1) | (df["col2"] == val2)]  # OR
df[df["col"].isin(["val1", "val2"])]             # equivalent to SQL IN
df[df["col"].between(low, high)]                 # equivalent to BETWEEN
df[df["col"].str.contains("keyword", case=False)] # string search

# ── COLUMN OPERATIONS ────────────────────────────────────────
df["new_col"] = df["col1"] / df["col2"]          # calculated column
df["col"] = df["col"].round(2)                    # round
df["col"] = df["col"].astype(int)                 # type conversion
df["col"] = df["col"].fillna(0)                   # fill NaN with 0
df["col"] = df["col"].replace("old", "new")       # replace values

# Conditional column -- equivalent to SQL CASE WHEN
df["tier"] = np.where(df["score"] > 6, "High", "Low")

# Multi-condition with lambda
df["tier"] = df["score"].apply(
    lambda x: "Critical" if x > 9 else "High" if x > 6 else "Low"
)

# Apply custom function to column
def classify(text):
    if "synthesize" in text.lower():
        return "Chemical"
    return "Benign"

df["category"] = df["query_text"].apply(classify)

# ── SORTING AND RANKING ──────────────────────────────────────
df.sort_values("column", ascending=False)
df.sort_values(["col1", "col2"], ascending=[False, True])
df.reset_index(drop=True)                         # reset after sorting

# ── GROUPBY AND AGGREGATION ──────────────────────────────────
df.groupby("column").mean()
df.groupby("column").agg({"col1": "sum", "col2": "mean"})

# Named aggregations
result = df.groupby("user_id").agg(
    total_queries=("user_id", "count"),
    avg_response=("response_length", "mean"),
    unique_ips=("ip_address", "nunique"),
    cbrn_count=("is_cbrn", "sum"),
    unknown_country=("country", lambda x: (x == "Unknown").sum())
).reset_index()

# ── MERGE (equivalent to SQL JOIN) ───────────────────────────
merged = df1.merge(df2, on="user_id", how="inner")   # inner join
merged = df1.merge(df2, on="user_id", how="left")    # left join
merged = df1.merge(df2, left_on="user_id", right_on="id")  # different col names

# ── DATETIME ─────────────────────────────────────────────────
now = datetime.now()
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["hour"] = df["timestamp"].dt.hour
df["day_of_week"] = df["timestamp"].dt.dayofweek   # 0=Monday
df["day_name"] = df["timestamp"].dt.day_name()
df["month"] = df["timestamp"].dt.month
df["date"] = df["timestamp"].dt.date
df["is_nighttime"] = df["hour"].between(0, 4)
df["is_weekend"] = df["day_of_week"].isin([5, 6])
one_week_ago = now - timedelta(days=7)
now.strftime("%Y-%m-%d %H:%M")                     # format as string

# ── OUTPUT ───────────────────────────────────────────────────
df.to_csv("output.csv", index=False)

with pd.ExcelWriter("report.xlsx", engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="Data", index=False)
    df2.to_excel(writer, sheet_name="Summary", index=False)

# =============================================================
# SECTION 4: MATPLOTLIB VISUALIZATION
# =============================================================

# Basic bar chart
plt.figure(figsize=(10, 6))
plt.bar(df["x_col"], df["y_col"], color="steelblue")
plt.title("Title")
plt.xlabel("X Label")
plt.ylabel("Y Label")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("chart.png", dpi=150)
plt.show()

plt.barh(df["user_id"], df["score"])               # horizontal bar
plt.axhline(y=6.0, color="orange", linestyle="--", label="Threshold")
plt.legend()
plt.scatter(df["x"], df["y"], c=colors, s=100)     # scatter plot
plt.close()                                         # close without showing

# Color coded bars
colors = ["red" if v > 6 else "steelblue" for v in df["score"]]
plt.bar(df["user_id"], df["score"], color=colors)

# Multiple subplots
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes[0, 0].bar(...)     # top left
axes[0, 1].bar(...)     # top right
axes[1, 0].scatter(...) # bottom left
axes[1, 1].pie(...)     # bottom right
plt.tight_layout()

# =============================================================
# SECTION 5: JSON AND REGEX
# =============================================================

# ── JSON ─────────────────────────────────────────────────────
with open("logs.json", "r") as f:
    data = json.load(f)

ip = data[0]["metadata"]["ip_address"]             # nested field access

records = []
for item in data:
    records.append({
        "user_id": item["user_id"],
        "ip_address": item["metadata"]["ip_address"],
        "country": item["metadata"]["country"]
    })
df = pd.DataFrame(records)

# ── REGULAR EXPRESSIONS ──────────────────────────────────────
match = re.search(r"\d+", text)                    # first match
all_numbers = re.findall(r"\d+", text)             # all matches

ip_pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
ts_pattern = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"
user_pattern = r"USR_\d{3}"

pattern = r"(?P<timestamp>\d{4}-\d{2}-\d{2}) (?P<user>USR_\d{3})"
match = re.search(pattern, log_line)
if match:
    ts = match.group("timestamp")
    user = match.group("user")

redacted = re.sub(ip_pattern, "[REDACTED IP]", text)  # replace/redact

# =============================================================
# SECTION 6: MACHINE LEARNING -- ISOLATION FOREST
# =============================================================

features = df[["col1", "col2", "col3"]].copy()
scaler = StandardScaler()
scaled = scaler.fit_transform(features)

# contamination = expected % of anomalies
model = IsolationForest(contamination=0.2, random_state=42)
predictions = model.fit_predict(scaled)            # 1=normal, -1=anomaly

raw_scores = model.decision_function(scaled)
anomaly_scores = 100 - (
    (raw_scores - raw_scores.min()) /
    (raw_scores.max() - raw_scores.min()) * 100
)

df["anomaly_flag"] = np.where(predictions == -1, 1, 0)
df["anomaly_score"] = anomaly_scores.round(1)

# =============================================================
# SECTION 7: NETWORKX GRAPH ANALYSIS
# =============================================================

G = nx.Graph()
G.add_edge("USR_001", "USR_003")

# Build from shared IP data
for ip in ip_data["ip_address"].unique():
    users = ip_data[ip_data["ip_address"] == ip]["user_id"].tolist()
    for i in range(len(users)):
        for j in range(i + 1, len(users)):
            G.add_edge(users[i], users[j])

G.number_of_nodes()
G.number_of_edges()

components = list(nx.connected_components(G))
large_clusters = [c for c in components if len(c) > 2]
degrees = sorted(G.degree(), key=lambda x: x[1], reverse=True)

component_map = {}
for component in components:
    for user in component:
        component_map[user] = len(component)
df["cluster_size"] = df["user_id"].map(component_map).fillna(1)

# =============================================================
# SECTION 8: CBRN INVESTIGATION PATTERNS
# =============================================================

# ── CBRN KEYWORD CLASSIFICATION ──────────────────────────────
def classify_query(query_text):
    text = query_text.lower()
    if any(w in text for w in ["synthesize", "compound", "stabilize"]):
        return "Chemical"
    elif any(w in text for w in ["pathogen", "transmission"]):
        return "Biological"
    elif any(w in text for w in ["nuclear", "fission"]):
        return "Radiological"
    elif any(w in text for w in ["dispersal", "precursor"]):
        return "Explosive"
    else:
        return "Benign"

df["cbrn_category"] = df["query_text"].apply(classify_query)
df["is_cbrn"] = df["cbrn_category"] != "Benign"
cbrn_pct = df["is_cbrn"].mean() * 100

# ── BEHAVIORAL SCORING SCHEMA v1.0 ───────────────────────────
# Signal 1: Midnight activity ratio  >20%       flag = 20pts
# Signal 2: CBRN query percentage    >25%       flag = 30pts
# Signal 3: Unknown country queries  any        flag = 20pts
# Signal 4: Response length anomaly  >1.5 std   flag = 15pts
# Signal 5: Network connectivity     any shared IP flag = 15pts

# Rule-based scoring pattern
df["rule_score"] = 0
df["flags"] = ""

mask = df["midnight_ratio"] > 0.20
df.loc[mask, "rule_score"] += 20
df.loc[mask, "flags"] += "MIDNIGHT_ACTIVITY | "

# Z-score for anomaly threshold
pop_mean = df["avg_response"].mean()
pop_std = df["avg_response"].std()
df["response_zscore"] = ((df["avg_response"] - pop_mean) / pop_std).round(3)

# =============================================================
# SECTION 9: GIT COMMANDS
# =============================================================

# git init                    -- initialize repository
# git add .                   -- stage all changes
# git add filename.py         -- stage specific file
# git commit -m "message"     -- save snapshot
# git push                    -- push to GitHub
# git pull origin main        -- sync from GitHub
# git status                  -- see current state
# git log --oneline           -- see commit history
# git rm --cached file.py     -- untrack a file