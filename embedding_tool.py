"""
Embedding Tool Module

Provides text embedding functionality using OpenAI's text-embedding-3-small
via OpenRouter API for creating vector representations of biographical experiences.
"""

import json
import requests
from typing import List, Dict, Union
import numpy as np


class EmbeddingTool:
    """Tool for creating text embeddings using OpenRouter API"""

    def __init__(self, config_path: str = "models.json"):
        """
        Initialize the embedding tool

        Args:
            config_path: Path to the JSON config file containing API credentials
        """
        with open(config_path, 'r') as f:
            config = json.load(f)

        self.config = config['models']['sonar']
        self.endpoint = f"{self.config['endpoint']}/embeddings"
        self.api_key = self.config['api_key']
        self.model = "openai/text-embedding-3-small"
        self.dimensions = 1536

    def embed(self, texts: Union[str, List[str]]) -> Union[List[float], List[List[float]]]:
        """
        Generate embeddings for text(s)

        Args:
            texts: Single text string or list of text strings

        Returns:
            Single embedding vector or list of embedding vectors
        """
        # Normalize input to list
        single_input = isinstance(texts, str)
        text_list = [texts] if single_input else texts

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "input": text_list
        }

        response = requests.post(self.endpoint, headers=headers, json=payload)
        response.raise_for_status()

        result = response.json()

        # Extract embeddings
        embeddings = [item['embedding'] for item in result['data']]

        # Return single embedding if single input
        return embeddings[0] if single_input else embeddings

    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """
        Calculate cosine similarity between two vectors

        Args:
            vec1: First embedding vector
            vec2: Second embedding vector

        Returns:
            Cosine similarity score (0 to 1)
        """
        vec1_np = np.array(vec1)
        vec2_np = np.array(vec2)

        dot_product = np.dot(vec1_np, vec2_np)
        norm1 = np.linalg.norm(vec1_np)
        norm2 = np.linalg.norm(vec2_np)

        return float(dot_product / (norm1 * norm2))

    def find_most_similar(
        self,
        query_text: str,
        candidate_texts: List[str],
        top_k: int = 5
    ) -> List[Dict]:
        """
        Find most similar texts to a query

        Args:
            query_text: The query text
            candidate_texts: List of texts to search
            top_k: Number of top results to return

        Returns:
            List of dicts with 'text', 'similarity', and 'index'
        """
        # Get embeddings
        all_texts = [query_text] + candidate_texts
        embeddings = self.embed(all_texts)

        query_embedding = embeddings[0]
        candidate_embeddings = embeddings[1:]

        # Calculate similarities
        similarities = [
            {
                'text': text,
                'similarity': self.cosine_similarity(query_embedding, emb),
                'index': i
            }
            for i, (text, emb) in enumerate(zip(candidate_texts, candidate_embeddings))
        ]

        # Sort by similarity (descending)
        similarities.sort(key=lambda x: x['similarity'], reverse=True)

        return similarities[:top_k]


    def parse_experiences_file(self, file_path: str) -> List[Dict]:
        """
        Parse experiences.txt into structured list

        Args:
            file_path: Path to experiences.txt file

        Returns:
            List of dicts with 'keywords', 'text', and optionally 'source_url'
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        experiences = []
        blocks = content.split('\n---\n')

        for block in blocks:
            if not block.strip():
                continue

            lines = block.strip().split('\n')

            # Extract keywords
            keywords_line = [l for l in lines if l.startswith('[KEYWORDS:')]
            keywords = []
            if keywords_line:
                kw_text = keywords_line[0].replace('[KEYWORDS:', '').replace(']', '')
                keywords = [k.strip() for k in kw_text.split(',')]

            # Extract source URL (optional)
            source_line = [l for l in lines if l.startswith('[SOURCE:')]
            source_url = ""
            if source_line:
                source_url = source_line[0].replace('[SOURCE:', '').replace(']', '').strip()

            # Extract text (everything else)
            text_lines = [l for l in lines if not l.startswith('[')]
            text = '\n'.join(text_lines).strip()

            if text:  # Only add if there's actual text
                exp = {
                    'keywords': keywords,
                    'text': text
                }
                if source_url:
                    exp['source_url'] = source_url
                experiences.append(exp)

        return experiences

    def match_across_database(
        self,
        query: str,
        db_folder: str = "data/vector_db",
        top_k: int = 5
    ) -> List[Dict]:
        """
        Find matching experiences across all celebrities

        Args:
            query: User's experience text
            db_folder: Path to vector database folder
            top_k: Number of top results to return

        Returns:
            List of matches with person, keywords, text, similarity
        """
        import json
        from pathlib import Path

        # Get query embedding
        query_emb = self.embed(query)

        # Load all celebrities and their experiences
        all_matches = []

        db_path = Path(db_folder)
        if not db_path.exists():
            print(f"Warning: Database folder '{db_folder}' not found")
            return []

        for json_file in db_path.glob("*.json"):
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            person = data['person']

            for exp in data['experiences']:
                similarity = self.cosine_similarity(query_emb, exp['embedding'])
                match = {
                    'person': person,
                    'keywords': exp['keywords'],
                    'text': exp['text'],
                    'similarity': similarity
                }
                if 'source_url' in exp:
                    match['source_url'] = exp['source_url']
                all_matches.append(match)

        # Sort by similarity descending
        all_matches.sort(key=lambda x: x['similarity'], reverse=True)

        return all_matches[:top_k]


def main():
    """Example usage"""
    tool = EmbeddingTool()

    # Example experiences
    experiences = [
        "Steve Jobs was fired from Apple in 1985, the company he founded.",
        "Oprah overcame childhood poverty and abuse to become a media mogul.",
        "J.K. Rowling was rejected by 12 publishers before Harry Potter succeeded.",
        "Building a successful startup from a garage with limited resources.",
        "Colonel Sanders was rejected 1009 times before KFC became successful."
    ]

    # User's experience
    user_query = "I was rejected from my own company and felt devastated."

    print("Finding similar experiences...")
    print(f"\nUser query: '{user_query}'")
    print("\n" + "="*80)

    results = tool.find_most_similar(user_query, experiences, top_k=3)

    print("\nTop 3 most similar experiences:")
    print("="*80)
    for i, result in enumerate(results, 1):
        print(f"\n{i}. Similarity: {result['similarity']:.4f}")
        print(f"   {result['text']}")


if __name__ == "__main__":
    main()
