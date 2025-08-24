import pandas as pd
import mysql.connector
from pathlib import Path

def export_table_to_csv(table_name, output_path, db_config):
    """Export a MySQL table to CSV."""
    conn = mysql.connector.connect(**db_config)
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, conn)
    df.to_csv(output_path, index=False)
    conn.close()
    print(f"Exported {table_name} to {output_path}")

def export_parquet_to_csv(parquet_filename, output_path, base_dir="./input/fishbase", columns=None):
    """
    Export a parquet file (from ./data/fishbase) to CSV, with optional column filtering.
    
    Args:
        parquet_filename (str): Name of the parquet file (e.g. 'species.parquet')
        output_path (str): Destination path for CSV
        base_dir (str): Base directory containing parquet files
        columns (list, optional): List of columns to include from the parquet file. 
                                  If None, all columns are included.
    """
    parquet_path = Path(base_dir) / parquet_filename
    if not parquet_path.exists():
        raise FileNotFoundError(f"Parquet file not found: {parquet_path}")
    
    # Read only specific columns if 'columns' is provided, otherwise read all columns
    df = pd.read_parquet(parquet_path, columns=columns)
    
    # Export to CSV
    df.to_csv(output_path, index=False)
    print(f"Exported {parquet_path} to {output_path}")