#!/usr/bin/env python3
"""Validate a generated gig catalog against the reviewed Fiverr rule snapshot.

This is a deterministic preflight check, not a promise of Fiverr approval.
Rules are sourced from references/policy-rules.json and carry a review date.
"""
import argparse
import json
import os
import re
import sys
from datetime import date


def default_rules_path():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(here, "..", "references", "policy-rules.json")


def load_rules(path=None):
    with open(path or default_rules_path(), encoding="utf-8") as fh:
        return json.load(fh)


def _words(value):
    return re.findall(r"[A-Za-z0-9]+(?:['’-][A-Za-z0-9]+)?", value or "")


def _revision_count(value):
    if isinstance(value, (int, float)):
        return value
    match = re.search(r"\d+", str(value or ""))
    return int(match.group()) if match else None


def validate_gig(gig, rules):
    limits = rules["gig"]
    errors, warnings = [], []
    title = str(gig.get("title") or "").strip()
    desc = str(gig.get("desc") or "").strip()
    tags = gig.get("tags") or []
    gid = gig.get("id", "?")

    if not title.lower().startswith(limits["title_prefix"].lower()):
        errors.append(f"gig {gid}: title must start with '{limits['title_prefix']}'")
    if len(title) > limits["title_max_chars"]:
        errors.append(f"gig {gid}: title is {len(title)} characters; max is {limits['title_max_chars']}")
    used = [c for c in limits.get("title_avoid_characters", []) if c in title]
    if used:
        warnings.append(f"gig {gid}: title uses discouraged character(s): {' '.join(used)}")

    if not isinstance(tags, list):
        errors.append(f"gig {gid}: tags must be a list")
    elif not limits["tags_min"] <= len(tags) <= limits["tags_max"]:
        errors.append(f"gig {gid}: use {limits['tags_min']}–{limits['tags_max']} tags; found {len(tags)}")
    if len(desc) > limits["description_max_chars"]:
        errors.append(f"gig {gid}: description is {len(desc)} characters; max is {limits['description_max_chars']}")

    pricing = gig.get("pricing") or {}
    if len(pricing) > limits["packages_max"]:
        errors.append(f"gig {gid}: at most {limits['packages_max']} packages are allowed")
    for tier, package in pricing.items():
        price = package.get("price")
        if isinstance(price, (int, float)) and price < limits["minimum_price_usd"]:
            errors.append(f"gig {gid}: {tier} price is below ${limits['minimum_price_usd']}")
        revisions = _revision_count(package.get("rev"))
        if revisions is not None and revisions < limits["minimum_revisions"]:
            errors.append(f"gig {gid}: {tier} must include at least one revision")

    img = gig.get("img") or {}
    image_copy = " ".join(str(img.get(k) or "") for k in ("headline", "sub", "badge"))
    count = len(_words(image_copy))
    if count > limits["image_text_max_words"]:
        warnings.append(f"gig {gid}: image copy has {count} words; Fiverr recommends at most {limits['image_text_max_words']}")
    if re.search(r"\bfiverr\b", image_copy, re.I):
        errors.append(f"gig {gid}: do not place Fiverr branding or badges in a Gig image")

    risky = (
        (r"\bguarantee(?:d)?\b", "avoid guaranteed-result claims"),
        (r"(?:[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}|\b(?:whatsapp|telegram)\b)",
         "remove contact details or off-platform messaging"),
    )
    for pattern, message in risky:
        if re.search(pattern, f"{title}\n{desc}", re.I):
            warnings.append(f"gig {gid}: {message}")
    return errors, warnings


def validate_catalog(config, rules=None):
    rules = rules or load_rules()
    errors, warnings = [], []
    for gig in config.get("gigs") or []:
        gig_errors, gig_warnings = validate_gig(gig, rules)
        errors.extend(gig_errors)
        warnings.extend(gig_warnings)
    if not config.get("gigs"):
        errors.append("catalog: at least one gig is required")
    reviewed = date.fromisoformat(rules["reviewed_at"])
    age_days = (date.today() - reviewed).days
    if age_days > rules.get("review_due_after_days", 90):
        warnings.append(
            f"policy snapshot is {age_days} days old; review the official sources"
        )
    return {
        "valid": not errors,
        "policy_reviewed_at": rules["reviewed_at"],
        "checked_at": date.today().isoformat(),
        "errors": errors,
        "warnings": warnings,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate gig-config.json against reviewed Fiverr rules.")
    parser.add_argument("config")
    parser.add_argument("--rules", help="Override policy-rules.json path.")
    parser.add_argument("--out", help="Optional path for the JSON report.")
    args = parser.parse_args(argv)
    with open(args.config, encoding="utf-8") as fh:
        config = json.load(fh)
    report = validate_catalog(config, load_rules(args.rules))
    rendered = json.dumps(report, indent=2, ensure_ascii=False)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as handle:
            handle.write(rendered + "\n")
    else:
        print(rendered)
    return 0 if report["valid"] else 2


if __name__ == "__main__":
    sys.exit(main())
