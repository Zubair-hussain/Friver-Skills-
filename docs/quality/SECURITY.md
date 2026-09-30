# Security

## Supported security posture

- Never provide or store Fiverr passwords, cookies, or session tokens.
- Marketplace scraping and automatic profile import are disabled.
- Community uploads are explicit, token-gated, allow-list filtered, and can be
  previewed with `--dry-run`.
- Secrets belong in environment variables or repository secret stores, never in
  tracked files.
- Generated catalog JSON is escaped before script embedding, and header values
  are HTML-escaped.
- Local data writes are atomic; corrupt and overwritten files are preserved.
- Policy changes and dependency updates arrive as reviewable pull requests.

## Reporting

Do not open a public issue containing credentials or personal data. Report the
minimum reproduction needed, redact all seller information, and rotate any token
that may have been exposed.
