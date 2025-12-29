@echo off
echo Starting E-commerce Recommendation System Deployment...

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Docker is not installed. Please install Docker Desktop first.
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Docker Compose is not installed. Please install Docker Compose first.
    pause
    exit /b 1
)

REM Create instance directory if it doesn't exist
if not exist "instance" mkdir instance

REM Build and start the containers
echo Building Docker containers...
docker-compose build

echo Starting services...
docker-compose up -d

echo Waiting for services to start...
timeout /t 10 /nobreak >nul

echo Deployment complete!
echo Application is running at: http://localhost
echo Direct Flask app access: http://localhost:5000
echo.
echo To stop the application, run: docker-compose down
echo To view logs, run: docker-compose logs -f
pause