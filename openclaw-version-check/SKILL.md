---
name: openclaw-version-check
description: Monitor and manage OpenClaw version updates. Automatically check current vs latest version on NPM, log updates, and sync version history to GitHub. Use when needing to track OpenClaw upgrades, manage deployment versions, or maintain version history for audit purposes.
---

# OpenClaw Version Check

## Overview

Monitor OpenClaw version updates automatically and maintain a version history in GitHub. This skill provides tools to:
- Check current OpenClaw version vs latest available
- Log version changes with timestamps
- Sync version information to a GitHub repository
- Generate version change reports

## Quick Start

Use the main script to check and log versions:

```bash
./scripts/check_version.sh
```

This will:
1. Compare current version with NPM latest
2. Log any changes to `version-history.json`
3. Sync changes to GitHub repo

## Workflow

### 1. Check Version Status

Run periodic checks via cron or heartbeat:
```bash
./scripts/check_version.sh
```

Output: `version-history.json` with entries like:
```json
{
  "checks": [
    {
      "timestamp": "2026-01-30T17:43:00Z",
      "current": "2026.1.29",
      "latest": "2026.1.29",
      "status": "up-to-date"
    }
  ]
}
```

### 2. Sync to GitHub

After version changes detected:
```bash
./scripts/sync_to_github.sh <github-repo-path> <github-token>
```

This commits and pushes `version-history.json` to your myskill repo.

## Configuration

Set these environment variables:
- `GITHUB_REPO`: Your GitHub repo (e.g., `username/myskill`)
- `GITHUB_TOKEN`: GitHub personal access token
- `VERSION_LOG_PATH`: Where to store `version-history.json` (default: `./`)

## Resources

### scripts/
- `check_version.sh` - Check and log OpenClaw versions
- `sync_to_github.sh` - Push version history to GitHub

### references/
- `API.md` - NPM API reference for version checking
- `GITHUB-SYNC.md` - GitHub sync workflow details
