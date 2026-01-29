---
name: blog-publishing
description: Complete guide for writing, publishing, and managing MDX blog posts on Firebase. Use when creating or editing blog articles, publishing to Firestore, or maintaining blog metadata. Covers frontmatter structure, slug generation, content guidelines, security, and automated publishing workflow.
---

# Blog Publishing Skill

Write and publish MDX blog articles with confidence. This skill covers the complete workflow from drafting to deployment on Firebase.

## Quick Start

### 1. Create a New Blog via Editor

```bash
# Web UI: /blog/editor
# Or use the script directly
```

**Minimum required fields:**
- **Title** - Article heading (English or Chinese)
- **Content** - MDX markdown text
- **Summary** - 1-2 sentence preview (optional but recommended)
- **Tags** - Comma-separated labels (e.g., `next-js, firebase, guide`)
- **Date** - Auto-set to current date

**Slug generation:**
- Automatically generated from title
- English titles: lowercase + special chars removed + hyphens for spaces (e.g., "My First Post" → `my-first-post`)
- Chinese titles or special-char-only titles: fallback to `post-{random}` (e.g., `post-7f8e9d3c`)
- Slug cannot be empty; editor validates before save

### 2. Publish via Script

```bash
python3 /home/node/clawd/submit-blog-to-firebase.py
# Reads: /home/node/clawd/your-article.mdx
# Output: Posted to Firebase + access URL
```

### 3. Verify Publication

- Check blog list: https://chenyefan.zeabur.app/blog
- Click article title (only works if slug is valid)
- All blogs are readable; only authenticated users can edit/delete

---

## MDX Frontmatter Format

**Template:**

```yaml
---
title: "Your Article Title"
date: "2026-01-29T18:30:00Z"
draft: false
summary: "One-sentence preview of your article"
tags: ["tag1", "tag2", "category"]
authors: ["evanchen"]
---

# Article Content Here (Markdown/MDX)
...
```

**Field Reference:**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `title` | string | ✅ Yes | Article headline |
| `date` | ISO 8601 | ✅ Yes | Publication date (e.g., `2026-01-29T18:30:00Z`) |
| `draft` | boolean | ❌ No | Set `true` to hide from main blog list (default: `false`) |
| `summary` | string | ❌ No | 1-2 sentence preview (shows in blog list) |
| `tags` | array | ❌ No | Categories/labels (e.g., `["python", "tutorial"]`) |
| `authors` | array | ❌ No | Author names (default: `["Admin"]`) |
| `slug` | string | 🔄 Auto | Generated from title; not manually editable in YAML (system-generated) |
| `fileName` | string | 🔄 Auto | MDX file name including extension |
| `content` | string | ✅ Yes | Article body (Markdown/MDX syntax) |
| `lastmod` | ISO 8601 | 🔄 Auto | Last modification timestamp |

---

## Slug Generation Rules

**Goal:** Every blog post must have a unique, valid slug for web routing.

### Slug Generation Logic

1. **English/Mixed Content:**
   - Convert to lowercase
   - Remove special characters: keep only `a-z`, `0-9`, spaces
   - Replace spaces with hyphens
   - Strip leading/trailing hyphens
   - Examples:
     - `"My First Post!"` → `my-first-post`
     - `"React 2025: Guide"` → `react-2025-guide`
     - `"Hello-World"` → `hello-world`

2. **Chinese/Pure Special Characters:**
   - If slug is empty after cleanup, fallback to: `post-{8-character random ID}`
   - Examples:
     - `"你好世界"` → `post-7f8e9d3c`
     - `"!!!@@##"` → `post-a1b2c3d4`

3. **Validation:**
   - Empty slugs are **not allowed**
   - Web UI enforces validation before save
   - Blog list shows visual indicator (❌) for invalid slugs

---

## Firebase Security & Authentication

### Current Setup

**Firestore Rules:**
```firestore
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /bloglist/{blogId} {
      allow read: if true;  // ✅ Anyone can read
      allow write: if request.headers.authorization == 'Bearer sk_blog_evanchen_20260129_7f8e9d3c4b5a6f7e8d9c0b1a2f3e4d5c';
    }
  }
}
```

**Environment Variables (Zeabur):**
- `BLOG_AUTH_TOKEN` = `sk_blog_evanchen_20260129_7f8e9d3c4b5a6f7e8d9c0b1a2f3e4d5c`
- `NEXT_PUBLIC_FIREBASE_*` - Firebase config (API key, project ID, etc.)

### Authentication Flow

1. **Web UI Writes:** Uses Firebase Client SDK + stored token in Zeabur env
2. **Script Writes:** Includes `Authorization: Bearer {token}` header in API requests
3. **Without Token:** Writes are rejected (403 Forbidden)

