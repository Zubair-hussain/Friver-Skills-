# Testing and Coverage

The quality gate covers the supported deterministic optimizer core with branch
coverage enabled. Deprecated marketplace-network adapters and optional external
service clients are tested separately but are excluded from the core percentage
because they are not part of the supported runtime path.

```bash
python -m coverage erase
python -m coverage run -m pytest -q
python -m coverage report -m
python -m coverage json
python -m coverage html
```

`.coveragerc` enforces `fail_under = 90`. The current verified result is recorded
under [`records/coverage`](../../records/coverage/README.md).

Coverage is a regression indicator, not proof of correctness. Tests prioritize:

- deterministic scoring and pricing boundaries;
- no-data and low-confidence paths;
- policy validation failures and warnings;
- atomic persistence and corruption preservation;
- renderer safety and valid generated output;
- CLI success and failure contracts.
