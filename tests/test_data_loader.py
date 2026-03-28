# tests/test_data_loader.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import pandas as pd
from unittest.mock import patch
from modules.data_loader import load_recipes, _safe_parse_list


def test_safe_parse_list_python_literal():
    result = _safe_parse_list("['egg', 'milk', 'flour']")
    assert result == ['egg', 'milk', 'flour']


def test_safe_parse_list_already_list():
    result = _safe_parse_list(['egg', 'milk'])
    assert result == ['egg', 'milk']


def test_safe_parse_list_invalid_returns_empty():
    result = _safe_parse_list('not_a_list{{}}')
    assert result == []


def test_safe_parse_list_nan_returns_empty():
    result = _safe_parse_list(float('nan'))
    assert result == []


def test_load_recipes_missing_column_raises(tmp_path):
    """If processed CSV is missing a required column, ValueError is raised."""
    # Create a CSV without 'tags' column
    bad_csv = tmp_path / 'recipes_clean.csv'
    df = pd.DataFrame({'id': [1], 'name': ['Test'], 'ingredients': ["['egg']"], 'steps': ["['step']"], 'minutes': [10]})
    df.to_csv(bad_csv, index=False)

    with patch('modules.data_loader.PROCESSED_DATA_PATH', str(bad_csv)):
        with pytest.raises(ValueError, match='tags'):
            load_recipes()


def test_load_recipes_valid(tmp_path):
    """A valid CSV should load and parse list columns."""
    good_csv = tmp_path / 'recipes_clean.csv'
    df = pd.DataFrame({
        'id': [1, 2],
        'name': ['Pasta', 'Salad'],
        'ingredients': ["['pasta', 'egg']", "['lettuce', 'tomato']"],
        'steps': ["['boil', 'mix']", "['chop', 'toss']"],
        'minutes': [30, 10],
        'tags': ["['italian']", "['vegan']"],
    })
    df.to_csv(good_csv, index=False)

    with patch('modules.data_loader.PROCESSED_DATA_PATH', str(good_csv)):
        result = load_recipes()

    assert len(result) == 2
    assert isinstance(result['ingredients'].iloc[0], list)
    assert isinstance(result['tags'].iloc[0], list)