### Security Best Practices

- ✅ **Never commit credentials** to Git (always use environment variables)
- ✅ **Token rotation:** If token leaks, generate new one and update Firestore rules
- ✅ **Read-only public:** Blog posts are readable by anyone; writes restricted
- ✅ **Draft mode:** Set `draft: true` to hide posts (doesn't prevent read access, just hides from lists)

---

## Publishing Workflows

### Workflow 1: Web UI Editor

1. Navigate to `/blog/editor`
2. Fill in fields (title, content, tags, summary)
3. Click **Save Article**
4. System auto-generates slug
5. Redirected to blog list
6. Verify article appears and link works

**Notes:**
- Slug auto-validated before save
- No manual slug editing in UI
- Title-only posts work fine (slug auto-generated)

### Workflow 2: Script-Based Publishing

**File location:** `/home/node/clawd/submit-blog-to-firebase.py`

**Usage:**

```bash
# Edit your MDX file
nano /home/node/clawd/my-article.mdx

# Run submission script (reads from file path)
python3 /home/node/clawd/submit-blog-to-firebase.py

# Output:
# ✅ Success! Document ID: my-first-post
# 🔗 Access: https://chenyefan.zeabur.app/blog/my-first-post
```

**Script features:**
- Extracts frontmatter (YAML)
- Generates slug from title
- Validates slug (no empty slugs)
- Sends to Firebase via REST API with auth token
- Returns access URL

### Workflow 3: Batch Updates (Advanced)

For bulk operations (e.g., updating multiple articles), contact admin or use Firebase Console directly.

---

## Common Scenarios

### Scenario 1: Post Article in Chinese

```yaml
---
title: "我的第一篇博客"
date: "2026-01-29T12:00:00Z"
summary: "一篇关于我的想法的文章"
tags: ["思考", "生活"]
---
```

**Result:**
- Slug auto-generated: `post-7f8e9d3c` (since title is pure Chinese)
- Article published immediately
- Accessible at: `/blog/post-7f8e9d3c`

### Scenario 2: Post Article with Code Blocks

```markdown
---
title: "React Hook Tutorial"
summary: "Learn custom React hooks"
tags: ["react", "javascript", "tutorial"]
---

## Custom Hook Example

\`\`\`jsx
function useCounter(initial = 0) {
  const [count, setCount] = useState(initial)
  return [count, () => setCount(count + 1)]
}
\`\`\`
```

**Notes:**
- Supports JSX syntax in code blocks
- Markdown rendering is automatic

### Scenario 3: Schedule Post (Draft Mode)

```yaml
---
title: "Future Article (Coming Soon)"
date: "2026-06-01T00:00:00Z"
draft: true
---
```

**Effect:**
- Post is saved in Firebase
- Not shown in main blog list
- Direct link `/blog/future-article` still works (if you share it)
- Set `draft: false` later to publish

### Scenario 4: Fix Invalid Slug After Publishing

**Problem:** Article has empty or invalid slug → link doesn't work

**Solution A (UI):** Delete article + recreate with valid title

**Solution B (Manual):** Edit document in Firebase Console:
1. Open Firebase Console → myblog-personal → Firestore → bloglist
2. Find the document
3. Edit `slug` field to valid value
4. Save

---

## Troubleshooting

### "Slug is empty" Error

**Cause:** Title contains only special characters or unprintable characters

**Fix:**
- Use a title with at least one alphanumeric character
- Or let system generate `post-{random}` fallback

### "Article doesn't appear in blog list"

**Causes:**
1. `draft: true` - Remove to publish
2. Invalid slug - Blog list hides articles with empty slugs (shows ❌ icon)
3. Firebase not loaded - Wait a few seconds for real-time sync

**Fix:**
- Check slug field in Firebase Console
- If empty, manually set to valid value (e.g., `post-abc123`)

### "Link returns 404"

**Cause:** Slug is invalid (empty, contains only hyphens, etc.)

**Fix:**
- Update `slug` field in Firebase Console
- Refresh blog list page
- Verify new slug is showing

### "Authentication error when publishing via script"

**Cause:** `BLOG_AUTH_TOKEN` environment variable not set

**Fix:**
```bash
export BLOG_AUTH_TOKEN="sk_blog_evanchen_20260129_7f8e9d3c4b5a6f7e8d9c0b1a2f3e4d5c"
python3 submit-blog-to-firebase.py
```

---

## Next Steps

See reference files for detailed guides:

- **[MDX Template](references/mdx-template.md)** - Full example with code blocks, links, embeds
- **[Firebase Admin Guide](references/firebase-guide.md)** - Credentials, rules, debugging
- **[Markdown Syntax](references/markdown-cheatsheet.md)** - Common patterns, tips
