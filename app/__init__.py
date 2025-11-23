from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:///movie_selector.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['PLEX_SERVER_URL'] = os.environ.get('PLEX_SERVER_URL', 'http://localhost:32400')

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    # Register routes
    from app.routes import register_routes
    register_routes(app)

    # Create database tables
    with app.app_context():
        db.create_all()

    return app
