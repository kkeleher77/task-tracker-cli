from __future__ import annotations
import re
from typing import Optional, Tuple, Dict, Any

def choose_tool(task: str) -> Optional[Tuple[str, Dict[str, Any]]]:
    """
    Heuristic planner:
    - If the task looks like math -> calculator
    - If the task asks to find/search/where/mention -> grep_files
    - Otherwise, return None (answer directly)
    """
    t = task.strip()

    # very rough "mathy" detector
    if re.search(r"\d", t) and re.search(r"[+\-/*()]", t):
        # try to extract a plausible expression (fallback to full string)
        expr = re.findall(r"[0-9+\-/*().\s]+", t)
        expression = expr[0].strip() if expr else t
        return ("calculator", {"expression": expression})

    if re.search(r"\b(find|search|grep|where|mention|look for)\b", t, re.I):
        # extract a quoted phrase if present, else use a keyword
        m = re.search(r"['\"]([^'\"]+)['\"]", t)
        query = m.group(1) if m else t.replace("find", "").replace("search", "").strip()
        query = query or "task"
        return ("grep_files", {"query": query})
    
    if re.search(r"\b(word\s*count|count\s*words|wc)\b", t, re.I):
        # try to grab a filename in quotes; otherwise default to README.md
        m = re.search(r"['\"]([^'\"]+)['\"]", t)
        file_path = m.group(1) if m else "README.md"
        return ("word_count", {"file_path": file_path})
    
        # summarization intents
    if re.search(r"\b(summarize|summary|tl;?dr|overview)\b", t, re.I):
        m = re.search(r"['\"]([^'\"]+)['\"]", t)
        file_path = m.group(1) if m else "README.md"
        return ("summarize_md", {"file_path": file_path, "max_chars": 1000})


    return None
