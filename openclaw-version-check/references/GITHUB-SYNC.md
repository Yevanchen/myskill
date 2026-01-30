# GitHub Sync Workflow

## Overview

Automatically sync version history to a GitHub repository for audit and tracking purposes.

## Setup

### 1. Create GitHub Personal Access Token

1. Go to GitHub Settings → Developer Settings → Personal Access Tokens
2. Create new token with `repo` scope (full control of repositories)
3. Copy the token (you'll use it once)

### 2. Configure Environment Variables

```bash
export GITHUB_REPO="username/myskill"
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxx"
export VERSION_LOG_PATH="/path/to/logs"
export REPO_DIR="/path/to/local/repo"
```

Or set in your shell profile or Zeabur environment variables.

### 3. Initialize Local Repository

If syncing to an existing repo:
```bash
git clone https://github.com/username/myskill.git
cd myskill
```

## Workflow

### Manual Sync

```bash
./scripts/check_version.sh          # Check versions and log
./scripts/sync_to_github.sh          # Push to GitHub
```

### Automated Sync with Cron

Schedule periodic syncs:

```bash
# Every 6 hours
0 */6 * * * /path/to/scripts/check_version.sh && /path/to/scripts/sync_to_github.sh
```

### With OpenClaw Cron

Use OpenClaw's cron system to schedule version checks and syncs:

```bash
cron add --name "Version Check and Sync" \
  --schedule "0 */6 * * *" \
  --payload "systemEvent:Check version and sync to GitHub"
```

## Commit Message Format

Version sync commits use format:
```
🔄 Update version history - 2026-01-30 17:43:00
```

## GitHub Repository Structure

After syncing, your repo will have:
```
myskill/
├── logs/
│   └── version-history.json
└── [other repo files]
```

## Troubleshooting

### Authentication Errors

```
fatal: Authentication failed for 'https://github.com/...'
```

- Check GITHUB_TOKEN is valid
- Verify token has `repo` scope
- Token might have expired (create a new one)

### Push Rejected

```
error: failed to push some refs to 'origin'
```

- Pull latest changes first: `git pull origin main`
- Ensure your local repo is up to date

### Missing Remote

```
fatal: 'origin' does not appear to be a remote repository
```

- Script auto-initializes git, but ensure GITHUB_REPO is correct format: `username/repo`
