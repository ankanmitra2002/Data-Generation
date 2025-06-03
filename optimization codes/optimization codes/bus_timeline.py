import json
from datetime import datetime, timedelta
import os


ROUTES_PATH = "input/Routes.json"
BUS_CONFIG_PATH = "input/bus_config.json"
OUTPUT_PATH = "output/bus_timeline.json"


START_TIME = datetime.strptime("00:00", "%H:%M")
END_TIME = datetime.strptime("23:59", "%H:%M")
STOP_DURATION = timedelta(minutes=5)
REST_DURATION = timedelta(minutes=20)


with open(ROUTES_PATH) as f:
    route_dict = json.load(f)

with open(BUS_CONFIG_PATH) as f:
    bus_config = json.load(f)


timeline = []

def generate_timeline(bus_id, route_id, stops):
    current_time = START_TIME
    direction = 1  # 1 = forward, -1 = reverse

    while current_time < END_TIME:
        stops_iter = stops if direction == 1 else list(reversed(stops))
        for stop in stops_iter:
            timeline.append({
                "bus_id": bus_id,
                "route_id": route_id,
                "stop": stop,
                "arrival_time": current_time.strftime("%H:%M")
            })
            current_time += STOP_DURATION
            if current_time >= END_TIME:
                break
        current_time += REST_DURATION
        direction *= -1 


for route_id, buses in bus_config.items():
    stops = route_dict[route_id]
    for bus in buses:
        generate_timeline(bus["bus_id"], route_id, stops)


os.makedirs("output", exist_ok=True)
with open(OUTPUT_PATH, "w") as f:
    json.dump(timeline, f, indent=4)

print(f"Timeline generated and saved to {OUTPUT_PATH}")