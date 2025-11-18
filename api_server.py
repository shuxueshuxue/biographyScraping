"""
Simple Flask API server for the Life Experience Search Engine
Serves the frontend and provides search API endpoint
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from embedding_tool import EmbeddingTool
import os

app = Flask(__name__, static_folder='frontend')
CORS(app)

# Initialize embedding tool
embedder = EmbeddingTool()

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files (CSS, JS)"""
    return send_from_directory('frontend', path)

@app.route('/api/search', methods=['POST'])
def search():
    """
    Search for matching experiences

    Request body:
    {
        "query": "user's experience text",
        "top_k": 5  (optional, default 5)
    }

    Response:
    {
        "matches": [
            {
                "person": "Steve Jobs",
                "similarity": 0.4367,
                "keywords": ["career-rejection", "firing"],
                "text": "experience text...",
                "source_url": "https://..."
            },
            ...
        ],
        "query": "original query",
        "total_matches": 5
    }
    """
    try:
        data = request.get_json()

        if not data or 'query' not in data:
            return jsonify({'error': 'Missing query in request body'}), 400

        query = data['query']
        top_k = data.get('top_k', 5)

        # Validate inputs
        if not isinstance(query, str) or not query.strip():
            return jsonify({'error': 'Query must be a non-empty string'}), 400

        if not isinstance(top_k, int) or top_k < 1 or top_k > 50:
            return jsonify({'error': 'top_k must be an integer between 1 and 50'}), 400

        # Perform search
        matches = embedder.match_across_database(query, top_k=top_k)

        return jsonify({
            'matches': matches,
            'query': query,
            'total_matches': len(matches)
        })

    except Exception as e:
        print(f"Error in search endpoint: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats', methods=['GET'])
def stats():
    """
    Get database statistics

    Response:
    {
        "total_celebrities": 122,
        "total_experiences": 3500,
        "database_path": "data/vector_db"
    }
    """
    try:
        import glob
        db_files = glob.glob('data/vector_db/*.json')

        total_experiences = 0
        for db_file in db_files:
            import json
            with open(db_file, 'r') as f:
                data = json.load(f)
                total_experiences += len(data.get('experiences', []))

        return jsonify({
            'total_celebrities': len(db_files),
            'total_experiences': total_experiences,
            'database_path': 'data/vector_db'
        })

    except Exception as e:
        print(f"Error in stats endpoint: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Check if vector database exists
    if not os.path.exists('data/vector_db'):
        print("ERROR: Vector database not found at data/vector_db/")
        print("Please run Stage 1 and Stage 2 to build the database first.")
        exit(1)

    print("="*80)
    print("Life Experience Search Engine - API Server")
    print("="*80)
    print("\nStarting server...")
    print("Frontend: http://localhost:5000")
    print("API: http://localhost:5000/api/search")
    print("\nPress Ctrl+C to stop")
    print("="*80)

    app.run(host='0.0.0.0', port=5000, debug=True)
