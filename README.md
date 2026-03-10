# openclaw agent run governor

a lightweight governance layer for autonomous ai agent workflows.

most builders focus on the brain of the agent:

- better models  
- more tools  
- bigger context  
- more memory  
- more routing  

then the stack finally does real work and the real problems show up.

the run gets stuck.  
the same tool fires again.  
the browser agent keeps wandering.  
the cost climbs.  
the trace is useless.  
the system almost does something you did not actually mean.

that is not just a model problem.

that is a runtime governance problem.

this repo gives you a **run governor**.

a small control layer that sits underneath your workflow and decides:

- how much a run can spend  
- how many steps it can take  
- which tools are allowed  
- which tools need approval  
- when the run is clearly stuck  
- what gets logged  
- how the run gets scored  
- which model lane the task should use  

the goal is simple:

turn fragile agent demos into controlled systems you can actually trust with real work.

---

## what this repo includes

- run governance for agent loops  
- approval gates for risky actions  
- tool risk classification  
- duplicate tool-call guards  
- hybrid model routing ladder  
- trace schema for run auditing  
- run scoring for workflow evaluation  
- reference implementation patterns for python and node builders  

---

## who this is for

this repo is for builders running:

- openclaw agents  
- browser agents  
- research agents  
- developer copilots  
- internal workflow automation  
- ai operators moving beyond demos  

if your agent can spend money, call tools, write data, or trigger external actions, you should add governance before using it on real work.

---

## the core idea

in this architecture, the governor sits between your workflow and the tools or models.

```
agent workflow
      │
      ▼
run governor
      │
      ├── step limit
      ├── cost cap
      ├── retry limit
      ├── duplicate tool-call guard
      ├── approval gate
      ├── trace logging
      ├── run scoring
      └── model router
      │
      ▼
tools and models
```

every action should pass through the governor before execution.

this means:

- tool calls can be inspected  
- model calls can be routed  
- steps can be limited  
- risky actions can require approval  
- every run can be logged and replayed  

---

## the five core rules

### 1. cap spend per run

provider dashboards are not enough.

each run should have limits such as:

- max cost per run  
- max llm calls  
- max tool calls  
- max wall clock time  
- max retries per step  

if you only notice problems after the bill arrives, you never had control.

you had a receipt.

---

### 2. fingerprint repeated tool calls

agents often repeat the same tool call when confused.

the governor can fingerprint tool calls using something like:

```
tool_signature = hash(tool_name + normalized_args)
```

if the same signature appears repeatedly during a run, the governor can stop execution.

this can eliminate a large amount of wasted behavior from:

- browser wandering  
- bad retries  
- stuck loops  
- malformed orchestration  

---

### 3. separate reading from writing

not all tools carry the same risk.

use three buckets.

#### read only

- search  
- scraping  
- retrieval  
- page parsing  

#### internal write

- database updates  
- crm notes  
- memory writes  
- internal docs  

#### external write or irreversible action

- emails  
- payments  
- social posts  
- deletes  
- account changes  

external and irreversible actions should typically require approval.

---

### 4. log every step

if something breaks and you cannot replay the run, the system is not serious.

every run should log information such as:

- workflow name  
- run id  
- step index  
- model used  
- tool used  
- arguments  
- tool signature hash  
- tokens used  
- cost  
- latency  
- confidence  
- status  
- stop reason  
- summary  
- approval required  
- approval result  

this gives you real observability instead of guesswork.

---

### 5. score the run

a run can produce the correct output while still behaving poorly operationally.

for example:

- it took too many steps  
- it escalated to a premium model too early  
- it retried the same thing too many times  
- it used too many tools for a simple task  

you should score how the run behaved, not just whether the final output looked acceptable.

recommended scoring areas:

- output quality  
- step efficiency  
- token efficiency  
- tool efficiency  
- escalation timing  
- safety behavior  

---

## the hybrid model ladder

many stacks fall into one of three defaults:

- local model everywhere  
- cheap api everywhere  
- premium model everywhere  

a better structure is a ladder.

### lane 1 — local floor

use local models for:

- routing  
- classification  
- extraction  
- heartbeat checks  
- cron tasks  
- cheap retries  
- simple parsing  

the goal is not perfection.

the goal is cheap, private, resilient baseline behavior.

---

### lane 2 — cheap api middle

use affordable api models for:

- summaries  
- standard research  
- routine writing  
- normal code help  
- workflow orchestration  

most agent work should live here.

---

### lane 3 — premium ceiling

reserve premium models for:

- complex debugging  
- advanced coding tasks  
- large context reasoning  
- high-risk decisions  
- final synthesis  

the governor rule is simple:

**what is the cheapest lane that can still solve this safely?**

---

## what beginners should do first

if you are new, do not start by wiring every feature at once.

start with this order:

1. install the run governor  
2. define max steps, cost, retries, and timeout  
3. classify your tools into risk buckets  
4. require approval for external write actions  
5. enable trace logging  
6. enable duplicate tool-call detection  
7. add model routing last  

this gives you a safe baseline quickly.

---

## quick mental model

think of the governor as the operating rules for the run.

the model is the brain.

the tools are the hands.

the governor decides:

- how long the brain can think  
- what the hands are allowed to touch  
- when to stop  
- when to ask permission  
- how to record what happened  

without this layer, you often do not have a reliable operator.

you may just have a chaotic script with a credit card.

---

## minimal example

a minimal run might look like this:

```python
from governor.run_governor import RunGovernor

governor = RunGovernor(
    max_steps=12,
    max_cost_usd=0.50,
    max_llm_calls=8,
    max_tool_calls=10,
    max_retries_per_step=2,
    max_wall_clock_seconds=120,
    duplicate_tool_call_limit=3
)

run = governor.start_run(workflow_name="research_task")

while run.active:
    action = agent.next_action()

    decision = governor.evaluate(action)

    if not decision.allowed:
        governor.stop_run(reason=decision.reason)
        break

    result = execute(action)
    governor.record_step(action=action, result=result)

governor.finalize_run()
```

see the `examples/simple_agent/` folder for a beginner-friendly runnable example.

---

## recommended repo structure

```
README.md
architecture.md
quickstart.md
run_governor_reference.md
tool_capabilities.md

governor/
    run_governor.py
    model_router.py
    loop_guard.py

prompts/
    approval_gate_prompt.md
    run_scoring_prompt.md

templates/
    trace_schema.json
    tool_risk_matrix.json
    run_ledger_template.json
    default_governor_config.json
    approval_policy_examples.json

examples/
    simple_agent/
        README.md
        agent.py
        governor.py
        tools.py
```

---

## what success looks like

after implementing governance like this, your agent should be able to:

- stop before it spirals  
- avoid repeating failed tool calls  
- separate safe actions from risky actions  
- log every run clearly  
- score runs for improvement  
- route tasks to the correct model tier  
- become cheaper, safer, and easier to debug  

that is the difference between a cool demo and something you can trust with real work.

---

## recommended implementation order

1. install run governor  
2. define tool risk matrix  
3. connect approval gate prompt  
4. log runs using trace schema  
5. score runs regularly  
6. tune model routing ladder  
7. expand capability scoping as workflows grow  

---

## why this matters

most agent failures in production are predictable:

- runaway loops  
- repeated tool retries  
- wasted token spend  
- unsafe actions  
- no traceability  
- unclear model allocation  

the run governor helps close the gap between:

cool demo

and

something you can actually trust.
