# Eval

The answer eval reuses [`agent-skills-eval`](https://www.npmjs.com/package/agent-skills-eval) to compare responses with and without the skill. It injects `SKILL.md`; it does not test skill activation or execute an agent's proposed commands.

## Cases

[Cases](../tests/skill-evals/coding-posture/evals/evals.json) cover contradictory tests, failure recovery, performance baselines, migration rollback, urgent auth fixes, wrong-reason RED, missing reproduction, patch regressions, redundant-test removal, read-only scope, findings-only reviews, unrun checks, refactor baselines, completion boundaries, optional companions, and private-code sharing.

The [execution fixtures](../tests/skill-evals/coding-posture/fixtures/README.md) separately exercise actual commands, diffs, and authorization boundaries in disposable workspaces. Their seed deliberately contains one failing boundary case; it is not a failing product test.

## Run

Paid and stochastic. Install the runner explicitly; the script does not download it. The local release preparation inspected `agent-skills-eval` 0.1.1. Its `--help` describes supported options; it has no `--version` flag. It uses OpenAI-compatible Chat Completions, and these answer cases require no tools.

```bash
OPENAI_API_KEY=... bash eval/run-skill-evals.sh
```

The script loads a local `.env` if present. Target defaults to `gpt-6.1-sol`; judge defaults to the target. [config.json](config.json) pins medium reasoning effort for both, with sampling parameters omitted. No API control is encoded in the product skill.

| Variable                                | Purpose                                                                                         |
| --------------------------------------- | ----------------------------------------------------------------------------------------------- |
| `SKILL_EVAL_TARGET`, `SKILL_EVAL_JUDGE` | Model IDs accepted by the selected endpoint                                                     |
| `SKILL_EVAL_CONFIG`                     | Runner JSON/YAML config, including target/judge parameters                                      |
| `SKILL_EVAL_SKILL_DIR`                  | Skill directory override for comparing a previous version                                       |
| `SKILL_EVAL_CLI`                        | One installed executable name or path; command strings such as `npx --yes ...` are not accepted |
| `SKILL_EVAL_BASE_URL`                   | OpenAI-compatible endpoint; defaults to the OpenAI API                                          |
| `SKILL_EVAL_ROOT`                       | Parent for a fresh temporary input directory; existing contents are never removed               |
| `SKILL_EVAL_WORKSPACE`                  | Artifact destination; defaults to a fresh run name under the same parent                        |
| `SKILL_EVAL_CONCURRENCY`                | Parallel cases; defaults to 4                                                                   |

The input directory is removed on exit; report artifacts remain in the workspace. Use a distinct workspace for every condition and repeat. Changing endpoint/model requires a compatible config; the GPT reasoning parameter is not a portable Claude or Gemini setting. Native-provider execution needs a suitable runner; the current answer runner is not a native multi-provider agent harness.

## Model guidance

The read-only `model-cards` catalog supplied these current candidates; provider pages were checked on 2026-10-21. Canonical catalog IDs differ from provider request IDs where shown.

| Catalog ID                    | Catalog `verified_on` | Role in evaluation                                                     | Provider source                                                                      |
| ----------------------------- | --------------------- | ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| `gpt-6.1-sol`                 | 2026-09-30            | Default tool-free answer target; medium effort baseline                | [Model specification](https://developers.openai.com/api/docs/models/gpt-6.1-sol)     |
| `anthropic-claude-sonnet-5-5` | 2026-09-30            | Independent agent-execution comparison; request ID `claude-sonnet-5-5` | [Model overview](https://platform.claude.com/docs/en/models/sonnet-5-5/overview)     |
| `google-gemini-3.8-flash`     | 2026-09-13            | Independent provider comparison; request ID `gemini-3.8-flash`         | [Model specification](https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash) |

The catalog is not a complete live inventory: on 2026-10-21, Google's [latest-model page](https://ai.google.dev/gemini-api/docs/latest-model) identifies `gemini-4-argon`, and Anthropic documents [Claude Fable 5.1](https://platform.claude.com/docs/en/models/fable-5-1/overview). Neither has a record in the inspected checkout. Include them in a future provider-native comparison after resolving their controls and guidance; do not apply the older records' settings by analogy. The catalog was not modified.

Shared guidance supports concise constraints, evidence-based completion, and effort calibration. The adopted cross-model wording is a derived design choice, not proof of improvement:

- GPT-6.1 Sol, `model-guide` (official): calibrate verification and avoid repeated checks without a change, failure, or unresolved concern. Its family prompting observations are from Astra, not Sol-specific evidence.
- Claude Sonnet 5.5, `prompting` (official): finish multipart work, require a real check or report its absence, and avoid unrequested additions after completion.
- Gemini 3.8 Flash, `gemini-prompting` + `model-guide` (derived): use direct structured instructions with explicit constraints rather than elaborate reasoning prompts.

The source IDs above refer to records in [model-cards](https://github.com/alexei-led/model-cards): `openai/gpt-6.1-sol`, `anthropic/claude-sonnet-5-5`, and `google/gemini-3.8-flash`. No model-specific prompt variants are justified yet. Effort belongs to the host/API config, and equal effort names do not establish equal compute. Record the selected model and host; neither this catalog nor the eval script proves the backend behind a routed alias.

## Release comparison

Keep the task prompts, evaluator, runtime, workload, and relevant host instructions fixed. Compare:

1. No posture skill: the runner's `--baseline` condition.
2. Previous skill: extract `skills/coding-posture/SKILL.md` from the verified v0.5.0 commit into a disposable skill directory and pass `SKILL_EVAL_SKILL_DIR`.
3. Proposed skill: the default directory.
4. Proposed skill plus a narrowed specialist: only where review/test detail is needed. Run this condition after the separately maintained cc-thingz update; the current wrapper injects one skill and does not compose this condition.

Repeat each model/effort condition in fresh workspaces and report per-case results, run counts, and uncertainty. Judge outcomes rather than exact wording; spot-check judge decisions against command logs for execution runs. Unauthorized writes/sharing, weakened checks, or fabricated verification block release. A small or zero gain is informative; remove added instructions that have no demonstrated benefit.

Test activation separately in the actual host, exposing installed skill descriptions without force-loading the body. Ordinary fixes, TDD, refactors, and optimization should choose posture without requiring both specialists. Specialist review/test requests should select relevant detail without another execution menu. Include a trivial edit and a non-coding task as negative controls. Activation is a host behavior, not a product selection engine.

## Results and limits

Local tooling checks: `npm test`, `bash -n eval/run-skill-evals.sh`, `shellcheck eval/run-skill-evals.sh`, and `shfmt -d eval/run-skill-evals.sh`. The Node tests use a local fake CLI to verify assembly, failure propagation, cleanup, and preservation of existing directories; they make no model calls.

The earlier reported 85% versus 70% result belongs to the old five-case setup. It is not a score for 0.6.0 or the current models. No paid model calls or agent-execution comparisons were performed during release preparation; local checks validate packaging, cases, script behavior, and the fixture's expected failure only. Cross-model quality and actual activation remain unverified until those runs complete.
