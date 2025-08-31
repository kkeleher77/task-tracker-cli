✅ Task Tracker CLI + Mini AI Agent

This project started as a simple command-line task manager written in Python, and has now grown to include a mini AI agent skeleton.

Task Tracker CLI → add, complete, list, and delete tasks (all stored locally in JSON).

AI Agent → decides which tool to use (search, calculator, word count, summarize) using either:

a heuristic brain (free, built-in, no setup needed), or

an optional Claude API brain (if you provide an Anthropic API key).

📂 Project Structure
task-tracker-cli/
├── src/
│   └── task_manager.py         # task tracker CLI
├── tasks.json                  # stores tasks
├── agents/
│   ├── simple_agent/
│   │   ├── agent.py            # orchestrator
│   │   ├── brain.py            # heuristic brain (default)
│   │   └── tools.py            # calculator, grep_files, word_count, summarize_md
│   └── brains/
│       └── claude_api.py       # optional Claude-powered brain

🚀 Quickstart (Task Tracker CLI)

Clone the repo and set up your environment:

git clone https://github.com/kkeleher77/task-tracker-cli.git
cd task-tracker-cli

python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt # optional, not needed yet


Run the CLI:

python src/task_manager.py add "My first task" --due 2025-09-05
python src/task_manager.py list
python src/task_manager.py done 1
python src/task_manager.py del 1

🤖 Mini AI Agent (Free Route)

The repo also includes a simple AI agent that decides what to do based on your prompt.

Available Tools

calculator(expression) → math (2+2, sqrt(2) * pi, etc.)

grep_files(query) → search your repo for text

word_count(file_path) → count lines, words, chars in a file

summarize_md(file_path) → list headings + preview content in a Markdown file

Heuristic Brain (default)

The default brain (agents/simple_agent/brain.py) uses keyword rules to decide which tool to call. No API key required.

Run the Agent

From repo root:

# 🔎 search the repo
python -m agents.simple_agent.agent "find 'task' in the repository"

# 🧮 calculator
python -m agents.simple_agent.agent "what is sqrt(2) * pi ?"

# 📊 word count
python -m agents.simple_agent.agent "word count 'README.md'"

# 📄 summarize markdown
python -m agents.simple_agent.agent "summarize README.md"

🤝 Optional: Claude-Powered Brain

You can replace the heuristic brain with a Claude-powered brain (agents/brains/claude_api.py).

Requirements

Anthropic account + API key

Installed dependencies:

pip install anthropic python-dotenv

Setup

Create a .env file in the repo root:

ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxx


Run the agent as usual:

python -m agents.simple_agent.agent "summarize README.md"

How It Works

The agent first tries to use Claude (choose_tool_via_claude).

If Claude is unavailable (no key, SDK not installed, or failure), it falls back to the heuristic brain.

Claude will return JSON like:

{"tool": "summarize_md", "arguments": {"file_path": "README.md", "max_chars": 1000}}

✅ Next Steps

Add more tools (e.g., web_fetch, github_issue_create)

Write pytest tests for tools and brain logic

Set up CI (GitHub Actions) to run tests automatically

📸 Demo
$ python -m agents.simple_agent.agent "find 'task' in the repository"
🔎 Searched repo for `task`. Matches:
README.md:1: # ✅ Task Tracker CLI
...

$ python -m agents.simple_agent.agent "what is sqrt(2) * pi ?"
🧮 Used calculator on `sqrt(2) * pi` → **4.442882938...**

$ python -m agents.simple_agent.agent "word count 'README.md'"
📊 README.md: 52 lines, 210 words, 1234 chars

$ python -m agents.simple_agent.agent "summarize README.md"
📄 Summary of README.md:
Headings:
- # ✅ Task Tracker CLI
- ## 🚀 Quickstart
...