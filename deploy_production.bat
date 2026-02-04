@echo off
echo 🚀 Starting production deployment...

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed. Please install Docker Desktop first.
    pause
    exit /b 1
)

docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose first.
    pause
    exit /b 1
)

REM Create necessary directories
echo 📁 Creating directories...
if not exist ssl mkdir ssl
if not exist logs mkdir logs
if not exist backups mkdir backups

REM Create environment file if it doesn't exist
if not exist .env (
    echo ⚙️ Creating environment file...
    copy .env.production .env
    echo 📝 Please edit .env file with your production values
)

REM Build and start services
echo 🏗️ Building Docker images...
docker-compose -f docker-compose_production.yml build

echo 🚀 Starting services...
docker-compose -f docker-compose_production.yml up -d

REM Wait for services to be ready
echo ⏳ Waiting for services to start...
timeout /t 30 /nobreak

REM Check service health
echo 🏥 Checking service health...
curl -f http://localhost/health >nul 2>&1
if errorlevel 1 (
    echo ❌ Health check failed. Check logs:
    docker-compose -f docker-compose_production.yml logs
) else (
    echo ✅ Application is healthy and running!
    echo 🌐 Access your application at: http://localhost
    echo 🔒 HTTPS access at: https://localhost
)

echo 📊 Service status:
docker-compose -f docker-compose_production.yml ps

echo 🎉 Deployment completed!
echo.
echo 📋 Next steps:
echo 1. Edit .env file with your production values
echo 2. Replace SSL certificates in ssl/ directory with real ones
echo 3. Configure your domain DNS to point to this server
echo 4. Set up monitoring and backups
echo.
echo 🔧 Useful commands:
echo   View logs: docker-compose -f docker-compose_production.yml logs -f
echo   Stop services: docker-compose -f docker-compose_production.yml down
echo   Restart: docker-compose -f docker-compose_production.yml restart

pause