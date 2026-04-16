import pandas as pd

# Try different encodings
for encoding in ['latin-1', 'iso-8859-1', 'cp1252']:
    try:
        df = pd.read_csv("capstone_logs.csv", encoding=encoding)
        print(f"Success with encoding: {encoding}")
        print(f"Loaded {len(df)} rows")
        print(f"Columns: {df.columns.tolist()}")
        print(df.head())
        
        # Resave as clean UTF-8
        df.to_csv("capstone_logs_clean.csv", index=False, encoding='utf-8')
        print("Clean file saved as capstone_logs_clean.csv")
        break
    except Exception as e:
        print(f"Failed with {encoding}: {e}")