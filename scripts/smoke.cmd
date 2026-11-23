@echo off
rem Checks that all four FamilyMeet services answer /health with 200.
set FAILED=0
for %%P in (8000 8001 8002 8003) do call :check %%P
if "%FAILED%"=="0" (
    echo All four services are healthy.
    exit /b 0
)
echo Some services are NOT healthy.
exit /b 1

:check
set CODE=000
for /f %%C in ('curl -s -o NUL -w "%%{http_code}" http://127.0.0.1:%1/health') do set CODE=%%C
echo port %1 : %CODE%
if not "%CODE%"=="200" set FAILED=1
exit /b 0