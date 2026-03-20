# NanoClaw

Personal Claude assistant. See [README.md](README.md) for philosophy and setup. See [docs/REQUIREMENTS.md](docs/REQUIREMENTS.md) for architecture decisions.

## Quick Context

Single Node.js process with skill-based channel system. Channels (WhatsApp, Telegram, Slack, Discord, Gmail) are skills that self-register at startup. Messages route to Claude Agent SDK running in containers (Linux VMs). Each group has isolated filesystem and memory.

## Key Files

| File | Purpose |
|------|---------|
| `src/index.ts` | Orchestrator: state, message loop, agent invocation |
| `src/channels/registry.ts` | Channel registry (self-registration at startup) |
| `src/ipc.ts` | IPC watcher and task processing |
| `src/router.ts` | Message formatting and outbound routing |
| `src/config.ts` | Trigger pattern, paths, intervals |
| `src/container-runner.ts` | Spawns agent containers with mounts |
| `src/task-scheduler.ts` | Runs scheduled tasks |
| `src/db.ts` | SQLite operations |
| `groups/{name}/CLAUDE.md` | Per-group memory (isolated) |
| `container/skills/agent-browser.md` | Browser automation tool (available to all agents via Bash) |

## Skills

| Skill | When to Use |
|-------|-------------|
| `/setup` | First-time installation, authentication, service configuration |
| `/customize` | Adding channels, integrations, changing behavior |
| `/debug` | Container issues, logs, troubleshooting |
| `/update-nanoclaw` | Bring upstream NanoClaw updates into a customized install |
| `/qodo-pr-resolver` | Fetch and fix Qodo PR review issues interactively or in batch |
| `/get-qodo-rules` | Load org- and repo-level coding rules from Qodo before code tasks |

## Memory Protocol (for all agents)

Each agent group has a `memory/` folder inside its group directory. Agents follow this protocol:

### Session Start

1. Load `memory/INDEX.md` at the start of every session (~20 tokens)
2. Read the INDEX to see what files exist and when to load each
3. Load 1-2 relevant files based on the task (~100-200 tokens each)
4. If resuming a task, also load the relevant STATE file (~100 tokens)

### During Work

- Use STATE for progress tracking on any task with 2+ steps
- NEVER auto-load conversation logs — they are archives for manual search only

### Task Complete

When STATE `i` is set to `"done"`:
1. Extract 1-3 new facts learned during the task
2. Write them into the most relevant memory file
3. If a new memory file was created, add it to `INDEX.md`
4. Keep every memory file under 50 lines

### Memory File Standard Structure

```
groups/{name}/memory/
├── INDEX.md        # Always loaded — lists files + when to load each (~20 lines)
├── preferences.md  # User communication style, formatting, working preferences
├── projects.md     # Active projects with brief context
├── contacts.md     # Key people the agent should know
└── context.md      # Environment facts: paths, servers, tools
```

### Token Budget per Session

| Item | Tokens |
|------|--------|
| INDEX.md | ~20 |
| 1-2 memory files | ~200-400 |
| STATE (if resuming) | ~100 |
| **Total overhead** | **~320-520** |

### Adding a New Agent

1. Create `groups/{name}/memory/` folder
2. Create `INDEX.md` listing the initial files
3. Create `preferences.md`, `projects.md`, `context.md` with known facts
4. Add Memory Protocol section to the agent's `CLAUDE.md`
5. Point memory paths to `/workspace/group/memory/` in the container

---

## STATE System (for multi-step tasks)

Use STATE for any task with 2+ steps. Saves ~82% tokens and enables resumption.

State directory: `/home/qgmoh/projects/salad/state/`
Tools: `/home/qgmoh/projects/salad/state/tools/state_manager.py`

```bash
python3 -c "
import sys; sys.path.insert(0, '/home/qgmoh/projects/salad/state/tools')
from state_manager import initial_state, save_state
state = initial_state('task-id', 'Goal description')
state['i'] = 'First step'
save_state(state)
"
```

After each step: load state, update `s` (done) and `i` (next), save. Set `i` to `"done"` when complete.

## Development

Run commands directly—don't tell the user to run them.

```bash
npm run dev          # Run with hot reload
npm run build        # Compile TypeScript
./container/build.sh # Rebuild agent container
```

Service management:
```bash
# macOS (launchd)
launchctl load ~/Library/LaunchAgents/com.nanoclaw.plist
launchctl unload ~/Library/LaunchAgents/com.nanoclaw.plist
launchctl kickstart -k gui/$(id -u)/com.nanoclaw  # restart

# Linux (systemd)
systemctl --user start nanoclaw
systemctl --user stop nanoclaw
systemctl --user restart nanoclaw
```

## Troubleshooting

**WhatsApp not connecting after upgrade:** WhatsApp is now a separate channel fork, not bundled in core. Run `/add-whatsapp` (or `git remote add whatsapp https://github.com/qwibitai/nanoclaw-whatsapp.git && git fetch whatsapp main && (git merge whatsapp/main || { git checkout --theirs package-lock.json && git add package-lock.json && git merge --continue; }) && npm run build`) to install it. Existing auth credentials and groups are preserved.

## Container Build Cache

The container buildkit caches the build context aggressively. `--no-cache` alone does NOT invalidate COPY steps — the builder's volume retains stale files. To force a truly clean rebuild, prune the builder then re-run `./container/build.sh`.
