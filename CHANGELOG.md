# Changelog

## [0.6.1]

### Changed

- Mode announcements are optional when they do not help explain the work.
- When the original incident cannot be reproduced, an evidenced contract
  violation may be corrected only with regression coverage. Guessing a fix or
  claiming unverified behavior remains prohibited.

### Verification

A small paired execution pilot found no scope or verification violations in the
tested cases. It did not establish an isolated coding-posture quality, cost, or
latency improvement. Automatic skill activation and long tasks remain unverified.

[Changes since v0.6.0](https://github.com/alexei-led/coding-posture/compare/v0.6.0...v0.6.1)

## [0.6.0]

### Summary

Coding-posture owns general execution procedures. Review rubrics, test-design techniques, language guidance, and report templates remain optional companion guidance.

### Changes

- Route by requested action: an authorized auth fix remains an implementation task with stronger evidence requirements.
- Require evidence before patching, diagnose new failures before another patch, and report missing reproduction or test seams honestly.
- Keep reviews scoped and findings-only unless edits were authorized; separate confirmed defects from uncertainty.
- Validate RED's failure reason, establish behavior baselines before refactoring, and compare performance under comparable workloads.
- Permit redundant-test removal when behavior coverage is preserved; continue prohibiting hidden failures, weakened gates, and fabricated verification.
- Respect read-only scope and existing authorization; finish the requested work without adding cleanup or repeated checks after completion.
- Expand answer evals and add disposable execution fixtures, informed by current model guidance. No model-specific variants or new quality score.
- Use an installed eval runner, fresh temporary inputs, and configurable model parameters; default to GPT-6.1 Sol at medium effort. Exclude local settings from packages.

### Upgrade

Replace older copies of `always-on-snippet.md` after updating. Otherwise copied instructions can retain the old blanket test-deletion rule.

Mode names and installation paths are unchanged. No cc-thingz skills are changed or removed by this release; overlapping descriptions in older cc-thingz versions require a separate update there. Coding-posture needs no companion installation.

For eval automation, `SKILL_EVAL_CLI` must name one installed executable. `SKILL_EVAL_ROOT` now names a parent directory, never cleared by the script. Supply a compatible `SKILL_EVAL_CONFIG` when changing model/provider.

[Changes since v0.5.0](https://github.com/alexei-led/coding-posture/compare/v0.5.0...v0.6.0)
