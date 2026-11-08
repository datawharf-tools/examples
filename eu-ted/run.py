"""IT-services contract notices from German and French buyers (last 30 days).
Usage: APIFY_TOKEN=... python run.py   (pip install apify-client first)
"""
import os

from apify_client import ApifyClient

token = os.environ.get("APIFY_TOKEN")
if not token:
    raise SystemExit("Set the APIFY_TOKEN environment variable.")

client = ApifyClient(token)
run_input = {
    "countries": [
        "DE",
        "FR"
    ],
    "cpvCodes": [
        "72"
    ],
    "noticeTypes": [
        "cn-standard"
    ],
    "titleLanguage": "en",
    "maxResults": 20
}

run = client.actor("datawharf-tools/eu-ted-tenders").call(run_input=run_input)
items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
for row in items:
    print(" | ".join(str(row.get(k, ""))[:60] for k in ["noticeId", "buyerCountry", "publicationDate", "deadline", "title"]))
print(f"{len(items)} rows, run {run['id']}")
