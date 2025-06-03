import json
import os
import random
from utils import load_routes
from datetime import timedelta

def seconds_to_hhmmss(seconds):
    return str(timedelta(seconds=seconds))

def generate_passenger(global_pid, routes):
    while True:
        route = random.choice(list(routes.values()))
        if len(route) >= 5:
            start_index = random.randint(0, len(route) - 4)
            src_stops = route[start_index:start_index + 3]
            dest_options = route[start_index + 3:]
            if dest_options:
                dest = random.choice(dest_options)
                break

    timestamp_seconds = random.randint(0, 86400 - 1)  
    passenger = {
        "id": f"P{global_pid:06d}",
        "source": src_stops,
        "destination": dest,
        "count": random.randint(1, 10),
        "timestamp": seconds_to_hhmmss(timestamp_seconds)
    }

    return passenger, timestamp_seconds

def main():
    routes = load_routes()
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    requests_dir = os.path.join(root_dir, "live_requests")
    os.makedirs(requests_dir, exist_ok=True)

   
    for f in os.listdir(requests_dir):
        if f.endswith(".json"):
            os.remove(os.path.join(requests_dir, f))

    total_passengers = 24 * 60 * 2  
    passengers_by_interval = {}

    for pid in range(total_passengers):
        passenger, timestamp_seconds = generate_passenger(pid, routes)

        
        interval_start = (timestamp_seconds // 300) * 5  
        passengers_by_interval.setdefault(interval_start, []).append(passenger)

    
    for interval_start, group in passengers_by_interval.items():
        filename = os.path.join(requests_dir, f"{interval_start}.json")
        with open(filename, "w") as f:
            json.dump(group, f, indent=4)

    print(f"Generated {len(passengers_by_interval)} interval batches in /live_requests/")

if __name__ == "__main__":
    main()
