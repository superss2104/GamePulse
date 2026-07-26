@echo off
echo ==================================================
echo      Starting CSpotlight Development Servers
echo ==================================================

:: Start the Python backend server
:: NOTE: --reload is intentionally omitted. Hot-reload restarts the server
:: process, which wipes the in-memory job store and causes 404 errors mid-run.
:: Restart the backend window manually after making Python code changes.
echo Starting FastAPI Backend...
start "CSpotlight Backend" cmd /k "py -m uvicorn server.app:app --port 8000"

:: Start the Next.js web frontend
echo Starting Next.js Frontend...
start "CSpotlight Frontend" cmd /k "cd web && npm run dev"

echo Done! Both services are launching in new windows.
echo You can close this window now.
