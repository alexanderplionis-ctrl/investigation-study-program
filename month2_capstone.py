# Month 2 Capstone -- End-to-End Detection Pipeline
# Behavioral Scoring and Schema v1.0
# Signals: Midnight Activity, CBRN%, Unknown Country, Response Anomaly, Network Connectivity

import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import networkx as nx
import matplotlib.pyplot as plt
from datetime import datetime

pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

print("=" * 60)
print("MONTH 2 CAPSTONE -- END-TO-END DETECTION PIPELINE")
print(f"Run time: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 60)

# -- Step 1: Data Ingestion via SQLAlchemy --
print("\n--- Step 1: Data Ingestion ---")

engine = create_engine("sqlite:///investigation.db")

logs = pd.read_sql("""
    SELECT user_id, timestamp, query_text,
                response_length, country, ip_address
    FROM capstone_logs
    ORDER BY timestamp
""", engine)

logs["timestamp"] = pd.to_datetime(logs["timestamp"])
print(f"Loaded {len(logs)} log entries from database")
print(f"Users: {logs['user_id'].nunique()}")
print(f"Date range: {logs['timestamp'].min().date()} to {logs['timestamp'].max().date()}")

# -- Step 2: Feature Engineering --
print("\n--- Step 2: Feature Engineering ---")

# CBRN classification function
def classify_query(query_text):
    text = query_text.lower()
    if any(word in text for word in ["synthesize", "compound", "stabilize"]):
        return "Chemical"
    elif any(word in text for word in ["pathogen", "transmission"]):
        return "Biological"
    elif any(word in text for word in ["nuclear", "fission"]):
        return "Radiological"
    elif any(word in text for word in ["dispersal", "precursor"]):
        return "Explosive"
    else:
        return "Benign"

# Apply classification
logs["cbrn_category"] = logs["query_text"].apply(classify_query)
logs["is_cbrn"] = logs["cbrn_category"] != "Benign"
logs["hour"] = logs["timestamp"].dt.hour
logs["is_nighttime"] = logs["hour"].between(0,3)
logs["is_unknown_country"] = logs["country"] == 'Unknown'

# Calculate per-user behavioral signals
user_features = logs.groupby("user_id").agg(
    total_queries=("user_id", "count"),
    avg_response=("response_length", "mean"),
    cbrn_queries=("is_cbrn", "sum"),
    nighttime_queries=("is_nighttime", "sum"),
    unknown_country_queries=("is_unknown_country", "sum"),
    unique_ips=("ip_address", "nunique")
).reset_index()

# Calculate signal ratios
user_features["midnight_ratio"] = (
    user_features["nighttime_queries"] /
    user_features["total_queries"]
).round(3)

user_features["cbrn_ratio"] = (
    user_features["cbrn_queries"] /
    user_features["total_queries"]
).round(3)

user_features["unknown_ratio"] = (
    user_features["unknown_country_queries"] /
    user_features["total_queries"]
).round(3)

# Signal 4 -- response length anomaly vs population
pop_mean = user_features["avg_response"].mean()
pop_std = user_features["avg_response"].std()
user_features["response_zscore"] = (
    (user_features["avg_response"]- pop_mean) / pop_std
).round(3)

print(f"Features calculated for {len(user_features)} users")
print(user_features[["user_id", "total_queries", "midnight_ratio", "cbrn_ratio", "unknown_ratio", "response_zscore"]].to_string())

# -- Step 3: Rule-Based Detection Layer --
print("\n--- Step 3: Rule-Based Detection ---")

# Initialize scoring columns
user_features["rule_score"] = 0
user_features["flags"] = ""

# Rule 1: Midnight activity ratio > 0.20 (20 points)
mask = user_features["midnight_ratio"] > 0.20
user_features.loc[mask, "rule_score"] += 20
user_features.loc[mask, "flags"] += "MIDNIGHT_ACTIVITY | "
print(f"Rule 1 (Midnight >20%): {mask.sum()} accounts flagged")

# Rule 2: CBRN query ratio > 0.25 (30 points)
mask = user_features["cbrn_ratio"] > 0.25
user_features.loc[mask, "rule_score"] += 30
user_features.loc[mask, "flags"] += "HIGH_CBRN | "
print(f"Rule 2 (CBRN >25%): {mask.sum()} accounts flagged")

# Rule 3: Any unknown country queries (20 points)
mask = user_features["unknown_ratio"] > 0
user_features.loc[mask, "rule_score"] += 20
user_features.loc[mask, "flags"] += "UNKNOWN_COUNTRY | "
print(f"Rule 3 (Unknown country): {mask.sum()} accounts flagged")

# Rule 4: Response length z-score > 1.5 (15 points)
mask = user_features["response_zscore"] > 1.5
user_features.loc[mask, "rule_score"] += 15
user_features.loc[mask, "flags"] += "RESPONSE_ANOMALY | "
print(f"Rule 4 (Response anomaly): {mask.sum()} accounts flagged")

# Rule 5: Multiple unique IPs (15 points)
mask = user_features["unique_ips"] > 5
user_features.loc[mask, "rule_score"] += 15
user_features.loc[mask, "flags"] += "MULTIPLE_IPS | "
print(f"Rule 5 (Multiple IPs): {mask.sum()} accounts flagged")

print("\nRule-based scores:")
print(user_features[["user_id", "rule_score", "flags"]].to_string())

# -- Step 4: IsolationForest ML Layer --
print("\n--- Step 4: IsolationForest ML Scoring ---")

# Prepare features for ML
ml_features = user_features[[
    "total_queries", "avg_response", "midnight_ratio", "cbrn_ratio", "unknown_ratio", "response_zscore"
]].copy()

# Normalize features
scalar = StandardScaler()
scaled_features = scalar.fit_transform(ml_features)

# Train IsolationForest
model = IsolationForest(contamination=0.2, random_state=42)
predictions = model.fit_predict(scaled_features)

# Get Anomaly scores normalized to 0-100
raw_scores = model.decision_function(scaled_features)
ml_scores = 100 - ((raw_scores - raw_scores.min()) /
                   (raw_scores.max() -raw_scores.min()) * 100)

# Add to user features
user_features["ml_anomaly"] = np.where(predictions == -1, 1, 0)
user_features["ml_score"] = ml_scores.round(1)

print(f"ML anomalies detected: {user_features['ml_anomaly'].sum()}")
print(user_features[["user_id", "ml_anomaly", "ml_score"]].sort_values("ml_score", ascending=False).to_string())

# -- Step 5: Network Analysis Layer --
print("\n--- Step 5: Network Analysis ---")

# Build shared IP network from actual log data
G = nx.Graph()

ip_users = logs.groupby("ip_address")["user_id"].unique()
for ip, users in ip_users.items():
    if len(users) > 1:
        for i in range(len(users)):
            for j in range(i + 1, len(users)):
                G.add_edge(users[i], users[j], ip=ip)

print(f"Network nodes: {G.number_of_nodes()}")
print(f"Network edges: {G.number_of_edges()}")

# Get degree for each user
degree_dict = dict(G.degree())
user_features["network_degree"] = user_features["user_id"].map(
    degree_dict).fillna(0).astype(int)

# Find connected components
if G.number_of_nodes() > 0:
    components = list(nx.connected_components(G))
    print(f"Connected components: {len(components)}")

    # Map each user to their component size
    component_map = {}
    for component in components:
        for user in component:
            component_map[user] = len(component)
    
    user_features["cluster_size"] = user_features["user_id"].map(
        component_map).fillna(1).astype(int)
else:
    print("No shared IPs found in dataset")
    user_features["cluster_size"] = 1

# Flag users in large clusters
user_features["network_flag"] = (
    user_features["cluster_size"] > 2).astype(int)

print("\nNetwork analysis results:")
print(user_features[["user_id", "network_degree", "cluster_size", "network_flag"]].to_string())

# -- Step 6: Composite Ranking --
print("\n--- Step 6: Composite Ranking ---")

# Normalize ML score to 0-40 range for composite
user_features["ml_contribution"] = (
    user_features["ml_score"] * 0.4).round(1)

# Network bonus -- 15 points for being in large cluster
user_features["network_contribution"] = (
    user_features["network_flag"] * 15)

# Composite score -- rule score (max 100) + ml contribution (max 40)
# + network contribution (max 15)
user_features["composite_score"] = (
    user_features["rule_score"] +
    user_features["ml_contribution"] +
    user_features["network_contribution"]
).round(1)

# Final priority ranking
priority_queue = user_features[[
    "user_id", "rule_score", "ml_score", "network_flag", "composite_score", "flags"
]].sort_values("composite_score", ascending=False).reset_index(drop=True)

priority_queue.index += 1 # start ranking at 1 not 0

print("PRIORITY INVESTIGATION QUEUE:")
print(priority_queue[["user_id", "rule_score", "ml_score", "composite_score"]].to_string())

# -- Step 7: Output and Investigation Summary --
print("\n--- Step 7: Output and Summary ---")

# Save priority queue to CSV
priority_queue.to_csv("month2_investigation_queue.csv", index=True)
print("Priority queue saved to month2_investigation_queue.csv")

# Generate text summaries for top 3 accounts
print("\n" + "=" * 60)
print("INVESTIGATION BRIEF -- TOP PRIORITY ACCOUNTS")
print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print("=" * 60)

for rank in range(1, 4):
    row = priority_queue.loc[rank]
    features = user_features[
        user_features["user_id"] == row["user_id"]].iloc[0]
    
    print(f"\nRank {rank}: {row['user_id']}")
    print(f"  Composite Score:    {row['composite_score']}")
    print(f"  Rule Score:         {row['rule_score']}")
    print(f"  ML Anomaly Score:   {row['ml_score']}")
    print(f"  Flags:              {row['flags'].strip(' |')}")
    print(f"  Total Queries:      {features['total_queries']}")
    print(f"  Midnight Ratio:     {features['midnight_ratio']*100:.1f}%")
    print(f"  CBRN Ratio:         {features['cbrn_ratio']*100:.1f}%")
    print(f"  Unknown Country:    {features['unknown_ratio']*100:.1f}%")
    print(f"  Response Z-Score:   {features['response_zscore']}")
    print("-" * 60)

print("\nFULL PIPELINE COMPLETE")
print(f"Accounts analyzed: {len(user_features)}")
print(f"Accounts in queue: {len(priority_queue)}")
print(f"Output saved: month2_investigation_queue.csv")
print("=" * 60)