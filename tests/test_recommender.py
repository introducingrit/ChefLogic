# tests/test_recommender.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from unittest.mock import patch, MagicMock
from modules.recommender import Recommender
from modules.preprocessor import preprocess_dataframe


def _build_recommender(sample_df):
    """Helper: return a fitted Recommender using the sample fixture DataFrame."""
    rec = Recommender()
    rec.df = preprocess_dataframe(sample_df).reset_index(drop=True)
    rec.engine.fit(rec.df['ingredient_text'].tolist())
    return rec


def test_recommend_returns_list(sample_df):
    rec = _build_recommender(sample_df)
    results = rec.recommend('egg butter')
    assert isinstance(results, list)


def test_recommend_results_have_name_key(sample_df):
    rec = _build_recommender(sample_df)
    results = rec.recommend('egg flour milk')
    assert all('name' in r for r in results)


def test_recommend_similarity_score_in_range(sample_df):
    rec = _build_recommender(sample_df)
    results = rec.recommend('egg butter milk')
    for r in results:
        # Score is multiplied by 100 for display (0–100 range)
        assert 0.0 <= r['similarity_score'] <= 100.0


def test_recommend_top_n_respected(sample_df):
    rec = _build_recommender(sample_df)
    results = rec.recommend('chicken garlic', top_n=2)
    assert len(results) <= 2


def test_recommend_with_cuisine_filter(sample_df):
    rec = _build_recommender(sample_df)
    results = rec.recommend('pasta egg', cuisine='italian')
    # All results should have 'italian' in their tags
    for r in results:
        tags_str = ' '.join(str(t) for t in r.get('tags', []))
        assert 'italian' in tags_str.lower()


def test_recommend_empty_on_impossible_filter(sample_df):
    rec = _build_recommender(sample_df)
    results = rec.recommend('egg', cuisine='nonexistent_xyz_cuisine')
    assert results == []


def test_get_similar_returns_list(sample_df):
    rec = _build_recommender(sample_df)
    similar = rec.get_similar(recipe_id=1)
    assert isinstance(similar, list)


def test_get_similar_excludes_self(sample_df):
    rec = _build_recommender(sample_df)
    similar = rec.get_similar(recipe_id=1)
    ids = [r['id'] for r in similar]
    assert 1 not in ids


def test_get_similar_unknown_id(sample_df):
    rec = _build_recommender(sample_df)
    similar = rec.get_similar(recipe_id=99999)
    assert similar == []
