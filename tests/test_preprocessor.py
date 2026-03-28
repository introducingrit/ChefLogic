# tests/test_preprocessor.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import pandas as pd
from modules.preprocessor import (
    clean_ingredient,
    build_ingredient_text,
    preprocess_dataframe,
    preprocess_user_input,
)


def test_clean_ingredient_lowercase():
    assert clean_ingredient('GARLIC') == 'garlic'


def test_clean_ingredient_removes_numbers():
    result = clean_ingredient('2 cups flour')
    assert '2' not in result
    assert 'flour' in result


def test_clean_ingredient_removes_fractions():
    result = clean_ingredient('1/2 teaspoon salt')
    assert '1/2' not in result
    assert 'salt' in result


def test_clean_ingredient_removes_stop_words():
    result = clean_ingredient('a pinch of salt')
    assert 'of' not in result.split()
    assert 'a' not in result.split()


def test_clean_ingredient_returns_string():
    result = clean_ingredient('butter')
    assert isinstance(result, str)


def test_build_ingredient_text_joins():
    result = build_ingredient_text(['egg', 'flour', 'milk'])
    assert 'egg' in result
    assert 'flour' in result


def test_preprocess_dataframe_adds_column(sample_df):
    result = preprocess_dataframe(sample_df)
    assert 'ingredient_text' in result.columns
    # pandas 3.0+ uses StringDtype; check values are strings, not a specific dtype
    assert all(isinstance(v, str) for v in result['ingredient_text'])



def test_preprocess_user_input_comma_separated():
    result = preprocess_user_input('egg, flour, milk')
    assert 'egg' in result
    assert 'flour' in result


def test_preprocess_user_input_ignores_empty_parts():
    result = preprocess_user_input('egg,,, flour')
    assert result.count('egg') == 1
