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

    def play_movie_direct(self, rating_key, selected_client_identifier=None):
        """Play a movie using direct server-proxied API commands (NEW METHOD)

        This simplified method uses the Plex server to proxy playback commands
        to clients, which is more reliable than direct client connections.
        Based on official Plex API documentation and PlayQueue approach.

        Args:
            rating_key: The Plex rating key for the movie
            selected_client_identifier: Machine identifier of the target client

        Returns:
            dict: {
                'success': bool,
                'error': str or None,
                'deep_link': str or None,
                'method': str
            }
        """
        if not self.server:
            return {
                'success': False,
                'error': 'Not connected to Plex server',
                'deep_link': None,
                'method': None
            }

        try:
            # Get the movie
            movie = self.get_movie_details(rating_key)
            if not movie:
                return {
                    'success': False,
                    'error': 'Movie not found',
                    'deep_link': None,
                    'method': None
                }

            print(f"\n=== Direct API Playback: {movie.title} ===")

            # Generate deep link as universal fallback
            server_id = self.server.machineIdentifier
            deep_link = f"plex://play/?key={movie.key}&server={server_id}"
            print(f"Deep link generated: {deep_link}")

            # If no client selected, return deep link immediately
            if not selected_client_identifier:
                return {
                    'success': False,
                    'error': 'No client selected. Use the deep link to play on your device.',
                    'deep_link': deep_link,
                    'method': 'deep_link'
                }

            # Method 1: Try PlayQueue with direct client connection
            print(f"Method 1: Looking for client with ID: {selected_client_identifier}")

            try:
                # Get all available clients from account
                from plexapi.myplex import MyPlexAccount
                account = MyPlexAccount(token=self.token)
                devices = account.devices()

                # Find the target device
                target_device = None
                for device in devices:
                    if device.clientIdentifier == selected_client_identifier:
                        target_device = device
                        break

                if not target_device:
                    print(f"  Client not found in account devices")
                else:
                    print(f"  Found device: {target_device.name} ({target_device.product})")

                    # Try to connect to the device
                    try:
                        client = target_device.connect()
                        if client:
                            from plexapi.client import PlexClient
                            if isinstance(client, PlexClient):
                                print(f"  Connected to client, attempting playback...")

                                # Create PlayQueue on server
                                from plexapi.playqueue import PlayQueue
                                pq = PlayQueue.create(self.server, movie)
                                print(f"  PlayQueue created with ID: {pq.playQueueID}")

                                # Play using PlayQueue
                                client.playMedia(pq)
                                print(f"  ✓ SUCCESS! Playback initiated via PlayQueue")

                                return {
                                    'success': True,
                                    'error': None,
                                    'deep_link': deep_link,
                                    'method': 'playqueue'
                                }
                    except Exception as e:
                        print(f"  PlayQueue method failed: {e}")

            except Exception as e:
                print(f"Method 1 failed: {e}")

            # Method 2: Try server-proxied playback command with headers
            print(f"Method 2: Trying server-proxied playback command with client headers...")

            try:
                from plexapi.playqueue import PlayQueue
                pq = PlayQueue.create(self.server, movie)
                print(f"  PlayQueue created with ID: {pq.playQueueID}")

                # Send command through server with X-Plex-Target-Client-Identifier header
                params = {
                    'type': 'video',
                    'providerIdentifier': 'com.plexapp.plugins.library',
                    'containerKey': f'/playQueues/{pq.playQueueID}',
                    'key': movie.key,
                    'offset': '0',
                    'commandID': '1'
                }

                # Add target client header
                headers = {
                    'X-Plex-Target-Client-Identifier': selected_client_identifier
                }

                play_url = '/player/playback/playMedia'
                result = self.server.query(play_url, method=self.server._session.post, params=params, headers=headers)
                print(f"  ✓ Server-proxied command sent successfully with headers")

                return {
                    'success': True,
                    'error': None,
                    'deep_link': deep_link,
                    'method': 'server_proxy'
                }

            except Exception as e:
                print(f"Method 2 failed: {e}")
                import traceback
                traceback.print_exc()

            # Method 3: Try using server.client() to get client object
            print(f"Method 3: Trying to get client from server.client()...")

            try:
                # Get all available clients
                clients = self.server.clients()
                print(f"  Found {len(clients)} active client(s)")

                # Try to find our target client
                target_client = None
                for client in clients:
                    if hasattr(client, 'machineIdentifier') and client.machineIdentifier == selected_client_identifier:
                        target_client = client
                        break

                if target_client:
                    print(f"  Found client in server.clients(): {target_client.title}")
                    from plexapi.playqueue import PlayQueue
                    pq = PlayQueue.create(self.server, movie)
                    print(f"  PlayQueue created with ID: {pq.playQueueID}")
                    target_client.playMedia(pq)
                    print(f"  ✓ SUCCESS! Playback via server.client() and PlayQueue")

                    return {
                        'success': True,
                        'error': None,
                        'deep_link': deep_link,
                        'method': 'server_client'
                    }
                else:
                    print(f"  Client not found in server.clients()")
                    print(f"  This means the client is not advertising for remote control")

            except Exception as e:
                print(f"Method 3 failed: {e}")
                import traceback
                traceback.print_exc()

            # Method 4: Try to find client in active sessions and control via session player
            print(f"Method 4: Checking active sessions for target client...")

            try:
                sessions = self.server.sessions()
                print(f"  Found {len(sessions)} active session(s)")

                for session in sessions:
                    if session.players:
                        for player in session.players:
                            player_id = getattr(player, 'machineIdentifier', None)
                            if player_id == selected_client_identifier:
                                print(f"  Found target client in active session: {player.title}")
                                print(f"  Attempting to get client from session player...")

                                try:
                                    # Try to get the client by title
                                    client = self.server.client(player.title)
                                    if client:
                                        from plexapi.playqueue import PlayQueue
                                        pq = PlayQueue.create(self.server, movie)
                                        print(f"  PlayQueue created with ID: {pq.playQueueID}")
                                        client.playMedia(pq)
                                        print(f"  ✓ SUCCESS! Playback via session client and PlayQueue")

                                        return {
                                            'success': True,
                                            'error': None,
                                            'deep_link': deep_link,
                                            'method': 'session_client'
                                        }
                                except Exception as client_err:
                                    print(f"  Could not control client from session: {client_err}")

                print(f"  Target client not found in any active sessions")

            except Exception as e:
                print(f"Method 4 failed: {e}")
                import traceback
                traceback.print_exc()

            # All automated methods failed - return deep link as fallback
            print(f"\nAll automated methods failed.")
            print(f"This usually means the client is not configured for remote control.")
            print(f"Providing deep link fallback...\n")

            # Provide specific error message based on device type
            if target_device and 'Windows' in target_device.product:
                error_msg = """Could not start playback automatically on Plex for Windows.

To enable remote control:
1. Open Plex for Windows
2. Go to Settings → Network
3. Enable "Advertise as player"
4. Restart Plex for Windows

Or click the "Open in Plex App" button below to play manually."""
            elif target_device and 'Android' in target_device.product:
                error_msg = """Could not start playback automatically.

For best results, try playing something on your device first, then use this app.

Or click the "Open in Plex App" button below to play manually."""
            else:
                error_msg = """Could not start playback automatically.

This client may not support remote control via the Plex API.

Click the "Open in Plex App" button below to play manually."""

            return {
                'success': False,
                'error': error_msg,
                'deep_link': deep_link,
                'method': 'deep_link'
            }

        except Exception as e:
            print(f"Error in play_movie_direct: {e}")
            import traceback
            traceback.print_exc()

            # Try to generate deep link even on error
            try:
                movie = self.get_movie_details(rating_key)
                if movie:
                    server_id = self.server.machineIdentifier
                    deep_link = f"plex://play/?key={movie.key}&server={server_id}"
                    return {
                        'success': False,
                        'error': str(e),
                        'deep_link': deep_link,
                        'method': 'deep_link'
                    }
            except:
                pass

            return {
                'success': False,
                'error': str(e),
                'deep_link': None,
                'method': None
            }

    def play_movie(self, rating_key, player_name=None, selected_client_name=None, selected_client_identifier=None):
        """Play a movie on the specified player or default player (LEGACY METHOD)

        This method tries multiple approaches:
        1. If selected_client specified - Only try that specific client
        2. server.clients() - Clients with remote control enabled
        3. Active sessions - Clients currently playing something
        4. Account devices - Try to connect to registered devices

        Args:
            rating_key: The Plex rating key for the movie
            player_name: (deprecated) Name of the player to use
            selected_client_name: Name of the pre-selected client from user preferences
            selected_client_identifier: Machine identifier of the pre-selected client

        Returns:
            tuple: (success: bool, error_message: str or None)
        """
        if not self.server:
            return False, "Not connected to Plex server"
        try:
            movie = self.get_movie_details(rating_key)
            if not movie:
                return False, "Movie not found"

            print(f"\n=== Attempting to play movie: {movie.title} ===")

            # If user has selected a specific client, try multiple methods to connect
            if selected_client_name and selected_client_identifier:
                print(f"User has pre-selected client: {selected_client_name}")
                print(f"Attempting to connect to selected client using multiple methods...")

                # Method 1: Try server.clients() first (fastest if client is advertising)
                print(f"  Method 1: Checking if '{selected_client_name}' is in server.clients()...")
                try:
                    clients = self.server.clients()
                    for client in clients:
                        if hasattr(client, 'machineIdentifier') and client.machineIdentifier == selected_client_identifier:
                            print(f"  ✓ Found '{selected_client_name}' in active clients!")
                            print(f"  Sending playMedia command...")
                            client.playMedia(movie)
                            print(f"  SUCCESS! Movie playback initiated on {selected_client_name}")
                            return True, None
                    print(f"  '{selected_client_name}' not found in active clients")
                except Exception as e:
                    print(f"  Method 1 failed: {e}")

                # Method 2: Try active sessions (if device is currently playing something)
                print(f"  Method 2: Checking if '{selected_client_name}' is in active sessions...")
                try:
                    sessions = self.server.sessions()
                    print(f"    Found {len(sessions)} active session(s)")

                    for idx, session in enumerate(sessions):
                        print(f"    Session {idx + 1}: {session.title if hasattr(session, 'title') else 'Unknown'}")
                        if session.players:
                            for player in session.players:
                                player_id = getattr(player, 'machineIdentifier', 'no-id')
                                player_title = getattr(player, 'title', 'no-title')
                                print(f"      Player: {player_title} (ID: {player_id})")
                                print(f"      Looking for ID: {selected_client_identifier}")

                                if player_id == selected_client_identifier:
                                    print(f"  ✓ MATCH! Found '{selected_client_name}' in active session!")
                                    # Try to get client by title
                                    try:
                                        client = self.server.client(player_title)
                                        if client:
                                            print(f"  Got client object, sending playMedia command...")
                                            client.playMedia(movie)
                                            print(f"  SUCCESS! Movie playback initiated on {selected_client_name}")
                                            return True, None
                                        else:
                                            print(f"  server.client() returned None")
                                    except Exception as client_err:
                                        print(f"  Could not get client object from session: {client_err}")
                        else:
                            print(f"      No players in this session")

                    print(f"  '{selected_client_name}' (ID: {selected_client_identifier}) not found in active sessions")
                except Exception as e:
                    print(f"  Method 2 failed: {e}")
                    import traceback
                    traceback.print_exc()

                # Method 3: Try device.connect() from account devices
                print(f"  Method 3: Trying device.connect() for '{selected_client_name}'...")
                try:
                    from plexapi.myplex import MyPlexAccount
                    account = MyPlexAccount(token=self.token)
                    devices = account.devices()

                    # Find the selected device
                    selected_device = None
                    for device in devices:
                        if device.clientIdentifier == selected_client_identifier:
                            selected_device = device
                            break

                    if not selected_device:
                        error_msg = f"Selected client '{selected_client_name}' not found in your account. Please refresh and select again."
                        print(f"  ERROR: {error_msg}")
                        return False, error_msg

                    # Check if it's a server (shouldn't be, but verify)
                    product = getattr(selected_device, 'product', '').lower()
                    if 'server' in product or 'media server' in product:
                        error_msg = f"'{selected_client_name}' is a server, not a client. Please select a playback device."
                        print(f"  ERROR: {error_msg}")
                        return False, error_msg

                    # Try to connect to the selected device
                    print(f"  Attempting device.connect() for {selected_device.name} ({selected_device.product})...")
                    device_connection = selected_device.connect()

                    if device_connection:
                        from plexapi.client import PlexClient
                        if isinstance(device_connection, PlexClient):
                            print(f"  ✓ Connected to {selected_device.name}")
                            print(f"  Sending playMedia command...")
                            device_connection.playMedia(movie)
                            print(f"  SUCCESS! Movie playback initiated on {selected_device.name}")
                            return True, None
                        else:
                            print(f"  Connected but object is not a PlexClient: {type(device_connection)}")
                    else:
                        print(f"  device.connect() returned None")

                except Exception as e:
                    print(f"  Method 3 failed: {e}")
                    import traceback
                    traceback.print_exc()

                # All methods failed
                error_msg = f"""Could not connect to '{selected_client_name}'.

Make sure:
1. Plex is OPEN and RUNNING on the device
2. The device is not sleeping or locked
3. The device is on the same network as the Plex server

Tip: Try playing something on '{selected_client_name}' first, then use this app."""
                print(f"\nERROR: {error_msg}")
                return False, error_msg

            # No selected client - try all methods (original behavior)
            print("No pre-selected client. Trying all available methods...")

            # Try Method 1: Get clients via server.clients()
            print("Method 1: Checking server.clients()...")
            clients = self.server.clients()
            print(f"  Found {len(clients)} client(s) with remote control enabled")

            if clients:
                client = clients[0]
                if player_name:
                    client = next((c for c in clients if c.title == player_name), clients[0])
                print(f"  Playing on client: {client.title}")
                client.playMedia(movie)
                return True, None

            # Try Method 2: Get clients from active sessions
            print("Method 2: Checking active sessions for playback clients...")
            try:
                sessions = self.server.sessions()
                print(f"  Found {len(sessions)} active session(s)")

                if sessions:
                    # Use the player from the first active session
                    session = sessions[0]
                    if session.players:
                        player = session.players[0]
                        print(f"  Found active player: {player.title}")
                        print(f"  Player machine identifier: {player.machineIdentifier}")

                        # Check if this is a web player - skip it as they can't be remotely controlled
                        web_players = ['chrome', 'firefox', 'safari', 'edge', 'opera', 'plex web']
                        is_web_player = any(wp in player.title.lower() for wp in web_players)

                        if is_web_player:
                            print(f"  ⚠️  Web players (browsers) cannot be remotely controlled")
                            print(f"  Please use a native Plex app (Android, iOS, TV, Windows app)")
                            print(f"  Skipping to Method 3 to try other devices...")
                        else:
                            # Try multiple methods to control the player
                            try:
                                # Method 2a: Try to get client by title from server
                                print(f"  Method 2a: Trying server.client('{player.title}')...")
                                try:
                                    client = self.server.client(player.title)
                                    if client:
                                        print(f"  SUCCESS! Found client: {client.title}")
                                        print(f"  Sending playMedia command to client...")
                                        client.playMedia(movie)
                                        return True, None
                                except Exception as e:
                                    print(f"  Method 2a failed: {e}")

                                # Method 2b: Create a playQueue for native apps
                                print(f"  Method 2b: Creating playQueue for native app playback...")
                                try:
                                    from plexapi.playqueue import PlayQueue
                                    playqueue = PlayQueue.create(self.server, movie)
                                    print(f"  PlayQueue created with ID: {playqueue.playQueueID}")

                                    params = {
                                        'type': 'video',
                                        'providerIdentifier': 'com.plexapp.plugins.library',
                                        'commandID': '1',
                                        'machineIdentifier': player.machineIdentifier,
                                        'containerKey': f'/playQueues/{playqueue.playQueueID}',
                                        'key': movie.key,
                                        'offset': '0'
                                    }

                                    # Use the player protocol if available
                                    if hasattr(player, 'protocol'):
                                        params['protocol'] = player.protocol
                                    if hasattr(player, 'address'):
                                        params['address'] = player.address
                                    if hasattr(player, 'port'):
                                        params['port'] = player.port

                                    print(f"  Sending playback command via server (POST)...")
                                    play_url = '/player/playback/playMedia'
                                    result = self.server.query(play_url, method=self.server._session.post, params=params)
                                    print(f"  Playback command sent successfully!")
                                    return True, None

                                except Exception as e:
                                    print(f"  Method 2b failed: {e}")
                                    import traceback
                                    traceback.print_exc()

                                # Method 2c: Direct playMedia on player object
                                print(f"  Method 2c: Trying direct player.playMedia()...")
                                if hasattr(player, 'playMedia'):
                                    player.playMedia(movie)
                                    print(f"  Direct playMedia sent to player")
                                    return True, None
                                else:
                                    print(f"  Player object doesn't have playMedia method")

                            except Exception as player_error:
                                print(f"  All Method 2 attempts failed: {player_error}")
                                import traceback
                                traceback.print_exc()
                    else:
                        print(f"  Session found but no player available")
            except Exception as e:
                print(f"  Could not use session client: {e}")
                import traceback
                traceback.print_exc()

            # Try Method 3: Get devices from account and try to connect
            print("Method 3: Trying to connect to account devices...")
            try:
                from plexapi.myplex import MyPlexAccount
                account = MyPlexAccount(token=self.token)
                devices = account.devices()
                print(f"  Found {len(devices)} device(s) on account")

                # Filter out servers - we only want client devices
                client_devices = []
                for d in devices:
                    product = getattr(d, 'product', '').lower()
                    # Skip servers
                    if 'server' in product or 'media server' in product:
                        print(f"  Skipping server device: {d.name} ({d.product})")
                        continue
                    # Only include devices with connections
                    if len(d.connections) > 0:
                        client_devices.append(d)

                print(f"  Found {len(client_devices)} client device(s) with active connections")

                for device in client_devices:
                    try:
                        print(f"  Attempting to connect to: {device.name} ({device.product})")
                        # Try to connect
                        device_connection = device.connect()

                        if device_connection:
                            # Check if this is a PlexClient (not a server)
                            from plexapi.client import PlexClient
                            if isinstance(device_connection, PlexClient):
                                print(f"  ✓ Connected to client: {device.name}")
                                print(f"  Sending playMedia command...")
                                device_connection.playMedia(movie)
                                print(f"  SUCCESS! Movie playback initiated on {device.name}")
                                return True, None
                            else:
                                print(f"  Connected object is not a PlexClient (type: {type(device_connection).__name__})")
                    except Exception as e:
                        print(f"  Could not use {device.name}: {e}")
                        continue

                print(f"  No client devices were able to accept playback commands")

            except Exception as e:
                print(f"  Could not use account devices: {e}")
                import traceback
                traceback.print_exc()

            # No methods worked
            error_msg = """No playable clients found. To enable playback:

1. Open Plex on a device
2. In Plex Settings → enable "Advertise as player" and "Enable remote control"
3. Or, start playing any movie on your device, then try again from this app

Devices found but not playable: Check Plex client settings."""

            print(f"\n{error_msg}")
            return False, error_msg

        except Exception as e:
            error_msg = str(e)
            print(f"Error playing movie: {error_msg}")
            import traceback
            traceback.print_exc()
            return False, f"Error playing movie: {error_msg}"

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

    def get_or_create_playlist(self, user_preference, playlist_name="Up Next"):
        """Get existing playlist by stored ID or create new one

        This method checks if a playlist exists by the ID stored in user preferences.
        If the playlist was deleted or doesn't exist, it creates a new one and updates
        the stored ID in the database.

        Args:
            user_preference: UserPreference model instance for the current user
            playlist_name: Name to use when creating a new playlist (default: "Up Next")

        Returns:
            Playlist object or None if error
        """
        if not self.server:
            print("ERROR: Not connected to Plex server")
            return None

        try:
            from app import db

            # Get the movies library section
            movies_section = self.get_movie_library()
            if not movies_section:
                print("ERROR: Could not access Movies library")
                return None

            # Check if user has a stored playlist ID
            if user_preference.playlist_id:
                print(f"Checking for playlist with ID: {user_preference.playlist_id}")
                try:
                    # Try to get the playlist by stored ID
                    playlist = self.server.playlist(user_preference.playlist_id)
                    if playlist:
                        print(f"✓ Found existing playlist: {playlist.title} (ID: {playlist.ratingKey})")
                        return playlist
                except Exception as e:
                    print(f"Stored playlist not found (may have been deleted): {e}")
                    # Will create new playlist below

            # Playlist doesn't exist or was deleted - create new one
            print(f"Creating new playlist: {playlist_name}")
            playlist = self.server.createPlaylist(
                title=playlist_name,
                section=movies_section,
                items=[]
            )
            print(f"✓ Created playlist: {playlist.title} (ID: {playlist.ratingKey})")

            # Store the playlist ID in user preferences
            user_preference.playlist_id = str(playlist.ratingKey)
            db.session.commit()
            print(f"✓ Saved playlist ID to database: {playlist.ratingKey}")

            return playlist

        except Exception as e:
            print(f"Error in get_or_create_playlist: {e}")
            import traceback
            traceback.print_exc()
            return None

    def add_movie_to_playlist(self, movie_rating_key, user_preference):
        """Add a movie to the user's playlist

        Args:
            movie_rating_key: The rating key of the movie to add
            user_preference: UserPreference model instance for the current user

        Returns:
            tuple: (success: bool, message: str)
        """
        if not self.server:
            return False, "Not connected to Plex server"

        try:
            print(f"\n=== Adding Movie to Playlist ===")

            # Get the movie from local library
            movie = self.get_movie_details(movie_rating_key)
            if not movie:
                return False, "Movie not found"

            print(f"Movie: {movie.title}")

            # Get or create the playlist
            playlist = self.get_or_create_playlist(user_preference)
            if not playlist:
                return False, "Could not access or create playlist"

            # Check if movie is already in playlist
            try:
                playlist_items = playlist.items()
                for item in playlist_items:
                    if item.ratingKey == movie.ratingKey:
                        print(f"Movie already in playlist")
                        return True, f"'{movie.title}' is already in your playlist"
            except Exception as e:
                print(f"Note: Could not check playlist items: {e}")

            # Add the movie to the playlist
            playlist.addItems(movie)
            print(f"✓ Added '{movie.title}' to playlist '{playlist.title}'")

            # Auto-cleanup watched movies from playlist
            self.cleanup_watched_movies_from_playlist(user_preference)

            return True, f"Added '{movie.title}' to your playlist!"

        except Exception as e:
            error_msg = str(e)
            print(f"Error adding movie to playlist: {error_msg}")
            import traceback
            traceback.print_exc()
            return False, f"Error adding movie to playlist: {error_msg}"

    def cleanup_watched_movies_from_playlist(self, user_preference):
        """Remove watched movies from the user's playlist

        This method checks all items in the playlist and removes any that have been watched.

        Args:
            user_preference: UserPreference model instance for the current user

        Returns:
            int: Number of movies removed from playlist
        """
        if not self.server:
            print("ERROR: Not connected to Plex server")
            return 0

        try:
            print(f"\n=== Cleaning Up Watched Movies from Playlist ===")

            # Get the playlist
            playlist = self.get_or_create_playlist(user_preference)
            if not playlist:
                print("Could not access playlist for cleanup")
                return 0

            # Get all items in the playlist
            playlist_items = playlist.items()
            print(f"Playlist has {len(playlist_items)} item(s)")

            # Find watched movies
            watched_items = []
            for item in playlist_items:
                if item.isWatched:
                    watched_items.append(item)
                    print(f"  Found watched movie: {item.title}")

            # Remove watched movies
            if watched_items:
                playlist.removeItems(watched_items)
                print(f"✓ Removed {len(watched_items)} watched movie(s) from playlist")
                return len(watched_items)
            else:
                print("No watched movies to remove")
                return 0

        except Exception as e:
            print(f"Error cleaning up playlist: {e}")
            import traceback
            traceback.print_exc()
            return 0

    def get_available_clients(self):
        """Get list of available Plex clients for playback

        This method tries multiple approaches to find Plex clients:
        1. server.clients() - Active connected clients
        2. MyPlex account devices - All devices on the account
        3. Active sessions - Currently playing clients

        Returns:
            list: List of dictionaries with client information
        """
        if not self.server:
            print("ERROR: No server connection")
            return []

        client_list = []

        try:
            print("\n=== Checking for Plex Clients ===")

            # Method 1: Try server.clients() - Gets currently connected clients for remote control
            print("Method 1: Checking server.clients()...")
            try:
                clients = self.server.clients()
                print(f"  Found {len(clients)} client(s) via server.clients()")
                for client in clients:
                    print(f"    - {client.title} ({client.product})")
                    client_info = {
                        'title': client.title,
                        'product': client.product,
                        'platform': getattr(client, 'platform', 'Unknown'),
                        'platformVersion': getattr(client, 'platformVersion', 'Unknown'),
                        'device': getattr(client, 'device', 'Unknown'),
                        'machineIdentifier': getattr(client, 'machineIdentifier', 'Unknown'),
                        'source': 'server.clients()'
                    }
                    client_list.append(client_info)
            except Exception as e:
                print(f"  Error with server.clients(): {e}")

            # Method 2: Try MyPlex account devices
            print("Method 2: Checking MyPlex account devices...")
            try:
                from plexapi.myplex import MyPlexAccount
                account = MyPlexAccount(token=self.token)
                devices = account.devices()
                print(f"  Found {len(devices)} device(s) on MyPlex account")
                for device in devices:
                    print(f"    - {device.name} ({device.product}) - Connections: {len(device.connections)}")
                    # Only add if not already in list
                    if not any(c['title'] == device.name for c in client_list):
                        client_info = {
                            'title': device.name,
                            'product': device.product,
                            'platform': getattr(device, 'platform', 'Unknown'),
                            'platformVersion': getattr(device, 'platformVersion', 'Unknown'),
                            'device': getattr(device, 'device', 'Unknown'),
                            'machineIdentifier': device.clientIdentifier,
                            'source': 'account.devices()'
                        }
                        client_list.append(client_info)
            except Exception as e:
                print(f"  Error getting account devices: {e}")

            # Method 3: Check active sessions (currently playing)
            print("Method 3: Checking active sessions...")
            try:
                sessions = self.server.sessions()
                print(f"  Found {len(sessions)} active session(s)")
                for session in sessions:
                    player = session.players[0] if session.players else None
                    if player:
                        print(f"    - {player.title} playing '{session.title}'")
                        if not any(c['title'] == player.title for c in client_list):
                            client_info = {
                                'title': player.title,
                                'product': getattr(player, 'product', 'Unknown'),
                                'platform': getattr(player, 'platform', 'Unknown'),
                                'platformVersion': getattr(player, 'platformVersion', 'Unknown'),
                                'device': getattr(player, 'device', 'Unknown'),
                                'machineIdentifier': getattr(player, 'machineIdentifier', 'Unknown'),
                                'source': 'sessions()'
                            }
                            client_list.append(client_info)
            except Exception as e:
                print(f"  Error getting sessions: {e}")

            print(f"=== Total unique clients found: {len(client_list)} ===\n")
            return client_list

        except Exception as e:
            print(f"Error in get_available_clients: {e}")
            import traceback
            traceback.print_exc()
            return []
