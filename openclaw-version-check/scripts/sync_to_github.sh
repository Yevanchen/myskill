#!/bin/bash

# GitHub Sync Script
# Syncs version history to GitHub repository

set -e

# Parameters
GITHUB_REPO="${1:${GITHUB_REPO}}"
GITHUB_TOKEN="${2:${GITHUB_TOKEN}}"
VERSION_LOG_FILE="${VERSION_LOG_PATH:-.}/version-history.json"
REPO_DIR="${REPO_DIR:-.}"

# Validate inputs
if [ -z "$GITHUB_REPO" ]; then
  echo "❌ Error: GITHUB_REPO not provided"
  echo "Usage: $0 <github-repo> [github-token]"
  echo "Or set GITHUB_REPO and GITHUB_TOKEN environment variables"
  exit 1
fi

if [ -z "$GITHUB_TOKEN" ]; then
  echo "❌ Error: GITHUB_TOKEN not provided"
  exit 1
fi

# Check if version log exists
if [ ! -f "$VERSION_LOG_FILE" ]; then
  echo "❌ Version log not found: $VERSION_LOG_FILE"
  exit 1
fi

echo "📤 Syncing version history to GitHub..."

# Navigate to repo directory
cd "$REPO_DIR"

# Check if git is initialized
if [ ! -d ".git" ]; then
  echo "⚙️  Initializing git repository..."
  git init
  git remote add origin "https://x-access-token:${GITHUB_TOKEN}@github.com/${GITHUB_REPO}.git" 2>/dev/null || true
fi

# Configure git
git config user.email "version-checker@openclaw.ai" || true
git config user.name "OpenClaw Version Checker" || true

# Copy version log to repo
mkdir -p "logs"
cp "$VERSION_LOG_FILE" "logs/version-history.json"

# Commit and push
if git diff --quiet HEAD -- logs/version-history.json 2>/dev/null; then
  echo "✅ No changes to sync"
else
  echo "📝 Committing changes..."
  git add logs/version-history.json
  TIMESTAMP=$(date -u +"%Y-%m-%d %H:%M:%S")
  git commit -m "🔄 Update version history - $TIMESTAMP" || true
  
  echo "🚀 Pushing to GitHub..."
  git push -u origin main 2>&1 | grep -v "^remote:" || true
fi

echo "✅ GitHub sync completed"
