# config.py
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DATA_PATH = os.path.join(BASE_DIR, 'data', 'raw', 'RAW_recipes.csv')
PROCESSED_DATA_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'recipes_clean.csv')

TOP_N_RESULTS = 300        # Return all matching recipes (was 10 — too restrictive)
MAX_COOKING_TIME = 300      # Default max cooking time cap (minutes)
TFIDF_MAX_FEATURES = 5000   # Vocabulary size cap for TF-IDF vectoriser
MIN_INGREDIENT_LENGTH = 2   # Reject inputs shorter than this
MAX_INPUT_INGREDIENTS = 20  # Reject inputs with more items than this

# Dietary tag mappings from SRS tags field
DIETARY_TAGS = {
    'vegetarian': ['vegetarian'],
    'vegan': ['vegan'],
    'gluten-free': ['gluten-free', 'gluten free'],
    'low-carb': ['low-carb', 'low carb', 'keto'],
}
