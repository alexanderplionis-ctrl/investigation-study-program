# Week 7 - pandas Deep Dive
import pandas as pd
import numpy as np

pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)

# Load our capstone data
logs = pd.read_csv("capstone_logs_clean.csv")
logs["timestamp"] = pd.to_datetime(logs["timestamp"])

print(f"Loaded {len(logs)} log entries")
print(logs.dtypes)
print(logs.head())

# Create a user profile DataFrame
profiles = pd.DataFrame({
    "user_id": ["USR_001", "USR_002", "USR_003", "USR_004", "USR_005",
                "USR_006", "USR_007", "USR_008", "USR_009", "USR_010"],
    "account_type": ["free", "premium", "free", "premium", "free",
                     "premium", "free", "premium", "free", "premium"],
    "account_age_days": [45, 365, 180, 90, 270, 120, 30, 450, 60, 200],
    "verified": [True, True, False, True, False,
                 True, False, True, False, True]
})

print("\n--- User Profiles ---")
print(profiles)

# Merging DataFrames --- pandas equivalent of SQL JOIN
print("\n--- Merged DataFrame ---")

# Inner merge -- only rows with matches in both DataFrames
merged = logs.merge(profiles, on="user_id", how="inner")
print(f"Logs rows: {len(logs)}")
print(f"Profiles rows: {len(profiles)}")
print(f"Merged rows: {len(merged)}")
print(merged.head())

# Check new columns added from profiles
print(f"\nMerged columns: {merged.columns.tolist()}")

# Left merge -- keep all logs even if no profile match
merged_left = logs.merge(profiles, on="user_id", how="left")
print(f"\nLeft merge rows: {len(merged_left)}")
print(f"Null account_types: {merged_left['account_type'].isna().sum()}")

# Advanced groupby analysis
print("\n--- Account Type Analysis ---")

account_analysis = merged.groupby("account_type").agg(
    total_queries=("user_id", "count"),
    unique_users=("user_id", "nunique"),
    avg_response=("response_length", "mean"),
    max_response=("response_length", "max"),
    unknown_country=("country", lambda x: (x == "Unknown").sum())
).round(1)

print(account_analysis)

print("\n--- Verified vs Unverified ---")
verified_analysis = merged.groupby("verified").agg(
    total_queries=("user_id", "count"),
    unique_users=("user_id", "nunique"),
    avg_response=("response_length", "mean")
).round(1)

print(verified_analysis)

# apply() and lambda functions
print("\n--- Apply and Lambda ---")

# Simple lambda -- classify response length
merged["response_tier"] = merged["response_length"].apply(
    lambda x: "Long" if x > 3000 else "Medium" if x > 1500 else "Short"
)

print(merged["response_tier"].value_counts())

# Apply a more complex function
def classify_query(query_text):
    """Classify query into CBRN category."""
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
    
merged["cbrn_category"] = merged["query_text"].apply(classify_query)
print("\nCBRN Category Distribution:")
print(merged["cbrn_category"].value_counts())

# Datetime deep dive
print("\n--- Datetime Feature Engineering ---")

# Extract time components
merged["hour"] = merged["timestamp"].dt.hour
merged["day_of_week"] = merged["timestamp"].dt.dayofweek # 0=Monday, 6=Sunday
merged["day_name"] = merged["timestamp"].dt.day_name()
merged["month"] = merged["timestamp"].dt.month
merged["is_weekend"] = merged["day_of_week"].isin([5,6])
merged["is_nighttime"] = merged["hour"].between(0,4)

print("Hour distribution:")
print(merged["hour"].value_counts().sort_index())

print("\nDay of week distribution:")
print(merged.groupby("day_name")["user_id"].count().sort_values(ascending=False))

print("\nNighttime queries:")
print(f"Total: {merged['is_nighttime'].sum()}")
print(f"Percentage: {merged['is_weekend'].mean()*100:.1f}%")

print("\nWeekend queries:")
print(f"Total: {merged['is_weekend'].sum()}")
print(f"Percentage: {merged['is_weekend'].mean()*100:.1f}%")

# Build a complete user behavioral profile
print("\n--- User Behavioral Profile ---")

# Calculate pre-user statistics
user_profile = merged.groupby("user_id").agg(
    total_queries=("user_id", "count"),
    avg_response=("response_length", "mean"),
    nighttime_queries=("is_nighttime", "sum"),
    weekend_queries=("is_weekend", "sum"),
    unknown_country=("country", lambda x: (x == "Unknown").sum()),
    cbrn_queries=("cbrn_category", lambda x: (x != "Benign").sum())
).round(1).reset_index()

# Add calculated ratio columns
user_profile["nighttime_pct"] = (
    user_profile["nighttime_queries"] / user_profile["total_queries"] * 100
).round(1)

user_profile["cbrn_pct"] = (
    user_profile["cbrn_queries"] / user_profile["total_queries"] * 100
).round(1)

# Add account type from profiles
user_profile = user_profile.merge(profiles[["user_id", "account_type", "verified", "account_age_days"]], on="user_id")
                                  
print(user_profile.to_string())