---
name: clawdbot-config
description: Clawdbot configuration, environment setup, and integration guides. Use when configuring Clawdbot for new integrations (GitHub, Google, Discord, etc.), managing environment variables, or troubleshooting deployment issues on Zeabur or local environments. Includes ~/.clawdbot/clawdbot.json schema, environment variable management, and integration patterns.
---

# Clawdbot Configuration & Integration Guide

This skill provides configuration guidance, environment setup, and integration patterns for Clawdbot deployments.

## Quick Reference

### Standard Workflow
1. Add environment variables to deployment (Zeabur dashboard or local `.env`)
2. Configure service integrations in `~/.clawdbot/config.yaml`
3. Restart Clawdbot to apply changes

### Key Locations
- **Config file**: `~/.clawdbot/clawdbot.json` or `~/.clawdbot/config.yaml`
- **Environment variables**: Zeabur dashboard → Settings → Environment Variables
- **Logs**: Check Zeabur deployment logs for startup issues

## Configuration Patterns

### Environment Variables (Zeabur)

```bash
# GitHub
GITHUB_TOKEN=ghp_xxxxxxxxxxxx

# Google (if using OAuth)
GOOGLE_CREDENTIALS_JSON={"type":"service_account",...}

# Other APIs
BRAVE_API_KEY=xxx...
OPENAI_API_KEY=sk-xxx...

# Execution permissions
EXEC_SECURITY_MODE=allowlist
EXEC_ALLOWLIST=curl,git,python3,jq
```

### Service Configuration

```yaml
# ~/.clawdbot/config.yaml
services:
  github:
    token: ${GITHUB_TOKEN}
  
  google:
    credentialPath: /tmp/google-creds.json
```

## Common Integration Scenarios

### Add GitHub Access
See [INTEGRATIONS.md](references/integrations.md#github) for token generation.

### Enable Google API Access
See [INTEGRATIONS.md](references/integrations.md#google) for OAuth setup.

### Configure Discord Bot
See [INTEGRATIONS.md](references/integrations.md#discord) for bot token setup.

## Schema Reference

For complete configuration schema:
- See [CONFIG-SCHEMA.md](references/config-schema.md)

For all available environment variables:
- See [ENVIRONMENT-VARIABLES.md](references/environment-variables.md)

## Real-World Examples

See [EXAMPLES.md](references/examples.md) for:
- Zeabur deployment setup
- Local development configuration
- Multi-service integration
- Troubleshooting common issues
