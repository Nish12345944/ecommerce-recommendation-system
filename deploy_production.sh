#!/bin/bash

# Production Deployment Script for E-commerce Recommendation System

set -e

echo "🚀 Starting production deployment..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p ssl
mkdir -p logs
mkdir -p backups

# Generate SSL certificates (self-signed for development)
if [ ! -f ssl/cert.pem ]; then
    echo "🔐 Generating SSL certificates..."
    openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem -out ssl/cert.pem -days 365 -nodes \
        -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
fi

# Create environment file if it doesn't exist
if [ ! -f .env ]; then
    echo "⚙️ Creating environment file..."
    cp .env.production .env
    echo "📝 Please edit .env file with your production values"
fi

# Build and start services
echo "🏗️ Building Docker images..."
docker-compose -f docker-compose_production.yml build

echo "🚀 Starting services..."
docker-compose -f docker-compose_production.yml up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 30

# Run database migrations
echo "🗄️ Running database migrations..."
docker-compose -f docker-compose_production.yml exec web python -c "
from app_production import app, db
with app.app_context():
    db.create_all()
    print('Database initialized successfully')
"

# Check service health
echo "🏥 Checking service health..."
if curl -f http://localhost/health > /dev/null 2>&1; then
    echo "✅ Application is healthy and running!"
    echo "🌐 Access your application at: http://localhost"
    echo "🔒 HTTPS access at: https://localhost"
else
    echo "❌ Health check failed. Check logs:"
    docker-compose -f docker-compose_production.yml logs
fi

echo "📊 Service status:"
docker-compose -f docker-compose_production.yml ps

echo "🎉 Deployment completed!"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env file with your production values"
echo "2. Replace SSL certificates in ssl/ directory with real ones"
echo "3. Configure your domain DNS to point to this server"
echo "4. Set up monitoring and backups"
echo ""
echo "🔧 Useful commands:"
echo "  View logs: docker-compose -f docker-compose_production.yml logs -f"
echo "  Stop services: docker-compose -f docker-compose_production.yml down"
echo "  Restart: docker-compose -f docker-compose_production.yml restart"