# AGENTS.md — running fiverr-gig-optimizer from any agentic CLI

This repository contains an **OpenAI-compatible Agent Skill** plus a Claude Code
compatibility manifest. The workflow lives in
`skills/fiverr-gig-optimizer/SKILL.md` with deterministic Python scripts, so
ChatGPT plugin surfaces, Codex, Claude Code, and other Agent Skills clients can
use the same measured-data contract. This file is the repository entry point.

## The one rule you may never break

**The model never emits a market number.** Competition counts, demand signals, and
competitor pricing come **only** from the scripts below, run on real data. If the
data isn't there, you **ask the user or say you don't have it** — you never estimate,
average-in-your-head, or fill a gap with a plausible figure. Offer design (delivery
days, revisions, package contents) *is* yours to author; market measurements are not.

Every score you surface must keep its provenance line. This is the whole point of the
project — a fabricated number defeats it.

## How to run it

1. Read `skills/fiverr-gig-optimizer/SKILL.md` — it is the full operating procedure.
2. Interview the user for their services (or read a CV/portfolio they provide).
3. Produce numbers only via the deterministic scripts:

```bash
python skills/fiverr-gig-optimizer/scripts/score_keyword.py   # competition + opportunity
python skills/fiverr-gig-optimizer/scripts/query_dataset.py    # demand from sample/user-owned data
python skills/fiverr-gig-optimizer/scripts/analyze_pricing.py  # 3-tier pricing from competitor percentiles
python skills/fiverr-gig-optimizer/scripts/build_catalog.py gig-config.json --out fiverr-catalog.html
```

4. Render `fiverr-catalog.html` — the deliverable — with a provenance line under every score.

## Contract enforcement

`tests/` encodes the honesty and policy rules. If you change scoring, pricing, or
rendering, run `python -m coverage run -m pytest -q` and
`python -m coverage report -m`; both tests and the 90% supported-core gate must
stay green. A change that lets the model author a market number is a bug, not a feature.
