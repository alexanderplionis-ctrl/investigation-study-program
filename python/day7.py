# Day 7 - JSON Handling

import json
import pandas as pd

pd.set_option("display.max_columns", None)

# Step 1 -- Load the JSON file
with open("api_logs.json", "r") as f:
    logs = json.load(f)

# Step 2 -- Inspect what we loaded
print(f"Type: {type(logs)}")
print(f"Number of records: {len(logs)}")
print(f"\nFirst Record:")
print(logs[0])

# Step 3 -- Extract fields including nested metadata
print("\n--- Extracting Fields ---")

records = []
for log in logs:
    record = {
        "user_id": log["user_id"],
        "timestamp": log["timestamp"],
        "query_text": log["query_text"],
        "response_length": log["response_length"],
        "ip_address": log["metadata"]["ip_address"],
        "country": log["metadata"]["country"],
        "flagged": log["metadata"]["flagged"]
    }
    records.append(record)

# Convert to DataFrame
df = pd.DataFrame(records)
print(df)
print(f"\nColumns: {df.columns.tolist()}")
print(f"Shape: {df.shape}")

# Step 4 -- Analyze the JSON data
print("\n--- JSON Data Analysis ---")

# Convert timestamp to datatime
df["timestamp"] = pd.to_datetime(df["timestamp"])
df["hour"] = df["timestamp"].dt.hour
# Flag long responses
df["long_response"] = df["response_length"] > 2000

# Show nighttime queries
print("\nNighttime queries (midnight to 4am):")
nighttime = df[df["hour"].between(0, 4)]
print(nighttime[["user_id", "timestamp", "query_text", "response_length"]])

# Show long responses
print("\nLong responses (>2000 chars):")
long = df[df["long_response"]]
print(long[["user_id", "query_text", "response_length"]])

# Summary statistics
print("\nResponse length statistics:")
print(df["response_length"].describe())

# Step 5 -- Save results
print("\n--- Saving JSON Analysis Results ---")

# Save full extracted data
df.to_csv("json_analysis.csv", index=False)
print("Full analysis saved to json_analysis.csv")

# Save only nighttime long response queries
suspicious = df[
    (df["hour"].between(0, 4)) &
    (df["response_length"] > 2000)
]
suspicious.to_csv("suspicious_queries.csv", index=False)
print(f"Suspicious queries saved: {len(suspicious)} records")