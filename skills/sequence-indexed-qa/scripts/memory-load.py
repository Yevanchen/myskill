#!/usr/bin/env python3
"""
Memory Loader - Retrieve context from QA index
Usage: python3 memory-load.py --index PATH [commands]
"""

import json
import sys
from pathlib import Path
from typing import List, Dict, Optional
import re

def load_index(index_file: Path) -> Dict:
    """Load the QA index from disk"""
    try:
        with open(index_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Index file not found at {index_file}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {index_file}: {e}", file=sys.stderr)
        sys.exit(1)

def extract_tokens(text: str) -> List[str]:
    """Extract tokens from text"""
    tokens = re.findall(r'\b\w{2,}\b', text.lower())
    return list(set(tokens))[:20]

def find_relevant_pairs(data: Dict, query: str, session_id: Optional[str] = None, 
                       limit: int = 5, min_significance: float = 0.0) -> List[Dict]:
    """Find relevant Q-A pairs for a query"""
    query_tokens = set(extract_tokens(query))
    relevant = []
    
    for session in data['sessions']:
        if session_id and session['session_id'] != session_id:
            continue
        
        for qa in session['qa_sequence']:
            if qa['a'] and qa['a_significance'] < min_significance:
                continue
            
            qa_tokens = set(qa['q_tokens'])
            overlap = len(query_tokens & qa_tokens)
            score = overlap
            if session['session_id'] == session_id:
                score *= 1.5
            
            relevant.append({
                'score': score,
                'session': session['session_id'],
                'seq': qa['seq'],
                'q': qa['q'],
                'a': qa['a'],
                'significance': qa['a_significance'],
                'timestamp': qa['timestamp']
            })
    
    relevant.sort(key=lambda x: (-x['score'], -x['timestamp']))
    return relevant[:limit]

def get_recent_context(data: Dict, session_id: str, window: int = 5) -> List[Dict]:
    """Get recent Q-A pairs from a session (for context injection)"""
    for session in data['sessions']:
        if session['session_id'] != session_id:
            continue
        
        qa_sequence = session['qa_sequence']
        recent = qa_sequence[-window:] if len(qa_sequence) >= window else qa_sequence
        
        return [
            {
                'seq': qa['seq'],
                'q': qa['q'],
                'a': qa['a'],
                'timestamp': qa['timestamp']
            }
            for qa in recent
        ]
    
    return []

def format_context(qa_pairs: List[Dict], include_answers: bool = True) -> str:
    """Format Q-A pairs as readable context"""
    lines = []
    lines.append("=== Recent Context ===\n")
    
    for pair in qa_pairs:
        lines.append(f"[{pair['seq']}] Q: {pair['q']}")
        if include_answers and pair['a']:
            answer = pair['a']
            if len(answer) > 300:
                answer = answer[:300] + "...[truncated]"
            lines.append(f"    A: {answer}\n")
        else:
            lines.append()
    
    return "\n".join(lines)

def print_topic_summary(data: Dict, topic: str) -> None:
    """Print a summary of Q-A pairs for a topic"""
    if topic not in data['index']['by_topic']:
        print(f"Topic '{topic}' not found")
        return
    
    refs = data['index']['by_topic'][topic]
    print(f"\n📌 Topic: {topic}")
    print(f"   References: {len(refs)}\n")
    
    for ref in refs:
        session_id = ref['session']
        seq = ref['seq']
        
        for session in data['sessions']:
            if session['session_id'] != session_id:
                continue
            
            for qa in session['qa_sequence']:
                if qa['seq'] == seq:
                    print(f"[{seq}] Q: {qa['q'][:80]}")
                    if qa['a']:
                        print(f"    Significance: {qa['a_significance']:.2f}")
                    print()
                    break

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Memory Loader - Retrieve context')
    parser.add_argument('--index', type=Path, default=Path('./qa-index.json'),
                       help='Path to qa-index.json (default: ./qa-index.json)')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Query command
    query_parser = subparsers.add_parser('query', help='Search for relevant Q-A pairs')
    query_parser.add_argument('query', help='Search query')
    query_parser.add_argument('--session', help='Filter by session')
    query_parser.add_argument('--limit', type=int, default=5, help='Max results')
    query_parser.add_argument('--min-sig', type=float, default=0.0, help='Min significance')
    
    # Recent command
    recent_parser = subparsers.add_parser('recent', help='Get recent context')
    recent_parser.add_argument('--session', required=True, help='Session ID')
    recent_parser.add_argument('--window', type=int, default=5, help='Window size')
    
    # Topic command
    topic_parser = subparsers.add_parser('topic', help='Show Q-A pairs for a topic')
    topic_parser.add_argument('topic', help='Topic name')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show statistics')
    
    args = parser.parse_args()
    
    data = load_index(args.index)
    
    if args.command == 'query':
        results = find_relevant_pairs(data, args.query, args.session, args.limit, args.min_sig)
        print(f"\n🔍 Found {len(results)} relevant pairs:\n")
        for i, pair in enumerate(results, 1):
            print(f"{i}. [{pair['seq']}] {pair['q'][:80]}")
            if pair['a']:
                print(f"   Significance: {pair['significance']:.2f}")
            print()
    
    elif args.command == 'recent':
        context = get_recent_context(data, args.session, args.window)
        print(format_context(context))
    
    elif args.command == 'topic':
        print_topic_summary(data, args.topic)
    
    elif args.command == 'stats':
        meta = data['metadata']
        print(f"\n📊 Memory Statistics:")
        print(f"   Total Q-A pairs: {meta['total_qa_pairs']}")
        print(f"   Stored answers: {meta['stored_answers']}")
        print(f"   Sessions: {len(data['sessions'])}")
        print(f"   Last updated: {meta['last_updated']}\n")
    
    else:
        parser.print_help()
