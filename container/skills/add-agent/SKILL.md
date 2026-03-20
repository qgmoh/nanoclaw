---
name: add-agent
description: Create a new NanoClaw agent with memory system, STATE, and CLAUDE.md. Interactively collects required info, creates all files, updates .gitignore, commits to qgclaw, and registers the group. Use when the user asks to create a new agent, add a new assistant, or set up a new channel bot.
---

# /add-agent — Create a New NanoClaw Agent

You are creating a new NanoClaw agent end-to-end. This is a multi-step task — use STATE to track progress.

## Step 0 — Initialise STATE

```bash
python3 -c "
import json, pathlib
state = {
    'v': 1, 't': 'add-agent',
    'g': 'Create new NanoClaw agent with memory, STATE, and CLAUDE.md',
    's': '', 'i': 'collect-info',
    'p': {}
}
p = pathlib.Path('/workspace/group/state'); p.mkdir(exist_ok=True)
(p / 'add-agent.json').write_text(json.dumps(state))
print('STATE ready')
"
```

---

## Step 1 — Collect Required Information

Check if the user already provided any of these in their message. For each missing piece, ask **one message** with all missing fields listed together. Do not ask field by field.

### Required fields

| Field | Example | Notes |
|---|---|---|
| `name` | `bella` | Lowercase, the agent's first name |
| `channel` | `telegram` | whatsapp / telegram / slack / discord / gmail |
| `purpose` | `Manages project updates and daily standups` | 1-2 sentences |
| `trigger` | `@Bella` | How users invoke the agent (default: `@{Name}`) |

### Optional fields (ask only if relevant)

| Field | Example | Notes |
|---|---|---|
| `group_folder` | `telegram_bella` | Default: `{channel}_{name}` |
| `extra_mounts` | `/home/qgmoh/projects/webapp` | Any host paths to mount into container |
| `requiresTrigger` | `true` | Set `false` for 1-on-1 / solo chats |

### Ask template (if info is missing)

Send this message, omitting lines for fields already provided:

```
To set up the new agent I need a few details:

• *Name* — what should the agent be called? (e.g. Bella)
• *Channel* — which platform? (whatsapp / telegram / slack / discord)
• *Purpose* — what will this agent do? (1-2 sentences)
• *Trigger word* — how do users invoke it? (default: @Name)

Anything else I should know upfront? (extra file mounts, 1-on-1 chat, etc.)
```

Once you have all required fields, derive:
- `name_lower` = lowercase name (e.g. `bella`)
- `name_title` = title case (e.g. `Bella`)
- `group_folder` = `{channel}_{name_lower}` unless overridden
- `trigger` = `@{name_title}` unless overridden

Update STATE:
```bash
python3 -c "
import json, pathlib
p = pathlib.Path('/workspace/group/state/add-agent.json')
state = json.loads(p.read_text())
state['s'] = 'Info collected'
state['i'] = 'create-files'
state['p'] = {
    'name': 'bella',
    'name_title': 'Bella',
    'channel': 'telegram',
    'group_folder': 'telegram_bella',
    'trigger': '@Bella',
    'purpose': 'Manages project updates and daily standups',
    'requiresTrigger': True,
    'extra_mounts': []
}
p.write_text(json.dumps(state))
"
```

---

## Step 2 — Determine Host Paths

### If running from main channel (`/workspace/project` exists)

```bash
test -d /workspace/project && echo "MAIN" || echo "NOT_MAIN"
```

- **MAIN**: nanoclaw root = `/workspace/project/`, groups dir = `/workspace/project/groups/`
- **NOT_MAIN**: nanoclaw root = `/workspace/extra/home/qgmoh/nanoclaw/`, groups dir = `/workspace/extra/home/qgmoh/nanoclaw/groups/`

Set `GROUPS_DIR` and `NANOCLAW_DIR` accordingly for all subsequent steps.

---

## Step 3 — Create Files

Run this block (substituting actual values for the placeholders):

```bash
GROUPS_DIR="/workspace/project/groups"   # or /workspace/extra/home/qgmoh/nanoclaw/groups
NAME_LOWER="bella"
NAME_TITLE="Bella"
CHANNEL="telegram"
GROUP_FOLDER="telegram_bella"
TRIGGER="@Bella"
PURPOSE="Manages project updates and daily standups"

mkdir -p "$GROUPS_DIR/$GROUP_FOLDER/memory" "$GROUPS_DIR/$GROUP_FOLDER/state"
touch "$GROUPS_DIR/$GROUP_FOLDER/state/.gitkeep"
```

