# Projects — Andy (main)

## salad (Saladmaster Dealer Automation)

- Repo: `git@github.com:qgmoh/salad.git`
- Host path: `/workspace/project/groups/` → accessible via project mount
- Stack: FastAPI + Python 3.13+, Docker
- Function 1: WhatsApp webhook → booking form parser (38 fields) → Excel/Google Sheets
- Function 2: Excel data → PowerPoint slide automation (category/marker/cell modes)
- STATE tools: `state/tools/state_manager.py` within repo

## herv3 (EHR System)

- Repo: `git@github.com:qgmoh/HER.git` (herv3 is a subdirectory)
- Stack: Django + FHIR, Celery for async tasks
- Function: Electronic Health Records system with FHIR resource mapping

## Memory+STATE System (nanoclaw-wide)

- STATE v2 schema: adds `proj`, `created`, `updated`, `k` (token counter) fields — v1 deprecated
- Archiving: done files auto-moved to `state/archive/` after 15 days, deleted after 30 days (configurable in `~/.claude/settings.local.json`)
- Templates: 5 nanoclaw templates in `groups/main/state/templates/` (generic-task, group-management, code-change, investigation, scheduled-task)
- Host skill: `~/.claude/skills/state-resume-task/SKILL.md` (compact, ≤150 tokens)
- Agent Tom: `~/.claude/agents/tom.md` — audits and reports on the memory+state system
- Container helper: `container/skills/state/state_manager.py` (init, load, save, done, list commands)

## nanoclaw (Personal Assistant Platform)

- Project root: `/workspace/project/` (read-only in Andy's container)
- Stack: Node.js, TypeScript, Claude Agent SDK, Docker containers
- Function: Multi-channel personal AI assistant
- SQLite DB: `/workspace/project/store/messages.db`
- Registered groups config: `registered_groups` table in SQLite
- Available groups list: `/workspace/ipc/available_groups.json`
- Andy = main group agent with isMain:true (no trigger required, elevated privileges)
- Amy = whatsapp_main group agent
- Memory+STATE system wired in src/memory-loader.ts — host injects INDEX.md + active STATE into every prompt
- All agents use /workspace/group/state/ for STATE (standardized Mar 20 2026)
