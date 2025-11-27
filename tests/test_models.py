import unittest
from src.models import Task, next_id, from_dict

class TestModels(unittest.TestCase):
    def test_task_to_from_dict(self):
        d = {"id": 5, "title": "t", "description": "d", "done": True, "tags": ["a"], "priority": 2}
        t = from_dict(d)
        self.assertEqual(t.id, 5)
        self.assertEqual(t.title, "t")
        self.assertTrue(t.done)
        self.assertEqual(t.tags, ["a"])
        self.assertEqual(t.priority, 2)

    def test_next_id_empty(self):
        assert next_id([]) == 1

    def test_next_id_nonempty(self):
        from src.models import Task
        tasks = [Task(id=1, title="a"), Task(id=3, title="b")]
        assert next_id(tasks) == 4
