# Biography Scraping Modules Documentation

## Overview
Two modules for automatically fetching famous people's life experiences to build a knowledge base for matching user experiences.

---

## Module 1: Citation Fetcher (`citation_fetcher.py`)

### Purpose
Given a famous person's name, fetch their biography from Perplexity and extract citation URLs for further scraping.

### Key Features
- Uses Perplexity Sonar API via OpenRouter
- Focuses on life challenges, struggles, and adversity
- Returns both biography text and citation URLs with titles
- Saves results to JSON for later use

### Usage

```python
from citation_fetcher import CitationFetcher

# Initialize
fetcher = CitationFetcher()

# Fetch citations for a person
result = fetcher.fetch_citations("Oprah Winfrey")

# Access the data
print(result['biography'])           # Full biography text
print(result['citation_urls'])       # List of URLs
print(result['citations_with_titles']) # URLs with titles
print(result['total_citations'])     # Number of sources

# Or save directly to JSON
fetcher.save_citations("Oprah Winfrey", "output.json")
```

### Output Structure
```json
{
  "name": "Person Name",
  "biography": "Full biography text...",
  "citation_urls": ["url1", "url2", ...],
  "citations_with_titles": [
    {"url": "...", "title": "..."},
    ...
  ],
  "total_citations": 11
}
```

---

## Module 2: Deep Scraper (`deep_scraper.py`)

### Purpose
Uses Claude Code (via PolyAgent) to deeply scrape citation URLs and extract raw biographical life experience narratives.

### Key Features
- Launches Claude Code for intelligent web scraping
- Extracts structured life experiences from URLs
- Saves individual source files and summary JSON
- Organized folder structure per celebrity

### Usage

```python
from deep_scraper import DeepScraper

# Initialize
scraper = DeepScraper()

# Scrape multiple URLs
urls = [
    "https://www.biography.com/...",
    "https://en.wikipedia.org/..."
]

summary = scraper.scrape_multiple_urls(
    urls=urls,
    person_name="Oprah Winfrey",
    output_dir="data/celebrities/oprah_winfrey"  # Optional
)

# Or scrape single URL
result = scraper.scrape_with_claude(
    url="https://...",
    person_name="Oprah Winfrey"
)
```

### Output Structure
```
data/celebrities/{person_name}/
├── source_1.txt          # Scraped content from URL 1
├── source_2.txt          # Scraped content from URL 2
├── ...
└── scrape_summary.json   # Summary of all scrapes
```

### Extracted Information
Focus areas:
- Early life and background
- Challenges, struggles, and adversity
- Failures and setbacks
- How they overcame difficulties
- Turning points
- Personal growth and transformation
- Notable achievements born from hardship

---

## Complete Workflow (`test_workflow.py`)

### End-to-End Process

```python
from citation_fetcher import CitationFetcher
from deep_scraper import DeepScraper

# Step 1: Fetch citations from Perplexity
fetcher = CitationFetcher()
citation_data = fetcher.fetch_citations("Oprah Winfrey")

# Step 2: Deep scrape with Claude Code
scraper = DeepScraper()
summary = scraper.scrape_multiple_urls(
    urls=citation_data['citation_urls'][:5],  # Limit URLs as needed
    person_name="Oprah Winfrey"
)

print(f"Scraped {summary['successful_scrapes']} sources")
```

### Run Test Workflow
```bash
source .venv/bin/activate
python test_workflow.py
```

---

## Configuration

### models.json
Contains API credentials for Perplexity/OpenRouter:

```json
{
  "models": {
    "sonar": {
      "endpoint": "https://openrouter.ai/api/v1",
      "api_key": "sk-or-v1-...",
      "model": "perplexity/sonar"
    }
  }
}
```

---

## Dependencies

```toml
dependencies = [
    "polyagent>=1.2.1",
    "requests>=2.32.0",
    "beautifulsoup4>=4.12.0",
    "anthropic>=0.40.0",
]
```

Install with:
```bash
uv pip install requests beautifulsoup4 anthropic
```

---

## Example Output

### Oprah Winfrey Results
- **Citations fetched**: 11 sources
- **URLs scraped**: 1 (test run)
- **Output**: `data/celebrities/oprah_winfrey/`
  - `source_1.txt`: Structured life experiences
  - `scrape_summary.json`: Metadata

### Extracted Content Includes
- Born in rural poverty (1954)
- Sexual abuse ages 9-13
- Pregnancy at 14
- Turning point: father's discipline and education
- Career transformation
- First Black woman billionaire
- Philanthropic achievements

---

## Next Steps

1. **Name Generation**: Create module to generate/suggest famous people with adversity stories
2. **Loop Automation**: Batch process multiple celebrities
3. **Experience Categorization**: Tag experiences by type (poverty, abuse, failure, etc.)
4. **Matching System**: Build user experience matching algorithm
5. **Database**: Consider SQLite for better querying

---

## Notes

- Uses Claude Code via `agent.run()` - no separate Anthropic API key needed
- Perplexity returns ~10-15 citation sources per query
- Each URL scrape takes ~30-60 seconds with Claude Code
- Output is raw text - organization/structuring is next phase
