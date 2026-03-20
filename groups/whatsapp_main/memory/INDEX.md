# Memory Index — Amy (whatsapp_main)

Load this file at every session start. Load other files only when relevant.

## Files

| File | Contents | Load When |
|------|----------|-----------|
| `preferences.md` | Nick's name, WhatsApp formatting rules, communication style | Every message session |
| `projects.md` | Active projects: salad, herv3, nanoclaw | Task involves a known project |
| `context.md` | Server paths, SSH keys, container mounts, env facts | File/server/clone operations |
| `contacts.md` | Key people Amy should know | Task involves people or teams |

## Rules

- NEVER auto-load `conversations/` — archive only, search manually if needed
- After task completes (STATE i="done"): extract 1-3 facts into relevant file
- Update this INDEX if a new memory file is created
- Memory files must stay under 50 lines each
