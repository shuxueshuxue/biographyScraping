"""
Module 1: Citation Fetcher

Given a famous person's name, fetch their biography from Perplexity
and return the citation URLs for further scraping.
"""

from perplexity_tool import PerplexityTool, PerplexityResponse
from typing import List, Dict
import json


class CitationFetcher:
    """Fetches citation URLs for a given person using Perplexity API"""

    def __init__(self, config_path: str = "models.json"):
        """Initialize with Perplexity tool"""
        self.perplexity = PerplexityTool(config_path)

    def fetch_citations(self, person_name: str) -> Dict[str, any]:
        """
        Fetch biography and citation URLs for a person

        Args:
            person_name: Name of the famous person

        Returns:
            Dictionary containing:
                - name: Person's name
                - biography: Text biography from Perplexity
                - citation_urls: List of source URLs
                - citations_with_titles: List of dicts with url and title
        """
        # Query Perplexity for comprehensive biography
        prompt = (
            f"Provide a comprehensive biography of {person_name}, "
            f"focusing on their life experiences, challenges, struggles, "
            f"failures, and how they overcame adversity. Include details about "
            f"their early life, career setbacks, and turning points."
        )

        response: PerplexityResponse = self.perplexity.query(prompt)

        # Extract citation data
        citations_with_titles = [
            {
                "url": citation.url,
                "title": citation.title
            }
            for citation in response.citations
        ]

        return {
            "name": person_name,
            "biography": response.content,
            "citation_urls": response.get_citation_urls(),
            "citations_with_titles": citations_with_titles,
            "total_citations": len(response.citations)
        }

    def save_citations(self, person_name: str, output_file: str = None) -> Dict[str, any]:
        """
        Fetch citations and save to JSON file

        Args:
            person_name: Name of the famous person
            output_file: Optional custom output file path

        Returns:
            The citation data dictionary
        """
        data = self.fetch_citations(person_name)

        if output_file is None:
            # Create safe filename from person name
            safe_name = person_name.lower().replace(" ", "_").replace(".", "")
            output_file = f"{safe_name}_citations.json"

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"Saved citations for {person_name} to {output_file}")
        print(f"Total citations: {data['total_citations']}")

        return data


def main():
    """Example usage"""
    fetcher = CitationFetcher()

    # Test with a famous person
    person = "Oprah Winfrey"
    print(f"Fetching citations for {person}...\n")

    result = fetcher.fetch_citations(person)

    print("=" * 80)
    print(f"Biography Preview (first 500 chars):")
    print("=" * 80)
    print(result['biography'][:500] + "...\n")

    print("=" * 80)
    print(f"Citation URLs ({result['total_citations']} sources):")
    print("=" * 80)
    for i, citation in enumerate(result['citations_with_titles'], 1):
        print(f"{i}. {citation['title']}")
        print(f"   {citation['url']}\n")

    # Save to file
    print("\n" + "=" * 80)
    fetcher.save_citations(person)


if __name__ == "__main__":
    main()
