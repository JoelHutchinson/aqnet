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
    """
    Filter for rows with Aquarium column set to 'commercial' or 'highly commercial'.
    """
    allowed_values = ['commercial', 'highly commercial']
    filtered_df = df[df['Aquarium'].isin(allowed_values)]
    return filtered_df
