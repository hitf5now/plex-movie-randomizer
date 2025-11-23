# Setting Up for Unraid Docker UI Installation

This guide helps you prepare your Plex Movie Selector project for installation through the Unraid Docker UI.

## Overview

To enable Unraid Docker UI installation, you need to:
1. Upload your code to GitHub
2. Make a few small adjustments to the template
3. Test the installation in Unraid

## Step-by-Step Setup

### Step 1: Prepare Your Files

Make sure these files are in your project:

**Required files:**
- ✅ `Dockerfile.unraid` - Unraid-optimized Dockerfile
- ✅ `plex-movie-selector.xml` - Unraid template
- ✅ `requirements.txt` - Python dependencies
- ✅ `run.py` - Application entry point
- ✅ `app/` directory with all application files
- ✅ `.dockerignore` - Excludes unnecessary files from Docker build
- ✅ `.gitignore` - Prevents committing sensitive files

**Optional but recommended:**
- ✅ `icon.png` - Container icon for Unraid (200x200px or larger)
- ✅ `README.md` - Project documentation
- ✅ `UNRAID_UI_INSTALL.md` - User installation guide

### Step 2: Create a Container Icon (Optional)

Create a 200x200px (or larger) PNG icon for your container.

**Quick options:**

1. **Use an existing Plex-related icon** from the web
2. **Create a custom icon** using:
   - Canva (free)
   - GIMP (free)
   - Photoshop
3. **Use a placeholder** - Download a movie reel icon

Save as `icon.png` in your project root.

### Step 3: Upload to GitHub

Follow the instructions in `GITHUB_SETUP.md`, or quick version:

```bash
# Navigate to your project
cd C:\movie_selector

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: Plex Movie Selector for Unraid"

# Add your GitHub repository as remote
git remote add origin https://github.com/yourusername/plex-movie-selector.git

# Push to GitHub
git branch -M main
git push -u origin main
```

Replace `yourusername` with your actual GitHub username.

### Step 4: Update the XML Template

Edit `plex-movie-selector.xml` and replace all instances of `yourusername` with your actual GitHub username:

**Find and replace:**
```xml
<!-- OLD -->
https://github.com/yourusername/plex-movie-selector

<!-- NEW -->
https://github.com/YOURACTUALUSERNAME/plex-movie-selector
```

**Lines to update:**
- `<Repository>` - Line 4
- `<Registry>` - Line 5
- `<Support>` - Line 10
- `<Project>` - Line 11
- `<TemplateURL>` - Line 25
- `<Icon>` - Line 26

**Example:**
If your GitHub username is `john_doe`, change:
```xml
<Repository>https://github.com/john_doe/plex-movie-selector.git</Repository>
<Icon>https://raw.githubusercontent.com/john_doe/plex-movie-selector/main/icon.png</Icon>
```

### Step 5: Rename Dockerfile (IMPORTANT)

Unraid needs the Dockerfile to be named exactly `Dockerfile`:

**Option A: Replace existing Dockerfile**
```bash
# Backup original
mv Dockerfile Dockerfile.standard

# Use Unraid version
mv Dockerfile.unraid Dockerfile

# Commit changes
git add .
git commit -m "Use Unraid-optimized Dockerfile"
git push
```

**Option B: Keep both (recommended for development)**

If you want to keep both versions:
1. Keep `Dockerfile.unraid` as the Unraid version
2. Update XML template to specify which to use (advanced)

For simplicity, we recommend Option A for Unraid-only deployments.

### Step 6: Test Your Repository URL

Verify the repository is accessible:

1. Open browser and go to:
   ```
   https://github.com/YOURUSERNAME/plex-movie-selector
   ```

2. Verify these files are visible:
   - `Dockerfile` (or `Dockerfile.unraid`)
   - `requirements.txt`
   - `run.py`
   - `app/` directory

3. Check raw URLs work:
   ```
   https://raw.githubusercontent.com/YOURUSERNAME/plex-movie-selector/main/Dockerfile
   https://raw.githubusercontent.com/YOURUSERNAME/plex-movie-selector/main/icon.png
   ```

### Step 7: Install in Unraid

Now you can install in Unraid!

**Method 1: Direct GitHub URL (Recommended)**

1. Unraid → Docker tab → Add Container
2. **Repository**: `https://github.com/YOURUSERNAME/plex-movie-selector.git#main`
3. Fill in other settings per `UNRAID_UI_INSTALL.md`
4. Click Apply
5. Unraid will clone and build automatically!

**Method 2: Import XML Template**

1. Download `plex-movie-selector.xml` to your computer
2. Upload to `/mnt/user/appdata/` in Unraid
3. Unraid → Docker tab → Add Container
4. Click template dropdown → Browse to XML file
5. Imports all settings automatically!

**Method 3: Community Applications (Advanced)**

For sharing with others:
1. Submit your template to Community Applications
2. Others can install with one click from CA
3. See Unraid CA submission guidelines

## Troubleshooting Setup

### Git Push Fails

**Error:** "remote: Permission to user/repo.git denied"

**Solution:**
- Use Personal Access Token (see GITHUB_SETUP.md)
- Or check SSH keys are configured

### Unraid Can't Clone Repository

**Error:** "Unable to clone repository"

**Solutions:**

1. **Verify repository is public:**
   - GitHub → Your repo → Settings
   - Scroll down to "Danger Zone"
   - Check it's not private

2. **Check repository URL format:**
   ```
   # Correct formats:
   https://github.com/username/plex-movie-selector.git
   https://github.com/username/plex-movie-selector.git#main

   # Wrong formats:
   https://github.com/username/plex-movie-selector (missing .git)
   git@github.com:username/plex-movie-selector.git (SSH, not supported)
   ```

