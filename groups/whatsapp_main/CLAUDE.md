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
import json, pathlib
state = {'v':1,'t':'my-task','g':'Goal here','s':'','i':'First step','p':{}}
p = pathlib.Path('/workspace/group/state'); p.mkdir(exist_ok=True)
(p / 'my-task.json').write_text(json.dumps(state, indent=2))
"
```

After each step: load state, update `s` (done) and `i` (next), save. When finished set `i` to `"done"`.

---

## Gated Push Policy (MANDATORY)

Amy must NEVER `git push` to any repo without passing validation first.

### Pipeline
```
1. Implement + commit locally
2. Run validation (commands below)   ← GATE: must pass
3. Security check (diff review)      ← GATE: must pass
4. git push — only after both gates green
```

If validation fails — fix, re-run, never push on a fail.

### Validation Commands (by project)

**herv3:**
```bash
cd /workspace/extra/home/qgmoh/projects/herv3
docker compose -f docker-compose.dev.improved.yml exec web pytest --tb=short -q
docker compose -f docker-compose.dev.improved.yml exec frontend npx tsc --noEmit
docker compose -f docker-compose.dev.improved.yml exec frontend npx eslint src --ext .ts,.tsx
```

**salad:**
```bash
cd /workspace/extra/home/qgmoh/projects/salad
python -m pytest src/tests/ -q --tb=short
```

**nanoclaw:**
```bash
cd /workspace/extra/home/qgmoh/nanoclaw
npm test && npx tsc --noEmit
```

**Security check (all projects):** review the diff for hardcoded secrets, PHI exposure, auth regressions, debug flags left on.
