# Reverse Image Search Web App

This project provides a simple web interface to upload an image and search for similar images on the internet. The search relies on an external image search API. By default Bing Visual Search is used, but you can also use SerpApi (Google Lens). Supply the appropriate credentials via environment variables.

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Provide your API credentials. You can configure either Bing Visual Search or SerpApi. There are two ways to supply the keys:

   * **Environment variables** (existing behaviour)
   * **Configuration file**: copy `config_example.py` to `config.py` and edit it with your credentials. This file is ignored by git.
   * **.env file**: create a `.env` file with the same variables if you prefer keeping them outside the code.

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

### Using a custom local domain

If you want to access the web app with a custom name such as
`https://recherche-image.com`, map this domain to your machine in your
`/etc/hosts` file:

```bash
127.0.0.1 recherche-image.com
```

Run the server with HTTPS enabled:

```bash
HOST=0.0.0.0 PORT=5000 HTTPS=1 python webapp/server.py
```

Then open `https://recherche-image.com:5000` in your browser. The Flask
development server uses a self-signed certificate, so your browser may display a
warning that you need to accept.

## Limitations

- This project uses an external API for image search. You may need to sign up for a key. Free tiers may have usage limits.
- The repository does not include any API credentials.
