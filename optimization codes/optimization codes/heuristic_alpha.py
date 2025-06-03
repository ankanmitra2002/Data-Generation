import json

# Tuning parameter for the scoring function
ALPHA = 0  # You can adjust this: higher = prioritize group size, lower = prioritize shorter route

# --------------------- Load Input Files ---------------------

with open("./input/Routes.json") as f:
    route_dict = json.load(f)  # {route_id: [stops]}
Routes = list(route_dict.values())
route_ids = list(route_dict.keys())

with open("./input/passengers_group.json") as f:
    passengers = json.load(f)  # {passenger_id: {source, destination, count}}

with open("./input/passenger_routes_group.json") as f:
    feasible = json.load(f)  # {passenger_id: [feasible route indices]}

with open("./input/route_capacities.json") as f:
    capacity = json.load(f)  # {route_id: capacity_per_stop}

# --------------------- Preprocess ---------------------

# Create a remaining capacity map for each stop in each route
remaining = {
    rid: {stop: capacity[rid] for stop in route_dict[rid]}
    for rid in route_ids
}

# Precompute max values for normalization in scoring
max_group_size = max(p["count"] for p in passengers.values())
max_segment_length = max(
    len(route) for route in route_dict.values()
)

# --------------------- Collect Assignment Options ---------------------

assign_options = []

for p_id, pdata in passengers.items():
    srcs = pdata["source"]
    dst = pdata["destination"]
    group_count = pdata["count"]

    for r_index in feasible[p_id]:
        rid = f"r{r_index}"
        route = route_dict[rid]

        for src in srcs:
            # Only valid if both source and destination exist and source is before destination
            if src in route and dst in route:
                si, di = route.index(src), route.index(dst)
                if si < di:
                    segment = route[si:di+1]
                    segment_length = len(segment)

                    # Compute score: prioritize large groups and short paths
                    group_score = ALPHA * (max_group_size / group_count)
                    distance_score = (1 - ALPHA) * (1 - (segment_length / max_segment_length))
                    score = group_score + distance_score

                    assign_options.append((score, p_id, rid, segment, group_count))

# --------------------- Sort Options by Score (Descending) ---------------------

# Higher score is better → sort in descending order
assign_options.sort(key=lambda x: -x[0])

# --------------------- Perform Assignments ---------------------

assigned = {}  # Final assignment dict

for score, p_id, rid, segment, count in assign_options:
    if p_id in assigned:
        continue  # Already assigned

    # Check if enough capacity exists on all segment stops
    if all(remaining[rid][stop] >= count for stop in segment):
        # Assign and reduce capacities
        for stop in segment:
            remaining[rid][stop] -= count

        assigned[p_id] = {
            "route": rid,
            "stops": segment,
            "count": count,
            "score": round(score, 4)
        }

# --------------------- Output Summary ---------------------

total_groups = len(passengers)
assigned_groups = len(assigned)
total_individuals = sum(p["count"] for p in passengers.values())
assigned_individuals = sum(a["count"] for a in assigned.values())

result = {
    "total_groups": total_groups,
    "assigned_groups": assigned_groups,
    "total_individuals": total_individuals,
    "assigned_individuals": assigned_individuals,
    "assignments": [{"passenger": p, **info} for p, info in assigned.items()]
}

with open("heuristic_combined_assignment.json", "w") as f:
    json.dump(result, f, indent=4)

# --------------------- Final Print ---------------------

print(f"✅ Assignment complete using combined heuristic.")
print(f"🧍 Assigned {assigned_groups}/{total_groups} passenger groups")
print(f"👥 Assigned {assigned_individuals}/{total_individuals} passengers")
