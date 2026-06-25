# Coding Posture

- The product is one file: `skills/coding-posture/SKILL.md`. No engine, no selection code.
- Modes are procedural checklists, not personas. Keep them aimed at situations models reliably get wrong.
- A mode never overrides user/project/safety instructions.
- Keep `SKILL.md` scannable: short checklists, plain mode names, no persona theatrics. Enrich modes only with practices that have evidence behind them.

## Releasing

Bump the version in **all four** markers together, then tag `vX.Y.Z`:

- `package.json` → `version`
- `.claude-plugin/plugin.json` → `version`
- `.claude-plugin/marketplace.json` → `metadata.version`, `plugins[0].version`, and top-level `version`
- `.codex-plugin/plugin.json` → `version`

The Claude plugin only updates for installed users when `version` changes, so it must move on every release.

## Local setup

Enable the bundled secret-scan hooks once per clone: `git config --local core.hooksPath scripts/git-hooks` (requires `gitleaks`).
