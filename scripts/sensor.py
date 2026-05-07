import paho.mqtt.client as mqtt
import time
import random
import json

# Config
BROKER = "localhost"
PORT = 1883
TOPIC_1 = "sensor/BevDecSns/sensor_1"
TOPIC_2 = "sensor/BevDecSns/sensor_2"

client = mqtt.Client()

print(f"Verbinden met MQTT broker op {BROKER}...")
try:
    client.connect(BROKER, PORT, 60)
    print("Verbonden! Publiceren gestart. Ctrl+C om te stoppen...\n")

    # Initial random values
    temp_1, luvo_1, co2_1 = round(random.uniform(-10.0, 32.0), 1), round(random.uniform(50.0, 90.0), 1), random.randint(400, 500)
    temp_2, luvo_2, co2_2 = round(random.uniform(-10.0, 32.0), 1), round(random.uniform(50.0, 90.0), 1), random.randint(400, 500)

    while True:
        # 1. Create the data as Python Dictionaries (Objects)
        sensor_data_1 = {"temperatuur": round(temp_1, 1), "luchtvochtigheid": round(luvo_1, 1), "co2": co2_1}
        sensor_data_2 = {"temperatuur": round(temp_2, 1), "luchtvochtigheid": round(luvo_2, 1), "co2": co2_2}

        # 2. Convert to JSON strings for transmission
        # This is what most modern subscribers will automatically parse as an object
        json_payload_1 = json.dumps(sensor_data_1)
        json_payload_2 = json.dumps(sensor_data_2)

        # 3. Publish directly
        client.publish(TOPIC_1, json_payload_1)
        client.publish(TOPIC_2, json_payload_2)

        print(f"Verstuurd naar {TOPIC_1}: {json_payload_1}")
        print(f"Verstuurd naar {TOPIC_2}: {json_payload_2}")

        time.sleep(3)

        # Value drift logic
        temp_1 = max(-10.0, min(32.0, temp_1 + round(random.uniform(-2.0, 2.0), 1)))
        luvo_1 = max(50.0, min(90.0, luvo_1 + round(random.uniform(-2.0, 2.0), 1)))
        co2_1 = max(400, min(500, co2_1 + random.randint(-5, 5)))

        temp_2 = max(-10.0, min(32.0, temp_2 + round(random.uniform(-2.0, 2.0), 1)))
        luvo_2 = max(50.0, min(90.0, luvo_2 + round(random.uniform(-2.0, 2.0), 1)))
        co2_2 = max(400, min(500, co2_2 + random.randint(-5, 5)))

except ConnectionRefusedError:
    print("\nKon niet verbinden met MQTT broker!")
except KeyboardInterrupt:
    print("\nProgramma gestopt...")
finally:
    client.disconnect()
