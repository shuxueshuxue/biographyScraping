"""
Module 2: Deep Scraper

Uses Claude Code via PolyAgent to intelligently scrape biographical content
from URLs and extract life experience narratives.
"""

import os
import polycli
from typing import List, Dict
from pathlib import Path


class DeepScraper:
    """Scrapes URLs using Claude Code to extract biographical life experiences"""

    def __init__(self):
        """Initialize the scraper with PolyAgent"""
        self.agent = polycli.PolyAgent(id="biography_scraper")

    def scrape_multiple_urls(
        self,
        urls: List[str],
        person_name: str,
        output_dir: str = None
    ) -> Dict[str, any]:
        """
        Scrape multiple URLs and save results using Claude Code

        Args:
            urls: List of URLs to scrape
            person_name: Name of the person
            output_dir: Directory to save results (relative or absolute path)

        Returns:
            Summary dictionary with all results
        """
        if output_dir is None:
            safe_name = person_name.lower().replace(" ", "_").replace(".", "")
            output_dir = f"data/celebrities/{safe_name}"

        # Get absolute path for output directory
        abs_output_dir = os.path.abspath(output_dir)

        # Create output directory
        Path(abs_output_dir).mkdir(parents=True, exist_ok=True)

        print(f"\n{'=' * 80}")
        print(f"Scraping {len(urls)} URLs for {person_name}")
        print(f"Output directory: {abs_output_dir}")
        print(f"{'=' * 80}\n")

        # Build comprehensive prompt for Claude Code
        urls_list = "\n".join([f"{i+1}. {url}" for i, url in enumerate(urls)])

        prompt = f"""You are tasked with scraping biographical information about {person_name} from multiple URLs.

**Person**: {person_name}

**URLs to scrape**:
{urls_list}

**Your task**:
For each URL:
1. Fetch the webpage content (use web requests, handle any errors gracefully)
2. Extract biographical life experiences focusing on:
   - Early life and background
   - Challenges, struggles, and adversity they faced
   - Failures and setbacks
   - How they overcame difficulties
   - Turning points in their life
   - Personal growth and transformation
   - Notable achievements born from hardship

3. Save the extracted content to `source_<number>.txt` where <number> is the URL's position (1, 2, 3, etc.)
4. Each file should contain:
   - The source URL at the top
   - A separator line
   - The extracted biographical narrative in clear, well-formatted text

**Important**:
- If a URL fails to load or doesn't contain relevant biographical information, note this in the file
- Save all files to the current working directory
- After scraping all URLs, create a summary file: scraping_summary.txt

Work autonomously and handle all file I/O yourself."""

        try:
            # Create a new agent with the output directory as working directory
            print("Launching Claude Code to scrape URLs...")
            scraper_agent = polycli.PolyAgent(id="biography_scraper", cwd=abs_output_dir)
            result = scraper_agent.run(prompt)

            print(f"\n{'=' * 80}")
            print("Claude Code scraping complete!")
            print(f"Check output directory: {abs_output_dir}")
            print(f"{'=' * 80}\n")

            return {
                "person_name": person_name,
                "total_urls": len(urls),
                "output_dir": abs_output_dir,
                "success": True,
                "result": str(result)
            }

        except Exception as e:
            print(f"Error running Claude Code: {e}")
            return {
                "person_name": person_name,
                "total_urls": len(urls),
                "output_dir": abs_output_dir,
                "success": False,
                "error": str(e)
            }

    def scrape_with_structured_format(
        self,
        urls: List[str],
        person_name: str,
        output_dir: str = None
    ) -> Dict[str, any]:
        """
        Scrape URLs and extract experiences in structured key-value format

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

        # Get absolute path for output directory
        abs_output_dir = os.path.abspath(output_dir)

        # Create output directory
        Path(abs_output_dir).mkdir(parents=True, exist_ok=True)

        print(f"\n{'=' * 80}")
        print(f"Scraping {len(urls)} URLs for {person_name}")
        print(f"Output: Structured key-value format")
        print(f"Output directory: {abs_output_dir}")
        print(f"{'=' * 80}\n")

        # Build comprehensive prompt for Claude Code
        urls_list = "\n".join([f"{i+1}. {url}" for i, url in enumerate(urls)])

        prompt = f"""You are tasked with scraping biographical information about {person_name} from multiple URLs and extracting individual life experiences in a structured format.

**Person**: {person_name}

**URLs to scrape**:
{urls_list}

**Your task**:

1. **Scrape all URLs** - Fetch content from each URL, handle errors gracefully

2. **Extract individual experiences** - From ALL scraped content, identify distinct life experiences. Each URL may contain MULTIPLE experiences. Look for:
   - Early life events
   - Challenges and adversity
   - Failures and setbacks
   - Turning points
   - Achievements born from hardship
   - Personal growth moments

3. **Create structured output file: `experiences.txt`**

   Format each experience as:
   ```
   [KEYWORDS: keyword1, keyword2, keyword3]
   [SOURCE: url_where_this_came_from]
   experience text here...
   describing the event, context, and impact.
   Can span multiple lines.

   ---

   [KEYWORDS: keyword4, keyword5]
   [SOURCE: url_where_this_came_from]
   another experience text...

   ---
   ```

   **IMPORTANT**: Always include the [SOURCE: url] line to track which URL each experience came from.

   **Keywords should be descriptive tags** like:
   - childhood-poverty, abuse, neglect
   - career-rejection, business-failure, bankruptcy
   - illness, addiction, loss
   - education-turning-point, mentor-influence
   - resilience, comeback, breakthrough

4. **Also create a summary file: `scraping_summary.txt`** with:
   - Total URLs attempted
   - Successfully scraped count
   - Total experiences extracted
   - Any errors encountered

**Important**:
- Each experience should be standalone and self-contained
- Keywords should help categorize the type of experience
- Multiple experiences can come from a single URL
- Save files to the current working directory
- Be comprehensive - extract ALL relevant experiences

Work autonomously and handle all web requests and file I/O yourself."""

        try:
            # Create a new agent with the output directory as working directory
            print("Launching Claude Code to scrape and structure experiences...")
            scraper_agent = polycli.PolyAgent(id="biography_scraper", cwd=abs_output_dir)
            result = scraper_agent.run(prompt)

            print(f"\n{'=' * 80}")
            print("Claude Code scraping complete!")
            print(f"Check output directory: {abs_output_dir}")
            print(f"Files: experiences.txt, scraping_summary.txt")
            print(f"{'=' * 80}\n")

            return {
                "person_name": person_name,
                "total_urls": len(urls),
                "output_dir": abs_output_dir,
                "success": True,
                "result": str(result)
            }

        except Exception as e:
            print(f"Error running Claude Code: {e}")
            return {
                "person_name": person_name,
                "total_urls": len(urls),
                "output_dir": abs_output_dir,
                "success": False,
                "error": str(e)
            }


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
