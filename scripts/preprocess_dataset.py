# scripts/preprocess_dataset.py
"""
Offline preprocessing script — run once locally or in Render build step.
Reads RAW_recipes.csv → cleans → writes recipes_clean.csv.

Usage:
    python scripts/preprocess_dataset.py
"""
import sys
import os

# Allow importing config from project root when running as a script
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
from config import RAW_DATA_PATH, PROCESSED_DATA_PATH

REQUIRED_COLS = ['id', 'name', 'ingredients', 'steps', 'minutes', 'tags']
OPTIONAL_COLS = ['nutrition']


def main():
    if not os.path.exists(RAW_DATA_PATH):
        print(f'ERROR: Raw dataset not found at {RAW_DATA_PATH}')
        print('Please download RAW_recipes.csv from:')
        print('  https://www.kaggle.com/datasets/shuyangli94/food-com-recipes-and-user-interactions')
        print(f'and place it at: {RAW_DATA_PATH}')
        sys.exit(1)

    print(f'Loading {RAW_DATA_PATH} ...')
    df = pd.read_csv(RAW_DATA_PATH)
    print(f'  Raw rows: {len(df)}')

    # Keep only required + optional columns that exist
    keep_cols = REQUIRED_COLS + [c for c in OPTIONAL_COLS if c in df.columns]
    df = df[[c for c in keep_cols if c in df.columns]]

    # Drop rows with missing critical fields
    df = df.dropna(subset=['name', 'ingredients', 'steps'])

    # Remove recipes with unrealistic cooking times (>720 min = 12 hours)
    df = df[df['minutes'] <= 720]

    # Remove recipes with 0 or negative cooking times
    df = df[df['minutes'] > 0]

    # Ensure id column is integer
    df['id'] = df['id'].astype(int)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(PROCESSED_DATA_PATH), exist_ok=True)
    df.to_csv(PROCESSED_DATA_PATH, index=False)
    print(f'Saved {len(df)} recipes to {PROCESSED_DATA_PATH}')


if __name__ == '__main__':
    main()
