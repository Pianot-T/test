import os
from flask import Flask, render_template, request, jsonify
from PIL import Image
import requests
from io import BytesIO

app = Flask(__name__)

# -- Image search helpers -----------------------------------------------------

def search_image_bing(image_bytes):
    """Search similar images using Bing Visual Search."""
    api_key = os.environ.get('BING_VISUAL_SEARCH_KEY')
    endpoint = os.environ.get('BING_VISUAL_SEARCH_ENDPOINT')
    if not api_key or not endpoint:
        return []

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


def search_image_serpapi(image_bytes):
    """Search similar images using SerpApi (Google Lens)."""
    api_key = os.environ.get('SERPAPI_KEY')
    endpoint = os.environ.get('SERPAPI_ENDPOINT', 'https://serpapi.com/search')
    if not api_key:
        return []

    # SerpApi expects multipart form with image data
    files = {
        'encoded_image': ('image.jpg', image_bytes)
    }
    data = {
        'engine': 'google_lens',
        'api_key': api_key,
        'hl': 'fr'
    }
    response = requests.post(endpoint, data=data, files=files)
    if response.status_code == 200:
        payload = response.json()
        results = []
        for match in payload.get('visual_matches', []):
            results.append({
                'url': match.get('link'),
                'thumbnail': match.get('thumbnail')
            })
        return results
    return []


def search_image(image_bytes):
    """Call the configured external API to search for similar images."""
    if os.environ.get('SERPAPI_KEY'):
        return search_image_serpapi(image_bytes)
    return search_image_bing(image_bytes)

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
