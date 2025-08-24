import pandas as pd

def normalize_dataframe(df):
    """
    Apply any transformations needed before loading to Neo4j.
    E.g., convert numeric columns, strip strings, etc.
    """
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.strip()
    return df

def apply_filters(df):
    # Bish