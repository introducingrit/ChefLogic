import os
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from modules.data_loader import load_recipes
from modules.preprocessor import preprocess_dataframe, preprocess_user_input
from modules.tfidf_engine import TFIDFEngine
from modules.filter_engine import apply_filters
from config import TOP_N_RESULTS

# Minimum score to consider a match meaningful
MIN_SCORE_THRESHOLD = 0.01

# ── Mood → keyword/tag mapping ────────────────────────────────────────────────
MOOD_MAP = {
    'spicy': {
        'emoji': '🌶️', 'label': 'Spicy & Bold',
        'keywords': ['chili', 'spicy', 'hot', 'jalapeño', 'sriracha', 'gochujang',
                     'vindaloo', 'szechuan', 'sichuan', 'peppers', 'chipotle', 'harissa',
                     'biryani', 'curry', 'rogan josh', 'nihari', 'korma'],
        'description': 'Fiery dishes that pack a punch!',
    },
    'sweet': {
        'emoji': '🍰', 'label': 'Sweets & Desserts',
        'keywords': ['dessert', 'chocolate', 'cake', 'sugar', 'pastry',
                     'cookie', 'brownie', 'ice cream', 'tiramisu', 'pudding', 'halwa',
                     'gulab', 'ladoo', 'barfi', 'tart', 'mousse', 'cheesecake',
                     'fudge', 'caramel', 'maple', 'waffle', 'pancake', 'custard',
                     'muffin', 'donut', 'pie', 'sorbet', 'baklava', 'syrup',
                     'mochi', 'rasgulla', 'gulab jamun', 'kheer', 'shrikhand', 'sweet'],
        'description': 'Indulge your sweet tooth!',
    },
    'comfort': {
        'emoji': '🍲', 'label': 'Comfort Food',
        'keywords': ['curry', 'stew', 'soup', 'casserole', 'pie', 'mash', 'gravy',
                     'biryani', 'daal', 'khichdi', 'pasta', 'mac', 'broth', 'roast',
                     'shepherd', 'stroganoff', 'lasagne', 'risotto', 'chowder'],
        'description': 'Warm, hearty dishes for the soul.',
    },
    'healthy': {
        'emoji': '🥗', 'label': 'Healthy & Light',
        'keywords': ['salad', 'grilled', 'steamed', 'quinoa', 'veggie', 'tofu',
                     'lean', 'keto', 'fresh', 'avocado', 'spinach', 'smoothie',
                     'bowl', 'wrap', 'edamame', 'sashimi', 'poké'],
        'description': 'Nutritious and feel-good meals.',
    },
    'beverages': {
        'emoji': '🍹', 'label': 'Beverages',
        'keywords': ['coffee', 'tea', 'milkshake', 'juice', 'mocktail', 'smoothie', 
                     'shake', 'latte', 'cappuccino', 'espresso', 'drink', 'beverage',
                     'lemonade', 'soda', 'cocktail', 'cooler', 'oreo shake', 'frappe'],
        'description': 'Refreshing drinks, coffees, and shakes.',
    },
    'seafood': {
        'emoji': '🦐', 'label': 'Seafood Feast',
        'keywords': ['fish', 'salmon', 'prawn', 'shrimp', 'crab', 'lobster',
                     'squid', 'tuna', 'cod', 'seafood', 'mussel', 'clam', 'scallop',
                     'anchovy', 'sardine', 'oyster', 'tilapia', 'halibut'],
        'description': 'Fresh from the ocean to your plate.',
    },
    'vegetarian': {
        'emoji': '🌿', 'label': 'Vegetarian',
        'keywords': ['paneer', 'tofu', 'lentil', 'chickpea', 'dal', 'veggie',
                     'mushroom', 'jackfruit', 'cauliflower', 'eggplant', 'beans',
                     'falafel', 'hummus', 'tempeh', 'soya', 'peas', 'spinach'],
        'description': 'Plant-based dishes full of flavour.',
    },
    'street-food': {
        'emoji': '🌮', 'label': 'Street Food Vibes',
        'keywords': ['taco', 'biryani', 'kebab', 'wrap', 'shawarma', 'burger',
                     'hotdog', 'samosa', 'pakora', 'falafel', 'gyros',
                     'kathi', 'momos', 'chaat', 'pav bhaji', 'satay',
                     'banh mi', 'bao', 'arepa', 'elote', 'churro'],
        'description': 'Bold flavours from food stalls worldwide.',
    },
}


