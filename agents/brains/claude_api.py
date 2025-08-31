from __future__ import annotations
import os, json
from typing import Optional, Dict, Any

try:
    from anthropic import Anthropic
except Exception:
    Anthropic = None

SYSTEM_PROMPT = """You are a tool-using planner. Return ONLY a JSON object:
- To use a tool: {"tool": "<name>", "arguments": {...}}
- To answer directly: {"final": "<answer>"}

Available tools:
- calculator(expression: string)
- grep_files(query: string)
- word_count(file_path: string)
- summarize_md(file_path: string, max_chars?: number)
"""

def choose_tool_via_claude(task: str) -> Optional[Dict[str, Any]]:
    """
    Use Claude API to decide which tool to call or return a final answer.
    Falls back to None if no API key or anthropic SDK is installed.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key or Anthropic is None:
        return None

    client = Anthropic(api_key=api_key)
    resp = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=400,
        temperature=0.2,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": task}],
    )

    text = ""
    for block in resp.content:
        if block.type == "text":
            text = block.text
            break

    try:
        data = json.loads(text.strip())
        if isinstance(data, dict) and (("tool" in data and "arguments" in data) or "final" in data):
            return data
    except Exception:
        return None

    return None
