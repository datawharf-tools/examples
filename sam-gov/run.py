"""Small-business IT solicitations. Runs without a SAM.gov key (daily public file).
Usage: APIFY_TOKEN=... python run.py   (pip install apify-client first)
"""
import os

from apify_client import ApifyClient

token = os.environ.get("APIFY_TOKEN")
if not token:
    raise SystemExit("Set the APIFY_TOKEN environment variable.")

client = ApifyClient(token)
run_input = {
    "naicsCodes": [
        "541512"
    ],
    "setAside": "SBA",
    "noticeTypes": [
        "o",
        "k"
    ],
    "maxResults": 20
}

run = client.actor("datawharf-tools/sam-gov-opportunities").call(run_input=run_input)
items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
for row in items:
    print(" | ".join(str(row.get(k, ""))[:60] for k in ["noticeId", "title", "agency", "responseDeadline", "setAside"]))
print(f"{len(items)} rows, run {run['id']}")
