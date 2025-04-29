import pulp
import json
import random

with open("passengers_group.json", "r") as f:
    passengers_data = json.load(f)

with open("passenger_routes_group.json", "r") as f:
    feasible_routes = json.load(f)

with open("Routes.json", "r") as f:
    route_dict = json.load(f)
    
with open("route_capacities.json") as f:
    capacity = json.load(f)

Routes = list(route_dict.values())

route_ids = [f"r{i}" for i in range(len(Routes))]
route_map = dict(zip(route_ids, Routes))




# --------------------------------------- Optimization Problem Formulation ---------------------------------------
prob = pulp.LpProblem("MaximizePassengerAssignments", pulp.LpMaximize)

# -------------------------------------------------Decision Variables----------------------------------------------
x = pulp.LpVariable.dicts("PassengerRoute", [(p, r) for p in passengers_data for r in route_ids], lowBound=0, upBound=1, cat="Continuous")
S = pulp.LpVariable.dicts("StopAssignment",
    [(p, r, stop) for p in passengers_data for r in route_ids for stop in set(sum(Routes, []))],
    lowBound=0,
    cat="Continuous"
)

# ------------------- Objective: Maximize Assigned Passengers ---------------------
prob += pulp.lpSum(x[p, r] * passengers_data[p]["count"] for p in passengers_data for r in route_ids)

# ------------------- Constraints ----------------------------
for p in passengers_data:
    sources = passengers_data[p]["source"]
    destination = passengers_data[p]["destination"]
    count = passengers_data[p]["count"]

    # Constraint 1: Each passenger group assigned to at most 1 route
    prob += pulp.lpSum(x[p, r] for r in route_ids if int(r[1:]) in feasible_routes[p]) <= 1

    for r in route_ids:
        r_index = int(r[1:])
        if r_index not in feasible_routes[p]:
            prob += x[p, r] == 0
            continue

        route_stops = route_map[r]

        # Constraint 2: If a passenger is assigned to a route, then all the bus stops from source to destination must be passenger count for that route for that passenger
        for stop in route_stops:
            if any(src in route_stops and destination in route_stops and route_stops.index(src) <= route_stops.index(stop) <= route_stops.index(destination) for src in sources):
                prob += S[p, r, stop] == count*x[p, r]

            else:
                prob += S[p, r, stop] == 0
            

# Constraint 3:  Max number of passengers per route for a given stop
for r in route_ids:
    for stop in set(sum(Routes, [])):
        prob += pulp.lpSum(S[p, r, stop] for p in passengers_data) <= capacity[r]

# ------------------- Solution ----------------------------
prob.solve()

assignment_results = {"assignments": []}
for p in passengers_data:
    for r in route_ids:
        if x[p, r].varValue > 0:
            r_index = int(r[1:])
            stops_in_route = Routes[r_index]
            assigned_stops = [stop for stop in stops_in_route if S[p, r, stop].varValue > 0]
            assignment_results["assignments"].append({
                "passenger": p,
                "count": passengers_data[p]["count"],
                "route": r,
                "stops": assigned_stops
            })

# Output Assignment
with open("optimized_routes_multiLPP.json", "w") as file:
    json.dump(assignment_results, file, indent=4)

print("Optimization complete. Results are saved to optimized_routes_multi.json")
