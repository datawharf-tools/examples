// IT-services contract notices from German and French buyers (last 30 days).
// Usage: APIFY_TOKEN=... node run.mjs   (npm install apify-client first)
import { ApifyClient } from 'apify-client';

const token = process.env.APIFY_TOKEN;
if (!token) throw new Error('Set the APIFY_TOKEN environment variable.');

const client = new ApifyClient({ token });
const input = {
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
};

const run = await client.actor('datawharf-tools/eu-ted-tenders').call(input);
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.table(items.map((r) => Object.fromEntries(["noticeId", "buyerCountry", "publicationDate", "deadline", "title"].map((k) => [k, String(r[k] ?? '').slice(0, 60)]))));
console.log(`${items.length} rows, run ${run.id}`);
