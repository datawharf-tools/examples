"""Annual revenue from SEC EDGAR XBRL, standard library only.
Set SEC_CONTACT to "Your Name you@example.com" (the SEC requires an identifying User-Agent).
Usage: SEC_CONTACT="Jane Doe jane@example.com" python sec_revenue.py AAPL
"""
import datetime
import json
import os
import sys
import urllib.request

UA = os.environ.get("SEC_CONTACT")
if not UA:
    raise SystemExit('Set SEC_CONTACT to "Your Name you@example.com".')
REVENUE_CONCEPTS = ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues", "SalesRevenueNet"]


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def cik_for(ticker):
    for row in get("https://www.sec.gov/files/company_tickers.json").values():
        if row["ticker"].upper() == ticker.upper():
            return str(row["cik_str"]).zfill(10)
    raise ValueError(f"unknown ticker {ticker}")


def _d(s):
    return datetime.date.fromisoformat(s)


def annual_revenue(ticker):
    gaap = get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik_for(ticker)}.json")["facts"]["us-gaap"]
    for concept in REVENUE_CONCEPTS:
        if concept not in gaap:
            continue
        best = {}
        points = sorted(gaap[concept]["units"]["USD"], key=lambda p: p["filed"])
        for p in points:
            if p["form"] != "10-K" or p["fp"] != "FY" or not p.get("start"):
                continue
            if not 350 <= (_d(p["end"]) - _d(p["start"])).days <= 380:  # full-year periods only
                continue
            best.setdefault(p["end"], {"ticker": ticker, "concept": concept, "end": p["end"],
                                       "value": p["val"], "accn": p["accn"], "filed": p["filed"]})
        if best:
            return [best[k] for k in sorted(best)]
    return []


if __name__ == "__main__":
    for r in annual_revenue(sys.argv[1] if len(sys.argv) > 1 else "AAPL")[-5:]:
        print(r)
