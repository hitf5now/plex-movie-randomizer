# Unraid Docker UI Installation Guide

This guide shows you how to install Plex Movie Selector directly through the Unraid Docker UI with **NO SSH required**. Everything is configured through the web interface.

## Overview

This method allows you to:
- ✅ Install directly from GitHub repository
- ✅ Configure everything through Unraid UI variables
- ✅ No SSH access needed
- ✅ No manual file creation
- ✅ One-click installation and updates

## Prerequisites

1. **Unraid 6.9.0 or newer** (6.11+ recommended)
2. **Docker enabled** in Unraid (enabled by default)
3. **Plex Media Server** running (on same Unraid server or different machine)
4. **Your Plex server URL** - you'll need to know this
5. **Optional: Plex Token** for easier authentication

## Installation Steps

### Step 1: Get Your Plex Information

Before installing, gather this information:

#### A. Plex Server URL

**If Plex is on the SAME Unraid server:**
```
http://172.17.0.1:32400
```
(This is the Docker bridge IP that allows containers to talk to the host)

**If Plex is on a DIFFERENT machine:**
```
http://192.168.1.XXX:32400
```
(Replace XXX with your Plex server's IP address)

**How to find your Plex server IP:**
1. Open Plex Web App
2. Settings → Network
3. Look for server IP address or custom URLs

#### B. Plex Token (Optional but Recommended)

Getting your Plex token allows the app to authenticate automatically.

**How to get your Plex Token:**

1. **Open Plex Web App** in your browser
2. **Play any media item** (movie, show, anything)
3. **Click the (i) info icon** or three dots menu
4. **Select "Get Info"** or "View XML"
5. **Look at the URL** - you'll see `X-Plex-Token=XXXXXXXXXXXXX`
6. **Copy everything after** `X-Plex-Token=`

**Alternative method:**
- Visit: https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/
- Follow Plex's official guide

**Example token:** `abc123def456ghi789jkl012mno345pq`

### Step 2: Add Docker Container in Unraid

#### Option A: Using the XML Template (Recommended)

1. **Download the template file:**
   - Go to https://github.com/yourusername/plex-movie-selector
   - Download `plex-movie-selector.xml`
   - Save it to `/mnt/user/appdata/plex-movie-selector/`

2. **Import template:**
   - In Unraid, go to **Docker** tab
   - Scroll to bottom, click **Add Container**
   - Click **Template repositories** dropdown
   - Browse to the XML file and select it

#### Option B: Manual Configuration (If XML template doesn't work)

1. **Open Unraid web interface**

2. **Go to Docker tab**

3. **Scroll to bottom and click "Add Container"**

4. **Fill in the template:**

---

**BASIC SETTINGS:**

**Name:**
```
plex-movie-selector
```

**Repository:**
```
https://github.com/yourusername/plex-movie-selector.git#main
```
*Replace `yourusername` with your actual GitHub username*

**Docker Hub URL:**
```
https://github.com/yourusername/plex-movie-selector
```

**Icon URL:** (Optional)
```
https://raw.githubusercontent.com/yourusername/plex-movie-selector/main/icon.png
```

**Network Type:**
```
Bridge
```

**Console shell command:**
```
Bash
```

**Privileged:**
```
No (unchecked)
```

---

**PORT MAPPINGS:**

Click **"Add another Path, Port, Variable, Label or Device"**

- **Config Type:** `Port`
- **Name:** `WebUI`
- **Container Port:** `5000`
- **Host Port:** `5000`
- **Connection Type:** `TCP`
- **Display:** `Always`
- **Required:** `Yes`

---

**PATH MAPPINGS:**

Click **"Add another Path, Port, Variable, Label or Device"**

- **Config Type:** `Path`
- **Name:** `AppData`
- **Container Path:** `/app/instance`
- **Host Path:** `/mnt/user/appdata/plex-movie-selector/instance`
- **Access Mode:** `Read/Write`
- **Display:** `Advanced`
- **Required:** `Yes`

---

**ENVIRONMENT VARIABLES:**

Add each of these by clicking **"Add another Path, Port, Variable, Label or Device"**

**1. Plex Server URL** (REQUIRED)

- **Config Type:** `Variable`
- **Name:** `Plex Server URL`
- **Key:** `PLEX_SERVER_URL`
- **Value:** `http://172.17.0.1:32400` (or your Plex server IP)
- **Display:** `Always`
- **Required:** `Yes`

**2. Plex Token** (OPTIONAL - Recommended)

- **Config Type:** `Variable`
- **Name:** `Plex Token`
- **Key:** `PLEX_TOKEN`
- **Value:** (paste your Plex token here, or leave empty)
- **Display:** `Always`
- **Required:** `No`
- **Mask:** `Yes` (hide the token)

**3. Secret Key** (OPTIONAL - Will auto-generate if empty)

- **Config Type:** `Variable`
- **Name:** `Secret Key`
- **Key:** `SECRET_KEY`
- **Value:** (leave empty to auto-generate)
- **Display:** `Advanced`
- **Required:** `No`
- **Mask:** `Yes`

**4. Database URI** (OPTIONAL - Use default)

- **Config Type:** `Variable`
- **Name:** `Database URI`
- **Key:** `DATABASE_URI`
- **Value:** `sqlite:///instance/movie_selector.db`
- **Display:** `Advanced`
- **Required:** `No`

**5. Debug Mode** (OPTIONAL)

- **Config Type:** `Variable`
- **Name:** `Debug Mode`
- **Key:** `DEBUG`
- **Value:** `False`
- **Display:** `Advanced`
- **Required:** `No`

**6. PUID** (User ID)

- **Config Type:** `Variable`
- **Name:** `PUID`
- **Key:** `PUID`
- **Value:** `99`
- **Display:** `Advanced`
- **Required:** `No`

**7. PGID** (Group ID)

- **Config Type:** `Variable`
- **Name:** `PGID`
- **Key:** `PGID`
- **Value:** `100`
- **Display:** `Advanced`
- **Required:** `No`

---

5. **Click "Apply"**

### Step 3: Wait for Container to Build

**First-time installation:**
- Unraid will clone the GitHub repository
- Build the Docker image (this takes 3-5 minutes)
- You'll see build progress in the logs
- Once complete, container will automatically start

**Watch the build:**
- While installing, click the container icon
- Select **Logs**
- Watch the build progress

**When you see this, it's ready:**
```
* Running on http://0.0.0.0:5000
Starting Plex Movie Selector...
```

### Step 4: Verify Installation

1. **Check Docker tab:**
   - You should see `plex-movie-selector` with a green "started" status

2. **Click the container icon:**
   - Select **WebUI** (or click the WebUI icon if configured)
   - This opens `http://YOUR_UNRAID_IP:5000`

3. **You should see the login page!**

### Step 5: First Login

1. **If you provided a PLEX_TOKEN:**
   - The app will use token-based authentication
   - Login with your Plex username and password
   - Authentication should be faster

2. **If you did NOT provide a token:**
   - Login with your Plex username/email and password
   - App will authenticate through Plex servers
   - This may take a few seconds

3. **First login creates your user profile**
   - Sets up your preferences
   - Initializes your passed movies list
   - You're ready to go!

## Configuration Reference

### Minimum Required Variables

To get started, you only need:

1. **PLEX_SERVER_URL** - Your Plex server address
2. That's it! Everything else has sensible defaults.

### Recommended Variables

For best experience:

1. **PLEX_SERVER_URL** - Your Plex server address
2. **PLEX_TOKEN** - Your Plex authentication token (makes login easier)

### All Variables Explained

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `PLEX_SERVER_URL` | **Yes** | `http://172.17.0.1:32400` | URL to your Plex server |
| `PLEX_TOKEN` | No | (empty) | Plex authentication token for easier login |
| `SECRET_KEY` | No | Auto-generated | Flask session secret (auto-generates if empty) |
| `DATABASE_URI` | No | `sqlite:///instance/movie_selector.db` | Database connection string |
| `DEBUG` | No | `False` | Enable debug mode (`True`/`False`) |
| `PUID` | No | `99` | User ID for file permissions (Unraid default) |
| `PGID` | No | `100` | Group ID for file permissions (Unraid default) |

### PLEX_SERVER_URL Examples

| Scenario | URL to Use |
|----------|------------|
| Plex on same Unraid (bridge network) | `http://172.17.0.1:32400` |
| Plex on same Unraid (host network) | `http://YOUR_UNRAID_IP:32400` |
| Plex on same Unraid (custom network/br0) | `http://PLEX_CONTAINER_IP:32400` |
| Plex on different computer | `http://192.168.1.50:32400` |
| Plex on remote server | `https://plex.yourdomain.com:32400` |

## Using the Application

### Access the Application

**From any device on your network:**
```
http://YOUR_UNRAID_IP:5000
```

For example: `http://192.168.1.100:5000`

### Quick Start

1. **Login** with your Plex credentials
2. **Configure filters** (optional) - exclude watched, filter by decade, etc.
3. **Click "Get Recommendation"**
4. **Play** the movie or **Pass** to get another
5. **Manage passed movies** from the Passed Movies page

See the main [README.md](README.md) for detailed usage instructions.

## Managing the Container

### Start/Stop/Restart

**In Unraid Docker tab:**
- Click the container icon
- Select **Start**, **Stop**, or **Restart**

### View Logs

**In Unraid Docker tab:**
- Click the container icon
- Select **Logs**
- View real-time application logs

### Edit Configuration

**To change variables:**
1. Stop the container
2. Click container icon → **Edit**
3. Modify any variable values
4. Click **Apply**
5. Container rebuilds and restarts

### Update the Container

When you update your GitHub repository:

**Method 1: Force Update**
1. Go to Docker tab
2. Click container icon
3. Select **Force Update**
4. Rebuilds from latest GitHub code

**Method 2: Manual**
1. Stop container
2. Remove container (settings are saved)
3. Re-add using same template
4. Your data in `/mnt/user/appdata/plex-movie-selector/instance` is preserved

## Troubleshooting

### Container Won't Start

**Check the logs:**
1. Docker tab → Container icon → **Logs**
2. Look for error messages

**Common issues:**

**1. Port 5000 already in use:**
- Edit container
- Change Host Port to `5001` or another free port
- Apply

**2. Can't clone repository:**
- Verify GitHub URL is correct
- Check internet connection
- Try: `https://github.com/username/repo.git#main`

**3. Build fails:**
- Check logs for specific error
- Verify Dockerfile exists in repository
- Try force update/rebuild

### Can't Connect to Plex

**Error:** "Failed to connect to Plex server"

**Solutions:**

1. **Verify PLEX_SERVER_URL is correct:**
   - Edit container
   - Check PLEX_SERVER_URL value
   - For Plex on same Unraid: `http://172.17.0.1:32400`

2. **Test Plex connectivity:**
   - Click container icon → **Console**
   - Run: `curl http://172.17.0.1:32400/web`
   - Should return HTML, not error

3. **Check Plex is running:**
   - Docker tab → Verify Plex container is started
   - Or open Plex Web App to confirm

4. **Try different URL:**
   - If `172.17.0.1` doesn't work, try your Unraid IP
   - Edit container, change to `http://192.168.1.100:32400`

### Authentication Fails

**Error:** "Invalid credentials"

**Solutions:**

1. **Verify Plex credentials:**
   - Try logging into Plex Web App with same credentials
   - Username is case-sensitive
   - Use email if you normally login with email

2. **Try using Plex Token:**
   - Get your token (see Step 1B above)
   - Edit container
   - Add token to PLEX_TOKEN variable
   - Apply

3. **Check Plex server access:**
   - Ensure your Plex account has access to this server
   - Check Plex server settings → Users

### Can't Access from Browser

**Problem:** Can't reach `http://UNRAID_IP:5000`

**Solutions:**

1. **Verify container is running:**
   - Docker tab → Check for green "started"

2. **Check port mapping:**
   - Edit container
   - Verify Port mapping: `5000` → `5000`

3. **Try localhost (from Unraid):**
   - In Unraid terminal/console
   - Run: `curl http://localhost:5000`
   - Should return HTML

4. **Check firewall:**
   - If accessing from outside local network
   - Check router firewall settings

### Database Permission Errors

**Error:** "Unable to open database file"

**Solution:**
1. Access Unraid terminal (Settings → Terminal)
2. Run:
   ```bash
   chown -R 99:100 /mnt/user/appdata/plex-movie-selector/instance
   chmod -R 755 /mnt/user/appdata/plex-movie-selector/instance
   ```
3. Restart container

### Application Runs Slow

**Solutions:**

1. **Move Docker to cache drive:**
   - Settings → Docker
   - Docker vDisk location: Use cache drive (SSD)

2. **Check Unraid resources:**
   - Dashboard → View CPU/RAM usage
   - Ensure sufficient resources available

3. **Check container resources:**
   - Docker tab → Click container icon → **Stats**

## Advanced Configuration

### Using a Different Port

If port 5000 is already in use:

1. Edit container
2. Change **Host Port** from `5000` to `8080` (or any free port)
3. Keep **Container Port** as `5000`
4. Apply
5. Access at `http://UNRAID_IP:8080`

### Custom Docker Network

To use custom network (br0, macvlan):

1. Edit container
2. Change **Network Type** to your custom network
3. Apply
4. Find new IP: Docker tab → Container icon → **Console**
   ```bash
   hostname -i
   ```
5. Access at `http://CONTAINER_IP:5000`

### Reverse Proxy (HTTPS)

For external access with SSL:

**Install Nginx Proxy Manager:**
1. Community Applications → Search "Nginx Proxy Manager"
2. Install
3. Add proxy host:
   - Domain: `movies.yourdomain.com`
   - Forward to: `172.17.0.1:5000`
   - Enable SSL

**Or install Swag:**
1. Community Applications → Search "Swag"
2. Install and configure
3. Create proxy config for this container

## Backup and Restore

### Automatic Backup (Recommended)

**Using CA Backup plugin:**

1. **Install CA Backup/Restore Appdata:**
   - Apps → Search "appdata backup"
   - Install "CA Backup / Restore Appdata"

2. **Configure:**
   - Plugins → CA Backup / Restore Appdata
   - Add `plex-movie-selector` to backup list
   - Set schedule (daily recommended)

### Manual Backup

**Backup location:**
```
/mnt/user/appdata/plex-movie-selector/instance/movie_selector.db
```

**To backup:**
1. Access Unraid shares from another computer
2. Navigate to `\\UNRAID_IP\appdata\plex-movie-selector\instance\`
3. Copy `movie_selector.db` to safe location

**To restore:**
1. Stop container
2. Copy `movie_selector.db` back to same location
3. Start container

## Updating Your GitHub Repository

When you make changes to your code:

1. **Push updates to GitHub** (from your development machine)
   ```bash
   git add .
   git commit -m "Update description"
   git push
   ```

2. **Update container in Unraid:**
   - Docker tab
   - Container icon → **Force Update**
   - Pulls latest code and rebuilds

## Template Customization

### Creating Your Own Template

The included `plex-movie-selector.xml` can be customized:

1. Edit the XML file
2. Change `yourusername` to your GitHub username
3. Customize descriptions
4. Add your own icon URL
5. Upload to your repository
6. Share the template URL with others

### Sharing Your Template

Once customized:
1. Upload XML to your GitHub repo
2. Share this URL for others to import:
   ```
   https://raw.githubusercontent.com/yourusername/plex-movie-selector/main/plex-movie-selector.xml
   ```

## Getting Help

### Check These First

1. **Container logs:**
   - Docker tab → Container icon → Logs
   - Look for error messages

2. **Plex connectivity:**
   - Verify Plex is running
   - Test PLEX_SERVER_URL

3. **Variable configuration:**
   - Edit container
   - Verify all required variables are set

### Support Resources

- **GitHub Issues:** https://github.com/yourusername/plex-movie-selector/issues
- **Unraid Forums:** https://forums.unraid.net/ (Docker Engine section)
- **Documentation:** See README.md and other guides in repository

### Providing Logs for Support

When asking for help, provide:

1. **Container logs:**
   - Docker tab → Container icon → Logs → Copy

2. **Your configuration** (remove sensitive data):
   - Docker tab → Container icon → Edit
   - Copy variable values (REMOVE your SECRET_KEY and PLEX_TOKEN)

3. **Unraid version:**
   - Main page → Shows at top

## Quick Reference

### Essential Info

**Default Access URL:**
```
http://YOUR_UNRAID_IP:5000
```

**Data Location:**
```
/mnt/user/appdata/plex-movie-selector/instance/
```

**Container Name:**
```
plex-movie-selector
```

### Minimum Configuration

**Required Variables:**
- `PLEX_SERVER_URL` - Your Plex server URL

**Recommended Variables:**
- `PLEX_SERVER_URL` - Your Plex server URL
- `PLEX_TOKEN` - Your Plex token (for easier auth)

### Common URLs

**Plex on same Unraid:**
```
http://172.17.0.1:32400
```

**Plex on different machine:**
```
http://192.168.1.XXX:32400
```

---

**That's it!** Your Plex Movie Selector is now running entirely through the Unraid Docker UI with no SSH required. Enjoy discovering your next movie! 🎬
