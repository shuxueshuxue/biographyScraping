"""
Stage 2: Parse experiences and generate embeddings

Usage:
    python stage2_embed.py "Person Name"

Input:
    data/celebrities/{person}/experiences.txt

Output:
    data/vector_db/{person}.json
"""

import sys
import json
from pathlib import Path
from embedding_tool import EmbeddingTool


def main():
    if len(sys.argv) < 2:
        print("Usage: python stage2_embed.py \"Person Name\"")
        print("\nExample: python stage2_embed.py \"Steve Jobs\"")
        sys.exit(1)

    person_name = sys.argv[1]
    safe_name = person_name.lower().replace(" ", "_").replace(".", "")

    print(f"\n{'='*80}")
    print(f"[STAGE 2] Generating embeddings")
    print(f"Person: {person_name}")
    print(f"{'='*80}\n")

    # Check if experiences file exists
    exp_file = Path(f"data/celebrities/{safe_name}/experiences.txt")
    if not exp_file.exists():
        print(f"✗ Error: {exp_file} not found")
        print(f"\nPlease run Stage 1 first:")
        print(f"  python stage1_scrape.py \"{person_name}\"")
        sys.exit(1)

    # Step 1: Parse experiences
    print(f"[1/3] Parsing experiences from {exp_file}...")
    embedder = EmbeddingTool()
    experiences = embedder.parse_experiences_file(str(exp_file))
    print(f"      ✓ Parsed {len(experiences)} experiences\n")

    if not experiences:
        print("✗ Error: No experiences found in file")
        sys.exit(1)

    # Step 2: Generate embeddings
    print(f"[2/3] Generating embeddings for {len(experiences)} experiences...")
    print("      (Calling OpenAI embedding API...)\n")

    texts = [exp['text'] for exp in experiences]
    embeddings = embedder.embed(texts)

    # Attach embeddings to experiences
    for exp, emb in zip(experiences, embeddings):
        exp['embedding'] = emb

    print(f"      ✓ Generated {len(embeddings)} embeddings (1536 dimensions each)\n")

    # Step 3: Save to vector database
    print(f"[3/3] Saving to vector database...")

    output = {
        "person": person_name,
        "experiences": experiences
    }

    db_dir = Path("data/vector_db")
    db_dir.mkdir(parents=True, exist_ok=True)

    output_file = db_dir / f"{safe_name}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)

    print(f"      ✓ Saved to {output_file}\n")

    # Summary
    print(f"{'='*80}")
    print("[STAGE 2 COMPLETE]")
    print(f"{'='*80}")
    print(f"✓ Person: {person_name}")
    print(f"✓ Experiences embedded: {len(experiences)}")
    print(f"✓ Database file: data/vector_db/{safe_name}.json")
    print(f"\nNext: Query the database with Stage 3")
    print(f"      python stage3_query.py \"your experience here\"")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()
