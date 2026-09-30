# Repository Structure

```text
.
├── .github/                 CI, policy monitoring, dependency updates
├── assets/                  Social-preview and product imagery
├── docs/
│   ├── architecture/        Architecture diagram and decisions
│   ├── archive/             Superseded product requirements
│   ├── governance/          Contribution and data policies
│   ├── guides/              User-facing operating guides
│   ├── planning/            Launch and issue planning
│   ├── quality/             Testing, security, and release controls
│   └── wireframes/          UI and workflow wireframes
├── examples/                Safe sample input configurations
├── patterns/                Reusable community-dataset pattern
├── records/                 Reproducible quality evidence
├── skills/                  Skill instructions, rules, and scripts
├── tests/                   Automated offline test suite
├── AGENTS.md                Agent operating contract
├── README.md                Project entry point
└── LICENSE*                 Code and documentation licenses
```

Generated user data and catalogs stay ignored at the root. Evidence that is safe
to publish belongs under `records/`; product documentation belongs under `docs/`.
