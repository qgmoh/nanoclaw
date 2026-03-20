# Projects — Amy (whatsapp_main)

## salad (Saladmaster Dealer Automation)

- Repo: `git@github.com:qgmoh/salad.git`
- Host path: `/workspace/extra/home/qgmoh/projects/salad/`
- Stack: FastAPI + Python 3.13+, Docker
- Function 1: WhatsApp webhook → booking form parser (38 fields) → Excel/Google Sheets
- Function 2: Excel data → PowerPoint slide automation (category/marker/cell modes)
- Dashboard: `http://localhost:8050/`

## herv3 (EHR System)

- Repo: `git@github.com:qgmoh/HER.git` (herv3 is a subdirectory)
- Host path: `/workspace/extra/home/qgmoh/projects/herv3/`
- Stack: Django + FHIR, Celery for async tasks
- Function: Electronic Health Records system with FHIR resource mapping
- Clone method: Clone full HER repo, extract herv3 subfolder

## nanoclaw (Personal Assistant Platform)

- Repo path on host: `/home/qgmoh/nanoclaw/`
- Stack: Node.js, TypeScript, Claude Agent SDK, Docker containers
- Function: Multi-channel personal AI assistant (WhatsApp, Telegram, Slack, etc.)
- Groups run in isolated containers with per-group CLAUDE.md and memory
- Amy = whatsapp_main group agent; Andy = main group agent (elevated privileges)
