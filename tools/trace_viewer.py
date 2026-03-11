import json
import sys

def format_event(event):
    step = event.get("step_index", "-")
    etype = event.get("event_type", "unknown")
    name = event.get("step_name") or event.get("tool") or event.get("model") or ""
    status = event.get("status", "")
    cost = event.get("cost_usd", 0)
    summary = event.get("summary", "")

    return f"[step {step}] {etype:<10} {name:<20} status={status} cost=${cost:.4f} {summary}"

def view_trace(path):
    with open(path, "r") as f:
        data = json.load(f)

    if isinstance(data, dict) and "steps" in data:
        events = data["steps"]
    else:
        events = data

    print("\nrun trace\n")
    for e in events:
        print(format_event(e))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python trace_viewer.py trace.json")
        sys.exit(1)

    view_trace(sys.argv[1])