# Clawdbot Configuration Schema

## File Locations

### Primary Config
- **Zeabur**: Environment variables in dashboard → Settings → Environment Variables
- **Local**: `~/.clawdbot/config.yaml` or `~/.clawdbot/config.json`

## Complete Configuration Structure

```yaml
gateway:
  # Gateway daemon configuration
  port: 8080
  host: 0.0.0.0
  
  security:
    exec:
      mode: allowlist | full | deny
      allowlist:
        - curl
        - git
        - python3
        - jq

services:
  # Service integrations
  github:
    token: ${GITHUB_TOKEN}
    
  google:
    credentialPath: /path/to/credentials.json
    # Or embed as environment variable
    
  discord:
    token: ${DISCORD_TOKEN}
    
  openai:
    apiKey: ${OPENAI_API_KEY}

channels:
  # Message channel configuration
  discord:
    enabled: true
    token: ${DISCORD_TOKEN}
    
  telegram:
    enabled: false
    botToken: ${TELEGRAM_BOT_TOKEN}
    
  whatsapp:
    enabled: false
    apiKey: ${WHATSAPP_API_KEY}

memory:
  # Memory/storage settings
  type: file | redis | memory
  path: /home/node/clawd/memory  # For file type
```

## Configuration via Environment Variables (Zeabur)

When deploying on Zeabur, use environment variables. The Gateway reads them on startup:

```
# Format: KEY=VALUE
GITHUB_TOKEN=ghp_xxxxx
GOOGLE_CREDENTIALS_JSON={"type":"service_account",...}
EXEC_SECURITY_MODE=allowlist
EXEC_ALLOWLIST=curl,git,python3
```

## Loading Order

1. **Environment variables** (highest priority)
2. **config.yaml file** (if present)
3. **config.json file** (fallback)
4. **Defaults** (built-in)

## Validation

The Gateway validates configuration on startup. If there are issues:
- Check logs in Zeabur dashboard
- Verify environment variable syntax
- Ensure all required fields are present
