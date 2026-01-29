---
name: linear
description: Linear project management integration. Create, query, and update issues in Linear using GraphQL API. Supports personal API keys and OAuth 2.0 authentication. Use for task automation, issue tracking, and ecosystem team workflow integration.
---

# Linear

Integrate with Linear's GraphQL API to manage issues, projects, and team workflows in the Ecosystem workspace.

## Quick Start

### Authentication

Set your Linear API key:
```bash
export LINEARAPIKEY="lin_api_..."  # Personal API key from Linear settings
```

Or use OAuth 2.0 token:
```bash
export LINEAR_OAUTH_TOKEN="..."
```

### Common Operations

**Check authentication:**
```bash
curl -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEARAPIKEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ viewer { id name email } }"}'
```

**List teams:**
```bash
curl -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEARAPIKEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ teams { nodes { id name } } }"}'
```

**Get issues for a team:**
```bash
curl -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEARAPIKEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "query { team(id: \"TEAM_ID\") { issues { nodes { id title state { name } } } } }"
  }'
```

## Operations

### 1. Create Issue

**GraphQL Mutation:**
```graphql
mutation CreateIssue($input: IssueCreateInput!) {
  issueCreate(input: $input) {
    issue {
      id
      identifier
      title
      url
    }
  }
}
```

**Variables:**
```json
{
  "input": {
    "teamId": "TEAM_ID",
    "projectId": "PROJECT_ID",
    "title": "Issue Title",
    "description": "Detailed description"
  }
}
```

### 2. Update Issue

**Mutation:**
```graphql
mutation UpdateIssue($id: String!, $input: IssueUpdateInput!) {
  issueUpdate(id: $id, input: $input) {
    issue {
      id
      title
      state { id name }
    }
  }
}
```

**Variables:**
```json
{
  "id": "ECO-301",
  "input": {
    "title": "New Title",
    "stateId": "NEW_STATE_ID",
    "assigneeId": "USER_ID"
  }
}
```

### 3. Query Issues

**Get all issues:**
```graphql
query {
  issues(first: 50) {
    nodes {
      id
      identifier
      title
      state { name }
      assignee { name }
      createdAt
    }
  }
}
```

**Get team issues:**
```graphql
query {
  team(id: "TEAM_ID") {
    issues(first: 50) {
      nodes {
        id
        identifier
        title
      }
    }
  }
}
```

### 4. Search Issues

**By identifier:**
```graphql
query {
  issue(id: "ECO-301") {
    id
    title
    description
    url
  }
}
```

### 5. Add Comments

```graphql
mutation AddComment($input: CommentCreateInput!) {
  commentCreate(input: $input) {
    comment {
      id
      body
    }
  }
}
```

**Variables:**
```json
{
  "input": {
    "issueId": "ISSUE_ID",
    "body": "Comment text"
  }
}
```

## Ecosystem Team

Your API key has access to the **Ecosystem team** workspace:

- **Team ID:** `a3ea541a-ea53-4f16-aed7-4fcd417a05a9`
- **Projects:** MAGA, Trigger, Developer Platform, Memory Orchestration, etc.

All skill-related tasks should be created in this team.

## Authentication Methods

### Method 1: Personal API Key (Recommended for Scripts)

1. Go to Linear Settings → Security & access
2. Create a new API key
3. Set `LINEARAPIKEY` environment variable

**Header:**
```
Authorization: lin_api_...
```

### Method 2: OAuth 2.0 (Recommended for Applications)

1. Create OAuth app in Linear
2. Complete OAuth flow to get access token
3. Use token as Bearer token

**Header:**
```
Authorization: Bearer <ACCESS_TOKEN>
```

## Examples

### Example 1: Create Issue from GitHub Event

```bash
curl -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEARAPIKEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { issueCreate(input: {teamId: \"a3ea541a-ea53-4f16-aed7-4fcd417a05a9\", projectId: \"23a0a3f3-fd89-45bc-acec-19c61c19d0bd\", title: \"$GITHUB_EVENT\", description: \"From GitHub action\"}) { issue { id identifier url } } }"
  }'
```

### Example 2: Update Issue Status

```bash
curl -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEARAPIKEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { issueUpdate(id: \"ECO-301\", input: {stateId: \"done\"}) { issue { id state { name } } } }"
  }'
```

### Example 3: Get Assigned Issues

```bash
curl -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEARAPIKEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "query { user(id: \"USER_ID\") { assignedIssues { nodes { id identifier title } } } }"
  }'
```

## Workflow Integration

Typical workflow:
1. **Create issue** when task is detected (GitHub, blog post, etc.)
2. **Update status** when work begins
3. **Add comments** with progress updates
4. **Link related issues** for cross-team visibility

## Rate Limiting

Linear has rate limits (typically 60 requests per minute).

**Best practices:**
- Batch queries when possible
- Use webhooks for real-time updates instead of polling
- Cache results locally
- Implement exponential backoff for retries

## Common Issues & Solutions

### "Invalid authentication credentials"
- Check API key is correctly set
- Verify key hasn't expired
- Ensure `Authorization` header format is correct

### "Field not found"
- Check team ID and project ID are valid
- Verify you have access to the resource
- Refer to GraphQL schema introspection

### "Rate limited"
- Reduce request frequency
- Implement caching
- Use webhooks instead of polling

## See Also

- **GraphQL API:** https://linear.app/developers/graphql
- **TypeScript SDK:** https://linear.app/developers/sdk
- **Webhooks:** https://linear.app/developers/webhooks
- **Linear Docs:** https://linear.app/developers
