# routes/main.py
from flask import Blueprint, render_template, request, current_app
from modules.validator import validate_ingredient_input, sanitise
from modules.substitution import get_substitutions
import os

main_bp = Blueprint('main', __name__)


@main_bp.route('/', methods=['GET'])
def index():
    """Landing page with ingredient input form."""
    return render_template('index.html')


@main_bp.route('/favourites')
def favourites():
    """Favourites page — content is rendered client-side from localStorage."""
    return render_template('favourites.html')


@main_bp.route('/all-recipes')
def all_recipes():
    """Browse all recipes, optionally filtered by cuisine or dietary tag."""
    recommender = current_app.config.get('RECOMMENDER')
    if not recommender or recommender.df is None:
        return render_template('results.html', results=[], query='All Recipes',
                               search_mode='all', substitutions={},
                               cuisine=None, dietary=None, max_time=None)

    cuisine = request.args.get('cuisine', '').strip() or None
    dietary = request.args.get('dietary', '').strip() or None

    from modules.filter_engine import apply_filters
    df = apply_filters(recommender.df, cuisine=cuisine, dietary=dietary)

    # Sort alphabetically by name
    df = df.sort_values('name')
    results = df.to_dict(orient='records')
    for r in results:
        recommender._assign_image(r)
        r['similarity_score'] = 0
        r['is_high_match'] = True

    return render_template(
        'results.html',
        results=results,
        query='All Recipes 🌍',
        search_mode='all',
        substitutions={},
        cuisine=cuisine,
        dietary=dietary,
        max_time=None,
    )


@main_bp.route('/recommend', methods=['POST'])
def recommend():
    """Process ingredient form and render ranked recipe results."""
    raw = sanitise(request.form.get('ingredients', ''))
    cuisine = request.form.get('cuisine') or None
    dietary = request.form.get('dietary') or None
    max_time_raw = request.form.get('max_time') or None
    max_time = int(max_time_raw) if max_time_raw and max_time_raw.isdigit() else None

    is_valid, error, items = validate_ingredient_input(raw)
    if not is_valid:
        return render_template('index.html', error=error)

    recommender = current_app.config['RECOMMENDER']
    results = recommender.recommend(raw, cuisine, dietary, max_time)
    substitutions = get_substitutions(items)

    return render_template(
        'results.html',
        results=results,
        query=raw,
        substitutions=substitutions,
        cuisine=cuisine,
        dietary=dietary,
        max_time=max_time,
        search_mode='ingredients',
    )


@main_bp.route('/search-dish', methods=['POST'])
def search_dish():
    """Search for recipes directly by dish name."""
    query = sanitise(request.form.get('dish_name', '').strip())
    if not query:
        return render_template('index.html', error='Please enter a dish name to search.')

    recommender = current_app.config['RECOMMENDER']
    results = recommender.search_by_name(query)

    return render_template(
        'results.html',
        results=results,
        query=query,
        substitutions={},
        cuisine=None,
        dietary=None,
        max_time=None,
        search_mode='name',
    )


@main_bp.route('/search-mood', methods=['POST'])
def search_mood():
    """Search for recipes by mood/craving."""
    from modules.recommender import MOOD_MAP
    mood_key = request.form.get('mood', '').strip().lower()
    if not mood_key or mood_key not in MOOD_MAP:
        return render_template('index.html', error='Please select a valid mood/craving.')

    mood_info = MOOD_MAP[mood_key]
    recommender = current_app.config['RECOMMENDER']
    results = recommender.search_by_mood(mood_key)

    return render_template(
        'results.html',
        results=results,
        query=f"{mood_info['emoji']} {mood_info['label']}",
        substitutions={},
        cuisine=None,
        dietary=None,
        max_time=None,
        search_mode='mood',
        mood_description=mood_info['description'],
    )


@main_bp.route('/recipe/<int:recipe_id>')
def detail(recipe_id):
    """Full recipe detail page."""
    recommender = current_app.config['RECOMMENDER']
    recipe_row = recommender.df[recommender.df['id'] == recipe_id]
    if recipe_row.empty:
        return render_template('index.html', error=f'Recipe #{recipe_id} not found.')

    recipe = recipe_row.iloc[0].to_dict()
    # Resolve image server-side
    jpg_path = f"static/images/recipes/{recipe['id']}.jpg"
    if os.path.exists(jpg_path):
        recipe['image_filename'] = f"images/recipes/{recipe['id']}.jpg"
    else:
        recipe['image_filename'] = f"images/recipes/{recipe['id']}.png"

    similar = recommender.get_similar(recipe_id)
    return render_template(
        'detail.html',
        recipe=recipe,
        similar=similar
    )
