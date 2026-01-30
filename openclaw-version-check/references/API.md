# NPM Registry API Reference

## OpenClaw Latest Version

Endpoint to fetch the latest published version of OpenClaw from NPM registry.

### Request

```bash
curl https://registry.npmjs.org/openclaw/latest
```

### Response Format

```json
{
  "name": "openclaw",
  "version": "2026.1.29",
  "description": "...",
  "dist": {
    "integrity": "...",
    "shasum": "...",
    "tarball": "https://registry.npmjs.org/openclaw/-/openclaw-2026.1.29.tgz"
  }
}
```

### Extracting Version

Using grep and sed:
```bash
curl -s https://registry.npmjs.org/openclaw/latest | grep -o '"version":"[^"]*"' | sed 's/.*"\([^"]*\)".*/\1/'
```

Using jq (if available):
```bash
curl -s https://registry.npmjs.org/openclaw/latest | jq -r '.version'
```

## Version History

See `version-history.json` for local version check history with timestamps and status.

Format:
```json
{
  "checks": [
    {
      "timestamp": "2026-01-30T17:43:00Z",
      "current": "2026.1.29",
      "latest": "2026.1.29",
      "status": "up-to-date" | "update-available"
    }
  ]
}
```
