# Validation Evidence

`sample-gig-policy.json` records the deterministic preflight result for the
tracked sample configuration. Regenerate it with:

```bash
python skills/fiverr-gig-optimizer/scripts/validate_gig.py examples/sample-gig-config.json --out records/validation/sample-gig-policy.json
```

The official policy source fingerprints are tracked separately in
`skills/fiverr-gig-optimizer/references/policy-source-state.json`.
