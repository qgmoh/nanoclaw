---
name: group-management
description: How to find, add, remove, and configure WhatsApp/Telegram/Slack groups in nanoclaw
type: reference
---

# Group Management — Andy

## Finding Groups
- Available groups: `/workspace/ipc/available_groups.json` (synced daily, ordered by activity)
- Force sync: `echo '{"type":"refresh_groups"}' > /workspace/ipc/tasks/refresh_$(date +%s).json`
- Fallback SQLite: `sqlite3 /workspace/project/store/messages.db "SELECT jid,name FROM chats WHERE jid LIKE '%@g.us' ORDER BY last_message_time DESC LIMIT 10;"`

## Registered Groups
Stored in SQLite `registered_groups` table. Key fields: `jid`, `name`, `folder`, `trigger`, `requiresTrigger`, `isMain`, `added_at`.

Folder naming: channel prefix + underscore + hyphenated name (e.g. `whatsapp_family-chat`, `telegram_dev-team`)

## Adding a Group
1. Find JID from available_groups or SQLite
2. Use `register_group` MCP tool (JID, name, folder, trigger)
3. Optionally add `containerConfig.additionalMounts` for extra dirs
4. Group folder auto-created at `/workspace/project/groups/{folder}/`
5. Offer sender allowlist setup after registering

## Trigger Behavior
- `isMain: true` → no trigger needed (Andy's channel)
- `requiresTrigger: false` → no trigger (solo/personal chats)
- Default → messages must start with `@AssistantName`

## Sender Allowlist
Config on host: `~/.config/nanoclaw/sender-allowlist.json`
Modes: `trigger` (store all, only allowed can trigger) | `drop` (non-allowed not stored)
Own messages (`is_from_me`) always bypass allowlist.

## Removing a Group
Remove entry from `registered_groups` table. Group folder is kept (not deleted).

## Scheduling for Other Groups
`schedule_task(prompt:"...", schedule_type:"cron", schedule_value:"0 9 * * 1", target_group_jid:"<jid>")`

## Global Memory
`/workspace/project/groups/global/CLAUDE.md` — facts for all groups. Update only when explicitly asked.
