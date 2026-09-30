# Release Checklist

- [ ] Confirm the working tree contains only intended changes.
- [ ] Run the 90% branch-coverage quality gate.
- [ ] Regenerate JUnit, coverage, and sample-policy records.
- [ ] Run `git diff --check`.
- [ ] Verify all local Markdown links and SVGs.
- [ ] Confirm no credentials, cookies, `.env` files, or local datasets are staged.
- [ ] Review official policy-source changes before changing rules.
- [ ] Validate `examples/sample-gig-config.json` and render a smoke-test catalog.
- [ ] Review dependency update PRs and pin a release tag.
- [ ] Update the changelog/release notes with user-visible behavior only.
