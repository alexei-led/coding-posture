import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import {
  cpSync,
  existsSync,
  mkdirSync,
  mkdtempSync,
  readFileSync,
  readdirSync,
  rmSync,
  writeFileSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";

function setup(t) {
  const dir = mkdtempSync(join(tmpdir(), "posture-runner-test-"));
  t.after(() => rmSync(dir, { recursive: true, force: true }));
  mkdirSync(join(dir, "eval"));
  cpSync(
    new URL("../eval/run-skill-evals.sh", import.meta.url),
    join(dir, "eval/run-skill-evals.sh"),
  );
  writeFileSync(join(dir, "eval/config.json"), "{}");
  const skillDir = join(dir, "skills/coding-posture");
  const evalDir = join(dir, "tests/skill-evals/coding-posture/evals");
  mkdirSync(skillDir, { recursive: true });
  mkdirSync(evalDir, { recursive: true });
  writeFileSync(join(skillDir, "SKILL.md"), "current skill");
  writeFileSync(join(evalDir, "evals.json"), '{"skill_name":"coding-posture","evals":[]}');
  const inputParent = join(dir, "input parent");
  mkdirSync(inputParent);
  writeFileSync(join(inputParent, "keep.txt"), "unrelated");
  const workspace = join(dir, "workspace");
  const cli = join(dir, "fake eval.mjs");
  writeFileSync(
    cli,
    `#!/usr/bin/env node
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
const args = process.argv.slice(2);
const workspace = args[args.indexOf('--workspace') + 1];
mkdirSync(workspace, { recursive: true });
writeFileSync(join(workspace, 'invocation.json'), JSON.stringify({
  args,
  skill: readFileSync(join(args[0], 'coding-posture/skills/coding-posture/SKILL.md'), 'utf8'),
  cases: JSON.parse(readFileSync(join(args[0], 'coding-posture/skills/coding-posture/evals/evals.json'), 'utf8')),
}));
process.exit(Number(process.env.FIXTURE_CLI_EXIT ?? 0));
`,
    { mode: 0o755 },
  );
  const run = (extraEnv) =>
    spawnSync("bash", [join(dir, "eval/run-skill-evals.sh")], {
      encoding: "utf8",
      env: {
        ...process.env,
        OPENAI_API_KEY: "unused",
        SKILL_EVAL_CLI: cli,
        SKILL_EVAL_ROOT: inputParent,
        SKILL_EVAL_WORKSPACE: workspace,
        SKILL_EVAL_CONFIG: join(dir, "eval/config.json"),
        SKILL_EVAL_SKILL_DIR: skillDir,
        SKILL_EVAL_TARGET: "fixture-target",
        SKILL_EVAL_JUDGE: "fixture-judge",
        SKILL_EVAL_BASE_URL: "http://127.0.0.1:1",
        SKILL_EVAL_CONCURRENCY: "1",
        FIXTURE_CLI_EXIT: "0",
        ...extraEnv,
      },
    });
  return { dir, inputParent, workspace, run };
}

for (const exitCode of [0, 7]) {
  test(`eval inputs are isolated and cleaned when CLI exits ${exitCode}`, (t) => {
    const { inputParent, workspace, run } = setup(t);
    const result = run({ FIXTURE_CLI_EXIT: String(exitCode) });
    assert.equal(result.status, exitCode, result.stderr);
    const invocation = JSON.parse(readFileSync(join(workspace, "invocation.json"), "utf8"));
    assert.equal(invocation.skill, "current skill");
    assert.equal(invocation.cases.skill_name, "coding-posture");
    for (const [flag, value] of [
      ["--target", "fixture-target"],
      ["--judge", "fixture-judge"],
      ["--base-url", "http://127.0.0.1:1"],
      ["--concurrency", "1"],
    ]) {
      assert.equal(invocation.args[invocation.args.indexOf(flag) + 1], value);
    }
    assert.ok(invocation.args.includes("--baseline"));
    assert.ok(invocation.args.includes("--config"));
    assert.ok(!existsSync(invocation.args[0]));
    assert.deepEqual(readdirSync(inputParent), ["keep.txt"]);
    assert.equal(readFileSync(join(inputParent, "keep.txt"), "utf8"), "unrelated");
  });
}

test("a previous skill directory can be evaluated with the same cases", (t) => {
  const { dir, workspace, run } = setup(t);
  const previous = join(dir, "previous skill");
  mkdirSync(previous);
  writeFileSync(join(previous, "SKILL.md"), "previous skill");
  const result = run({ SKILL_EVAL_SKILL_DIR: previous });
  assert.equal(result.status, 0, result.stderr);
  const invocation = JSON.parse(readFileSync(join(workspace, "invocation.json"), "utf8"));
  assert.equal(invocation.skill, "previous skill");
  assert.equal(invocation.cases.skill_name, "coding-posture");
});

test("a previous skill directory from .env is used for comparison", (t) => {
  const { dir, workspace, run } = setup(t);
  const previous = join(dir, "previous skill");
  mkdirSync(previous);
  writeFileSync(join(previous, "SKILL.md"), "previous skill from dotenv");
  writeFileSync(join(dir, ".env"), 'SKILL_EVAL_SKILL_DIR="$FIXTURE_PREVIOUS_SKILL"\n');
  const result = run({ FIXTURE_PREVIOUS_SKILL: previous });
  assert.equal(result.status, 0, result.stderr);
  const invocation = JSON.parse(readFileSync(join(workspace, "invocation.json"), "utf8"));
  assert.equal(invocation.skill, "previous skill from dotenv");
});

test("a missing CLI fails without installing or touching existing inputs", (t) => {
  const { dir, inputParent, workspace, run } = setup(t);
  const result = run({ SKILL_EVAL_CLI: join(dir, "missing-cli") });
  assert.equal(result.status, 1);
  assert.match(result.stderr, /Eval CLI not found/);
  assert.deepEqual(readdirSync(inputParent), ["keep.txt"]);
  assert.ok(!existsSync(workspace));
});
