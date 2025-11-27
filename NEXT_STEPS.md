# Plex Movie Randomizer - Next Steps

**Last Updated:** 2025-11-26
**Current Status:** Client selection feature implemented; Testing device compatibility

---

## Recent Accomplishments ✅

### 1. Play Movie Functionality - WORKING!
- ✅ Successfully implemented multi-method playback approach
- ✅ SHIELD Android TV confirmed working via Method 3 (device.connect())
- ✅ Play Movie button successfully initiates playback on compatible devices

**Working Deployment:**
- Repository: `mestopgoboom/plex-movie-selector:latest`
- Digest: `sha256:67753064bb82be171538c58cb34e4d8a56581faba6f30d38078998da9a9d8823`

### 2. Client Selection Feature - IMPLEMENTED!

**What Was Added:**
1. **Client Selection UI** (Plex Clients page)
   - Dropdown showing all available playback devices
   - Automatically filters out web players (Chrome, Firefox, etc.)
   - Filters out server devices (only shows playback clients)
   - "Save Selection" button to persist user choice
   - "Currently Selected" indicator

2. **Database Updates**
   - Added `selected_client_name` field to UserPreference model
   - Added `selected_client_identifier` field to UserPreference model
   - Automatic migration runs on app startup to add columns

3. **Smart Play Button**
   - Greyed out (disabled) until client is selected
   - Shows tooltip: "Please select a playback client in the Plex Clients page"
   - When client selected: Shows "Play on [device name]"

4. **Targeted Playback**
   - App only sends play commands to selected device
   - Uses multi-method approach for maximum compatibility

**Files Modified:**
- `app/models.py` - Added client selection fields
- `app/__init__.py` - Added automatic database migration
- `app/routes.py` - Added GET/POST `/api/selected-client` endpoints
- `app/plex_api.py` - Updated `play_movie()` with client selection logic
- `app/templates/clients.html` - Added client selector dropdown and UI
- `app/templates/index.html` - Added client checking and Play button state management
- `app/static/css/style.css` - Added client selection styles

---

## Current Issue: Mobile Device Compatibility

### Working Devices ✅
- **SHIELD Android TV** - Confirmed working via Method 3
  - Logs show: "SUCCESS! Movie playback initiated on SHIELD Android TV"
  - Uses device.connect() successfully

### Not Working Devices ❌
- **Pixel 8 Pro (Plex for Android Mobile)** - All methods fail
- **Plex for Windows (DESKTOP-GC21T49)** - Session detected but control fails

### Test Results - Pixel 8 Pro

**Test Date:** 2025-11-26
**Scenario:** Plex app open and actively playing a movie on Pixel 8 Pro

**Results:**
```
Method 1: Checking if 'Pixel 8 Pro' is in server.clients()...
  'Pixel 8 Pro' not found in active clients

Method 2: Checking if 'Pixel 8 Pro' is in active sessions...
  'Pixel 8 Pro' not found in active sessions

Method 3: Trying device.connect() for 'Pixel 8 Pro'...
  ERROR: Unable to connect to device: Pixel 8 Pro
```

**Issue Analysis:**
1. Device not advertising for remote control (Method 1 fails)
2. Active session not detected even while playing (Method 2 fails)
3. Direct connection fails - no accessible connections (Method 3 fails)

**Possible Causes:**
- Mobile devices often don't advertise properly for remote control
- Device may be on cellular data instead of WiFi
- Plex mobile app may not support remote playback initiation
- NAT/firewall preventing connection from Docker container
- Different network segments (Docker bridge vs LAN)

---

## Multi-Method Playback Implementation

**Current Approach** (app/plex_api.py lines 118-219):

When user has selected a client, the app tries 3 methods:

### Method 1: server.clients()
- Checks if device is in active clients advertising remote control
- Fastest method if device is properly advertising
- Uses `client.machineIdentifier` to match selected device
- **Works for:** TV devices with "Advertise as player" enabled

