@echo off
REM Quick Start Setup Script for AI Support Ticket Processor (Windows)
REM This script sets up the environment and starts the services

echo ================================
echo AI Support Ticket Processor
echo Quick Start Setup
echo ================================
echo.

REM Check for Docker
docker --version >nul 2>&1
if errorlevel 1 (
    echo.Cannot find Docker. Please install Docker Desktop first.
    echo. https://docs.docker.com/get-docker/
    exit /b 1
)
echo [OK] Docker found

docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Cannot find Docker Compose
    exit /b 1
)
echo [OK] Docker Compose found
echo.

REM Check for .env file
if not exist ".env" (
    echo [INFO] .env file not found. Creating from template...
    copy .env.example .env >nul
    echo [OK] Created .env file
    echo.
    echo [ACTION] Please edit .env with your configuration:
    echo.  - OPENAI_API_KEY (required)
    echo.  - GOOGLE_APPLICATION_CREDENTIALS_JSON (required for Google Sheets)
    echo.  - EMAIL_SMTP_USER, EMAIL_SMTP_PASSWORD (for alerts)
    echo.
    pause
) else (
    echo [OK] Found existing .env file
)

echo.
echo Starting services with Docker Compose...
echo.

REM Stop existing services
docker-compose down -v >nul 2>&1

REM Start services
docker-compose up -d
if errorlevel 1 (
    echo [ERROR] Failed to start Docker Compose services
    exit /b 1
)

echo.
echo [INFO] Waiting for services to be ready (10 seconds)...
timeout /t 10 /nobreak
echo.

REM Check n8n
for /f %%i in ('curl -s -o /dev/null -w "%%{http_code}" http://localhost:5678 2^>nul') do set n8n_status=%%i
if "%n8n_status%"=="200" (
    echo [OK] n8n is ready at http://localhost:5678
) else (
    echo [INFO] n8n may still be starting, check http://localhost:5678
)

REM Check Qdrant
for /f %%i in ('curl -s -o /dev/null -w "%%{http_code}" http://localhost:6333/health 2^>nul') do set qdrant_status=%%i
if "%qdrant_status%"=="200" (
    echo [OK] Qdrant is ready at http://localhost:6333
) else (
    echo [INFO] Qdrant may still be starting, check http://localhost:6333/health
)

echo.
echo ================================
echo Service Status
echo ================================
docker-compose ps

echo.
echo ================================
echo Next Steps
echo ================================
echo.
echo 1. Open n8n at http://localhost:5678
echo 2. Create account and login
echo 3. Import the workflow (n8n_workflow.json):
echo    - Create a new workflow
echo    - Import ^> Database ^> Load from file JSON
echo    - Select n8n_workflow.json
echo.
echo 4. Configure credentials in n8n:
echo    - OpenAI API key
echo    - Google Sheets
echo    - Email (optional)
echo.
echo 5. Ingest knowledge base:
echo    - For local: pip install openai qdrant-client
echo               $env:OPENAI_API_KEY="your-key"; python ingest_kb.py
echo.
echo    - Or in Docker: docker-compose exec -T n8n python /data/ingest_kb.py
echo.
echo 6. Test webhook:
echo    - curl -X POST http://localhost:5678/webhook/support-ticket ^
echo      -H "Content-Type: application/json" ^
echo      -d "{\"name\":\"Test\",\"email\":\"test@example.com\",\"subject\":\"Test\",\"message\":\"Test message\"}"
echo.
echo For more details, see README.md
echo.
