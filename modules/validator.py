# modules/validator.py
import re
from config import MIN_INGREDIENT_LENGTH, MAX_INPUT_INGREDIENTS

ALLOWED_PATTERN = re.compile(r'^[a-zA-Z0-9\s,\-\']+$')


def validate_ingredient_input(raw: str) -> tuple:
    """
    Validate user ingredient input.

    Returns:
        (is_valid: bool, error_message: str, parsed_items: list)
    """
    if not raw or not raw.strip():
        return False, 'Ingredient input cannot be empty.', []

    if not ALLOWED_PATTERN.match(raw):
        return False, 'Input contains invalid characters. Use letters, numbers, commas, hyphens.', []

    items = [i.strip() for i in raw.split(',') if i.strip()]

    if not items:
        return False, 'Please enter at least one ingredient.', []

    if len(items) > MAX_INPUT_INGREDIENTS:
        return False, f'Maximum {MAX_INPUT_INGREDIENTS} ingredients allowed.', []

    short = [i for i in items if len(i) < MIN_INGREDIENT_LENGTH]
    if short:
        return False, f'Ingredient too short: {short}. Minimum {MIN_INGREDIENT_LENGTH} characters.', []

    return True, '', items


def sanitise(text: str) -> str:
    """Strip HTML-unsafe characters for XSS prevention."""
    return re.sub(r'[<>&"\']', '', text).strip()
