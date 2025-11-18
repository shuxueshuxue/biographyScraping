# Biography Scraping & Matching System

> Build a vector database of famous people's life experiences to match and inspire users facing similar challenges.

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

This project automatically scrapes biographical information about famous people, extracts their life experiences (especially challenges and adversity), and builds a searchable vector database. Users can then query with their own experiences to find matching stories from famous people who overcame similar challenges.

**Example:**
```
User: "I was fired from my own company and feel devastated"

Match: Steve Jobs (Similarity: 0.46)
"In 1985, Jobs faced his greatest professional blow when Apple's board
removed him as cofounder... 'Getting fired from Apple was the best thing
that could have ever happened to me.'"
```

## Features

- **Automated Scraping:** Uses Perplexity API to find sources, Claude Code to scrape and extract experiences
- **Structured Extraction:** Each experience tagged with keywords (e.g., "firing, career-devastation, resilience")
- **Vector Search:** Find semantically similar experiences using OpenAI embeddings
- **Simple Architecture:** No complex database - just JSON files and linear search (fast enough for 100+ people)
- **Manual Control:** Three-stage workflow for full control over the process

## Quick Start

### Web Interface

```bash
# Clone and install
git clone https://github.com/shuxueshuxue/biographyScraping.git
cd biographyScraping

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .

# Start web server
python api_server.py
# Open http://localhost:5000
```

### Command Line

```bash
# Python 3.12+
python --version

# Install uv (optional)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Configuration

Create `models.json` with your API keys:

```json
{
  "models": {
    "sonar": {
      "endpoint": "https://openrouter.ai/api/v1",
      "api_key": "sk-or-v1-YOUR-KEY-HERE",
      "model": "perplexity/sonar"
    }
  }
}
```

Get your [OpenRouter API key](https://openrouter.ai/) (includes Perplexity and OpenAI models).

## Usage

### Three-Stage Workflow

#### Stage 1: Scrape Biographical Experiences

```bash
python stage1_scrape.py "Steve Jobs"
```

- Fetches ~10-15 citation URLs from Perplexity
- Launches Claude Code to scrape all URLs
- Extracts structured experiences with keywords
- **Output:** `data/celebrities/steve_jobs/experiences.txt`
- **Time:** ~3-5 minutes per person

#### Stage 2: Generate Embeddings

```bash
python stage2_embed.py "Steve Jobs"
```

- Parses experiences from text file
- Generates 1536-dimensional embeddings via OpenAI API
- **Output:** `data/vector_db/steve_jobs.json`
- **Time:** ~10 seconds per person

#### Stage 3: Query the Database

```bash
python stage3_query.py "I was fired from my own company"
python stage3_query.py "I failed my startup" --top 10
```

- Searches all experiences in vector database
- Returns top-k most similar experiences
- **Time:** Instant (< 1 second)

### Example Workflow

```bash
# Process multiple people
python stage1_scrape.py "Steve Jobs"
python stage2_embed.py "Steve Jobs"

python stage1_scrape.py "Oprah Winfrey"
python stage2_embed.py "Oprah Winfrey"

python stage1_scrape.py "Elon Musk"
python stage2_embed.py "Elon Musk"

# Query across all people
python stage3_query.py "I overcame childhood poverty" --top 5
```

## Project Structure

```
biographyScraping/
├── api_server.py               # Flask web server
├── batch_process.py            # Batch processing script
├── pyproject.toml              # Dependencies
│
├── Tool Modules
│   ├── citation_fetcher.py
│   ├── deep_scraper.py
│   ├── embedding_tool.py
│   └── perplexity_tool.py
│
├── Workflow Scripts
│   ├── stage1_scrape.py
│   ├── stage2_embed.py
│   └── stage3_query.py
│
├── frontend/                   # Web UI
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   └── images/
│
└── data/ (gitignored)
    ├── celebrities/{person}/
    └── vector_db/{person}.json
```

## How It Works

### 1. Citation Discovery (Perplexity)
Uses Perplexity's Sonar model to search for biographical sources and extract citation URLs.

### 2. Intelligent Scraping (Claude Code)
Claude Code autonomously:
- Fetches webpage content
- Extracts biographical narratives
- Identifies individual experiences
- Tags with relevant keywords
- Handles errors gracefully

### 3. Vector Embedding (OpenAI)
Each experience is converted to a 1536-dimensional vector using `text-embedding-3-small`.

### 4. Semantic Search
User queries are embedded and compared using cosine similarity to find matching experiences.

## Performance

- **Build Time:** ~6-8 hours for 100 people (mostly scraping)
- **Database Size:** ~50-100MB (JSON files)
- **Query Speed:** < 1 second (linear search works fine)
- **Accuracy:** Cosine similarity 0.3-0.5+ indicates good matches

## Example Famous People

```
Business: Steve Jobs, Elon Musk, Jeff Bezos, Mark Zuckerberg, Jack Ma
Media: Oprah Winfrey, Walt Disney, Steven Spielberg, J.K. Rowling
Sports: Michael Jordan, Serena Williams, Muhammad Ali, Simone Biles
Science: Albert Einstein, Marie Curie, Stephen Hawking, Neil deGrasse Tyson
Politics: Abraham Lincoln, Nelson Mandela, Winston Churchill, Barack Obama
Arts: Maya Angelou, Vincent van Gogh, Frida Kahlo, Lin-Manuel Miranda
```

## API Requirements

- **OpenRouter API** (required)
  - Includes Perplexity Sonar for citations
  - Includes OpenAI embeddings
  - Get key at [openrouter.ai](https://openrouter.ai/)
  - Cost: ~$0.10 per person for scraping + embeddings

## Contributing

Contributions welcome! Areas for improvement:

- Add more famous people to the database
- Improve keyword extraction
- Optimize scraping prompts
- Enhance web interface

## License

MIT License - see [LICENSE](LICENSE) file

## Acknowledgments

- [Perplexity AI](https://www.perplexity.ai/) for citation discovery
- [Anthropic](https://www.anthropic.com/) for Claude Code
- [OpenAI](https://openai.com/) for embeddings
- [OpenRouter](https://openrouter.ai/) for API aggregation

## Documentation

- [Workflow Guide](docs/WORKFLOW.md) - Detailed workflow documentation
- [Module API Reference](docs/MODULES_DOCUMENTATION.md) - Module documentation

## Use Cases

- **Personal Inspiration:** Find role models who overcame similar challenges
- **Career Coaching:** Match clients with relevant success stories
- **Content Creation:** Discover compelling narratives for articles/books
- **Research:** Analyze patterns in how famous people overcame adversity
- **Education:** Teach resilience through real-world examples
