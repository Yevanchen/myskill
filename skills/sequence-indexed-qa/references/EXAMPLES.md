# Examples - Sequence-Indexed QA Memory

Real conversation examples from Discord integration with OpenClaw.

## Example 1: Technical Q&A Session

Session: `discord-tech-20260130`

### Conversation Flow

```
[1] Q: "How do I configure Discord message listening?"
    A: "You need to enable message content intent in gateway config. Options: (1) message content intent, (2) prefix commands, (3) passive monitoring"
    Significance: 0.85 (length: high, technical: yes, actionable: yes)
    Topics: [discord_config, messaging]

[2] Q: "Where are the persistent volumes stored?"
    A: "Three volumes: config (/home/node/.clawdbot - 7.2MB), storage (/home/node/clawdctl - 6B), workspace (/home/node/.openclaw/workspace - 99MB)"
    Significance: 0.80 (length: high, technical: yes)
    Topics: [storage, volumes, infrastructure]

[3] Q: "Why does memory reset on restart?"
    A: "Security design. MEMORY.md only loads in private sessions, not shared channels. Prevents leaking personal context in group chats."
    Significance: 0.90 (important: yes, addresses privacy concern)
    Topics: [memory, security, privacy]
```

### Retrieval Examples

**User asks later:** "How's my memory working?"

```
Query: "memory working"
Tokens: [memory, working, how]

Results:
  1. [3] "Why does memory reset on restart?" (sig: 0.90, match: 2 tokens)
  2. [1] "How do I configure..." (sig: 0.85, match: 0 tokens)

Context window for injection:
  [1] Q: "How do I configure Discord..."
  [2] Q: "Where are persistent volumes..."
  [3] Q: "Why does memory reset..."
  [3] A: "Security design..."
```

## Example 2: Memory System Design

Session: `discord-tech-20260130`

### Long Q-A about System Design

```
[6] Q: "I want you to design a memory mechanism. Our conversation is QA sequence. Q is key, A is value. Store only significant A's. Q is meaningful because you're an LLM. Q like your token activation scatter plot. Trajectory matters: 5 Q's and 5 A's. Design sparse index with files on persistent disk."
    A: "Core insight: Sequence-Indexed QA System. [Long design answer covering architecture, indexing, significance scoring]"
    Significance: 0.95 (extremely complex question, technical depth, actionable design)
    Topics: [memory_design, llm_architecture, data_structure, sparse_indexing]
    A_tokens: 350 (long answer, significant)
```

### Cross-Topic Retrieval

**Later, user asks:** "Can you explain sparse indexing to someone new?"

```
Query: "sparse indexing explain"
Tokens: [sparse, indexing, explain]

Results:
  1. [6] Memory system design (sig: 0.95, match: 1 token "sparse")
  2. [other_session:4] Previous indexing discussion (match: 2 tokens)
```

**Inject previous design into context:**
```
[4] Q: "Previous indexing question from another session"
[6] Q: "Design memory mechanism with sparse index..."
[6] A: "[Full design showing sparse indexing approach]"
```

## Example 3: Conversation with No Answers

Session: `discord-casual-20260131`

```
[1] Q: "hi"
    A: null
    Significance: 0.1 (no answer)
    Topics: []

[2] Q: "What's up?"
    A: null
    Significance: 0.0
    Topics: []

[3] Q: "You there?"
    A: "Yes, I'm here. How can I help?"
    Significance: 0.2 (short answer, simple question)
    Topics: [greeting, interaction]
```

**Storage:** Only [3] is stored (significance > 0.6 disabled for greeting). [1] and [2] are still logged but A is null.

**Why:** Greeting exchanges are not valuable to retrieve later; just noise.

## Example 4: Auto-Scoring Demonstration

### High-Scoring Answer

