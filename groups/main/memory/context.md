# Context — Andy (main)

## Container Mounts (Andy's View)

| Container Path | Host Path | Access |
|----------------|-----------|--------|
| `/workspace/project` | NanoClaw project root | read-only |
| `/workspace/group` | `groups/main/` | read-write |
| `/workspace/group/memory/` | `groups/main/memory/` | read-write |
| `/workspace/ipc/` | IPC directory | read-write |

## Key Paths

- SQLite database: `/workspace/project/store/messages.db`
- All group folders: `/workspace/project/groups/`
- Global memory: `/workspace/project/groups/global/CLAUDE.md`
- Registered groups: `registered_groups` table in SQLite DB
- Available groups sync: `/workspace/ipc/available_groups.json`
- State files: `/workspace/group/state/` (local to Andy's container)

## Group Management

- Find group JID: query `chats` table in SQLite, filter `jid LIKE '%@g.us'`
- Register group: use `register_group` MCP tool with JID, name, folder, trigger
- Folder naming: `{channel}_{group-name}` e.g. `whatsapp_family-chat`
- Remove group: edit `registered_groups` in SQLite — do NOT delete group folder
- Refresh available groups: `echo '{"type": "refresh_groups"}' > /workspace/ipc/tasks/refresh_$(date +%s).json`
- Sender allowlist config: `~/.config/nanoclaw/sender-allowlist.json` on host

## Trigger Behavior

- Main group (`isMain: true`): no trigger needed, all messages processed
- `requiresTrigger: false`: no trigger needed (1-on-1 or solo chats)
- Other groups: messages must start with `@AssistantName`

## Scheduling for Other Groups

- Use `target_group_jid` param in `schedule_task` to run task in another group's context
- Group JIDs found in `registered_groups` table

## STATE System (v2)

- State dir: `/workspace/group/state/` — see `/workspace/project/container/skills/state/state.md` for full v2 format and commands
- Templates: `/workspace/group/state/templates/` — generic-task, group-management, code-change, investigation, scheduled-task
