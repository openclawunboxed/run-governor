# Quickstart

This guide runs the governor in under two minutes.

The examples demonstrate the core ideas:

- step tracking
- tool tracking
- LLM call tracking
- cost accounting
- trace logging

You do not need OpenClaw or any external services to run these examples.

---

# Step 1 — Clone the repo

git clone https://github.com/openclawunboxed/run-governor.git  
cd run-governor

---

# Step 2 — Run the Python example

From the repo root run:

python python/example_agent_loop.py

You should see output similar to:

{
  "run_id": "abc123",
  "step_count": 2,
  "tool_calls": 1,
  "llm_calls": 1,
  "cost_usd": 0.015,
  "elapsed_seconds": 0.3
}

Followed by a trace showing the sequence of events.

Example trace events:

step  
tool_call  
llm_call

Each event includes fields like:

- run_id
- step_index
- event_type
- tool or model
- cost
- timestamp

The event format follows:

schema/trace_schema.json

---

# Step 3 — Run the Node example

From the repo root run:

node node/exampleAgentLoop.js

You should see similar output to the Python example.

Both implementations demonstrate the same runtime pattern.

---

# What the Example Shows

The example agent does three things:

1. records a step
2. performs a tool call
3. performs an LLM call

During the run the governor:

- counts steps
- counts tool calls
- tracks cost
- detects repeated tool calls
- records trace events

If any limit is exceeded the governor stops the run.

---

# Next Steps

After running the example you can experiment with the configuration.

Lower limits by editing:

policies/default-medium-risk.json

Reduce values like:

max_steps  
max_tool_calls  
max_llm_calls  
max_cost_usd  

Then run the example again.

---

# Changing Tool Risk Levels

Edit:

policies/tool_risk_matrix.json

Move tools between:

read_only  
internal_write  
external_write  
system_exec  

This lets you test approval policies.

---

# Inspecting Traces

Traces follow the schema:

schema/trace_schema.json

You can visualize them using the trace viewer:

python tools/trace_viewer.py trace.json

This prints a readable timeline of the run.

---

# What This Starter Kit Does Not Do

This repo intentionally stays small.

It does not include:

- full agent orchestration
- automatic approval workflows
- automatic run scoring
- full model routing systems

Instead it provides the core primitives needed to build those systems safely.