### Method 2: Active Sessions
- Checks if device is currently playing content
- Gets player from session and attempts `server.client(player.title)`
- **Added diagnostic logging** to show session details
- **Should work for:** Devices actively streaming

### Method 3: device.connect()
- Tries to connect to device via account.devices()
- Requires device to have accessible connections
- **Works for:** SHIELD Android TV and similar devices
- **Fails for:** Mobile devices, devices on different networks

---

## Diagnostic Logging Added

**Latest Version** includes detailed session debugging (lines 138-174):

```python
# Shows:
- Number of active sessions found
- Each session's title (movie being played)
- Each player's title and machine identifier
- ID comparison (expected vs actual)
```

**Expected Output:**
```
Method 2: Checking if 'Pixel 8 Pro' is in active sessions...
  Found 1 active session(s)
  Session 1: [Movie Title]
    Player: Pixel 8 Pro (ID: abc123...)
    Looking for ID: abc123...
```

**Note:** If diagnostic output isn't showing in logs, user may need to pull latest image.

---

## Next Steps for Debugging

### 1. Verify Latest Image Deployed
```bash
# Check digest
docker inspect mestopgoboom/plex-movie-selector:latest | grep -A 2 "RepoDigests"

# Should see:
# sha256:67753064bb82be171538c58cb34e4d8a56581faba6f30d38078998da9a9d8823

# If different, pull and restart
docker pull mestopgoboom/plex-movie-selector:latest
docker stop plex-movie-selector
docker rm plex-movie-selector
docker run [your normal docker run command]
```

### 2. Confirm SHIELD Android TV Still Works
- [ ] Select SHIELD Android TV in client selector
- [ ] Save selection
- [ ] Try playing a movie
- [ ] Verify success in logs

### 3. Analyze Pixel 8 Pro Diagnostic Output
With latest image, logs should show:
- [ ] How many sessions are detected
- [ ] What player IDs are in those sessions
- [ ] If ID matches or mismatches
- [ ] Why Method 2 isn't finding the device

### 4. Investigate Session Detection Issue

If Pixel 8 Pro is playing but shows "0 active sessions":
- Check if playing from a different Plex server
- Verify both devices on same network
- Check Plex server logs for session information
- Test with different content (movie vs TV show)

### 5. Alternative Approaches to Consider

If mobile devices fundamentally can't be controlled:

**Option A: Accept Limitation**
- Document that mobile devices don't support remote playback
- Focus on TV devices (SHIELD, Roku, Apple TV, Smart TVs)
- Add warning in UI about device compatibility

**Option B: Try Plex Companion Protocol**
- Research Plex Companion API
- Implement companion-based playback commands
- May work better for mobile devices

**Option C: Use Plex Web Player Integration**
- Instead of remote control, open Plex Web Player
- Navigate to movie and auto-play
- Works universally but requires browser

