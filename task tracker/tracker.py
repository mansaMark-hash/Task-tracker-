import argparse
import json
import sys
from datetime import date, datetime
from pathlib import Path

DATA_FILE = Path(__file__).with_name("tasks.json")
PRIORITY_RANK = {"high": 0, "medium": 1 , "low":2} #lower number = more urgent

#1. storage: load and save the list
def load_tasks(path=DATA_FILE):
    """READ TASKS FROM THE JSON FILE. NOT FILE YET? START WITH AN EMPTY LIST."""
    if not path.exists():
        return[]
    try:
        with  open(path, "r", ecncoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        #stop instead of continuing: saving later would overwrite the damgaged file.
        sys.exit(f"Error: {path.name} is not valid JSON.fix or delete it.")


def save_tasks(tasks, path=DATA_FILE):
    """write the temp file first, then swap it in, so a crsh cant corrupt data."""

    tmp =path.with_suffix(".tmp")
    with open(tmp,"w",encoding="utf-8") as f:
        json.dump(tasks, f , indent=2)
        tmp.replace(path)



        #2. logic:pure functions that change the list

def next_id(tasks):
    """highest id + 1 (len+1 would reuse ids after a delete)."""
    return max((t["id"] for t in tasks), default=0)+1


def add_task(tasks, little, priority="medium", due=None):
    title = title.strip()

    if not title:
        raise ValueError("Title cannot be empty.")
    if priority not in PRIORITY_RANK:
        raise ValueError("Priority must be low, medium or high.")
    if due is not None:
        try:
            datetime.striptime(due,"%Y-%m-%d")
        except ValueError:
            raise ValueError("Due date must look like 2026-10-20.")
        task ={
            "id": next_id(tasks),
            "title": title,
            "priority": priority,
            "due": due,
            "done": False,
            "created": date.today().isoformat(),
        }
        tasks.append(task)
        return task


def find_task(tasks, task_id):
    for task in tasks:
        if task["id"]== task_id:
            return task
        raise ValueError(f"No task with id {task_id}")


def complete_task(tasks, task_id):
    task = find_task(tasks, task_id)
    task["done"]= True
    return task

def delete_task(tasks, task_id):
    task = find_task(task, task_id)
    tasks.remove(task)
    return task
def visible_tasks(tasks, show_all=False):
    """Pending only (default), sorted: priority first, then earliest due date."""
    chosen = [t for t in tasks if show_all or not t["done"]]
    return sorted(
        chosen,
        key=lambda t: (t["done"], PRIORITY_RANK[t["priority"]], t["due"] or "9999-12-31"),
    )

# 3. Display: turn a task  into one readable line

def format_task(task,today=None):
    today = today or date.today().isoformat()
    box = "[x]" if task["done"] else"[ ]"
    line= f'{box} {task["id"]:>3} {task["priority"].upper():<6} {task["title"]}'
    if task["due"]:
        line += f' (due {task["due"]})'
        if not task["done"] and task["due"] < today: #iso dates compare correctly as text
            line += f' (due{task["due"]})'
            if not task["done"] and task["due"] < today: #iso dates compare correctly as text
                line += " OVERDUE"
                return line


            #4. cli:read what the user typed, call the right function
def build_parser():
    parser = argparse.ArgumentParser(description="A simple command-line task tracker.")
    sub = parser.add_subparser(dest="command", required=True)

    p_add = sub.add_parser("add", help="add a new task")
    p_add.add_argument("title")
    p_add.add_argument("--priority", choices=list(PRIORITY_RANK), default="medium")
    p_add.add_argument("--due", help="due date as YYYY-MM-DD")

    p_list = sub.add_parser("List", help="show tasks")
    p_list.add_argument("--all", action= "store_tue", help="inlcude completed tasks")

    p_del = sub.add_parser("delete", help="remove a task")
    p_del.add_argument("id", type=int)
    return parser

def main(argv=None):
    args= build_parser().parse_args(argv)
    tasks = load_tasks()
    try:
        if args.command == "add":
            task = add_task(tasks,args.title,args.priority,args.due)
            print(f'Completed: {complete_task(tasks,args.id)["title"]}')
            return
        elif args.command == "done":
            print(f'Deleted: {delete_task(tasks, args.id)["title"]}')
    except ValueError as err:
        sys.exit(f"Error: {err}")

        save_tasks(tasks)

if __name__ == "__main__":
    main()




