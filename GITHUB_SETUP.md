# GitHub Setup Instructions

This guide will walk you through putting your Plex Movie Selector application on GitHub.

## Prerequisites

- A GitHub account (create one at https://github.com/signup if needed)
- Git installed on your computer (see INSTALLATION.md for Git installation)

## Step-by-Step GitHub Setup

### Step 1: Create a GitHub Repository

1. **Go to GitHub** and log in to your account at https://github.com

2. **Create a new repository**:
   - Click the "+" icon in the top-right corner
   - Select "New repository"

3. **Configure your repository**:
   - **Repository name**: `plex-movie-selector` (or any name you prefer)
   - **Description**: "A web application for selecting random movies from Plex with intelligent filtering"
   - **Visibility**: Choose "Public" or "Private"
   - **DO NOT** check "Initialize this repository with a README" (we already have one)
   - **DO NOT** add .gitignore or license yet (we have these)
   - Click "Create repository"

4. **Copy the repository URL**:
   - After creating, you'll see a URL like: `https://github.com/yourusername/plex-movie-selector.git`
   - Keep this handy for the next steps

### Step 2: Initialize Git in Your Project (If Not Already Done)

Open a terminal/command prompt and navigate to your project directory:

```bash
cd C:\movie_selector
```

Initialize Git repository (if not already initialized):

```bash
git init
```

### Step 3: Add Your Files to Git

1. **Check which files will be added**:
   ```bash
   git status
   ```

2. **Add all files to Git**:
   ```bash
   git add .
   ```

3. **Verify files are staged**:
   ```bash
   git status
   ```

   You should see all your files in green. The `.gitignore` file will prevent sensitive files from being added.

### Step 4: Create Your First Commit

```bash
git commit -m "Initial commit: Plex Movie Selector application"
```

### Step 5: Connect to GitHub Repository

Replace `yourusername` and `repository-name` with your actual GitHub username and repository name:

```bash
git remote add origin https://github.com/yourusername/plex-movie-selector.git
```

Verify the remote was added:

```bash
git remote -v
```

### Step 6: Push Your Code to GitHub

1. **Rename the default branch to main** (if needed):
   ```bash
   git branch -M main
   ```

2. **Push your code**:
   ```bash
   git push -u origin main
   ```

3. **Authenticate**:
   - GitHub will prompt you for authentication
   - **Personal Access Token (Recommended)**:
     - Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
     - Click "Generate new token (classic)"
     - Give it a name: "Plex Movie Selector"
     - Select scopes: Check "repo" (all sub-options)
     - Click "Generate token"
     - **COPY THE TOKEN** (you won't see it again!)
     - Use this token as your password when pushing

### Step 7: Verify Upload

1. Go to your GitHub repository in your browser
2. You should see all your files listed
3. The README.md will be displayed on the main page

## Important: Protect Sensitive Information

### Before Pushing to Public Repository

Make sure these files are in your `.gitignore` (they already are):

```
.env
*.db
*.sqlite
__pycache__/
instance/
```

### Never Commit These Files:
- `.env` - Contains your secret keys
- `*.db` or `*.sqlite` - Contains your database with user data
- Any files with passwords or tokens

### If You Accidentally Committed Sensitive Data

If you accidentally committed sensitive information:

1. **Remove the file from Git** (keeps local copy):
   ```bash
   git rm --cached .env
   git commit -m "Remove sensitive file"
   git push
   ```

2. **Rotate any exposed secrets**:
   - Generate new SECRET_KEY
   - Change any exposed passwords
   - Regenerate Plex tokens if exposed

3. **For complete removal from history** (advanced):
   ```bash
   # WARNING: This rewrites history
   git filter-branch --force --index-filter \
   "git rm --cached --ignore-unmatch .env" \
   --prune-empty --tag-name-filter cat -- --all

   git push origin --force --all
   ```

## Updating Your Repository

After making changes to your code:

1. **Check what changed**:
   ```bash
   git status
   ```

2. **Add changed files**:
   ```bash
   git add .
   ```
   Or add specific files:
   ```bash
   git add app/models.py
   ```

3. **Commit changes**:
   ```bash
   git commit -m "Description of what you changed"
   ```

4. **Push to GitHub**:
   ```bash
   git push
   ```

## Common Git Commands

### View commit history
```bash
git log
```

### View changes before committing
```bash
git diff
```

### Undo changes to a file (before commit)
```bash
git checkout -- filename
```

### Create a new branch
```bash
git checkout -b feature-branch-name
```

### Switch branches
```bash
git checkout main
```

### Merge a branch
```bash
git checkout main
git merge feature-branch-name
```

## Cloning Your Repository on Another Computer

Once your code is on GitHub, you can clone it anywhere:

```bash
git clone https://github.com/yourusername/plex-movie-selector.git
cd plex-movie-selector
```

Then follow the installation instructions in INSTALLATION.md and DOCKER_INSTALL.md.

## Adding a GitHub Actions Badge (Optional)

You can add status badges to your README to show build status, etc. These can be added later as you set up CI/CD.

## Best Practices

1. **Commit Often**: Make small, focused commits with clear messages
2. **Write Good Commit Messages**:
   - ✅ "Add filter for movies by decade"
   - ❌ "Fixed stuff"
3. **Never Commit Secrets**: Use environment variables and .gitignore
4. **Use Branches**: Create feature branches for new features
5. **Pull Before Push**: If collaborating, always pull latest changes first

## Troubleshooting

### Error: "failed to push some refs"

This usually means the remote has changes you don't have locally:

```bash
git pull origin main --rebase
git push
```

### Error: "Permission denied"

Make sure you're using a Personal Access Token, not your password.

### Error: "Repository not found"

Check that:
- The repository URL is correct
- You have access to the repository
- You're logged in to the correct GitHub account

## Additional Resources

- [GitHub Documentation](https://docs.github.com)
- [Git Documentation](https://git-scm.com/doc)
- [GitHub Desktop](https://desktop.github.com) - GUI alternative to command line

## Security Checklist

Before making your repository public:

- [ ] `.env` file is in `.gitignore`
- [ ] No passwords or API keys in code
- [ ] No database files committed
- [ ] README doesn't contain sensitive information
- [ ] Example environment file (`.env.example`) has placeholder values only
- [ ] All secrets are loaded from environment variables

---

**Note**: If you make your repository public, anyone can see and copy your code. This is fine for the application logic, but make sure no sensitive data is included.
