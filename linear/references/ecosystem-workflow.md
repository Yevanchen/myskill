# Ecosystem Team Workflow with Linear

Guide for automating Ecosystem team tasks using Linear API.

## Team Setup

**Ecosystem Team ID:** `a3ea541a-ea53-4f16-aed7-4fcd417a05a9`

### Projects in Ecosystem

1. **MAGA** - `23a0a3f3-fd89-45bc-acec-19c61c19d0bd`
2. **Trigger Phase II** - `aed19245-47f0-46d2-83e3-2c7d695f1a7f`
3. **Developer Platform Phase I** - `6738cc88-bc75-4709-ae0f-d69c8857f3ce`
4. **Memory Orchestration** - `6eb907de-7556-4551-acfe-c2d5113c6faf`
5. And 10+ others...

## Workflow Examples

### 1. Automated Issue Creation from Events

**Trigger:** New GitHub commit, blog post, or feature

```python
from linear_client import LinearClient

client = LinearClient()

# Create issue
issue = client.create_issue(
    team_id="a3ea541a-ea53-4f16-aed7-4fcd417a05a9",
    project_id="23a0a3f3-fd89-45bc-acec-19c61c19d0bd",
    title="[MAGA] New Feature: Bird Integration",
    description="Implement X/Twitter CLI integration for Clawdbot"
)

print(f"Created: {issue['data']['issueCreate']['issue']['identifier']}")
```

### 2. Status Updates from Script Completion

**Pattern:** When automation task completes, update Linear issue

```python
# After script runs successfully
client.update_issue(
    issue_id="ECO-301",
    state_id="DONE_STATE_ID",  # Get from Linear UI
    comment="✅ Skill sync completed successfully"
)
```

### 3. Track Clawdbot Work

**All Clawdbot activities logged to Linear:**

```python
# When creating new skill
client.create_issue(
    team_id="ECOSYSTEM_TEAM_ID",
    project_id="MAGA_PROJECT_ID",
    title="[Skill] Linear Integration - Create Issues",
    description="Add Linear API support to Clawdbot"
)

# When skill is complete
client.update_issue(
    issue_id="ECO-XXX",
    state_id="DONE",
    assignee_id="YOUR_USER_ID"
)
```

## Common Patterns

### Pattern 1: Create Issue with Link

```python
# Create issue with reference
issue = client.create_issue(
    team_id=team_id,
    project_id=project_id,
    title="[GitHub] PR #123 Review",
    description=f"""
Review PR: https://github.com/Yevanchen/myskill/pull/123

Related to: Bird integration
Status: Pending review
    """
)
```

### Pattern 2: Query Recent Issues

```python
# Get last 10 issues in MAGA project
issues = client.query("""
query {
  team(id: "ECOSYSTEM_TEAM_ID") {
    projects {
      nodes {
        id
        name
        issues(first: 10, orderBy: CREATED_AT) {
          nodes {
            id
            identifier
            title
            state { name }
            createdAt
          }
        }
      }
    }
  }
}
""")
```

### Pattern 3: Bulk Updates

```python
# Mark multiple issues as done
for issue_id in ["ECO-300", "ECO-301", "ECO-302"]:
    client.update_issue(
        issue_id,
        state_id="DONE_STATE"
    )
```

## Integration Points

### With Clawdbot

When Clawdbot completes a task:
1. Log action to Linear
2. Update issue status
3. Add comment with results
4. Link to GitHub commit/PR

### With GitHub

When GitHub activity detected:
1. Create Linear issue
2. Reference in PR description
3. Update on merge

### With Discord

When project milestone reached:
1. Create summary issue
2. Post link to Discord
3. Assign to team

## Workflow States

Linear tracks issues through states. Common ones:

- **Backlog** - Unstarted work
- **Todo** - Planned work
- **In Progress** - Currently working
- **In Review** - Awaiting approval
- **Done** - Completed
- **Cancelled** - Discarded

Get state IDs from:
```graphql
query {
  workflowStates {
    nodes {
      id
      name
      type  # backlog, unstarted, started, completed, cancelled
    }
  }
}
```

## Tips

- **Use identifiers:** Reference issues by `ECO-301` instead of UUID
- **Batch operations:** Group multiple mutations together
- **Cache data:** Don't query same data repeatedly
- **Set assignees:** Always assign issues to someone
- **Use projects:** Organize by project, not just team
- **Add descriptions:** Include context for future reference

## Errors & Debugging

### Rate Limited
```
Error: Rate limit exceeded (60 requests/min)
```
→ Wait and retry, or batch queries

### Permission Denied
```
Error: Insufficient permissions
```
→ Check team access, verify API key

### Invalid ID
```
Error: Not a valid UUID
```
→ Use correct project/team ID format
