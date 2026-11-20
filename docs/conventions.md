# Team conventions
 
## Branches
- main is always working. Nobody pushes to main directly: use a branch and a pull request.
- Names: feature/<service>-<topic>, fix/<topic>, docs/<topic>, chore/<topic>
- Examples: feature/members-login, fix/vote-duplicate, docs/concept-note
 
## Commits
Start with a type, then a short message in the present tense:
feat: add login endpoint | fix: reject duplicate vote | test: add attendance tests
docs: update README | chore: configure ruff
 
## Pull requests
- Small (under about 400 changed lines) and about one thing.
- Reviewed by the other engineer before merging. CI must be green.
- Say what changed, why, and how you tested it.
 
## Code style
- Ruff checks and formats the code (make lint, make format). Line length 100.
- snake_case for names. Type hints on functions that other code calls.
 
## API rules
- Every route starts with /v1. Errors use the shared format (familymeet_common).
- Lists use ?page=1&page_size=20 (maximum 100).
 
## Configuration
- Settings come from environment variables written in UPPER_SNAKE_CASE.
- Every variable is listed in .env.example. The real .env is never committed.
 
## Ports
BFF 8000 | Members & Meetings 8001 | Debate 8002 | Treasury 8003 | AI Assistant 8004
