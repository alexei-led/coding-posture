#!/usr/bin/env bash
set -euo pipefail
: "${PI_CLI:=pi}"
coding-posture --agent pi run "Prototype a small API client; return a patch or plan if file editing is unavailable"
