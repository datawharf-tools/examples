"""Recent EU tenders from TED (Tenders Electronic Daily), keyless Search API v3.
Standard library only. Source: TED, Publications Office of the EU, CC BY 4.0.
"""
import csv
import json
import sys
import urllib.request

ENDPOINT = "https://api.ted.europa.eu/v3/notices/search"
FIELDS = ["publication-number", "notice-title", "buyer-name", "buyer-country",
          "classification-cpv", "notice-type", "publication-date",
          "deadline-receipt-tender-date-lot"]


def pick(value, prefer="eng"):
    """Titles and buyer names come as {language: [text, ...]}; prefer English."""
    if not isinstance(value, dict):
        return value
    for lang in (prefer, *value):
        v = value.get(lang)
        if v:
            return v[0] if isinstance(v, list) else v
    return None


def search(query, limit=10):
    body = json.dumps({"query": query, "fields": FIELDS, "limit": limit,
                       "paginationMode": "ITERATION"}).encode()
    req = urllib.request.Request(ENDPOINT, data=body, method="POST",
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


if __name__ == "__main__":
    # German buyers (DEU), CPV branch 72 (IT services), published since 1 Oct 2026, newest first
    sys.stdout.reconfigure(encoding="utf-8")
    q = ("publication-date>=20261001 AND buyer-country=DEU AND classification-cpv=72* "
         "SORT BY publication-number DESC")
    res = search(q, limit=5)
    print("total matching:", res.get("totalNoticeCount"))
    rows = []
    for n in res.get("notices", []):
        rows.append({
            "id": n["publication-number"],
            "date": (n.get("publication-date") or "")[:10],
            "title": pick(n.get("notice-title")),
            "buyer": pick(n.get("buyer-name")),
            "country": (n.get("buyer-country") or [None])[0],
            "type": n.get("notice-type"),
            "url": f"https://ted.europa.eu/en/notice/-/detail/{n['publication-number']}",
        })
    w = csv.DictWriter(sys.stdout, fieldnames=list(rows[0]) if rows else ["id"])
    w.writeheader()
    w.writerows(rows)
    # next page: pass res["iterationNextToken"] back as "iterationNextToken" in the body