3. **Verify Unraid has internet access:**
   - Unraid Terminal: `ping github.com`

### Build Fails in Unraid

**Error:** "Cannot locate specified Dockerfile"

**Solution:**
- Ensure file is named exactly `Dockerfile` (capital D, no extension)
- Verify it's in the root of your repository
- Check it wasn't excluded by `.dockerignore`

**Error:** "Failed to build"

**Check:**
1. View build logs in Unraid (Docker → Container → Logs)
2. Verify `requirements.txt` is present
3. Check all Python files are in `app/` directory
4. Ensure `run.py` exists in root

### Icon Not Showing

**Solutions:**

1. **Verify icon.png exists:**
   - Check in GitHub repository root
   - Should be publicly accessible

2. **Test raw URL:**
   ```
   https://raw.githubusercontent.com/YOURUSERNAME/plex-movie-selector/main/icon.png
   ```
   - Should display the image
   - If 404, icon wasn't committed/pushed

3. **Icon URL in XML:**
   - Edit `plex-movie-selector.xml`
   - Update `<Icon>` tag with correct username
   - Re-import template in Unraid

## Configuration Checklist

Before sharing or deploying:

### GitHub Repository
- [ ] Repository is public (or accessible to Unraid)
- [ ] All files committed and pushed
- [ ] `Dockerfile` (not Dockerfile.unraid) is in root
- [ ] `requirements.txt` is present
- [ ] `app/` directory structure is correct
- [ ] `.gitignore` prevents `.env` and `*.db` files
- [ ] `README.md` exists with documentation

### XML Template
- [ ] All `yourusername` replaced with actual username
- [ ] Icon URL points to your repository
- [ ] Support and Project URLs updated
- [ ] TemplateURL updated (if hosting template elsewhere)

### Testing
- [ ] Repository URL loads in browser
- [ ] Raw Dockerfile URL works
- [ ] Icon URL displays image
- [ ] XML template imports correctly in Unraid
- [ ] Container builds successfully
- [ ] Application starts and is accessible

### Documentation
- [ ] README.md updated with your information
- [ ] UNRAID_UI_INSTALL.md included for users
- [ ] Installation instructions are clear
- [ ] Support information provided

## Updating After Installation

When you update your code:

```bash
# Make your changes
git add .
git commit -m "Description of changes"
git push

# In Unraid:
# Docker tab → Container icon → Force Update
# Rebuilds from latest GitHub code
```

## Sharing Your Template

Once tested and working:

### Option 1: Direct GitHub Link

Share this with others:
```
https://github.com/YOURUSERNAME/plex-movie-selector
```

Users can manually add the container using your GitHub URL.

### Option 2: Template URL

Host your XML template and share:
```
https://raw.githubusercontent.com/YOURUSERNAME/plex-movie-selector/main/plex-movie-selector.xml
```

Users can import this URL directly in Unraid.

### Option 3: Community Applications

For widest reach:
1. Fork the CA template repository
2. Add your `plex-movie-selector.xml`
3. Submit pull request
4. Once approved, appears in Community Applications

See: https://forums.unraid.net/topic/38582-plug-in-community-applications/

## Best Practices

### Keep It Simple
- Don't require SSH access
- All configuration through Unraid UI variables
- Sensible defaults for all settings
- Clear error messages

### Documentation
- Include UNRAID_UI_INSTALL.md in repository
- Keep README.md updated
- Provide examples for PLEX_SERVER_URL
- Document all environment variables

### Testing
- Test on fresh Unraid installation
- Verify with minimal configuration
- Test with both token and password auth
- Check all documented scenarios work

### Maintenance
- Keep dependencies updated
- Test after Unraid updates
- Monitor GitHub issues
- Update documentation as needed

## Support Resources

### For Setup Questions
- This file (SETUP_FOR_UNRAID.md)
- GITHUB_SETUP.md - Git and GitHub help
- UNRAID_UI_INSTALL.md - User installation guide

### For Unraid Questions
- https://forums.unraid.net/
- Docker Engine section
- Community Applications section

### For Issues
- Create issues on your GitHub repository
- Provide logs and configuration details
- Check existing issues first

## Quick Start Commands

```bash
# Setup from scratch
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOURUSERNAME/plex-movie-selector.git
git branch -M main
git push -u origin main

# Update XML template
sed -i 's/yourusername/YOURUSERNAME/g' plex-movie-selector.xml

# Rename Dockerfile for Unraid
mv Dockerfile Dockerfile.standard
mv Dockerfile.unraid Dockerfile
git add .
git commit -m "Prepare for Unraid"
git push

# Test URLs
echo "Repository: https://github.com/YOURUSERNAME/plex-movie-selector"
echo "Dockerfile: https://raw.githubusercontent.com/YOURUSERNAME/plex-movie-selector/main/Dockerfile"
echo "Icon: https://raw.githubusercontent.com/YOURUSERNAME/plex-movie-selector/main/icon.png"
echo "Template: https://raw.githubusercontent.com/YOURUSERNAME/plex-movie-selector/main/plex-movie-selector.xml"
```

## Summary

To make your project Unraid-ready:

1. ✅ Create/update all required files
2. ✅ Upload to public GitHub repository
3. ✅ Update XML template with your username
4. ✅ Rename `Dockerfile.unraid` to `Dockerfile`
5. ✅ Test repository URLs are accessible
6. ✅ Install in Unraid using GitHub URL
7. ✅ Share with others!

Your users can now install with just a GitHub URL - no SSH, no manual file creation, all configuration through the Unraid UI!

---

**Ready to Deploy?** Once setup is complete, users follow `UNRAID_UI_INSTALL.md` for a simple, guided installation experience.
