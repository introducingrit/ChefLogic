# tests/test_filter_engine.py
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from modules.filter_engine import apply_filters


def test_no_filters_returns_all(sample_df):
    result = apply_filters(sample_df)
    assert len(result) == len(sample_df)


def test_cuisine_filter_reduces_rows(sample_df):
    result = apply_filters(sample_df, cuisine='italian')
    assert len(result) < len(sample_df)
    assert len(result) >= 1


def test_dietary_vegan_filter(sample_df):
    result = apply_filters(sample_df, dietary='vegan')
    # Only the vegan taco recipe has 'vegan' tag
    for _, row in result.iterrows():
        assert any('vegan' in str(t).lower() for t in row['tags'])


def test_time_filter_removes_long_recipes(sample_df):
    result = apply_filters(sample_df, max_time=30)
    assert all(row['minutes'] <= 30 for _, row in result.iterrows())


def test_combined_filters(sample_df):
    result = apply_filters(sample_df, dietary='vegetarian', max_time=60)
    for _, row in result.iterrows():
        assert row['minutes'] <= 60
        assert any('vegetarian' in str(t).lower() for t in row['tags'])


def test_no_matching_filter_returns_empty(sample_df):
    result = apply_filters(sample_df, cuisine='nonexistent_cuisine_xyz')
    assert len(result) == 0


def test_time_filter_max5_minutes(sample_df):
    result = apply_filters(sample_df, max_time=5)
    assert len(result) == 0
