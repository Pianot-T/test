import os
from flask import Flask, render_template, request, jsonify
from PIL import Image
import requests
from io import BytesIO
from dotenv import load_dotenv

try:
    import config  # local configuration (not tracked in git)
except ImportError:  # pragma: no cover - config is optional
    config = None

load_dotenv()

def get_setting(name, default=None):
    """Return configuration from environment or optional config module."""
    value = os.environ.get(name)
    if value:
        return value
    if config and hasattr(config, name):
        return getattr(config, name)
    return default

app = Flask(__name__)


def api_is_active():
    """Return True if at least one API key is configured."""
    if get_setting('SERPAPI_KEY'):
        return True
    if get_setting('BING_VISUAL_SEARCH_KEY') and get_setting('BING_VISUAL_SEARCH_ENDPOINT'):
        return True
    return False

# -- Image search helpers -----------------------------------------------------

def search_image_bing(image_bytes):
    """Search similar images using Bing Visual Search."""
    api_key = get_setting('BING_VISUAL_SEARCH_KEY')
    endpoint = get_setting('BING_VISUAL_SEARCH_ENDPOINT')
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
    api_key = get_setting('SERPAPI_KEY')
    endpoint = get_setting('SERPAPI_ENDPOINT', 'https://serpapi.com/search')
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
    if get_setting('SERPAPI_KEY'):
        return search_image_serpapi(image_bytes)
    return search_image_bing(image_bytes)

@app.route('/')
def index():
    return render_template('index.html', api_active=api_is_active())

@app.route('/search', methods=['POST'])
def search():
    image_file = request.files.get('image')
    if not image_file:
        return jsonify([])
    image_bytes = image_file.read()
    results = search_image(image_bytes)
    return jsonify(results)

if __name__ == '__main__':
    host = os.environ.get('HOST', '127.0.0.1')
    port = int(os.environ.get('PORT', 5000))
    use_https = os.environ.get('HTTPS') == '1'
    if use_https:
        app.run(host=host, port=port, debug=True, ssl_context='adhoc')
    else:
        app.run(host=host, port=port, debug=True)
