#!/bin/bash

echo "Starting E-commerce Recommendation System Deployment..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create instance directory if it doesn't exist
mkdir -p instance

# Build and start the containers
echo "Building Docker containers..."
docker-compose build

echo "Starting services..."
docker-compose up -d

echo "Waiting for services to start..."
sleep 10

echo "Deployment complete!"
echo "Application is running at: http://localhost"
echo "Direct Flask app access: http://localhost:5000"
echo ""
echo "To stop the application, run: docker-compose down"
echo "To view logs, run: docker-compose logs -f"