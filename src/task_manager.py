import argparse
import json
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).resolve().parent.parent / "tasks.json"

def load_tasks():
    if not DB_PATH.exists():
        return []
    with open(DB_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_tasks(tasks):
    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)

def add_task(title, due=None):
    tasks = load_tasks()
    task = {
        "id": (max([t["id"] for t in tasks]) + 1) if tasks else 1,
        "title": title,
        "done": False,
        "created_at": datetime.utcnow().isoformat() + "Z",
        "due": due,
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"✅ Added: {task['id']} - {task['title']}")

def list_tasks(show_all=False):
    tasks = load_tasks()
    for t in tasks:
        if show_all or not t["done"]:
            status = "✔" if t["done"] else "•"
            due = f" (due {t['due']})" if t.get("due") else ""
            print(f"{status} {t['id']}: {t['title']}{due}")

def complete_task(task_id):
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = True
            save_tasks(tasks)
            print(f"🎉 Completed task {task_id}")
            return
    print(f"⚠️ No task found with id {task_id}")

def delete_task(task_id):
    tasks = load_tasks()
    new_tasks = [t for t in tasks if t["id"] != task_id]
    if len(new_tasks) == len(tasks):
        print(f"⚠️ No task found with id {task_id}")
    else:
        save_tasks(new_tasks)
        print(f"🗑️ Deleted task {task_id}")

def main():
    parser = argparse.ArgumentParser(prog="tasks", description="Simple Task Tracker CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    add_p = sub.add_parser("add", help="Add a new task")
    add_p.add_argument("title", type=str, help="Task title (quote multi-word)")
    add_p.add_argument("--due", type=str, help="Optional due date (e.g., 2025-09-15)")

    list_p = sub.add_parser("list", help="List tasks")
    list_p.add_argument("--all", action="store_true", help="Include completed")

    done_p = sub.add_parser("done", help="Complete a task by id")
    done_p.add_argument("id", type=int)

    del_p = sub.add_parser("del", help="Delete a task by id")
    del_p.add_argument("id", type=int)

    args = parser.parse_args()

    if args.cmd == "add":
        add_task(args.title, due=args.due)
    elif args.cmd == "list":
        list_tasks(show_all=args.all)
    elif args.cmd == "done":
        complete_task(args.id)
    elif args.cmd == "del":
        delete_task(args.id)

if __name__ == "__main__":
    main()

