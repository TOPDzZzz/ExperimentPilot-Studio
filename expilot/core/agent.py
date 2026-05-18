import time
from typing import Generator, Dict, Any
from expilot.core.llm import LLMClient
from expilot.tools.registry import get_tool_descriptions, call_tool
from expilot.core.memory import load_memory, add_recent_task
from expilot.core.trace import log_trace

PROFILE_PROMPTS = {
    "general": "You are a general-purpose assistant. Plan, summarize, and execute tasks efficiently.",
    "code": "You are a senior code assistant. Scan projects, analyze logic, and locate bugs.",
    "data": "You are a data analysis assistant. Analyze CSV/Excel statistics, handle missing values, and suggest visualizations.",
    "ml": "You are an ML experiment assistant. Analyze metrics, compare results, and suggest improvements.",
    "file": "You are a file processing assistant. Extract, rewrite content, and generate reports.",
    "research": "You are a research assistant. Organize materials, compare options, and generate research reports.",
}


class AgentEngine:
    def __init__(self, max_steps: int = 8, profile: str = "general"):
        self.llm = LLMClient()
        self.max_steps = min(max_steps, 30)
        self.profile = profile

    def _build_prompt(self, task: str, history: list) -> tuple:
        memory = load_memory()
        sys_prompt = (
            f"{PROFILE_PROMPTS.get(self.profile, PROFILE_PROMPTS['general'])}\n\n"
            f"Available tools:\n{get_tool_descriptions()}\n\n"
            "Rules:\n"
            "1. Use tools ONLY when information is insufficient. If you already have enough info, return final_answer.\n"
            "2. Never guess file contents — always read first.\n"
            "3. Keep steps minimal. Most tasks need 1-3 steps max.\n"
            "4. Prefer final_answer over extra tool calls when possible.\n"
            "5. Stay within workspace/ sandbox.\n"
            "6. Respond in the same language as the user's task.\n"
            "7. CRITICAL: When calling a tool, you MUST include ALL required parameters marked (REQUIRED) in the tool description. Do NOT call a tool with empty arguments.\n\n"
            "Output format: You MUST respond with a JSON object in <answer> tags:\n"
            "<answer>{\"thought\": \"your reasoning\", \"action_type\": \"final\" or \"tool\", \"tool_call\": {\"tool_name\": \"...\", \"arguments\": {...}} or null, \"final_answer\": \"...\" or null}</answer>"
        )
        recent_memory = memory.get("recent_tasks", [])[-3:]
        user_prompt = (
            f"Task: {task}\n\n"
            f"Recent tasks: {recent_memory}\n\n"
            f"Previous steps: {history}\n\n"
            "Output your next decision."
        )
        return sys_prompt, user_prompt

    def _get_final_answer(self, task: str, history: list) -> str:
        recent_memory = load_memory().get("recent_tasks", [])[-3:]
        final_prompt = (
            f"Task: {task}\n\n"
            f"Recent tasks: {recent_memory}\n\n"
            f"Previous steps: {history}\n\n"
            "You have reached the maximum number of steps. Please provide a final answer based on the information gathered so far."
        )
        final_action = self.llm.decide(
            "You are a helpful assistant. Provide a clear, concise final answer based on the available information.",
            final_prompt,
            history,
        )
        if isinstance(final_action, str):
            return final_action
        return final_action.final_answer or "Task completed with partial results. Please try again with a simpler task."

    def run_stream(self, task: str, history: list = None) -> Generator[Dict[str, Any], None, None]:
        if history is None:
            history = []

        yield {"type": "thought", "content": f"Analyzing task: {task[:100]}"}

        steps_used = 0

        for step in range(1, self.max_steps + 1):
            sys_prompt, user_prompt = self._build_prompt(task, history)
            try:
                action = self.llm.decide(sys_prompt, user_prompt, history)
            except Exception as e:
                yield {"type": "error", "content": f"LLM call failed: {e}"}
                return

            # decide() 可能返回字符串：403 限流提示或模型直接输出的文本
            if isinstance(action, str):
                if action.startswith("⚠️"):
                    yield {"type": "error", "content": action}
                else:
                    yield {"type": "final", "content": action}
                add_recent_task(task)
                return

            steps_used = step

            log_trace("decision", f"Step {step}", {"thought": action.thought, "type": action.action_type}, str(action))

            # ── Final answer ──
            if action.action_type == "final":
                yield {"type": "final", "content": action.final_answer or ""}
                add_recent_task(task)
                return

            # ── Tool call ──
            if action.tool_call:
                yield {
                    "type": "tool_call",
                    "tool_name": action.tool_call.tool_name,
                    "arguments": action.tool_call.arguments,
                    "content": action.thought,
                }

                try:
                    result = str(call_tool(action.tool_call.tool_name, action.tool_call.arguments) or "")
                except Exception as e:
                    result = f"Tool error: {e}"

                preview = result[:300] + "..." if len(result) > 300 else result
                log_trace("tool", action.tool_call.tool_name, action.tool_call.arguments, result[:500])

                yield {"type": "observation", "tool_name": action.tool_call.tool_name, "content": preview}

                history.append({"role": "assistant", "content": f"[Tool] {action.tool_call.tool_name} -> {result[:300]}"})

                # Brief pause between steps to avoid RPM bursts
                if step < self.max_steps:
                    time.sleep(1)

            # ── Max steps reached ──
            if step == self.max_steps:
                answer = self._get_final_answer(task, history)
                yield {"type": "final", "content": answer}
                add_recent_task(task)
                return

        yield {"type": "error", "content": "Agent execution error"}

    # Keep run() for backward compatibility (pages that still use it)
    def run(self, task: str, history: list = None) -> dict:
        trace = []
        answer = ""
        status = "error"
        steps = 0

        for step_info in self.run_stream(task, history):
            if step_info["type"] == "tool_call":
                steps += 1
                trace.append({
                    "step": steps, "type": "thought", "content": step_info.get("content", "")
                })
            elif step_info["type"] == "observation":
                trace.append({
                    "step": steps, "type": "tool_call",
                    "tool": step_info.get("tool_name", ""),
                    "input": {}, "output": step_info.get("content", ""),
                })
            elif step_info["type"] == "final":
                steps += 1
                answer = step_info["content"]
                status = "done"
                trace.append({"step": steps, "type": "final_answer", "content": answer})
                break
            elif step_info["type"] == "error":
                steps += 1
                answer = step_info["content"]
                status = "error"
                trace.append({"step": steps, "type": "error", "content": answer})
                break

        return {"status": status, "answer": answer, "steps": steps, "trace": trace}
