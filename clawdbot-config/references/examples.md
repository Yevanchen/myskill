# Configuration Examples

Real-world configuration examples for common Clawdbot setups.

## Table of Contents
- [Zeabur Deployment (Cloud)](#zeabur-deployment-cloud)
- [Local Development](#local-development)
- [Multi-Service Integration](#multi-service-integration)
- [Troubleshooting Real Scenarios](#troubleshooting-real-scenarios)

## Zeabur Deployment (Cloud)

### Minimal Setup (GitHub Only)

**Environment Variables in Zeabur:**
```
GITHUB_TOKEN=ghp_Xxxxxxxxxxxxxxxxxxx
EXEC_SECURITY_MODE=allowlist
EXEC_ALLOWLIST=curl,git,python3,echo
```

**What this enables:**
- GitHub repo access
- Ability to run curl, git, python3 commands
- No external API calls beyond GitHub

**Deploy flow:**
1. Add above variables to Zeabur
2. Click Redeploy
3. Wait 2-3 minutes
4. Check logs for success

---

### Full Stack (GitHub + Google + Discord)

**Environment Variables:**
```
# Authentication
GITHUB_TOKEN=ghp_Xxxxxxxxxxxxxxxxxxxxxxxx
GOOGLE_CREDENTIALS_JSON={"type":"service_account","project_id":"my-project",...}
DISCORD_TOKEN=MjYyxxxxxxxxxxxxxxxxxxxxxxx

# Execution
EXEC_SECURITY_MODE=allowlist
EXEC_ALLOWLIST=curl,git,python3,jq,cat,ls,echo,grep,sed

# Logging
LOG_LEVEL=info
```

**What this enables:**
- Full GitHub integration (repos, PRs, gists)
- Google Services (Gmail, Drive, Sheets)
- Discord bot functionality
- Advanced data processing (jq, sed, grep)

**Config file (~/.clawdbot/config.yaml):**
```yaml
gateway:
  security:
    exec:
      mode: allowlist
      allowlist:
        - curl
        - git
        - python3
        - jq
        - cat
        - ls

services:
  github:
    token: ${GITHUB_TOKEN}
  
  google:
    credentialPath: /tmp/google-creds.json
```

---

## Local Development

### Mac Development Setup

**Step 1: Install dependencies**
```bash
brew install git curl python3
pip3 install jq-like
```

**Step 2: Create config**
```bash
mkdir -p ~/.clawdbot
cat > ~/.clawdbot/config.yaml << 'EOF'
gateway:
  port: 8080
  security:
    exec:
      mode: allowlist
      allowlist:
        - curl
        - git
        - python3
        - cat
        - ls

services:
  github:
    token: ${GITHUB_TOKEN}
EOF
```

**Step 3: Set environment variables**
```bash
export GITHUB_TOKEN=ghp_Xxxxxxxxxxxxx
export LOG_LEVEL=debug
```

**Step 4: Start Clawdbot**
```bash
clawdbot gateway start
```

**Step 5: Test**
```bash
curl http://localhost:8080/status
```

---

## Multi-Service Integration

### Use Case: GitHub → Google Sheets → Discord Notifications

This flow:
1. Monitors GitHub repos
2. Logs activity to Google Sheets
3. Posts updates to Discord

**Required environment variables:**
```
GITHUB_TOKEN=ghp_xxxxx
GOOGLE_CREDENTIALS_JSON={...}
DISCORD_TOKEN=Mj_xxx
EXEC_ALLOWLIST=curl,git,python3,echo
```

**Workflow script (Python):**
```python
import os
import json
import subprocess

# Get recent GitHub activity
github_token = os.getenv('GITHUB_TOKEN')
result = subprocess.run([
    'curl', '-s',
    '-H', f'Authorization: token {github_token}',
    'https://api.github.com/user/repos'
], capture_output=True, text=True)

repos = json.loads(result.stdout)

# Log to Google Sheets (via API)
# Post to Discord (via webhook)

for repo in repos[:5]:
    print(f"Repo: {repo['name']}")
```

---

## Troubleshooting Real Scenarios

### Scenario 1: GitHub Token Works in Zeabur, But Commands Fail

**Symptoms:**
- `curl -H "Authorization: token $GITHUB_TOKEN"` works manually
- But exec commands return "Permission Denied"

**Solution:**
```
EXEC_SECURITY_MODE=allowlist
EXEC_ALLOWLIST=curl,git
```
Then **Redeploy** (important!)

---

### Scenario 2: Google Credentials JSON Too Large for Environment Variable

**Symptoms:**
- Zeabur rejects the environment variable (too long)
- Or JSON parsing fails

**Solution:** Use file-based approach
```bash
# 1. Create credentials file in Zeabur's persistent storage
# 2. Set environment variable to file path instead:
GOOGLE_CREDENTIALS_PATH=/persistent/google-creds.json

# 3. Update config.yaml:
services:
  google:
    credentialPath: ${GOOGLE_CREDENTIALS_PATH}
```

---

### Scenario 3: Discord Bot Added But Not Responding

**Symptoms:**
- Bot is online in Discord
- But doesn't respond to messages

**Check:**
1. Bot permissions: Read Messages, Send Messages
2. Bot intents enabled (if required)
3. Token hasn't been regenerated recently
4. Check Zeabur logs for errors

**Debug:**
```bash
# Verify token is correct
curl -H "Authorization: Bot YOUR_TOKEN" \
  https://discord.com/api/v10/users/@me

# Should return bot info, not error
```

---

### Scenario 4: Variables Work Locally, Fail on Zeabur

**Symptoms:**
- Local `GITHUB_TOKEN=...` works
- Same token on Zeabur doesn't work

**Common causes:**
1. **Variable name typo** - Check exact spelling
2. **Quotes in value** - Zeabur sometimes adds quotes
3. **Cache issue** - Browser cache interfering
4. **Not redeployed** - Restart alone won't apply env changes

**Solution:**
1. Delete variable from Zeabur
2. Wait 10 seconds
3. Re-add with exact spelling
4. Click "Redeploy" (not restart)
5. Wait for deployment to complete
6. Check logs

---

## Real-World Workflow

### Complete Journey: Set Up GitHub + Exec on Zeabur

1. **Generate GitHub token** (on GitHub.com)
   - Settings → Developer → Personal Access Tokens
   - Create token with `repo` scope
   - Copy: `ghp_Xxxxx...`

2. **Add to Zeabur**
   - Open Zeabur project
   - Settings → Environment Variables
   - Add: `GITHUB_TOKEN=ghp_Xxxxx...`
   - Add: `EXEC_SECURITY_MODE=allowlist`
   - Add: `EXEC_ALLOWLIST=curl,git,python3`

3. **Redeploy**
   - Click Redeploy button
   - Wait for green checkmark

4. **Test**
   - Check deployment logs for success message
   - If you have access: `curl $GITHUB_TOKEN | grep login`

5. **Use**
   - Ask Clawdbot to access your repos
   - It will use the token automatically
