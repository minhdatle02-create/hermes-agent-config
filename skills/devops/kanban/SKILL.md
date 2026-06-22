---
name: kanban
description: "Multi-agent work queue: orchestrator decomposition, worker lifecycle, and Codex-lane integration."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [kanban, multi-agent, orchestration, routing, codex, worktrees]
    related_skills: [coding-agent, hermes-agent]
---

# Kanban — Orchestrator, Worker, and Codex Lane

This skill covers the full Hermes Kanban system from three viewpoints in labeled sections.

## 1. Orchestrator (Route-Work-Playbook)

**Trigger:** You are an orchestrator profile responsible for decomposing user requests and assigning them through the Kanban board.

**Key rules:**
- **Discover profiles before planning.** The dispatcher silently drops unknown assignees — `hermes profile list` or `kanban_list` first.
- **Decompose, don't execute.** Route every concrete task as a Kanban card; use `delegate_task` for quick reasoning within your own session.
- **Split multi-lane requests** into independent cards with no parent links; link true data dependencies only using `parents=[...]`.
- **Don't pre-create the whole graph** if the shape depends on intermediate findings — let synthesis tasks plan their own continuation from parent handoffs.

## 2. Worker Role

**Trigger:** A Kanban dispatcher spawned you as a worker assigned to a specific task.

**Lifecycle:**
1. **Orient** — `kanban_show` first; check status (blocked/archived means stop).
2. **Work** — operate only inside `$HERMES_KANBAN_WORKSPACE`.
3. **Heartbeat** — send `kanban_heartbeat` with progress details every few minutes for long tasks.
4. **Block or complete** — `kanban_block(reason="...")` when you need a human decision, `kanban_complete(summary=..., metadata={...})` when genuinely done.

**Workspace kinds:**
- `scratch` — fresh tmp dir, yours alone, GC'd on archive.
- `dir:<path>` — shared persistent dir, treat like long-lived state.
- `worktree` — git worktree; create it yourself if missing.

## 3. Codex Lane (Kanban Worker Delegating to Codex)

**Trigger:** A Kanban worker wants to delegate implementation to Codex CLI in an isolated lane while Hermes keeps ownership of the task lifecycle.

**Rules:**
1. Hermes owns Kanban lifecycle. Codex is input-only — never let it write board state.
2. Always isolate in a git worktree or branch tied to the task ID.
3. Hermes reconciles the diff, runs verification, writes `kanban_complete`.
4. Use `templates/pmb-codex-lane-prompt.md` when working on prediction-market-bot.

**Monitoring pattern:**
- Start with `terminal(..., background=True, pty=True, notify_on_complete=True)`.
- Monitor with `process(action="poll")` / `process(action="log")`.
- `kanban_heartbeat` every few minutes during long runs.
- Kill conditions: secrets requests, writes outside worktree, unrelated rewrites, near timeout with no safe artifact.