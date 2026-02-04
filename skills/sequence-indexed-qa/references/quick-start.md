# Quick Start - Memory System

Get your memory system running in 5 minutes.

## Step 1: Verify Installation

```bash
# Check if files exist
ls -l /home/node/clawd/memory/
# Should show: qa-index.json, memory-log.py, cron-config.json, etc.

# Test the script
python3 /home/node/clawd/memory/memory-log.py --help
```

## Step 2: Log Your First Q-A Pair

```bash
python3 /home/node/clawd/memory/memory-log.py \
  --session "discord-常规-20260130" \
  --user "Evanchen" \
  --q "What is the memory system?" \
  --a "It's a persistent Q-A storage system that logs conversations, extracts patterns, and maintains searchable history." \
  --topics "memory" "explanation" \
  --significance 0.8
```

**Expected output:**
```
✅ Added Q-A pair #16 to discord-常规-20260130
   Significance: 0.80 | Topics: ['memory', 'explanation']
```

## Step 3: Check Your Index

```bash
# View the index file
python3 << 'EOF'
import json

with open('/home/node/clawd/memory/qa-index.json') as f:
    data = json.load(f)

# Show metadata
meta = data['metadata']
print(f"Total Q-A pairs: {meta['total_qa_pairs']}")
print(f"Stored answers: {meta['stored_answers']}")
print(f"Last updated: {meta['last_updated']}")

# Show last 3 Q-A pairs
session = data['sessions'][0]
print(f"\nLast 3 Q-A pairs in {session['session_id']}:")
for qa in session['qa_sequence'][-3:]:
    print(f"  [{qa['seq']}] {qa['user']}: {qa['q'][:50]}...")
EOF
```

## Step 4: Enable Automatic Extraction

Already done! Check cron status:

```bash
cron list | grep memory-extraction-summarizer
```

**Should show:**
```
memory-extraction-summarizer (enabled, runs every hour at :00)
```

## Step 5: Test Extraction (Optional)

Manually trigger extraction:

```bash
python3 /home/node/clawd/memory/extract-conversations.py \
  --index /home/node/clawd/memory/qa-index.json \
  --output-dir /tmp/test-extraction \
  --hours 1 \
  --session "discord-常规-20260130"

# View results
ls -la /tmp/test-extraction/
cat /tmp/test-extraction/discord-常规-20260130-qa.json
```

---

## Common Tasks

### Add Multiple Q-A Pairs (Batch)

```bash
#!/bin/bash
# batch-log.sh

python3 /home/node/clawd/memory/memory-log.py \
  --session "discord-常规-20260130" --user "Evanchen" \
  --q "Q1" --a "A1" --topics "topic1"

python3 /home/node/clawd/memory/memory-log.py \
  --session "discord-常規-20260130" --user "Evanchen" \
  --q "Q2" --a "A2" --topics "topic2"

python3 /home/node/clawd/memory/memory-log.py \
  --session "discord-常規-20260130" --user "Evanchen" \
  --q "Q3" --a "A3" --topics "topic3"

echo "✅ Batch logging complete"
```

### Query by Topic

```bash
python3 << 'EOF'
import json

with open('/home/node/clawd/memory/qa-index.json') as f:
    data = json.load(f)

topic = "memory"
if topic in data['index']['by_topic']:
    pairs = data['index']['by_topic'][topic]
    print(f"Q-A pairs tagged '{topic}': {len(pairs)}")
    for ref in pairs:
        print(f"  {ref}")
else:
    print(f"No Q-A pairs tagged '{topic}'")
EOF
```

### View High-Significance Answers

```bash
python3 << 'EOF'
import json

with open('/home/node/clawd/memory/qa-index.json') as f:
    data = json.load(f)

session = data['sessions'][0]
high_sig = [qa for qa in session['qa_sequence'] if qa.get('a_significance', 0) > 0.7]

print(f"High-significance Q-A pairs (>0.7): {len(high_sig)}")
for qa in high_sig[-5:]:
    print(f"\n[{qa['seq']}] Sig: {qa['a_significance']:.2f}")
    print(f"Q: {qa['q'][:60]}...")
    print(f"Topics: {qa['topic_tags']}")
EOF
```

---

## Troubleshooting

### Script not found?
```bash
# Make sure you're in the right directory
cd /home/node/clawd/memory
ls -la memory-log.py

# If not found, you may need to set up the memory system first
# Check SKILL.md for setup instructions
```

### Index file corrupted?
```bash
# Backup the old one
cp /home/node/clawd/memory/qa-index.json \
   /home/node/clawd/memory/qa-index.json.backup

# Reset index (WARNING: deletes all data!)
python3 << 'EOF'
import json
from datetime import datetime

# Create fresh index with one session
config = {
    "version": 1,
    "structure": "sequence-indexed-qa",
    "sessions": [
        {
            "session_id": "discord-常规-20260130",
            "channel_name": "常规",
            "channel_id": "1466083818061566090",
            "created": datetime.utcnow().isoformat() + 'Z',
            "last_updated": datetime.utcnow().isoformat() + 'Z',
            "qa_sequence": []
        }
    ],
    "index": {
        "by_topic": {},
        "by_recency": [],
        "by_semantic_hash": {}
    },
    "metadata": {
        "total_qa_pairs": 0,
        "stored_answers": 0,
        "empty_answers_count": 0,
        "last_updated": datetime.utcnow().isoformat() + 'Z'
    }
}

with open('/home/node/clawd/memory/qa-index.json', 'w') as f:
    json.dump(config, f, ensure_ascii=False, indent=2)

print("✅ Index reset. Ready to use.")
EOF
```

---

## Next Steps

✅ **You're ready to:**
- Log Q-A pairs manually
- Let cron automatically extract hourly
- Query your memory anytime
- Build long-term context

📚 **For more details:**
- See `SKILL.md` for full documentation
- See `DESIGN.md` for architecture details
- See `EXAMPLES.md` for usage examples