### 3a — INDEX.md

```bash
cat > "$GROUPS_DIR/$GROUP_FOLDER/memory/INDEX.md" << 'ENDOFFILE'
# Memory Index — {NAME_TITLE} ({GROUP_FOLDER})

Load this file at every session start. Load other files only when relevant.

## Files

| File | Contents | Load When |
|------|----------|-----------|
| `preferences.md` | Nick's style, formatting rules | Every session |
| `projects.md` | Active projects | Task involves a project |
| `context.md` | Container paths, env facts | File/server operations |
| `contacts.md` | Key people | Task involves people |

## Rules

- NEVER auto-load `conversations/` — archive only, search manually if needed
- After task completes (STATE i="done"): extract 1-3 facts into relevant file
- Update this INDEX if a new memory file is created
- Memory files must stay under 50 lines each
ENDOFFILE
```

Replace `{NAME_TITLE}` and `{GROUP_FOLDER}` with actual values.

### 3b — preferences.md

```bash
cat > "$GROUPS_DIR/$GROUP_FOLDER/memory/preferences.md" << 'ENDOFFILE'
# Preferences — {NAME_TITLE} ({GROUP_FOLDER})

## User

- Name: Nick
- Prefers direct, concise answers
- Will repeat a request if the agent gets it wrong; correct silently on retry

## Message Formatting

- Match formatting rules for {CHANNEL}
- Telegram: standard markdown supported (*bold*, _italic_, `code`)
- WhatsApp: NEVER use ## headings or **double asterisks**; use *single asterisks* for bold
- Keep messages short and readable on mobile

## Communication Style

- Acknowledge before starting long work (use `mcp__nanoclaw__send_message`)
- Wrap internal reasoning in `<internal>` tags — not sent to user
- Only use `send_message` if instructed when acting as a sub-agent
ENDOFFILE
```

### 3c — projects.md

```bash
cat > "$GROUPS_DIR/$GROUP_FOLDER/memory/projects.md" << 'ENDOFFILE'
# Projects — {NAME_TITLE} ({GROUP_FOLDER})

## salad (Saladmaster Dealer Automation)

- Repo: git@github.com:qgmoh/salad.git
- Stack: FastAPI + Python 3.13+, Docker
- Function: WhatsApp booking parser + Excel/PowerPoint automation

## herv3 (EHR System)

- Repo: git@github.com:qgmoh/HER.git
- Stack: Django + FHIR + Celery
- Function: Electronic Health Records system

## nanoclaw / qgclaw (Personal Assistant Platform)

- Host path: /home/qgmoh/nanoclaw/
- Private repo: git@github.com:qgmoh/qgclaw.git
- Stack: Node.js, TypeScript, Claude Agent SDK, Docker
- Function: Multi-channel personal AI assistant
ENDOFFILE
```

### 3d — context.md

Content depends on channel. Use this template, adjusting paths:

```bash
cat > "$GROUPS_DIR/$GROUP_FOLDER/memory/context.md" << 'ENDOFFILE'
# Context — {NAME_TITLE} ({GROUP_FOLDER})

## Container Paths

| What | Path | Notes |
|------|------|-------|
| Group workspace (read-write) | `/workspace/group/` | Persistent files |
| Memory files | `/workspace/group/memory/` | Maps to groups/{GROUP_FOLDER}/memory/ on host |
| STATE files | `/workspace/group/state/` | Local task progress |

## STATE System

- State dir: `/workspace/group/state/`
- Use STATE for every multi-step task (skip only for single reads/greps)
- Format: JSON with fields v, t, g, s, i, p

## NanoClaw Architecture

- Single Node.js process routes messages to Claude agent containers
- Each group = isolated Docker container with its own CLAUDE.md and memory
- Amy = whatsapp_main group agent
- Andy = main group agent (elevated privileges, manages groups)
ENDOFFILE
```

### 3e — contacts.md

