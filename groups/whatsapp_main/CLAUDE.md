# Ai-group — Amy

## Server Access

The host's home directory is mounted at `/workspace/extra/home/qgmoh/`.

- Files & projects: `/workspace/extra/home/qgmoh/`
- Projects folder: `/workspace/extra/home/qgmoh/projects/` (**always use this exact path**)
- SSH key (GitHub): `/workspace/extra/home/qgmoh/.ssh/id_ed25519`

## GitHub / Git

For SSH cloning, always specify the identity file explicitly:

```bash
GIT_SSH_COMMAND="ssh -i /workspace/extra/home/qgmoh/.ssh/id_ed25519 -o StrictHostKeyChecking=no" git clone git@github.com:qgmoh/repo.git /workspace/extra/projects/repo
```

Or set it once in the session:
```bash
export GIT_SSH_COMMAND="ssh -i /workspace/extra/home/qgmoh/.ssh/id_ed25519 -o StrictHostKeyChecking=no"
```

## Memory Protocol

### Session Start

1. Load `/workspace/group/memory/INDEX.md` (always — ~20 tokens)
2. Load 1-2 relevant memory files based on the current task (~100-200 tokens each)
3. If resuming a multi-step task, load the STATE file too (~100 tokens)

### During Work

- Use STATE for any task with 2+ steps (mandatory — see STATE section below)
- Do NOT load `conversations/` automatically — archive only; search manually if needed

### Task Complete

When STATE `i` is set to `"done"`:
1. Extract 1-3 new facts from the task
2. Write into the relevant file: `preferences.md`, `projects.md`, `context.md`, or `contacts.md`
3. If a new memory file was created, add it to `INDEX.md`
4. Keep each file under 50 lines

### Memory File Paths (container)

- `/workspace/group/memory/INDEX.md` — load every session
- `/workspace/group/memory/preferences.md` — Nick's style, formatting rules
- `/workspace/group/memory/projects.md` — active projects
- `/workspace/group/memory/context.md` — server paths, env facts
- `/workspace/group/memory/contacts.md` — key people

---

## STATE System (MANDATORY)

**Every multi-step task MUST use STATE.** This is not optional.
Skip only for: single file reads, greps, one-line answers — nothing else.

State directory: `/workspace/group/state/`
Full guide: read the `state` skill (`/state`)

```bash
python3 -c "
import json, pathlib, datetime
now = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
state = {'v':2,'t':'my-task','proj':'salad','g':'Goal here','s':'','i':'First step','created':now,'updated':now,'p':{},'k':{'tot':0,'in':0,'out':0,'started_at':now}}
p = pathlib.Path('/workspace/group/state'); p.mkdir(exist_ok=True)
(p / 'my-task.json').write_text(json.dumps(state, indent=2))
"
```

After each step: load state, update `s` (done) and `i` (next), save. When finished set `i` to `"done"`.

---

## Gated Push Policy (MANDATORY)

Never push to any repo without validation first.
```
commit locally → validate → security check → git push
```
Full commands: load `memory/pipeline.md` before any push.