**Option D: QR Code / Deep Link**
- Generate Plex deep link (plex://...)
- Show QR code for mobile devices to scan
- Opens directly in Plex app on device

---

## Known Working Configuration

**Device:** SHIELD Android TV (Plex for Android TV)
**Method:** Method 3 - device.connect()
**Logs:**
```
Attempting to connect to: SHIELD Android TV (Plex for Android (TV))
✓ Connected to client: SHIELD Android TV
Sending playMedia command...
SUCCESS! Movie playback initiated on SHIELD Android TV
```

**Requirements for Working Playback:**
1. Device must be on same network as Plex server
2. Plex app must be open (can be in background)
3. Device must have accessible connections
4. For TV devices: "Advertise as player" helps but not required

---

## Device Compatibility Matrix

| Device Type | Method 1 | Method 2 | Method 3 | Status |
|-------------|----------|----------|----------|---------|
| SHIELD Android TV | ❌ | ❓ | ✅ | **Working** |
| Pixel 8 Pro (Mobile) | ❌ | ❌ | ❌ | **Not Working** |
| Plex for Windows | ❌ | ❌ | ❓ | **Needs Testing** |
| Chrome Browser | ❌ | ❌ | ❌ | **Not Supported** (by design) |
| Smart TV (Sony Bravia) | ❓ | ❓ | ❓ | **Needs Testing** |

**Legend:**
- ✅ = Confirmed working
- ❌ = Confirmed not working
- ❓ = Not tested yet

---

## Recommended User Workflow

**For Best Experience:**

1. **Go to Plex Clients page**
2. **Look for TV/streaming devices** (SHIELD, Roku, Apple TV, Smart TV)
3. **Avoid mobile devices** (phones, tablets) - they often don't work
4. **Select a TV device** from dropdown
5. **Click "Save Selection"**
6. **Return to Recommendations page**
7. **Play button is now enabled** - click to play on selected device

**If Device Doesn't Work:**
- Try a different device from the list
- Make sure Plex is open on the target device
- Restart the Plex app on the device
- Check that device is on same network as server

---

## Technical Details

### Database Migration
**File:** `app/__init__.py` (lines 36-67)

Automatic migration adds columns on startup:
```python
def migrate_database():
    # Checks if columns exist
    # Adds selected_client_name if missing
    # Adds selected_client_identifier if missing
    # Prints success messages to logs
```

**Migration Logs:**
```
Adding selected_client_name column to user_preferences...
✓ Added selected_client_name column
Adding selected_client_identifier column to user_preferences...
✓ Added selected_client_identifier column
Database migration completed successfully
```

### API Endpoints

**GET /api/selected-client**
- Returns currently selected client name and identifier
- Returns null if no client selected

**POST /api/selected-client**
- Saves selected client to user preferences
- Parameters: `client_name`, `client_identifier`
- Persists across sessions

**GET /api/clients**
- Returns all available Plex clients
- Filters out web players automatically
- Includes machine identifiers for selection

---

## Questions to Answer

1. **Why doesn't Pixel 8 Pro show up in active sessions even while playing?**
   - Is it connecting to a different server?
   - Is the session being created but not detected?
   - Is there an API version difference?

2. **Can we get session information directly from Plex server?**
   - Check Plex server dashboard
   - Compare server view vs API view
   - Verify session actually exists

3. **What makes SHIELD work but not Pixel?**
   - Network configuration differences?
   - Plex app version differences?
   - Android TV vs Mobile API differences?

4. **Should we document device type compatibility?**
   - Create a "Supported Devices" page
   - Add warnings about mobile device limitations
   - Set user expectations appropriately

---

## Reference Commands

```bash
# View logs
docker logs plex-movie-selector -f

# View recent logs
docker logs plex-movie-selector --tail 100

# Check for migration
docker logs plex-movie-selector | grep -A 5 "migration"

# Check current digest
docker inspect mestopgoboom/plex-movie-selector:latest | grep "RepoDigests"

# Full restart
docker pull mestopgoboom/plex-movie-selector:latest
docker stop plex-movie-selector
docker rm plex-movie-selector
# Run your docker run command
```

---

## Success Criteria

Client selection feature will be considered complete when:
1. ✅ Users can select a playback device from dropdown
2. ✅ Selection persists across sessions
3. ✅ Play button is disabled until client selected
4. ✅ Playback works reliably on at least one device type (SHIELD ✅)
5. ❓ Mobile device compatibility documented (if not working)
6. ❓ Clear user guidance on which devices work best

---

## Notes

- **Working as of 2025-11-26:** Client selection feature fully implemented
- **SHIELD Android TV:** Confirmed working via Method 3
- **Mobile Devices:** May have fundamental limitations for remote control
- **Next Session:** Test with latest diagnostic logging, verify SHIELD, analyze session detection
- **Consider:** Adding device type compatibility warnings in UI
