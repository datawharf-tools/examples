# Datawharf Actor examples

Small, runnable examples for the Datawharf Tools Actors on Apify. Each folder has the same example in JavaScript (`run.mjs`) and Python (`run.py`) using the official Apify API client. Tokens and keys are read from environment variables; nothing is stored in the repo.

| Folder | Actor | Needs |
|---|---|---|
| `sec-edgar/` | [SEC EDGAR filings and XBRL data](https://apify.com/datawharf-tools/sec-edgar-api) | Apify token |
| `sam-gov/` | [SAM.gov contract opportunities](https://apify.com/datawharf-tools/sam-gov-opportunities) | Apify token (SAM.gov key optional) |
| `eu-ted/` | [EU TED tenders](https://apify.com/datawharf-tools/eu-ted-tenders) | Apify token |
| `research-search/` | [Crossref, PubMed and ClinicalTrials.gov search](https://apify.com/datawharf-tools/research-search) | Apify token |
| `youtube/` | [YouTube Data API v3 client](https://apify.com/datawharf-tools/youtube-data-api) | Apify token + your own Google API key |
| `diy/` | Free standard-library Python scripts that call the public APIs directly (no Apify) | see each file |
| `mcp/` | Calling the Actors from an MCP client | Apify token |

## Setup

```bash
git clone <this repo> && cd <this repo>
export APIFY_TOKEN=...            # Apify Console > Settings > API & Integrations
npm install                       # JavaScript examples
pip install -r requirements.txt   # Python examples
node sec-edgar/run.mjs            # or: python sec-edgar/run.py
```

## Cost

The Actors bill per result row (about $0.34 to $0.40 per 1,000 rows) plus a small per-run start fee and standard Apify platform usage. The default inputs here return 5 to 20 rows. Apify's free monthly credit covers many runs; check your plan. Set a maximum charge per run in the Apify Console if you want a hard cap.

## Notes

- These Actors read official public APIs. They are not affiliated with or endorsed by the SEC, GSA/SAM.gov, the EU Publications Office/TED, Crossref, NLM/NIH or YouTube/Google.
- The `diy/` scripts need no Apify account. The SEC and research scripts ask for a contact string or email because those services require an identifying User-Agent.
- Not investment, legal or medical advice.

## Licence

MIT, see `LICENSE`.
