# modules/preprocessor.py
import re
import pandas as pd

STOP_WORDS = {
    'and', 'or', 'with', 'a', 'an', 'the', 'of', 'to', 'in', 'for',
    'into', 'by', 'at', 'on', 'as', 'is', 'are', 'be', 'been',
    # Cooking verbs / instruction words
    'chopped', 'sliced', 'diced', 'minced', 'grated', 'crushed',
    'beaten', 'divided', 'melted', 'softened', 'peeled', 'deveined',
    'trimmed', 'halved', 'quartered', 'shredded', 'julienned',
    'blanched', 'soaked', 'rinsed', 'drained', 'thawed', 'frozen',
    'cooked', 'raw', 'dried', 'fresh', 'canned', 'packed', 'whole',
    'large', 'medium', 'small', 'extra', 'thick', 'thin', 'fine',
    'finely', 'roughly', 'coarsely', 'thinly', 'generously',
    # Units / quantities (words, not just numbers)
    'cup', 'cups', 'tbsp', 'tsp', 'tablespoon', 'tablespoons',
    'teaspoon', 'teaspoons', 'kg', 'grams', 'gram', 'g', 'lb', 'lbs',
    'oz', 'ounce', 'ounces', 'litre', 'litres', 'ml', 'liter',
    'piece', 'pieces', 'handful', 'bunch', 'head', 'clove', 'cloves',
    'can', 'jar', 'packet', 'pinch', 'dash', 'sprig', 'sprigs',
    'stick', 'sticks', 'slice', 'slices', 'strip', 'strips',
    'inch', 'inches', 'cm', 'block', 'blocks', 'fillet', 'fillets',
    'bone', 'cut', 'cubed', 'chunk', 'chunks', 'julienne', 'round',
    'to', 'taste', 'optional', 'needed', 'about', 'approximately',
}


def clean_ingredient(text: str) -> str:
    """
    Extract meaningful ingredient keywords from a full cooking description.

    Input:  '500g mutton on bone, cut into pieces'
    Output: 'mutton'

    Input:  '2 large eggs, beaten'
    Output: 'eggs'

    Input:  '1 tbsp ginger garlic paste'
    Output: 'ginger garlic paste'
    """
    text = text.lower()
    # Remove quantities with units: '500g', '1/2 cup'
    text = re.sub(r'\b\d+[\./]?\d*\s*(?:g|kg|ml|l|lb|oz|cups?|tbsp?|tsp?|tablespoons?|teaspoons?)\b', '', text)
    # Remove unitless numbers
    text = re.sub(r'\b\d+[\./]?\d*\b', '', text)
    # Remove bracketed extras like '(optional)', '(about 400ml)'
    text = re.sub(r'\(.*?\)', '', text)
    # Remove everything after a comma → strips instructions like ", cut into pieces"
    text = text.split(',')[0]
    # Remove non-alpha characters
    text = re.sub(r'[^a-z\s]', ' ', text)
    
    # Simple plural to singular mapping
    plurals = {
        'eggs': 'egg', 'crabs': 'crab', 'prawns': 'prawn', 'shrimps': 'shrimp',
        'tomatoes': 'tomato', 'potatoes': 'potato', 'onions': 'onion',
        'chillies': 'chili', 'chilies': 'chili', 'leaves': 'leaf',
        'mushrooms': 'mushroom', 'carrots': 'carrot', 'noodles': 'noodle'
    }
    
    # Tokenize, filter stop words, and singularize
    tokens = []
    for w in text.split():
        w = plurals.get(w, w)
        # generic naive 's' stripping
        if w.endswith('s') and len(w) > 3 and not w.endswith('ss') and w != 'asparagus':
            w = w[:-1]
        if w not in STOP_WORDS and len(w) > 1:
            tokens.append(w)
            
    return ' '.join(tokens)


def build_ingredient_text(ingredient_list: list) -> str:
    """Join cleaned ingredients into a single space-separated string."""
    if not isinstance(ingredient_list, list):
        return ''
    return ' '.join(clean_ingredient(str(i)) for i in ingredient_list if i)


def preprocess_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Add ingredient_text column used by the TF-IDF engine."""
    df = df.copy()

    def combine_name_ingredients(row):
        # Clean the name just like an ingredient to get meaningful keywords
        name_cleaned = clean_ingredient(str(row['name']))
        # Clean the ingredients list
        ingreds_cleaned = build_ingredient_text(row['ingredients'])
        # Combine both, ensuring no leading/trailing whitespace
        return f"{name_cleaned} {ingreds_cleaned}".strip()

    df['ingredient_text'] = df.apply(combine_name_ingredients, axis=1)
    return df


def preprocess_user_input(raw_input: str) -> str:
    """Process comma-separated user ingredient string into cleaned text."""
    items = [i.strip() for i in raw_input.split(',') if i.strip()]
    return ' '.join(clean_ingredient(i) for i in items)
