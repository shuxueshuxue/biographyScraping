"""
Alternative scraper using Wikipedia for Oprah Winfrey biography
Wikipedia is more scraping-friendly than biography.com
"""

import requests
from bs4 import BeautifulSoup
import json

def scrape_wikipedia_biography(person_name: str):
    """Scrape biographical content from Wikipedia"""

    # Convert name to Wikipedia format
    wiki_name = person_name.replace(" ", "_")
    url = f"https://en.wikipedia.org/wiki/{wiki_name}"

    headers = {
        'User-Agent': 'BiographyResearchBot/1.0 (Educational purposes)'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Get the main content
        content_div = soup.find('div', id='mw-content-text')

        if not content_div:
            return {
                "success": False,
                "error": "Could not find Wikipedia content",
                "url": url
            }

        # Extract sections relevant to biography
        biographical_sections = []

        # Get all headings and content
        for element in content_div.find_all(['h2', 'h3', 'p']):
            if element.name in ['h2', 'h3']:
                section_title = element.get_text().strip().replace('[edit]', '').strip()

                # Focus on biographical sections
                relevant_keywords = [
                    'early life', 'childhood', 'education', 'career',
                    'personal', 'biography', 'life', 'background',
                    'struggles', 'challenges', 'adversity', 'success',
                    'achievements', 'breakthrough', 'rise'
                ]

                if any(keyword in section_title.lower() for keyword in relevant_keywords):
                    biographical_sections.append(f"\n## {section_title}\n")

            elif element.name == 'p' and biographical_sections:
                text = element.get_text().strip()
                # Filter out reference markers like [1], [2]
                if text and len(text) > 50:  # Ignore very short paragraphs
                    biographical_sections.append(text + "\n")

        # Also get the introduction (first few paragraphs before any heading)
        intro_paragraphs = []
        for p in content_div.find_all('p', limit=5):
            text = p.get_text().strip()
            if text and len(text) > 50:
                intro_paragraphs.append(text)
            if len(intro_paragraphs) >= 3:
                break

        # Combine intro and biographical sections
        full_content = "## Introduction\n\n" + "\n\n".join(intro_paragraphs)
        if biographical_sections:
            full_content += "\n\n" + "\n".join(biographical_sections)

        # Get title
        title = soup.find('h1', id='firstHeading')
        title_text = title.get_text().strip() if title else person_name

        return {
            "success": True,
            "title": title_text,
            "content": full_content,
            "url": url,
            "source": "Wikipedia"
        }

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"Request failed: {str(e)}",
            "url": url
        }

if __name__ == "__main__":
    person_name = "Oprah Winfrey"

    print(f"Scraping Wikipedia for: {person_name}\n")
    print("=" * 80)

    result = scrape_wikipedia_biography(person_name)

    if result['success']:
        print(f"Title: {result['title']}")
        print(f"Source: {result['source']}\n")
        print("=" * 80)
        print("BIOGRAPHICAL CONTENT:")
        print("=" * 80)
        print(result['content'])

        # Save to file
        output_file = "oprah_winfrey_wikipedia.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"Title: {result['title']}\n")
            f.write(f"Source: {result['source']}\n")
            f.write(f"URL: {result['url']}\n")
            f.write(f"{'=' * 80}\n\n")
            f.write(result['content'])

        print(f"\n\n{'=' * 80}")
        print(f"Content saved to: {output_file}")

        # Also save as JSON
        json_file = "oprah_winfrey_wikipedia.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"JSON saved to: {json_file}")

    else:
        print(f"ERROR: {result['error']}")
