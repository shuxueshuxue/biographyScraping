"""
Test structured format scraping with all URLs
"""

from citation_fetcher import CitationFetcher
from deep_scraper import DeepScraper


person_name = "Steve Jobs"

print("Fetching citations...")
fetcher = CitationFetcher()
citation_data = fetcher.fetch_citations(person_name)

print(f"\nFound {citation_data['total_citations']} citations")
print("\nScraping ALL URLs with structured format...")

scraper = DeepScraper()
result = scraper.scrape_with_structured_format(
    urls=citation_data['citation_urls'],
    person_name=person_name
)

print(f"\nDone! Check: {result['output_dir']}")
