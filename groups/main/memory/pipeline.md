---
name: pipeline
description: Gated push policy — validation commands per project before any git push
type: reference
---

# Gated Push Policy — Andy

Never push without passing validation. Elevated privileges do NOT exempt this rule.

## Pipeline
```
1. commit locally → 2. validate → 3. security check → 4. git push
```

## Validation Commands

**herv3:**
```bash
cd /workspace/extra/home/qgmoh/projects/herv3
docker compose -f docker-compose.dev.improved.yml exec web pytest --tb=short -q
docker compose -f docker-compose.dev.improved.yml exec frontend npx tsc --noEmit
docker compose -f docker-compose.dev.improved.yml exec frontend npx eslint src --ext .ts,.tsx
```

**salad:**
```bash
cd /workspace/extra/home/qgmoh/projects/salad && python -m pytest src/tests/ -q --tb=short
```

**nanoclaw:**
```bash
cd /workspace/extra/home/qgmoh/nanoclaw && npm test && npx tsc --noEmit
```

## Security Check (all projects)
Review diff for: hardcoded secrets, PHI exposure, auth regressions, debug flags left on.
