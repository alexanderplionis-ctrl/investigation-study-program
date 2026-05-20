import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- Load data ---
df = pd.read_csv('data/capstone_logs_enhanced.csv')

# --- Step 1: Compute query count per user ---
query_counts = df.groupby('user_id').size().reset_index(name='query_count')

# --- Step 2: Compute percentile thresholds ---
p25 = query_counts['query_count'].quantile(0.25)
p75 = query_counts['query_count'].quantile(0.75)
p95 = query_counts['query_count'].quantile(0.95)
iqr = p75 -p25
upper_fence = p75 + (1.5 * iqr)

print(f"25th percentile: {p25:.1f}")
print(f"75th percentile: {p75:.1f}")
print(f"95th percentile: {p95:.1f}")
print(f"IQR: {iqr:.1f}")
print(f"Upper fence (outlier threshold): {upper_fence:.1f}")

# --- Step 3: Flag outliers using IQR method ---
query_counts['iqr_outlier'] = query_counts['query_count'] > upper_fence

# --- Step 4: Flag outliers using 95th percentile method ---
query_counts['p95_outlier'] = query_counts['query_count'] > p95

# --- Step 5: Print results ---
print("n\All users with percentile flags:")
print(query_counts.sort_values('query_count', ascending=False).to_string(index=False))

print("n\IQR outliers:")
print(query_counts[query_counts['iqr_outlier']].to_string(index=False))

print("n95th percentile outliers:")
print(query_counts[query_counts['p95_outlier']].to_string(index=False))

# --- Step 6: Box plot visualization ---
plt.figure(figsize=(8, 6))
plt.boxplot(query_counts['query_count'], vert=True, patch_artist=True,
            boxprops=dict(facecolor='steelblue', color='navy'),
            medianprops=dict(color='red', linewidth=2))
plt.axhline(p95, color='orange', linestyle='--', label=f'95th percentile: {p95:.0f}')
plt.axhline(upper_fence, color='red', linestyle='--', label=f'IQR upper fence: {upper_fence:.0f}')
plt.ylabel('Query Count')
plt.title('Query Count Distribution with Outlier Thresholds')
plt.legend()
plt.tight_layout()
plt.savefig('outputs/week9_day2_boxplot.png')
plt.show()
print("\nChart saved to outputs/week9_day2_boxplot.png")