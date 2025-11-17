"""
Stage 3: Find matching experiences for user query

Usage:
    python stage3_query.py "user experience text"
    python stage3_query.py "user experience text" --top 10

Input:
    data/vector_db/*.json

Output:
    Top matching experiences from famous people
"""

import sys
from embedding_tool import EmbeddingTool


def main():
    if len(sys.argv) < 2:
        print("Usage: python stage3_query.py \"user experience text\" [--top N]")
        print("\nExamples:")
        print("  python stage3_query.py \"I was fired from my own company\"")
        print("  python stage3_query.py \"I failed my startup\" --top 10")
        sys.exit(1)

    # Parse arguments
    args = sys.argv[1:]
    top_k = 5

    if '--top' in args:
        top_idx = args.index('--top')
        if top_idx + 1 < len(args):
            top_k = int(args[top_idx + 1])
            args = args[:top_idx]  # Remove --top and number

    query = " ".join(args)

    print(f"\n{'='*80}")
    print(f"[STAGE 3] Finding matching experiences")
    print(f"{'='*80}")
    print(f"Query: \"{query}\"")
    print(f"Top-K: {top_k}")
    print(f"{'='*80}\n")

    # Search database
    print("Searching vector database...")
    embedder = EmbeddingTool()
    matches = embedder.match_across_database(query, top_k=top_k)

    if not matches:
        print("✗ No matches found. Is the database empty?")
        print("\nMake sure you've run Stage 1 and Stage 2 for at least one person.")
        sys.exit(1)

    print(f"✓ Found {len(matches)} matches\n")

    # Display results
    print(f"{'='*80}")
    print(f"TOP {len(matches)} MATCHING EXPERIENCES")
    print(f"{'='*80}\n")

    for i, match in enumerate(matches, 1):
        print(f"{i}. {match['person']}")
        print(f"   Similarity: {match['similarity']:.4f}")
        print(f"   Keywords: {', '.join(match['keywords'])}")
        if 'source_url' in match:
            print(f"   Source: {match['source_url']}")
        print(f"\n   {match['text'][:300]}...")
        print(f"\n{'-'*80}\n")

    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()
