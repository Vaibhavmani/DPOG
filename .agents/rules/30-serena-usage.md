---
activation: Always On
---

# Serena usage

Serena is connected as an MCP server. Use it deliberately, not reflexively.

## Read memories at session start

Antigravity resets agent context between sessions. Serena's memories do not — they live on disk in `.serena/memories/`. **Before planning any task, list and read the relevant memories.** Start with `core`, then whichever of `tech_stack`, `conventions`, `suggested_commands`, `task_completion`, and `decisions` bear on the task.

This is the main reason Serena is in this project. Skipping it means relearning decisions that were already made and argued.

## Write memories when a decision is made

After resolving something that a future session would otherwise have to rediscover, write it to a memory. Specifically:

- A rejected approach and why it was rejected
- A non-obvious constraint discovered during build (a font subset that broke conjuncts, a cache strategy that served stale content)
- A convention established mid-build that is not yet in the rules

Read `memory_maintenance` before writing your first memory in a session — it defines the style and reference conventions. Use the `mem:NAME` convention when one memory references another.

Do not write a memory for routine progress. That is what the Task List artifact is for. Memories are for decisions and constraints, not status.

## Prefer symbol tools over grep

For anything structural — finding where a function is defined, what references it, what a module exports — use Serena's symbol tools rather than text search. They understand the code; grep matches strings.

Text search is still right for content: finding a specific instruction string, checking whether a colour literal leaked into CSS, locating a slug.

## Known limitation in this project

Serena's HTML and SCSS/CSS language servers are experimental and were listed explicitly in `.serena/project.yml` — they are not auto-detected. Cross-file go-to-definition is not meaningful for HTML, so expect symbol tools to be strong on the JavaScript modules and weaker on markup. Fall back to reading files directly for markup work rather than fighting the tooling.

If symbol lookups return nothing on a file you know exists, check that its language is listed in `.serena/project.yml` before assuming the file is the problem.

## Do not

- Do not run Serena's onboarding again once `.serena/memories/` is populated. The seeded memories are hand-written and more accurate than a re-derived pass.
- Do not edit `.serena/project.yml` to add languages without saying why in the Walkthrough. Each added language server costs startup time.
