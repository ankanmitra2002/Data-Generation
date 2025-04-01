import traci
import random
import json

SUMO_BINARY = "sumo-gui"  # Use "sumo" for visualization
SUMO_CONFIG = "busStop.sumocfg"  # Replace with your actual SUMO config

# Start SUMO in a non-blocking mode
traci.start([SUMO_BINARY, "-c", SUMO_CONFIG,"--start"])

# Extract all bus stops from SUMO network
bus_stops = traci.busstop.getIDList()
print("Bus Stops:", bus_stops)
num_passengers = 100
passengers = []

for i in range(num_passengers):
    source_stop = random.choice(bus_stops)
    destination_stop = random.choice(bus_stops)

    while destination_stop == source_stop:  # Ensure different source & destination
        destination_stop = random.choice(bus_stops)

    passenger_id = f"p{i}"
    assigned_route = random.choice(traci.route.getIDList())  # Assign a random route

    passengers.append({
        "id": passenger_id,
        "source": source_stop,
        "destination": destination_stop,
        "route": assigned_route
    })

# Store passenger data
with open("passengers.json", "w") as file:
    json.dump(passengers, file, indent=4)

print("Generated 100 passengers in random locations.")
traci.close()
