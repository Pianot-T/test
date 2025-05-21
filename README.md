# Reverse Image Search Web App

This project provides a simple web interface to upload an image and search for similar images on the internet. The search relies on an external image search API. By default Bing Visual Search is used, but you can also use SerpApi (Google Lens). Supply the appropriate credentials via environment variables.

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Export your API credentials. You can configure either Bing Visual Search or SerpApi:

```bash
# For Bing
export BING_VISUAL_SEARCH_KEY=your_key
export BING_VISUAL_SEARCH_ENDPOINT="https://api.bing.microsoft.com/v7.0/images/visualsearch"

# Or for SerpApi (Google Lens)
export SERPAPI_KEY=your_serpapi_key
export SERPAPI_ENDPOINT="https://serpapi.com/search"
```

If `SERPAPI_KEY` is set, the application will use SerpApi. Otherwise it falls back to Bing Visual Search.

3. Run the server:

```bash
python webapp/server.py
```

4. Open your browser at `http://localhost:5000` and upload an image to search.

Alternatively you can run the helper script which starts the server and
opens your default browser automatically:

```bash
python run_webapp.py
```

## Limitations

- This project uses an external API for image search. You may need to sign up for a key. Free tiers may have usage limits.
- The repository does not include any API credentials.
