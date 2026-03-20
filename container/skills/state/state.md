# STATE System — Low-Token Task Resumption

Use STATE for any multi-step task. It saves ~82% tokens by storing minimal progress JSON instead of replaying full conversation history.

The host automatically injects your memory files and any active STATE into every session — you will see them in a `<context>` block at the start of each prompt. If an active STATE is present, resume from the `"i"` field immediately.

## State Directory

```
/workspace/group/state/
```

State files: `{task-id}.json` — one file per task, lives here for all agents.

## STATE Format

```json
{
  "v": 1,
  "t": "task-id",
  "g": "Goal (≤300 chars)",
  "s": "Summary of work done (≤300 chars)",
  "i": "Next action to take (≤300 chars)",
  "p": { "any": "params needed" }
}
```

| Field | Meaning |
|-------|---------|
| `v` | Schema version (always 1) |
| `t` | Task identifier = filename in kebab-case |
| `g` | Goal — what you are achieving |
| `s` | Summary — what has been completed so far |
| `i` | Next action to take. Set to `"done"` when complete |
| `p` | Extra key-value context (paths, flags, etc.) |

## Quick Bash Commands

### Check for existing state
```bash
cat /workspace/group/state/{task-id}.json 2>/dev/null
```

### Create new state
```bash
python3 -c "
import json, pathlib
state = {'v':1,'t':'task-id','g':'Goal here','s':'','i':'First step','p':{}}
p = pathlib.Path('/workspace/group/state'); p.mkdir(exist_ok=True)
(p / 'task-id.json').write_text(json.dumps(state, indent=2))
print('STATE created')
"
```

### Update state after completing a step
```bash
python3 -c "
import json, pathlib
p = pathlib.Path('/workspace/group/state/task-id.json')
s = json.loads(p.read_text())
s['s'] = 'Completed step 1: read config, found issue'
s['i'] = 'Next: fix the timeout value in settings.py'
p.write_text(json.dumps(s, indent=2))
"
```

### Mark task done (triggers memory harvest)
```bash
python3 -c "
import json, pathlib
p = pathlib.Path('/workspace/group/state/task-id.json')
s = json.loads(p.read_text())
s['s'] = 'All steps complete'
s['i'] = 'done'
p.write_text(json.dumps(s, indent=2))
"
```

### List all state files
```bash
ls /workspace/group/state/*.json 2>/dev/null
```

## Workflow

1. **Session start** → host injects active STATE into `<context>` block automatically
2. **Resume** → read `i` field and continue from there
3. **After each step** → update `s` (what was done) and `i` (what's next), save
4. **When done** → set `i` to `"done"`, then harvest 1-3 facts into memory files

## When to Use STATE

- **Use for**: any task with 2+ steps, debugging, implementing features, research across multiple files
- **Skip for**: single read/grep/one-line answer

## Memory Harvest (when i = "done")

1. Identify 1-3 new facts learned during the task
2. Write them into the relevant memory file:
   - `preferences.md` — user style, formatting rules, working preferences
   - `projects.md` — active projects with context
   - `context.md` — paths, env facts, server config
   - `contacts.md` — key people
3. If a new memory file was created, add it to `INDEX.md`
4. Keep every memory file under 50 lines — trim stale facts if needed
