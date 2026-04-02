#!/bin/bash

echo "🚀 Start CI/CD Deployment: Smart Sensor Gateway..."

cd ~/smart-sensor-gateway

echo "📦 Pulling latest images..."
docker-compose pull

echo "🛑 Stopping and removing old containers..."
docker-compose down

echo "🏗️ Starting new stack..."
docker-compose up -d

echo "🧹 Cleaning up unused Docker images..."
docker image prune -f

echo "✅ Deployment successful! Run 'docker ps' to verify."
