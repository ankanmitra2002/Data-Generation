import json
import os
import random
import numpy as np
from datetime import timedelta
from utils import load_routes,calculate_lambda_ratio

# ---------- CONFIG ----------
LAMBDA_RATIO = calculate_lambda_ratio()  
MINUTES_IN_DAY = 24 * 60
START_MINUTE = 6 * 60         # 6:00 AM
END_MINUTE = 24 * 60          # 11:59 PM
INTERVAL_MINUTES = 5
TOTAL_EXPECTED_REQUESTS = int((END_MINUTE - START_MINUTE) * LAMBDA_RATIO*2)
TOTAL_INTERVALS = (END_MINUTE - START_MINUTE) // INTERVAL_MINUTES
# ----------------------------

def seconds_to_hhmmss(seconds):
    return str(timedelta(seconds=int(seconds)))

def generate_passenger(global_pid, routes, timestamp_seconds):
    while True:
        route = random.choice(list(routes.values()))
        if len(route) >= 5:
            start_index = random.randint(0, len(route) - 4)
            src_stops = route[start_index:start_index + 3]
            dest_options = route[start_index + 3:]
            if dest_options:
                dest = random.choice(dest_options)
                break

    passenger = {
        "id": f"P{global_pid:06d}",
        "source": src_stops,
        "destination": dest,
        "count": random.randint(1, 6),
        "timestamp": seconds_to_hhmmss(timestamp_seconds)
    }

    return passenger

def main():
    routes = load_routes()
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    requests_dir = os.path.join(root_dir, "live_requests")
    os.makedirs(requests_dir, exist_ok=True)

    for f in os.listdir(requests_dir):
        if f.endswith(".json"):
            os.remove(os.path.join(requests_dir, f))

    print(f"Generating {TOTAL_EXPECTED_REQUESTS} requests using Poisson model...")

    passengers_by_interval = {}
    global_pid = 0

    for interval_offset in range(TOTAL_INTERVALS):
        interval_min = START_MINUTE + interval_offset * INTERVAL_MINUTES
        interval_start_seconds = interval_min * 60

        expected_interval_lambda = LAMBDA_RATIO * INTERVAL_MINUTES*2
        passenger_count = np.random.poisson(expected_interval_lambda)

        for _ in range(passenger_count):
            offset_within_interval = random.randint(0, INTERVAL_MINUTES * 60 - 1)
            timestamp = interval_start_seconds + offset_within_interval
            passenger = generate_passenger(global_pid, routes, timestamp)

            rounded_interval = (timestamp // 300) * 5
            passengers_by_interval.setdefault(rounded_interval, []).append(passenger)
            global_pid += 1


    for interval_min, group in passengers_by_interval.items():
        filename = os.path.join(requests_dir, f"{interval_min}.json")
        with open(filename, "w") as f:
            json.dump(group, f, indent=4)

    print(f"Created {len(passengers_by_interval)} interval files in /live_requests/")
    print(f"Total passengers generated: {global_pid}")

if __name__ == "__main__":
    main()
