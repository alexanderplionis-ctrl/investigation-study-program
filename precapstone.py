# Pre-Capstone Tools -- SQLAlchemy, IsolationForest, NetworkX
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.ensemble import IsolationForest
import networkx as nx
import matplotlib.pyplot as plt

pd.set_option("display.max_columns", None)

# -- Tool 1: SQLAlchemy --
print("---SQLAlchemy Database Connection ---")

# Connect to the investigation database
engine = create_engine("sqlite:///investigation.db")

# Run SQL query directly from Python
df = pd.read_sql("""
                 SELECT user_id,
                    timestamp,
                    query_text,
                    response_length,
                    country
                 FROM capstone_logs
                 ORDER BY timestamp
""", engine)

print(f"Loaded {len(df)} rows from database")
print(f"Columns: {df.columns.tolist()}")
print(df.head())

# Running a more complex investigation query via SQLAlchemy
print("\n--- Complex SQL Query via SQLAlchemy ---")

investigation_query = """
    SELECT user_id,
    COUNT(*) AS total_queries,
    AVG(response_length) AS avg_response,
    SUM(CASE WHEN STRFTIME('%H', timestamp) BETWEEN '00' AND '03'
        THEN 1 ELSE 0 END) AS midnight_queries,
    SUM(CASE WHEN country = 'Unknown'
        THEN 1 ELSE 0 END) AS unknown_country_queries
    FROM capstone_logs
    GROUP BY user_id
    ORDER BY total_queries DESC
"""

user_stats = pd.read_sql(investigation_query, engine)
user_stats["midnight_pct"] = (
    user_stats["midnight_queries"] / user_stats["total_queries"] * 100
).round(1)
user_stats["avg_response"] = user_stats["avg_response"].round(0)

print(user_stats)

# -- Tool 2: IsolationForest --
print("\n--- IsolationForest Anomaly Detection ---")

from sklearn.preprocessing import StandardScaler

# Prepare features for anomaly detection
features = user_stats[["total_queries", "avg_response",
                       "midnight_queries", "unknown_country_queries",
                       "midnight_pct"]].copy()

# Normalize features to same scale
scalar = StandardScaler()
scaled_features = scalar.fit_transform(features)

# Train IsolationForest
model = IsolationForest(contamination=0.2, random_state=42)
predictions = model.fit_predict(scaled_features)

# Get anomaly scores and convert to 0-100 scale
raw_scores = model.decision_function(scaled_features)
anomaly_scores = 100 - ((raw_scores - raw_scores.min()) /
                        (raw_scores.max() - raw_scores.min()) * 100)
anomaly_scores = anomaly_scores.round(1)

# Add results to DataFrame
user_stats["anomaly_flag"] = predictions # 1=normal, -1=anomaly
user_stats["anomaly_score"] = anomaly_scores

print(user_stats[["user_id", "total_queries", "midnight_pct",
                  "anomaly_flag", "anomaly_score"]].sort_values(
                    "anomaly_score", ascending=False))

# -- Tool 3: NetworkX --
print("\n--- NetworkX Graph Analysis (Simulated) ---")

# Create simulated shared infrastructure data
shared_ip_data = pd.DataFrame({
    "user_id": ["USR_001", "USR_003", "USR_001", "USR_005", 
                "USR_007", "USR_009", "USR_002", "USR_002",
                "USR_006", "USR_008"],
    "ip_address": ["10.0.0.1", "10.0.0.1", "10.0.0.2", "10.0.0.2",
                   "10.0.0.3", "10.0.0.3", "10.0.0.4", "10.0.0.5",
                   "10.0.0.5", "10.0.0.6"]
})

print("Simulated shared IP connections:")
print(shared_ip_data)

# Build graph
G = nx.Graph()

for ip in shared_ip_data["ip_address"].unique():
    users_sharing_ip = shared_ip_data[
        shared_ip_data["ip_address"] == ip]["user_id"].tolist()
    for i in range(len(users_sharing_ip)):
        for j in range(i + 1, len(users_sharing_ip)):
            G.add_edge(users_sharing_ip[i], users_sharing_ip[j], ip=ip)

print(f"\nGraph nodes: {G.number_of_nodes()}")
print(f"Graph edges: {G.number_of_edges()}")

# Find connected components
components = list(nx.connected_components(G))
print(f"\nConnected components: {len(components)}")
for i, component in enumerate(components):
    print(f"  Component {i+1}: {component} ({len(component)} accounts)")

# Flag large components
print("\nLarge clusters (more than 2 accounts):")
for component in components:
    if len(component) > 2:
        print(f"  FLAGGED cluster: {component}")

# Degree centrality
print("\nAccount connectivity (degree):")
degrees = sorted(G.degree(), key=lambda x: x[1], reverse=True)
for user, degree in degrees[:5]:
    print(f"  {user}: connected to {degree} other accounts")