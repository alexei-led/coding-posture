#!/usr/bin/env bash
set -euo pipefail
coding-posture --agent codex run "Review auth/token diff for correctness, security, and missing tests"
