# Environment Variables Reference

Complete list of environment variables for Clawdbot configuration.

## Table of Contents
- [Authentication & Tokens](#authentication--tokens)
- [Execution & Security](#execution--security)
- [Services Configuration](#services-configuration)
- [Deployment Settings](#deployment-settings)

## Authentication & Tokens

### GitHub
```
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
```
- **Source**: GitHub Settings → Developer Settings → Personal Access Tokens
- **Permissions**: Minimal (read:repo, read:user)
- **Used for**: Repository access, code operations

### Google Services
```
GOOGLE_CREDENTIALS_JSON={"type":"service_account","project_id":"..."}
```
- **Source**: Google Cloud Console → APIs & Services → Credentials
- **Format**: Full Service Account JSON
- **Used for**: Gmail, Google Drive, Google Calendar access

### OpenAI
```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
```
- **Source**: https://platform.openai.com/api/keys
- **Used for**: GPT models, image generation

### Brave Search
```
BRAVE_API_KEY=xxxxxxxxxxxxxxxx
```
- **Source**: https://api.search.brave.com
- **Used for**: Web search functionality

## Execution & Security

### Allowlist Mode
```
EXEC_SECURITY_MODE=allowlist
EXEC_ALLOWLIST=curl,git,python3,jq,cat,ls,echo
```
- **Options**: `allowlist`, `full`, `deny`
- **Default**: `deny`
- **Used for**: Controlling which shell commands can run

### Minimum Safe Allowlist
```
EXEC_ALLOWLIST=curl,git,python3,cat,echo
```

### Full Allowlist (Testing)
```
EXEC_SECURITY_MODE=full
```

## Services Configuration

### Discord Bot
```
DISCORD_TOKEN=MjYyxxxxxxxxxxxxxxxxxxxxxxxxx
```
- **Source**: Discord Developer Portal → Bot Settings → Token

### Telegram Bot
```
TELEGRAM_BOT_TOKEN=xxxxxxxxxxxxx:xxxxxxxxxxxxxxxxxxx
```
- **Source**: BotFather on Telegram

## Deployment Settings

### Zeabur-Specific
```
NODE_ENV=production
LOG_LEVEL=info | debug | error
```

### Local Development
```
NODE_ENV=development
LOG_LEVEL=debug
```

## How to Add in Zeabur

1. Go to Zeabur Dashboard
2. Select your Clawdbot project
3. Click **Settings**
4. Find **Environment Variables**
5. Click **Add Variable**
6. Paste: `KEY=VALUE`
7. Click **Save & Redeploy**

## Best Practices

✅ **DO**:
- Use environment variables for secrets
- Minimize token permissions (read-only when possible)
- Rotate tokens periodically
- Use allowlist for exec security

❌ **DON'T**:
- Hardcode secrets in code
- Share tokens in chat/Discord
- Use admin-level permissions unless necessary
- Leave secrets in git history

## Troubleshooting

### Variable Not Being Read
- Check spelling (case-sensitive)
- Verify format (no quotes needed in Zeabur)
- After adding, trigger a **Redeploy** (not just restart)

### Permission Denied on Exec
- Verify `EXEC_ALLOWLIST` includes the command
- Check `EXEC_SECURITY_MODE` is set correctly
- Restart Gateway after changing exec settings

### Token Invalid/Expired
- Re-generate token from the service
- Update in Zeabur environment variables
- Redeploy
