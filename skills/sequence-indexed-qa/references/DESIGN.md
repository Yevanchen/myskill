# Design Rationale - Sequence-Indexed QA System

## Problem Statement

LLM agents need persistent memory across sessions. Traditional approaches:

1. **Dense embeddings** (e.g., FAISS, Pinecone) - Fast but expensive
   - Requires embedding model (cost + compute)
   - Stores every Q-A in high-dimensional space
   - Not interpretable (what does index [483] mean?)
   
2. **Full conversation history** - Simple but inefficient
   - Every restart reloads entire history
   - Scales poorly with time (token budget)
   - No semantic organization

3. **Manual curation** - Effective but not scalable
   - Humans pick important Q-A pairs
   - Subjective and time-consuming

## Solution: Sequence-Indexed QA

**Core insight:** For LLMs, conversation trajectory matters more than individual Q-A pairs.

### Design Decisions

#### 1. Store All Q's, Selective A's

**Why?**
- Questions are semantic anchors (what the LLM needs to understand context)
- Generating a question consumes tokens anyway — keep it for future reference
- Answers are large (100-500 tokens) — only store if significant
- Result: 70-85% compression vs full history

**Trade-off:**
- More storage per question (but still minimal)
- Faster retrieval (questions are small, fast to parse)
- Interpretable indexing (hash of question is meaningful)

#### 2. Sparse Indexing (Hash + Keywords)

**Why not embeddings?**
- Dense embeddings require external model (OpenAI API, local transformer)
- Slow for large indices (n dimensional lookups)
- Brittle — small embedding model changes break existing indices
- Overkill for simple token-matching tasks

**Hash + Keyword approach:**
- MD5 hash for exact matches (O(1) lookup)
- Keyword tokens for semantic search (O(n) but n = small)
- No external dependencies
- Survives model updates

**Performance:**
- Add Q-A: O(1) append + index
- Query by topic: O(1) hash
- Query by semantic: O(n) linear scan, but n << total stored

#### 3. Sequence Preservation

**Why?**
- 5 sequential questions create context that random Q-A pairs don't
- Conversation flow matters (Q2 builds on A1, Q3 assumes Q1)
- LLMs predict next token based on sequence, not bag-of-words

**Example:**
```
Sequential: 
  Q1: "How does memory work?"
  A1: "It stores Q-A pairs..."
  Q2: "What about updating significance?"
  → Understands Q2 in context of A1

Random:
  Q2: "What about updating significance?"
  Q1: "How does memory work?"
  → Needs to infer relationship
```

#### 4. Significance Scoring

**Motivation:**
- Not all answers deserve storage
- Avoid noise (Q: "hi" → A: "hi", significance: 0.0)
- Still need human override (some answers matter despite low score)

**Scoring factors:**
- Length: Longer answers carry more information
- Complexity: More keywords = more conceptual depth
- Technical: Code, architecture, design = higher value
- Important: Security, critical, must-have = higher value
- Actionable: How-to, steps, follow = higher value

**Threshold:** Default 0.6 (can be adjusted)

#### 5. Single JSON File

**Why not database?**
- Self-hosted systems prefer files (no DB setup)
- Easy version control (git track changes)
- Portable (copy file = migrate)
- Transparent (inspect, grep, audit)

**Scaling:** Single JSON works for:
- <10,000 Q-A pairs: ~100KB
- <100,000 Q-A pairs: ~1MB
- >100,000: Consider splitting sessions or archiving

## Comparison with Alternatives

### vs. Vector Database (Pinecone, Weaviate)

| Feature | Seq-Indexed QA | Vector DB |
|---------|-----------------|-----------|
| Setup | None | API key required |
| Cost | Free | $20-200/month |
| Latency | O(1) hash | O(log n) tree |
| Accuracy | Keyword-based | Semantic similarity |
| Portability | 100% (file) | 0% (API lock-in) |
| Interpretability | High (hash)| Low (embeddings) |

**Best for:** Self-hosted, low-cost, portable
**Vector DB better for:** Semantic search, very large scale (1M+)

### vs. Full History

| Feature | Seq-Indexed | Full History |
|---------|-------------|--------------|
| Storage | 70-85% compression | 100% |
| Retrieval | O(1) recent, O(n) search | O(1) slice |
| Context quality | Trajectory preserved | Trajectory preserved |
| Startup time | Fast (load index) | Fast (slice) |
| Scalability | Excellent | Poor (token budget) |

**Best for:** Long-running agents
**Full history better for:** Short conversations, simple use

### vs. Manual Curation

| Feature | Seq-Indexed | Manual |
|---------|-------------|--------|
| Consistency | High (scoring) | Variable (human) |
| Effort | Automatic | High (human) |
| Accuracy | Good (heuristics) | Excellent (expert) |
| Scalability | ∞ (no human) | ∼100 (human limited) |

**Best for:** Automated, scalable systems
**Manual better for:** High-precision, domain-specific curation

## Trade-offs

### What We Gained

1. ✅ Lightweight (no external deps)
2. ✅ Fast (O(1) operations)
3. ✅ Portable (single file)
4. ✅ Transparent (inspect JSON)
5. ✅ Scalable (works for 10K+ pairs)

### What We Lost

1. ❌ Semantic similarity (keyword matching only)
2. ❌ Clustering (no automatic grouping)
3. ❌ Recommendations (no ML-based suggestions)
4. ❌ Full-text search (keywords only)

## Extensions

### Future Enhancements

1. **Sliding window compression** — Merge old Q-A pairs into summaries
2. **Automatic clustering** — Group topics by semantic tokens
3. **Importance decay** — Lower significance for very old Q-A
4. **Multi-index sharding** — Split large indices across files
5. **Search ranking** — TF-IDF for better keyword matching
6. **Metadata tagging** — Custom fields per Q-A pair

### When to Migrate

Consider moving to embeddings if:
- >100,000 Q-A pairs stored
- Semantic search accuracy critical (not keyword matching)
- Need real-time similarity rankings
- Have compute budget for embedding model

## References

- **Architecture:** Sparse indexing inspired by Lucene, ElasticSearch
- **Significance scoring:** Similar to TF-IDF, document importance heuristics
- **Sequence preservation:** Based on LLM context window behavior
