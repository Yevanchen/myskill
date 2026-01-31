---
name: sequence-indexed-qa
description: Sequence-Indexed QA memory system for LLM context persistence. Create, manage, and retrieve conversation history using sparse semantic hashing and topic indexing. Store all questions (Q) as semantic anchors and selectively store significant answers (A) to build persistent context without dense embeddings. Use when building memory systems that preserve conversation trajectory, need efficient semantic lookup, or require persistent storage of QA pairs across sessions.
---

# Sequence-Indexed QA Memory System

A lightweight, efficient memory architecture for LLM agents that preserves conversation trajectory using sparse semantic indexing. Designed for self-hosted systems with limited resources.

## Quick Start

### 1. Initialize Index

The system stores all data in a single `qa-index.json` file:

```bash
python3 memory-log.py \
  --session discord-常規-20260130 \
  --user Evanchen \
  --q "What is this memory system?" \
  --a "A QA-indexed memory that stores questions and significant answers..." \
  --topics memory_design
```

### 2. Retrieve Recent Context

Load the last 5 QA pairs from a session (inject into prompt):

```bash
python3 memory-load.py recent \
  --session discord-常規-20260130 \
  --window 5
```

### 3. Query by Topic

Find all QA pairs related to a specific topic:

```bash
python3 memory-load.py topic memory_design
```

### 4. Search Globally

Find relevant QA pairs by query text:

```bash
python3 memory-load.py query "how does this work" --limit 5
```

## Core Design

### Why Sequence-Indexed?

**Principle:** The order of questions matters. A sequence of 5 questions in conversation provides more context than 5 random QA pairs.

```
Good:  [Q1] [A1] [Q2] [A2] [Q3] [A3]  ← Coherent trajectory
Bad:   [Q5] [A3] [Q1] [A2] [Q2]       ← Random samples
```

### Storage Strategy

- **All Q's stored** (10-50 tokens each) — Questions are semantic anchors; generating them consumes tokens anyway
- **A's selectively stored** (significance > 0.6) — Only keep answers that matter
- **Compression ratio** typically 0.7-0.85 (70-85% of Q tokens, 40-60% of A tokens)

### Indexing

Three fast indices for retrieval:

| Index | Lookup | Use Case |
|-------|--------|----------|
| **by_topic** | O(1) hash | "Show me memory-related QA" |
| **by_recency** | O(1) slice | "Get last 5 pairs" |
| **by_semantic_hash** | O(1) match | "Did we discuss this before?" |

All indices are simple JSON structures, no external dependencies.

## File Format

### qa-index.json Structure

```json
{
  "version": 1,
  "structure": "sequence-indexed-qa",
  
  "sessions": [
    {
      "session_id": "discord-常規-20260130",
      "channel_id": "optional_channel_id",
      "created": "2026-01-30T18:16:00Z",
      "last_updated": "2026-01-30T18:28:00Z",
      
      "qa_sequence": [
        {
          "seq": 1,
          "timestamp": "2026-01-30T18:16:00Z",
          "user": "Evanchen",
          "q": "Question text",
          "q_tokens": ["question", "text", "keywords"],
          "q_hash": "8f14e45fceea167a5a36dedd4bea2543",
          "a": "Answer text or null",
          "a_significance": 0.85,
          "a_tokens": 42,
          "topic_tags": ["memory_design", "architecture"]
        }
      ]
    }
  ],
  
  "index": {
    "by_topic": {
      "memory_design": [{"session": "...", "seq": 1}]
    },
    "by_recency": [
      {"session": "...", "seq": 1, "timestamp": "..."}
    ],
    "by_semantic_hash": {
      "8f14e45fceea167a5a36dedd4bea2543": {"session": "...", "seq": 1}
    }
  },
  
  "metadata": {
    "total_qa_pairs": 10,
    "stored_answers": 7,
    "compression_ratio": 0.82
  }
}
```

## Tools

### memory-log.py — Add QA Pairs

```bash
python3 memory-log.py \
  --session SESSION_ID \
  --user USERNAME \
  --q "Your question" \
  --a "Your answer" \
  --topics topic1 topic2 \
  --significance 0.85
```

**Options:**
- `--session`: Session ID (required)
- `--user`: Username (optional, default: "unknown")
- `--q`: Question text (required)
- `--a`: Answer text (optional, can be null)
- `--topics`: Space-separated topic tags (optional)
- `--significance`: Override auto-score (0-1, optional)

**Auto-Significance Scoring:**

Answers score based on:
- Length: 0-0.3 (longer = more valuable)
- Complexity: 0-0.2 (more keywords = complex)
- Technical content: 0-0.25 (code, API, design)
- Important keywords: 0-0.15 (security, critical)
- Actionable: 0-0.1 (how-to, steps)

### memory-load.py — Retrieve Context

```bash
# Get recent context (for prompt injection)
python3 memory-load.py recent --session ID --window 5

# Query by topic
python3 memory-load.py topic TOPIC_NAME

# Search by relevance
python3 memory-load.py query "search text" --limit 5 --min-sig 0.6

# Show stats
python3 memory-load.py stats
```

### memory-cli.sh — Shell Interface

Quick lookups without Python:

```bash
# List all topics
./memory-cli.sh list-topics

# Get last N pairs
./memory-cli.sh query-recent 5

# Find topic
./memory-cli.sh query-topic memory_design

# Update significance
./memory-cli.sh set-significance 2 0.95

# Statistics
./memory-cli.sh stats
```

## Integration Patterns

### Pattern 1: Auto-Log During Conversation

After each agent response, log the QA pair:

```python
# In your agent loop
response = agent.generate(user_input)

memory_log.add_qa(
  session_id="current_session",
  user="username",
  q=user_input,
  a=response,
  topic_tags=extract_topics(response)
)
```

### Pattern 2: Inject Context on Wake-Up

When an agent restarts:

```python
context = memory_load.get_recent_context(
  session_id=session,
  window=5
)

prompt = f"""
{system_prompt}

Recent conversation context:
{context}

User: {new_message}
"""
```

### Pattern 3: Cross-Session Learning

Find related QA from other sessions:

```python
relevant = memory_load.find_relevant_pairs(
  query=current_message,
  limit=3,
  min_significance=0.7
)

# Inject most relevant pairs regardless of session
```

## Performance

| Operation | Time | Space |
|-----------|------|-------|
| Add QA | O(1) | ~100 bytes per pair |
| Query by topic | O(1) | N/A |
| Query by hash | O(1) | N/A |
| Recent context | O(1) | N/A |
| Search by relevance | O(n) | n = total pairs |
| Index rebuild | O(n) | One-time |

**Disk Usage:**
- 100 QA pairs: ~10KB
- 1000 QA pairs: ~100KB
- 10000 QA pairs: ~1MB

No external dependencies. Works entirely with JSON and Python stdlib.

## Customization

### Adjust Significance Threshold

Questions stored: always (0.0)
Answers stored: if significance > threshold (default: 0.6)

Modify in `memory-log.py`:

```python
SIGNIFICANCE_THRESHOLD = 0.6
```

### Change Topic Tagging

Auto-tag based on answer content by modifying extraction logic:

```python
def extract_topics(text):
  # Your custom topic extraction here
  return ["topic1", "topic2"]
```

### Prune Old Sessions

Archive sessions >30 days:

```bash
find memory/sessions -mtime +30 -exec mv {} memory/archive/ \;
```

## References

See `references/` directory for:
- **DESIGN.md** — Full architecture rationale and trade-offs
- **QUICKSTART.md** — Step-by-step usage guide
- **EXAMPLES.md** — Real conversation examples
