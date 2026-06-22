---
name: software-development-workflow
description: "Class-level software development lifecycle: plan, TDD, subagent execution, review, and systematic debugging for Hermes Agent."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [planning, testing, tdd, debugging, subagent, code-review, workflow, development]
---

# Agentic Software Development Workflow

This umbrella covers the full agent-driven development lifecycle:
**Plan → TDD → Implement → Review → Debug**.

Use this as the entry point. Load the subsection that matches the current phase,
or chain them sequentially for end-to-end delivery.

## 1. Planning: writing-plans

Write comprehensive implementation plans before any code is written. Document:
- exact file paths, complete copy-pasteable code examples
- test strategies and verification commands
- bite-sized tasks (2-5 minutes each)
- DRY, YAGNI, TDD principles applied throughout

**When to load:** Before implementing multi-step features, breaking down complex
requirements, or delegating to subagents.

See the standalone `writing-plans` skill for the full plan document structure,
task templates, and execution handoff procedures.

## 2. Test-Driven Development: test-driven-development

Enforce the RED-GREEN-REFACTOR cycle. No production code without a failing
test first. Write the test, watch it fail, write minimal code to pass,
refactor.

**When to load:** During implementation of every new feature, bug fix,
refactor, or behavior change. Apply to every task in a plan.

See the standalone `test-driven-development` skill for the Iron Law,
rationalization table, red flags, and subagent integration patterns.

## 3. Subagent Execution: subagent-driven-development

Execute plans by dispatching fresh `delegate_task` subagents per task with
two-stage review:
1. Spec compliance review (did it match the plan?)
2. Code quality review (is it well built?)

**When to load:** When you have an implementation plan and want automated,
high-quality execution with consistent review gates.

See the standalone `subagent-driven-development` skill for the full per-task
workflow, context-sharing rules, issue-handling loops, and integration notes
for `writing-plans`, `test-driven-development`, `requesting-code-review`,
and `systematic-debugging`.

## 4. Pre-Commit Verification: requesting-code-review

Automated verification pipeline before code lands:
- Static security scan (secrets, injection, eval)
- Baseline-aware tests and linting
- Independent reviewer subagent for logic/suggestions
- Auto-fix loop (max 2 cycles)

**When to load:** After implementing a feature or bug fix, before `git commit`
or `git push`. Run after EACH task in subagent-driven-development.

See the standalone `requesting-code-review` skill for the full 8-step pipeline,
reviewer subagent prompt template, and baseline comparison methodology.

## 5. Systematic Debugging: systematic-debugging

4-phase root-cause debugging:
1. Root Cause Investigation (read errors, reproduce, check changes, trace data flow)
2. Pattern Analysis (find working examples, compare differences)
3. Hypothesis & Testing (scientific method, one variable at a time)
4. Implementation (regression test first, fix root cause, verify)

**When to load:** For any technical issue — test failures, production bugs,
unexpected behavior, build failures, or performance problems. Especially under
time pressure or after multiple failed fixes.

See the standalone `systematic-debugging` skill for the full phase breakdowns,
checklists, red flags, common rationalizations, and integration with TDD.

## Workflow Chains

### End-to-end feature delivery

```
writing-plans  →  subagent-driven-development  →  requesting-code-review
                      ↓ uses TDD per task
               systematic-debugging (when bugs arise)
```

### Quick fix / bug patch

```
systematic-debugging  →  test-driven-development  →  requesting-code-review
```

### Solo implementation

```
writing-plans  →  test-driven-development  →  requesting-code-review
```

## Choosing the Right Phase

| User trigger | Load this phase |
|--------------|-----------------|
| "Build X", "Implement X", "Plan X" | writing-plans |
| "Write code", "Start implementing" | test-driven-development |
| "Execute the plan", "Dispatch subagents" | subagent-driven-development |
| "Verify", "Review", "Commit", "Push" | requesting-code-review |
| "Something is broken", "Bug in X" | systematic-debugging |
