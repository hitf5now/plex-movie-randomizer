from plexapi.myplex import MyPlexAccount
from plexapi.server import PlexServer
from plexapi.exceptions import BadRequest, Unauthorized
import os

class PlexAPI:
    def __init__(self, token=None):
        self.token = token
        self.server = None
        if token:
            self._connect_server()

    def _connect_server(self):
        """Connect to Plex server using token"""
        try:
            server_url = os.environ.get('PLEX_SERVER_URL', 'http://localhost:32400')
            self.server = PlexServer(server_url, self.token)
            return True
        except Exception as e:
            print(f"Error connecting to Plex server: {e}")
            return False

    @staticmethod
    def authenticate(username, password):
        """Authenticate user with Plex and return token"""
        try:
            account = MyPlexAccount(username, password)
            return account.authenticationToken
        except (BadRequest, Unauthorized) as e:
            print(f"Authentication error: {e}")
            return None

    def get_movie_library(self, library_name='Movies'):
        """Get the movie library from Plex"""
        if not self.server:
            return None
        try:
            return self.server.library.section(library_name)
        except Exception as e:
            print(f"Error getting library: {e}")
            return None

    def get_all_movies(self, library_name='Movies'):
        """Get all movies from the specified library"""
        library = self.get_movie_library(library_name)
        if not library:
            return []
        return library.all()

    def get_movie_details(self, rating_key):
        """Get detailed information about a specific movie"""
        if not self.server:
            return None
        try:
            return self.server.fetchItem(rating_key)
        except Exception as e:
            print(f"Error fetching movie: {e}")
            return None

    def get_user_watched_movies(self, username):
        """Get list of movies watched by user"""
        if not self.server:
            return []
        try:
            movies = self.get_all_movies()
            watched = []
            for movie in movies:
                if movie.isWatched:
                    watched.append(movie)
            return watched
        except Exception as e:
            print(f"Error getting watched movies: {e}")
            return []

    def get_last_watched_movie(self, username):
        """Get the last movie watched by the user"""
        if not self.server:
            return None
        try:
            movies = self.get_all_movies()
            watched_movies = [m for m in movies if m.isWatched and m.lastViewedAt]
            if not watched_movies:
                return None
            # Sort by last viewed date
            watched_movies.sort(key=lambda x: x.lastViewedAt, reverse=True)
            return watched_movies[0]
        except Exception as e:
            print(f"Error getting last watched movie: {e}")
            return None

    def play_movie(self, rating_key, player_name=None):
        """Play a movie on the specified player or default player"""
        if not self.server:
            return False
        try:
            movie = self.get_movie_details(rating_key)
            if not movie:
                return False

            # Get available clients
            clients = self.server.clients()
            if not clients:
                print("No active Plex clients found")
                return False

            # Use first available client or specified player
            client = clients[0]
            if player_name:
                client = next((c for c in clients if c.title == player_name), clients[0])

            # Play the movie
            client.playMedia(movie)
            return True
        except Exception as e:
            print(f"Error playing movie: {e}")
            return False

    def get_movie_actors(self, movie):
        """Get list of actor names from a movie"""
        try:
            return [role.tag for role in movie.roles] if movie.roles else []
        except Exception as e:
            print(f"Error getting actors: {e}")
            return []

    def get_movie_directors(self, movie):
        """Get list of director names from a movie"""
        try:
            return [director.tag for director in movie.directors] if movie.directors else []
        except Exception as e:
            print(f"Error getting directors: {e}")
            return []

    def get_movie_year(self, movie):
        """Get the year of the movie"""
        try:
            return movie.year if hasattr(movie, 'year') else None
        except Exception as e:
            print(f"Error getting year: {e}")
            return None

    def get_movie_rating(self, movie):
        """Get the rating of the movie (audience rating or user rating)"""
        try:
            # Try audience rating first, then user rating
            rating = movie.audienceRating if hasattr(movie, 'audienceRating') and movie.audienceRating else None
            if not rating and hasattr(movie, 'rating'):
                rating = movie.rating
            return rating if rating else 0
        except Exception as e:
            print(f"Error getting rating: {e}")
            return 0
