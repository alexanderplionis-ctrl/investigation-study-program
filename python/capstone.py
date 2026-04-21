# Month 1 Capstone -- Task 2
# Python/pandas analysis of capstone_logs

import pandas as pd

# Load the clean CSV
df=pd.read_csv("capstone_logs_clean.csv")
print(f"Loaded {len(df)} rows")
print(f"Columns {df.columns.tolist()}")
print(df.head())

# Task 2a -- Convert timestamp to datatime
df["timestamp"] = pd.to_datetime(df["timestamp"])

# Task 2b -- Filter rows where response length > 2000
print("\n--- Filtering Long Responses ---")
long_responses = df[df["response_length"] > 2000]
print(f"Total rows: {len(df)}")
print(f"Rows with response_length > 2000: {len(long_responses)}")
print(f"Percentage: {len(long_responses)/len(df)*100:.1f}%")

# Task 2c -- Add flagged column and output CSV
print("\n--- Adding Flagged Column ---")
df["flagged"] = df["response_length"] > 2000
flagged_df = df[df["flagged"] == True].copy()
print(f"Flagged accounts: {len(flagged_df)}")

# Save to new CSV
flagged_df.to_csv("capstone_flagged.csv", index=False)
print("Saved to capstone_flagged.csv")

# Summary by user
print("\n--- Flagged Queries by User ---")
user_summary = flagged_df.groupby("user_id").agg(
    flagged_queries=("flagged", "count"),
    avg_response=("response_length", "mean")
).round(0).sort_values("flagged_queries", ascending=False)
print(user_summary)