# Firebase Configuration & Troubleshooting

Guide for managing Firebase setup, security rules, and debugging publishing issues.

## Firebase Project Overview

**Project ID:** `myblog-personal`
**Region:** Global (Firestore multi-region)

### Collections

- **`bloglist`** - All blog posts
  - Document ID: Auto-generated or slug-based
  - Fields: title, slug, content, date, tags, draft, etc.

### Firestore Rules (Current)

```firestore
rules_version = '2';

service cloud.firestore {
  match /databases/{database}/documents {
    match /bloglist/{blogId} {
      allow read: if true;
      allow write: if request.headers.authorization == 'Bearer sk_blog_evanchen_20260129_7f8e9d3c4b5a6f7e8d9c0b1a2f3e4d5c';
    }
  }
}
```

**Security Model:**
- ✅ **Public read** - Anyone can read all blog posts
- 🔐 **Authenticated write** - Only requests with valid token can publish/edit
- 🔐 **No delete** - Rules don't explicitly allow delete (security default)

## Environment Variables

### Web Application (Next.js)

Set these in `.env.local` or Zeabur environment:

```env
# Firebase configuration (from Firebase Console)
NEXT_PUBLIC_FIREBASE_API_KEY=AIzaSy...
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=myblog-personal.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=myblog-personal
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=myblog-personal.firebasestorage.app
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=1071308430329
NEXT_PUBLIC_FIREBASE_APP_ID=1:1071308430329:web:3d04c1cc3681f16c7f7b28
NEXT_PUBLIC_FIREBASE_MEASUREMENT_ID=G-M5JRXRQW4L

# Authentication token for publishing
BLOG_AUTH_TOKEN=sk_blog_evanchen_20260129_7f8e9d3c4b5a6f7e8d9c0b1a2f3e4d5c
```

### Publishing Script

```bash
export BLOG_AUTH_TOKEN="sk_blog_evanchen_20260129_7f8e9d3c4b5a6f7e8d9c0b1a2f3e4d5c"
python3 submit-blog-to-firebase.py
```

## Getting Firebase Credentials

### Step 1: Open Firebase Console

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Select project: `myblog-personal`
3. Click **Settings** ⚙️ → **Project Settings**

### Step 2: Find API Credentials

Under **General** tab, scroll to **Your apps**:

```
Firebase SDK snippet
Web
const firebaseConfig = {
  apiKey: "AIzaSy...",
  authDomain: "myblog-personal.firebaseapp.com",
  projectId: "myblog-personal",
  storageBucket: "myblog-personal.firebasestorage.app",
  messagingSenderId: "1071308430329",
  appId: "1:1071308430329:web:3d04c1cc3681f16c7f7b28",
  measurementId: "G-M5JRXRQW4L"
};
```

Copy these values into your `.env` file.

### Step 3: Update Firestore Rules

1. Go to **Firestore Database** (left sidebar)
2. Click **Rules** tab
3. Replace with new rules (see above)
4. Click **Publish**

## Authentication & Token Management

### Current Token

```
sk_blog_evanchen_20260129_7f8e9d3c4b5a6f7e8d9c0b1a2f3e4d5c
```

### Rotate Token (When Leaked or Expired)

1. **Generate new token:**
   ```python
   import random, string
   new_token = 'sk_blog_' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=40))
   print(new_token)
   ```

2. **Update Firestore Rules:**
   ```firestore
   allow write: if request.headers.authorization == 'Bearer {NEW_TOKEN}';
   ```

3. **Update Environment Variables:**
   - Zeabur: `BLOG_AUTH_TOKEN = {NEW_TOKEN}`
   - Local: `.env` file

4. **Publish Rules** in Firebase Console

5. **Update Scripts:** Edit `submit-blog-to-firebase.py` with new token

## Common Issues & Solutions

### Issue 1: "Authentication Failed" When Publishing

