# tests/test_tfidf_engine.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import numpy as np
from modules.tfidf_engine import TFIDFEngine


CORPUS = [
    'egg butter milk',
    'chicken garlic curry',
    'pasta egg bacon parmesan',
    'tortilla beans avocado',
    'beef potato carrot onion',
]


@pytest.fixture
def fitted_engine():
    engine = TFIDFEngine()
    engine.fit(CORPUS)
    return engine


def test_score_returns_array(fitted_engine):
    scores = fitted_engine.score('egg butter')
    assert isinstance(scores, np.ndarray)


def test_score_length_equals_corpus(fitted_engine):
    scores = fitted_engine.score('egg butter')
    assert len(scores) == len(CORPUS)


def test_score_values_in_range(fitted_engine):
    scores = fitted_engine.score('chicken curry')
    assert all(0.0 <= s <= 1.0 for s in scores)


def test_exact_match_highest_score(fitted_engine):
    scores = fitted_engine.score('egg butter milk')
    # Recipe 0 is 'egg butter milk' — should be highest
    assert np.argmax(scores) == 0


def test_score_before_fit_raises():
    engine = TFIDFEngine()
    with pytest.raises(RuntimeError):
        engine.score('test query')


def test_fit_stores_matrix(fitted_engine):
    assert fitted_engine.matrix is not None
    assert fitted_engine.matrix.shape[0] == len(CORPUS)
