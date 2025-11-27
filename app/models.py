from datetime import datetime, timedelta
from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    plex_username = db.Column(db.String(100), unique=True, nullable=False)
    plex_token = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    passed_movies = db.relationship('PassedMovie', backref='user', lazy=True, cascade='all, delete-orphan')
    preferences = db.relationship('UserPreference', backref='user', uselist=False, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.plex_username}>'

class PassedMovie(db.Model):
    __tablename__ = 'passed_movies'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    plex_rating_key = db.Column(db.String(100), nullable=False)
    movie_title = db.Column(db.String(255), nullable=False)
    passed_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, *args, **kwargs):
        super(PassedMovie, self).__init__(*args, **kwargs)
        if not self.expires_at:
            # Set expiration to 6 months from now
            self.expires_at = datetime.utcnow() + timedelta(days=180)

    @property
    def is_expired(self):
        return datetime.utcnow() > self.expires_at

    def __repr__(self):
        return f'<PassedMovie {self.movie_title}>'

class UserPreference(db.Model):
    __tablename__ = 'user_preferences'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # Filter preferences
    exclude_watched = db.Column(db.Boolean, default=True)
    exclude_same_actors = db.Column(db.Boolean, default=False)
    exclude_same_director = db.Column(db.Boolean, default=False)
    filter_decade = db.Column(db.String(10), nullable=True)  # e.g., "1990s", "2000s"
    filter_actor = db.Column(db.String(100), nullable=True)

    # Playback client preferences
    selected_client_name = db.Column(db.String(255), nullable=True)  # e.g., "SHIELD Android TV"
    selected_client_identifier = db.Column(db.String(255), nullable=True)  # Machine identifier for verification

    def __repr__(self):
        return f'<UserPreference for user_id {self.user_id}>'
