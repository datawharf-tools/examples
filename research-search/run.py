"""Crossref + PubMed + ClinicalTrials.gov in one search.
Usage: APIFY_TOKEN=... python run.py   (pip install apify-client first)
"""
import os

from apify_client import ApifyClient

token = os.environ.get("APIFY_TOKEN")
if not token:
    raise SystemExit("Set the APIFY_TOKEN environment variable.")

client = ApifyClient(token)
run_input = {
    "mode": "all",
    "query": "CRISPR gene therapy",
    "maxResultsPerSource": 5
}

run = client.actor("datawharf-tools/research-search").call(run_input=run_input)
items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
for row in items:
    print(" | ".join(str(row.get(k, ""))[:60] for k in ["source", "id", "date", "title", "url"]))
print(f"{len(items)} rows, run {run['id']}")
