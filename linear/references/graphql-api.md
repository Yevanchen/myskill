# Linear GraphQL API Reference

Quick reference for common Linear GraphQL operations.

## Endpoint

```
POST https://api.linear.app/graphql
```

## Authentication Headers

**Personal API Key:**
```
Authorization: lin_api_...
Content-Type: application/json
```

**OAuth 2.0:**
```
Authorization: Bearer <ACCESS_TOKEN>
Content-Type: application/json
```

## Core Objects

### User
```graphql
{
  viewer {
    id          # User UUID
    name        # Display name
    email       # Email address
    avatarUrl   # Profile picture
  }
}
```

### Team
```graphql
{
  team(id: "TEAM_ID") {
    id          # Team UUID
    name        # Team name
    projects {  # Projects in team
      nodes {
        id
        name
      }
    }
    issues {    # All issues
      nodes { ... }
    }
  }
}
```

### Issue
```graphql
{
  issue(id: "ECO-301") {
    id              # UUID or identifier (ECO-301)
    identifier      # Short ID (ECO-301)
    title           # Issue title
    description     # Long description
    state {         # Status (Todo, In Progress, Done, etc.)
      id
      name
    }
    assignee {      # Who it's assigned to
      id
      name
    }
    creator {       # Who created it
      id
      name
    }
    priority        # 0 (No priority) to 4 (Urgent)
    dueDate         # YYYY-MM-DD format
    estimate        # Time estimate in points
    createdAt       # ISO 8601 timestamp
    updatedAt       # ISO 8601 timestamp
    url             # Direct link to issue
  }
}
```

### Project
```graphql
{
  project(id: "PROJECT_ID") {
    id
    name
    description
    icon
    color          # Hex color code
    team {
      id
      name
    }
    issues {
      nodes { ... }
    }
  }
}
```

## Common Queries

### Get Current User
```graphql
query Me {
  viewer {
    id
    name
    email
    assignedIssues {
      nodes {
        id
        identifier
        title
      }
    }
  }
}
```

### Get All Teams
```graphql
query Teams {
  teams {
    nodes {
      id
      name
    }
  }
}
```

### Get Team Issues
```graphql
query TeamIssues($teamId: String!) {
  team(id: $teamId) {
    issues(first: 50) {
      nodes {
        id
        identifier
        title
        state { name }
        assignee { name }
      }
    }
  }
}
```

### Search Issues
```graphql
query SearchIssues($query: String!) {
  issues(filter: {searchableContent: {containsAll: [$query]}}, first: 20) {
    nodes {
      id
      identifier
      title
    }
  }
}
```

### Get Issue by ID
```graphql
query IssueDetail($id: String!) {
  issue(id: $id) {
    id
    identifier
    title
    description
    state { name }
    assignee { name }
    priority
    estimate
    dueDate
  }
}
```

## Common Mutations

### Create Issue
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

**Input:**
```json
{
  "teamId": "TEAM_UUID",
  "projectId": "PROJECT_UUID",
  "title": "Issue title",
  "description": "Optional description",
  "priority": 2,
  "estimate": 5,
  "dueDate": "2026-02-01",
  "assigneeId": "USER_UUID"
}
```

### Update Issue
```graphql
mutation UpdateIssue($id: String!, $input: IssueUpdateInput!) {
  issueUpdate(id: $id, input: $input) {
    issue {
      id
      title
      state { name }
    }
  }
}
```

**Input (all optional):**
```json
{
  "title": "New title",
  "description": "New description",
  "stateId": "STATE_UUID",
  "assigneeId": "USER_UUID",
  "priority": 3,
  "estimate": 8,
  "dueDate": "2026-02-15"
}
```

### Archive Issue
```graphql
mutation ArchiveIssue($id: String!) {
  issueArchive(id: $id) {
    issue {
      id
      archivedAt
    }
  }
}
```

### Add Comment
```graphql
mutation AddComment($input: CommentCreateInput!) {
  commentCreate(input: $input) {
    comment {
      id
      body
      createdAt
    }
  }
}
```

**Input:**
```json
{
  "issueId": "ISSUE_UUID",
  "body": "Comment text"
}
```

### Create Project
```graphql
mutation CreateProject($input: ProjectCreateInput!) {
  projectCreate(input: $input) {
    project {
      id
      name
      url
    }
  }
}
```

**Input:**
```json
{
  "teamId": "TEAM_UUID",
  "name": "Project name",
  "description": "Optional description",
  "icon": "briefcase",
  "color": "#FF0000"
}
```

## Pagination

```graphql
query Issues {
  issues(
    first: 50        # Number of results
    after: "cursor"  # For next page
    orderBy: CREATED_AT
  ) {
    pageInfo {
      hasNextPage
      endCursor
    }
    nodes { ... }
  }
}
```

## Filtering

```graphql
query FilteredIssues {
  issues(filter: {
    state: { name: { eq: "Todo" } }
    assignee: { id: { eq: "USER_ID" } }
    priority: { gte: 2 }
  }) {
    nodes { ... }
  }
}
```

## Workflow States

States represent issue status. Get all:

```graphql
query States {
  workflowStates {
    nodes {
      id
      name
      type        # backlog, unstarted, started, completed, cancelled
      position    # Order in workflow
    }
  }
}
```

## Error Handling

All errors follow GraphQL standard format:

```json
{
  "errors": [
    {
      "message": "Error description",
      "path": ["field", "name"],
      "extensions": {
        "code": "ERROR_CODE",
        "userError": true
      }
    }
  ]
}
```

Common errors:
- `AUTHENTICATION_FAILED` - Bad API key
- `INVALID_INPUT` - Missing required fields
- `NOT_FOUND` - Resource doesn't exist
- `RATE_LIMITED` - Too many requests
- `PERMISSION_DENIED` - Insufficient access

## Rate Limits

- **60 requests per minute** per API key
- Headers will include current usage
- Retry with exponential backoff

## Resources

- **API Docs:** https://linear.app/developers/graphql
- **Schema Playground:** https://studio.apollographql.com/public/Linear-API
- **TypeScript SDK:** https://linear.app/developers/sdk
