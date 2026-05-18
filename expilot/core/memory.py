import json
from pathlib import Path

MEMORY_PATH = Path("expilot/storage/memory.json")
MEMORY_PATH.parent.mkdir(parents=True, exist_ok=True)

def load_memory() -> dict:
    if not MEMORY_PATH.exists():
        return {"user_preferences": {}, "recent_tasks": [], "project_context": {}}
    return json.loads(MEMORY_PATH.read_text(encoding="utf-8"))

def save_memory(memory: dict):
    MEMORY_PATH.write_text(json.dumps(memory, ensure_ascii=False, indent=2), encoding="utf-8")

def add_recent_task(task: str):
    memory = load_memory()
    memory.setdefault("recent_tasks", [])
    memory["recent_tasks"].append(task)
    memory["recent_tasks"] = memory["recent_tasks"][-20:]
    save_memory(memory)