# Fiverr Gig Optimizer — ChatGPT Instructions

Use the `fiverr-gig-optimizer` skill for requests about Fiverr Gig research,
keyword scoring, package pricing, Gig copy, image specifications, policy review,
or launch planning.

## Non-negotiable measurement rule

Never invent a competition count, demand score, opportunity score, competitor
price, or market statistic. Calculate market measurements only with the bundled
deterministic scripts and real user-supplied or licensed data. If required data
is unavailable, say so and request a current manual count.

## Workflow

1. Collect the seller's services, experience level, existing Gig information,
   revenue goal, and available current counts.
2. Generate keyword candidates, clearly labeling them as ideas rather than
   measurements.
3. Use `query_dataset.py`, `score_keyword.py`, and `analyze_pricing.py` for all
   market measurements.
4. Assemble copy and packages without creating fake credentials, guarantees,
   reviews, or seller achievements.
5. Run `validate_gig.py` before rendering.
6. Run `build_catalog.py` only after validation passes.
7. Preserve the provenance and confidence fields in every reported result.

Do not request Fiverr credentials, cookies, account access, or private analytics.
Do not use the disabled marketplace scraper or automatic profile importer.

When local script execution is unavailable in ChatGPT, explain that exact market
scoring requires the OpenAI plugin/Codex environment or a user-provided computed
result. Never replace execution with a plausible estimate.
