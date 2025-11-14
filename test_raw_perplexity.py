import requests
import json

# Load the model configuration
with open('models.json', 'r') as f:
    config = json.load(f)

sonar_config = config['models']['sonar']

# Make a raw API request
url = f"{sonar_config['endpoint']}/chat/completions"
headers = {
    "Authorization": f"Bearer {sonar_config['api_key']}",
    "Content-Type": "application/json"
}

payload = {
    "model": sonar_config['model'],
    "messages": [
        {
            "role": "user",
            "content": "Who is Elon Musk? Give me a brief biography."
        }
    ]
}

print("Making request to Perplexity API...")
response = requests.post(url, headers=headers, json=payload)

print(f"\nStatus Code: {response.status_code}")
print(f"\nResponse Headers:")
for key, value in response.headers.items():
    print(f"  {key}: {value}")

print(f"\n{'='*80}")
print("RAW JSON RESPONSE:")
print(f"{'='*80}\n")

# Parse and pretty-print the JSON response
response_json = response.json()
print(json.dumps(response_json, indent=2))

print(f"\n{'='*80}")
print("ANALYZING RESPONSE STRUCTURE:")
print(f"{'='*80}\n")

# Check for citations in various possible locations
def find_citations(obj, path=""):
    """Recursively search for citation-related fields"""
    if isinstance(obj, dict):
        for key, value in obj.items():
            new_path = f"{path}.{key}" if path else key
            if 'citation' in key.lower() or 'source' in key.lower() or 'reference' in key.lower() or 'url' in key.lower():
                print(f"Found potential citation field at: {new_path}")
                print(f"  Value: {value}\n")
            find_citations(value, new_path)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            find_citations(item, f"{path}[{i}]")

find_citations(response_json)
