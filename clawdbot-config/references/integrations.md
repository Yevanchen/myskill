# Integration Guides

Step-by-step guides for integrating external services with Clawdbot.

## Table of Contents
- [GitHub](#github)
- [Google Services](#google-services)
- [Discord](#discord)
- [Zeabur Configuration](#zeabur-configuration)

## GitHub

### Generate Personal Access Token

1. Go to: https://github.com/settings/tokens
2. Click **Generate new token → Personal access tokens (classic)**
3. Name: `Clawdbot`
4. Expiration: 90 days (or your preference)
5. **Select scopes**: Only check `repo` (read-only)
6. Click **Generate token**
7. **Copy immediately** (you won't see it again)

### Add to Zeabur

1. Zeabur Dashboard → Your Clawdbot Project
2. Settings → Environment Variables
3. Add: `GITHUB_TOKEN=ghp_xxxxxxxxxxxxx`
4. Click Save & Redeploy

### Test Connection

```bash
curl -H "Authorization: token ${GITHUB_TOKEN}" https://api.github.com/user
```

Expected response: Your GitHub profile info

---

## Google Services

### Create Service Account (OAuth)

1. Go to: https://console.cloud.google.com
2. Create a new project
3. APIs & Services → **Enable APIs** (Gmail, Drive, Calendar as needed)
4. APIs & Services → **Credentials**
5. Click **Create Credentials → Service Account**
6. Fill in name: `clawdbot-agent`
7. Grant roles: Editor (for testing; restrict later)
8. Create → Click on the service account
9. **Keys** tab → **Add Key → Create new key**
10. Choose JSON format
11. **Download** and save securely

### Add to Zeabur

The JSON file is large. Two options:

**Option 1: As environment variable (simple)**
```
GOOGLE_CREDENTIALS_JSON=<paste entire JSON here>
```

**Option 2: As file (recommended for production)**
1. Upload JSON to Zeabur's persistent storage
2. Set: `GOOGLE_CREDENTIALS_PATH=/path/to/credentials.json`

### Test Connection

```bash
python3 << 'EOF'
import json
import os

creds_json = os.getenv('GOOGLE_CREDENTIALS_JSON')
creds = json.loads(creds_json)
print(f"✅ Service Account: {creds['client_email']}")
EOF
```

---

## Discord

### Create Bot & Get Token

1. Go to: https://discord.com/developers/applications
2. Click **New Application**
3. Name: `Clawdbot`
4. Go to **Bot** → **Add Bot**
5. Under **TOKEN**, click **Copy**

### Set Permissions & Scope

1. OAuth2 → **URL Generator**
2. Scopes: `bot`
3. Permissions: 
   - Read/Send Messages
   - Read Message History
   - Embed Links
4. Copy generated URL and add bot to your server

### Add to Zeabur

```
DISCORD_TOKEN=MjYyxxxxxxxxxxxxxxxxxxxxxxxx
DISCORD_GUILD_ID=your_server_id
```

---

## Zeabur Configuration

### Environment Variables Setup

1. **Open Project Dashboard**
   - Zeabur Home → Select Clawdbot project

2. **Navigate to Settings**
   - Click "Settings" in the sidebar

3. **Find Environment Variables**
   - Look for "Environment" or "Variables" section

4. **Add Each Variable**
   - Click "+ Add Variable"
   - Paste: `KEY=VALUE`
   - Don't use quotes
   - Click Save

5. **Redeploy**
   - After adding all variables, click "Redeploy"
   - Wait 2-3 minutes for deployment

### Verify Deployment

Check logs:
1. Zeabur Dashboard → Deployments
2. Click latest deployment
3. Scroll to logs
4. Look for "Successfully loaded" or error messages

---

## Troubleshooting Integration Issues

### GitHub Token Not Working
- [ ] Token is valid (not expired)
- [ ] Scope includes `repo`
- [ ] Environment variable name is exactly `GITHUB_TOKEN`
- [ ] Redeploy after adding token

### Google Credentials Invalid
- [ ] JSON is valid (check syntax)
- [ ] APIs are enabled in Google Cloud Console
- [ ] Service account has correct permissions
- [ ] Email is verified if using Gmail API

### Discord Bot Not Responding
- [ ] Bot is online in your server
- [ ] Bot has message permissions
- [ ] Token hasn't been regenerated
- [ ] Intents are enabled (if required)

### Variables Not Being Read
- [ ] Spelling is exactly correct (case-sensitive)
- [ ] Format is `KEY=VALUE` (no quotes)
- [ ] **Redeploy triggered** (not just restart)
- [ ] Check deployment logs for errors
