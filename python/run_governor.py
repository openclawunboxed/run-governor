import time
import json
import hashlib
import uuid
from typing import Any, Dict, List, Optional


class RunGovernor:
    def __init__(
        self,
        max_steps: int = 50,
        max_tool_calls: int = 25,
        max_llm_calls: int = 25,
        max_cost_usd: float = 1.0,
        max_wall_clock_seconds: int = 300,
        max_retries_per_step: int = 2,
        loop_signature_window: int = 5,
        loop_threshold: int = 3,
        run_id: Optional[str] = None,
    ) -> None:
        self.run_id = run_id or str(uuid.uuid4())

        self.max_steps = max_steps
        self.max_tool_calls = max_tool_calls
        self.max_llm_calls = max_llm_calls
        self.max_cost_usd = max_cost_usd
        self.max_wall_clock_seconds = max_wall_clock_seconds
        self.max_retries_per_step = max_retries_per_step
        self.loop_signature_window = loop_signature_window
        self.loop_threshold = loop_threshold

        self.step_count = 0
        self.tool_calls = 0
        self.llm_calls = 0
        self.cost_usd = 0.0
        self.started_at = time.time()
        self.retries_by_step: Dict[str, int] = {}
        self.recent_tool_signatures: List[str] = []
        self.trace: List[Dict[str, Any]] = []

    def _now(self) -> float:
        return time.time()

    def _check_timeout(self) -> None:
        elapsed = self._now() - self.started_at
        if elapsed > self.max_wall_clock_seconds:
            raise RuntimeError("wall clock time limit exceeded")

    def _check_budget(self) -> None:
        if self.cost_usd > self.max_cost_usd:
            raise RuntimeError("cost limit exceeded")

    def _stable_json(self, value: Any) -> str:
        return json.dumps(value or {}, sort_keys=True, separators=(",", ":"), default=str)

    def _make_tool_signature(self, tool_name: str, arguments: Optional[Dict[str, Any]]) -> str:
        raw = f"{tool_name}:{self._stable_json(arguments)}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def _check_loop_guard(self, signature: str) -> None:
        self.recent_tool_signatures.append(signature)
        self.recent_tool_signatures = self.recent_tool_signatures[-self.loop_signature_window:]

        repeats = self.recent_tool_signatures.count(signature)
        if repeats >= self.loop_threshold:
            raise RuntimeError("loop guard triggered")

    def _append_trace(self, event: Dict[str, Any]) -> None:
        event["run_id"] = self.run_id
        self.trace.append(event)

    def record_step(self, step_name: str = "default_step", summary: str = "") -> None:
        self._check_timeout()
        self.step_count += 1

        if self.step_count > self.max_steps:
            raise RuntimeError("step limit exceeded")

        self._append_trace(
            {
                "event_type": "step",
                "step_index": self.step_count,
                "step_name": step_name,
                "timestamp": self._now(),
                "status": "ok",
                "summary": summary,
            }
        )

    def record_tool(
        self,
        tool_name: str,
        arguments: Optional[Dict[str, Any]] = None,
        cost_usd: float = 0.0,
        step_name: str = "default_step",
        summary: str = "",
    ) -> str:
        self._check_timeout()
        self.tool_calls += 1

        if self.tool_calls > self.max_tool_calls:
            raise RuntimeError("tool call limit exceeded")

        self.cost_usd += cost_usd
        self._check_budget()

        signature = self._make_tool_signature(tool_name, arguments)
        self._check_loop_guard(signature)

        self._append_trace(
            {
                "event_type": "tool_call",
                "step_index": self.step_count,
                "step_name": step_name,
                "tool": tool_name,
                "arguments": arguments or {},
                "tool_signature_hash": signature,
                "cost_usd": cost_usd,
                "timestamp": self._now(),
                "status": "ok",
                "summary": summary,
            }
        )

        return signature

    def record_llm_call(
        self,
        model: str,
        tokens: int = 0,
        cost_usd: float = 0.0,
        step_name: str = "default_step",
        summary: str = "",
    ) -> None:
        self._check_timeout()
        self.llm_calls += 1

        if self.llm_calls > self.max_llm_calls:
            raise RuntimeError("llm call limit exceeded")

        self.cost_usd += cost_usd
        self._check_budget()

        self._append_trace(
            {
                "event_type": "llm_call",
                "step_index": self.step_count,
                "step_name": step_name,
                "model": model,
                "tokens": tokens,
                "cost_usd": cost_usd,
                "timestamp": self._now(),
                "status": "ok",
                "summary": summary,
            }
        )

    def record_retry(self, step_name: str, summary: str = "") -> None:
        self.retries_by_step[step_name] = self.retries_by_step.get(step_name, 0) + 1

        if self.retries_by_step[step_name] > self.max_retries_per_step:
            raise RuntimeError(f"retry limit exceeded for step: {step_name}")

        self._append_trace(
            {
                "event_type": "retry",
                "step_index": self.step_count,
                "step_name": step_name,
                "timestamp": self._now(),
                "status": "ok",
                "summary": summary,
                "retry_count": self.retries_by_step[step_name],
            }
        )

    def summary(self) -> Dict[str, Any]:
        return {
            "run_id": self.run_id,
            "step_count": self.step_count,
            "tool_calls": self.tool_calls,
            "llm_calls": self.llm_calls,
            "cost_usd": round(self.cost_usd, 6),
            "elapsed_seconds": round(self._now() - self.started_at, 3),
        }

    def export_trace(self) -> List[Dict[str, Any]]:
        return self.trace