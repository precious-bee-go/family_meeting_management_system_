# FamilyMeet concept note
 
## Problem
Families in Cameroon hold monthly meetings. Members abroad cannot follow, and money
(contributions, fines, assistance) is often disputed because records are kept in notebooks.
 
## Goal
One transparent platform for meetings, debates and votes, finances and the assistance fund.
 
## Users and roles
member, president, secretary, treasurer, assistance_committee
 
## Services and boundaries
| Service | Owns | Does not own |
|---|---|---|
| Members & Meetings (8001) | members, roles, login, meetings, agenda, attendance, minutes | money, votes |
| Debate & Resolution (8002) | debates, posts, votes, results | members, money |
| Treasury & Assistance (8003) | contributions, fines, expenses, assistance, fund ledger | meetings, votes |
| GraphQL BFF (8000) | nothing (stateless) | any business rule |
| AI Assistant (8004, Phase 5) | conversations, minutes drafts, audit log | any decision |
 
## Rules we all follow
- One owner per fact. No shared database tables.
- Business rules live in the owning service, never in the BFF.
- Every service has /health and /ready.
 
## Out of scope for the MVP
Real Mobile Money, many families (multi-tenancy), subscription billing, app store release.