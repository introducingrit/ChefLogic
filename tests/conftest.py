# tests/conftest.py
"""
Shared pytest fixtures available to all test modules.
"""
import sys
import os
import pytest
import pandas as pd

# Add project root to sys.path so modules resolve correctly from tests/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


SAMPLE_DF = pd.DataFrame({
    'id':          [1, 2, 3, 4, 5],
    'name':        ['Pasta Carbonara', 'Chicken Curry', 'Vegan Tacos', 'Beef Stew', 'Omelette'],
    'ingredients': [
        ['pasta', 'egg', 'bacon', 'parmesan'],
        ['chicken', 'curry powder', 'coconut milk', 'garlic'],
        ['tortilla', 'black beans', 'avocado', 'lime'],
        ['beef', 'potato', 'carrot', 'onion'],
        ['egg', 'butter', 'milk', 'salt'],
    ],
    'steps': [
        ['boil pasta', 'fry bacon', 'mix egg and cheese', 'combine'],
        ['marinate chicken', 'fry spices', 'add coconut milk', 'simmer'],
        ['warm tortilla', 'mash beans', 'assemble', 'serve'],
        ['brown beef', 'add vegetables', 'simmer 2 hours'],
        ['beat eggs', 'melt butter', 'cook omelette'],
    ],
    'tags': [
        ['italian', 'pasta'],
        ['indian', 'chicken'],
        ['mexican', 'vegan', 'vegetarian'],
        ['american', 'beef'],
        ['breakfast', 'vegetarian'],
    ],
    'minutes': [30, 45, 20, 120, 10],
})


@pytest.fixture
def sample_df():
    return SAMPLE_DF.copy()
