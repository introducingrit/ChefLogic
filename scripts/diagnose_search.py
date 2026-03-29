import sys
import os
from pathlib import Path
import pandas as pd

# Add project root to sys.path
PROJECT_ROOT = Path(r'c:\Users\RITAJA\Downloads\ChefLogic')
sys.path.insert(0, str(PROJECT_ROOT))

from modules.data_loader import load_recipes
from modules.preprocessor import preprocess_dataframe
from modules.recommender import MOOD_MAP

def test_sweet_mood():
    print("Loading data...")
    df = load_recipes()
    df = preprocess_dataframe(df)
    
    mood_key = 'sweet'
    mood = MOOD_MAP[mood_key]
    keywords = mood['keywords']
    
    MEAT_KEYWORDS = ['chicken', 'beef', 'lamb', 'mutton', 'pork', 'fish', 'seafood',
                     'shrimp', 'prawn', 'crab', 'lobster', 'duck', 'turkey', 'meat', 'steak']

    problematic_dishes = [
        "Restaurant Style Butter Chicken",
        "Authentic Pad Thai",
        "Paneer Butter Masala",
        "Classic Chicken Tikka Masala",
        "Beef Burger With Caramelised Onions",
        "Sweet And Sour Pork",
        "Crab Cakes",
        "Steak Tartare",
        "Honey Walnut Shrimp"
    ]

    def score_row(row):
        name = str(row.get('name', '')).lower()
        ingreds = str(row.get('ingredient_text', '')).lower()
        haystack = f"{name} {ingreds}"
        haystack_words = haystack.replace(',', ' ').replace('.', ' ').split()
        
        # Meat check
        has_meat = any(mk in haystack for mk in MEAT_KEYWORDS)
        
        score = sum(1 for kw in keywords if kw.lower() in haystack_words or f" {kw.lower()} " in f" {haystack} ")
        
        # Result to return for debugging
        return score, has_meat, haystack

    print(f"\nEvaluating mood: {mood_key}")
    print(f"{'Dish Name':<40} | {'Score':<5} | {'Has Meat':<8} | {'Matches'}")
    print("-" * 80)
    
    for dish in problematic_dishes:
        match = df[df['name'].str.lower() == dish.lower()]
        if match.empty:
            print(f"{dish:<40} | NOT FOUND")
            continue
        
        row = match.iloc[0]
        score, has_meat, haystack = score_row(row)
        
        matches = [kw for kw in keywords if kw.lower() in haystack]
        print(f"{dish:<40} | {score:<5} | {has_meat:<8} | {matches}")

test_sweet_mood()
