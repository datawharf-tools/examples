"""Annual revenue and net income for two tickers from 10-K filings.
Usage: APIFY_TOKEN=... python run.py   (pip install "apify-client>=3" first)
"""
import os

from apify_client import ApifyClient

token = os.environ.get("APIFY_TOKEN")
if not token:
    raise SystemExit("Set the APIFY_TOKEN environment variable.")

client = ApifyClient(token)
run_input = {
    "mode": "companyFacts",
    "companies": [
        "AAPL",
        "MSFT"
    ],
    "concepts": [
        "RevenueFromContractWithCustomerExcludingAssessedTax",
        "NetIncomeLoss"
    ],
    "forms": [
        "10-K"
    ],
    "fiscalPeriod": "FY",
    "userAgent": "YOUR NAME your@email.com",
    "maxResultsPerCompany": 6,
    "maxResults": 20
}

run = client.actor("datawharf-tools/sec-edgar-api").call(run_input=run_input)
items = list(client.dataset(run.default_dataset_id).iterate_items())
for row in items:
    print(" | ".join(str(row.get(k, ""))[:60] for k in ["ticker", "concept", "periodEnd", "value", "form"]))
print(f"{len(items)} rows, run {run.id}")
