#!/usr/bin/env bash
# Evaluate the coding-posture skill by REUSING cc-thingz's `agent-skills-eval`
# runner (LLM-judge, with/without-skill baseline). The skill lives in this repo,
# outside the cc-thingz monorepo, so we assemble the layout the runner expects
# (<root>/<plugin>/skills/<skill>/{SKILL.md,evals/evals.json}) and invoke it.
#
# Paid + stochastic. Needs an installed agent-skills-eval CLI and API key.
#   OPENAI_API_KEY=sk-... bash eval/run-skill-evals.sh
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/.." && pwd)"
evals_src="$repo_root/tests/skill-evals/coding-posture/evals"

# Load a local .env (gitignored) if present, so the run is self-contained.
if [ -f "$repo_root/.env" ]; then
	set -a
	# shellcheck disable=SC1091
	. "$repo_root/.env"
	set +a
fi

skill_src="${SKILL_EVAL_SKILL_DIR:-$repo_root/skills/coding-posture}"
plugin="coding-posture"
skill="coding-posture"
root_base="${SKILL_EVAL_ROOT:-${TMPDIR:-/tmp}}"
target="${SKILL_EVAL_TARGET:-gpt-6.1-sol}"
judge="${SKILL_EVAL_JUDGE:-$target}"
cli="${SKILL_EVAL_CLI:-agent-skills-eval}"
config="${SKILL_EVAL_CONFIG:-$repo_root/eval/config.json}"

: "${OPENAI_API_KEY:?set OPENAI_API_KEY — agent-skills-eval makes paid model calls}"

if ! command -v "$cli" >/dev/null 2>&1; then
	printf 'Eval CLI not found: %s. Install it explicitly or set SKILL_EVAL_CLI to an executable path.\n' "$cli" >&2
	exit 1
fi

mkdir -p "$root_base"
root=$(mktemp -d "$root_base/coding-posture-skill-eval.XXXXXX")
trap 'rm -rf -- "$root"' EXIT
ws="${SKILL_EVAL_WORKSPACE:-$root_base/coding-posture-skill-eval-workspace-${root##*.}}"

dest="$root/$plugin/skills/$skill"
mkdir -p "$dest" "$ws"
cp "$skill_src/SKILL.md" "$dest/SKILL.md"
cp -R "$evals_src" "$dest/evals"

"$cli" "$root" \
	--config "$config" \
	--include "$plugin/skills/$skill" \
	--workspace "$ws" \
	--baseline \
	--target "$target" \
	--judge "$judge" \
	--base-url "${SKILL_EVAL_BASE_URL:-https://api.openai.com/v1}" \
	--api-key-env OPENAI_API_KEY \
	--concurrency "${SKILL_EVAL_CONCURRENCY:-4}" \
	--layout iteration \
	--report
