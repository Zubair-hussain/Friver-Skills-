# Test Evidence

`junit.xml` is produced by:

```bash
python -m pytest -q --junitxml=records/test-results/junit.xml
```

CI systems can ingest this file directly. A new run replaces the record rather
than appending unverifiable prose.
