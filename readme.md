# openclaw agent governor

a lightweight governance layer for autonomous agent workflows.

this repo provides a minimal but practical control layer for builders running
openclaw-style agents, browser agents, or automation loops.

core capabilities:

- run governance (step limits, tool limits, loop detection)
- approval gates for risky actions
- tool risk classification
- hybrid model routing ladder
- trace schema for run auditing
- run scoring for workflow evaluation

the goal is simple:
give builders a small, understandable control plane so agents behave like
operators instead of chaotic scripts.

recommended implementation order:

1 install run governor
2 define tool risk matrix
3 connect approval gate prompt
4 log runs using trace schema
5 score runs weekly with run scorer
