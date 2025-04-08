import pulp
import json
import random
# ----- Load Data -----
with open("passengers.json", "r") as f:
    passengers_data = json.load(f)

with open("passenger_routes.json", "r") as f:
    feasible_routes = json.load(f)

# ----- Define Route Set -----
Routes = [
    ["College More", "New Town", "Unitech", "Eco Space", "Aliah University", "Daber More", "ECO Park", "City"],
    ["Marquis Street", "SN Banerjee", "MG Road", "Shyambazar", "Sinthee More", "Baranagar", "Dunlop", "BT Road", "Tobin Road", "Khardah", "Titagarh", "Barrackpore"],
    ["Howrah", "Sealdah", "Park Circus", "Ruby", "Garia", "Sonarpur"],
    ["Tollygunge", "Hazra", "Kalighat", "Minto Park", "Esplanade", "Ultadanga", "Salt Lake"],
    ["Garia", "Jadavpur", "Kalighat", "Esplanade", "Howrah Station"],
    ["Thakurpukur", "Behala", "Tollygunge", "Hazra", "Esplanade", "Howrah Station"],
    ["Kasba", "Bosepukur", "Gariahat", "Golpark", "Hazra", "Kalighat", "Esplanade"],
    ["Bagbazar", "Shyambazar", "Beleghata", "Salt Lake", "Karunamoyee"],
    ["Rajarhat", "Newtown", "Salt Lake", "Ultadanga", "Esplanade", "Howrah Station"],
    ["Jadavpur", "Dhakuria", "Gariahat", "Rashbehari", "Kalighat", "Esplanade"],
    ["Dumdum", "Belgachia", "Shyambazar", "Esplanade", "Tollygunge", "Joka"],
    ["Barasat", "Dumdum", "Shyambazar", "Esplanade", "Maidan", "Rabindra Sadan"],
    ["Barasat", "Airport Gate No. 1", "VIP Road", "Ultadanga", "Phoolbagan", "Sealdah"],
    ["Garia", "Ballygunge", "Esplanade"],
    ["Tollygunge", "Rashbehari", "Gariahat", "Ballygunge", "Park Circus", "Sealdah"],
    ["Bagbazar", "Shyambazar", "Esplanade", "Park Circus", "Ruby Hospital"],
    ["Howrah Station", "Shibpur", "Alipore", "Tollygunge", "Garia"],
    ["Salt Lake Sector V", "Karunamoyee", "Ultadanga", "Phoolbagan", "Sealdah", "Park Street"],
    ["Howrah Station", "Esplanade", "Minto Park", "Gariahat", "Ruby Hospital", "Patuli"],
    ["Salt Lake", "Ultadanga", "Phoolbagan", "Park Circus", "Ruby", "Garia"],
    ["Dumdum", "Airport Gate No. 1", "VIP Road", "New Town", "Eco Park"],
    ["Tollygunge", "Kalighat", "Hazra", "Gariahat", "Ultadanga"],
    ["Garia", "Jadavpur", "Ballygunge", "Sealdah", "MG Road", "Howrah Station"],
    ["Barasat", "Dumdum", "VIP Road", "Ultadanga", "Ruby", "Garia"],
    ["Bagbazar", "Shyambazar", "Esplanade", "Sealdah", "Park Circus"],
    ["New Town", "ECO Park", "Salt Lake", "Karunamoyee", "Ultadanga", "Esplanade", "Howrah Station"],
    ["Esplanade", "Ultadanga", "Salt Lake", "New Town", "Rajarhat"],
    ["Garia", "Ruby", "Ultadanga", "Salt Lake", "Karunamoyee"],
    ["Park Street", "Sealdah", "Phoolbagan", "Ultadanga", "Dumdum"],
    ["Sealdah", "Phoolbagan", "Ultadanga", "Salt Lake", "New Town", "Eco Park"],
    ["Ruby", "Gariahat", "Ultadanga", "VIP Road", "Airport Gate No. 1", "Barasat"],
    ["Howrah", "Esplanade", "Ultadanga", "Salt Lake", "New Town"],
    ["Gariahat", "Ballygunge", "Park Circus", "VIP Road", "Airport Gate No. 1"],
    ["Kasba", "Gariahat", "Phoolbagan", "Ultadanga", "Dumdum"],
    ["Tollygunge", "Hazra", "Kalighat", "Esplanade", "Salt Lake", "New Town", "Rajarhat"],
    ["Esplanade", "Ultadanga", "Karunamoyee", "New Town", "Eco Space"],
    ["Behala", "Tollygunge", "Kalighat", "Esplanade", "Salt Lake", "Karunamoyee"],
    ["Park Circus", "MG Road", "Shyambazar", "Baranagar", "Dunlop", "Titagarh"],
    ["Alipore", "Minto Park", "Esplanade", "Ultadanga", "Karunamoyee", "Salt Lake Sector V"],
    ["Shyambazar", "MG Road", "SN Banerjee", "Esplanade", "Park Street", "Rabindra Sadan"],
    ["Howrah Station", "Esplanade", "Kalighat", "Jadavpur", "Garia", "Narendrapur"],
    ["Airport Gate No. 1", "VIP Road", "Ultadanga", "Salt Lake", "Sector V", "New Town"],
    ["Behala", "Sakherbazar", "Tollygunge", "Kalighat", "Hazra", "Minto Park", "Esplanade"],
    ["Baranagar", "Shyambazar", "MG Road", "Sealdah", "Park Circus", "Ruby"],
    ["Rajarhat", "New Town", "Eco Park", "Eco Space", "Unitech", "Salt Lake"],
    ["Thakurpukur", "Behala", "Sakherbazar", "New Alipore", "Alipore", "Minto Park"],
    ["Garia", "Kamalgazi", "Narendrapur", "Sonarpur", "Garia Station Road", "Ruby Hospital"],
    ["Salt Lake", "Karunamoyee", "Ultadanga", "Kankurgachi", "Sealdah", "Park Street"],
    ["Park Circus", "Ripon Street", "SN Banerjee", "Lalbazar", "Howrah Station"],
    ["Bagbazar", "Shyambazar", "Beleghata", "Phoolbagan", "Salt Lake", "Sector V"],
    ["Dumdum", "Lake Town", "Bangur", "Ultadanga", "Bidhannagar", "Salt Lake"],
    ["Howrah", "Lalbazar", "Esplanade", "Rashbehari", "Gariahat", "Ruby"],
    ["Esplanade", "Park Street", "Maidan", "Rabindra Sadan", "Bhowanipore", "Kalighat"],
    ["Jadavpur", "Dhakuria", "Gariahat", "Golpark", "Bosepukur", "Kasba"],
    ["Sealdah", "Moulali", "Park Circus", "Ballygunge", "Rashbehari", "Tollygunge"],
    ["Garia", "Jadavpur", "Kasba", "Bosepukur", "Gariahat", "Ruby"],
    ["BT Road", "Baranagar", "Sinthee", "Shyambazar", "MG Road", "Park Street"],
    ["Ultadanga", "Salt Lake", "New Town", "Eco Park", "Chinar Park", "Airport"],
    ["Howrah Station", "Lalbazar", "Minto Park", "Kalighat", "Jadavpur", "Garia"]
]

