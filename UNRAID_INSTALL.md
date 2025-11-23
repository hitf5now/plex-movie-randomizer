# Unraid Installation Guide

This guide provides step-by-step instructions for installing and running the Plex Movie Selector application on an Unraid server using Docker.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation Methods](#installation-methods)
3. [Method 1: Using Docker Compose (Recommended)](#method-1-using-docker-compose-recommended)
4. [Method 2: Using Unraid Docker UI](#method-2-using-unraid-docker-ui)
5. [Configuration](#configuration)
6. [Accessing the Application](#accessing-the-application)
7. [Updating the Container](#updating-the-container)
8. [Troubleshooting](#troubleshooting)
9. [Advanced Configuration](#advanced-configuration)

---

## Prerequisites

### Required

- **Unraid 6.9.0 or newer** (6.11+ recommended)
- **Docker enabled** in Unraid (enabled by default)
- **Plex Media Server** installed and running (can be on same Unraid server or different machine)
- **Plex account** with access to your Plex server
- **At least 2GB free RAM**
- **500MB free disk space**

### Recommended

- **Community Applications (CA) plugin** installed
- **Basic familiarity** with Unraid Docker containers
- **SSH access** to Unraid server (for Docker Compose method)

### Verify Docker is Enabled

1. Log in to your Unraid web interface
2. Go to **Settings** → **Docker**
3. Ensure "Enable Docker" is set to **Yes**
4. Note the Docker path (usually `/mnt/user/appdata`)

---

## Installation Methods

You can install this application using two methods:

| Method | Difficulty | Recommended For | Pros | Cons |
|--------|-----------|-----------------|------|------|
| **Docker Compose** | Easy-Medium | Users comfortable with SSH | Easy updates, portable configuration | Requires SSH access |
| **Unraid Docker UI** | Easy | All users | Native Unraid interface, no SSH needed | More manual setup |

---

## Method 1: Using Docker Compose (Recommended)

This method uses docker-compose through Unraid's command line.

### Step 1: Enable SSH Access

1. In Unraid web interface, go to **Settings** → **Management Access**
2. Under SSH, set to **Yes**
3. Note your Unraid server's IP address (shown at top of web interface)

### Step 2: Connect to Unraid via SSH

**Windows** (use PowerShell or PuTTY):
```powershell
ssh root@192.168.1.100
```

**Mac/Linux**:
```bash
ssh root@192.168.1.100
```

Replace `192.168.1.100` with your Unraid server's IP address.

Enter your Unraid root password when prompted.

### Step 3: Create Application Directory

```bash
# Navigate to appdata directory
cd /mnt/user/appdata

# Create directory for the application
mkdir -p plex-movie-selector

# Navigate into it
cd plex-movie-selector
```

### Step 4: Download Application Files

#### Option A: Clone from GitHub (if you've uploaded it)

```bash
# Install git if not already installed
curl -o /tmp/git.txz https://slackware.uk/slackware/slackware64-current/slackware64/d/git-2.40.0-x86_64-1.txz
installpkg /tmp/git.txz

# Clone repository
git clone https://github.com/yourusername/plex-movie-selector.git .
```

#### Option B: Download ZIP and Extract

```bash
# Download the ZIP file
wget https://github.com/yourusername/plex-movie-selector/archive/refs/heads/main.zip -O repo.zip

# Install unzip if needed
curl -o /tmp/unzip.txz https://slackware.uk/slackware/slackware64-current/slackware64/a/infozip-6.0-x86_64-5.txz
installpkg /tmp/unzip.txz

# Extract
unzip repo.zip
mv plex-movie-selector-main/* .
rm -rf plex-movie-selector-main repo.zip
```

#### Option C: Create Files Manually

If you have the files on another computer, you can use Unraid's built-in file sharing:

1. Access your Unraid shares via network (e.g., `\\192.168.1.100\appdata` on Windows)
2. Create folder `plex-movie-selector`
3. Copy all your project files into this folder

### Step 5: Create Environment Configuration

```bash
# Copy example environment file
cp .env.example .env

# Edit the configuration
nano .env
```

Configure your settings (see [Configuration](#configuration) section below).

Press `Ctrl+X`, then `Y`, then `Enter` to save.

### Step 6: Create docker-compose.yml for Unraid

The existing `docker-compose.yml` needs slight modifications for Unraid:

```bash
# Backup original
cp docker-compose.yml docker-compose.yml.backup

# Create Unraid-optimized version
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  movie-selector:
    build: .
    container_name: plex-movie-selector
    network_mode: bridge
    ports:
      - "5000:5000"
    environment:
      - SECRET_KEY=${SECRET_KEY:-change-this-secret-key-in-production}
      - PLEX_SERVER_URL=${PLEX_SERVER_URL:-http://172.17.0.1:32400}
      - DATABASE_URI=sqlite:///instance/movie_selector.db
      - HOST=0.0.0.0
      - PORT=5000
      - DEBUG=False
    volumes:
      # Persist database
      - /mnt/user/appdata/plex-movie-selector/instance:/app/instance
    restart: unless-stopped
EOF
```

**Note**: Changed `PLEX_SERVER_URL` default to `172.17.0.1` (Docker bridge gateway) for Plex on same Unraid server.

### Step 7: Build and Start the Container

```bash
# Make sure you're in the directory
cd /mnt/user/appdata/plex-movie-selector

# Build and start
docker-compose up -d
```

First build will take 2-5 minutes.

### Step 8: Verify Container is Running

```bash
# Check status
docker-compose ps

# View logs
docker-compose logs

# Follow logs in real-time
docker-compose logs -f
```

Press `Ctrl+C` to stop following logs.

### Step 9: Access the Application

Open your browser and go to:
```
http://UNRAID_IP:5000
```

For example: `http://192.168.1.100:5000`

---

## Method 2: Using Unraid Docker UI

This method uses Unraid's built-in Docker management interface.

### Step 1: Prepare Application Files

First, you need to get the application files onto your Unraid server:

1. **Access Unraid shares** from another computer:
   - Windows: `\\UNRAID_IP\appdata`
   - Mac: `smb://UNRAID_IP/appdata`
   - Linux: Mount SMB share

2. **Create directory structure**:
   ```
   appdata/
   └── plex-movie-selector/
       ├── app/
       │   ├── (all app files)
       ├── requirements.txt
       ├── Dockerfile
       ├── run.py
       └── .env
   ```

3. **Copy all project files** to `appdata/plex-movie-selector/`

4. **Create .env file** (see [Configuration](#configuration) section)

### Step 2: Build Docker Image

Since we're building from source, we need to build the image first:

1. **Enable SSH** (Settings → Management Access)

2. **Connect via SSH**:
   ```bash
   ssh root@UNRAID_IP
   ```

3. **Build the image**:
   ```bash
   cd /mnt/user/appdata/plex-movie-selector
   docker build -t plex-movie-selector:latest .
   ```

   This will take 2-5 minutes.

### Step 3: Add Container via Unraid UI

1. **Open Unraid web interface**

2. **Go to Docker tab**

3. **Click "Add Container"** at the bottom

4. **Fill in the template**:

   **Basic Settings:**
   - **Name**: `plex-movie-selector`
   - **Repository**: `plex-movie-selector:latest`
   - **Network Type**: `Bridge`
   - **Console shell command**: `Bash`

   **Port Mappings:**
   - Click "Add another Path, Port, Variable, Label or Device"
   - **Config Type**: `Port`
   - **Name**: `WebUI`
   - **Container Port**: `5000`
   - **Host Port**: `5000`
   - **Connection Type**: `TCP`

   **Path Mappings:**
   - Click "Add another Path, Port, Variable, Label or Device"
   - **Config Type**: `Path`
   - **Name**: `Database`
   - **Container Path**: `/app/instance`
   - **Host Path**: `/mnt/user/appdata/plex-movie-selector/instance`
   - **Access Mode**: `Read/Write`

   **Environment Variables:**

   Add each of these (click "Add another Path, Port, Variable, Label or Device" for each):

   - **Config Type**: `Variable`
     - **Name**: `SECRET_KEY`
     - **Key**: `SECRET_KEY`
     - **Value**: `your-long-random-secret-key-here`

   - **Config Type**: `Variable`
     - **Name**: `PLEX_SERVER_URL`
     - **Key**: `PLEX_SERVER_URL`
     - **Value**: `http://172.17.0.1:32400` (if Plex on same Unraid server)

   - **Config Type**: `Variable`
     - **Name**: `DATABASE_URI`
     - **Key**: `DATABASE_URI`
     - **Value**: `sqlite:///instance/movie_selector.db`

5. **Click Apply**

6. **Wait for container to start**

### Step 4: Verify Container is Running

1. On the Docker tab, you should see `plex-movie-selector` with a green "started" indicator
2. Click the container icon → **Logs** to view startup logs
3. Click the container icon → **WebUI** to open the application (or go to `http://UNRAID_IP:5000`)

---

## Configuration

### Environment Variables

Edit your `.env` file with these settings:

```env
# REQUIRED: Generate a secure random secret key
# Use: python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY=your-very-long-random-secret-key-change-this

# REQUIRED: Your Plex Server URL
# See options below based on your setup
PLEX_SERVER_URL=http://172.17.0.1:32400

# Database location (default is fine)
DATABASE_URI=sqlite:///instance/movie_selector.db
```

### Plex Server URL Options

Choose based on your setup:

#### Plex on Same Unraid Server (Most Common)

```env
# Use Docker bridge gateway IP
PLEX_SERVER_URL=http://172.17.0.1:32400
```

**Why 172.17.0.1?** This is the Docker bridge gateway IP that allows containers to access the host machine.

#### Plex on Different Unraid Server/Machine

```env
# Use the actual IP address of the Plex server
PLEX_SERVER_URL=http://192.168.1.50:32400
```

Replace `192.168.1.50` with your Plex server's IP address.

#### Plex Using Custom Network (br0, macvlan, etc.)

If your Plex container uses a custom network:

```env
# Use the Plex container's IP address
PLEX_SERVER_URL=http://192.168.1.150:32400
```

Find Plex container IP:
```bash
docker inspect plex | grep IPAddress
```

### Generating SECRET_KEY

**Option 1: Using Python (if available on another machine)**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

**Option 2: Using OpenSSL (on Unraid via SSH)**
```bash
openssl rand -hex 32
```

**Option 3: Online Generator**
- Go to https://randomkeygen.com/
- Use a "CodeIgniter Encryption Key"

Copy the generated key into your `.env` file.

---

## Accessing the Application

### From Your Network

1. **Find your Unraid IP**: Check the top of the Unraid web interface
2. **Open browser** and go to: `http://UNRAID_IP:5000`
3. **Login** with your Plex username/email and password

### From Different Devices

- **Desktop**: `http://UNRAID_IP:5000`
- **Phone/Tablet**: `http://UNRAID_IP:5000`
- **Smart TV Browser**: `http://UNRAID_IP:5000`

### Adding to Unraid Dashboard (Optional)

You can add a custom icon to access the application from your Unraid Docker page:

1. Edit the container
2. Under **WebUI**: `http://[IP]:[PORT:5000]`
3. Under **Icon URL**: (optional) Add a custom icon URL
4. Click **Apply**

Now you can click the container icon and select **WebUI** to open the app.

---

## Updating the Container

### Using Docker Compose

```bash
# SSH into Unraid
ssh root@UNRAID_IP

# Navigate to directory
cd /mnt/user/appdata/plex-movie-selector

# Pull latest code (if using Git)
git pull

# Rebuild and restart
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Using Unraid Docker UI

```bash
# SSH into Unraid
ssh root@UNRAID_IP

# Navigate to directory
cd /mnt/user/appdata/plex-movie-selector

# Pull latest code (if using Git)
git pull

# Rebuild image
docker build -t plex-movie-selector:latest .
```

Then in Unraid UI:
1. Go to **Docker** tab
2. Stop the `plex-movie-selector` container
3. Click **Force Update** on the container
4. Start the container

---

## Managing the Container

### Start/Stop/Restart

**Via Unraid UI:**
- Go to **Docker** tab
- Click container icon → **Start/Stop/Restart**

**Via SSH:**
```bash
# Using Docker Compose
docker-compose stop
docker-compose start
docker-compose restart

# Using Docker directly
docker stop plex-movie-selector
docker start plex-movie-selector
docker restart plex-movie-selector
```

### View Logs

**Via Unraid UI:**
- Go to **Docker** tab
- Click container icon → **Logs**

**Via SSH:**
```bash
# Using Docker Compose
docker-compose logs
docker-compose logs -f  # Follow logs

# Using Docker directly
docker logs plex-movie-selector
docker logs -f plex-movie-selector  # Follow logs
```

### Access Container Console

**Via Unraid UI:**
- Go to **Docker** tab
- Click container icon → **Console**

**Via SSH:**
```bash
docker exec -it plex-movie-selector /bin/bash
```

Type `exit` to leave the container.

---

## Backup and Restore

### Backup

Your data is stored in `/mnt/user/appdata/plex-movie-selector/instance/`

**Manual Backup:**
```bash
# SSH into Unraid
cd /mnt/user/appdata/plex-movie-selector

# Create backup
tar -czf backup-$(date +%Y%m%d).tar.gz instance/
```

**Using Unraid CA Backup Plugin:**
1. Install **CA Backup / Restore Appdata** plugin
2. Add `plex-movie-selector` to backup list
3. Set backup schedule

### Restore

```bash
# SSH into Unraid
cd /mnt/user/appdata/plex-movie-selector

# Stop container
docker-compose down
# OR via UI: Stop container

# Extract backup
tar -xzf backup-20231115.tar.gz

# Start container
docker-compose up -d
# OR via UI: Start container
```

---

## Troubleshooting

### Container Won't Start

**Check logs:**
```bash
docker logs plex-movie-selector
```

**Common issues:**

1. **Port 5000 already in use**:
   - Check what's using port 5000: `netstat -tulpn | grep 5000`
   - Change host port in docker-compose.yml or Unraid template to `5001:5000`

2. **Permission issues**:
   ```bash
   chown -R nobody:users /mnt/user/appdata/plex-movie-selector/instance
   chmod -R 755 /mnt/user/appdata/plex-movie-selector/instance
   ```

3. **Build errors**:
   ```bash
   # Rebuild without cache
   docker-compose build --no-cache
   ```

### Can't Connect to Plex

**Issue**: "Failed to connect to Plex server"

**Solutions:**

1. **Verify Plex is running**:
   - Check Docker tab for Plex container
   - Ensure Plex container is started

2. **Check PLEX_SERVER_URL**:

   **If Plex is on same Unraid server**, test connectivity:
   ```bash
   docker exec plex-movie-selector curl http://172.17.0.1:32400/web
   ```

   If this fails, try:
   ```env
   # In .env file
   PLEX_SERVER_URL=http://UNRAID_IP:32400
   ```

3. **Check Plex Network Mode**:
   - If Plex uses `host` network mode, use Unraid IP
   - If Plex uses `bridge` mode, use `172.17.0.1`
   - If Plex uses custom network (br0), use Plex container IP

4. **Find Plex container IP**:
   ```bash
   docker inspect plex | grep IPAddress
   ```

### Authentication Fails

**Issue**: "Invalid credentials"

1. **Verify Plex credentials**:
   - Username/email must be exact
   - Password is case-sensitive
   - Try logging into Plex Web UI first

2. **Check Plex server accessibility**:
   - Ensure your Plex account has access to this server
   - Check Plex server is not restricted to certain users

### Database Permission Errors

```bash
# Fix permissions
chown -R 99:100 /mnt/user/appdata/plex-movie-selector/instance
chmod -R 755 /mnt/user/appdata/plex-movie-selector/instance
```

**Note**: 99:100 is `nobody:users` in Unraid.

### Application Slow or Unresponsive

1. **Check Unraid resources**:
   - Go to Unraid Dashboard
   - Check CPU and RAM usage
   - Ensure Docker is on cache drive (SSD), not array

2. **Check container resources**:
   ```bash
   docker stats plex-movie-selector
   ```

3. **Move Docker appdata to cache**:
   - Settings → Docker
   - Set Docker vDisk location to `/mnt/cache/...`

### Can't Access from Other Devices

1. **Check Unraid firewall** (if using):
   - Settings → Network Settings
   - Ensure port 5000 is allowed

2. **Check device is on same network**:
   - Must be on same LAN as Unraid

3. **Try Unraid IP**:
   - Don't use `localhost` from other devices
   - Use actual IP: `http://192.168.1.100:5000`

---

## Advanced Configuration

### Running on Different Port

**Docker Compose method:**

Edit `docker-compose.yml`:
```yaml
ports:
  - "8080:5000"  # Change 8080 to your desired port
```

Then:
```bash
docker-compose down
docker-compose up -d
```

Access at: `http://UNRAID_IP:8080`

**Unraid UI method:**
1. Edit container
2. Change Host Port from `5000` to `8080`
3. Apply

### Using Custom Docker Network

If you want the container on a custom network (e.g., to use macvlan):

1. **Create custom network** (via SSH):
   ```bash
   docker network create --driver=bridge --subnet=192.168.1.0/24 --gateway=192.168.1.1 custom-network
   ```

2. **Edit docker-compose.yml**:
   ```yaml
   services:
     movie-selector:
       # ... other settings ...
       networks:
         - custom-network

   networks:
     custom-network:
       external: true
   ```

3. **Restart container**

### Reverse Proxy Setup (HTTPS)

For secure external access, use Nginx Proxy Manager or Swag:

#### Using Nginx Proxy Manager

1. **Install Nginx Proxy Manager** from Community Applications

2. **Add Proxy Host**:
   - Domain: `movies.yourdomain.com`
   - Forward Hostname/IP: `172.17.0.1` (or Unraid IP)
   - Forward Port: `5000`
   - Enable SSL (use Let's Encrypt)

3. **Access via**: `https://movies.yourdomain.com`

#### Using Swag (Secure Web Application Gateway)

1. **Install Swag** from Community Applications

2. **Create proxy config**:
   ```bash
   cd /mnt/user/appdata/swag/nginx/proxy-confs/
   nano plex-movie-selector.subdomain.conf
   ```

   Add:
   ```nginx
   server {
       listen 443 ssl;
       listen [::]:443 ssl;

       server_name movies.*;

       location / {
           proxy_pass http://172.17.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

3. **Restart Swag container**

### Auto-Update with Watchtower

To automatically update the container when you push changes:

1. **Install Watchtower** from Community Applications

2. **Add label to container**:

   Edit `docker-compose.yml`:
   ```yaml
   services:
     movie-selector:
       # ... other settings ...
       labels:
         - "com.centurylinklabs.watchtower.enable=true"
   ```

Watchtower will check for updates and rebuild/restart your container automatically.

---

## Unraid-Specific Tips

### Use Cache Drive for Docker

Ensure Docker appdata is on your cache drive (SSD) for best performance:

1. Settings → Docker → **Docker vDisk location**: `/mnt/cache/...`
2. Much faster than array drives

### Add to Community Applications (Advanced)

If you want to share this with other Unraid users, you can create a Community Applications template:

1. Create a template XML file
2. Submit to CA repository
3. Others can install with one click

### Integration with Plex Docker Container

If Plex is also running in Docker on same Unraid server:

```yaml
# docker-compose.yml
version: '3.8'

services:
  movie-selector:
    # ... your config ...
    depends_on:
      - plex
    environment:
      - PLEX_SERVER_URL=http://plex:32400
    networks:
      - plex-network

networks:
  plex-network:
    name: plex-network
    external: true
```

Then connect Plex container to the same network.

---

## Unraid Dashboard Integration

### Custom Icon

Add a nice icon to your Docker container:

1. Edit container in Unraid UI
2. **Icon URL**: `https://raw.githubusercontent.com/yourusername/plex-movie-selector/main/icon.png`
   (upload an icon.png to your GitHub repo)
3. Apply

### WebUI Link

Make it easy to access:

1. Edit container
2. **WebUI**: `http://[IP]:[PORT:5000]`
3. Now you can click the container icon → **WebUI**

---

## Monitoring and Maintenance

### Check Container Health

```bash
docker ps | grep plex-movie-selector
docker stats plex-movie-selector
```

### View Resource Usage

In Unraid UI:
- Dashboard → Docker containers section
- Shows CPU and memory usage per container

### Regular Maintenance

1. **Weekly**: Check logs for errors
2. **Monthly**: Backup database
3. **Quarterly**: Update container to latest version
4. **As needed**: Clean up old passed movies

---

## Support and Resources

### Unraid Forums

- https://forums.unraid.net/
- Docker Engine section
- Ask for help with container issues

### Logs for Support

When asking for help, provide:

```bash
# Container logs
docker logs plex-movie-selector > logs.txt

# Docker compose config
cat docker-compose.yml

# Environment (remove sensitive data)
cat .env | sed 's/SECRET_KEY=.*/SECRET_KEY=REDACTED/'
```

---

## Quick Reference

### Essential Commands

```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# Restart
docker-compose restart

# Logs
docker-compose logs -f

# Rebuild
docker-compose build --no-cache
docker-compose up -d

# Access console
docker exec -it plex-movie-selector /bin/bash

# Check status
docker ps | grep plex-movie-selector
```

### File Locations

- **Application**: `/mnt/user/appdata/plex-movie-selector/`
- **Database**: `/mnt/user/appdata/plex-movie-selector/instance/movie_selector.db`
- **Logs**: `docker logs plex-movie-selector`
- **Config**: `/mnt/user/appdata/plex-movie-selector/.env`

---

**Congratulations!** Your Plex Movie Selector is now running on Unraid. Access it at `http://YOUR_UNRAID_IP:5000` and start discovering movies!
