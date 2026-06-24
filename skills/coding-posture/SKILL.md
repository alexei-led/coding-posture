---
name: coding-posture
description: Use before non-trivial coding work to pick a task-appropriate working mode — debugging, fixing, reviewing, test-first, refactoring, migrating, spiking, or getting unstuck — then follow its checklist. Modes are procedures, not personas.
license: MIT
metadata:
  tags: [coding-agent, posture, mode, risk, verification]
---

# Coding Posture

Pick a working mode that fits the task, state it, and follow its checklist. A mode is a short procedure for a situation models tend to get wrong — not a role to play.

## How to use

1. Before non-trivial coding work, scan the modes and pick the one matching the task's dominant risk. If none fit, proceed normally — "no mode" is a valid choice.
2. If the task is underspecified in a way that changes the implementation, ask before coding — models rarely notice their own missing requirements, and one clarifying round is cheaper than the wrong build.
3. State the mode and a one-line reason.
4. Follow its checklist while planning and editing.
5. If the risk class changes mid-task (a "quick fix" turns out to touch auth), switch modes and say why.
6. A mode tunes _how_ you work. It never overrides instructions or authorizes unsafe actions.

Priority: `system/safety > user instruction > project rules > task plan > mode > style`

## Always (every mode)

- Never run destructive git/deploy/data commands — `force push`, `reset --hard`, `drop`, `delete`, `truncate`, `rm -rf` — without explicit scope. Inspect state before mutating.
- Verify by running the real check (test, build, repro), not by re-reading your own work. Re-checking without external feedback fixes some errors and introduces others — ground every claim of "done" in executed output.
- Never report a result you did not run, and never accept a check that does not exercise the case in question. A test that passes without touching the bug is not verification.
- Never weaken, delete, skip, or special-case a test — or hard-code an expected value — to turn it green. Solve the task, not the grader.

## The loop that works

The pattern with the strongest evidence behind it for coding agents: **gather context → localize → smallest change → run the real check → read the actual output → repeat.** Read the surrounding code and establish a baseline before editing — agents that rush to patch in the first few steps fail more often. Tight execution-feedback loops are where agents outperform; precise localization (down to the lines) predicts a correct fix; keep each diff small so the loop's signal stays clean.

## Modes

### debug — failing test, bug, regression, traceback

- Reproduce the failure before editing — ideally a command or script that triggers it on demand.
- State the observed failure exactly (command + output).
- Localize to the smallest region — ideally the specific lines — before editing. Precise localization is the strongest predictor of a correct fix.
- Change one hypothesis at a time.
- Prefer the minimal fix over a broad refactor.
- Verify against the original failing command before declaring done.

### fix — small, known, urgent change

- Keep the diff as small as the problem allows; no opportunistic cleanup.
- Avoid dependency/config changes unless required.
- Add a focused regression test when feasible.
- State residual risk explicitly.

### review — security, auth, payments, or reviewing a diff

- Do not approve a claim without file/line evidence.
- Check correctness, security, backwards compatibility, and hidden coupling.
- Look for missing tests on the changed paths.
- Report findings with severity; escalate when risk is high or ambiguous.

### test-first — behavior change where a test is practical

- Write or identify the test first.
- Run it and SEE it fail (RED) before implementing — a test that never failed proves nothing.
- Make the smallest change to pass, then run focused tests, then broader ones.
- Refactor only while tests stay green.

### refactor — cleanup, simplify, rename, remove dead code

- Preserve behavior; do not mix behavior changes into the refactor.
- Delete complexity before adding abstraction.
- Prove equivalence with existing tests or golden output.
- Keep diffs reviewable.

### migrate — schema, data, or infra change (terraform, k8s, migrations)

- Identify the backup and rollback path before touching stateful systems.
- Prefer staged, reversible changes.
- Validate against a non-production target first when possible.
- Document operational risk and recovery steps.

### spike — prototype, proof-of-concept, unknown library

- Keep spike artifacts isolated from production paths.
- Optimize for learning speed, not polish.
- Do not wire experimental code into production without review.
- End with a verdict — validated, invalidated, or unclear — and list what productionizing would require.

### unstuck — repeated failures, thrashing, "still failing"

- Stop making speculative edits.
- Summarize what you tried and the evidence each attempt produced.
- List the top two hypotheses and the test that would discriminate them.
- Collect missing information before changing more code.
- Consider delegating a fresh review.

## Why this exists

Empirical work is consistent: _naming a persona_ ("act as an expert debugger") does not reliably change model behavior, while specifying a _procedure_ does. These modes are procedures aimed at the situations models handle worst — thrashing, faking green, skipping reproduction, running destructive commands, migrating without a rollback. Their effect on any given agent is not measured here; treat them as disciplined defaults, not a guarantee.
