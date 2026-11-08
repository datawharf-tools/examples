// Crossref + PubMed + ClinicalTrials.gov in one search.
// Usage: APIFY_TOKEN=... node run.mjs   (npm install apify-client first)
import { ApifyClient } from 'apify-client';

const token = process.env.APIFY_TOKEN;
if (!token) throw new Error('Set the APIFY_TOKEN environment variable.');

const client = new ApifyClient({ token });
const input = {
    "mode": "all",
    "query": "CRISPR gene therapy",
    "maxResultsPerSource": 5
};

const run = await client.actor('datawharf-tools/research-search').call(input);
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.table(items.map((r) => Object.fromEntries(["source", "id", "date", "title", "url"].map((k) => [k, String(r[k] ?? '').slice(0, 60)]))));
console.log(`${items.length} rows, run ${run.id}`);
