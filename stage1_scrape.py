"""
Stage 1: Scrape biographical experiences from URLs

Usage:
    python stage1_scrape.py "Person Name"

Output:
    data/celebrities/{person}/experiences.txt
    data/celebrities/{person}/scraping_summary.txt
"""

import sys
from citation_fetcher import CitationFetcher
from deep_scraper import DeepScraper


def main():
    if len(sys.argv) < 2:
        print("Usage: python stage1_scrape.py \"Person Name\"")
        print("\nExample: python stage1_scrape.py \"Steve Jobs\"")
        sys.exit(1)

    person_name = sys.argv[1]

    print(f"\n{'='*80}")
    print(f"[STAGE 1] Scraping biographical experiences")
    print(f"Person: {person_name}")
    print(f"{'='*80}\n")

    # Step 1: Get citations from Perplexity
    print("[1/2] Fetching citations from Perplexity...")
    fetcher = CitationFetcher()
    citations = fetcher.fetch_citations(person_name)
    print(f"      ✓ Found {citations['total_citations']} citation URLs\n")

    # Step 2: Scrape and extract experiences
    print(f"[2/2] Scraping {citations['total_citations']} URLs with Claude Code...")
    print("      (This may take several minutes...)\n")

    scraper = DeepScraper()
    result = scraper.scrape_with_structured_format(
        urls=citations['citation_urls'],
        person_name=person_name
    )

    # Summary
    print(f"\n{'='*80}")
    print("[STAGE 1 COMPLETE]")
    print(f"{'='*80}")
    print(f"✓ Person: {person_name}")
    print(f"✓ Output directory: {result['output_dir']}")
    print(f"✓ Files created:")
    print(f"  - experiences.txt (structured experiences)")
    print(f"  - scraping_summary.txt (scraping report)")
    print(f"\nNext: Run Stage 2 to generate embeddings")
    print(f"      python stage2_embed.py \"{person_name}\"")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()
