from pprint import pprint
from run_governor import RunGovernor


def run_agent():
    gov = RunGovernor(
        max_steps=12,
        max_tool_calls=10,
        max_llm_calls=8,
        max_cost_usd=0.50,
        max_wall_clock_seconds=120,
        max_retries_per_step=2,
        loop_signature_window=5,
        loop_threshold=3,
    )

    gov.record_step("search", "start search step")
    gov.record_tool(
        "search",
        {"query": "openclaw run governor"},
        cost_usd=0.01,
        step_name="search",
        summary="search query executed",
    )

    gov.record_step("summarize", "summarize results")
    gov.record_llm_call(
        "gpt-4o-mini",
        tokens=500,
        cost_usd=0.005,
        step_name="summarize",
        summary="summary generated",
    )

    pprint(gov.summary())
    pprint(gov.export_trace())


if __name__ == "__main__":
    run_agent()