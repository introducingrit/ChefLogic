import sys
import os
from pathlib import Path
import pandas as pd

# Add project root to sys.path
PROJECT_ROOT = Path(r'c:\Users\RITAJA\Downloads\ChefLogic')
sys.path.insert(0, str(PROJECT_ROOT))

# Manual initialization of Recommender
from modules.recommender import Recommender

def test_global_search_consistency():
    print("--- Testing Global Search Consistency ---")
    
    recommender = Recommender()
    recommender.load()
    
    # 1. Test Dish Name Search for "dessert"
    print("\nTesting Dish Name Search: 'dessert'")
    results = recommender.search_by_name("dessert")
    found_savory = [r['name'] for r in results if any(mk in r['name'].lower() for mk in ['chicken', 'beef', 'pork', 'fish'])]
    if found_savory:
        print(f"FAILED: Found savory dishes in dessert name search: {found_savory}")
    else:
        print(f"PASSED: No savory dishes found in dessert name search. Count: {len(results)}")

    # 2. Test Ingredient Search for "chocolate"
    print("\nTesting Ingredient Search: 'chocolate'")
    results = recommender.recommend("chocolate")
    found_savory = [r['name'] for r in results if any(mk in r['name'].lower() for mk in ['chicken', 'beef', 'pork', 'fish'])]
    if found_savory:
        print(f"FAILED: Found savory dishes in chocolate ingredient search: {found_savory}")
    else:
        print(f"PASSED: No savory dishes found in chocolate ingredient search. Count: {len(results)}")

    # 3. Test Dish Name Search for "sweet"
    print("\nTesting Dish Name Search: 'sweet'")
    results = recommender.search_by_name("sweet")
    is_sp_present = any("sweet and sour pork" in r['name'].lower() for r in results)
    if is_sp_present:
        print("FAILED: Found 'Sweet and Sour Pork' in sweet name search.")
    else:
        print(f"PASSED: 'Sweet and Sour Pork' excluded. Count: {len(results)}")

    # 4. Test Mood Search for "sweet"
    print("\nTesting Mood Search: 'sweet'")
    results = recommender.search_by_mood("sweet")
    found_savory = [r['name'] for r in results if any(mk in r['name'].lower() for mk in ['chicken', 'beef', 'pork', 'fish'])]
    if found_savory:
        print(f"FAILED: Found savory dishes in sweet mood search: {found_savory}")
    else:
        print(f"PASSED: No savory dishes found in sweet mood search. Count: {len(results)}")

if __name__ == "__main__":
    test_global_search_consistency()
