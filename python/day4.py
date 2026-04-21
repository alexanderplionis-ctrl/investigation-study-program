# Day 4 - Introduction to pandas
import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv("accounts.csv")

# Basic exploration -- always do this first with new data
print("--- DataFrame Shape ---")
print(df.shape)         # rows and columns

print("\n--- Column Names ---")
print(df.columns.tolist())

print("\n--- First 5 Rows ---")
print(df.head())

print("\n--- Data Types ---")
print(df.dtypes)

print("\n--- Basic Statistics ---")
print(df.describe())

# Filtering and Sorting
print("\n--- High Query Accounts ---")
high_query = df[df["query_count"] > 500]
print(high_query)

print("\n--- Accounts with CBRN Hits ---")
cbrn_accounts = df[df["cbrn_hits"] > 0]
print(cbrn_accounts)

print("\n--- Sorted by Risk (query_count descending) ---")
sorted_df = df.sort_values("query_count", ascending=False)
print(sorted_df)

print("\n--- Multiple Conditions ---")
suspicious = df[(df["query_count"] > 100) & (df["cbrn_hits"] > 0)]
print(suspicious)

# Adding calculated columns
print("\n--- Calculated Columns ---")

df["velocity"] =df["query_count"] / df["account_age_days"]
df["cbrn_ratio"] = df["cbrn_hits"] / df["query_count"]
df["risk_score"] = (df["velocity"] * 0.4) + (df["cbrn_ratio"] * 100 * 0.6)
df["risk_score"] = df["risk_score"].round(2)

# Round columns for clean output
df["velocity"] = df["velocity"].round(2)
df["cbrn_ratio"] = df["cbrn_ratio"].round(4)

print(df[["user_id", "velocity", "cbrn_ratio", "risk_score"]])

print("\n--- Final Risk Ranking ---")
ranked = df.sort_values("risk_score", ascending=False)
print(ranked[["user_id", "query_count", "cbrn_hits", "risk_score"]])

# Saving results
print("\n--- Saving Results ---")

ranked.to_csv("investigation_queue.csv", index=False)
print("Investigation queue saved to investigation_queue.csv")

# Save only flagged accounts
flagged = ranked[ranked["risk_score"] >= 6.0]
flagged.to_csv("flagged_accounts.csv", index=False)
print(f"Flagged accounts saved: {len(flagged)} accounts")

