#!/bin/bash

# OpenClaw Version Check Script
# Checks current vs latest version and logs changes

set -e

# Configuration
VERSION_LOG_FILE="${VERSION_LOG_PATH:-.}/version-history.json"
VERSION_LOG_DIR=$(dirname "$VERSION_LOG_FILE")

# Ensure log directory exists
mkdir -p "$VERSION_LOG_DIR"

# Get current version
CURRENT_VERSION=$(grep '"version"' /app/package.json 2>/dev/null | head -1 | sed 's/.*"version": "\([^"]*\)".*/\1/')

if [ -z "$CURRENT_VERSION" ]; then
  echo "❌ Could not determine current OpenClaw version"
  exit 1
fi

# Get latest version from NPM
LATEST_VERSION=$(curl -s https://registry.npmjs.org/openclaw/latest | grep -o '"version":"[^"]*"' | head -1 | sed 's/.*"\([^"]*\)".*/\1/')

if [ -z "$LATEST_VERSION" ]; then
  echo "❌ Could not fetch latest OpenClaw version from NPM"
  exit 1
fi

# Determine status
if [ "$CURRENT_VERSION" = "$LATEST_VERSION" ]; then
  STATUS="up-to-date"
else
  STATUS="update-available"
fi

# Get timestamp
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Create or update log file
if [ ! -f "$VERSION_LOG_FILE" ]; then
  echo '{"checks": []}' > "$VERSION_LOG_FILE"
fi

# Add new entry using jq
jq ".checks += [{
  \"timestamp\": \"$TIMESTAMP\",
  \"current\": \"$CURRENT_VERSION\",
  \"latest\": \"$LATEST_VERSION\",
  \"status\": \"$STATUS\"
}]" "$VERSION_LOG_FILE" > "$VERSION_LOG_FILE.tmp"

mv "$VERSION_LOG_FILE.tmp" "$VERSION_LOG_FILE"

# Output result
echo "✅ Version check completed"
echo "   Current:  $CURRENT_VERSION"
echo "   Latest:   $LATEST_VERSION"
echo "   Status:   $STATUS"
echo "   Log:      $VERSION_LOG_FILE"

# Return 0 if up-to-date, 1 if update available
[ "$STATUS" = "up-to-date" ]
