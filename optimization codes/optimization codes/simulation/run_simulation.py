
import os
import json
from assigner import DynamicAssigner
from utils import time_to_minutes  

SIMULATION_DURATION = 24 * 60  
INTERVAL = 5 
LIVE_FOLDER = "../live_requests"
OUTPUT_FILE = "../output/dynamic_assignments.json"
WAIT_LIMIT = 20  
assigner = DynamicAssigner()

for current_time in range(360, SIMULATION_DURATION, INTERVAL):
   
    assigner.release_passengers(current_time)

    
    request_file = os.path.join(LIVE_FOLDER, f"{current_time}.json")
    if os.path.exists(request_file):
        with open(request_file) as f:
            all_passengers = json.load(f)

        
        passengers = [
            p for p in all_passengers
            if time_to_minutes(p["timestamp"]) <= current_time + WAIT_LIMIT
        ]

        print(f"T+{current_time:04d} | Loaded: {len(all_passengers)}")
        assigner.assign_batch(passengers, current_time)


assigner.export_logs()
with open(OUTPUT_FILE, "w") as f:
    json.dump(assigner.assignments, f, indent=4)

print("Dynamic simulation complete.")
