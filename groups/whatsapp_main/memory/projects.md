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
- Stack: Django + React/TypeScript, Celery, Redis, Postgres, AWS DocumentDB
- Active phase: Phase 10 — Telemedicine (Weeks 1-2 backend done, Weeks 3-4 frontend pending)
- UX Foundation Sprint complete (Mar 2026): PatientContextBanner on all pages, co-sign, handoff notes, voice dictation, drug interaction alerts
- Gate system: Marcus (tsc+eslint), James (appsec), clinical-testers write JSON to `.claude/state/` — Amy reads and fixes
- ESLint: migrated to v9 flat config (`eslint.config.js`) — `.eslintrc.cjs` renamed `.bak`
- JWT: production ACCESS_TOKEN_LIFETIME = 15 minutes (was 1hr — fixed Mar 2026)
- HandoffNote.note uses EncryptedTextField (PHI) — migration 0035
- Canonical H&P URL: `/api/history-physical-exams/` (alias `/api/history-physical/` also registered)
- H&P sign URL: `POST /api/history-physical-exams/{id}/sign/` (url_path='sign', method=sign_visit)
- H&P field names: `history_present_illness`, `assessment_plan`, `physical_exam_data`, `review_of_systems_data`
- Patient email is EncryptedField — ORM filter(email=...) broken; use `_get_patient_ids_for_email()` helper
- InBasketViewSet.summary uses ThreadParticipant.aggregate(Sum) — not values_list flat=True
- Test users: admin@herv3.local/Admin1234!, dr.johnson@herv3.local/Doctor1234!, nurse.miller@herv3.local/Nurse1234!
- Login endpoint uses email not username: POST /api/auth/login/legacy/ or /api/auth/login/

## nanoclaw (Personal Assistant Platform)

- Repo path on host: `/home/qgmoh/nanoclaw/`
- Stack: Node.js, TypeScript, Claude Agent SDK, Docker containers
- Function: Multi-channel personal AI assistant (WhatsApp, Telegram, Slack, etc.)
- Groups run in isolated containers with per-group CLAUDE.md and memory
- Amy = whatsapp_main group agent; Andy = main group agent (elevated privileges)
