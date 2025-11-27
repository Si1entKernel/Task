import json
import subprocess
from pathlib import Path
from .storage import JSONStorage
from .models import Task


def run_task(task: Task):
    if not task.command:
        print(f"[!] Task #{task.id} has no command to execute.")
        return

    cmd_display = " ".join(str(x) for x in task.command)
    print(f"\n=== Running Task ===")

    try:
        result = subprocess.run(
            task.command,
            capture_output=True,
            text=True,
            shell=True  
        )
        print("--- STDOUT ---")
        print("--- STDERR ---")
        print(f"Exit code: {result.returncode}")
    except Exception as e:
        print(f"[!] Failed to execute Task #{task.id}: {e}")


def main(argv=None):
    cfg_path = Path("config.json")
    if not cfg_path.exists():
        print("[!] config.json not found.")
        return

    try:
        config = json.loads(cfg_path.read_text(encoding="utf-8"))
        data_file = config.get("data_file", "tasks.json")
    except Exception as e:
        print("[!] Failed to read config.json:", e)
        return

    storage = JSONStorage(data_file)
    tasks = storage.load_tasks()

    if not tasks:
        print("[*] No tasks found in", data_file)
        return

    print(f"[*] Loaded {len(tasks)} tasks from {data_file}")
    for task in tasks:
        run_task(task)


if __name__ == "__main__":
    main()
