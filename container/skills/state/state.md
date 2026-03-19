# STATE System — Low-Token Task Resumption

Use STATE for any multi-step task. It saves ~82% tokens by storing minimal progress JSON instead of replaying full conversation history.

## State Directory

```
/workspace/extra/projects/salad/state/
```

State files: `{task-id}.json`
Tools: `/workspace/extra/projects/salad/state/tools/state_manager.py`
Templates: `/workspace/extra/projects/salad/state/templates/`

## STATE Format

```json
{
  "v": 1,
  "t": "task-id",
  "g": "Goal (≤300 chars)",
  "s": "Summary of work done (≤300 chars)",
  "i": "Next action to take (≤300 chars)",
  "p": { "any": "params needed" }
}
```

## Quick Bash Commands

### Check for existing state
```bash
cat /workspace/extra/projects/salad/state/{task-id}.json 2>/dev/null
```

### Create new state
```bash
python3 -c "
import sys; sys.path.insert(0, '/workspace/extra/projects/salad/state/tools')
from state_manager import initial_state, save_state
state = initial_state('my-task-001', 'Goal description here')
state['i'] = 'First specific step'
state['p'] = {'key': 'value'}
save_state(state)
print('STATE created')
"
```

### Create from template
```bash
python3 -c "
import sys; sys.path.insert(0, '/workspace/extra/projects/salad/state/tools')
from state_manager import create_state_from_template, save_state
state = create_state_from_template('generic-task', {
    'TASK_ID': 'fix-login',
    'GOAL': 'Fix login timeout',
    'FIRST_STEP': 'Read auth config',
    'TASK_TYPE': 'bugfix',
    'SCOPE': 'src/auth/'
})
save_state(state)
"
```

### Update state after completing a step
```bash
python3 -c "
import sys; sys.path.insert(0, '/workspace/extra/projects/salad/state/tools')
from state_manager import load_state, save_state
state = load_state('my-task-001')
state['s'] = 'Completed step 1: read config, found issue'
state['i'] = 'Next: fix the timeout value in settings.py'
save_state(state)
"
```

### Mark task done
```bash
python3 -c "
import sys; sys.path.insert(0, '/workspace/extra/projects/salad/state/tools')
from state_manager import load_state, save_state
state = load_state('my-task-001')
state['s'] = 'All steps complete'
state['i'] = 'done'
state['p']['resolution'] = 'Fixed timeout, tested, deployed'
save_state(state)
"
```

### List all active states
```bash
ls /workspace/extra/projects/salad/state/*.json | grep -v templates
```

## Workflow

1. **Start task** → check if state file exists, create if not
2. **Read `i`** → that's where you resume from
3. **Do the work** described in `i`
4. **Update `s`** with what you did, **update `i`** with what's next
5. **Save state** after each significant step
6. **Mark done** when `i` = "done - [summary]"

## When to Use STATE

Use for: any task with 2+ steps, debugging, implementing features, research across multiple files

Skip for: single read/grep/question

## Available Templates

- `generic-task` — any task
- `container-fix` — Docker container issues

List templates:
```bash
ls /workspace/extra/projects/salad/state/templates/
```
