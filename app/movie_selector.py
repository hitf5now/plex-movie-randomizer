import random
from datetime import datetime
from app.models import PassedMovie
from app.plex_api import PlexAPI

class MovieSelector:
    def __init__(self, user, plex_api):
        self.user = user
        self.plex = plex_api
        self.preferences = user.preferences

    def get_decade_from_year(self, year):
        """Convert year to decade string (e.g., 1995 -> '1990s')"""
        if not year:
            return None
        decade = (year // 10) * 10
        return f"{decade}s"

    def filter_movies(self, movies):
        """Apply all active filters to the movie list based on filter mode"""
        filtered_movies = movies

        # Always: Exclude watched movies (if preference is set)
        if self.preferences and self.preferences.exclude_watched:
            filtered_movies = [m for m in filtered_movies if not getattr(m, 'isWatched', False)]

        # Always: Exclude passed movies
        passed_keys = self._get_passed_movie_keys()
        filtered_movies = [m for m in filtered_movies if str(m.ratingKey) not in passed_keys]

        # Apply mode-specific filters
        if self.preferences:
            filter_mode = self.preferences.filter_mode or 'linked'

            if filter_mode == 'linked':
                # LINKED MODE: Filter by actors OR directors from last watched
                link_type = self.preferences.link_type

                if link_type == 'actors':
                    filtered_movies = self._filter_by_actors(filtered_movies)
                elif link_type == 'directors':
                    filtered_movies = self._filter_by_director(filtered_movies)

            else:
                # SEARCH MODE: Filter by decade and/or specific actor
                if self.preferences.filter_decade:
                    filtered_movies = self._filter_by_decade(filtered_movies)

                if self.preferences.filter_actor:
                    filtered_movies = self._filter_by_specific_actor(filtered_movies)

        return filtered_movies

    def _get_passed_movie_keys(self):
        """Get list of rating keys for movies that are currently passed (not expired)"""
        passed_movies = PassedMovie.query.filter_by(user_id=self.user.id).all()
        # Only include non-expired passes - store as strings for comparison
        return set([str(pm.plex_rating_key) for pm in passed_movies if not pm.is_expired])

    def _filter_by_actors(self, movies):
        """Filter to only include movies with actors from the last watched movie"""
        last_watched = self.plex.get_last_watched_movie(self.user.plex_username)
        if not last_watched:
            return movies

        last_actors = set(self.plex.get_movie_actors(last_watched))
        if not last_actors:
            return movies

        filtered = []
        for movie in movies:
            movie_actors = set(self.plex.get_movie_actors(movie))
            # Include if there's any overlap in actors
            if movie_actors.intersection(last_actors):
                filtered.append(movie)

        return filtered

    def _filter_by_director(self, movies):
        """Filter to only include movies from the same director as last watched movie"""
        last_watched = self.plex.get_last_watched_movie(self.user.plex_username)
        if not last_watched:
            return movies

        last_directors = set(self.plex.get_movie_directors(last_watched))
        if not last_directors:
            return movies

        filtered = []
        for movie in movies:
            movie_directors = set(self.plex.get_movie_directors(movie))
            # Include if there's any overlap in directors
            if movie_directors.intersection(last_directors):
                filtered.append(movie)

        return filtered

    def _filter_by_decade(self, movies):
        """Filter movies by specified decade"""
        target_decade = self.preferences.filter_decade
        if not target_decade:
            return movies

        filtered = []
        for movie in movies:
            year = self.plex.get_movie_year(movie)
            if year:
                movie_decade = self.get_decade_from_year(year)
                if movie_decade == target_decade:
                    filtered.append(movie)

        return filtered

    def _filter_by_specific_actor(self, movies):
        """Filter movies by specific actor name"""
        target_actor = self.preferences.filter_actor.lower()
        if not target_actor:
            return movies

        filtered = []
        for movie in movies:
            actors = self.plex.get_movie_actors(movie)
            # Check if any actor name contains the target actor string
            if any(target_actor in actor.lower() for actor in actors):
                filtered.append(movie)

        return filtered

    def group_movies_by_rating(self, movies):
        """Group movies by their rating (rounded down to integer)"""
        rating_groups = {}

        for movie in movies:
            rating = self.plex.get_movie_rating(movie)
            # Round down to integer (e.g., 4.5 -> 4)
            rating_group = int(rating) if rating else 0

            if rating_group not in rating_groups:
                rating_groups[rating_group] = []

            rating_groups[rating_group].append(movie)

        return rating_groups

    def get_random_movie(self, rating_group):
        """Get a random movie from a specific rating group"""
        if not rating_group or len(rating_group) == 0:
            return None
        return random.choice(rating_group)

    def recommend_movie(self):
        """
        Main recommendation method that:
        1. Gets all movies
        2. Applies filters
        3. Groups by rating
        4. Returns random movie from highest rating group (includes unrated movies)
        """
        # Get all movies from Plex
        all_movies = self.plex.get_all_movies()
        if not all_movies:
            return None, "No movies found in library"

        # Apply filters
        filtered_movies = self.filter_movies(all_movies)
        if not filtered_movies:
            return None, "No movies match the current filters"

        # Group by rating
        rating_groups = self.group_movies_by_rating(filtered_movies)
        if not rating_groups:
            return None, "No movies available"

        # Get highest rating group (excluding unrated if there are rated movies)
        rated_groups = {k: v for k, v in rating_groups.items() if k > 0}

        if rated_groups:
            # If we have rated movies, select from highest rated group
            highest_rating = max(rated_groups.keys())
            highest_group = rated_groups[highest_rating].copy()

            # IMPORTANT: Include unrated movies (rating 0) with the highest rated group
            # This ensures unrated movies are always considered for selection
            if 0 in rating_groups:
                highest_group.extend(rating_groups[0])
        else:
            # If only unrated movies exist, use them
            highest_group = rating_groups.get(0, [])

        if not highest_group:
            return None, "No movies available"

        # Get random movie from combined group
        selected_movie = self.get_random_movie(highest_group)

        return selected_movie, None

    def get_linking_person(self, movie):
        """
        Determine which actor or director from last watched appears in this movie (for Linked Mode)
        Returns: dict with 'type' ('actor' or 'director'), 'name', and 'image_url'
        """
        if not self.preferences or not self.preferences.filter_mode == 'linked':
            return None

        last_watched = self.plex.get_last_watched_movie(self.user.plex_username)
        if not last_watched:
            return None

        link_type = self.preferences.link_type

        if link_type == 'actors':
            # Find common actors
            last_actors = set(self.plex.get_movie_actors(last_watched))
            movie_actors = set(self.plex.get_movie_actors(movie))
            common = last_actors.intersection(movie_actors)
            if common:
                # Return first common actor
                actor_name = list(common)[0]
                return {
                    'type': 'actor',
                    'name': actor_name,
                    'image_url': None  # Plex API doesn't easily expose actor images
                }

        elif link_type == 'directors':
            # Find common directors
            last_directors = set(self.plex.get_movie_directors(last_watched))
            movie_directors = set(self.plex.get_movie_directors(movie))
            common = last_directors.intersection(movie_directors)
            if common:
                # Return first common director
                director_name = list(common)[0]
                return {
                    'type': 'director',
                    'name': director_name,
                    'image_url': None  # Plex API doesn't easily expose director images
                }

        return None

    def get_movie_info(self, movie):
        """Get formatted movie information"""
        if not movie:
            return None

        # Get linking person info if in linked mode
        linking_person = self.get_linking_person(movie)

        return {
            'rating_key': movie.ratingKey,
            'title': movie.title,
            'year': self.plex.get_movie_year(movie),
            'rating': self.plex.get_movie_rating(movie),
            'summary': movie.summary if hasattr(movie, 'summary') else '',
            'poster': movie.thumbUrl if hasattr(movie, 'thumbUrl') else '',
            'actors': self.plex.get_movie_actors(movie)[:5],  # Top 5 actors
            'directors': self.plex.get_movie_directors(movie),
            'duration': movie.duration if hasattr(movie, 'duration') else 0,
            'linked_by': linking_person  # Info about which actor/director created the link
        }
