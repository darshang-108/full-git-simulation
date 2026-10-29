"""
File-based JSON storage for tasks.

Each task is a dict with keys: id, title, status.
Tasks are persisted to a JSON file so data survives between runs.
"""

import json
import os

DEFAULT_FILE = "tasks.json"


def _load(filepath: str = DEFAULT_FILE) -> list[dict]:
    """Load tasks from the JSON file. Returns an empty list if the file
    does not exist or is empty."""
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", encoding="utf-8") as fh:
        try:
            return json.load(fh)
        except json.JSONDecodeError:
            return []


def _save(tasks: list[dict], filepath: str = DEFAULT_FILE) -> None:
    """Write the full task list back to the JSON file."""
    with open(filepath, "w", encoding="utf-8") as fh:
        json.dump(tasks, fh, indent=2)


def _next_id(tasks: list[dict]) -> int:
    """Return the next available integer ID."""
    if not tasks:
        return 1
    return max(t["id"] for t in tasks) + 1


# ── Public API ────────────────────────────────────────────────────────

def add_task(title: str, filepath: str = DEFAULT_FILE) -> dict:
    """Create a new task and persist it. Returns the created task."""
    if not title or not title.strip():
        raise ValueError("Task title cannot be empty.")
    tasks = _load(filepath)
    task = {"id": _next_id(tasks), "title": title.strip(), "status": "pending"}
    tasks.append(task)
    _save(tasks, filepath)
    return task


def list_tasks(filepath: str = DEFAULT_FILE) -> list[dict]:
    """Return all tasks."""
    return _load(filepath)


def update_task(task_id: int, title: str | None = None,
                status: str | None = None,
                filepath: str = DEFAULT_FILE) -> dict:
    """Update an existing task's title and/or status. Returns the updated task."""
    valid_statuses = {"pending", "in-progress", "done"}
    if status and status not in valid_statuses:
        raise ValueError(f"Status must be one of {valid_statuses}.")

    tasks = _load(filepath)
    for task in tasks:
        if task["id"] == task_id:
            if title is not None:
                task["title"] = title.strip()
            if status is not None:
                task["status"] = status
            _save(tasks, filepath)
            return task
    raise KeyError(f"Task with id {task_id} not found.")


def delete_task(task_id: int, filepath: str = DEFAULT_FILE) -> dict:
    """Delete a task by ID. Returns the deleted task."""
    tasks = _load(filepath)
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            removed = tasks.pop(i)
            _save(tasks, filepath)
            return removed
    raise KeyError(f"Task with id {task_id} not found.")
