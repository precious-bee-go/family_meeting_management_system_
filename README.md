# FamilyMeet
 
Family meeting management system for family associations in Cameroon:
meetings, debates and votes, finances and an assistance fund.
React Native mobile app with FastAPI microservices.
 
## Services
 
| Service | Port | Folder |
|---|---|---|
| GraphQL BFF | 8000 | bff |
| Members & Meetings | 8001 | services/members-meeting |
| Debate & Resolution | 8002 | services/debate |
| Treasury & Assistance | 8003 | services/treasury |
 
Shared code lives in libs/familymeet_common.
 
## Quick start (Windows, Command Prompt)
 
```
git clone https://github.com/OWNER/familymeet.git
cd familymeet
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
make test-common
copy .env.example .env
docker compose up --build -d
scripts\smoke.cmd
docker compose down
```
 
Open http://127.0.0.1:8001/docs in a browser to see the API of a running service.
 
## Useful commands
 
| Command | What it does |
|---|---|
| make lint | Check code style |
| make format | Fix code style |
| make test | Run all tests |
| make up / make down | Start / stop all containers |
 
## Team rules
See docs/CONVENTIONS.md. Open questions are in docs/DECISIONS.md.
    