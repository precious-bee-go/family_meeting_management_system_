PYTHON = python
 
.PHONY: help lint format test test-common test-members test-debate test-treasury test-bff run-members run-debate run-treasury run-bff up down logs
 
help:
	@echo Targets: lint format test test-common up down logs run-members
 
lint:
	ruff check .
	ruff format --check .
 
format:
	ruff check . --fix
	ruff format .
 
test: test-common test-members test-debate test-treasury test-bff
 
test-common:
	cd libs/familymeet_common && $(PYTHON) -m pytest
 
test-members:
	cd services/members-meetings && $(PYTHON) -m pytest
 
test-debate:
	cd services/debate && $(PYTHON) -m pytest
test-treasury:
	cd services/treasury && $(PYTHON) -m pytest
 
test-bff:
	cd bff && $(PYTHON) -m pytest
 
run-members:
	cd services/members-meetings && uvicorn app.main:app --reload --port 8001
 
run-debate:
	cd services/debate && uvicorn app.main:app --reload --port 8002
 
run-treasury:
	cd services/treasury && uvicorn app.main:app --reload --port 8003
 
run-bff:
	cd bff && uvicorn app.main:app --reload --port 8000
 
up:
	docker compose up --build -d
 
down:
	docker compose down
 
logs:
	docker compose logs -f
