# Memory + STATE System — NanoClaw Agent Architecture

## Overview

NanoClaw agents operate across sessions without persistent conversation context. Two complementary systems handle continuity:

| System | Purpose | Scope | Lifespan |
|--------|---------|-------|----------|
| **STATE** | Track progress through a multi-step task | One task | Until `i = "done"` |
| **Memory** | Store permanent facts about user, projects, environment | All sessions forever | Indefinitely |

**Why both?**

STATE is a scratchpad: it holds the "where am I in this task" pointer and can be loaded in ~100 tokens to resume work mid-task. It is transient — once a task is done, the STATE file is no longer needed.

Memory is the long-term knowledge base: names, preferences, project paths, key decisions. These facts are small (memory files stay under 50 lines), load fast (~100-200 tokens each), and accumulate over time.

Neither replaces conversation logs. Logs are archives — searchable if needed, but never auto-loaded because they are too large (~5,000-50,000 tokens).

---

## Token Budget Analysis

### Per-Session Overhead

| Item | Approx Tokens | Notes |
|------|--------------|-------|
| `INDEX.md` | ~20 | ~80 chars × 4 chars/token, loaded every session |
| `preferences.md` | ~120 | ~480 chars of facts |
| `projects.md` | ~200 | ~800 chars of project context |
| `context.md` | ~200 | ~800 chars of paths/env facts |
| STATE file (if resuming) | ~100 | JSON blob, ~400 chars |
| **Minimum (INDEX only)** | **~20** | Simple single-step tasks |
| **Typical (INDEX + 2 files)** | **~340** | Most task sessions |
| **Maximum (INDEX + all + STATE)** | **~640** | Complex resume sessions |

### Comparison: Old vs New

| Approach | Tokens | Notes |
|----------|--------|-------|
| Full conversation log | 5,000-50,000 | Loaded everything |
| Memory + STATE system | 320-640 | Targeted loading |
| **Savings** | **~97-99%** | Per session |

---

## Memory File Format

### INDEX.md

The index is the only file always loaded. It must stay under 20 lines.

```markdown
# Memory Index — {Agent} ({group})

Load this file at every session start. Load other files only when relevant.

## Files

| File | Contents | Load When |
|------|----------|-----------|
| `preferences.md` | User style, formatting rules | Every message session |
| `projects.md` | Active projects | Task involves a known project |
| `context.md` | Server paths, env facts | File/server operations |
| `contacts.md` | Key people | Task involves people |

## Rules

- NEVER auto-load `conversations/` — archive only
- After task completes (STATE i="done"): extract 1-3 facts into relevant file
- Update this INDEX if a new memory file is created
- Memory files must stay under 50 lines each
```

### Fact Files (preferences.md, projects.md, context.md, contacts.md)

Each fact file is plain markdown under 50 lines. Use `##` headings to section it. Facts only — no narrative, no logs.

**Good entry format:**
```markdown
## User
- Name: Nick
- Prefers direct, concise answers
- Uses WhatsApp — never use markdown headings or double asterisks

## Project: salad
- Repo: git@github.com:qgmoh/salad.git
- Path: /workspace/extra/home/qgmoh/projects/salad/
- Stack: FastAPI + Python 3.13+, Docker
```

---

## STATE File Format

STATE is a compact JSON file. Each field has a 300-character limit.

```json
{
  "v": 1,
  "t": "task-id",
  "g": "Goal: what you are achieving",
  "s": "Summary: what has been completed so far",
  "i": "Next action to take (or 'done' when complete)",
  "p": {
    "optional": "extra key-value context"
  }
}
```

| Field | Meaning | Limit |
|-------|---------|-------|
| `v` | Schema version | always 1 |
| `t` | Task identifier (= filename) | kebab-case |
| `g` | Goal description | 300 chars |
| `s` | Summary of work done | 300 chars |
| `i` | Next action / `"done"` | 300 chars |
| `p` | Extra params dict | flexible |

### All agents — STATE location

State lives at `/workspace/group/state/` for every agent. This maps to `groups/{name}/state/` on the host and is injected automatically into each session by the orchestrator.

```bash
python3 -c "
import json, pathlib
state = {'v':1,'t':'task-id','g':'Goal here','s':'','i':'First step','p':{}}
p = pathlib.Path('/workspace/group/state'); p.mkdir(exist_ok=True)
(p / 'task-id.json').write_text(json.dumps(state, indent=2))
"
```

---

## Session Protocol

### Step 1 — Session Start

```
1. Load /workspace/group/memory/INDEX.md
2. Read INDEX to identify relevant files for this task
3. Load 1-2 relevant memory files
4. Check if a STATE file exists for an in-progress task
5. If STATE exists and i != "done": load it and resume from i
6. If no STATE or i == "done": begin fresh task
```

### Step 2 — During Work

```
For every significant step:
1. Do the work
2. Load STATE → update s (what was done) → update i (next step) → save STATE
3. Continue to next step

For quick single-step tasks:
- No STATE needed; answer directly
```

### Step 3 — Task Complete

