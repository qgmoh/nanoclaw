# STATE v2 — Low-Token Task Resumption

Use STATE for any task with 2+ steps. Saves ~82% tokens vs replaying full conversation history.

The host injects active STATE into every session via `<context>` block. If present, **resume from `i` immediately**.

## State Directory

```
/workspace/group/state/
```

## STATE v2 Format

```json
{
  "v": 2,
  "t": "task-id",
  "proj": "nanoclaw",
  "g": "Goal ≤300 chars",
  "s": "Summary of work done ≤300 chars",
  "i": "Next action ≤300 chars",
  "created": "2026-03-20T10:00:00Z",
  "updated": "2026-03-20T10:05:00Z",
  "p": {},
  "k": {"tot": 0, "in": 0, "out": 0}
}
```

| Field | Meaning |
|-------|---------|
| `v` | Schema version — always 2 |
| `t` | Task ID = filename (kebab-case) |
| `proj` | Project: nanoclaw, herv3, salad |
| `g` | Goal — what you are achieving |
| `s` | Summary — what has been completed |
| `i` | Next action. Set `"done"` when complete |
| `created` | ISO timestamp, set once at creation |
| `updated` | ISO timestamp, update on every save |
| `p` | Extra context (paths, flags, etc.) |
| `k` | Token counter — update each step: `tot`=total, `in`=input, `out`=output |

## Quick Commands

**Create:**
```bash
python3 /workspace/project/container/skills/state/state_manager.py init my-task-id "Goal here" nanoclaw
```

**Or inline:**
```bash
python3 -c "
import json, pathlib
from datetime import datetime, timezone
now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
s = {'v':2,'t':'task-id','proj':'nanoclaw','g':'Goal','s':'','i':'First step','created':now,'updated':now,'p':{},'k':{'tot':0,'in':0,'out':0}}
p = pathlib.Path('/workspace/group/state'); p.mkdir(exist_ok=True)
(p / 'task-id.json').write_text(json.dumps(s))
print('STATE created')
"
```

**Update after a step:**
```bash
python3 -c "
import json, pathlib
from datetime import datetime, timezone
p = pathlib.Path('/workspace/group/state/task-id.json')
s = json.loads(p.read_text())
s['s'] = 'Step 1 done: found the issue'
s['i'] = 'Step 2: fix timeout in settings.py'
s['k']['tot'] += 800; s['k']['in'] += 200; s['k']['out'] += 600
s['updated'] = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
p.write_text(json.dumps(s))
"
```

**Mark done:**
```bash
python3 /workspace/project/container/skills/state/state_manager.py done task-id "All steps complete"
```

## Workflow

1. **Session start** → check `<context>` block for active STATE
2. **Resume** → read `i` and continue from there, do NOT repeat `s`
3. **After each step** → update `s`, `i`, `k` counters, `updated` timestamp, save
4. **When done** → set `i = "done"`, then do memory harvest

## When to Use

- **Use**: 2+ step tasks, debugging, feature implementation, multi-file changes
- **Skip**: single read, grep, one-line answer

## Memory Harvest (when i = "done")

Extract 1-3 new facts and write to the relevant memory file:

| File | What goes there |
|------|----------------|
| `preferences.md` | User style, formatting rules, working preferences |
| `projects.md` | Active projects with context |
| `context.md` | Paths, env facts, server config |
| `contacts.md` | Key people |

After writing: check the file stays under 50 lines. Add to `INDEX.md` if a new file was created.

## Templates

Pre-built STATE files for common tasks are in `/workspace/group/state/templates/`.

```bash
# List templates
ls /workspace/group/state/templates/

# Use a template (copy and fill in your task-id)
python3 -c "
import json, pathlib
from datetime import datetime, timezone
now = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
t = json.loads(pathlib.Path('/workspace/group/state/templates/generic-task.json').read_text())
t['t'] = 'my-actual-task-id'
t['g'] = 'My actual goal'
t['created'] = now; t['updated'] = now
pathlib.Path('/workspace/group/state/my-actual-task-id.json').write_text(json.dumps(t))
"
```
