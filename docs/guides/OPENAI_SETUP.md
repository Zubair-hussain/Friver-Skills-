# ChatGPT and Codex Setup

This repository is packaged as an OpenAI plugin and an Agent Skill. The same
skill supplies the workflow to supported ChatGPT plugin surfaces and Codex.

## Codex

### Repository mode

Open this repository as the Codex working directory. Codex automatically reads
the root `AGENTS.md`, which directs it to the skill when the task concerns Fiverr
Gig optimization.

```bash
codex -C /path/to/fiverr-gig-optimizer
```

Example prompt:

```text
Use the fiverr-gig-optimizer skill to score these keywords from my pasted counts,
validate the Gig copy, and build the HTML catalog.
```

### Plugin mode

The repository root contains `.codex-plugin/plugin.json`. Import or install the
repository/ZIP as a plugin on a supported Codex surface, then select **Fiverr Gig
Optimizer** or explicitly ask Codex to use the `fiverr-gig-optimizer` skill.

Build a clean upload ZIP with:

```bash
python tools/build_openai_plugin.py
```

Upload `dist/fiverr-gig-optimizer-openai-plugin.zip` when the surface offers a
plugin ZIP import control.

## ChatGPT

### Supported plugin workspaces

Import the repository or its ZIP through your workspace's plugin creation flow.
After installation, start a new chat, type `@`, select **Fiverr Gig Optimizer**,
and provide your services plus real counts or a lawful dataset.

The plugin includes executable scripts. Availability of local execution and file
creation depends on the ChatGPT surface and workspace policy.

### ChatGPT projects or accounts without plugin import

Upload `chatgpt/INSTRUCTIONS.md` as project instructions/reference material,
then upload the specific configuration or dataset needed for the task. A normal
ChatGPT project does not automatically gain access to this local repository.

If that ChatGPT surface cannot execute the bundled Python scripts, it can help
with offer design and policy review, but it must not invent market measurements.
Use Codex or the plugin-enabled workflow for exact scoring and catalog builds.

## Verification prompts

Test these after installation:

1. `Explain where every market number is allowed to come from.`
2. `Validate examples/sample-gig-config.json and list any policy warnings.`
3. `Build a catalog from the sample config and tell me where it was written.`
4. `I have no current count for this keyword—what should you do?`

Expected behavior: the plugin uses deterministic scripts, preserves provenance,
refuses to guess missing market data, and never requests Fiverr credentials.

## Branding

The plugin uses `assets/plugin-logo.png`, an original FGO mark in a Fiverr-green
palette. It is intentionally not Fiverr's official logo. Upload
`assets/og-card.png` separately as the GitHub repository Social Preview.
