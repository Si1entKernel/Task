import unittest
import tempfile
import json
from pathlib import Path
from src.storage import JSONStorage
from src.models import Task

class TestStorage(unittest.TestCase):
    def setUp(self):
        self.tmpfile = Path(tempfile.mktemp(suffix=".json"))
        self.tmpfile.write_text(json.dumps({"tasks": []}), encoding="utf-8")
        self.storage = JSONStorage(self.tmpfile)

    def tearDown(self):
        try:
            self.tmpfile.unlink()
        except Exception:
            pass

    def test_add_and_load(self):
        t = self.storage.add_task("hello", "desc", tags=["x"], priority=1)
        tasks = self.storage.load_tasks()
        assert any(tt.id == t.id and tt.title == "hello" for tt in tasks)

    def test_update(self):
        t = self.storage.add_task("to_update")
        t.title = "updated"
        self.storage.update_task(t)
        loaded = self.storage.load_tasks()
        assert any(x.title == "updated" for x in loaded)

    def test_delete(self):
        t = self.storage.add_task("todel")
        self.storage.delete_task(t.id)
        loaded = self.storage.load_tasks()
        assert all(x.id != t.id for x in loaded)
