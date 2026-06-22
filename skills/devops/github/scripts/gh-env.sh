#!/usr/bin/env bash
# Source this: source "${HERMES_HOME:-$HOME/.hermes}/skills/devops/github/scripts/gh-env.sh"
set -euo pipefail
: "${HERMES_HOME:=${HOME}/.hermes}"

if command -v gh &>/dev/null && gh auth status &>/dev/null; then
  GH_TOKEN="$(gh auth token)"
  # If GH_OWNER/GH_REPO already set, don't overwrite
  : "${GH_OWNER:=$(gh api user --jq .login)}"
  : "${GH_REPO:=$(basename "$(git rev-parse --show-toplevel 2>/dev/null || echo .)")}"
  export GH_TOKEN GH_OWNER GH_REPO
  GITHUB_TOKEN="$GH_TOKEN"
  export GITHUB_TOKEN
else
  # Token sourcing order
  for candidate in \
    "${HOME}/.env" \
    "${HERMES_HOME}/.env" \
    "${HOME}/.git-credentials"; do
    if [ -n "${GITHUB_TOKEN:-}" ]; then break; fi
    if [ -f "$candidate" ]; then
      token="$(grep -E "(GITHUB_|github.com)" "$candidate" | head -1 || true)"
      if [ -n "$token" ]; then
        GITHUB_TOKEN="$(echo "$token" | sed -E 's/.*(ghp_|github_pat_[^:]+).*/\1/')"
      fi
    fi
  done
  export GITHUB_TOKEN
  : "${GH_OWNER:=${GITHUB_OWNER:-}}"
  : "${GH_REPO:=${GITHUB_REPO:-}}"
  export GH_OWNER GH_REPO
fi

if [ -z "${GITHUB_TOKEN:-}" ]; then
  echo "[gh-env] no GITHUB_TOKEN detected; pass --token, export it, or run gh auth login" >&2
fi