#!/usr/bin/env bash
set -euo pipefail
coding-posture --agent claude run "Fix failing pytest regression; keep diff minimal and report test output"
