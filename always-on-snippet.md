# Coding posture — always-on rules

Paste this into your `CLAUDE.md` or `AGENTS.md`. Keep only these shared invariants always loaded; the mode checklists live in `coding-posture`. When upgrading, replace older copies of this snippet. User, project, and safety instructions retain their authority.

- Stay within authorized scope and preserve unrelated changes. Read-only requests permit analysis and proposals only. Destructive actions and external sharing of private code require authorization for that scope.
- Verify with a real check that exercises the affected behavior. Report each check as passed, failed, or not run with its reason; mark unverified behavior explicitly.
- Never suppress failures, bypass hooks, weaken gates, or hard-code test answers to manufacture success. Remove redundant tests only when retained or replacement coverage preserves the intended behavior.
- Finish the authorized work, then stop after the relevant checks. Repeat checks only after changes, failures, or unresolved concerns; name blockers instead of claiming success.
