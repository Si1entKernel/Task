import json
from pathlib import Path
from typing import List
from .models import Task, from_dict, next_id

class StorageError(Exception):
    pass

class JSONStorage:
    def __init__(self, path):
        self.path = Path(path)

    def _ensure_file(self):
        if not self.path.exists():
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text(json.dumps({"tasks": []}, indent=2), encoding="utf-8")

    def load_tasks(self) -> List[Task]:
        self._ensure_file()
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
            tasks = [from_dict(d) for d in raw.get("tasks", [])]
            return tasks
        except Exception as e:
            raise StorageError(f"Failed to load tasks: {e}")

    def save_tasks(self, tasks: List[Task]) -> None:
        self._ensure_file()
        try:
            raw = {"tasks": [t.to_dict() for t in tasks]}
            self.path.write_text(json.dumps(raw, indent=2), encoding="utf-8")
        except Exception as e:
            raise StorageError(f"Failed to save tasks: {e}")

    def add_task(self, title: str, description: str = "", tags=None, priority: int = 3) -> Task:
        tasks = self.load_tasks()
        nid = next_id(tasks)
        task = Task(id=nid, title=title, description=description, tags=tags or [], priority=priority)
        tasks.append(task)
        self.save_tasks(tasks)
        return task

    def find_task(self, task_id: int) -> Task:
        tasks = self.load_tasks()
        for t in tasks:
            if t.id == task_id:
                return t
        raise StorageError(f"Task with id {task_id} not found")

    def update_task(self, updated: Task) -> None:
        tasks = self.load_tasks()
        for i, t in enumerate(tasks):
            if t.id == updated.id:
                tasks[i] = updated
                self.save_tasks(tasks)
                return
        raise StorageError(f"Task with id {updated.id} not found")

    def delete_task(self, task_id: int) -> None:
        tasks = self.load_tasks()
        tasks = [t for t in tasks if t.id != task_id]
        self.save_tasks(tasks)
