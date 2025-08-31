from __future__ import annotations
import re
from typing import Optional, Tuple, Dict, Any

def choose_tool(task: str) -> Optional[Tuple[str, Dict[str, Any]]]:
    t = task.strip()

    # 👇 Word count intents (moved up BEFORE math check)
    if re.search(r"\b(word\s*count|count\s*words|wc)\b", t, re.I):
        # try to grab a filename in quotes; otherwise default to README.md
        m = re.search(r"['\"]([^'\"]+)['\"]", t)
        file_path = m.group(1) if m else "README.md"
        return ("word_count", {"file_path": file_path})

    # 👇 Summarize intents (still before math too)
    if re.search(r"\b(summarize|summary|tl;?dr|overview)\b", t, re.I):
        m = re.search(r"['\"]([^'\"]+)['\"]", t)
        file_path = m.group(1) if m else "README.md"
        return ("summarize_md", {"file_path": file_path, "max_chars": 1000})

    # 👇 Math detection
    if re.search(r"\d|sqrt|sin|cos|tan|pi|e", t, re.I) and re.search(r"[+\-/*()]", t):
        m = re.search(r"[`'\"]([^`'\"]+)[`'\"]", t)
        if m:
            expression = m.group(1).strip()
        else:
            m2 = re.search(r"(?:sqrt|sin|cos|tan|pi|e|\d)[A-Za-z0-9_+\-/*().\s]*", t, re.I)
            expression = (m2.group(0) if m2 else t).strip(" ?!.")
            expression = re.sub(r"^(what(\s+is|'s)?|is|calculate|compute|please)\s+", "", expression, flags=re.I)
        return ("calculator", {"expression": expression})

    # 👇 Search in repo
    if re.search(r"\b(find|search|grep|where|mention|look for)\b", t, re.I):
        m = re.search(r"['\"]([^'\"]+)['\"]", t)
        query = m.group(1) if m else t.replace("find", "").replace("search", "").strip()
        query = query or "task"
        return ("grep_files", {"query": query})

    return None
