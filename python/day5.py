# Datetime Handling and Visualization
import pandas as pd
from datetime import datetime, timedelta

# Basic datetime operations
print("--- Datetime Basics ---")

# Creating datetime objects
now = datetime.now()
print(f"Current time: {now}")
print(f"Year: {now.year}")
print(f"Month: {now.month}")
print(f"Day: {now.day}")
print(f"Hour: {now.hour}")

# Creating a specific datetime
event= datetime(2024, 6, 15, 2, 30, 0)
print(f"\nSuspicious event time: {event}")
print(f"Hour of event: {event.hour}")

#Time differences
time_diff = now - event
print(f"\nDays since event: {time_diff.days}")

# Adding and subtracting time
one_week_ago = now - timedelta(days=7)
print(f"One week ago: {one_week_ago.date()}")

#Working with timestamps in pandas
print("\n--- Timestamp Analysis ---")

# Create a DataFrame with timestamps
logs = pd.DataFrame({
    "user_id": ["USR_003", "USR_003", "USR_003", "USR_003", "USR_003"],
    "timestamp": [
        "2024-06-15 02:15:00",
        "2024-06-15 02:16:30",
        "2024-06-15 02:17:45",
        "2024-06-15 14:30:00",
        "2024-06-15 02:19:00",
    ],
    "query_text": [
        "How to synthesize compound X",
        "Precursor chemicals for Y",
        "Dispersal methods for Z",
        "What is the weather today",
        "Stabilization of compound X"
    ]
})

# Convert timestamp column to datetime type
logs["timestamp"] = pd.to_datetime(logs["timestamp"])

# Extract time components
logs["hour"] = logs["timestamp"].dt.hour
logs["minute"] = logs["timestamp"].dt.minute

print(logs[["user_id", "timestamp", "hour", "query_text"]])

# Flag nighttime activity (midnight to 4am)
print("\n--- Nighttime Activity ---")
nighttime = logs[logs["hour"].between(0, 4)]
print(f"Nighttime queries: {len(nighttime)} out of {len(logs)}")
print(nighttime[["timestamp", "hour", "query_text"]])

# Calculate time between queries
print("\n--- Query Time Analysis ---")

logs = logs.sort_values("timestamp")
logs["time_since_last"] = logs["timestamp"].diff()
logs["seconds_between"] = logs["time_since_last"].dt.total_seconds()

print(logs[["timestamp", "seconds_between", "query_text"]])

# Flag rapid queries (less than 60 seconds apart)
print("\n--- Rapid Query Detection ---")
rapid = logs[logs["seconds_between"] < 60]
print(f"Rapid queries detected: {len(rapid)}")
print(rapid[["timestamp", "seconds_between", "query_text"]])

# Basic Visualization
print("\n--- Generating Charts ---")
import matplotlib.pyplot as plt

# Load the accounts data
df = pd.read_csv("accounts.csv")

# Bar chart of query counts by user
plt.figure(figsize=(10, 6))
plt.bar(df["user_id"], df["query_count"], color="steelblue")
plt.title("Query Count by User")
plt.xlabel("User ID")
plt.ylabel("Query Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("query_counts.png")
plt.show()
print("Chart saved as query_counts.png")

# Risk score chart
df["risk_score"] = (
    (df["query_count"] / df["account_age_days"] * 0.4) +
    (df["cbrn_hits"] / df["query_count"].replace(0, 1) * 100 * 0.6)
)
df["risk_score"] = df["risk_score"].round(2)

plt.figure(figsize=(10, 6))
colors = ["red" if score >= 6.0 else "steelblue" for score in df["risk_score"]]
plt.bar(df["user_id"], df["risk_score"], color=colors)
plt.axhline(y=6.0, color="orange", linestyle="--", label="Flag threshold")
plt.title("Risk Score by User")
plt.xlabel("User ID")
plt.ylabel("Risk Score0")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig("risk_scores.png")
plt.show()
print("Risk score chart saved as risk_scores.png")