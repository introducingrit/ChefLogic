# modules/tfidf_engine.py
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from config import TFIDF_MAX_FEATURES


class TFIDFEngine:
    """TF-IDF vectoriser + cosine similarity engine for recipe recommendations."""

    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=TFIDF_MAX_FEATURES,
            ngram_range=(1, 2),   # unigrams + bigrams (e.g., 'olive oil')
            analyzer='word',
            sublinear_tf=True     # dampens very frequent terms
        )
        self.matrix = None        # sparse matrix: (n_recipes, n_features)

    def fit(self, corpus: list) -> None:
        """Fit vectoriser on list of ingredient_text strings and store matrix."""
        self.matrix = self.vectorizer.fit_transform(corpus)

    def score(self, query: str) -> np.ndarray:
        """Return cosine similarity scores for query against all recipes."""
        if self.matrix is None:
            raise RuntimeError('TFIDFEngine.fit() must be called before score()')
        query_vec = self.vectorizer.transform([query])
        return cosine_similarity(query_vec, self.matrix).flatten()
