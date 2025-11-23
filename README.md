# Plex Movie Selector

A web-based application that helps you select a random movie to watch from your Plex server library with intelligent filtering and rating-based recommendations.

## Features

- **Smart Rating Grouping**: Movies are grouped by rating (rounded down), recommendations start from the highest-rated group
- **Multi-User Support**: Each user has their own preferences and passed movie list
- **Advanced Filtering**:
  - Exclude watched movies
  - Exclude movies with actors from your last watched movie
  - Exclude movies from the same director as your last watched movie
  - Filter by decade (1950s-2020s)
  - Filter by specific actor
- **Pass System**: Pass on movies and they'll be excluded from recommendations for 6 months
- **Direct Playback**: Play recommended movies directly on your active Plex client
- **Passed Movies Management**: View and manage your passed movies list

## Requirements

- Docker and Docker Compose (recommended)
- OR Python 3.11+ (for local development)
- Active Plex Media Server
- Plex account with access to the server

## Installation & Setup

### Option 1: Docker (Recommended)

1. **Clone or download this repository**

2. **Configure environment variables**

   Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and set your values:
   ```
   SECRET_KEY=your-secure-random-secret-key
   PLEX_SERVER_URL=http://your-plex-server:32400
   ```

   **Important**:
   - If running on the same machine as Plex, use `http://host.docker.internal:32400`
   - If Plex is on a different machine, use the actual IP address

3. **Start the application**

   ```bash
   docker-compose up -d
   ```

   The application will be available at `http://localhost:5000`

4. **Stop the application**

   ```bash
   docker-compose down
   ```

### Option 2: Local Development

1. **Create a virtual environment**

   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On Linux/Mac
   source venv/bin/activate
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**

   Copy `.env.example` to `.env` and configure your settings

4. **Run the application**

   ```bash
   python run.py
   ```

   The application will be available at `http://localhost:5000`

## Usage

### Initial Setup

1. Navigate to `http://localhost:5000`
2. Log in with your Plex credentials (username/email and password)
3. The application will authenticate with Plex and create your user profile

### Getting Recommendations

1. **Configure Filters** (optional):
   - Toggle on/off the filter options in the left sidebar
   - Select a specific decade or actor if desired
   - Click "Apply Filters" to save your preferences

2. **Get a Recommendation**:
   - Click "Get Recommendation" button
   - The app will show a random movie from the highest-rated group that matches your filters

3. **Take Action**:
   - **Play Movie**: Starts playing the movie on your active Plex client
   - **Pass**: Excludes this movie from recommendations for 6 months and gets another recommendation
   - **Get Another Recommendation**: Gets a different movie from the current rating group

### Managing Passed Movies

1. Navigate to "Passed Movies" from the top menu
2. View all movies you've passed on with their expiration dates
3. Remove movies from the passed list to make them available again

## How It Works

### Rating Groups

Movies are grouped by their Plex rating rounded down to the nearest integer:
- A movie with a 4.5 rating is grouped as a "4-star" movie
- A movie with a 7.8 rating is grouped as a "7-star" movie

Recommendations always start from the highest-rated group available after applying filters.

### Filter Logic

Filters work cumulatively to narrow down the movie list:

1. **Exclude Watched**: Removes movies you've already watched in Plex
2. **Exclude Same Actors**: Excludes movies featuring any actors from your last watched movie
3. **Exclude Same Director**: Excludes movies from the director(s) of your last watched movie
4. **Decade Filter**: Only shows movies from the selected decade
5. **Actor Filter**: Only shows movies featuring the specified actor
6. **Passed Movies**: Automatically excludes movies you've passed on (within the 6-month window)

### Pass System

When you pass on a movie:
- The movie is flagged in the database
- It's excluded from recommendations for 6 months
- The next recommendation comes from the same rating group
- When all movies in a rating group are watched or passed, recommendations move to the next lower rating group

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SECRET_KEY` | Flask secret key for sessions | `dev-secret-key-change-in-production` |
| `PLEX_SERVER_URL` | URL to your Plex server | `http://localhost:32400` |
| `DATABASE_URI` | SQLite database location | `sqlite:///movie_selector.db` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `5000` |
| `DEBUG` | Debug mode (True/False) | `False` |

### Docker Volumes

The `instance` directory is mounted as a volume to persist the SQLite database between container restarts.

## Project Structure

```
movie_selector/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── models.py            # Database models
│   ├── plex_api.py          # Plex API integration
│   ├── movie_selector.py    # Movie filtering and selection logic
│   ├── routes.py            # API endpoints and page routes
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css    # Application styles
│   │   └── js/
│   │       └── app.js       # Common JavaScript functions
│   └── templates/
│       ├── base.html        # Base template
│       ├── login.html       # Login page
│       ├── index.html       # Main recommendation page
│       └── passed_list.html # Passed movies management
├── instance/                # SQLite database location
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker image definition
├── docker-compose.yml      # Docker Compose configuration
├── run.py                  # Application entry point
└── README.md               # This file
```

## API Endpoints

### Authentication
- `POST /api/auth/login` - Login with Plex credentials
- `POST /api/auth/logout` - Logout current user

### Recommendations
- `GET /api/recommend` - Get a movie recommendation

### Actions
- `POST /api/play` - Play a movie on Plex client
- `POST /api/pass` - Pass on a movie

### Passed Movies
- `GET /api/passed-movies` - Get user's passed movies list
- `DELETE /api/passed-movies/<id>` - Remove a passed movie

### Preferences
- `GET /api/preferences` - Get user preferences
- `POST /api/preferences` - Update user preferences

## Troubleshooting

### Cannot connect to Plex server

- Verify your `PLEX_SERVER_URL` is correct
- If running in Docker on the same machine as Plex, use `http://host.docker.internal:32400`
- Ensure your Plex server is running and accessible

### Authentication fails

- Verify you're using the correct Plex credentials
- Ensure your Plex account has access to the server
- Check that your Plex server is accessible from the application

### No active Plex clients found

- Make sure you have a Plex client open and logged in (web player, mobile app, TV app, etc.)
- The client must be accessible from your Plex server
- Try refreshing the Plex client

### No movies match filters

- Try relaxing some of your filters
- Check that your Plex library actually has movies
- Verify the library name is "Movies" (default) or update the code if different

## Development

### Running Tests

(Tests to be implemented)

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is provided as-is for personal use.

## Acknowledgments

- Built with Flask and Python
- Uses the PlexAPI library for Plex integration
- Designed for personal Plex media server users
