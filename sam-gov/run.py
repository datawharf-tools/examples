"""Recent software solicitations. Runs without a SAM.gov key (daily public file).
Usage: APIFY_TOKEN=... python run.py   (pip install "apify-client>=3" first)
"""
import os

from apify_client import ApifyClient

token = os.environ.get("APIFY_TOKEN")
if not token:
    raise SystemExit("Set the APIFY_TOKEN environment variable.")

client = ApifyClient(token)
run_input = {
    "keywords": ["software"],
    "noticeTypes": ["o", "k"],
    "maxResults": 10
}

run = client.actor("datawharf-tools/sam-gov-opportunities").call(run_input=run_input)
items = list(client.dataset(run.default_dataset_id).iterate_items())
for row in items:
    print(" | ".join(str(row.get(k, ""))[:60] for k in ["postedDate", "responseDeadline", "title", "agency"]))
print(f"{len(items)} rows, run {run.id}")
