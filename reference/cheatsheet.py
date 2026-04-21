# =============================================================
# INVESTIGATION STUDY PROGRAM -- REFERENCE CHEATSHEET
# Covers: SQL patterns, Python, pandas, ML, NetworkX
# =============================================================

# ---- IMPORTS ------------------------------------------------
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

# ---- SQLALCHEMY DATABASE CONNECTION -------------------------
engine = create_engine("sqlite:///database.db")

# Run SQL query and return DataFrame
df = pd.read_sql("SELECT * FROM table", engine)

# Parameterized query -- safe, prevents SQL injection
df = pd.read_sql(
    "SELECT * FROM logs WHERE user_id = :uid",
    engine,
    params={"uid": "USR_001"}
)

# ---- PANDAS BASICS ------------------------------------------

# Load data
df = pd.read_csv("file.csv")
df = pd.read_csv("file.csv", encoding="latin-1")  # if UTF-8 fails

# Basic exploration -- always do these first
df.shape                    # (rows, columns)
df.columns.tolist()         # list of column names
df.head()                   # first 5 rows
df.dtypes                   # data types per column
df.describe()               # statistics for numeric columns
df.isnull().sum()           # count missing values per column
df["col"].nunique()         # count unique values
df["col"].value_counts()    # count occurrences of each value

# Display settings
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

# ---- PANDAS FILTERING ---------------------------------------

# Single condition
df[df["column"] > value]
df[df["column"] == "text"]
df[df["column"].isna()]         # find NULL/NaN rows
df[df["column"].notna()]        # find non-NULL rows

# Multiple conditions -- use & for AND, | for OR
df[(df["col1"] > val1) & (df["col2"] == val2)]
df[(df["col1"] > val1) | (df["col2"] == val2)]

# List membership -- equivalent to SQL IN
df[df["col"].isin(["val1", "val2", "val3"])]

# Range -- equivalent to SQL BETWEEN
df[df["col"].between(low, high)]

# String contains
df[df["col"].str.contains("keyword", case=False)]

# ---- PANDAS COLUMN OPERATIONS -------------------------------

# Add calculated column
df["new_col"] = df["col1"] / df["col2"]

# Conditional column -- equivalent to SQL CASE WHEN
df["tier"] = np.where(df["score"] > 6, "High", "Low")

# Multi-condition with apply and lambda
df["tier"] = df["score"].apply(
    lambda x: "Critical" if x > 9 else "High" if x > 6 else "Low"
)

# Apply a custom function to a column
def classify(text):
    if "synthesize" in text.lower():
        return "Chemical"
    return "Benign"

df["category"] = df["query_text"].apply(classify)

# Round numeric column
df["col"] = df["col"].round(2)

# Type conversion
df["col"] = df["col"].astype(int)
df["col"] = df["col"].astype(str)

# Replace values
df["col"] = df["col"].fillna(0)          # fill NaN with 0
df["col"] = df["col"].replace("old", "new")

# ---- PANDAS SORTING AND RANKING -----------------------------

df.sort_values("column", ascending=False)
df.sort_values(["col1", "col2"], ascending=[False, True])
df.reset_index(drop=True)   # reset index after sorting

# ---- PANDAS GROUPBY AND AGGREGATION -------------------------

# Basic groupby
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

# ---- PANDAS MERGE (equivalent to SQL JOIN) ------------------

# Inner join -- only matching rows
merged = df1.merge(df2, on="user_id", how="inner")

# Left join -- all rows from left, NaN for unmatched right
merged = df1.merge(df2, on="user_id", how="left")

# Join on different column names
merged = df1.merge(df2, left_on="user_id", right_on="id")

# ---- DATETIME -----------------------------------------------

from datetime import datetime, timedelta

# Current time
now = datetime.now()

# Convert string column to datetime
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Extract components
df["hour"] = df["timestamp"].dt.hour
df["day_of_week"] = df["timestamp"].dt.dayofweek  # 0=Monday
df["day_name"] = df["timestamp"].dt.day_name()
df["month"] = df["timestamp"].dt.month
df["date"] = df["timestamp"].dt.date

