import json
import time
import random
from datetime import datetime, timezone

from azure.core.exceptions import ResourceNotFoundError
from azure.storage.blob import BlobServiceClient

from config import CONNECTION_STRING

DEVICE_ID = "livingroom-01"
CONTAINER = "readings"
INTERVAL_SECONDS = 5

service = BlobServiceClient.from_connection_string(CONNECTION_STRING)
container = service.get_container_client(CONTAINER)

temperature = 21.0
heater_on = False

print("Simulator started. Press Ctrl+C to stop.")

while True:
    # 1. Buluttan komut var mi diye bak
    try:
        data = container.download_blob(f"commands/{DEVICE_ID}.json").readall()
        command = json.loads(data)["command"]
        if command == "heater_on":
            heater_on = True
        elif command == "heater_off":
            heater_on = False
    except ResourceNotFoundError:
        pass  # henuz komut yok

    # 2. Sahte sicaklik uret
    if heater_on:
        temperature += 0.3
    else:
        temperature -= 0.1
    temperature += random.uniform(-0.1, 0.1)
    temperature = max(15, min(28, temperature))

    now = datetime.now(timezone.utc)
    reading = {
        "deviceId": DEVICE_ID,
        "timestamp": now.isoformat(),
        "temperature": round(temperature, 1),
        "humidity": round(random.uniform(40, 55), 1),
        "motion": random.choice([True, False]),
        "heaterOn": heater_on,
    }

    # 3. Olcumu buluta yukle
    blob_name = f"{DEVICE_ID}/{now.strftime('%Y%m%dT%H%M%SZ')}.json"
    container.upload_blob(name=blob_name, data=json.dumps(reading), overwrite=True)
    print("Sent:", reading)

    time.sleep(INTERVAL_SECONDS)