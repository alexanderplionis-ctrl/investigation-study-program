# Day 6 - Complete Investigation Pipeline
# This script loads account data, scores risk, detects suspicious 
# behavior, generates charts, and saves an investigation queue

import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# ---Step 1: Load Data----
def load_accounts(filepath):
    """Load account data from CSV and return a DataFrame."""
    df = pd.read_csv(filepath)
    print(f"Loaded {len(df)} accounts from {filepath}")
    return df

# Run Step 1
df = load_accounts("accounts.csv")
print(df.head())

#--- Step 2: Calculate Risk Scores ---
def calculate_risk_scores(df):
    """Add velocity, cbrn_ratio and risk_score columns to DataFrame."""
    df["velocity"] = (df["query_count"] / df["account_age_days"]).round(2)
    df["cbrn_ratio"] = (df["cbrn_hits"] / df["query_count"].replace(0, 1)).round(4)
    df["risk_score"] = (
        (df["velocity"] * 0.4) + 
        (df["cbrn_ratio"] * 100 * 0.6)
    ).round(2)
    print(f"Risk scores calculated for {len(df)} accounts")
    return df

# Run Step 2
df = calculate_risk_scores(df)
print(df[["user_id", "velocity", "cbrn_ratio","risk_score"]])

# --- Step 3: Flag Suspicious Accounts ---
def flag_accounts(df, threshold=6.0):
    """Add a flag column and return flagged accounts separately."""
    df["flagged"] = df["risk_score"] >= threshold
    flagged = df[df["flagged"]].sort_values("risk_score", ascending=False)
    print(f"Flagged {len(flagged)} accounts above threshold {threshold}")
    return df, flagged

# Run Step 3
df, flagged = flag_accounts(df)
print(flagged[["user_id", "risk_score", "country"]])

# --- Step 4: Generate Charts ---
def generate_charts(df):
    """Generate and save risk score visualization."""
    colors = ["red" if f else "steelblue" for f in df["flagged"]]

    plt.figure(figsize=(10, 6))
    plt.bar(df["user_id"], df["risk_score"], color=colors)
    plt.axhline(y=6.0, color="orange", linestyle="--", label="Flag threshold")
    plt.title(f"Account Risk Scores --- {datetime.now().strftime('%Y-%m-%d')}")
    plt.xlabel("User ID")
    plt.ylabel("Risk Score")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig("risk_scores.png")
    plt.close()
    print("chart saved as risk_scores.png")

# Run Step 4
generate_charts(df)

# --- Step 5: Generate Summary Report ---
def generate_report(df, flagged):
    """Print a plain English investigation summary."""
    print("\n" + "="*60)
    print("INVESTIGATION SUMMARY REPORT")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("="*60)

    print(f"\nACCOUNTS ANALYZED: {len(df)}")
    print(f"ACCOUNTS FLAGGED: {len(flagged)}")
    print(f"FLAG RATE:        {len(flagged)/len(df)*100:.1f}%")

    print("\nTOP PRIORITY ACCOUNTS:")
    for _, row in flagged.iterrows():
        print(f"  {row['user_id']:10} "
          f"Risk: {row['risk_score']:7.2f} "
          f"Queries: {row['query_count']:5} "
          f"CBRN Hits: {row['cbrn_hits']:3} "
          f"Country: {row['country']}")
    
    print("\nKEY STATISTICS:")
    print(f"   Highest risk score: {df['risk_score'].max()}")
    print(f"   Average risk score: {df['risk_score'].mean():.2f}")
    print(f"   Unknown country accounts: {(df['country'] == 'Unknown').sum()}")
    print("="*60)

# Run Step 5
generate_report(df, flagged)

# --- Step 6: Save Results ---
def save_results(df, flagged):
    """Save full ranked results and flagged accounts to CSV."""
    ranked = df.sort_values("risk_score", ascending=False)
    ranked.to_csv("investigation_queue.csv", index=False)
    flagged.to_csv("flagged_accounts.csv", index=False)
    print(f"\nResults saved:")
    print(f"   investigation_queue.csv -- all {len(ranked)} accounts ranked")
    print(f"   flagged_accounts.csv -- {len(flagged)} flagged accounts")

# Run Step 6
save_results(df, flagged)