from dataclasses import dataclass, asdict
from typing import List, Optional

@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    done: bool = False
    tags: List[str] = None
    priority: int = 3 
    command: Optional[List[str]] = None 

    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.command is None:
            self.command = [] 

    def to_dict(self):
        return asdict(self)

def next_id(tasks: List["Task"]) -> int:
    if not tasks:
        return 1
    return max(t.id for t in tasks) + 1

def from_dict(d: dict) -> "Task":
    return Task(
        id=d["id"],
        title=d["title"],
        description=d.get("description", ""),
        done=bool(d.get("done", False)),
        tags=list(d.get("tags", [])),
        priority=int(d.get("priority", 3)),
        command=d.get("command", []) 
    )
