# modules/substitution.py
"""
Ingredient substitution suggestions.
Uses a static lookup dictionary covering 25+ common ingredients.
"""

SUBSTITUTION_MAP = {
    'mutton': ['lamb', 'goat meat', 'beef'],
    'lamb': ['mutton', 'goat meat', 'beef'],
    'goat': ['mutton', 'lamb'],
    'butter': ['margarine', 'coconut oil', 'olive oil'],
    'milk': ['almond milk', 'oat milk', 'soy milk', 'coconut milk'],
    'egg': ['flax egg', 'chia egg', 'applesauce'],
    'flour': ['almond flour', 'oat flour', 'rice flour', 'chickpea flour'],
    'sugar': ['honey', 'maple syrup', 'coconut sugar'],
    'cream': ['coconut cream', 'cashew cream', 'yogurt'],
    'sour cream': ['greek yogurt', 'coconut cream'],
    'beef': ['mushroom', 'lentils', 'jackfruit', 'lamb', 'mutton'],
    'chicken': ['tofu', 'tempeh', 'chickpeas', 'turkey'],
    'pork': ['turkey', 'beef', 'tofu'],
    'prawn': ['shrimp', 'scallop', 'fish'],
    'shrimp': ['prawn', 'scallop', 'fish'],
    'lard': ['vegetable shortening', 'coconut oil'],
    'honey': ['maple syrup', 'agave nectar', 'sugar'],
    'bread crumbs': ['oat crumbs', 'almond meal', 'crushed crackers', 'panko'],
    'oil': ['applesauce', 'greek yogurt', 'avocado'],
    'bacon': ['tempeh bacon', 'mushroom bacon', 'smoked tofu'],
    'cheese': ['nutritional yeast', 'cashew cheese', 'vegan cheese'],
    'paneer': ['tofu', 'halloumi', 'farmer\'s cheese'],
    'yogurt': ['sour cream', 'coconut yogurt', 'cashew cream'],
    'ghee': ['clarified butter', 'coconut oil', 'butter'],
    'coconut milk': ['cream', 'oat milk', 'cashew cream'],
    'fish sauce': ['soy sauce', 'tamari', 'worcestershire sauce'],
    'soy sauce': ['tamari', 'coconut aminos', 'fish sauce'],
    'tahini': ['peanut butter', 'almond butter', 'cashew butter'],
    'parmesan': ['pecorino romano', 'nutritional yeast', 'grana padano'],
    'mozzarella': ['provolone', 'monterey jack', 'vegan mozzarella'],
    'anchovy': ['capers', 'miso paste', 'fish sauce'],
    'rice': ['quinoa', 'cauliflower rice', 'barley'],
    'pasta': ['zucchini noodles', 'rice noodles', 'spaghetti squash'],
    'breadcrumb': ['oat crumbs', 'almond meal', 'crushed crackers'],
}


def get_substitutions(ingredients: list) -> dict:
    """Return substitution suggestions for any matched ingredients."""
    result = {}
    for ingredient in ingredients:
        key = ingredient.lower().strip()
        for base, subs in SUBSTITUTION_MAP.items():
            if base in key:
                result[ingredient] = subs
                break
    return result