```
User Q: "How should I implement OAuth 2.0 in Python?"

Agent A: "Use authlib library. Installation: pip install authlib. 
Key steps:
1. Create OAuth client with client_id/secret
2. Redirect user to authorization endpoint
3. Handle callback with authorization code
4. Exchange code for access token
5. Use token for API calls

See references/oauth_patterns.py for full example."

Auto-Score Calculation:
  - Length: 180 chars / 500 = 0.36 * 0.3 = 0.11
  - Complexity: 9 keywords / 8 = 1.0 * 0.2 = 0.20
  - Technical: contains "authlib", "OAuth", "API" = 0.25
  - Important: no critical keywords = 0.0
  - Actionable: contains "steps", "implementation" = 0.10
  
  Total: 0.11 + 0.20 + 0.25 + 0.0 + 0.10 = 0.66 ✅ STORED (> 0.6)
```

### Low-Scoring Answer

```
User Q: "What's your favorite color?"

Agent A: "Blue"

Auto-Score:
  - Length: 4 chars = 0.0
  - Complexity: 1 keyword = 0.025
  - Technical: none = 0.0
  - Important: none = 0.0
  - Actionable: none = 0.0
  
  Total: 0.025 ❌ NOT STORED
```

## Example 5: Topic-Based Organization

Index for a multi-purpose Discord bot:

```
by_topic:
  - discord_config: [sess:1:2, sess:1:5, sess:2:3]
  - memory_design: [sess:1:6, sess:3:1]
  - security: [sess:1:3, sess:2:5]
  - storage: [sess:1:2]
  - llm_architecture: [sess:1:6, sess:3:2]
  - oauth: [sess:2:1, sess:2:4]
  - python: [sess:2:1, sess:3:5]
  - greeting: [sess:4:3]
```

**Query:** "Tell me about auth implementation"
- Search topics: matches `oauth` and `security`
- Load pairs: sess:2:1 (OAuth impl), sess:1:3 (security concern)
- Context window: last 5 from current session + these related pairs

## Example 6: API Usage (Python)

```python
from memory_log import add_qa
from memory_load import find_relevant_pairs, get_recent_context
import json

# Initialize (assumes qa-index.json exists)
index_file = Path("qa-index.json")

# After agent response, log Q-A
add_qa(
  index_file=index_file,
  session_id="discord-tech",
  user="evanchen",
  q=user_message,
  a=agent_response,
  topic_tags=["memory", "persistence"],
  # significance auto-calculated
)

# On agent restart, load context
data = json.loads(index_file.read_text())
context = get_recent_context(data, session_id="discord-tech", window=5)

prompt = f"""
[System prompt]

Recent conversation:
{format_context(context)}

User: {new_message}
"""

# Agent generates response with context
response = agent.generate(prompt)
```

## Example 7: Significance Override

```bash
# Auto-score a very technical answer
python3 memory-log.py \
  --index qa-index.json \
  --session tech-20260131 \
  --q "Explain transformer attention mechanism" \
  --a "[500-word technical explanation]" \
  --topics ml, llm, architecture
  # Significance auto-calculated: 0.75

# But user thinks it's more important than auto-score
./memory-cli.sh set-significance 42 0.99

# Or override during logging:
python3 memory-log.py \
  --index qa-index.json \
  --session tech-20260131 \
  --q "Explain transformer attention" \
  --a "[explanation]" \
  --significance 0.99
```

## Example 8: Cross-Session Learning

Session 1: Discord #tech
```
[5] Q: "How do I use Docker for development?"
    A: "[Docker dev setup guide]"
    Topics: [docker, devops]
```

Session 2: Discord #questions (same user)
```
User: "We need containerization for our CI/CD"

Agent loads context:
  1. Recent from #questions (session 2, last 5 pairs)
  2. Relevant pairs from other topics via search:
     - Find "docker" and "devops" → Load sess1:5
  3. Inject combined context:
     "Previous discussion [sess1:5] about Docker. [A5 content]"
```

Result: Agent remembers Docker knowledge from previous session and applies it.
