import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- Load data ---
df = pd.read_csv('data/capstone_logs_clean.csv')

# --- Step 1: Compute query count per user ---
query_counts = df.groupby('user_id').size().reset_index(name='query_count')

# --- Step 2: Compute mean and standard deviation across all users ---
mean_queries = query_counts['query_count'].mean()
std_queries = query_counts['query_count'].std()

print(f"Mean queries per user: {mean_queries:.1f}")
print(f"Std deviation: {std_queries:.1f}")

# --- Step 3: Compute z-score for each user ---
query_counts['z_score'] = (query_counts['query_count'] - mean_queries) / std_queries

# --- Step 4: Flag outliers at z > 2 ---
query_counts['outlier'] = query_counts['z_score'] > 2

# --- Step 5: Print results ---
print("\nAll users with z-scores:")
print(query_counts.sort_values('z_score', ascending=False).to_string(index=False))

print("\nFlagged outliers (z > 2):")
print(query_counts[query_counts['outlier']].sort_values('z_score', ascending=False).to_string(index=False))

# --- Step 6: Visualize the distribution ---
plt.figure(figsize=(10, 5))
plt.bar(query_counts['user_id'], query_counts['query_count'], color='steelblue')
plt.axhline(mean_queries + 2 * std_queries, color='red', linestyle='--', label='Z=2 threshold')
plt.xlabel('User ID')
plt.ylabel('Query Count')
plt.title('Query Count per User with Z-score Threshold')
plt.legend()
plt.tight_layout()
plt.savefig('outputs/week9_day1_zscore_chart.png')
plt.show()
print("\nChart saved to outputs/week9_day1_zscore_chart.png")