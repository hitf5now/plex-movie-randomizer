# Docker Installation and Setup Guide

This guide provides detailed instructions for installing Docker and running the Plex Movie Selector application in a Docker container.

## What is Docker?

Docker is a platform that allows you to run applications in isolated containers. This means:
- No need to install Python or other dependencies on your system
- Consistent environment across different machines
- Easy deployment and updates
- Isolation from other applications

## Table of Contents

1. [Installing Docker](#installing-docker)
2. [Verifying Docker Installation](#verifying-docker-installation)
3. [Setting Up the Application](#setting-up-the-application)
4. [Running the Application](#running-the-application)
5. [Managing the Application](#managing-the-application)
6. [Troubleshooting](#troubleshooting)

---

## Installing Docker

### Windows 10/11 (64-bit)

#### Prerequisites
- Windows 10/11 64-bit: Pro, Enterprise, or Education (Build 19041 or higher)
- OR Windows 10/11 Home with WSL 2
- Virtualization must be enabled in BIOS

#### Installation Steps

1. **Download Docker Desktop**:
   - Go to https://www.docker.com/products/docker-desktop
   - Click "Download for Windows"
   - Save the installer file

2. **Run the Installer**:
   - Double-click `Docker Desktop Installer.exe`
   - Follow the installation wizard
   - When prompted, ensure "Use WSL 2 instead of Hyper-V" is checked (recommended)
   - Click "Ok" to proceed

3. **Complete Installation**:
   - Wait for installation to complete
   - Click "Close and restart" when prompted
   - Your computer will restart

4. **Start Docker Desktop**:
   - After restart, Docker Desktop should start automatically
   - If not, find "Docker Desktop" in your Start menu and launch it
   - Wait for Docker Desktop to start (you'll see the Docker icon in your system tray)
   - The icon will show "Docker Desktop is running" when ready

5. **Accept Terms**:
   - On first launch, you may need to accept the Docker Subscription Service Agreement
   - You can use Docker Desktop for free for personal use

### macOS

#### Prerequisites
- macOS 10.15 or newer
- At least 4GB of RAM

#### Installation Steps

1. **Download Docker Desktop**:
   - Go to https://www.docker.com/products/docker-desktop
   - Click "Download for Mac"
   - Choose the correct version:
     - **Mac with Intel chip**: Download Intel version
     - **Mac with Apple chip (M1/M2)**: Download Apple Chip version

2. **Install Docker Desktop**:
   - Open the downloaded `.dmg` file
   - Drag the Docker icon to the Applications folder
   - Open Docker from Applications

3. **Grant Permissions**:
   - You may be asked to enter your password to install networking components
   - Click "OK" and enter your password

4. **Complete Setup**:
   - Docker Desktop will start
   - You'll see the Docker icon in your menu bar
   - Wait for it to show "Docker Desktop is running"

### Linux (Ubuntu/Debian)

#### Installation Steps

1. **Update package index**:
   ```bash
   sudo apt-get update
   ```

2. **Install prerequisites**:
   ```bash
   sudo apt-get install -y \
       ca-certificates \
       curl \
       gnupg \
       lsb-release
   ```

3. **Add Docker's official GPG key**:
   ```bash
   sudo mkdir -p /etc/apt/keyrings
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
   ```

4. **Set up the repository**:
   ```bash
   echo \
     "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
     $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   ```

5. **Install Docker Engine**:
   ```bash
   sudo apt-get update
   sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
   ```

6. **Start Docker**:
   ```bash
   sudo systemctl start docker
   sudo systemctl enable docker
   ```

7. **Add your user to docker group** (optional, to run without sudo):
   ```bash
   sudo usermod -aG docker $USER
   ```

   Log out and back in for this to take effect.

### Linux (CentOS/RHEL/Fedora)

```bash
# Add Docker repository
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# Install Docker
sudo yum install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Start Docker
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group
sudo usermod -aG docker $USER
```

---

## Verifying Docker Installation

Open a terminal/command prompt and run:

```bash
docker --version
```

You should see something like:
```
Docker version 24.0.6, build ed223bc
```

Check Docker Compose:

```bash
docker compose version
```

You should see:
```
Docker Compose version v2.21.0
```

Test Docker is working:

```bash
docker run hello-world
```

If successful, you'll see a "Hello from Docker!" message.

---

## Setting Up the Application

### Step 1: Get the Application Files

#### Option A: Clone from GitHub (if you've uploaded it)

```bash
git clone https://github.com/yourusername/plex-movie-selector.git
cd plex-movie-selector
```

#### Option B: Use Your Local Files

If you already have the files locally:

```bash
cd C:\movie_selector
```

Or on Mac/Linux:

```bash
cd /path/to/movie_selector
```

### Step 2: Create Environment Configuration

1. **Copy the example environment file**:

   **Windows (Command Prompt):**
   ```cmd
   copy .env.example .env
   ```

   **Windows (PowerShell):**
   ```powershell
   Copy-Item .env.example .env
   ```

   **Mac/Linux:**
   ```bash
   cp .env.example .env
   ```

2. **Edit the .env file**:

   Open `.env` in a text editor (Notepad, VS Code, nano, etc.)

   **Windows:**
   ```cmd
   notepad .env
   ```

   **Mac:**
   ```bash
   open -e .env
   ```

   **Linux:**
   ```bash
   nano .env
   ```

3. **Configure your settings**:

   ```env
   # Generate a random secret key (important for security!)
   SECRET_KEY=change-this-to-a-long-random-string-abc123xyz789

   # Your Plex Server URL
   # If Plex is on the SAME computer as Docker:
   PLEX_SERVER_URL=http://host.docker.internal:32400

   # If Plex is on a DIFFERENT computer on your network:
   PLEX_SERVER_URL=http://192.168.1.100:32400
   # (replace 192.168.1.100 with your Plex server's IP address)

   # If Plex is on a remote server:
   PLEX_SERVER_URL=https://your-plex-server.com:32400
   ```

4. **Generate a secure SECRET_KEY**:

   **Python method** (if you have Python installed):
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```

   **Manual method**: Use a random string generator or create your own long random string (at least 32 characters)

5. **Find your Plex Server URL**:

   - Open Plex Web App
   - Go to Settings → Network
   - Look for "Custom server access URLs" or note your server's IP address
   - Default Plex port is 32400

---

## Running the Application

### Step 1: Build and Start the Container

In the project directory, run:

```bash
docker compose up -d
```

**What this does**:
- `docker compose`: Uses Docker Compose to manage the application
- `up`: Starts the containers
- `-d`: Runs in detached mode (in the background)

**First run will take a few minutes** as Docker:
1. Downloads the Python base image
2. Builds your application container
3. Installs all dependencies
4. Starts the application

You'll see output like:
```
[+] Building 45.3s (12/12) FINISHED
[+] Running 2/2
 ✔ Network movie_selector_plex-network  Created
 ✔ Container plex-movie-selector        Started
```

### Step 2: Verify the Application is Running

Check container status:

```bash
docker compose ps
```

You should see:
```
NAME                    IMAGE                  STATUS
plex-movie-selector     movie_selector-movie-selector   Up 30 seconds
```

Check the logs:

```bash
docker compose logs
```

Look for:
```
* Running on http://0.0.0.0:5000
```

### Step 3: Access the Application

Open your web browser and go to:

```
http://localhost:5000
```

You should see the Plex Movie Selector login page!

### Accessing from Other Devices on Your Network

To access from another device (phone, tablet, another computer):

1. **Find your computer's IP address**:

   **Windows:**
   ```cmd
   ipconfig
   ```
   Look for "IPv4 Address" (usually starts with 192.168.x.x)

   **Mac:**
   ```bash
   ifconfig | grep inet
   ```

   **Linux:**
   ```bash
   hostname -I
   ```

2. **Access from other device**:
   ```
   http://YOUR_COMPUTER_IP:5000
   ```

   For example: `http://192.168.1.50:5000`

---

## Managing the Application

### Stop the Application

```bash
docker compose stop
```

The container stops but is not removed. Data persists.

### Start the Application (after stopping)

```bash
docker compose start
```

### Restart the Application

```bash
docker compose restart
```

### Stop and Remove Containers

```bash
docker compose down
```

**Note**: This removes containers but keeps your data (database) in the `instance` folder.

### View Logs (Real-time)

```bash
docker compose logs -f
```

Press `Ctrl+C` to stop viewing logs.

### View Logs (Last 100 lines)

```bash
docker compose logs --tail=100
```

### Update the Application

After making code changes:

1. **Rebuild the container**:
   ```bash
   docker compose down
   docker compose build
   docker compose up -d
   ```

2. **Or in one command**:
   ```bash
   docker compose up -d --build
   ```

### Access Container Shell (for debugging)

```bash
docker compose exec movie-selector /bin/bash
```

Type `exit` to leave the container shell.

### Remove Everything (including data)

**WARNING**: This deletes your database!

```bash
docker compose down -v
rm -rf instance/
```

---

## Data Persistence

### Where is Data Stored?

The application database is stored in:
```
./instance/movie_selector.db
```

This folder is mounted as a Docker volume, so your data persists even when:
- You stop the container
- You remove the container
- You rebuild the container

### Backup Your Data

**Backup the database**:

```bash
# Create backups folder
mkdir backups

# Copy database (while container is running)
docker compose exec movie-selector cp /app/instance/movie_selector.db /app/instance/movie_selector_backup.db

# Copy to your computer
cp instance/movie_selector.db backups/movie_selector_$(date +%Y%m%d).db
```

**Restore from backup**:

```bash
docker compose stop
cp backups/movie_selector_20231115.db instance/movie_selector.db
docker compose start
```

---

## Troubleshooting

### Container Won't Start

**Check logs**:
```bash
docker compose logs
```

**Common issues**:

1. **Port 5000 already in use**:
   - Edit `docker-compose.yml`
   - Change `"5000:5000"` to `"5001:5000"` (or another port)
   - Access at `http://localhost:5001`

2. **Permission errors** (Linux):
   ```bash
   sudo chown -R $USER:$USER instance/
   ```

### Can't Connect to Plex Server

1. **Verify Plex is running**:
   - Open Plex Web App
   - Check server is online

2. **Check PLEX_SERVER_URL in .env**:
   - If same computer: `http://host.docker.internal:32400`
   - If different computer: `http://ACTUAL_IP:32400`

3. **Test connectivity from container**:
   ```bash
   docker compose exec movie-selector curl http://host.docker.internal:32400/web
   ```

### Application is Slow

1. **Check Docker resources** (Docker Desktop):
   - Settings → Resources
   - Increase CPUs and Memory if needed
   - Recommended: 2 CPUs, 4GB RAM

2. **Check container resources**:
   ```bash
   docker stats
   ```

### Database Errors

**Reset database** (WARNING: deletes all data):
```bash
docker compose down
rm -rf instance/
docker compose up -d
```

### Docker Commands Not Found

**Windows**: Make sure Docker Desktop is running (check system tray)

**Linux**:
```bash
sudo systemctl start docker
```

### Container Keeps Restarting

```bash
docker compose logs --tail=50
```

Look for Python errors in the logs. Common issues:
- Missing environment variables
- Database permission errors
- Python dependency errors

---

## Performance Optimization

### Reduce Image Size

The current Dockerfile is already optimized, but you can:

1. **Use multi-stage builds** (advanced)
2. **Clean up apt cache** (already done)
3. **Use alpine images** (smaller but may have compatibility issues)

### Increase Container Resources

Edit `docker-compose.yml` to add resource limits:

```yaml
services:
  movie-selector:
    # ... existing config ...
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 512M
```

---

## Security Best Practices

1. **Never commit .env file to Git** (already in .gitignore)
2. **Use strong SECRET_KEY** (generate random string)
3. **Don't expose port 5000 to the internet** without additional security (use reverse proxy with HTTPS)
4. **Keep Docker updated**:
   ```bash
   # Check for updates in Docker Desktop
   # Or on Linux:
   sudo apt-get update
   sudo apt-get upgrade docker-ce docker-ce-cli containerd.io
   ```

---

## Advanced: Using Docker with Reverse Proxy (HTTPS)

For production use with HTTPS, you can use nginx or Traefik as a reverse proxy. This is an advanced topic. Consult the respective documentation for setup.

---

## Getting Help

- **Docker Documentation**: https://docs.docker.com
- **Docker Forums**: https://forums.docker.com
- **Stack Overflow**: Tag your questions with `docker`

---

## Quick Reference

### Essential Commands

```bash
# Start application
docker compose up -d

# Stop application
docker compose stop

# View logs
docker compose logs -f

# Restart application
docker compose restart

# Rebuild after code changes
docker compose up -d --build

# Stop and remove everything
docker compose down

# View running containers
docker compose ps

# Access container shell
docker compose exec movie-selector /bin/bash
```

---

**Next Steps**: After Docker is running successfully, see the main README.md for how to use the application!
