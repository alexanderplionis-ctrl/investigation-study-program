# ---- PANDAS CHEATSHEET ----

# Load CSV
df = pd.read_csv("file.csv")

# Basic exploration
df.shape
df.columns.tolist()
df.head()
df.dtypes
df.describe()

# Filter rows
df[df["column"] > value]
df[(df["col1"] > val1) & (df["col2"] == val2)]

# Add calculated column
df["new_col"] = df["col1"] / df["col2"]

# Sort
df.sort_values("column", ascending=False)

# Group by
df.groupby("column").mean()

# Save to CSV
df.to_csv("output.csv", index=False)

# ---- DATETIME ----
from datetime import datetime, timedelta
now = datetime.now()
logs["timestamp"] = pd.to_datetime(logs["timestamp"])
logs["hour"] = logs["timestamp"].dt.hour

# ---- MATPLOTLIB ----
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 6))
plt.bar(df["x_col"], df["y_col"])
plt.title("Title")
plt.savefig("chart.png")
plt.show()