# Reverse Image Search Web App

This project provides a simple web interface to upload an image and search for similar images on the internet. The search relies on an external image search API (for example, Bing Visual Search). You must supply your own API key and endpoint in environment variables `BING_VISUAL_SEARCH_KEY` and `BING_VISUAL_SEARCH_ENDPOINT`.

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Export your API credentials:

```bash
export BING_VISUAL_SEARCH_KEY=your_key
export BING_VISUAL_SEARCH_ENDPOINT="https://api.bing.microsoft.com/v7.0/images/visualsearch"
```

3. Run the server:

```bash
python webapp/server.py
```

4. Open your browser at `http://localhost:5000` and upload an image to search.

## Limitations

- This project uses an external API for image search. You may need to sign up for a key. Free tiers may have usage limits.
- The repository does not include any API credentials.
