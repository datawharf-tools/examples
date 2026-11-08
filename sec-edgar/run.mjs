// Annual revenue and net income for two tickers from 10-K filings.
// Usage: APIFY_TOKEN=... node run.mjs   (npm install apify-client first)
import { ApifyClient } from 'apify-client';

const token = process.env.APIFY_TOKEN;
if (!token) throw new Error('Set the APIFY_TOKEN environment variable.');

const client = new ApifyClient({ token });
const input = {
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
};

const run = await client.actor('datawharf-tools/sec-edgar-api').call(input);
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.table(items.map((r) => Object.fromEntries(["ticker", "concept", "periodEnd", "value", "form"].map((k) => [k, String(r[k] ?? '').slice(0, 60)]))));
console.log(`${items.length} rows, run ${run.id}`);
