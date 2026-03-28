# routes/api.py
from flask import Blueprint, jsonify, request, current_app
from modules.validator import validate_ingredient_input, sanitise
from modules.substitution import get_substitutions

api_bp = Blueprint('api', __name__)


@api_bp.route('/recommend', methods=['GET'])
def api_recommend():
    """
    JSON API endpoint.
    GET /api/recommend?ingredients=egg,flour&cuisine=italian&dietary=vegetarian&max_time=60
    """
    raw = sanitise(request.args.get('ingredients', ''))
    cuisine = request.args.get('cuisine') or None
    dietary = request.args.get('dietary') or None
    max_time_raw = request.args.get('max_time') or None
    max_time = int(max_time_raw) if max_time_raw and max_time_raw.isdigit() else None

    is_valid, error, _ = validate_ingredient_input(raw)
    if not is_valid:
        return jsonify({'error': error}), 400

    recommender = current_app.config['RECOMMENDER']
    results = recommender.recommend(raw, cuisine, dietary, max_time)

    # Serialise lists that may not be JSON-serialisable straight from pandas
    for r in results:
        for key in ['ingredients', 'steps', 'tags']:
            if key in r and not isinstance(r[key], list):
                r[key] = []
        r['similarity_score'] = float(r.get('similarity_score', 0))

    return jsonify({'query': raw, 'count': len(results), 'results': results})


@api_bp.route('/substitutions', methods=['GET'])
def api_substitutions():
    """
    GET /api/substitutions?ingredients=butter,egg,milk
    Returns ingredient substitution suggestions.
    """
    raw = sanitise(request.args.get('ingredients', ''))
    is_valid, error, items = validate_ingredient_input(raw)
    if not is_valid:
        return jsonify({'error': error}), 400
    return jsonify({'substitutions': get_substitutions(items)})


@api_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint for Render uptime monitoring."""
    recommender = current_app.config.get('RECOMMENDER')
    ready = recommender is not None and recommender.df is not None
    total = len(recommender.df) if ready else 0
    return jsonify({'status': 'ok' if ready else 'loading', 'recipes_loaded': total})


@api_bp.route('/search-data', methods=['GET'])
def search_data():
    """Return all recipe names and ingredient list for Fuse.js fuzzy search."""
    recommender = current_app.config.get('RECOMMENDER')
    if recommender is None or recommender.df is None:
        return jsonify({'names': [], 'ingredients': []})
    names = recommender.df['name'].dropna().tolist()
    return jsonify({'names': names})
