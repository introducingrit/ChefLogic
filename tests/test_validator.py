# tests/test_validator.py
import pytest
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from modules.validator import validate_ingredient_input, sanitise


def test_empty_input_is_invalid():
    valid, err, items = validate_ingredient_input('')
    assert not valid
    assert 'empty' in err.lower()


def test_whitespace_only_is_invalid():
    valid, err, items = validate_ingredient_input('   ')
    assert not valid


def test_valid_single_ingredient():
    valid, err, items = validate_ingredient_input('egg')
    assert valid
    assert items == ['egg']


def test_valid_multiple_ingredients():
    valid, err, items = validate_ingredient_input('egg, flour, milk')
    assert valid
    assert items == ['egg', 'flour', 'milk']


def test_xss_characters_rejected():
    valid, err, items = validate_ingredient_input('<script>alert(1)</script>')
    assert not valid


def test_too_many_ingredients():
    raw = ', '.join([f'ingredient{i}' for i in range(25)])
    valid, err, items = validate_ingredient_input(raw)
    assert not valid
    assert 'maximum' in err.lower()


def test_ingredient_too_short():
    valid, err, items = validate_ingredient_input('a, flour')
    assert not valid
    assert 'short' in err.lower() or 'minimum' in err.lower()


def test_sanitise_removes_angle_brackets():
    result = sanitise('<b>hello</b>')
    assert '<' not in result
    assert '>' not in result


def test_sanitise_strips_whitespace():
    result = sanitise('  hello  ')
    assert result == 'hello'


def test_valid_ingredient_with_hyphen():
    valid, err, items = validate_ingredient_input('gluten-free flour')
    assert valid
