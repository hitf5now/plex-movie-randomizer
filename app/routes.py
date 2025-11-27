from flask import render_template, request, jsonify, redirect, url_for, session
from flask_login import login_user, logout_user, login_required, current_user
from app import db, login_manager
from app.models import User, PassedMovie, UserPreference
from app.plex_api import PlexAPI
from app.movie_selector import MovieSelector
from datetime import datetime
import os

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def register_routes(app):

    @app.route('/')
    def index():
        """Main page - redirect to login if not authenticated"""
        if current_user.is_authenticated:
            return render_template('index.html')
        return redirect(url_for('login'))

    @app.route('/login')
    def login():
        """Login page"""
        return render_template('login.html')

    @app.route('/api/auth/login', methods=['POST'])
    def api_login():
        """API endpoint for user authentication"""
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400

        # Check if PLEX_TOKEN is set in environment (Unraid UI configuration)
        env_token = os.environ.get('PLEX_TOKEN', '').strip()

        if env_token:
            # Use environment token for authentication
            token = env_token
            # Verify the token works by testing connection
            plex = PlexAPI(token)
            if not plex.server:
                return jsonify({'error': 'Invalid Plex token in configuration'}), 401
        else:
            # Authenticate with Plex using username/password
            token = PlexAPI.authenticate(username, password)
            if not token:
                return jsonify({'error': 'Invalid credentials'}), 401

        # Check if user exists
        user = User.query.filter_by(plex_username=username).first()

        if not user:
            # Create new user
            user = User(plex_username=username, plex_token=token)
            db.session.add(user)

            # Create default preferences
            preferences = UserPreference(user=user)
            db.session.add(preferences)

            db.session.commit()
        else:
            # Update token and last login
            user.plex_token = token
            user.last_login = datetime.utcnow()
            db.session.commit()

        # Log user in
        login_user(user)

        return jsonify({
            'success': True,
            'username': user.plex_username
        })

    @app.route('/api/auth/logout', methods=['POST'])
    @login_required
    def api_logout():
        """API endpoint for logout"""
        logout_user()
        return jsonify({'success': True})

    @app.route('/api/recommend', methods=['GET'])
    @login_required
    def api_recommend():
        """Get a movie recommendation"""
        try:
            # Create Plex API instance
            plex = PlexAPI(current_user.plex_token)

            # Create movie selector
            selector = MovieSelector(current_user, plex)

            # Get recommendation
            movie, error = selector.recommend_movie()

            if error:
                return jsonify({'error': error}), 404

            if not movie:
                return jsonify({'error': 'No movie found'}), 404

            # Get movie info
            movie_info = selector.get_movie_info(movie)

            return jsonify({
                'success': True,
                'movie': movie_info
            })

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/add-to-playlist', methods=['POST'])
    @login_required
    def api_add_to_playlist():
        """Add a movie to the user's playlist"""
        data = request.get_json()
        rating_key = data.get('rating_key')

        if not rating_key:
            return jsonify({'error': 'rating_key required'}), 400

        try:
            plex = PlexAPI(current_user.plex_token)

            # Get user preferences (needed for playlist ID)
            prefs = current_user.preferences
            if not prefs:
                # Create default preferences if none exist
                prefs = UserPreference(user_id=current_user.id)
                db.session.add(prefs)
                db.session.commit()

            success, message = plex.add_movie_to_playlist(rating_key, prefs)

            if success:
                return jsonify({
                    'success': True,
                    'message': message
                })
            else:
                return jsonify({
                    'success': False,
                    'error': message
                }), 500

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/pass', methods=['POST'])
    @login_required
    def api_pass():
        """Pass on a movie (exclude for 6 months)"""
        data = request.get_json()
        rating_key = data.get('rating_key')
        title = data.get('title', 'Unknown')

        if not rating_key:
            return jsonify({'error': 'rating_key required'}), 400

        try:
            # Check if already passed (convert rating_key to string for consistency)
            existing = PassedMovie.query.filter_by(
                user_id=current_user.id,
                plex_rating_key=str(rating_key)
            ).first()

            if existing:
                # Update expiration date
                from datetime import datetime, timedelta
                existing.passed_at = datetime.utcnow()
                existing.expires_at = datetime.utcnow() + timedelta(days=180)
            else:
                # Create new pass entry
                passed_movie = PassedMovie(
                    user_id=current_user.id,
                    plex_rating_key=str(rating_key),
                    movie_title=title
                )
                db.session.add(passed_movie)

            db.session.commit()

            return jsonify({'success': True})

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/passed-movies', methods=['GET'])
    @login_required
    def api_get_passed_movies():
        """Get list of passed movies for current user"""
        try:
            passed_movies = PassedMovie.query.filter_by(user_id=current_user.id).all()

            movies_list = [{
                'id': pm.id,
                'title': pm.movie_title,
                'rating_key': pm.plex_rating_key,
                'passed_at': pm.passed_at.isoformat(),
                'expires_at': pm.expires_at.isoformat(),
                'is_expired': pm.is_expired
            } for pm in passed_movies]

            return jsonify({
                'success': True,
                'movies': movies_list
            })

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/passed-movies/<int:movie_id>', methods=['DELETE'])
    @login_required
    def api_delete_passed_movie(movie_id):
        """Remove a movie from the passed list"""
        try:
            passed_movie = PassedMovie.query.filter_by(
                id=movie_id,
                user_id=current_user.id
            ).first()

            if not passed_movie:
                return jsonify({'error': 'Movie not found'}), 404

            db.session.delete(passed_movie)
            db.session.commit()

            return jsonify({'success': True})

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/preferences', methods=['GET'])
    @login_required
    def api_get_preferences():
        """Get user preferences"""
        try:
            prefs = current_user.preferences
            if not prefs:
                # Create default preferences if none exist
                prefs = UserPreference(user_id=current_user.id)
                db.session.add(prefs)
                db.session.commit()

            return jsonify({
                'success': True,
                'preferences': {
                    'exclude_watched': prefs.exclude_watched,
                    'exclude_same_actors': prefs.exclude_same_actors,
                    'exclude_same_director': prefs.exclude_same_director,
                    'filter_decade': prefs.filter_decade,
                    'filter_actor': prefs.filter_actor
                }
            })

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/api/preferences', methods=['POST'])
    @login_required
    def api_update_preferences():
        """Update user preferences"""
        try:
            data = request.get_json()
            prefs = current_user.preferences

            if not prefs:
                prefs = UserPreference(user_id=current_user.id)
                db.session.add(prefs)

            # Update preferences
            if 'exclude_watched' in data:
                prefs.exclude_watched = data['exclude_watched']
            if 'exclude_same_actors' in data:
                prefs.exclude_same_actors = data['exclude_same_actors']
            if 'exclude_same_director' in data:
                prefs.exclude_same_director = data['exclude_same_director']
            if 'filter_decade' in data:
                prefs.filter_decade = data['filter_decade'] if data['filter_decade'] else None
            if 'filter_actor' in data:
                prefs.filter_actor = data['filter_actor'] if data['filter_actor'] else None

            db.session.commit()

            return jsonify({'success': True})

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/passed-list')
    @login_required
    def passed_list():
        """Passed movies management page"""
        return render_template('passed_list.html')


    @app.route('/api/last-watched', methods=['GET'])
    @login_required
    def api_get_last_watched():
        """Get the last watched movie information"""
        try:
            plex = PlexAPI(current_user.plex_token)
            last_watched = plex.get_last_watched_movie(current_user.plex_username)

            if not last_watched:
                return jsonify({'success': True, 'movie': None})

            # Get movie details
            movie_info = {
                'title': last_watched.title,
                'year': plex.get_movie_year(last_watched),
                'poster': last_watched.thumbUrl if hasattr(last_watched, 'thumbUrl') else '',
                'actors': plex.get_movie_actors(last_watched)[:5],
                'directors': plex.get_movie_directors(last_watched)
            }

            return jsonify({'success': True, 'movie': movie_info})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

