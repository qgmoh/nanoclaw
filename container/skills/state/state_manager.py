"""
STATE v2 manager for nanoclaw container agents.
Usage: python3 /workspace/project/container/skills/state/state_manager.py <command> [task-id] [args]

Commands:
  init  <task-id> <goal> [proj]   Create new STATE v2 file
  load  <task-id>                  Print STATE JSON
  save  <task-id> <json>           Write STATE JSON (compact)
  done  <task-id> <summary>        Mark complete, print memory harvest prompt
  list                             List active (i != done) state files
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

STATE_DIR = Path("/workspace/group/state")


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def state_path(task_id: str) -> Path:
    return STATE_DIR / f"{task_id}.json"


def load(task_id: str) -> dict:
    p = state_path(task_id)
    if not p.exists():
        raise FileNotFoundError(f"No STATE for task: {task_id}")
    return json.loads(p.read_text())


def save(state: dict) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    state["updated"] = now_iso()
    p = state_path(state["t"])
    p.write_text(json.dumps(state, separators=(",", ":")))


def init(task_id: str, goal: str, proj: str = "nanoclaw") -> dict:
    state = {
        "v": 2,
        "t": task_id,
        "proj": proj,
        "g": goal[:300],
        "s": "",
        "i": "plan first step",
        "created": now_iso(),
        "updated": now_iso(),
        "p": {},
        "k": {"tot": 0, "in": 0, "out": 0, "started_at": now_iso()},
    }
    save(state)
    print(f"STATE created: {state_path(task_id)}")
    print(json.dumps(state, indent=2))
    return state


def mark_done(task_id: str, summary: str) -> None:
    state = load(task_id)
    state["s"] = summary[:300]
    state["i"] = "done"
    save(state)
    print(f"STATE done: {task_id}")
    print("\nMemory harvest — extract 1-3 facts and write to relevant file:")
    print("  preferences.md  — user style, formatting, working preferences")
    print("  projects.md     — active projects with context")
    print("  context.md      — paths, env facts, server config")
    print("  contacts.md     — key people")


def list_active() -> None:
    if not STATE_DIR.exists():
        print("No state directory found.")
        return
    active = []
    for f in sorted(STATE_DIR.glob("*.json")):
        if f.parent.name == "templates":
            continue
        try:
            s = json.loads(f.read_text())
            if s.get("i") and not str(s["i"]).startswith("done"):
                active.append(s)
        except Exception:
            pass
    if not active:
        print("No active STATE files.")
    for s in active:
        print(f"  {s['t']}: {s['i']}")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    if cmd == "init":
        task_id = sys.argv[2]
        goal = sys.argv[3]
        proj = sys.argv[4] if len(sys.argv) > 4 else "nanoclaw"
        init(task_id, goal, proj)
    elif cmd == "load":
        state = load(sys.argv[2])
        print(json.dumps(state, indent=2))
    elif cmd == "save":
        state = json.loads(sys.argv[3])
        save(state)
        print(f"Saved: {state['t']}")
    elif cmd == "done":
        mark_done(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "Task complete")
    elif cmd == "list":
        list_active()
    else:
        print(__doc__)
