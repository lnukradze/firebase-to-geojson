from flask import Flask, jsonify
import requests

app = Flask(__name__)

FIREBASE_URL = "https://ln-gps-tracker-default-rtdb.firebaseio.com/live_locations.json"

@app.route("/", methods=["GET"])
def get_locations():
    response = requests.get(FIREBASE_URL)
    data = response.json()

    geojson = {
        "type": "FeatureCollection",
        "features": []
    }

    for record_id, loc in data.items():
        if isinstance(loc, dict) and "lat" in loc and "lon" in loc:
            feature = {
                "type": "Feature",
                "properties": {
                    "device_id": loc.get("tid", "Unknown"),
                    "timestamp": loc.get("tst", 0)
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [loc["lon"], loc["lat"]]
                }
            }
            geojson["features"].append(feature)

    return jsonify(geojson)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
