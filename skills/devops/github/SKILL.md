---
name: github
description: "Complete GitHub lifecycle: authenticate, manage repos, issues, PRs, code review, CI, and releases via gh CLI or REST."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [GitHub, Repositories, Pull-Requests, Issues, Code-Review, CI/CD, Authentication, Releases]
    related_skills: [native-mcp, github]
---

# GitHub — Complete Lifecycle

One skill covers the full GitHub workflow: authenticate → repo → issues → PRs → review → CI → merge → release.

## 0. Prerequisites & Setup

Complete authentication setup (HTTPS tokens, SSH keys, gh CLI login, credential helpers, headless environments). See `references/auth-setup.md` for the full detection flow and troubleshooting.

```bash
# Quick auth detection (sets GH_AUTH_METHOD, GITHUB_TOKEN, GH_USER, GH_OWNER, GH_REPO)
source "${HERMES_HOME:-$HOME/.hermes}/skills/github/scripts/gh-env.sh"
```

## 1. Repository Management

Clone, create, fork, and configure repos. Settings, topics, branch protection, secrets, Releases, GitHub Actions, and gists. See `references/github-api-cheatsheet.md` for the full REST API reference.

**Key actions:** `gh repo clone/clone/create/fork/sync` and `curl` equivalents via `references/github-api-cheatsheet.md`.

## 2. Issues

Create, search, triage, label, assign, and close issues. Bulk operations. See `templates/issue-bug-report.md` and `templates/issue-feature-request.md` for body templates.

Key patterns:
- Filter issues by label, assignee, state.
- Bulk close with `gh issue list --label wontfix --json number | xargs`.
- Auto-close on PR merge with `Closes #N` in body.

## 3. Pull Request Workflow

Complete PR lifecycle: branch → commit → push → create → CI monitoring → auto-fix failures → merge.

### 3.1 PR Body Templates

Use `templates/pr-body-bugfix.md` or `templates/pr-body-feature.md` as the starting point for body text.

### 3.2 Commit Messages

Follow the convention in `references/conventional-commits.md`:
```
feat(scope): short description

Longer explanation if needed.
```

### 3.3 CI Troubleshooting

When CI fails, see `references/ci-troubleshooting.md` for the full auto-fix loop: fetch failed logs, diagnose, patch, commit, recheck.

## 4. Code Review

Review PRs locally or on GitHub. Use `references/review-output-template.md` for the structured report format.

**Local pre-push review:**
- `git diff main...HEAD --stat` → scope.
- Check for debug statements, secrets, large files, merge markers.

**GitHub PR review:**
- Check out PR locally: `git fetch origin pull/N/head:pr-N && git checkout pr-N`.
- Run tests and linters.
- Post formal review with inline comments (gh or curl).
- Use the severity guide: 🔴 Critical / ⚠ Warning / 💡 Suggestion / ✅ Looks Good.