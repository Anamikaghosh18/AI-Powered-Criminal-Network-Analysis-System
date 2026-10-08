import pandas as pd
import argparse

def inspect_dataset(file_path, num_rows=100000):
    print(f"Inspecting {file_path}...")
    
    # Read a sample to avoid memory issues if the file is massive
    # but still enough to infer data types
    df = pd.read_csv(file_path, nrows=num_rows)
    
    print(f"\n--- Dataset Info (Sample {num_rows} rows) ---")
    print(f"Number of columns: {len(df.columns)}")
    print("Columns:", list(df.columns))
    
    print("\n--- Data Types ---")
    print(df.dtypes)
    
    print("\n--- Missing Values ---")
    print(df.isnull().sum())
    
    print("\n--- Unique Values (Categorical) ---")
    categorical_cols = df.select_dtypes(include=['object', 'bool']).columns
    for col in categorical_cols:
        print(f"{col}: {df[col].nunique()} unique values")
        
    print("\n--- First 5 Rows ---")
    print(df.head())
    
    print("\n--- Checking for potential duplicates ---")
    # Assuming 'ID' or 'Case Number' might be present
    if 'ID' in df.columns:
        dups = df['ID'].duplicated().sum()
        print(f"Duplicate IDs in sample: {dups}")
    if 'Case Number' in df.columns:
        dups = df['Case Number'].duplicated().sum()
        print(f"Duplicate Case Numbers in sample: {dups}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Inspect Chicago Crimes dataset")
    parser.add_argument("--file", type=str, default="data/raw/chicago_crimes.csv", help="Path to the CSV file")
    args = parser.parse_args()
    
    inspect_dataset(args.file)
