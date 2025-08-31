# Task Tracker CLI

A tiny command-line task manager written in Python. Stores tasks in a JSON file.

## Quickstart
```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt # optional (not needed yet)
python src/task_manager.py add "Try the CLI" --due 2025-09-05
python src/task_manager.py list

