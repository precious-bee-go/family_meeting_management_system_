@echo off
echo Checking the /health endpoint of every service (expect 200 for each)
for %%p in (8000 8001 8002 8003) do (
  echo Port %%p:
  curl -s -o NUL -w "%%{http_code}\n" http://127.0.0.1:%%p/health
)
docker compose up --build -d
docker compose ps
scripts\smoke.cmd
