"""Video search. Needs your own YouTube Data API v3 key in YOUTUBE_API_KEY.
Usage: APIFY_TOKEN=... python run.py   (pip install "apify-client>=3" first)
"""
import os

from apify_client import ApifyClient

token = os.environ.get("APIFY_TOKEN")
if not token:
    raise SystemExit("Set the APIFY_TOKEN environment variable.")
api_key = os.environ.get("YOUTUBE_API_KEY")
if not api_key:
    raise SystemExit("Set YOUTUBE_API_KEY (your own Google API key).")

client = ApifyClient(token)
run_input = {
    "mode": "searchVideos",
    "query": "python tutorial",
    "maxResults": 10,
    "apiKey": api_key,
}

run = client.actor("datawharf-tools/youtube-data-api").call(run_input=run_input)
items = list(client.dataset(run.default_dataset_id).iterate_items())
for row in items:
    print(" | ".join(str(row.get(k, ""))[:60] for k in ["videoId", "title", "channelTitle", "publishedAt"]))
print(f"{len(items)} rows, run {run.id}")