```bash
cat > "$GROUPS_DIR/$GROUP_FOLDER/memory/contacts.md" << 'ENDOFFILE'
# Contacts — {NAME_TITLE} ({GROUP_FOLDER})

## Primary User

- **Nick** — owner of the nanoclaw setup; the user this agent serves

## System Agents

- **Andy** — main group agent; elevated privileges; manages group registrations
- **Amy** — whatsapp_main agent; handles Nick's personal WhatsApp group
- **{NAME_TITLE}** — this agent; {PURPOSE}

## Notes

- Add contacts here when Nick mentions specific people to remember
- Include role, relationship to Nick, and relevant context
- Keep entries to 1-3 lines per person
ENDOFFILE
```

### 3f — CLAUDE.md

Create the agent's main instruction file:

```bash
cat > "$GROUPS_DIR/$GROUP_FOLDER/CLAUDE.md" << 'ENDOFFILE'
# {NAME_TITLE}

You are {NAME_TITLE}, a personal assistant. {PURPOSE}

## What You Can Do

- Answer questions and have conversations
- Search the web and fetch content from URLs
- **Browse the web** with `agent-browser` — open pages, click, fill forms, take screenshots
- Read and write files in your workspace
- Run bash commands in your sandbox
- Schedule tasks to run later or on a recurring basis
- Send messages back to the chat

## Communication

Your output is sent to the user or group.

You also have `mcp__nanoclaw__send_message` to send a message immediately while still working. Use this to acknowledge long tasks before starting.

### Internal thoughts

Wrap internal reasoning in `<internal>` tags — logged but not sent to user:

```
<internal>Compiled results, ready to summarise.</internal>

Here are the key findings...
```

### Sub-agents and teammates

When acting as a sub-agent, only use `send_message` if instructed by the main agent.

## Memory Protocol

### Session Start

1. Load `/workspace/group/memory/INDEX.md` (always — ~20 tokens)
2. Load 1-2 relevant memory files based on the current task (~100-200 tokens each)
3. If resuming a multi-step task, load the STATE file too (~100 tokens)

### During Work

- Use STATE for any task with 2+ steps (mandatory)
- Do NOT load `conversations/` automatically — archive only; search manually if needed

### Task Complete

When STATE `i` is set to `"done"`:
1. Extract 1-3 new facts from the task
2. Write into the relevant file: `preferences.md`, `projects.md`, `context.md`, or `contacts.md`
3. If a new memory file was created, add it to `INDEX.md`
4. Keep each file under 50 lines

### Memory File Paths (container)

- `/workspace/group/memory/INDEX.md` — load every session
- `/workspace/group/memory/preferences.md` — user style, formatting rules
- `/workspace/group/memory/projects.md` — active projects
- `/workspace/group/memory/context.md` — container paths, env facts
- `/workspace/group/memory/contacts.md` — key people

## STATE System (MANDATORY)

**Every multi-step task MUST use STATE.** This is not optional.
Skip only for: single file reads, greps, one-line answers.

State directory: `/workspace/group/state/`

```bash
python3 -c "
import json, pathlib
state = {'v':1,'t':'task-id','g':'Goal here','s':'','i':'First step','p':{}}
p = pathlib.Path('/workspace/group/state'); p.mkdir(exist_ok=True)
(p / 'task-id.json').write_text(json.dumps(state))
"
```

After each step: load state, update `s` (done) and `i` (next), save. Set `i` to `"done"` when complete.

## Message Formatting

Follow formatting rules for {CHANNEL}. When in doubt: no markdown headings, short messages, mobile-readable.
ENDOFFILE
```

Update STATE after file creation:
```bash
python3 -c "
import json, pathlib
p = pathlib.Path('/workspace/group/state/add-agent.json')
state = json.loads(p.read_text())
state['s'] = 'All files created'
state['i'] = 'update-gitignore'
p.write_text(json.dumps(state))
"
```

---

## Step 4 — Update .gitignore

```bash
GITIGNORE="$NANOCLAW_DIR/.gitignore"
GROUP_FOLDER="telegram_bella"   # substitute actual value

# Add tracking rules for the new group
cat >> "$GITIGNORE" << ENDOFFILE

# {GROUP_FOLDER}
!groups/${GROUP_FOLDER}/
groups/${GROUP_FOLDER}/*
!groups/${GROUP_FOLDER}/CLAUDE.md
!groups/${GROUP_FOLDER}/memory/
groups/${GROUP_FOLDER}/memory/*
!groups/${GROUP_FOLDER}/memory/*.md
!groups/${GROUP_FOLDER}/state/
groups/${GROUP_FOLDER}/state/*
!groups/${GROUP_FOLDER}/state/.gitkeep
ENDOFFILE

echo "gitignore updated"
```

