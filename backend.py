import json
from datetime import datetime, timezone

from flask import Flask, jsonify, request
from azure.storage.blob import BlobServiceClient

from config import CONNECTION_STRING

app = Flask(__name__)
service = BlobServiceClient.from_connection_string(CONNECTION_STRING)
container = service.get_container_client("readings")


def get_readings(device_id, limit):
    names = sorted(
        b.name for b in container.list_blobs(name_starts_with=f"{device_id}/")
    )
    names = names[-limit:]
    return [json.loads(container.download_blob(n).readall()) for n in names]


@app.get("/devices/<device_id>/readings/latest")
def latest_reading(device_id):
    readings = get_readings(device_id, 1)
    if not readings:
        return jsonify({"error": "No readings found"}), 404
    return jsonify(readings[0])


@app.get("/devices/<device_id>/readings")
def reading_history(device_id):
    limit = request.args.get("limit", default=20, type=int)
    return jsonify(get_readings(device_id, limit))


@app.post("/devices/<device_id>/commands")
def send_command(device_id):
    body = request.get_json(silent=True) or {}
    command = body.get("command")
    if command not in ("heater_on", "heater_off"):
        return jsonify({"error": "command must be heater_on or heater_off"}), 400

    payload = {
        "deviceId": device_id,
        "command": command,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    container.upload_blob(
        name=f"commands/{device_id}.json", data=json.dumps(payload), overwrite=True
    )
    return jsonify(payload), 201


if __name__ == "__main__":
    app.run(port=5000)