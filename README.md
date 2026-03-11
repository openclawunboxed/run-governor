# Run Governor

A lightweight runtime governance layer for agent workflows.

Most agent builders focus on the **brain**:

- better models
- more tools
- more context
- more memory

Then the agent finally touches real work and the problems show up.

Runs get stuck.  
Tools repeat endlessly.  
Costs spike.  
Logs are useless.  
The system almost performs actions you never intended.

That is not a model problem.

It is a **runtime governance problem**.

The Run Governor adds a safety layer underneath an agent workflow to control how runs behave.

---

# What the Governor Controls

During a run the governor enforces limits and records events.

It answers questions like:

- how many steps can the run take
- how many tool calls are allowed
- how many LLM calls are allowed
- how much money can the run spend
- when a loop should be stopped
- which tools are safe to execute
- how the run should be logged
- how the run should be scored afterward

Without these controls agents behave like demos.

With them they start behaving like systems.

---

 Architecture

The Run Governor sits between your agent logic and the outside world.

Agent workflow  
↓  
Run Governor  
↓  
Policies and limits  
↓  
Tool execution  
↓  
Trace logging and run ledger

During a run the governor observes every step and enforces constraints.

Example flow:

agent step  
↓  
governor records step event  
↓  
agent requests tool  
↓  
governor checks policy and limits  
↓  
tool executes  
↓  
governor records trace event  
↓  
run continues or stops if limits are exceeded

This separation keeps the agent logic simple while the governor handles safety, budgeting, and observability.


# Core Ideas

## Budget Caps

Each run has limits:

- max steps
- max tool calls
- max LLM calls
- max cost
- max runtime

Without caps agents eventually burn time or money.

---

## Loop Guards

Agents frequently repeat the same tool calls.

Example:

search → fail  
search → fail  
search → fail

The governor fingerprints tool calls and stops runs when identical calls repeat too many times.

---

## Tool Risk Levels

Tools are separated into categories.

| Category | Example |
|--------|--------|
| read_only | search, scrape |
| internal_write | memory updates |
| external_write | email, social posting |
| system_exec | shell commands |

Higher-risk tools can require human approval.

Configuration lives in:

policies/tool_risk_matrix.json

---

## Trace Logging

Every run emits structured events:

- step events
- tool calls
- LLM calls
- retries

These follow the schema in:

schema/trace_schema.json

If something breaks you should be able to reconstruct the run.

---

## Run Scoring

Producing the correct answer is not enough.

Runs can also be evaluated for:

- budget discipline
- tool relevance
- retry behavior
- escalation timing
- safety compliance

See:

prompts/run-scorer-prompt.txt

These prompts are included as assets.  
They are not automatically wired into the governor.

---

## Hybrid Model Ladder

Not every task deserves a premium model.

A simple model ladder can allocate work across three lanes.

Lane 1 — Local models  
Lane 2 — Cheap API models  
Lane 3 — Premium reasoning models

Example configuration:

policies/local-free-premium-ladder.json

---

# Repository Structure

node/
    runGovernor.js
    exampleAgentLoop.js

python/
    run_governor.py
    example_agent_loop.py

policies/
    default-medium-risk.json
    local-free-premium-ladder.json
    tool_risk_matrix.json

schema/
    trace_schema.json

sheets/
    run-ledger.csv

prompts/
    approval-gate-prompt.txt
    run-scorer-prompt.txt

tools/
    trace_viewer.py

---

# What This Repo Is

This repo is a **starter governance layer**.

It is designed to:

- show the runtime governance pattern
- give a minimal working implementation
- provide reusable policies and prompts

It is not a full orchestration framework.

You are expected to integrate the governor into your own agent workflows.

---

# Quick Start

See quickstart.md for a minimal example.

Python example:

python python/example_agent_loop.py

Node example:

node node/exampleAgentLoop.js

These examples demonstrate:

- step tracking
- tool call tracking
- LLM call tracking
- loop protection
- cost accounting
- trace generation

---

# License

MIT