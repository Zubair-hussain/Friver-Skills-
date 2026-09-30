# User Manual — Fiverr Gig Optimizer

This guide covers the supported, policy-aware workflow. The tool never needs
your Fiverr email, password, session cookie, or private analytics.

## 1. Requirements

- Python 3.9 or newer
- an agentic coding client that can load `skills/fiverr-gig-optimizer/SKILL.md`
- optional: Chrome or Edge for PDF output
- optional: `huggingface_hub` for your own community dataset

Install optional dependencies:

```bash
python -m pip install -r requirements.txt
```

## 2. Install from your repository

After publishing this code under your account:

```text
/plugin marketplace add YOUR_GITHUB_USERNAME/fiverr-gig-optimizer
/plugin install fiverr-gig-optimizer@fiverr-tools
```

## 3. Prepare your input

Provide your name or brand, at least three services, experience level, any
current Gig copy and packages, your revenue goal, and current Fiverr search
counts when available.

Do not provide account passwords or cookies. Existing profile data must be
pasted or exported by the account owner; automatic profile scraping is not part
of the supported workflow.

## 4. Choose a data path

Use the bundled sample:

```bash
python skills/fiverr-gig-optimizer/scripts/query_dataset.py --keyword "ai chatbot"
```

Or score a current count copied from your own browser session:

```bash
python skills/fiverr-gig-optimizer/scripts/score_keyword.py --keyword "ai chatbot" --gig-count 240
```

Or build local artifacts from JSON/CSV data you are allowed to use:

```bash
python skills/fiverr-gig-optimizer/scripts/build_benchmarks.py --csv rows.csv
```

Direct marketplace crawling, TLS impersonation, proxy-based scraping, and
automatic Fiverr profile import are not supported under the reviewed 2026 Terms.

## 5. Validate and render

```bash
python skills/fiverr-gig-optimizer/scripts/validate_gig.py gig-config.json
python skills/fiverr-gig-optimizer/scripts/build_catalog.py gig-config.json --out fiverr-catalog.html
```

The renderer stops on hard policy errors and prints softer risks as warnings.

## 6. Policy updates

Rules live in `skills/fiverr-gig-optimizer/references/policy-rules.json`. Check
the official sources with:

```bash
python skills/fiverr-gig-optimizer/scripts/sync_policy_sources.py
```

The weekly workflow opens a review PR when an official source changes. Review
the linked source before editing a rule; an unrelated wording change should not
silently change optimizer behavior.

## 7. Optional community data

Configure your own Hugging Face dataset URL in `scoring-config.json`, then
preview every outgoing row before any upload:

```bash
python skills/fiverr-gig-optimizer/scripts/contribute.py --input benchmarks.local.json --dry-run
```

Only proceed with a dedicated fine-grained `HF_TOKEN` if you intentionally want
to contribute. The script strips seller identity fields and never needs Fiverr
credentials.

## 8. Troubleshooting

- `no_match`: use a current manual count; do not guess.
- low-confidence pricing: add more lawful competitor-price observations.
- policy validation failure: fix the listed field before rendering.
- policy source changed: review the official page and update the rule snapshot.
- no dataset configured: set your own dataset URL or stay on local/sample data.
- no Chrome/Edge: use the HTML catalog; PDF output is optional.

Run the full test suite with `python -m pytest -q`.
