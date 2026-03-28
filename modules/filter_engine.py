# modules/filter_engine.py
import ast
import pandas as pd
from config import DIETARY_TAGS, MAX_COOKING_TIME


def _parse_tags(raw) -> list:
    """Safely parse a tags value that may be a list or a stringified list."""
    if isinstance(raw, list):
        return raw
    if not raw or (isinstance(raw, float)):
        return []
    try:
        result = ast.literal_eval(str(raw))
        if isinstance(result, list):
            return result
        return [str(result)]
    except Exception:
        # Fallback: treat the raw string as a single tag
        return [str(raw)]


def apply_filters(
    df: pd.DataFrame,
    cuisine: str = None,
    dietary: str = None,
    max_time: int = None
) -> pd.DataFrame:
    """
    Apply optional cuisine, dietary, and cooking-time filters.
    Returns a filtered DataFrame slice preserving original index so that
    similarity scores align correctly with the recommender.
    """
    mask = pd.Series([True] * len(df), index=df.index)

    if cuisine:
        cuisine_lower = cuisine.strip().lower()
        # Also match partial cuisine names (e.g. 'sichuan' matches 'szechuan')
        CUISINE_ALIASES = {
            'sichuan': ['sichuan', 'szechuan', 'chinese'],
            'chinese':  ['chinese', 'sichuan', 'szechuan', 'cantonese', 'dim sum'],
            'middle-eastern': ['middle-eastern', 'middle eastern', 'arab', 'lebanese',
                               'turkish', 'persian', 'iranian', 'arabic'],
            'indian': ['indian', 'south asian', 'mughlai', 'hyderabadi', 'kashmiri',
                       'kerala', 'goan', 'punjabi'],
            'coastal': ['coastal', 'seafood', 'fish', 'prawn', 'crab'],
        }
        aliases = CUISINE_ALIASES.get(cuisine_lower, [cuisine_lower])

        def matches_cuisine(raw_tags):
            tags = _parse_tags(raw_tags)
            tags_lower = [str(t).lower() for t in tags]
            return any(
                any(alias in tag for tag in tags_lower)
                for alias in aliases
            )

        mask &= df['tags'].apply(matches_cuisine)

    if dietary and dietary in DIETARY_TAGS:
        keywords = DIETARY_TAGS[dietary]

        def matches_dietary(raw_tags):
            tags = _parse_tags(raw_tags)
            tags_lower = [str(t).lower() for t in tags]
            return any(k in tag for k in keywords for tag in tags_lower)

        mask &= df['tags'].apply(matches_dietary)

    if max_time:
        try:
            mask &= df['minutes'].fillna(9999) <= int(max_time)
        except (ValueError, TypeError):
            pass  # ignore malformed time filter

    return df[mask]
