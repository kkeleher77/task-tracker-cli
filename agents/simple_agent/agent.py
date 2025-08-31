from __future__ import annotations
import sys
from typing import Dict, Any

from .brain import choose_tool
from .tools import calculator, grep_files, word_count, summarize_md

try:
    from agents.brains.claude_api import choose_tool_via_claude
except Exception:
    choose_tool_via_claude = None

TOOL_FUNCS = {
    "calculator": calculator,
    "grep_files": grep_files,
    "word_count": word_count,
    "summarize_md": summarize_md,
}

def dispatch(tool_name: str, args: Dict[str, Any]) -> str:
    fn = TOOL_FUNCS.get(tool_name)
    if not fn:
        return f"Unknown tool: {tool_name}"
    try:
        return fn(**args)
    except TypeError as e:
        return f"Tool argument error: {e}"
    except Exception as e:
        return f"Tool execution error: {e}"

def solve(task: str) -> str:
    plan = None

    # 👇 Try Claude API brain first (only works if SDK + API key are available)
    if choose_tool_via_claude:
        plan = choose_tool_via_claude(task)

    # 👇 Fallback to heuristic brain
    if plan is None:
        plan = choose_tool(task)

    if not plan:
        return f"I didn't need a tool for that. Here's my take:\n{task}"

    tool_name, arguments = plan
    tool_result = dispatch(tool_name, arguments)

    # 👇 Simple "agent-y" finalization messages
    if tool_name == "calculator":
        return f"🧮 Used calculator on `{arguments['expression']}` → **{tool_result}**"
    elif tool_name == "grep_files":
        header = f"🔎 Searched repo for `{arguments['query']}`. Matches:"
        return header + ("\n" + tool_result if tool_result else "\nNo matches.")
    elif tool_name == "word_count":
        return f"📊 {tool_result}"
    elif tool_name == "summarize_md":
        return f"📄 Summary of {arguments['file_path']}:\n{tool_result}"
    else:
        return tool_result


if __name__ == "__main__":
    user_task = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Find 'task' in the repo"
    print(solve(user_task))
