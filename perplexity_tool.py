"""
Perplexity API Tool Module

This module provides a wrapper for the Perplexity Sonar API through OpenRouter,
specifically designed to extract both content and citation links from responses.
"""

import requests
import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class Citation:
    """Represents a single citation from Perplexity response"""
    url: str
    title: str
    start_index: int = 0
    end_index: int = 0

    def __repr__(self):
        return f"Citation(url='{self.url}', title='{self.title}')"


@dataclass
class PerplexityResponse:
    """Container for Perplexity API response with content and citations"""
    content: str
    citations: List[Citation]
    raw_response: Dict

    def get_citation_urls(self) -> List[str]:
        """Get just the URLs from citations"""
        return [citation.url for citation in self.citations]

    def format_citations(self) -> str:
        """Format citations as a numbered list"""
        formatted = "\n\nSources:\n"
        for i, citation in enumerate(self.citations, 1):
            formatted += f"{i}. {citation.title}\n   {citation.url}\n"
        return formatted


class PerplexityTool:
    """Tool for interacting with Perplexity Sonar API"""

    def __init__(self, config_path: str = "models.json"):
        """
        Initialize the Perplexity tool

        Args:
            config_path: Path to the JSON config file containing API credentials
        """
        with open(config_path, 'r') as f:
            config = json.load(f)

        self.sonar_config = config['models']['sonar']
        self.endpoint = f"{self.sonar_config['endpoint']}/chat/completions"
        self.api_key = self.sonar_config['api_key']
        self.model = self.sonar_config['model']

    def query(self,
              prompt: str,
              system_prompt: Optional[str] = None,
              temperature: float = 0.7) -> PerplexityResponse:
        """
        Query the Perplexity API and extract content with citations

        Args:
            prompt: The user query/prompt
            system_prompt: Optional system prompt for context
            temperature: Sampling temperature (0.0 to 1.0)

        Returns:
            PerplexityResponse containing content, citations, and raw response

        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature
        }

        response = requests.post(self.endpoint, headers=headers, json=payload)
        response.raise_for_status()

        return self._parse_response(response.json())

    def _parse_response(self, response_json: Dict) -> PerplexityResponse:
        """
        Parse the raw API response to extract content and citations

        Args:
            response_json: Raw JSON response from the API

        Returns:
            PerplexityResponse object
        """
        # Extract content
        content = response_json['choices'][0]['message']['content']

        # Extract citations from annotations
        citations = []
        annotations = response_json['choices'][0]['message'].get('annotations', [])

        for annotation in annotations:
            if annotation['type'] == 'url_citation':
                citation_data = annotation['url_citation']
                citations.append(Citation(
                    url=citation_data['url'],
                    title=citation_data['title'],
                    start_index=citation_data.get('start_index', 0),
                    end_index=citation_data.get('end_index', 0)
                ))

        return PerplexityResponse(
            content=content,
            citations=citations,
            raw_response=response_json
        )

    def search_biography(self, person_name: str) -> PerplexityResponse:
        """
        Convenience method for searching biographical information

        Args:
            person_name: Name of the person to search for

        Returns:
            PerplexityResponse with biography and sources
        """
        prompt = f"Who is {person_name}? Give me a comprehensive biography including early life, career, and notable achievements."
        return self.query(prompt)


def main():
    """Example usage of the PerplexityTool"""
    # Initialize the tool
    tool = PerplexityTool()

    # Query for a biography
    print("Querying Perplexity API for Elon Musk biography...\n")
    result = tool.search_biography("Elon Musk")

    # Display results
    print("=" * 80)
    print("CONTENT:")
    print("=" * 80)
    print(result.content)

    print("\n" + "=" * 80)
    print(f"CITATIONS ({len(result.citations)} sources):")
    print("=" * 80)
    print(result.format_citations())

    # Access individual citation URLs
    print("\n" + "=" * 80)
    print("CITATION URLS ONLY:")
    print("=" * 80)
    for url in result.get_citation_urls():
        print(f"  - {url}")


if __name__ == "__main__":
    main()
