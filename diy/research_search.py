"""Crossref + PubMed + ClinicalTrials.gov search, standard library only.
Usage: CONTACT_EMAIL=you@example.com python research_search.py "CRISPR gene therapy"
"""
import json
import os
import sys
import urllib.parse
import urllib.request

EMAIL = os.environ.get("CONTACT_EMAIL")
if not EMAIL:
    raise SystemExit("Set CONTACT_EMAIL (Crossref and NCBI ask for a contact address).")


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": f"research-example (mailto:{EMAIL})"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def crossref(q, n=5):
    url = "https://api.crossref.org/works?" + urllib.parse.urlencode({"query": q, "rows": n, "mailto": EMAIL})
    return [{"source": "crossref", "id": w.get("DOI"), "title": (w.get("title") or [""])[0]}
            for w in get(url)["message"]["items"]]


def pubmed(q, n=5):
    base = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
    common = {"tool": "research-example", "email": EMAIL}
    ids = get(base + "esearch.fcgi?" + urllib.parse.urlencode({**common, "db": "pubmed", "term": q, "retmax": n, "retmode": "json"}))["esearchresult"]["idlist"]
    if not ids:
        return []
    summ = get(base + "esummary.fcgi?" + urllib.parse.urlencode({**common, "db": "pubmed", "id": ",".join(ids), "retmode": "json"}))["result"]
    return [{"source": "pubmed", "id": i, "title": summ[i].get("title")} for i in ids]


def trials(q, n=5):
    url = "https://clinicaltrials.gov/api/v2/studies?" + urllib.parse.urlencode({"query.term": q, "pageSize": n})
    return [{"source": "clinicaltrials", "id": s["protocolSection"]["identificationModule"]["nctId"],
             "title": s["protocolSection"]["identificationModule"].get("briefTitle")} for s in get(url).get("studies", [])]


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    query = " ".join(sys.argv[1:]) or "CRISPR gene therapy"
    for fn in (crossref, pubmed, trials):
        for row in fn(query):
            print(row)