Update STATE:
```bash
python3 -c "
import json, pathlib
p = pathlib.Path('/workspace/group/state/add-agent.json')
state = json.loads(p.read_text())
state['s'] = 'Files created, gitignore updated'
state['i'] = 'commit'
p.write_text(json.dumps(state))
"
```

---

## Step 5 — Commit to qgclaw

```bash
cd "$NANOCLAW_DIR"

git add \
  .gitignore \
  "groups/$GROUP_FOLDER/CLAUDE.md" \
  "groups/$GROUP_FOLDER/memory/" \
  "groups/$GROUP_FOLDER/state/.gitkeep"

git commit -m "feat: add $GROUP_FOLDER agent ($NAME_TITLE) with memory system

- CLAUDE.md with Memory Protocol and STATE mandate
- memory/INDEX.md, preferences.md, projects.md, context.md, contacts.md
- state/.gitkeep to track state directory
- .gitignore updated to track new group

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"

GIT_SSH_COMMAND="ssh -i /home/qgmoh/.ssh/id_ed25519 -o StrictHostKeyChecking=no" \
  git push qgclaw main
```

Update STATE:
```bash
python3 -c "
import json, pathlib
p = pathlib.Path('/workspace/group/state/add-agent.json')
state = json.loads(p.read_text())
state['s'] = 'Files created, committed and pushed to qgclaw'
state['i'] = 'register-group'
p.write_text(json.dumps(state))
"
```

---

## Step 6 — Register the Group

### If running from main channel

Use the `register_group` MCP tool:

```
register_group(
  jid="<ask Nick for the JID or find it from available_groups.json>",
  name="{NAME_TITLE}",
  folder="{GROUP_FOLDER}",
  trigger="{TRIGGER}",
  requiresTrigger=true
)
```

To find the JID, check available groups:
```bash
cat /workspace/ipc/available_groups.json 2>/dev/null | python3 -c "
import json,sys
groups = json.load(sys.stdin).get('groups', [])
for g in groups[:20]:
    print(g.get('jid'), g.get('name'))
"
```

If the channel/group isn't listed yet, tell Nick:
> The group isn't in the available list yet. Once you've added me to the {CHANNEL} group/chat, send `/add-agent` again and I'll complete the registration.

### If NOT running from main channel

Send a message to Andy:
> Andy, please register a new group: name="{NAME_TITLE}", folder="{GROUP_FOLDER}", trigger="{TRIGGER}". The CLAUDE.md and memory files are already created and committed. Nick will provide the JID.

---

## Step 7 — Finalise and Harvest to Memory

Update STATE to done:
```bash
python3 -c "
import json, pathlib
p = pathlib.Path('/workspace/group/state/add-agent.json')
state = json.loads(p.read_text())
state['s'] = 'Agent {NAME_TITLE} fully created, committed, registered'
state['i'] = 'done'
p.write_text(json.dumps(state))
"
```

Add the new agent to your own `contacts.md`:
```bash
echo "- **{NAME_TITLE}** — {GROUP_FOLDER} agent; {PURPOSE}" >> /workspace/group/memory/contacts.md
```

Send Nick a confirmation:
```
✓ *{NAME_TITLE}* is ready.

• Group folder: `{GROUP_FOLDER}`
• Trigger: `{TRIGGER}`
• Memory files: INDEX, preferences, projects, context, contacts
• Committed to qgclaw

{IF_REGISTERED: She's registered and will respond to {TRIGGER} in the {CHANNEL} group.}
{IF_PENDING: Once you share the group JID (or add the bot to the chat), Andy can complete registration.}
```

---

## Error Handling

| Error | Action |
|---|---|
| Missing info after asking once | Wait for Nick's reply; don't proceed |
| Git push fails | Check SSH key path; retry with correct key |
| `register_group` fails | Note JID issue in STATE `p`; tell Nick to provide JID manually |
| Group folder already exists | Tell Nick: "A group folder for `{GROUP_FOLDER}` already exists. Do you want to overwrite or use a different name?" |
| File write fails (read-only path) | Switch to the correct host path (see Step 2) |
