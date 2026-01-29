# Markdown Cheatsheet for Blog Posts

Quick reference for markdown syntax supported in blog articles.

## Headers

```markdown
# H1 - Main Title
## H2 - Section Title
### H3 - Subsection
#### H4 - Minor Section
```

## Text Formatting

```markdown
**Bold text** or __bold__
*Italic text* or _italic_
~~Strikethrough~~
`inline code`
```

**Renders as:**
- **Bold text** or __bold__
- *Italic text* or _italic_
- ~~Strikethrough~~
- `inline code`

## Lists

### Unordered List
```markdown
- Item 1
- Item 2
  - Nested item
  - Another nested
- Item 3
```

### Ordered List
```markdown
1. First step
2. Second step
3. Third step
```

### Checklist
```markdown
- [x] Completed task
- [ ] Pending task
- [x] Done
```

## Code Blocks

### JavaScript
\`\`\`javascript
function hello(name) {
  console.log(\`Hello, \${name}!\`)
}
\`\`\`

### Python
\`\`\`python
def fibonacci(n):
  if n <= 1:
    return n
  return fibonacci(n-1) + fibonacci(n-2)
\`\`\`

### TypeScript with Highlighting
\`\`\`typescript
interface User {
  id: string
  name: string
  email: string
}

const user: User = {
  id: "1",
  name: "John",
  email: "john@example.com"
}
\`\`\`

### Shell/Bash
\`\`\`bash
# Clone repository
git clone https://github.com/user/repo.git
cd repo

# Install dependencies
npm install

# Run development server
npm run dev
\`\`\`

### YAML (for config files)
\`\`\`yaml
# Database configuration
database:
  host: localhost
  port: 5432
  username: admin
  password: ${DB_PASSWORD}
\`\`\`

**Supported languages:** javascript, python, typescript, bash, yaml, json, html, css, sql, go, rust, and more.

## Links & Images

### Links
```markdown
[Link text](https://example.com)
[Link with title](https://example.com "Hover text")
<https://example.com>
```

### Images
```markdown
![Alt text](https://example.com/image.jpg)
![Alt text](https://example.com/image.jpg "Image title")
```

## Tables

```markdown
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Cell 1   | Cell 2   | Cell 3   |
| Cell 4   | Cell 5   | Cell 6   |
```

| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Cell 1   | Cell 2   | Cell 3   |
| Cell 4   | Cell 5   | Cell 6   |

### Alignment
```markdown
| Left | Center | Right |
|:-----|:------:|------:|
| L1   |  C1    |    R1 |
| L2   |  C2    |    R2 |
```

## Blockquotes

```markdown
> This is a blockquote
> 
> It can span multiple lines
> 
> > And nested quotes

> **Note:** Important information
```

> This is a blockquote
> 
> It can span multiple lines
> 
> > And nested quotes

## Horizontal Rules

```markdown
---
***
___
```

---

## Special Elements

### Info Box
```markdown
> ℹ️ **Note:** This is important information
```

### Warning
```markdown
> ⚠️ **Warning:** Be careful with this
```

### Success
```markdown
> ✅ **Success:** Operation completed
```

### Error
```markdown
> ❌ **Error:** Something went wrong
```

## Emoji Support

Common emoji you can use:

```markdown
✅ Success / Done
❌ Failed / Error
⚠️ Warning
ℹ️ Info / Note
💡 Idea / Tip
🚀 Launch / Rocket
🔧 Tools / Fix
📝 Document / Notes
🎯 Target / Goal
```

Examples:
- ✅ Completed
- ❌ Not working
- ⚠️ Caution required
- 💡 Good idea
- 🚀 Ready to deploy

## Escape Characters

```markdown
\*Not italic\*
\[Not a link\]
\`Not code\`
```

## Line Breaks

```markdown
Line one  
Line two (two spaces at end creates line break)

Line three (blank line creates paragraph break)
```

## Tips for Better Articles

1. **Use descriptive headers** - Readers scan headers first
2. **Keep paragraphs short** - 2-3 sentences max
3. **Use lists** - Easier to scan than paragraphs
4. **Add code examples** - Show, don't just tell
5. **Link to resources** - Help readers dive deeper
6. **Use emphasis** - **Bold** for key terms
7. **Add visual breaks** - Use headers and blank lines
8. **Check for typos** - Bad spelling looks unprofessional

## Common Patterns

### Tutorial Step-by-Step
```markdown
## Step 1: Set Up

Start by...

\`\`\`bash
command here
\`\`\`

## Step 2: Configure

Now configure...

## Step 3: Deploy

Finally, deploy...
```

### Comparison Table
```markdown
| Feature | Option A | Option B |
|---------|----------|----------|
| Price   | $10      | $20      |
| Speed   | Fast     | Faster   |
| Feature | Basic    | Advanced |
```

### Callout Box
```markdown
> **Pro Tip:** Use this technique to save time
```

### Code Explanation
```markdown
Here's the important part:

\`\`\`javascript
const result = array.filter(item => item.active)
\`\`\`

This filters only active items.
```

## Testing Your Markdown

1. Write in your editor
2. Preview in the blog editor UI
3. Publish to Firebase
4. Verify on live blog site

If something doesn't render correctly:
- Check for typos in syntax
- Ensure code blocks have language specified
- Verify links are full URLs (with https://)
- Check table alignment (use pipes and dashes)

---

For more markdown features, see [CommonMark Spec](https://spec.commonmark.org/).
