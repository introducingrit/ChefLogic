# app.py
from flask import Flask
from modules.recommender import Recommender
from routes.main import main_bp
from routes.api import api_bp


def create_app():
    """Flask application factory. Loads dataset and registers blueprints once."""
    app = Flask(__name__)
    app.secret_key = 'rrs-secret-change-in-prod'

    recommender = Recommender()
    recommender.load()   # Loads CSV + fits TF-IDF (runs once, ~2-5s)
    app.config['RECOMMENDER'] = recommender

    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
