import yaml
from extract.fishbase_extract import export_parquet_to_csv
from transform.transform_utils import normalize_dataframe
from load.neo4j_loader import Neo4jLoader
import pandas as pd

# --- Config ---
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "password",
    "database": "fishbase"
}

NEO4J_CONFIG = {
    "uri": "bolt://localhost:7687",
    "user": "neo4j",
    "password": "password"
}

with open("config/fishbase.yaml") as f:
    fishbase = yaml.safe_load(f)

# --- Extract ---
for table_name, table_info in fishbase['tables'].items():
    # Extracting table-specific info
    csv_path = f"data/{table_name}.csv"
    
    # Get columns for this specific table
    columns = table_info.get('columns', None)  # Use 'None' as default if no columns are provided

    # Export parquet to CSV with the correct columns for each table
    export_parquet_to_csv(f"{table_name}.parquet", csv_path, "./input/fishbase", columns)

# --- Transform ---
# Apply fishbase filters (aquarium-only)

# --- Load ---
loader = Neo4jLoader(**NEO4J_CONFIG)

for table_name, table_conf in mappings['tables'].items():
    if 'properties' in table_conf:
        df = pd.read_csv(f"data/{table_name}.csv")
        df = normalize_dataframe(df)
        for _, row in df.iterrows():
            props = {k: row[k] for k in table_conf['properties']}
            loader.create_node(table_conf['label'], props)
    if 'relationships' in table_conf:
        for rel in table_conf['relationships']:
            rel_df = pd.read_csv(f"data/{rel.get('source_table', table_name)}.csv")
            for _, row in rel_df.iterrows():
                loader.create_relationship(
                    source_label=table_conf.get('label', 'Species'),
                    source_key=rel['source_key'],
                    source_val=row[rel['source_key']],
                    target_label=rel['target'],
                    target_key=rel['target_key'],
                    target_val=row[rel['target_key']],
                    rel_type=rel['type']
                )

loader.close()
print("ETL completed successfully!")
