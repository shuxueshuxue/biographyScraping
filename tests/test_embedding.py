"""
Test OpenRouter embedding API with text-embedding-3-small
"""

import json
import requests

# Load config
with open('models.json', 'r') as f:
    config = json.load(f)

sonar_config = config['models']['sonar']

# Test embedding API
url = f"{sonar_config['endpoint']}/embeddings"
headers = {
    "Authorization": f"Bearer {sonar_config['api_key']}",
    "Content-Type": "application/json"
}

test_texts = [
    "Steve Jobs was fired from Apple in 1985",
    "Overcoming childhood poverty and abuse",
    "Building a startup from a garage"
]

payload = {
    "model": "openai/text-embedding-3-small",
    "input": test_texts
}

print("Testing OpenRouter embedding API...")
print(f"Endpoint: {url}")
print(f"Model: openai/text-embedding-3-small")
print(f"Test texts: {len(test_texts)}")
print()

try:
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    result = response.json()

    print("✓ API call successful!")
    print()
    print(f"Response structure:")
    print(f"  - Object: {result.get('object')}")
    print(f"  - Model: {result.get('model')}")
    print(f"  - Data entries: {len(result.get('data', []))}")
    print()

    if 'data' in result and len(result['data']) > 0:
        first_embedding = result['data'][0]['embedding']
        print(f"First embedding:")
        print(f"  - Index: {result['data'][0]['index']}")
        print(f"  - Embedding dimensions: {len(first_embedding)}")
        print(f"  - First 10 values: {first_embedding[:10]}")
        print()

    # Show usage if available
    if 'usage' in result:
        print(f"Usage:")
        print(f"  - Prompt tokens: {result['usage'].get('prompt_tokens')}")
        print(f"  - Total tokens: {result['usage'].get('total_tokens')}")

    print()
    print("Full response (pretty printed):")
    print(json.dumps(result, indent=2))

except requests.exceptions.HTTPError as e:
    print(f"✗ HTTP Error: {e}")
    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.text}")
except Exception as e:
    print(f"✗ Error: {e}")
