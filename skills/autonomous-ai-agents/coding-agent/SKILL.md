---
name: coding-agent
description: "Delegate coding tasks to external coding agents: Claude Code, OpenAI Codex, and OpenCode CLI."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Coding-Agent, Code-Review, Refactoring, Automation, PTY, Claude, Codex, OpenCode]
    related_skills: [kanban, hermes-agent]
---

# Coding Agents — Claude Code, Codex, OpenCode

Use an external coding agent CLI for implementation, refactoring, PR reviews, and parallel batch work. Three sections below cover the three supported agents.

## 1. Claude Code

Claude Code is Anthropic's autonomous coding CLI. Supports print mode (`-p`) for one-shots and interactive PTY mode via tmux for multi-turn sessions.

### When to use
- One-shot tasks (fix, refactor, review)
- CI/CD automation with `--output-format json`
- Multi-turn interactive work requiring human in the loop

### Key flags
| Flag | Effect |
|------|--------|
| `-p "task"` | Print mode — non-interactive, exits when done |
| `-c` / `-r <id>` | Resume most recent or specific session |
| `--model <alias>` | `sonnet`, `opus`, `haiku`, or full name |
| `--max-turns <n>` | Limit agentic loops (print mode only) |
| `--dangerously-skip-permissions` | Auto-approve ALL tool use; handles Yaml defaults to "No" — send Down then Enter |
| `--bare` | Skip hooks/plugins/OAuth; fastest for CI |
| `--output-format json/stream-json` | Structured output; parse with jq for streaming |

### PTY handling
Always use tmux for interactive mode. Handle the workspace trust dialog (Enter = Yes) on first visit; handle the permissions dialog (Down + Enter = Yes) when `--dangerously-skip-permissions` is used.

## 2. OpenAI Codex

Codex is OpenAI's autonomous coding CLI. Requires a git repo. Uses `pty=true` for interactive or `codex exec` for one-shots.

### When to use
- Feature build / refactoring
- PR reviews
- Parallel issue fixing via worktrees
- Batch PR reviews

### Key flags / modes
| Flag | Effect |
|------|--------|
| `codex exec "prompt"` | One-shot, exits when done |
| `--full-auto` | Sandboxed, auto-approves in workspace |
| `--yolo` | No sandbox, no approvals (fastest, most dangerous) |
| background + pty + notify | Long-running background tasks |

### Worktree pattern
Use isolated branches/worktrees for parallel fixes. Cherry-pick accepted commits, discard rejected parts.

```bash
BRANCH="fix/issue-78"
WORKTREE="/tmp/issue-78"
git worktree add -b "$BRANCH" "$WORKTREE" main
```

## 3. OpenCode

OpenCode is a provider-agnostic, open-source coding agent with TUI and CLI.

### When to use
- User explicitly asks for OpenCode
- Long-running coding sessions with progress checks
- Parallel isolated directories/worktrees

### Key flags
| Flag | Effect |
|------|--------|
| `opencode run "prompt"` | One-shot, exits when done (no pty needed) |
| `-f <file>` | Attach context files |
| `--think` | Show reasoning |
| `--model provider/model` | Force specific model |
| `--variant <level>` | Reasoning effort (high, max, minimal) |

### Interactive sessions
Start with `background=true, pty=true`. Exit with Ctrl+C, NOT `/exit` (opens agent selector).

## Cross-Agent Patterns

### Parallel work
Run multiple agent processes simultaneously in isolated workdirs to avoid collisions.

### Common pitfalls across all three
1. Always set `pty=true` for interactive TUI tools.
2. Always scope to a single repo/workdir.
3. Monitor long tasks with `process(action="poll"/"log")`.
4. Never let the agent own kanban lifecycle — only Hermes does.
5. Prefer print/run mode for one-shots; interactive only when iteration is needed.