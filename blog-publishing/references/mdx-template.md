# MDX Template & Examples

Complete MDX article template with common patterns.

## Full Template

```mdx
---
title: "How to Build a React Dashboard"
date: "2026-01-29T14:30:00Z"
draft: false
summary: "Learn step-by-step how to build a real-time dashboard with React, TypeScript, and Firebase"
tags: ["react", "firebase", "dashboard", "tutorial"]
authors: ["evanchen"]
---

# How to Build a React Dashboard

## Introduction

This guide walks through building a production-ready dashboard. We'll cover:
- Data fetching with React hooks
- Real-time updates with Firebase
- Responsive design with Tailwind CSS
- Error handling and loading states

## Prerequisites

- React 18+
- TypeScript knowledge
- Firebase account

## Step 1: Set Up the Project

\`\`\`bash
npx create-react-app dashboard --template typescript
cd dashboard
npm install firebase tailwindcss
\`\`\`

## Step 2: Configure Firebase

Create a Firebase config file:

\`\`\`typescript
// lib/firebase.ts
import { initializeApp } from 'firebase/app'
import { getFirestore } from 'firebase/firestore'

const firebaseConfig = {
  apiKey: process.env.REACT_APP_FIREBASE_API_KEY,
  projectId: process.env.REACT_APP_FIREBASE_PROJECT_ID,
  // ... other config
}

export const app = initializeApp(firebaseConfig)
export const db = getFirestore(app)
\`\`\`

**Important:** Never hardcode API keys. Use environment variables!

## Step 3: Create a Data Hook

\`\`\`typescript
// hooks/useData.ts
import { useEffect, useState } from 'react'
import { collection, onSnapshot } from 'firebase/firestore'
import { db } from '@/lib/firebase'

export function useData(collectionName: string) {
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<Error | null>(null)

  useEffect(() => {
    const unsubscribe = onSnapshot(
      collection(db, collectionName),
      (snapshot) => {
        const items = snapshot.docs.map(doc => ({
          id: doc.id,
          ...doc.data()
        }))
        setData(items)
        setLoading(false)
      },
      (err) => {
        setError(err)
        setLoading(false)
      }
    )

    return () => unsubscribe()
  }, [collectionName])

  return { data, loading, error }
}
\`\`\`

## Step 4: Build the Dashboard Component

\`\`\`typescript
// components/Dashboard.tsx
import { useData } from '@/hooks/useData'

export function Dashboard() {
  const { data, loading, error } = useData('metrics')

  if (loading) return <div>Loading...</div>
  if (error) return <div>Error: {error.message}</div>

  return (
    <div className="grid grid-cols-4 gap-4">
      {data.map(item => (
        <div key={item.id} className="bg-white p-4 rounded shadow">
          <h3 className="font-bold">{item.name}</h3>
          <p className="text-2xl text-blue-600">{item.value}</p>
        </div>
      ))}
    </div>
  )
}
\`\`\`

## Common Patterns

### Pattern: Responsive Tables

\`\`\`typescript
<table className="w-full border-collapse">
  <thead>
    <tr className="bg-gray-100">
      <th className="text-left p-2">Name</th>
      <th className="text-right p-2">Value</th>
    </tr>
  </thead>
  <tbody>
    {data.map(item => (
      <tr key={item.id} className="border-b hover:bg-gray-50">
        <td className="p-2">{item.name}</td>
        <td className="text-right p-2">{item.value}</td>
      </tr>
    ))}
  </tbody>
</table>
\`\`\`

### Pattern: Loading Skeleton

\`\`\`typescript
function Skeleton({ count = 3 }) {
  return (
    <div className="space-y-4">
      {Array(count).fill(0).map((_, i) => (
        <div key={i} className="bg-gray-200 animate-pulse h-12 rounded" />
      ))}
    </div>
  )
}
\`\`\`

### Pattern: Error Boundary

\`\`\`typescript
class ErrorBoundary extends React.Component {
  state = { hasError: false }

  static getDerivedStateFromError() {
    return { hasError: true }
  }

  render() {
    if (this.state.hasError) {
      return <div className="text-red-600">Something went wrong</div>
    }
    return this.props.children
  }
}
\`\`\`

## Best Practices

✅ **Do:**
- Use environment variables for sensitive config
- Implement proper error handling
- Add loading states for better UX
- Unsubscribe from Firestore listeners
- Use TypeScript for type safety

❌ **Don't:**
- Hardcode API keys in source code
- Ignore Firebase rule errors
- Leave listeners unsubscribed (memory leaks)
- Fetch all data upfront for large datasets

## Deployment

### To Vercel

\`\`\`bash
vercel env add REACT_APP_FIREBASE_API_KEY
vercel deploy
\`\`\`

### To Docker

\`\`\`dockerfile
FROM node:18-alpine
WORKDIR /app
COPY . .
RUN npm install && npm run build
EXPOSE 3000
CMD ["npm", "start"]
\`\`\`

## Next Steps

- Add authentication with Firebase Auth
- Implement real-time notifications
- Set up analytics
- Add dark mode support

## Resources

- [Firebase Documentation](https://firebase.google.com/docs)
- [React Docs](https://react.dev)
- [Tailwind CSS](https://tailwindcss.com)
```

---

## Short-Form Blog Example

```mdx
---
title: "Today's Learnings"
date: "2026-01-29T18:00:00Z"
summary: "Quick notes from my day"
tags: ["daily", "notes"]
---

## What I Learned Today

- React's `useCallback` prevents unnecessary re-renders
- Firebase's Firestore supports offline persistence
- Good sleep improves coding productivity

## Action Items

- [ ] Review PR feedback
- [ ] Update documentation
- [ ] Deploy to production
```

---

## Key Takeaways

1. **Always use environment variables** for API keys
2. **Include frontmatter** at the top (between `---` markers)
3. **Use descriptive titles** for better SEO and slug generation
4. **Add summaries** for blog list preview
5. **Tag your posts** for organization and discoverability
