# OAuth 2.0 Blog Publishing

Long-term, secure publishing solution using Google OAuth 2.0.

## Overview

Instead of hardcoding API keys or temporary tokens, the blog publishing system uses **Firebase service account credentials** to automatically generate **Google OAuth 2.0 tokens** on each publish.

### Flow

```
MDX File
    ↓
Extract frontmatter + content
    ↓
Generate slug
    ↓
Create JWT (signed with private key)
    ↓
Exchange JWT for Google OAuth 2.0 token
    ↓
Use token to authenticate Firestore REST API
    ↓
Publish to Firebase
```

## Prerequisites

### Environment Variables (Zeabur)

These should already be configured, but here's what you need:

- `client_email` - Service account email (e.g., `firebase-adminsdk-xxx@project.iam.gserviceaccount.com`)
- `private_key` - Base64-encoded private key (from service account JSON)

### Firestore Rules

Rules should allow OAuth-authenticated requests:

```firestore
rules_version = '2';

service cloud.firestore {
  match /databases/{database}/documents {
    match /bloglist/{blogId} {
      allow read: if true;
      allow write: if request.headers.authorization != null;
    }
  }
}
```

## Usage

### Publish a Single Article

```bash
python3 publish-blog-oauth.py /path/to/article.mdx
```

### Publish Multiple Articles

```bash
for mdx_file in *.mdx; do
  python3 publish-blog-oauth.py "$mdx_file"
done
```

## How It Works

### 1. JWT Creation

The script creates a **JWT (JSON Web Token)** containing:
- Service account email (`iss`)
- Scopes: `cloud-platform` (Firestore access)
- Expiry: 1 hour
- Issued at: current time

```json
{
  "iss": "firebase-adminsdk-xxx@project.iam.gserviceaccount.com",
  "scope": "https://www.googleapis.com/auth/cloud-platform",
  "aud": "https://oauth2.googleapis.com/token",
  "exp": 1234567890,
  "iat": 1234567800
}
```

### 2. JWT Signing

The JWT is signed with the **private key** using RSA SHA-256. This proves the request comes from the service account.

### 3. Token Exchange

The signed JWT is sent to Google's OAuth endpoint:

```
POST https://oauth2.googleapis.com/token
grant_type=urn:ietf:params:oauth:grant-type:jwt-bearer&assertion={JWT}
```

Google validates the JWT signature and returns an **access token**.

### 4. Firebase Authentication

The access token is sent to Firestore REST API:

```
Authorization: Bearer {access_token}
```

Firestore validates the token and processes the request.

## Security Benefits

✅ **No hardcoded credentials** — Only environment variables
✅ **No permanent tokens** — New token generated per request
✅ **Respects Firestore rules** — Proper authentication
✅ **Automatic expiry** — Token valid for 1 hour max
✅ **Auditable** — Google OAuth tracks all access
✅ **Rotatable** — Can revoke/regenerate service account anytime

## Troubleshooting

### "Missing credentials in environment"

Check if environment variables are set:

```bash
echo $client_email
echo $private_key
```

If empty, add to Zeabur environment.

### "Signing failed"

Private key format issue. Ensure it's:
- Base64-encoded (without PEM headers in environment)
- Valid RSA private key
- Script automatically formats it as PEM

### "Token exchange failed"

Usually means:
- Service account is disabled
- Project has billing issues
- OAuth endpoint is unreachable

Check service account in Firebase Console → Service Accounts.

### "Firestore API not enabled"

Enable Firestore API in Google Cloud Console:
1. Go to APIs & Services
2. Search "Firestore API"
3. Click "Enable"

## Comparison: Publishing Methods

| Method | Security | Setup | Long-term | Maintenance |
|--------|----------|-------|-----------|-------------|
| Hardcoded Key | ❌ Low | Easy | ❌ No (expires) | Key rotation needed |
| API Key Direct | ❌ Low | Easy | ❌ No | Anyone can access |
| Bearer Token | ⚠️ Medium | Medium | ❌ No (expires) | Manual refresh |
| OAuth 2.0 | ✅ High | Medium | ✅ Yes | Automatic |

## Implementation Details

See `scripts/publish-oauth.py` for the actual implementation.

Key steps:
1. Format private key from environment
2. Create JWT header + payload
3. Sign JWT with `openssl dgst -sha256`
4. Exchange JWT for token via `curl`
5. Publish to Firestore with token

## References

- [Google OAuth 2.0 Documentation](https://developers.google.com/identity/protocols/oauth2)
- [Firebase Service Accounts](https://firebase.google.com/docs/admin/setup)
- [JWT Introduction](https://jwt.io)
