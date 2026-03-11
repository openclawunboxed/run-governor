# quickstart

this repo is a lightweight starter kit for adding runtime governance to an agent loop.

it is meant to be:

- simple enough for beginners to understand
- useful enough for advanced users to extend

---

## 1. start with the python or node example

python example:

- `example_agent_loop.py`

node example:

- `exampleAgentLoop.js`

both show the same basic idea:

1. create a governor
2. record each step
3. record each tool call
4. record each llm call
5. inspect the summary and trace

---

## 2. configure safe defaults

use the values in `default-medium-risk.json` as your starting point.

important settings:

- `max_steps`
- `max_tool_calls`
- `max_llm_calls`
- `max_cost_usd`
- `max_wall_clock_seconds`
- `max_retries_per_step`
- `loop_signature_window`
- `loop_threshold`

do not start with unlimited runs.

---

## 3. classify your tools

use `tool_risk_matrix.json`.

start simple:

- `read_only`
- `internal_write`
- `external_write`
- `system_exec`

good beginner rule:

- read-only tools can often run automatically
- external write and system tools should usually require approval

---

## 4. add approval gates

use `approval-gate-prompt.txt` for risky actions.

good first candidates for approval:

- sending email
- posting publicly
- shell commands
- deployments
- payments
- database writes to production systems

---

## 5. log traces

use `trace_schema.json` as the standard event format for run events.

minimum useful fields:

- `run_id`
- `step_index`
- `event_type`
- `model`
- `tool`
- `arguments`
- `tool_signature_hash`
- `tokens`
- `cost_usd`
- `timestamp`
- `status`
- `summary`

if a run fails and you cannot reconstruct what happened, debugging becomes archaeology.

---

## 6. score the run after it finishes

use `run-scorer-prompt.txt`.

score the run itself, not just the final answer.

important dimensions already included:

- `goal_completion`
- `budget_discipline`
- `tool_relevance`
- `retry_quality`
- `escalation_quality`
- `safety_compliance`

---

## 7. add model routing last

use `local-free-premium-ladder.json` after the system is already stable.

first get the run under control.

then optimize model allocation.

that order matters.

---

## 8. minimum viable beginner setup

if you are brand new, do this in order:

1. run the example
2. lower `max_steps`
3. lower `max_tool_calls`
4. add one risky tool to approval
5. log one trace entry per event
6. inspect the trace after the run
7. then add model routing

that gives you a real first win without needing to understand the whole stack at once.