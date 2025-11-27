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
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', 'sqlite:////app/instance/movie_selector.db')
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

        # Run migrations
        migrate_database()

    return app

def migrate_database():
    """Run database migrations to add new columns"""
    try:
        # Check if we need to add the new client selection columns
        from sqlalchemy import inspect, text
        inspector = inspect(db.engine)

        # Get existing columns for user_preferences table
        columns = [col['name'] for col in inspector.get_columns('user_preferences')]

        # Add selected_client_name column if it doesn't exist
        if 'selected_client_name' not in columns:
            print("Adding selected_client_name column to user_preferences...")
            with db.engine.connect() as conn:
                conn.execute(text('ALTER TABLE user_preferences ADD COLUMN selected_client_name VARCHAR(255)'))
                conn.commit()
            print("✓ Added selected_client_name column")

        # Add selected_client_identifier column if it doesn't exist
        if 'selected_client_identifier' not in columns:
            print("Adding selected_client_identifier column to user_preferences...")
            with db.engine.connect() as conn:
                conn.execute(text('ALTER TABLE user_preferences ADD COLUMN selected_client_identifier VARCHAR(255)'))
                conn.commit()
            print("✓ Added selected_client_identifier column")

        print("Database migration completed successfully")

    except Exception as e:
        print(f"Error during database migration: {e}")
        import traceback
        traceback.print_exc()
