"""
Tests for Task Tracker storage module.

Run with:  pytest -v
"""

import os
import json
import pytest

from task_tracker.storage import add_task, list_tasks, update_task, delete_task


@pytest.fixture(autouse=True)
def tmp_storage(tmp_path):
    """Use a temp file for every test so tests never interfere."""
    filepath = str(tmp_path / "test_tasks.json")
    # Monkey-patch the default filepath for each public function
    pytest.filepath = filepath
    yield filepath
    if os.path.exists(filepath):
        os.remove(filepath)


# ── add_task ──────────────────────────────────────────────────────────

class TestAddTask:
    def test_add_creates_task(self, tmp_storage):
        task = add_task("Write README", filepath=tmp_storage)
        assert task["id"] == 1
        assert task["title"] == "Write README"
        assert task["status"] == "pending"

    def test_add_strips_whitespace(self, tmp_storage):
        task = add_task("  Trim me  ", filepath=tmp_storage)
        assert task["title"] == "Trim me"

    def test_add_increments_id(self, tmp_storage):
        add_task("First", filepath=tmp_storage)
        second = add_task("Second", filepath=tmp_storage)
        assert second["id"] == 2

    def test_add_empty_title_raises(self, tmp_storage):
        with pytest.raises(ValueError, match="empty"):
            add_task("", filepath=tmp_storage)

    def test_add_whitespace_only_title_raises(self, tmp_storage):
        with pytest.raises(ValueError, match="empty"):
            add_task("   ", filepath=tmp_storage)


# ── list_tasks ────────────────────────────────────────────────────────

class TestListTasks:
    def test_list_empty(self, tmp_storage):
        assert list_tasks(filepath=tmp_storage) == []

    def test_list_returns_all(self, tmp_storage):
        add_task("A", filepath=tmp_storage)
        add_task("B", filepath=tmp_storage)
        assert len(list_tasks(filepath=tmp_storage)) == 2


# ── update_task ───────────────────────────────────────────────────────

class TestUpdateTask:
    def test_update_title(self, tmp_storage):
        add_task("Old", filepath=tmp_storage)
        updated = update_task(1, title="New", filepath=tmp_storage)
        assert updated["title"] == "New"

    def test_update_status(self, tmp_storage):
        add_task("Do it", filepath=tmp_storage)
        updated = update_task(1, status="done", filepath=tmp_storage)
        assert updated["status"] == "done"

    def test_update_invalid_status_raises(self, tmp_storage):
        add_task("Task", filepath=tmp_storage)
        with pytest.raises(ValueError, match="Status must be"):
            update_task(1, status="invalid", filepath=tmp_storage)

    def test_update_missing_id_raises(self, tmp_storage):
        with pytest.raises(KeyError, match="not found"):
            update_task(999, title="Nope", filepath=tmp_storage)


# ── delete_task ───────────────────────────────────────────────────────

class TestDeleteTask:
    def test_delete_removes_task(self, tmp_storage):
        add_task("Remove me", filepath=tmp_storage)
        deleted = delete_task(1, filepath=tmp_storage)
        assert deleted["title"] == "Remove me"
        assert list_tasks(filepath=tmp_storage) == []

    def test_delete_missing_id_raises(self, tmp_storage):
        with pytest.raises(KeyError, match="not found"):
            delete_task(42, filepath=tmp_storage)


# ── persistence ───────────────────────────────────────────────────────

class TestPersistence:
    def test_data_survives_reload(self, tmp_storage):
        add_task("Persist me", filepath=tmp_storage)
        # Simulate a fresh load
        tasks = list_tasks(filepath=tmp_storage)
        assert len(tasks) == 1
        assert tasks[0]["title"] == "Persist me"
