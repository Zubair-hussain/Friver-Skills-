#!/usr/bin/env python3
"""Detect changes to the official Fiverr Help Center policy sources.

The script records normalized article hashes only; it does not copy article text
or silently rewrite operational rules. CI opens a review PR whenever a hash
changes, keeping policy changes visible and auditable.
"""
import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from html.parser import HTMLParser
from urllib.request import Request, urlopen


class ArticleText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.depth = 0
        self.found_article = False
        self.skip = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "svg", "nav", "footer"):
            self.skip += 1
        if tag == "article":
            self.found_article = True
            self.depth += 1
        elif self.depth:
            self.depth += 1

    def handle_endtag(self, tag):
        if tag in ("script", "style", "svg", "nav", "footer") and self.skip:
            self.skip -= 1
        if self.depth:
            self.depth -= 1

    def handle_data(self, data):
        if not self.skip and self.depth:
            self.parts.append(data)


def normalized_article_text(html):
    parser = ArticleText()
    parser.feed(html)
    text = " ".join(parser.parts)
    return re.sub(r"\s+", " ", text).strip()


def fetch(url, timeout=30):
    request = Request(url, headers={
        "User-Agent": "fiverr-gig-optimizer-policy-monitor/1.0",
        "Accept": "application/json",
    })
    with urlopen(request, timeout=timeout) as response:
        return response.read().decode(response.headers.get_content_charset() or "utf-8", "replace")


def main(argv=None):
    here = os.path.dirname(os.path.abspath(__file__))
    references = os.path.abspath(os.path.join(here, "..", "references"))
    parser = argparse.ArgumentParser(description="Check official Fiverr policy pages for changes.")
    parser.add_argument("--rules", default=os.path.join(references, "policy-rules.json"))
    parser.add_argument("--state", default=os.path.join(references, "policy-source-state.json"))
    args = parser.parse_args(argv)

    with open(args.rules, encoding="utf-8") as fh:
        rules = json.load(fh)
    try:
        with open(args.state, encoding="utf-8") as fh:
            previous = json.load(fh)
    except FileNotFoundError:
        previous = {"sources": {}}

    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    next_sources, changed = {}, []
    for source in rules["sources"]:
        payload = json.loads(fetch(source.get("api_url", source["url"])))
        body = payload.get("article", {}).get("body", "")
        text = normalized_article_text(f"<article>{body}</article>")
        if len(text) < 200:
            raise RuntimeError(f"Could not extract policy article: {source['url']}")
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        old = previous.get("sources", {}).get(source["id"], {})
        first_seen = old.get("first_seen_at", now)
        next_sources[source["id"]] = {
            "url": source["url"], "sha256": digest,
            "first_seen_at": first_seen,
            "changed_at": now if old.get("sha256") != digest else old.get("changed_at", first_seen),
        }
        if old.get("sha256") != digest:
            changed.append(source["id"])

    if not changed:
        print("No official policy source changes detected.")
        return 0
    state = {"schema_version": 1, "sources": next_sources}
    with open(args.state, "w", encoding="utf-8") as fh:
        json.dump(state, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print("Changed policy sources: " + ", ".join(changed))
    print("Review the linked pages and update policy-rules.json when required.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
