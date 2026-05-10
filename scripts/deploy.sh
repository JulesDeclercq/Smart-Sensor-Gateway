#!/bin/bash

# Verify folder
cd ~/smart-sensor-gateway || { echo "Map niet gevonden!"; exit 1; }

echo " Start CI/CD Deployment: Smart Sensor Gateway..."

# Fetch from Github
echo " Fetching latest code from GitHub..."
git pull origin main --rebase

# New images
echo " Pulling latest images..."
docker compose pull

# Kill stack & orphans
echo " Stopping and removing old containers..."
docker compose down --remove-orphans

# Delete old containers
docker rm -f grafana mqtt_broker portainer time_series_db sensor-sim 2>/dev/null || true

# Restart stack
echo " Starting new stack..."
docker compose up -d --build

# Cleanup
echo " Cleaning up unused Docker images..."
docker image prune -f

echo " Deployment successful! Run 'docker ps' to verify."