**Error Message:**
```
Request had invalid authentication credentials. Expected OAuth 2 access token...
```

**Causes:**
- `BLOG_AUTH_TOKEN` not set
- Token is outdated or wrong
- Token not in request headers

**Solution:**
```bash
# Check token is set
echo $BLOG_AUTH_TOKEN

# If empty, set it
export BLOG_AUTH_TOKEN="sk_blog_evanchen_20260129_7f8e9d3c4b5a6f7e8d9c0b1a2f3e4d5c"

# Try again
python3 submit-blog-to-firebase.py
```

### Issue 2: Blog Post Appears But Link is Broken (404)

**Cause:** Slug is invalid (empty, contains only hyphens, etc.)

**Solution:**
1. Open Firebase Console → Firestore → bloglist collection
2. Find the document with broken link
3. Check the `slug` field
4. If empty or invalid, manually set it:
   ```
   slug: "valid-slug-here"
   ```
5. Refresh blog list page

### Issue 3: Can't Edit Articles After Publishing

**Cause:** Firestore rules are too strict (require token)

**Current rules allow:**
- ✅ Read (anyone)
- ✅ Write with token (authenticated)
- ❌ Delete (not allowed)

**To enable delete:**
```firestore
allow delete: if request.headers.authorization == 'Bearer sk_blog_evanchen_20260129_7f8e9d3c4b5a6f7e8d9c0b1a2f3e4d5c';
```

Then publish rules.

### Issue 4: "Slug is Empty" Error in Editor

**Cause:** Title contains only special characters or is empty

**Solution:**
- Use a title with at least one letter or number
- Or let the system generate `post-{random}` slug

### Issue 5: Firebase Quota Exceeded

**Error:** `PERMISSION_DENIED: Cloud Firestore operation failed: This operation has consumed the maximum allowed operations`

**Solution:**
- Check Firestore usage in Firebase Console
- Upgrade to Blaze plan if on Spark (free) plan
- Optimize queries to read fewer documents

## Monitoring & Debugging

### Check Firestore Usage

1. Firebase Console → **Firestore Database**
2. Click **Usage** tab
3. View reads/writes/deletes per day

### View Database

1. Firebase Console → **Firestore Database**
2. Click **Data** tab
3. Expand `bloglist` collection
4. Click document to view/edit fields

### Check Publishing Logs

For script-based publishing:
```bash
python3 submit-blog-to-firebase.py 2>&1 | tee publish.log
```

For web UI, check browser console:
```javascript
// Open DevTools (F12) → Console tab
// Look for errors starting with "Firebase"
```

## Security Best Practices

### ✅ Do

- Use environment variables for tokens
- Rotate tokens periodically (e.g., quarterly)
- Keep Firebase rules restrictive (read public, write authenticated)
- Use HTTPS for all requests
- Enable Firestore audit logging (in Firebase Console)

### ❌ Don't

- Hardcode tokens in source code
- Commit `.env` files to Git
- Use overly permissive rules (`allow read/write: if true`)
- Share tokens via unencrypted channels
- Leave old tokens active after rotation

## Advanced: Service Account Setup (Optional)

For more control, use Firebase Admin SDK with service account:

1. Go to Firebase Console → **Settings** ⚙️ → **Service Accounts**
2. Click **Generate New Private Key**
3. Save JSON file (keep private!)
4. Use in Python:

```python
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('serviceAccountKey.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Now you can use admin SDK (bypasses rules)
db.collection('bloglist').document('my-post').set({
  'title': 'My Post',
  'slug': 'my-post'
})
```

**Security Note:** Service accounts have full access. Never expose the JSON file.

## Resources

- [Firebase Documentation](https://firebase.google.com/docs)
- [Firestore Security Rules](https://firebase.google.com/docs/firestore/security/start)
- [Firebase Console](https://console.firebase.google.com/)
- [Firestore Pricing](https://firebase.google.com/pricing)
