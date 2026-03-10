class RunGovernor:

    def __init__(self, max_steps=50, max_tool_calls=25):
        self.max_steps = max_steps
        self.max_tool_calls = max_tool_calls
        self.step_count = 0
        self.tool_calls = 0

    def record_step(self):
        self.step_count += 1
        if self.step_count > self.max_steps:
            raise RuntimeError("step limit exceeded")

    def record_tool(self):
        self.tool_calls += 1
        if self.tool_calls > self.max_tool_calls:
            raise RuntimeError("tool call limit exceeded")
