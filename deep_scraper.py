"""
Module 2: Deep Scraper

Uses Claude Code via PolyAgent to intelligently scrape biographical content
from URLs and extract life experience narratives.
"""

import os
import json
import polycli
from typing import List, Dict
from pathlib import Path


class DeepScraper:
    """Scrapes URLs using Claude Code to extract biographical life experiences"""

    def __init__(self):
        """Initialize the scraper with PolyAgent"""
        self.agent = polycli.PolyAgent(id="biography_scraper")

    def scrape_with_claude(self, url: str, person_name: str) -> Dict[str, str]:
        """
        Use Claude Code to intelligently extract biographical content from a URL

        Args:
            url: The URL to scrape
            person_name: Name of the person for context

        Returns:
            Dictionary with extracted content and metadata
        """
        print(f"Scraping: {url}")

        # Build prompt for Claude Code
        prompt = f"""Scrape the following URL and extract biographical life experiences about {person_name}.

URL: {url}

Focus on extracting:
- Early life and background
- Challenges, struggles, and adversity they faced
- Failures and setbacks
- How they overcame difficulties
- Turning points in their life
- Personal growth and transformation
- Notable achievements born from hardship

Please:
1. Fetch the webpage content
2. Extract relevant biographical narrative text
3. Return the extracted information in a clear, narrative format

If the page doesn't contain relevant biographical information, state that clearly."""

        try:
            # Use agent.run() which launches Claude Code
            result = self.agent.run(prompt)

            # Extract text from RunResult object
            content = str(result) if result else ""

            return {
                "url": url,
                "success": True,
                "content": content
            }

        except Exception as e:
            print(f"Error processing with Claude Code: {e}")
            return {
                "url": url,
                "success": False,
                "error": str(e),
                "content": ""
            }

    def scrape_multiple_urls(
        self,
        urls: List[str],
        person_name: str,
        output_dir: str = None
    ) -> Dict[str, any]:
        """
        Scrape multiple URLs and save results

        Args:
            urls: List of URLs to scrape
            person_name: Name of the person
            output_dir: Directory to save results

        Returns:
            Summary dictionary with all results
        """
        if output_dir is None:
            safe_name = person_name.lower().replace(" ", "_").replace(".", "")
            output_dir = f"data/celebrities/{safe_name}"

        # Create output directory
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        results = []

        for i, url in enumerate(urls, 1):
            print(f"\n[{i}/{len(urls)}] Processing {url}...")

            result = self.scrape_with_claude(url, person_name)
            results.append(result)

            if result['success']:
                # Save individual source file
                source_file = os.path.join(output_dir, f"source_{i}.txt")
                with open(source_file, 'w', encoding='utf-8') as f:
                    f.write(f"URL: {url}\n")
                    f.write(f"{'=' * 80}\n\n")
                    f.write(result['content'])

                print(f"  ✓ Saved to {source_file}")
            else:
                print(f"  ✗ Failed: {result.get('error', 'Unknown error')}")

        # Save summary
        summary = {
            "person_name": person_name,
            "total_urls": len(urls),
            "successful_scrapes": sum(1 for r in results if r['success']),
            "failed_scrapes": sum(1 for r in results if not r['success']),
            "results": results
        }

        summary_file = os.path.join(output_dir, "scrape_summary.json")
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)

        print(f"\n{'=' * 80}")
        print(f"Scraping complete!")
        print(f"  Successful: {summary['successful_scrapes']}/{summary['total_urls']}")
        print(f"  Output directory: {output_dir}")
        print(f"{'=' * 80}")

        return summary


def main():
    """Example usage"""
    # Example: scrape citations for a person
    scraper = DeepScraper()

    # Test URLs (you would get these from citation_fetcher)
    test_urls = [
        "https://en.wikipedia.org/wiki/Oprah_Winfrey",
        "https://www.biography.com/business-leaders/oprah-winfrey"
    ]

    person_name = "Oprah Winfrey"

    summary = scraper.scrape_multiple_urls(
        urls=test_urls,
        person_name=person_name
    )

    print(f"\nScraping summary: {summary['successful_scrapes']} successful")


if __name__ == "__main__":
    main()
