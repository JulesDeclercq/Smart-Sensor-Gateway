#!/bin/bash

if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
else
    echo "Error: .env bestand niet gevonden op $(pwd)"
    exit 1
fi

BACKUP_DIR="./backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Backup InfluxDB data
docker exec time_series_db influx backup "$BACKUP_DIR" -t "$BACKUP_TOKEN"

# Backup Node-RED flows
cp ./nodered/data/flows.json $BACKUP_DIR/flows_backup.json

echo "Backup succesvol opgeslagen in $BACKUP_DIR"
