import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime

def run_eda(file_path):
    """Run full EDA on a CSV or Excel file"""
    
    if not os.path.exists(file_path):
        print(f"ERROR: File not found: {file_path}")
        return
    
    output_dir = "D:/stage1/output"
    os.makedirs(output_dir, exist_ok=True)
    output_name = os.path.splitext(os.path.basename(file_path))[0]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"{output_dir}/{output_name}_EDA_{timestamp}.xlsx"
    
    # Read file
    if file_path.endswith('.csv'):
        df = pd.read_csv(file_path)
    else:
        df = pd.read_excel(file_path)
    
    # Remove fully empty columns and unnamed columns
    df = df.dropna(axis=1, how='all')
    df = df.loc[:, ~df.columns.str.contains('^Unnamed', case=False)]
    
    print(f"File loaded: {df.shape[0]} rows x {df.shape[1]} columns")
    print(f"Columns: {list(df.columns)}")
    print()
    
    # Column info
    print("=== COLUMN INFO ===")
    for col in df.columns:
        dtype = df[col].dtype
        missing = df[col].isnull().sum()
        unique = df[col].nunique()
        print(f"  {col}: type={dtype}, missing={missing}, unique={unique}")
    
    print(f"\nTotal missing values: {df.isnull().sum().sum()}")
    print(f"Duplicate rows: {df.duplicated().sum()}")
    
    # Numeric stats
    num_cols = df.select_dtypes(include=[np.number]).columns
    if len(num_cols) > 0:
        print("\n=== NUMERIC STATISTICS ===")
        print(df[num_cols].describe().round(2))
    
    # Categorical top values
    cat_cols = df.select_dtypes(include=['object']).columns
    if len(cat_cols) > 0:
        print("\n=== TOP CATEGORIES ===")
        for col in cat_cols[:5]:
            print(f"  {col}:")
            print(df[col].value_counts().head(5).to_string())
            print()
    
    # Write Excel
    try:
        with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Original', index=False)
            
            info = pd.DataFrame({
                'Column': df.columns,
                'Type': df.dtypes.astype(str).values,
                'Missing': df.isnull().sum().values,
                'Missing_%': (df.isnull().sum()/len(df)*100).round(2).values,
                'Unique': df.nunique().values
            })
            info.to_excel(writer, sheet_name='Info', index=False)
            
            if len(num_cols) > 0:
                df[num_cols].describe().to_excel(writer, sheet_name='Statistics')
            
            # Cleaned data
            cleaned = df.copy()
            for col in cleaned.columns:
                if pd.api.types.is_numeric_dtype(cleaned[col]):
                    cleaned[col] = cleaned[col].fillna(cleaned[col].median())
                else:
                    cleaned[col] = cleaned[col].fillna('MISSING')
            cleaned = cleaned.drop_duplicates()
            cleaned.to_excel(writer, sheet_name='Cleaned', index=False)
            
            # Summary
            summary = pd.DataFrame({
                'Metric': ['Rows', 'Columns', 'Missing', 'Duplicates', 'Numeric Cols', 'Text Cols'],
                'Value': [len(df), len(df.columns), df.isnull().sum().sum(), df.duplicated().sum(), len(num_cols), len(cat_cols)]
            })
            summary.to_excel(writer, sheet_name='Summary', index=False)
            
            # Top values
            for col in cat_cols[:5]:
                safe_name = col[:25].replace('/', '_').replace('\\', '_')
                df[col].value_counts().head(15).to_excel(writer, sheet_name=f'{safe_name}_Top15')
        
        print(f"\nSUCCESS! Output saved to: {output_path}")
        return output_path
    except PermissionError:
        # Try with a different name
        output_path = f"{output_dir}/{output_name}_EDA_{timestamp}_v2.xlsx"
        with pd.ExcelWriter(output_path, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Original', index=False)
        print(f"\nSUCCESS! Output saved to: {output_path}")
        return output_path

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_eda(sys.argv[1])
    else:
        print("Usage: python data_tool.py <file_path>")