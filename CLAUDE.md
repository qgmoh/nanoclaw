# NanoClaw

Personal Claude assistant. See [README.md](README.md) for philosophy and [docs/REQUIREMENTS.md](docs/REQUIREMENTS.md) for architecture.

## Quick Context

Single Node.js process, skill-based channel system. Channels (WhatsApp, Telegram, Slack, Discord, Gmail) self-register at startup. Messages route to Claude Agent SDK in isolated containers. Each group has its own filesystem, memory, and STATE.

## Key Files

| File | Purpose |
|------|---------|
| `src/index.ts` | Orchestrator: message loop, agent invocation, memory loader |
| `src/channels/registry.ts` | Channel self-registration |
| `src/ipc.ts` | IPC watcher and task processing |
| `src/container-runner.ts` | Spawns agent containers with mounts |
| `src/task-scheduler.ts` | Scheduled tasks |
| `src/db.ts` | SQLite operations |
| `src/memory-loader.ts` | Injects INDEX.md + active STATE into every container prompt |
| `groups/{name}/CLAUDE.md` | Per-group agent config (isolated) |

## Skills

| Skill | When to Use |
|-------|-------------|
| `/setup` | First-time install, auth, service config |
| `/customize` | Add channels, integrations, change behavior |
| `/debug` | Container issues, logs, troubleshooting |
| `/update-nanoclaw` | Bring upstream updates into customized install |

## Memory + STATE

- Each group: `groups/{name}/memory/` + `groups/{name}/state/`
- Host auto-injects `INDEX.md` + active STATE into every container prompt via `src/memory-loader.ts`
- Full spec: `docs/MEMORY_STATE_SYSTEM.md`
- STATE v2 format: `{'v':2,'t':'id','proj':'nanoclaw','g':'goal','s':'done','i':'next','created':ISO,'updated':ISO,'p':{},'k':{'tot':0,'in':0,'out':0}}`

## Gated Push Policy

No push without validation:
```
commit locally → npm test + tsc --noEmit → security check → git push
```

## Development Commands

```bash
npm run dev          # Hot reload
npm run build        # Compile TypeScript
./container/build.sh # Rebuild agent container
```

Service management (Linux):
```bash
systemctl --user start|stop|restart nanoclaw
```

## Key Troubleshooting Notes

- **WhatsApp not connecting after upgrade:** Run `/add-whatsapp` to install the separate channel fork. Existing auth and groups are preserved.
- **Stale container build:** `--no-cache` alone doesn't invalidate COPY steps. Prune the builder volume first, then re-run `./container/build.sh`.
