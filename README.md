# Coding Posture

A small skill that gives coding agents **task-aware working modes**. Before non-trivial work, the agent picks a mode — `debug`, `fix`, `review`, `test-first`, `refactor`, `migrate`, `spike`, `unstuck` — and follows its checklist.

The point is not to make agents theatrical. It is to stop them from behaving like optimistic elevators with write access: thrashing on a stuck bug, faking green tests, skipping reproduction, running destructive commands, or migrating without a rollback.

## Design

The whole product is one file: [`skills/coding-posture/SKILL.md`](skills/coding-posture/SKILL.md). There is no selection engine and no code. The agent reads the modes and chooses the one that fits the task's context.

Two deliberate choices, both grounded in research:

- **Modes are procedures, not personas.** Naming a role ("act as an expert debugger") does not reliably change model behavior ([Zheng et al., EMNLP 2024](https://aclanthology.org/2024.findings-emnlp.888/)). Specifying a _procedure_ does ([self-consistency / CoT](https://arxiv.org/abs/2203.11171); role-play helps only [as an implicit CoT trigger](https://arxiv.org/html/2308.07702v2)). So each mode is a checklist, not a character.
- **The model self-selects; no keyword router.** Context-based strategy selection beats fixed keyword rules ([Route-to-Reason, 2025](https://arxiv.org/html/2505.19435v1)), and self-selection works on strong models — exactly the targets here. So selection lives in the agent, not in a brittle scoring table.

## Install

It is a standard [`SKILL.md`](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills) skill, so it works unmodified across compatible agents.

**Hermes:** drop `skills/coding-posture/` into `~/.hermes/skills/` (the default skills dir); Hermes auto-discovers it on startup. It also supports installing a skill by hub name or from a URL — see the [Hermes skills docs](https://hermes-agent.nousresearch.com/docs/guides/work-with-skills) for the current command.

**Claude Code / Codex / Cursor:** copy `skills/coding-posture/` into the agent's skills directory (e.g. `~/.claude/skills/coding-posture/`).

**Pi:**

```bash
pi install git:github.com/alexei-led/coding-posture-engine
```

The agent activates the skill from its `description` when a coding task starts.

## Modes

| Mode         | Use when                                 | Core discipline                                     |
| ------------ | ---------------------------------------- | --------------------------------------------------- |
| `debug`      | failing test, bug, regression            | reproduce first, one hypothesis at a time           |
| `fix`        | small known urgent change                | smallest diff, no opportunistic cleanup             |
| `review`     | security/auth/payments, reviewing a diff | no approval without file/line evidence              |
| `test-first` | behavior change, tests practical         | see RED before implementing, never fake green       |
| `refactor`   | cleanup, simplify, rename                | preserve behavior, prove equivalence                |
| `migrate`    | schema/data/infra change                 | rollback path before touching state                 |
| `spike`      | prototype, PoC, unknown library          | isolate, end with a verdict                         |
| `unstuck`    | repeated failures, thrashing             | stop editing, summarize evidence, narrow hypotheses |

Plus invariants that hold in every mode: no destructive commands without explicit scope, verify by running the real check (not by re-reading — [self-correction without external feedback degrades results](https://arxiv.org/abs/2310.01798)), and never report a result you did not run. The modes lean on the practices with the strongest evidence for coding agents: tight [execution-feedback loops](https://arxiv.org/abs/2304.05128), [gathering context before editing rather than rushing to patch](https://arxiv.org/abs/2604.02547), precise fault localization, small diffs, [clarifying underspecified requirements before coding](https://arxiv.org/pdf/2310.10996), and refusing to [game the tests](https://arxiv.org/abs/2604.15149).

## Status

This is an MVP. It is deliberately small: no code, no model calls, no network, no secrets. The bet is that procedural checklists aimed at known model failure modes are useful defaults. **That bet is not yet measured** — there is no eval here comparing agent behavior with and without the skill. Treat the modes as disciplined defaults, not a guarantee.

Future work: an eval harness that measures behavior change on fixed tasks; refine the mode set from what actually moves outcomes.
