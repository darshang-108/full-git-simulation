"""
Command-line interface for Task Tracker.

Usage:
    python -m task_tracker.cli add "Buy groceries"
    python -m task_tracker.cli list
    python -m task_tracker.cli update 1 --title "Buy vegetables" --status done
    python -m task_tracker.cli delete 1
"""

import argparse
import sys

from task_tracker import __version__
from task_tracker.storage import add_task, list_tasks, update_task, delete_task


def build_parser() -> argparse.ArgumentParser:
    """Construct and return the argument parser."""
    parser = argparse.ArgumentParser(
        prog="task-tracker",
        description="A minimal CLI task tracker.",
    )
    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {__version__}"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # ── add ────────────────────────────────────────────────────────────
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Title of the task")

    # ── list ───────────────────────────────────────────────────────────
    subparsers.add_parser("list", help="List all tasks")

    # ── update ─────────────────────────────────────────────────────────
    upd_parser = subparsers.add_parser("update", help="Update a task")
    upd_parser.add_argument("id", type=int, help="Task ID to update")
    upd_parser.add_argument("--title", help="New title")
    upd_parser.add_argument(
        "--status",
        choices=["pending", "in-progress", "done"],
        help="New status",
    )

    # ── delete ─────────────────────────────────────────────────────────
    del_parser = subparsers.add_parser("delete", help="Delete a task")
    del_parser.add_argument("id", type=int, help="Task ID to delete")

    return parser


def main(argv: list[str] | None = None) -> None:
    """Entry point for the CLI."""
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    if args.command == "add":
        task = add_task(args.title)
        print(f"[+] Added task #{task['id']}: {task['title']}")

    elif args.command == "list":
        tasks = list_tasks()
        if not tasks:
            print("No tasks found.")
        else:
            print(f"{'ID':<5} {'Title':<30} {'Status':<12}")
            print("-" * 47)
            for t in tasks:
                print(f"{t['id']:<5} {t['title']:<30} {t['status']:<12}")

    elif args.command == "update":
        try:
            task = update_task(args.id, title=args.title, status=args.status)
            print(f"[*] Updated task #{task['id']}: {task['title']} [{task['status']}]")
        except (KeyError, ValueError) as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)

    elif args.command == "delete":
        try:
            task = delete_task(args.id)
            print(f"[x] Deleted task #{task['id']}: {task['title']}")
        except KeyError as exc:
            print(f"Error: {exc}", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
