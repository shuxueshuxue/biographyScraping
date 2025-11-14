"""
Integration test for the complete workflow:
1. Fetch citations from Perplexity
2. Deep scrape the URLs with Claude
"""

from citation_fetcher import CitationFetcher
from deep_scraper import DeepScraper
import os


def test_complete_workflow(person_name: str, max_urls: int = 3):
    """
    Test the complete workflow for a famous person

    Args:
        person_name: Name of the person to research
        max_urls: Maximum number of URLs to scrape (to control costs)
    """
    print("=" * 80)
    print(f"BIOGRAPHY SCRAPING WORKFLOW TEST")
    print(f"Person: {person_name}")
    print("=" * 80)

    # Step 1: Fetch citations from Perplexity
    print("\n[STEP 1] Fetching citations from Perplexity...")
    print("-" * 80)

    fetcher = CitationFetcher()
    citation_data = fetcher.fetch_citations(person_name)

    print(f"✓ Received {citation_data['total_citations']} citations")
    print(f"\nBiography preview:")
    print(citation_data['biography'][:300] + "...\n")

    # Show all URLs
    print("Citation URLs:")
    for i, citation in enumerate(citation_data['citations_with_titles'], 1):
        print(f"  {i}. {citation['title']}")
        print(f"     {citation['url']}")

    # Step 2: Deep scrape with Claude Code
    print(f"\n[STEP 2] Deep scraping top {max_urls} URLs with Claude Code...")
    print("-" * 80)

    scraper = DeepScraper()

    # Limit URLs to avoid excessive API costs during testing
    urls_to_scrape = citation_data['citation_urls'][:max_urls]

    summary = scraper.scrape_multiple_urls(
        urls=urls_to_scrape,
        person_name=person_name
    )

    # Final summary
    print("\n" + "=" * 80)
    print("WORKFLOW COMPLETE")
    print("=" * 80)
    print(f"Person: {person_name}")
    print(f"Citations fetched: {citation_data['total_citations']}")
    print(f"URLs scraped: {summary['successful_scrapes']}/{len(urls_to_scrape)}")
    print(f"Output directory: data/celebrities/{person_name.lower().replace(' ', '_')}")
    print("=" * 80)


if __name__ == "__main__":
    # Test with a famous person known for overcoming adversity
    test_complete_workflow("Oprah Winfrey", max_urls=1)