class Recommender:
    """
    Central orchestrator: filter → score → rank.
    Loaded once at startup; only engine.score() runs per request.
    """

    def __init__(self):
        self.df = None
        self.engine = TFIDFEngine()

    def load(self):
        """Load dataset and fit TF-IDF engine. Call once at app startup."""
        raw_df = load_recipes()
        self.df = preprocess_dataframe(raw_df).reset_index(drop=True)
        self.engine.fit(self.df['ingredient_text'].tolist())

    def _assign_image(self, r: dict) -> dict:
        """Assign image_filename to a recipe dict based on whether a real jpg exists."""
        rid = r.get('id', '')
        jpg_path = f"static/images/recipes/{rid}.jpg"
        r['image_filename'] = (
            f"images/recipes/{rid}.jpg"
            if os.path.exists(jpg_path)
            else f"images/recipes/{rid}.png"
        )
        return r

    def recommend(
        self,
        raw_input: str,
        cuisine: str = None,
        dietary: str = None,
        max_time: int = None,
        top_n: int = TOP_N_RESULTS
    ) -> list:
        """Return top-n recipe dicts ranked by cosine similarity."""
        query_text = preprocess_user_input(raw_input)
        filtered_df = apply_filters(self.df, cuisine, dietary, max_time)

        if filtered_df.empty:
            return []

        all_scores = self.engine.score(query_text)
        filtered_idx = filtered_df.index.to_numpy()
        filtered_scores = all_scores[filtered_idx]

        sorted_positions = np.argsort(filtered_scores)[::-1][:top_n]
        results = filtered_df.iloc[sorted_positions].copy().reset_index(drop=True)
        results['similarity_score'] = filtered_scores[sorted_positions].tolist()

        max_score = results['similarity_score'].max()
        if max_score >= MIN_SCORE_THRESHOLD:
            results = results[results['similarity_score'] >= MIN_SCORE_THRESHOLD]

        result_list = results.to_dict(orient='records')

        query_words = set(query_text.split())
        for r in result_list:
            recipe_text = r.get('ingredient_text', '').lower()
            matching_words = [w for w in query_words if w in recipe_text]
            r['is_high_match'] = len(matching_words) > 0 and r['similarity_score'] > 0.05
            r['similarity_score'] = round(r.get('similarity_score', 0) * 100, 1)
            self._assign_image(r)

        return result_list

    def search_by_name(self, query: str, top_n: int = 60) -> list:
        """Search recipes by dish name using substring matching."""
        if self.df is None:
            return []

        q = query.strip().lower()
        names = self.df['name'].str.lower()

        exact_mask = names == q
        starts_mask = names.str.startswith(q) & ~exact_mask
        contains_mask = names.str.contains(q, na=False) & ~exact_mask & ~starts_mask

        combined = pd.concat([
            self.df[exact_mask],
            self.df[starts_mask],
            self.df[contains_mask]
        ]).head(top_n)

        result_list = combined.to_dict(orient='records')
        for r in result_list:
            r['is_high_match'] = True
            name_lower = str(r.get('name', '')).lower()
            if name_lower == q:
                r['similarity_score'] = 100.0
            elif name_lower.startswith(q):
                r['similarity_score'] = 92.0
            else:
                r['similarity_score'] = 78.0
            self._assign_image(r)

        return result_list

    def search_by_mood(self, mood_key: str, top_n: int = 60) -> list:
        """Return recipes matching a mood by keyword-scanning name/ingredient_text."""
        if self.df is None:
            return []

        mood = MOOD_MAP.get(mood_key)
        if not mood:
            return []

        keywords = mood.get('keywords', [])
        max_minutes = mood.get('max_minutes')

        df = self.df.copy()

        # Optional time filter
        if max_minutes and 'minutes' in df.columns:
            df = df[df['minutes'].fillna(9999) <= max_minutes]

        if df.empty:
            return []

        # Score each recipe by how many mood keywords appear in its name + ingredient_text
        def score_row(row):
            name = str(row.get('name', '')).lower()
            tags = [str(t).lower() for t in row.get('tags', [])]
            ingred_text = str(row.get('ingredient_text', '')).lower()
            haystack = (name + ' ' + ingred_text).lower()
            haystack_words = haystack.replace(',', ' ').replace('.', ' ').split()

            # --- STRICT CATEGORY CHECKS ---
            if mood_key == 'sweet':
                # Only allow if explicitly tagged as dessert or has high-conf keywords AND NO meat
                is_dessert_tag = 'category:dessert' in tags
                if not is_dessert_tag:
                    # Fallback for untagged: must have at least one keyword and NO meat
                    MEAT_KEYWORDS = ['chicken', 'beef', 'lamb', 'mutton', 'pork', 'fish', 'seafood',
                                     'shrimp', 'prawn', 'crab', 'lobster', 'duck', 'turkey', 'meat', 'steak']
                    if any(mk in haystack for mk in MEAT_KEYWORDS):
                        return 0
                    if not any(kw in name or kw in tags for kw in keywords):
                        return 0
            
            if mood_key == 'beverages':
                # Only allow if explicitly tagged as beverage
                if 'category:beverage' not in tags:
                    return 0

            # --- SCORING ---
            base_score = 0
            # Extra weight for category match
            if mood_key == 'sweet' and 'category:dessert' in tags: base_score += 5
            if mood_key == 'beverages' and 'category:beverage' in tags: base_score += 5

            keyword_score = sum(1 for kw in keywords if kw.lower() in haystack_words or f" {kw.lower()} " in f" {haystack} ")
            return base_score + keyword_score

        df = df.copy()
        df['_mood_score'] = df.apply(score_row, axis=1)
        matched = df[df['_mood_score'] > 0].sort_values('_mood_score', ascending=False).head(top_n)

        result_list = matched.drop(columns=['_mood_score']).to_dict(orient='records')
        for r in result_list:
            r['is_high_match'] = True
            r['similarity_score'] = 95.0
            self._assign_image(r)

        return result_list

    def get_similar(self, recipe_id: int, top_n: int = 5) -> list:
        """Return recipes similar to a given recipe_id."""
        if self.df is None or self.engine.matrix is None:
            return []
        idx_series = self.df[self.df['id'] == recipe_id].index
        if idx_series.empty:
            return []
        recipe_vec = self.engine.matrix[idx_series[0]]
        sims = cosine_similarity(recipe_vec, self.engine.matrix).flatten()
        top_idx = np.argsort(sims)[::-1][1:top_n + 1]

        sim_results = self.df.iloc[top_idx].to_dict(orient='records')
        for r in sim_results:
            self._assign_image(r)
        return sim_results
