from __future__ import annotations
from pathlib import Path
from typing import List

import math

def calculator(expression: str) -> str:
    """
    Very simple, safe-ish calculator for + - * / and a few math funcs.
    """
    allowed = {k: getattr(math, k) for k in ["sqrt", "pow", "sin", "cos", "tan", "pi", "e"]}
    allowed["__builtins__"] = {}
    try:
        result = eval(expression, allowed, {})
        return str(result)
    except Exception as e:
        return f"Calculator error: {e}"

def grep_files(query: str, root: str = ".") -> str:
    from pathlib import Path
    root_path = Path(root)
    hits = []
    exts = {".py", ".md", ".txt", ".json", ".toml", ".yml", ".yaml"}
    ignore_dirs = {".git", ".venv", "__pycache__", ".pytest_cache", ".github"}

    for p in root_path.rglob("*"):
        if p.is_dir():
            # skip ignored directories early
            if p.name in ignore_dirs:
                # tell rglob to skip walking this directory
                continue
        if not p.is_file():
            continue
        if p.suffix and p.suffix.lower() not in exts:
            continue
        # skip any file inside an ignored dir
        if any(part in ignore_dirs for part in p.parts):
            continue

        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        q = query.lower()
        for i, line in enumerate(text.splitlines()):
            if q in line.lower():
                hits.append(f"{p}:{i+1}: {line.strip()}")
        if len(hits) > 200:
            break

    return "\n".join(hits[:200]) if hits else "No matches."

def word_count(file_path: str) -> str:
    """
    Count words, lines, and characters in a text file.
    """
    from pathlib import Path
    p = Path(file_path)
    if not p.exists() or not p.is_file():
        return f"File not found: {file_path}"
    try:
        text = p.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        return f"Could not read {file_path}: {e}"
    lines = text.splitlines()
    words = text.split()
    chars = len(text)
    return f"{file_path}: {len(lines)} lines, {len(words)} words, {chars} chars"

def summarize_md(file_path: str, max_chars: int = 1000) -> str:
    """
    Lightweight markdown 'summary':
    - lists top-level headings (lines starting with '#')
    - returns the first ~max_chars of body text (stripped of excessive whitespace)
    """
    from pathlib import Path
    p = Path(file_path)
    if not p.exists() or not p.is_file():
        return f"File not found: {file_path}"
    try:
        text = p.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        return f"Could not read {file_path}: {e}"

    lines = text.splitlines()
    headings = [ln.strip() for ln in lines if ln.strip().startswith("#")]
    # crude body cleanup
    cleaned = "\n".join(ln.rstrip() for ln in lines if ln.strip())
    teaser = cleaned[:max_chars].rstrip()
    if len(cleaned) > max_chars:
        teaser += " ..."

    out = []
    if headings:
        out.append("Headings:")
        for h in headings[:10]:
            out.append(f"- {h}")
        if len(headings) > 10:
            out.append(f"- (+{len(headings)-10} more)")
        out.append("")  # blank line

    out.append(f"Preview ({min(max_chars, len(cleaned))} chars):")
    out.append(teaser)
    return "\n".join(out)