# Boolean flags
df["is_nighttime"] = df["hour"].between(0, 4)
df["is_weekend"] = df["day_of_week"].isin([5, 6])

# Time arithmetic
one_week_ago = now - timedelta(days=7)

# Format datetime as string
now.strftime("%Y-%m-%d %H:%M")

# ---- PANDAS OUTPUT ------------------------------------------

# Save to CSV
df.to_csv("output.csv", index=False)

# Save to Excel with multiple sheets
from openpyxl.styles import PatternFill, Font
import openpyxl

with pd.ExcelWriter("report.xlsx", engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="Data", index=False)
    df2.to_excel(writer, sheet_name="Summary", index=False)

# ---- MATPLOTLIB VISUALIZATION -------------------------------

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

# Horizontal bar chart
plt.barh(df["user_id"], df["score"])

# Color coded bars
colors = ["red" if v > 6 else "steelblue" for v in df["score"]]
plt.bar(df["user_id"], df["score"], color=colors)

# Threshold line
plt.axhline(y=6.0, color="orange", linestyle="--", label="Threshold")
plt.legend()

# Scatter plot
plt.scatter(df["x"], df["y"], c=colors, s=100)

# Multiple subplots
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes[0, 0].bar(...)   # top left
axes[0, 1].bar(...)   # top right
axes[1, 0].scatter(...) # bottom left
axes[1, 1].pie(...)   # bottom right
plt.tight_layout()

# Close without showing (for automated pipelines)
plt.close()

# ---- JSON HANDLING ------------------------------------------

# Load JSON file
with open("logs.json", "r") as f:
    data = json.load(f)

# Access nested fields
ip = data[0]["metadata"]["ip_address"]

# Flatten nested JSON to DataFrame
records = []
for item in data:
    records.append({
        "user_id": item["user_id"],
        "ip_address": item["metadata"]["ip_address"],
        "country": item["metadata"]["country"]
    })
df = pd.DataFrame(records)

# ---- REGULAR EXPRESSIONS ------------------------------------

import re

# Find first match
match = re.search(r"\d+", text)
if match:
    print(match.group())

# Find all matches
all_numbers = re.findall(r"\d+", text)

# Find IP addresses
ip_pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
ips = re.findall(ip_pattern, text)

# Find timestamps
ts_pattern = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"
timestamps = re.findall(ts_pattern, text)

# Find user IDs
user_pattern = r"USR_\d{3}"
users = re.findall(user_pattern, text)

# Named groups
pattern = r"(?P<timestamp>\d{4}-\d{2}-\d{2}) (?P<user>USR_\d{3})"
match = re.search(pattern, log_line)
if match:
    ts = match.group("timestamp")
    user = match.group("user")

# Replace/redact
redacted = re.sub(ip_pattern, "[REDACTED IP]", text)

# ---- ISOLATION FOREST (ML ANOMALY DETECTION) ----------------

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# Prepare and normalize features
features = df[["col1", "col2", "col3"]].copy()
scaler = StandardScaler()
scaled = scaler.fit_transform(features)

# Train model -- contamination = expected % of anomalies
model = IsolationForest(contamination=0.2, random_state=42)
predictions = model.fit_predict(scaled)  # 1=normal, -1=anomaly

# Get anomaly scores normalized to 0-100
raw_scores = model.decision_function(scaled)
anomaly_scores = 100 - (
    (raw_scores - raw_scores.min()) /
    (raw_scores.max() - raw_scores.min()) * 100
)

# Add to DataFrame
df["anomaly_flag"] = np.where(predictions == -1, 1, 0)
df["anomaly_score"] = anomaly_scores.round(1)

# ---- NETWORKX GRAPH ANALYSIS --------------------------------

import networkx as nx

# Create graph
G = nx.Graph()

