# Plex Movie Randomizer - Work Session Notes

## Session Date: November 26, 2025

---

## Issues Resolved

### 1. Docker Container Database Path Issue

**Problem:** Container was failing to start in Unraid with error:
```
sqlite3.OperationalError: unable to open database file
```

**Root Cause:**
- SQLite URI path was using 3 slashes (`sqlite:///instance/movie_selector.db`) which SQLAlchemy interprets as absolute path `/instance/movie_selector.db` from filesystem root
- Should have been 4 slashes with full path (`sqlite:////app/instance/movie_selector.db`)

**Files Modified:**
1. `Dockerfile` (line 52)
   - Changed: `sqlite:///instance/movie_selector.db`
   - To: `sqlite:////app/instance/movie_selector.db`

2. `app/__init__.py` (line 14)
   - Changed: `sqlite:///movie_selector.db`
   - To: `sqlite:////app/instance/movie_selector.db`

3. `plex-movie-selector.xml` (line 38)
   - Updated Database URI default and value to: `sqlite:////app/instance/movie_selector.db`

**Additional Improvements:**
- Added comprehensive debugging output to `Dockerfile` startup script (lines 38-73)
- Shows user info, permissions, directory listing, and write test
- Helps diagnose permission issues in containers

**Docker Image:**
- Repository: `mestopgoboom/plex-movie-selector:latest`
- Successfully rebuilt and pushed to Docker Hub
- Tested and working in Unraid

---

## Current Application State

### Technology Stack
- **Backend:** Flask 3.0.0, Python 3.11
- **Database:** SQLite with Flask-SQLAlchemy 3.1.1
- **Authentication:** Flask-Login 0.6.3
- **Plex Integration:** PlexAPI 4.15.6
- **Container:** Docker (Python 3.11-slim base)

### Key Features (Current)
1. User authentication with Plex credentials
2. Smart rating grouping - movies grouped by rating
3. Advanced filtering options
4. Pass system - excluded for 6 months
5. Direct playback on active Plex client
6. Multi-user support

### File Structure
```
/app/
├── Dockerfile
├── requirements.txt
├── run.py
├── app/
│   ├── __init__.py
│   ├── routes.py
│   └── models.py
├── instance/
│   └── movie_selector.db (SQLite database)
└── plex-movie-selector.xml (Unraid template)
```

---

## Pending Feature Requests

### 1. Pass List Not Filtering Recommendations
**Issue:** When a movie is added to "Pass" list, it still appears in next recommendation

**Task:** Debug and fix the pass list filtering logic in recommendation engine

**Affected Files:** Likely `app/routes.py` (recommendation logic)

---

### 2. Actor Filter - Reverse Logic
**Current Behavior:** "Exclude movies with same actor as last watched"

**Requested Behavior:** "Movies with actors from the last movie watched"
- Include at least 1 actor from previously watched movie
- Show small movie poster and title of last watched movie
- Show which actor links the two movies
- Only display option if user has a previously watched movie
- Make exclusive with "Filter by Actor" selection
- Group both visually together
- When checked, hide single actor filter field

**Affected Files:**
- `app/routes.py` (filter logic)
- Templates (UI changes)
- Possibly `app/models.py` (if database schema needs updating)

---

### 3. Director Filter - Reverse Logic
**Current Behavior:** "Exclude movies from same director as last watched"

**Requested Behavior:** "Movies with the same director as the last movie watched"
- Same logic and UI changes as actor filter (#2)
- Show director name that links the two movies

**Affected Files:**
- `app/routes.py` (filter logic)
- Templates (UI changes)

---

### 4. Exclude Watched Movies Not Working
**Issue:** "Exclude Watched Movies" filter doesn't appear to be filtering watched content

**Task:** Debug and verify Plex API watched status integration

**Affected Files:** `app/routes.py` (watched status check)

---

### 5. Collapsible Top Menu
**Request:** Make top menu (Recommendations, Passed Movies, Logout) collapsible for mobile screens

**Requirements:**
- Hamburger menu icon
- Responsive design for mobile
- More room for logo on small screens

**Affected Files:**
- Templates (header/navigation)
- Static CSS files (if any)
- May need to add JavaScript for menu toggle

---

## Next Steps

1. Commit current Docker fixes to git repository
2. Explore codebase to understand current filter implementation
3. Read `app/routes.py` to understand recommendation logic
4. Read template files to understand current UI
5. Implement fixes for pass list filtering
6. Reverse actor/director filter logic
7. Add last watched movie display
8. Implement exclusive filter grouping
9. Fix watched movies filter
10. Implement collapsible mobile menu

---

## Docker Hub Info
- **Repository:** mestopgoboom/plex-movie-selector
- **Registry:** https://hub.docker.com/r/mestopgoboom/plex-movie-selector
- **GitHub:** https://github.com/hitf5now/plex-movie-randomizer

---

## Unraid Configuration
- **Container Path:** `/app/instance`
- **Host Path:** `/mnt/user/appdata/plex-movie-selector/instance`
- **Port:** 5000
- **Default Plex URL:** `http://172.17.0.1:32400`
- **PUID/PGID:** 99/100 (nobody user)

---

## Important Notes
- Database is persisted in Unraid appdata directory
- Container runs as root (UID 0) but /app/instance has 777 permissions
- Volume mount ensures data persistence across container rebuilds
- Template file is hosted in GitHub repo for easy Unraid installation