# Assign unique route IDs (r0, r1, ...)
route_ids = [f"r{i}" for i in range(len(Routes))]
route_map = dict(zip(route_ids, Routes))

# Assign dummy capacities to each route
random.seed(42)  # For reproducibility
capacity = {rid: random.randint(1, 2) for rid in route_ids}

# ----- Setup Model -----
prob = pulp.LpProblem("MaximizePassengerAssignments", pulp.LpMaximize)

# Create decision variables
x = pulp.LpVariable.dicts("PassengerRoute", [(p, r) for p in passengers_data for r in route_ids], cat="Binary")
S = pulp.LpVariable.dicts("StopAssignment", [(p, r, stop) for p in passengers_data for r in route_ids for stop in set(sum(Routes, []))], cat="Binary")

# Objective: Maximize the number of passengers assigned
prob += pulp.lpSum(x[p, r] for p in passengers_data for r in route_ids)

# ----- Constraints -----

for p in passengers_data:
    sources = passengers_data[p]["source"]
    destination = passengers_data[p]["destination"]

    # Constraint: Each passenger assigned to max 1 route
    prob += pulp.lpSum(x[p, r] for r in route_ids if int(r[1:]) in feasible_routes[p]) <= 1

    for r in route_ids:
        r_index = int(r[1:])
        if r_index not in feasible_routes[p]:
            prob += x[p, r] == 0
            continue

        route_stops = route_map[r]

        
        # Only allow stop assignment between source and destination (inclusive)
        for stop in route_stops:
            if any(src in route_stops and destination in route_stops and route_stops.index(src) <= route_stops.index(stop) <= route_stops.index(destination) for src in sources):
                prob += S[p, r, stop] == x[p, r]

            else:
                prob += S[p, r, stop] == 0

# Capacity constraints: max number of passengers per stop per route
for r in route_ids:
    for stop in set(sum(Routes, [])):
        prob += pulp.lpSum(S[p, r, stop] for p in passengers_data) <= capacity[r]

# ----- Solve -----
prob.solve()

# ----- Output Results -----
# Store Results
assignment_results = {"assignments": []}
for p in passengers_data:
    for r in route_ids:
        if x[p, r].varValue == 1:
            r_index = int(r[1:])  # Extract route number from route ID like "r7"
            stops_in_route = Routes[r_index]  # Only consider stops from this route
            assigned_stops = [stop for stop in stops_in_route if S[p, r, stop].varValue == 1]
            assignment_results["assignments"].append({
                "passenger": p,
                "route": r,
                "stops": assigned_stops
            })

# Save results to JSON file
with open("optimized_routes.json", "w") as file:
    json.dump(assignment_results, file, indent=4)

print("Optimization complete. Results saved to optimized_routes.json")