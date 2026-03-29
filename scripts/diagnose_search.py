import sys
import os
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(r'c:\Users\RITAJA\Downloads\ChefLogic')
sys.path.insert(0, str(PROJECT_ROOT))

from modules.recommender import Recommender

def test_strict_ingredient_search():
    print("--- Testing Strict Ingredient Search ---")
    
    recommender = Recommender()
    recommender.load()
    
    # Test 1: Search for "noodle"
    print("\nTesting Ingredient Search: 'noodle'")
    results = recommender.recommend("noodle")
    print(f"Found {len(results)} dishes.")
    for r in results[:5]:
        text = str(r.get('ingredient_text', '')) + " " + str(r.get('steps', '')).lower()
        if 'noodle' not in text.lower():
            print(f"FAILED: 'noodle' missing from recipe: {r['name']}")
        else:
            print(f"PASSED Recipe: {r['name']}")

    # Test 2: Search for "chocolate, cake"
    print("\nTesting Ingredient Search: 'chocolate, cake'")
    results = recommender.recommend("chocolate, cake")
    print(f"Found {len(results)} dishes.")
    for r in results[:5]:
        text = str(r.get('ingredient_text', '')) + " " + str(r.get('steps', '')).lower()
        if 'chocolate' not in text.lower() or 'cake' not in text.lower():
            print(f"FAILED: 'chocolate' or 'cake' missing from recipe: {r['name']}")
        else:
            print(f"PASSED Recipe: {r['name']}")

if __name__ == "__main__":
    test_strict_ingredient_search()
