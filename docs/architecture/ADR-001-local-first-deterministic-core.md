# ADR-001: Local-first deterministic core

- Status: Accepted
- Date: 2026-09-30

## Context

The product reports market measurements that can affect seller decisions. Model-
generated estimates would be difficult to audit, while direct marketplace
automation conflicts with the supported compliance posture.

## Decision

Keep measurement and validation logic in deterministic local Python modules.
Accept only bundled, manual, or user-authorized data. Preserve provenance with
every result. Treat external policy monitoring as a change signal requiring
human review, not as executable configuration.

## Consequences

- Results are repeatable for the same input and configuration.
- Missing data cannot be disguised as certainty.
- Users must provide fresh counts when local data is insufficient.
- External integrations remain optional and explicit.
- Core logic can be covered by fast offline tests.
