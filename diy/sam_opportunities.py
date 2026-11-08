"""SAM.gov Opportunities API, standard library only. Needs your own free key in SAM_API_KEY.
Usage: SAM_API_KEY=... python sam_opportunities.py
"""
import os
import csv
import json
import urllib.parse
import urllib.request
from datetime import date, timedelta

API_KEY = os.environ.get("SAM_API_KEY")
if not API_KEY:
    raise SystemExit("Set SAM_API_KEY (your own free SAM.gov key).")
BASE = "https://api.sam.gov/prod/opportunities/v2/search"


def fmt(d):
    return d.strftime("%m/%d/%Y")  # the API wants MM/dd/yyyy


def search(**params):
    params["api_key"] = API_KEY
    url = BASE + "?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=30) as r:
        return json.load(r)


def fetch_all(ncode, set_aside, ptype="o", days=30, page_size=1000, max_pages=3):
    today = date.today()
    base = {
        "postedFrom": fmt(today - timedelta(days=days)),  # window must be 1 year or less
        "postedTo": fmt(today),
        "ncode": ncode,
        "typeOfSetAside": set_aside,
        "ptype": ptype,
        "limit": page_size,
    }
    rows = []
    for page in range(max_pages):  # each page is one request against your daily quota
        res = search(**base, offset=page)  # offset is the page index, starting at 0
        items = res.get("opportunitiesData") or []
        rows.extend(items)
        if len(items) < page_size or len(rows) >= res.get("totalRecords", 0):
            break
    return rows


if __name__ == "__main__":
    notices = fetch_all("541512", "SBA")
    with open("opportunities.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["noticeId", "title", "agency", "posted", "deadline", "setAside", "naics", "link"])
        for o in notices:
            w.writerow([
                o.get("noticeId"), o.get("title"), o.get("fullParentPathName"),
                o.get("postedDate"), o.get("responseDeadLine"),
                o.get("typeOfSetAsideDescription"), o.get("naicsCode"), o.get("uiLink"),
            ])
    print(len(notices), "notices written")
