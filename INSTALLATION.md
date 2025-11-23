# Complete Installation Guide

This comprehensive guide covers installing all requirements needed to run the Plex Movie Selector application, whether using Docker or running it directly with Python.

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation Path Decision](#installation-path-decision)
3. [Installing Git](#installing-git)
4. [Installing Python](#installing-python)
5. [Installing Docker](#installing-docker)
6. [Getting the Application](#getting-the-application)
7. [Setting Up Python Virtual Environment](#setting-up-python-virtual-environment)
8. [Installing Python Dependencies](#installing-python-dependencies)
9. [Configuring the Application](#configuring-the-application)
10. [Running the Application](#running-the-application)
11. [Troubleshooting](#troubleshooting)

---

## System Requirements

### Minimum Requirements

- **Operating System**:
  - Windows 10/11 (64-bit)
  - macOS 10.15 or newer
  - Linux (Ubuntu 20.04+, Debian 10+, CentOS 8+, Fedora 35+)

- **Hardware**:
  - 2 GB RAM minimum (4 GB recommended)
  - 500 MB free disk space
  - Internet connection

- **Network**:
  - Access to a Plex Media Server (local network or remote)
  - Plex account with access to the server

### Software Requirements

You'll need to install (detailed instructions below):

**For Docker Installation (Recommended)**:
- Docker Desktop (Windows/Mac) or Docker Engine (Linux)
- Git (for cloning from GitHub)

**For Python Installation**:
- Python 3.11 or newer
- pip (Python package manager, usually included with Python)
- Git (optional, for cloning from GitHub)

---

## Installation Path Decision

Choose ONE of these two installation methods:

### Option A: Docker Installation (Recommended)

**Pros**:
- ✅ Easier setup - no need to install Python
- ✅ Consistent environment across all systems
- ✅ Isolated from other applications
- ✅ Easier to update and manage
- ✅ Better for production use

**Cons**:
- ❌ Requires Docker (additional download)
- ❌ Uses more system resources
- ❌ Slightly more complex if you need to debug

**Best for**: Users who want a simple, reliable setup or plan to run this long-term

### Option B: Python Installation

**Pros**:
- ✅ Direct control over the code
- ✅ Easier to modify and debug
- ✅ No Docker overhead
- ✅ Better for development

**Cons**:
- ❌ More setup steps
- ❌ Need to manage Python environment
- ❌ Can conflict with other Python projects
- ❌ Different behavior across systems

**Best for**: Developers, users who want to modify the code, or users who already have Python

---

## Installing Git

Git is used to download the application from GitHub and track changes.

### Windows

#### Option 1: Git for Windows (Recommended)

1. **Download Git**:
   - Go to https://git-scm.com/download/windows
   - Click "Click here to download" for the latest version
   - Save the installer file

2. **Run the Installer**:
   - Double-click the downloaded `.exe` file
   - Click "Next" through the setup wizard
   - **Important settings**:
     - Default editor: Choose your preferred editor (VS Code, Notepad++, or Vim)
     - Path environment: Select "Git from the command line and also from 3rd-party software"
     - HTTPS transport backend: Use "Use the OpenSSL library"
     - Line ending conversions: "Checkout Windows-style, commit Unix-style"
     - Terminal emulator: "Use MinTTY"
   - Click "Install"
   - Click "Finish"

3. **Verify Installation**:
   Open Command Prompt or PowerShell:
   ```cmd
   git --version
   ```
   You should see: `git version 2.x.x`

#### Option 2: GitHub Desktop (GUI Alternative)

1. Download from https://desktop.github.com
2. Install and sign in with your GitHub account
3. Provides a graphical interface instead of command line

### macOS

#### Option 1: Using Homebrew (Recommended)

1. **Install Homebrew** (if not already installed):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install Git**:
   ```bash
   brew install git
   ```

3. **Verify Installation**:
   ```bash
   git --version
   ```

#### Option 2: Using Xcode Command Line Tools

1. **Install Xcode Command Line Tools**:
   ```bash
   xcode-select --install
   ```

2. **Click "Install"** in the popup window

3. **Verify Installation**:
   ```bash
   git --version
   ```

### Linux

#### Ubuntu/Debian

```bash
sudo apt-get update
sudo apt-get install -y git
git --version
```

#### CentOS/RHEL/Fedora

```bash
sudo yum install -y git
# OR for newer versions:
sudo dnf install -y git

git --version
```

### Configure Git (All Platforms)

After installing Git, configure your identity:

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

---

## Installing Python

Required only if you're NOT using Docker.

### Windows

#### Option 1: Official Python Installer (Recommended)

1. **Download Python**:
   - Go to https://www.python.org/downloads/
   - Click "Download Python 3.11.x" (or latest 3.11+ version)
   - Save the installer

2. **Run the Installer**:
   - Double-click the downloaded `.exe` file
   - **IMPORTANT**: Check "Add Python 3.11 to PATH" at the bottom
   - Click "Install Now"
   - Wait for installation to complete
   - Click "Close"

3. **Verify Installation**:
   Open Command Prompt:
   ```cmd
   python --version
   ```
   Should show: `Python 3.11.x`

   Check pip:
   ```cmd
   pip --version
   ```
   Should show: `pip 23.x.x from ...`

#### Option 2: Windows Store

1. Open Microsoft Store
2. Search for "Python 3.11"
3. Click "Get" or "Install"
4. Verify installation (same as above)

### macOS

#### Option 1: Using Homebrew (Recommended)

1. **Install Homebrew** (if not already installed):
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **Install Python**:
   ```bash
   brew install python@3.11
   ```

3. **Add to PATH** (add to `~/.zshrc` or `~/.bash_profile`):
   ```bash
   echo 'export PATH="/usr/local/opt/python@3.11/bin:$PATH"' >> ~/.zshrc
   source ~/.zshrc
   ```

4. **Verify Installation**:
   ```bash
   python3 --version
   pip3 --version
   ```

#### Option 2: Official Python Installer

1. Go to https://www.python.org/downloads/macos/
2. Download Python 3.11.x macOS installer
3. Run the `.pkg` file
4. Follow installation wizard
5. Verify installation

### Linux

#### Ubuntu/Debian

```bash
# Update package list
sudo apt-get update

# Install Python 3.11
sudo apt-get install -y python3.11 python3.11-venv python3-pip

# Verify installation
python3.11 --version
pip3 --version
```

If Python 3.11 is not available:

```bash
# Add deadsnakes PPA
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt-get update
sudo apt-get install -y python3.11 python3.11-venv python3.11-dev
```

#### CentOS/RHEL/Fedora

```bash
# CentOS/RHEL 8+
sudo dnf install -y python3.11 python3.11-pip

# Fedora
sudo dnf install -y python3.11

# Verify installation
python3.11 --version
pip3 --version
```

---

## Installing Docker

See **DOCKER_INSTALL.md** for complete Docker installation instructions for all platforms.

Quick summary:

- **Windows/Mac**: Download and install Docker Desktop from https://www.docker.com/products/docker-desktop
- **Linux**: Install Docker Engine using package manager

Verify installation:
```bash
docker --version
docker compose version
```

---

## Getting the Application

### Option 1: Clone from GitHub (Recommended)

If you've uploaded the code to GitHub:

```bash
# Navigate to where you want to store the project
cd ~/Projects  # or C:\Users\YourName\Projects on Windows

# Clone the repository
git clone https://github.com/yourusername/plex-movie-selector.git

# Navigate into the project
cd plex-movie-selector
```

### Option 2: Download ZIP from GitHub

1. Go to your GitHub repository
2. Click the green "Code" button
3. Click "Download ZIP"
4. Extract the ZIP file to your desired location
5. Open terminal/command prompt in that folder

### Option 3: Use Existing Local Files

If you already have the files:

```bash
# Navigate to the project directory
cd C:\movie_selector
# or on Mac/Linux:
cd /path/to/movie_selector
```

---

## Setting Up Python Virtual Environment

**Required only for Python installation** (skip if using Docker).

A virtual environment isolates this project's dependencies from other Python projects.

### Windows (Command Prompt)

```cmd
# Navigate to project directory
cd C:\movie_selector

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate
```

Your prompt should now show `(venv)` at the beginning.

### Windows (PowerShell)

```powershell
# Navigate to project directory
cd C:\movie_selector

# Create virtual environment
python -m venv venv

# Enable script execution (one-time, if needed)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Activate virtual environment
venv\Scripts\Activate.ps1
```

### macOS/Linux

```bash
# Navigate to project directory
cd /path/to/movie_selector

# Create virtual environment
python3.11 -m venv venv

# Activate virtual environment
source venv/bin/activate
```

Your prompt should show `(venv)` at the beginning.

### Deactivating Virtual Environment

When you're done working:

```bash
deactivate
```

**Note**: You need to activate the virtual environment every time you open a new terminal to work on this project.

---

## Installing Python Dependencies

**Required only for Python installation** (skip if using Docker).

### Install Requirements

With virtual environment activated:

```bash
# Upgrade pip first (recommended)
pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- Flask-SQLAlchemy (database)
- Flask-Login (user authentication)
- PlexAPI (Plex integration)
- python-dotenv (environment variables)
- requests (HTTP library)

### Verify Installation

```bash
pip list
```

You should see all the packages listed.

### Troubleshooting Installation Issues

#### Windows: Microsoft C++ Build Tools Error

If you see errors about "Microsoft Visual C++ 14.0 is required":

1. Download "Build Tools for Visual Studio" from:
   https://visualstudio.microsoft.com/downloads/
2. Scroll down to "All Downloads" → "Tools for Visual Studio"
3. Download "Build Tools for Visual Studio 2022"
4. Run installer and select "C++ build tools"
5. Try `pip install -r requirements.txt` again

#### macOS: Xcode Command Line Tools

If you get compilation errors:

```bash
xcode-select --install
```

#### Linux: Missing Development Headers

```bash
# Ubuntu/Debian
sudo apt-get install -y python3.11-dev build-essential

# CentOS/RHEL
sudo dnf install -y python3.11-devel gcc
```

---

## Configuring the Application

### Step 1: Create Environment File

**All installation methods**:

```bash
# Windows (Command Prompt)
copy .env.example .env

# Windows (PowerShell)
Copy-Item .env.example .env

# macOS/Linux
cp .env.example .env
```

### Step 2: Edit Configuration

Open `.env` in a text editor:

```bash
# Windows
notepad .env

# macOS
open -e .env

# Linux
nano .env
# or
vim .env
```

### Step 3: Set Required Values

```env
# REQUIRED: Generate a secure random secret key
SECRET_KEY=your-very-long-random-secret-key-here

# REQUIRED: Your Plex Server URL
PLEX_SERVER_URL=http://your-plex-server:32400

# OPTIONAL: Database location (default is fine for most users)
DATABASE_URI=sqlite:///movie_selector.db
```

### Finding Your Plex Server URL

#### Same Computer

- **Not using Docker**: `http://localhost:32400`
- **Using Docker**: `http://host.docker.internal:32400`

#### Different Computer on Same Network

1. Find Plex server's IP address:
   - On the Plex server computer, run:
     - Windows: `ipconfig`
     - Mac/Linux: `ifconfig` or `ip addr`
   - Look for IP starting with `192.168.x.x` or `10.x.x.x`

2. Use that IP:
   ```
   PLEX_SERVER_URL=http://192.168.1.100:32400
   ```

#### Remote Server

If your Plex server is accessible over the internet:

```
PLEX_SERVER_URL=https://your-domain.com:32400
```

### Generating a Secure SECRET_KEY

#### Using Python:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output into your `.env` file.

#### Using Online Generator:

Go to https://randomkeygen.com/ and copy a "CodeIgniter Encryption Key"

#### Manual:

Create a random string of at least 32 characters with letters, numbers, and symbols.

---

## Running the Application

### Using Docker

See **DOCKER_INSTALL.md** for detailed instructions.

Quick start:

```bash
# Build and start
docker compose up -d

# View logs
docker compose logs -f

# Stop
docker compose down
```

Access at: http://localhost:5000

### Using Python

#### Start the Application

With virtual environment activated:

```bash
# Windows
python run.py

# macOS/Linux
python3 run.py
```

You should see:

```
* Running on http://0.0.0.0:5000
* Running on http://127.0.0.1:5000
```

#### Access the Application

Open your browser to:
```
http://localhost:5000
```

#### Stop the Application

Press `Ctrl+C` in the terminal where the app is running.

---

## Troubleshooting

### Common Issues

#### "python: command not found" (macOS/Linux)

Try `python3` instead:
```bash
python3 --version
python3 run.py
```

#### "pip: command not found" (macOS/Linux)

Try `pip3` instead:
```bash
pip3 --version
pip3 install -r requirements.txt
```

#### Port 5000 Already in Use

**Error**: "Address already in use"

**Solution**: Change the port in `.env`:

```env
PORT=5001
```

Then restart the application. Access at http://localhost:5001

#### Permission Denied (Linux/macOS)

If you get permission errors with the database:

```bash
chmod 755 instance/
chmod 644 instance/movie_selector.db
```

#### Virtual Environment Not Activating (Windows PowerShell)

**Error**: "cannot be loaded because running scripts is disabled"

**Solution**:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activating again.

#### Flask App Not Found

Make sure you're in the project directory:

```bash
ls -la  # Should show run.py, requirements.txt, etc.
pwd     # Should show /path/to/movie_selector
```

#### Database Errors

Reset the database:

```bash
# Stop the application
# Delete the database
rm -rf instance/
# Restart the application (database will be recreated)
```

#### Plex Connection Errors

1. Verify Plex server is running
2. Check `PLEX_SERVER_URL` in `.env`
3. Test connectivity:
   ```bash
   curl http://localhost:32400/web
   # Should return HTML
   ```

---

## Environment Comparison

| Feature | Docker | Python |
|---------|--------|--------|
| Installation Time | 10-15 min | 5-10 min |
| Disk Space | ~500 MB | ~200 MB |
| Ease of Setup | Easier | Moderate |
| Ease of Updates | Very Easy | Moderate |
| Performance | Good | Slightly Better |
| Isolation | Excellent | Moderate |
| Best For | Production, beginners | Development, advanced users |

---

## Next Steps

After successful installation:

1. **Login**: Use your Plex username/email and password
2. **Configure Filters**: Set your movie preferences
3. **Get Recommendations**: Click "Get Recommendation"
4. **Enjoy**: Watch your randomly selected movie!

See the main **README.md** for detailed usage instructions.

---

## Additional Resources

### Documentation

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Python Documentation](https://docs.python.org/3/)
- [Docker Documentation](https://docs.docker.com/)
- [Plex API Documentation](https://python-plexapi.readthedocs.io/)

### Getting Help

- **Python Issues**: https://stackoverflow.com/questions/tagged/python
- **Docker Issues**: https://forums.docker.com/
- **Plex Issues**: https://forums.plex.tv/

### Keeping Updated

#### Update Python Dependencies

```bash
# Activate virtual environment first
pip install --upgrade -r requirements.txt
```

#### Update Docker

```bash
docker compose pull
docker compose up -d
```

#### Update Git Repository

```bash
git pull origin main
```

---

## Security Checklist

Before running in production:

- [ ] Generated a strong, unique SECRET_KEY
- [ ] `.env` file is not committed to Git (check `.gitignore`)
- [ ] Using HTTPS if exposing to internet (use reverse proxy)
- [ ] Firewall configured if exposing to network
- [ ] Regular backups of `instance/movie_selector.db`
- [ ] Docker/Python/dependencies kept up to date

---

## Performance Tips

### For Python Installation

- Use Python 3.11+ (faster than 3.10 and earlier)
- Consider using PyPy for better performance (advanced)

### For Docker Installation

- Allocate sufficient resources in Docker Desktop settings
- Use Docker volumes for better I/O performance (already configured)

### General

- Run on an SSD for better database performance
- Ensure stable network connection to Plex server
- Close unused applications to free up resources

---

**Congratulations!** You now have everything installed and configured. Proceed to **DOCKER_INSTALL.md** or start the Python application with `python run.py`!
