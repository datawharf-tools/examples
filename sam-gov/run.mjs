// Recent software solicitations. Runs without a SAM.gov key (daily public file).
// Usage: APIFY_TOKEN=... node run.mjs   (npm install apify-client first)
import { ApifyClient } from 'apify-client';

const token = process.env.APIFY_TOKEN;
if (!token) throw new Error('Set the APIFY_TOKEN environment variable.');

const client = new ApifyClient({ token });
const input = {
    "keywords": ["software"],
    "noticeTypes": ["o", "k"],
    "maxResults": 10
};

const run = await client.actor('datawharf-tools/sam-gov-opportunities').call(input);
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.table(items.map((r) => Object.fromEntries(["postedDate", "responseDeadline", "title", "agency"].map((k) => [k, String(r[k] ?? '').slice(0, 60)]))));
console.log(`${items.length} rows, run ${run.id}`);