# Add edges (connections between nodes)
G.add_edge("USR_001", "USR_003")
G.add_edge("USR_001", "USR_005")

# Build from shared IP data
for ip in ip_data["ip_address"].unique():
    users = ip_data[ip_data["ip_address"] == ip]["user_id"].tolist()
    for i in range(len(users)):
        for j in range(i + 1, len(users)):
            G.add_edge(users[i], users[j])

# Graph statistics
G.number_of_nodes()
G.number_of_edges()

# Connected components -- clusters of linked accounts
components = list(nx.connected_components(G))
for component in components:
    print(f"Cluster: {component} ({len(component)} accounts)")

# Flag large clusters
large_clusters = [c for c in components if len(c) > 2]

# Degree -- how many connections each node has
degrees = sorted(G.degree(), key=lambda x: x[1], reverse=True)

# Map cluster size back to DataFrame
component_map = {}
for component in components:
    for user in component:
        component_map[user] = len(component)
df["cluster_size"] = df["user_id"].map(component_map).fillna(1)

# ---- CBRN KEYWORD CLASSIFICATION ----------------------------

def classify_query(query_text):
    """Classify query into CBRN threat category."""
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

# ---- BEHAVIORAL SCORING SCHEMA v1.0 -------------------------

# Signal 1: Midnight activity ratio (>20% = flag, 20pts)
# Signal 2: CBRN query percentage (>25% = flag, 30pts)
# Signal 3: Unknown country queries (any = flag, 20pts)
# Signal 4: Response length anomaly (>1.5 std = flag, 15pts)
# Signal 5: Network connectivity (any shared IP = flag, 15pts)

# Rule-based scoring pattern
df["rule_score"] = 0
df["flags"] = ""

mask = df["midnight_ratio"] > 0.20
df.loc[mask, "rule_score"] += 20
df.loc[mask, "flags"] += "MIDNIGHT_ACTIVITY | "

# Z-score calculation for anomaly threshold
pop_mean = df["avg_response"].mean()
pop_std = df["avg_response"].std()
df["response_zscore"] = ((df["avg_response"] - pop_mean) / pop_std).round(3)

# ---- GIT COMMANDS -------------------------------------------

# git init                          -- initialize repository
# git add .                         -- stage all changes
# git add filename.py               -- stage specific file
# git commit -m "message"           -- save snapshot
# git push                          -- push to GitHub
# git status                        -- see current state
# git log --oneline                 -- see commit history
# git rm --cached file.py           -- untrack a file

# ---- SQL QUICK REFERENCE ------------------------------------

# Basic query structure (Silly Frogs Wear Green Hats Outdoors)
# SELECT, FROM, WHERE, GROUP BY, HAVING, ORDER BY

# Window functions
# ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY timestamp)
# RANK() OVER (PARTITION BY user_id ORDER BY score DESC)
# LAG(timestamp) OVER (PARTITION BY user_id ORDER BY timestamp)
# LEAD(timestamp) OVER (PARTITION BY user_id ORDER BY timestamp)
# AVG(response_length) OVER (PARTITION BY user_id)

# CTE structure
# WITH cte_name AS (
#     SELECT ...
# )
# SELECT * FROM cte_name;

# Recursive CTE structure
# WITH RECURSIVE cte AS (
#     SELECT ...              -- anchor
#     UNION ALL
#     SELECT ... FROM cte     -- recursive step
#     WHERE depth < 5         -- stopping condition
# )

# CBRN keyword detection in SQL
# INSTR(LOWER(query_text), 'synthesize') > 0

# Pivot table pattern
# SUM(CASE WHEN category = 'Chemical' THEN 1 ELSE 0 END) AS chemical

# Temporal SQL -- time between events
# ROUND((JULIANDAY(timestamp) - JULIANDAY(prev_timestamp)) * 86400, 0)

# Index for performance
# CREATE INDEX IF NOT EXISTS idx_country ON table(country);
# EXPLAIN QUERY PLAN SELECT ...  -- check if index is used