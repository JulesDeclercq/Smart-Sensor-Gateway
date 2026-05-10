# Smart-Sensor-Gateway

Semesteropdracht Switching Routing Wireless Essentials.

Gemaakt door Bram De Bevere en Jules Declercq.
In opdracht van dhr M. Leroy.

Focus van bijdragen:
- Bram: MQTT, Node-RED, Grafana
- Jules: Sensor script, InfluxDB, Back-ups

## Architectuur (dataflow)

Dit project is een Docker Compose-stack met gescheiden componenten voor opname, verwerking en persistente opslag.

**Datastroom**

1. **Sensor simulator (Python)**
   - `scripts/sensor.py` genereert telemetrie (temperatuur, luchtvochtigheid, CO₂) en publiceert JSON-berichten op MQTT-topics.
   - De topics in kwestie: `sensor/BevDecSns/sensor_1` en `sensor/BevDecSns/sensor_2`.

2. **MQTT broker (Mosquitto)**
   - De broker fungeert als message bus voor sensor-data.
   - Poort: `1883`.

3. **Node-RED (ETL / Stream Processing)**
   - Node-RED subscribe’t op `sensor/BevDecSns/#`.
   - Een function node parse’t/valideert de payload en zet deze om naar een structuur die geschikt is voor InfluxDB.

4. **InfluxDB (Time-series Storage)**
   - Persistente opslag van sensormetingen in een InfluxDB bucket.
   - Poort: `8086`.

5. **Grafana (Visualisatie)**
   - Grafana leest data uit InfluxDB en biedt dashboards/alerts.
   - Poort: `9001` (host) → `3000` (container).

**Schematisch**

`scripts/sensor.py` → `Mosquitto (MQTT)` → `Node-RED (flows.json)` → `InfluxDB` → `Grafana`

## Installatie en opstart

### Vereisten

- Docker Engine
- Docker Compose

### Configuratie

InfluxDB wordt bij de eerste start geïnitialiseerd via environment variables in `docker-compose.yml`.
Voorzie een `.env` bestand in de root van het project met minstens:

- `INFLUX_USER`
- `INFLUX_PASS`
- `INFLUX_ORG`
- `INFLUX_BUCKET`
- `INFLUX_TOKEN`

### Stack opstarten

Start alle services in detached mode:

```bash
docker-compose up -d
```

Stoppen en opruimen:

```bash
docker-compose down
```

### Exposed services

- Mosquitto: `tcp/1883`
- Node-RED: `http://localhost:1880`
- InfluxDB: `http://localhost:8086`
- Grafana: `http://localhost:9001`
- Portainer: `https://localhost:9443`

## CI/CD (deploy.sh)

De deployment is geïmplementeerd als **pull-based** update op de target host via `scripts/deploy.sh`.
Het script veronderstelt dat de repository op de server aanwezig is onder `~/smart-sensor-gateway`.

**Werking**

1. Navigeert naar de projectdirectory (`cd ~/smart-sensor-gateway`).
2. Voert `docker-compose pull` uit om de nieuwste images op te halen.
3. Doet een controlled restart van de stack met `docker-compose down`.
4. Start de stack opnieuw in background met `docker-compose up -d`.
5. Ruimt ongebruikte images op met `docker image prune -f`.

**Gebruik**

- Maak het script uitvoerbaar en voer het uit op de deployment host:

```bash
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

Opmerking: dit script voert geen build/test-stappen uit; het is bedoeld als operationele deploy-runbook voor een reeds correct geconfigureerde host.

## Uitbreiding 1: Grafana dashboard

Grafana is inbegrepen als service in `docker-compose.yml`.
Het Grafana dashbord bevat panels voor o.a. temperatuur, luchtvochtigheid en CO₂, voor real-time visualisatie van time-series data en de mogelijkheid tot alerting.

## Uitbreiding 2: Automatische backups

Volgende data wordt persistent geback-upt in een lokale folder (`/backups`) op de Virtuele Machine (afgezonderd van Docker):

- InfluxDB data volume: `./influxdb/data`. (bevat eigenlijke sensorwaarden)
- Node-RED runtime data: `./nodered/data` (bevat `flows.json`, credentials, context).

A.d.h.v. een cronjob wordt een back-up van deze gegevens aangemaakt iedere nacht om 2:00.
