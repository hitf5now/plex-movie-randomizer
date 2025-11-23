# Unraid Quick Start Guide

The fastest way to get Plex Movie Selector running on Unraid through the Docker UI.

## For End Users (Installing the App)

### Prerequisites
- Unraid server with Docker enabled
- Plex server running (same server or different machine)
- Know your Plex server URL

### Installation (5 minutes)

1. **Open Unraid** → **Docker** tab → **Add Container**

2. **Repository**:
   ```
   https://github.com/YOURUSERNAME/plex-movie-selector.git#main
   ```
   *(Replace YOURUSERNAME with the actual GitHub username)*

3. **Required Settings**:
   - **Name**: `plex-movie-selector`
   - **Port**: `5000` (host) → `5000` (container)
   - **Path**: `/mnt/user/appdata/plex-movie-selector/instance` → `/app/instance`
   - **Variable - PLEX_SERVER_URL**: `http://172.17.0.1:32400` *(if Plex on same Unraid)*

4. **Optional but Recommended**:
   - **Variable - PLEX_TOKEN**: *(your Plex token - makes login easier)*

5. **Click Apply** → Wait 3-5 minutes for build

6. **Access**: `http://YOUR_UNRAID_IP:5000`

**Full instructions**: See [UNRAID_UI_INSTALL.md](UNRAID_UI_INSTALL.md)

---

## For Developers (Setting Up the Repository)

### Prerequisites
- GitHub account
- Git installed
- Code ready to deploy

### Setup (10 minutes)

1. **Create GitHub repository**:
   - Go to https://github.com/new
   - Name: `plex-movie-selector`
   - Public repository
   - Create

2. **Prepare Dockerfile**:
   ```bash
   mv Dockerfile Dockerfile.standard
   mv Dockerfile.unraid Dockerfile
   ```

3. **Update XML template**:
   - Edit `plex-movie-selector.xml`
   - Replace all `yourusername` with your GitHub username

4. **Push to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOURUSERNAME/plex-movie-selector.git
   git branch -M main
   git push -u origin main
   ```

5. **Test**:
   - Open `https://github.com/YOURUSERNAME/plex-movie-selector`
   - Verify all files are there
   - Try installing in Unraid

**Full instructions**: See [SETUP_FOR_UNRAID.md](SETUP_FOR_UNRAID.md)

---

## Getting Your Plex Token

1. Open Plex Web App
2. Play any media item
3. Click (i) → View XML
4. Look in URL for `X-Plex-Token=XXXXX`
5. Copy everything after the `=`

**Alternative**: https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/

---

## Common Plex Server URLs

| Scenario | URL |
|----------|-----|
| Plex on same Unraid (bridge) | `http://172.17.0.1:32400` |
| Plex on same Unraid (host) | `http://YOUR_UNRAID_IP:32400` |
| Plex on different machine | `http://192.168.1.XXX:32400` |

---

## Troubleshooting

### Container won't start
- Check logs: Docker tab → Container icon → Logs
- Verify PLEX_SERVER_URL is correct

### Can't connect to Plex
- Verify Plex is running
- Test: Container Console → `curl http://172.17.0.1:32400/web`
- Try using Unraid IP instead of 172.17.0.1

### Build fails
- Verify Dockerfile exists in GitHub root
- Check internet connection
- Try Force Update

**More help**: See [UNRAID_UI_INSTALL.md](UNRAID_UI_INSTALL.md) troubleshooting section

---

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `PLEX_SERVER_URL` | **YES** | `http://172.17.0.1:32400` | Plex server URL |
| `PLEX_TOKEN` | No | - | Plex token (recommended) |
| `SECRET_KEY` | No | Auto-generated | Session security key |
| `DATABASE_URI` | No | `sqlite:///instance/movie_selector.db` | Database path |

---

## File Locations

- **Application data**: `/mnt/user/appdata/plex-movie-selector/instance/`
- **Database**: `/mnt/user/appdata/plex-movie-selector/instance/movie_selector.db`
- **Access URL**: `http://YOUR_UNRAID_IP:5000`

---

## Quick Commands

### View logs
```bash
docker logs plex-movie-selector
```

### Restart container
```bash
docker restart plex-movie-selector
```

### Update container (Unraid UI)
Docker tab → Container icon → Force Update

---

## What Makes This Unraid-Ready?

✅ **No SSH required** - Everything through Unraid UI
✅ **Direct GitHub installation** - Just paste repository URL
✅ **UI variable configuration** - All settings in Unraid interface
✅ **Auto-builds on install** - No manual steps
✅ **Persistent data** - Database survives updates
✅ **One-click updates** - Force Update rebuilds from latest code
✅ **WebUI integration** - Click to open from Unraid
✅ **Proper permissions** - Works with Unraid's nobody:users

---

## Support

- **Installation issues**: [UNRAID_UI_INSTALL.md](UNRAID_UI_INSTALL.md)
- **Setup questions**: [SETUP_FOR_UNRAID.md](SETUP_FOR_UNRAID.md)
- **General help**: [README.md](README.md)
- **GitHub issues**: Create issue in repository

---

**That's it!** The entire installation is done through the Unraid Docker UI with no terminal access required. Just paste the GitHub URL, set your Plex server URL, and go! 🚀
