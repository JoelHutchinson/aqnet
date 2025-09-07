import os
from dotenv import load_dotenv
import yaml
from extract.fishbase_extract import export_parquet_to_csv
from transform.transform_utils import normalize_dataframe
from load.neo4j_loader import Neo4jLoader
import pandas as pd

# --- Load .env ---
load_dotenv()  # this loads the environment variables from .env

NEO4J_CONFIG = {
    "uri": os.getenv("NEO4J_URI"),
    "user": os.getenv("NEO4J_USER"),
    "password": os.getenv("NEO4J_PASSWORD")
}

# --- Load FishBase config ---
with open("config/fishbase.yaml") as f:
    fishbase = yaml.safe_load(f)

# --- Utility: filter aquarium species ---
def apply_filters(df):
    allowed_values = ['commercial', 'highly commercial']
    return df[df['Aquarium'].str.strip().isin(allowed_values)]

# --- Extract, Transform & Load (same as before) ---
for table_name, table_info in fishbase['tables'].items():
    # Extract
    csv_path = f"data/{table_name}.csv"
    columns = table_info.get('columns', None)
    export_parquet_to_csv(f"{table_name}.parquet", csv_path, "./input/fishbase", columns)

    # Transform & filter
    df = pd.read_csv(csv_path)
    df = normalize_dataframe(df)
    if 'Aquarium' in df.columns:
        df = apply_filters(df)
    df.to_csv(csv_path, index=False)

# Load into Neo4j
loader = Neo4jLoader(**NEO4J_CONFIG)
for table_name, table_conf in fishbase['tables'].items():
    df = pd.read_csv(f"data/{table_name}.csv")
    
    if 'properties' in table_conf:
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
