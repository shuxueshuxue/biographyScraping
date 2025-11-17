# Biography Scraping Workflow

## Overview
Build a vector database of famous people's life experiences for matching user experiences.

## Folder Structure
```
├── Tool Modules (reusable)
│   ├── citation_fetcher.py      - Fetch citations from Perplexity
│   ├── deep_scraper.py          - Scrape URLs with Claude Code
│   └── embedding_tool.py        - Generate embeddings & match
│
├── Workflow Scripts (stages)
│   ├── stage1_scrape.py         - Scrape biographical experiences
│   ├── stage2_embed.py          - Generate embeddings
│   └── stage3_query.py          - Query the database
│
└── Data
    ├── data/celebrities/{person}/
    │   ├── experiences.txt       - Structured experiences
    │   └── scraping_summary.txt  - Scraping report
    └── data/vector_db/{person}.json - Embeddings database
```

## Workflow Stages

### Stage 1: Scrape Experiences
```bash
python stage1_scrape.py "Person Name"
```

**What it does:**
1. Fetches ~10-15 citation URLs from Perplexity
2. Launches Claude Code to scrape all URLs
3. Extracts individual experiences with keywords
4. Saves to `data/celebrities/{person}/experiences.txt`

**Example:**
```bash
python stage1_scrape.py "Steve Jobs"
python stage1_scrape.py "Oprah Winfrey"
python stage1_scrape.py "Elon Musk"
```

**Output format (experiences.txt):**
```
[KEYWORDS: firing, career-devastation, setback]
In 1985, Jobs faced his greatest professional blow when Apple's board...

---

[KEYWORDS: resilience, comeback, new-venture]
Instead of accepting defeat, Jobs channeled his energy into founding NeXT...

---
```

### Stage 2: Generate Embeddings
```bash
python stage2_embed.py "Person Name"
```

**What it does:**
1. Parses `experiences.txt` file
2. Generates 1536-dimensional embeddings for each experience
3. Saves to `data/vector_db/{person}.json`

**Example:**
```bash
python stage2_embed.py "Steve Jobs"
python stage2_embed.py "Oprah Winfrey"
```

**Output format (vector_db JSON):**
```json
{
  "person": "Steve Jobs",
  "experiences": [
    {
      "keywords": ["firing", "career-devastation"],
      "text": "In 1985, Jobs faced...",
      "embedding": [0.123, -0.456, ...]
    }
  ]
}
```

### Stage 3: Query Database
```bash
python stage3_query.py "user experience text"
python stage3_query.py "user experience text" --top 10
```

**What it does:**
1. Embeds user query
2. Searches all experiences in vector database
3. Returns top-k most similar experiences

**Example:**
```bash
python stage3_query.py "I was fired from my own company"
python stage3_query.py "I failed my startup" --top 10
```

**Output:**
```
TOP 5 MATCHING EXPERIENCES
================================================================================

1. Steve Jobs (Similarity: 0.4626)
   Keywords: career-devastation, firing, greatest-setback
   In 1985, Jobs faced his greatest professional blow...

2. Oprah Winfrey (Similarity: 0.4012)
   Keywords: rejection, early-career, discrimination
   Early in her career, Oprah was told she was...
```

## Building Database for 100+ People

```bash
# Process famous people one by one
python stage1_scrape.py "Steve Jobs"
python stage2_embed.py "Steve Jobs"

python stage1_scrape.py "Oprah Winfrey"
python stage2_embed.py "Oprah Winfrey"

python stage1_scrape.py "Elon Musk"
python stage2_embed.py "Elon Musk"

# ... repeat for 100+ people ...

# Query across all people
python stage3_query.py "I overcame childhood poverty"
```

## Performance

- **Stage 1:** ~3-5 minutes per person (depends on Claude Code scraping)
- **Stage 2:** ~10 seconds per person (embedding API calls)
- **Stage 3:** Instant query (loads all JSONs in memory, < 1 second)

For 100 people:
- Total build time: ~6-8 hours
- Database size: ~50-100MB (JSON files)
- Query latency: < 1 second (linear search is fast enough)

## Tips

1. **Run Stage 1 in batches:** Process 5-10 people, then take a break
2. **Stage 2 is cheap:** Can re-run without re-scraping
3. **Stage 3 is instant:** Query as many times as you want
4. **Keep it simple:** No fancy database needed, JSON files work great

## Example Famous People List

```
Steve Jobs, Oprah Winfrey, Elon Musk, J.K. Rowling, Colonel Sanders,
Walt Disney, Thomas Edison, Abraham Lincoln, Nelson Mandela,
Maya Angelou, Albert Einstein, Marie Curie, Stephen Hawking,
Michael Jordan, Serena Williams, Arnold Schwarzenegger, Jim Carrey,
Sylvester Stallone, Harrison Ford, Vera Wang, Anna Wintour,
Howard Schultz, Jack Ma, Richard Branson, Larry Page, Jeff Bezos,
Mark Zuckerberg, Bill Gates, Warren Buffett, Ray Dalio, Sam Walton...
```

Total: 100+ people with diverse backgrounds and adversity stories
