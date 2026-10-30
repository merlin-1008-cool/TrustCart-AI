import pandas as pd
from pathlib import Path

# Locate the project folder
project_root = Path(__file__).resolve().parent.parent

# Load seller dataset
file_path = project_root / "data" / "raw" / "seller_data.csv"
df = pd.read_csv(file_path)

# Display dataset information
print("Dataset loaded successfully!")
print("-" * 40)
print("Total rows:", len(df))
print("Total columns:", len(df.columns))
print("\nColumn names:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())