import pandas as pd
import ast
import os
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(r'c:\Users\RITAJA\Downloads\ChefLogic')
PROCESSED_DATA_PATH = PROJECT_ROOT / 'data' / 'processed' / 'recipes_clean.csv'

def _safe_parse_list(val):
    try:
        if isinstance(val, float): return []
        return ast.literal_eval(val) if isinstance(val, str) else val
    except: return []

def categorize_recipes():
    print(f"Loading {PROCESSED_DATA_PATH}...")
    df = pd.read_csv(PROCESSED_DATA_PATH)
    df['tags'] = df['tags'].apply(_safe_parse_list)
    df['ingredients_parsed'] = df['ingredients'].apply(_safe_parse_list)

    # Classification logic
    MEAT_KEYWORDS = ['chicken', 'beef', 'lamb', 'mutton', 'pork', 'fish', 'seafood',
                     'shrimp', 'prawn', 'crab', 'lobster', 'duck', 'turkey', 'meat', 'steak', 'bacon']
    
    DESSERT_KEYWORDS = ['cake', 'chocolate', 'dessert', 'sweet', 'cookie', 'brownie', 
                        'ice cream', 'pudding', 'pastry', 'halwa', 'gulab jamun', 
                        'rasgulla', 'mochi', 'kheer', 'tiramisu', 'tart', 'custard', 'mousse', 'donut', 'pie']
    
    BEVERAGE_KEYWORDS = ['coffee', 'tea', 'juice', 'shake', 'smoothie', 'mocktail', 
                         'drink', 'latte', 'espresso', 'cappuccino', 'frappe', 'lemonade', 'cooler']

    def get_category(row):
        name = str(row['name']).lower()
        tags = [str(t).lower() for t in row['tags']]
        ingreds = str(row.get('ingredients', '')).lower()
        
        # 1. Check for Beverages (highest priority)
        if any(kw in name or kw in tags for kw in BEVERAGE_KEYWORDS):
            return 'category:beverage'
        
        # 2. Check for Desserts
        # If it has a dessert keyword AND NO meat keyword, it's a dessert
        if any(kw in name or kw in tags for kw in DESSERT_KEYWORDS):
            if not any(mk in name or mk in ingreds for mk in MEAT_KEYWORDS):
                return 'category:dessert'
        
        # 3. Check for Starters/Snacks
        STARTER_KEYWORDS = ['taco', 'kebab', 'snack', 'momo', 'bao', 'spring roll', 'samosa', 'pakora', 'appetizer', 'starter']
        if any(kw in name or kw in tags for kw in STARTER_KEYWORDS):
            return 'category:starter'
            
        # 4. Default to Main
        return 'category:main'

    print("Categorizing recipes...")
    df['category_tag'] = df.apply(get_category, axis=1)
    
    # Append the category tag to the tags list
    def update_tags(row):
        tags = row['tags']
        # Remove any existing category tags to prevent duplicates
        tags = [t for t in tags if not str(t).startswith('category:')]
        tags.append(row['category_tag'])
        return tags

    df['tags'] = df.apply(update_tags, axis=1)
    
    # Cleanup and save
    df_save = df.drop(columns=['category_tag', 'ingredients_parsed'])
    # Convert tags back to stringified list for CSV
    df_save['tags'] = df_save['tags'].apply(lambda x: str(x).replace('"', "'"))
    
    df_save.to_csv(PROCESSED_DATA_PATH, index=False)
    print(f"Successfully categorized {len(df_save)} recipes.")
    
    # Summary of counts
    counts = df['category_tag'].value_counts()
    print("\nCategorization Summary:")
    print(counts)

if __name__ == "__main__":
    categorize_recipes()
