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

- State files: `/workspace/extra/projects/salad/state/`
- Tools: `/workspace/extra/projects/salad/state/tools/state_manager.py`
- Templates: `/workspace/extra/projects/salad/state/templates/`
- Full guide: read the `state` skill (`/state`)

```bash
python3 -c "
import sys; sys.path.insert(0, '/workspace/extra/projects/salad/state/tools')
from state_manager import initial_state, save_state
state = initial_state('my-task', 'Goal here')
state['i'] = 'First step'
save_state(state)
"
```

After each step: load state, update `s` (done) and `i` (next), save. When finished set `i` to `"done"`.
