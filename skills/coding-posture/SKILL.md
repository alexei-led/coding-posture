---
name: coding-posture
description: General execution procedures for non-trivial coding work — debug, fix, review, test-first, refactor, optimize, migrate, upgrade, integrate, spike, or unstuck. Pick a mode and follow its checklist. Not needed for trivial one-line edits or non-coding tasks. Specialist review rubrics, test-design techniques, and language guidance remain with their domain skills.
license: MIT
metadata:
  tags: [coding-agent, posture, mode, risk, verification]
---

# Coding Posture

Pick a working mode that fits the task and follow its checklist. Modes are procedures, not personas. This skill owns the general execution loop; it works without companion skills.

## How to use

1. Pick the mode matching the requested action. If none fit, proceed normally — "no mode" is valid. Test work uses the same modes: test review, test refactor, suite optimization, or test-first implementation.
2. Ask only when missing information materially changes the result or authorization; otherwise state a reasonable assumption and proceed.
3. State the mode when it helps the user understand the work.
4. Follow its checklist. Switch modes when the work changes, such as debug → fix after diagnosis. Sensitive code needs stronger evidence; an authorized auth fix does not become a findings-only review.
5. Load specialist guidance only when its review rubric, test-design technique, language detail, or requested report format helps. For example, cc-thingz's reviewing-code and improving-tests supply detail; do not require them for every task or repeat their execution checklists.
6. A mode never overrides user, project, or safety instructions and grants no additional authorization.

Priority: `system/safety > user instruction > project rules > task plan > mode > style`

## Always (every mode)

- Stay within authorized scope and preserve unrelated changes. Read-only requests permit analysis and proposals only. Ask before expanding into unrelated failures, destructive git/deploy/data actions, or sharing private code externally; reuse authorization already given for that scope. Inspect state before mutating.
- Never suppress failures, bypass hooks, lower check severity, or hard-code test answers to manufacture success. Clear caches only when evidence identifies stale state as the cause.
- Never weaken or remove checks merely to hide a failure or improve a metric. Remove redundant tests only when retained or replacement coverage preserves the intended behavior.
- Finish the authorized work, then stop after verification. Do not add unrequested cleanup, tooling, or review rounds. If blocked, name the missing artifact, access, or approval.

## The loop that works

**Gather context → localize → smallest change → run the real check → read the actual output.**

- Establish the relevant baseline before editing. Use the narrowest reliable check during iteration, then run the project's relevant build/test/lint/type checks. Keep required browser, race, integration, or other checks when they exercise the affected behavior.
- Repeat or broaden checks only after changes, failures, or unresolved concerns. Re-reading code and syntax-only checks do not establish behavior correctness.
- Report what changed or was found, supporting evidence, and which checks passed, failed, or did not run and why. Distinguish confirmed results from hypotheses and unverified behavior; a blocker or failing gate is not successful verification. Use a specialist report format only when needed.

## Modes

### debug — unknown cause of a failure

- Establish a reliable failing signal when feasible: a test, command, replay, or trace through the real path. Record the command and observed failure.
- If reproduction is unavailable, collect existing evidence and name the gap. Patch only an evidenced contract violation with regression coverage; do not patch a guess or claim reproduction succeeded.
- Trace the failure to the first bad state or contract mismatch, with file/line evidence. For unclear or intermittent failures, rank falsifiable hypotheses and test one at a time.

### fix — known cause or scoped correction

- Use the established failure evidence; diagnose first if the cause is unknown. Keep the patch as small as the problem allows, without adjacent cleanup.
- Avoid dependency/config changes unless required.
- Verify the original failing signal when available and add regression coverage at the affected behavior boundary where practical. Report a missing repro or test seam rather than substituting a helper test that misses the bug.
- If the patch causes a new failure, diagnose it before another patch. Remove temporary probes or promote them to real tests; state residual risk.

### review — findings on a diff, files, or tests

- Produce findings unless edits were authorized. Establish the requested scope; ask if its target is ambiguous. Report an empty scope rather than inventing work.
- Read enough surrounding code, callers, and affected tests to support each finding with a location and failure scenario. Tool or graph output is evidence only when relevant and current.
- Separate confirmed defects, severity, and uncertainty. State coverage gaps; keep unrelated suspicions out of the requested scope. Domain rubrics and report templates belong to specialist guidance.

### test-first — behavior change where a test is practical

- Work one requested behavior slice at a time; write or identify its test first.
- Run it before implementing and confirm RED is caused by the intended missing behavior. Setup, import, or syntax errors do not establish RED.
- Make the smallest passing change. Do not build bulk suites for imagined behavior.
- Refactor only while tests stay green.

### refactor — cleanup, simplify, rename, remove dead code

- Establish a behavior baseline before editing; preserve behavior rather than mixing in functional changes. If existing checks miss the affected behavior, add characterization coverage first or report the gap.
- Delete complexity before adding abstraction.
- Before removing code, trace call sites, feature flags, tests, and docs — "unused in this file" does not mean safe to delete.
- Check equivalence against the baseline with tests or golden output; state remaining coverage limits.
- Keep diffs reviewable.

### optimize — performance work, slow path, hot loop

- Measure first: profile or benchmark to find the real hotspot. Do not optimize what merely looks expensive.
- Record a baseline before changing anything; compare the same command and workload under comparable conditions after. Name the measured bottleneck and retain a repeatable check for regression.
- Change one thing at a time and keep correctness tests green.
- Prefer the smallest change that moves the measured number; stop when the target is met.

### migrate — schema, data, or infra change (terraform, k8s, migrations)

- Identify the backup and rollback path before touching stateful systems.
- Prefer staged, reversible changes.
- Validate against a non-production target first when possible.
- Document operational risk and recovery steps.

### upgrade — dependency or library version bump

- Read the changelog, release notes, or migration guide for breaking changes before editing.
- Account for transitive dependencies and the lockfile, not just the named package.
- Update the call sites the breaking changes require; do not blind search-and-replace.
- Run the build and the full suite. Keep a rollback path for the version, lockfile, and required call-site changes together.

### integrate — calling an external API, service, or tool

- Read the contract; do not infer behavior from the name or a single sample call.
- Validate request and response schemas; handle auth failure, timeouts, retries, rate limits, pagination, and empty or partial responses.
- Treat the dependency as untrusted: check status and errors, never assume success.
- Test the error paths, not just the happy path.

### spike — prototype, proof-of-concept, unknown library

- Keep spike artifacts isolated from production paths.
- Optimize for learning speed, not polish.
- Do not wire experimental code into production without review.
- End with a verdict — validated, invalidated, or unclear — and list what productionizing would require.

### unstuck — repeated failures, thrashing, "still failing"

- Stop making speculative edits.
- Summarize what you tried and the evidence each attempt produced.
- Rank the remaining hypotheses and choose a check that would discriminate them.
- Collect missing information before changing more code.
- Consider delegating a fresh review.
