# Context — Amy (whatsapp_main)

## Container Paths (Amy's View)

| What | Container Path | Notes |
|------|---------------|-------|
| Group workspace (read-write) | `/workspace/group/` | Amy's persistent files |
| Host home directory | `/workspace/extra/home/qgmoh/` | Mounted from host |
| Projects (persistent) | `/workspace/extra/home/qgmoh/projects/` | **Always use this path** |
| Memory files | `/workspace/group/memory/` | Maps to `groups/whatsapp_main/memory/` on host |
| SSH key | `/workspace/extra/home/qgmoh/.ssh/id_ed25519` | For GitHub SSH cloning |

## Critical Path Rules

- Files written to `/workspace/projects/` or `/workspace/extra/projects/` may be lost
- ALWAYS use `/workspace/extra/home/qgmoh/projects/` for repos that must persist on server
- `/workspace/extra/` is read-only — cannot write directly; it is the host mount point

## SSH / Git Cloning

```bash
GIT_SSH_COMMAND="ssh -i /workspace/extra/home/qgmoh/.ssh/id_ed25519 -o StrictHostKeyChecking=no" \
  git clone git@github.com:qgmoh/REPO.git /workspace/extra/home/qgmoh/projects/REPO
```

## STATE System

- State directory: `/workspace/group/state/`
- Use STATE for every multi-step task (skip only for single reads/greps)
- Host injects active STATE into `<context>` block at session start automatically

## NanoClaw Architecture

- Single Node.js process routes messages to Claude agent containers
- Each group = isolated Docker container with its own CLAUDE.md and workspace
- Messages route via channel skills (WhatsApp, Telegram, Slack, Discord, Gmail)
- Amy's group: `whatsapp_main` — personal WhatsApp group
