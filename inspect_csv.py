import pandas as pd
import sys

try:
    # Try reading with skipping first 2 rows (header at index 2)
    df = pd.read_csv('/Users/aoyamahiroki/Desktop/field_analysis/question.csv', encoding='shift_jis', header=2)
    print("Columns:", df.columns.tolist())
    print("\nFirst 5 rows:")
    print(df.head().to_string())
except Exception as e:
    print(f"Error with shift_jis: {e}")
    try:
        df = pd.read_csv('/Users/aoyamahiroki/Desktop/field_analysis/question.csv', encoding='cp932', header=2) 
        print("Columns:", df.columns.tolist())
        print("\nFirst 5 rows:")
        print(df.head().to_string())
    except Exception as e2:
         print(f"Error with cp932: {e2}")
