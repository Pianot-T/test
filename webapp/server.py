import os
from flask import Flask, render_template, request, jsonify
from PIL import Image
import requests
from io import BytesIO

app = Flask(__name__)

# Placeholder function to call an external reverse image search API
# You need to supply your own API key and endpoint.
# Example uses Bing Visual Search which requires a key.

def search_image(image_bytes):
    """Call external API to search for similar images."""
    api_key = os.environ.get('BING_VISUAL_SEARCH_KEY')
    endpoint = os.environ.get('BING_VISUAL_SEARCH_ENDPOINT')
    if not api_key or not endpoint:
        return []  # API not configured

    headers = {
        'Ocp-Apim-Subscription-Key': api_key,
        'Content-Type': 'multipart/form-data'
    }
    files = {'image': ('image.jpg', image_bytes)}
    response = requests.post(endpoint, headers=headers, files=files)
    if response.status_code == 200:
        data = response.json()
        results = []
        for tag in data.get('tags', []):
            for action in tag.get('actions', []):
                if action.get('actionType') == 'VisualSearch':
                    for item in action.get('data', {}).get('value', []):
                        results.append({
                            'url': item.get('hostPageUrl'),
                            'thumbnail': item.get('thumbnailUrl')
                        })
        return results
    return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    image_file = request.files.get('image')
    if not image_file:
        return jsonify([])
    image_bytes = image_file.read()
    results = search_image(image_bytes)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
