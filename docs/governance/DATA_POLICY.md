# Data Policy

This skill handles **only user-supplied or licensed Fiverr listing metadata**.
It stores no private user account data and does not support automated Fiverr
marketplace scraping.

## What is handled

When you import or contribute data, only listing metadata is processed. The
canonical record (PRD §7.1) is:

`scraped_at, category, subcategory, title, seller_level, seller_country,
rating, review_count, basic_price, standard_price, premium_price,
basic_delivery_days, standard_delivery_days, premium_delivery_days, tags,
gig_count_in_search, currency, original_currency`.

`seller_country` is a coarse market signal (a country code) kept for regional
pricing analysis. It is *not* tied to a username, profile, or any other
identifier — those are always stripped (below) — so a row cannot be traced back
to a specific seller.

## What is kept vs stripped on contribution

Contribution is **opt-in** and defaults to nothing. When you contribute,
`contribute.py` rebuilds every row from the keep-list above and **drops** all
seller-identifying fields before anything leaves your machine:

**Dropped (hard requirement):** seller username, seller display name, profile
URL, gig URL, seller profile URL, profile photo URL, any free-text review
content, any image URLs, any ID fields.

A PII guard (`assert_no_pii`) runs before any upload and aborts if a non-keep
field is present. Use `contribute.py --dry-run` to inspect the exact cleaned,
deduplicated records first.

## License

Contributed data and all documentation are released under **CC-BY-4.0**
(`LICENSE-DATA`). Code is **MIT** (`LICENSE`). By contributing you agree to
release your anonymized rows under CC-BY-4.0. Contributors are credited in
`CONTRIBUTORS.md`.

## Supported collection methods

Use counts copied from your own browser session, data you exported yourself, or
a dataset whose license permits your use. Legacy scraper code is retained only
for test fixtures and historical compatibility; its network entry points are
disabled in the supported 2026 workflow.

## No account data

The skill never asks for, stores, or transmits your Fiverr login, password, or
any private account information. Never paste those values into a config file.
