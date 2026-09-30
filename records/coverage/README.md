# Coverage Evidence

Regenerate with:

```bash
python -m coverage erase
python -m coverage run -m pytest -q
python -m coverage report -m
python -m coverage json
python -m coverage html
```

The enforced threshold is 90% branch-aware coverage of the supported optimizer
core. `coverage.json` is machine-readable; `html/index.html` is the browsable
line-by-line report.