```
When i = "done":
1. Extract 1-3 new facts learned during the task
2. Write facts into the relevant memory file (preferences/projects/context/contacts)
3. If a new memory file was created: add entry to INDEX.md
4. If a memory file exceeds 50 lines: summarise or remove stale facts
5. STATE file can remain (it signals completion); no need to delete it
```

---

## STATE → Memory Handoff Protocol

The moment a task ends (`i = "done"`), the agent performs a memory harvest:

1. **Identify new facts**: What did this task reveal that wasn't already in memory?
2. **Classify**: Does the fact belong in preferences, projects, context, or contacts?
3. **Write**: Append 1-3 lines to the appropriate file. No full sentences — use bullet facts.
4. **Check size**: If file exceeds 50 lines, merge or trim stale entries.

**Example handoff:**

After cloning a repo and setting it up:

```markdown
# Addition to projects.md
## herv3
- Clone: git@github.com:qgmoh/HER.git → extract herv3/ subdirectory
- Host path: /workspace/extra/home/qgmoh/projects/herv3/
- Stack: Django + FHIR + Celery
```

This fact is now permanent across all future sessions — no need to ask Nick again.

---

## How to Add a New Agent

**Checklist:**

- [ ] Create group folder: `groups/{name}/`
- [ ] Create memory folder: `groups/{name}/memory/`
- [ ] Create `INDEX.md` listing initial files and load-when guidance
- [ ] Create `preferences.md` with user style facts
- [ ] Create `projects.md` with known active projects
- [ ] Create `context.md` with container paths, env facts
- [ ] Create `contacts.md` with key people (can start minimal)
- [ ] Create state folder: `groups/{name}/state/` with a `.gitkeep`
- [ ] Create or update agent's `CLAUDE.md` with Memory Protocol and STATE sections
- [ ] Update `.gitignore` to track `CLAUDE.md`, `memory/*.md`, and `state/.gitkeep`
- [ ] Point memory paths to `/workspace/group/memory/` in the container
- [ ] Verify token estimates: count lines × ~20 chars × 0.25 tokens/char

**Container path convention:** All agents use `/workspace/group/memory/` inside the container. The host mapping varies by group folder.

---

## How to Extend the System

### Add a new memory file

1. Create the file under `groups/{name}/memory/your-file.md`
2. Add an entry to `INDEX.md` with: filename, contents, load-when condition
3. Keep it under 50 lines
4. Follow the fact-only format (no narrative, no logs)

### Increase memory granularity

If a file grows beyond 50 lines, split it:

- `projects.md` → `projects-salad.md` + `projects-herv3.md`
- Add both to `INDEX.md` with specific load-when conditions

### Share facts across agents

Global facts belong in `/workspace/project/groups/global/CLAUDE.md` (Andy can write there; Amy can read via mounted project path if given access).

Agent-specific facts stay in their own `memory/` folder.

### Add memory to a new channel

Same process as adding a new agent. The memory system is channel-agnostic — it works for WhatsApp, Telegram, Slack, Discord, or any future channel.

---

## Examples: Good vs Bad Memory Entries

### Good — Specific, factual, compact

```markdown
- Name: Nick
- Prefers bullet-point summaries over paragraphs
- Never use ## headings in WhatsApp messages
- salad repo: git@github.com:qgmoh/salad.git → /workspace/extra/home/qgmoh/projects/salad/
- SSH key for GitHub: /workspace/extra/home/qgmoh/.ssh/id_ed25519
```

### Bad — Vague, narrative, or log-like

```markdown
- The user seems to prefer shorter messages (I noticed this in our conversation)
- On March 19 Nick asked me to clone HER but I couldn't because the filesystem was read-only
  then he asked again and I managed to do it eventually. Remember this for next time.
- Nick wants things done. He is a busy person.
```

**Why bad:** The first is vague opinion, the second is a conversation log extract (never copy logs into memory), the third is filler with no actionable fact.

---

## Anti-Patterns to Avoid

| Anti-Pattern | Why Bad | What to Do Instead |
|---|---|---|
| Auto-loading `conversations/` | 5,000-50,000 tokens per file | Load only on explicit request |
| Copying conversation excerpts into memory | Defeats the purpose; still large | Extract only the concrete fact |
| Duplicating STATE content in memory | STATE is transient progress; memory is permanent facts | Keep them separate |
| One giant `memory.md` file | Loads entirely even when irrelevant | Split into focused files |
| Memory files over 50 lines | Excess tokens for irrelevant facts | Trim stale facts; split if needed |
| Writing narrative in memory | Hard to scan; wastes tokens | Bullet-point facts only |
| Loading all memory files every session | Unnecessary overhead | Use INDEX to decide what to load |
| Updating global CLAUDE.md without being asked | Pollutes shared state | Only update global memory on explicit instruction |

---

## System Architecture Summary

```
Session Start
  └── Load INDEX.md (~20 tokens)
      └── Load relevant memory files (~200-400 tokens)
          └── Load STATE if resuming (~100 tokens)
              └── Do work
                  └── Update STATE after each step
                      └── When i="done":
                          └── Harvest 1-3 facts → write to memory file
                              └── Session end
```

**Total overhead per session: 320-520 tokens**
**vs. loading conversation history: 5,000-50,000 tokens**
**Savings: ~97-99% per session**
