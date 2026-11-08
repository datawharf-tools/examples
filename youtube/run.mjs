// Video search. Needs your own YouTube Data API v3 key in YOUTUBE_API_KEY.
// Usage: APIFY_TOKEN=... node run.mjs   (npm install apify-client first)
import { ApifyClient } from 'apify-client';

const token = process.env.APIFY_TOKEN;
if (!token) throw new Error('Set the APIFY_TOKEN environment variable.');
const apiKey = process.env.YOUTUBE_API_KEY;
if (!apiKey) throw new Error('Set YOUTUBE_API_KEY (your own Google API key).');

const client = new ApifyClient({ token });
const input = {
    mode: "searchVideos",
    "query": "python tutorial",
    "maxResults": 10,
    apiKey,
};

const run = await client.actor('datawharf-tools/youtube-data-api').call(input);
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.table(items.map((r) => Object.fromEntries(["videoId", "title", "channelTitle", "publishedAt"].map((k) => [k, String(r[k] ?? '').slice(0, 60)]))));
console.log(`${items.length} rows, run ${run.id}`);
