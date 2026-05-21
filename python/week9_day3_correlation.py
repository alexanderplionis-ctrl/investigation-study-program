import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- Load Data ---
df = pd.read_csv('data/capstone_logs_enhanced.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])

# --- Stept 1: Feature engineering per user ---
# Extract hour from timestamp
df['hour'] = df['timestamp'].dt.hour

# Flag CBRN queries
CBRN_KEYWORDS = ['synthesize', 'pathogen', 'fission', 'dispersal', 'compound', 'nuclear', 'precursor', 'transmission']

df['is_cbrn'] = df['query_text'].str.lower().apply(
    lambda x: any(keyword in x for keyword in CBRN_KEYWORDS)
)

# Flag midnight queries (00:00 - 04:00)
df['is_midnight'] = df['hour'].between(0,4)

# --- Step 2: Agregate features per user ---
user_features = df.groupby('user_id').agg(
    query_count=('user_id', 'count'),
    avg_response_length=('response_length', 'mean'),
    cbrn_ratio=('is_cbrn', 'mean'),
    midnight_ratio=('is_midnight', 'mean')
).reset_index()

print("User features sample:")
print(user_features.head(10).to_string(index=False))

# --- Step 3: Compute correlation matrix ---
numeric_features = user_features[['query_count', 'avg_response_length', 'cbrn_ratio', 'midnight_ratio']]
corr_matrix = numeric_features.corr()

print("\nCorrelation matrix:")
print(corr_matrix.round(3).to_string())

# --- Step 4: Identify strongest correlations ---
print("\nStrongest correlations (excluding self-correlation):")
corr_pairs = []
cols = corr_matrix.columns
for i in range(len(cols)):
    for j in range(i+1, len(cols)):
        corr_pairs.append({
            'variable1': cols[i],
            'variable2': cols[j],
            'correlation': corr_matrix.iloc[i, j]
        })

corr_df = pd.DataFrame(corr_pairs).sort_values('correlation', key=abs, ascending=False)
print(corr_df.to_string(index=False))

# --- Step 5: Heatmap visualization ---
plt.figure(figsize=(8,6))
plt.imshow(corr_matrix, cmap='coolwarm', vmin=-1, vmax=1)
plt.colorbar(label='Correlation coefficient')
plt.xticks(range(len(corr_matrix.columns)), corr_matrix.columns, rotation=45, ha='right')
plt.yticks(range(len(corr_matrix.columns)), corr_matrix.columns)

# Add correlation values as text on the heatmap
for i in range(len(corr_matrix.columns)):
    for j in range(len(corr_matrix.columns)):
        plt.text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',
                 ha='center', va='center', fontsize=12,
                 color='white' if abs(corr_matrix.iloc[i, j]) > 0.5 else 'black')
        
plt.title('Feature Correlation Matrix')
plt.tight_layout()
plt.savefig('outputs/week9_day3_correlation_heatmap.png')
plt.show()
print("\nChart saved to outputs/week9_day3_correlation_heatmap.png")

# --- Step 6: Scatter plot - query count vs response length ---
plt.figure(figsize=(8, 6))
plt.scatter(user_features['query_count'], user_features['avg_response_length'], alpha=0.5, color='steelblue')
plt.xlabel('Query Count')
plt.ylabel('Average Response Length')
plt.title('Query Count vs Average Response Length')
plt.tight_layout()
plt.savefig('outputs/week9_day3_scatter.png')
plt.show()
print("Scatter plot saved to outputs/week9_day3_scatter.png")