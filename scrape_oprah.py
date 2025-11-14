"""
Quick script to scrape Oprah Winfrey's biography from biography.com
"""

import requests
from bs4 import BeautifulSoup
import json

def scrape_biography(url: str):
    """Scrape biographical content from biography.com"""

    # Use headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract the main content
        # Biography.com typically uses article tags or specific content divs

        # Try to find the main article content
        article = soup.find('article') or soup.find('div', class_='article-body')

        if not article:
            # Try to find content by common classes
            article = (soup.find('div', class_='content') or
                      soup.find('div', class_='biography-content') or
                      soup.find('main'))

        if article:
            # Extract all paragraphs
            paragraphs = article.find_all('p')
            content = '\n\n'.join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])

            # Also try to get the title
            title = soup.find('h1')
            title_text = title.get_text().strip() if title else "Oprah Winfrey Biography"

            return {
                "success": True,
                "title": title_text,
                "content": content,
                "url": url
            }
        else:
            return {
                "success": False,
                "error": "Could not find article content on the page",
                "url": url
            }

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"Request failed: {str(e)}",
            "url": url
        }

if __name__ == "__main__":
    url = "https://www.biography.com/movies-tv/oprah-winfrey"

    print(f"Scraping: {url}\n")
    print("=" * 80)

    result = scrape_biography(url)

    if result['success']:
        print(f"Title: {result['title']}\n")
        print("=" * 80)
        print("BIOGRAPHICAL CONTENT:")
        print("=" * 80)
        print(result['content'])

        # Save to file
        output_file = "oprah_winfrey_biography.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"Title: {result['title']}\n")
            f.write(f"URL: {result['url']}\n")
            f.write(f"{'=' * 80}\n\n")
            f.write(result['content'])

        print(f"\n\n{'=' * 80}")
        print(f"Content saved to: {output_file}")

        # Also save as JSON
        json_file = "oprah_winfrey_biography.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"JSON saved to: {json_file}")

    else:
        print(f"ERROR: {result['error']}")
