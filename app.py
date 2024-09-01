from flask import Flask, request, jsonify
import random
import string

app = Flask(__name__)

# In-memory storage for URLs
url_mapping = {}
base_url = "http://127.0.0.1:5000/"

def generate_short_url(length=6):
    """Generate a random short URL."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@app.route('/shorten', methods=['POST'])
def shorten_url():
    """Create a short URL."""
    data = request.json
    long_url = data.get('long_url')
    
    if not long_url:
        return jsonify({"error": "Missing long_url"}), 400

    short_code = generate_short_url()
    short_url = base_url + short_code

    # Store the mapping
    url_mapping[short_code] = long_url

    return jsonify({"short_url": short_url}), 201

@app.route('/<short_code>', methods=['GET'])
def get_long_url(short_code):
    """Retrieve the long URL from the short code."""
    long_url = url_mapping.get(short_code)
    
    if not long_url:
        return jsonify({"error": "URL not found"}), 404

    return jsonify({"long_url": long_url}), 200

@app.route('/urls', methods=['GET'])
def list_urls():
    """List all stored URLs."""
    return jsonify(url_mapping), 200

if __name__ == '__main__':
    app.run(debug=True)