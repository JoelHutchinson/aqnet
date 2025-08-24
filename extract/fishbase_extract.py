import pandas as pd
import mysql.connector

def export_table_to_csv(table_name, output_path, db_config):
    """Export a MySQL table to CSV."""
    conn = mysql.connector.connect(**db_config)
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, conn)
    df.to_csv(output_path, index=False)
    conn.close()
    print(f"Exported {table_name} to {output_path}")
