# modules/data_loader.py
import pandas as pd
import ast
from config import PROCESSED_DATA_PATH

REQUIRED_COLUMNS = ['id', 'name', 'ingredients', 'steps', 'minutes', 'tags']


def load_recipes() -> pd.DataFrame:
    """Load processed CSV into a DataFrame, validate schema, parse list columns."""
    df = pd.read_csv(PROCESSED_DATA_PATH)
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f'Dataset missing columns: {missing}')
    # Parse Python-style list strings (e.g. "['egg', 'milk']")
    for col in ['ingredients', 'steps', 'tags']:
        df[col] = df[col].apply(_safe_parse_list)
    return df


def _safe_parse_list(val):
    """Safely parse a Python-literal list string; return [] on failure or NaN."""
    try:
        if isinstance(val, float):   # catches float('nan') from missing CSV cells
            return []
        return ast.literal_eval(val) if isinstance(val, str) else val
    except Exception:
        return []

