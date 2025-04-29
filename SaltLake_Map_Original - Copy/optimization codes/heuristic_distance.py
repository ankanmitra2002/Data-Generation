import json
from collections import defaultdict

# 1. Load data
with open("Routes.json") as f:
    route_dict = json.load(f)
Routes = list(route_dict.values())
route_ids = list(route_dict.keys())

with open("passengers_group.json") as f:
    passengers = json.load(f)

with open("passenger_routes.json") as f:
    feasible = json.load(f)

# 2. Set capacities (example: uniform capacity of 1 per route per stop)

with open("route_capacities.json") as f:
    route_capacities = json.load(f)

remaining = {
    rid: {stop: route_capacities[rid] for stop in Routes[i]}
    for i, rid in enumerate(route_ids)
}

# 3. Build list of (p, r, distance, segment_stops)
assign_options = []
for p, info in passengers.items():
    srcs, dst = info["source"], info["destination"]
    for rid in feasible[p]:
        rix = route_ids[rid] if False else f"r{rid}"
    # but our passenger_routes.json keys are list of indices, so:
    for ridx in feasible[p]:
        rid = f"r{ridx}"
        route = route_dict[rid]
        # find minimal segment among possible sources
        best_seg = None
        best_len = None
        for s in srcs:
            if s in route and dst in route:
                si, di = route.index(s), route.index(dst)
                if si < di:
                    seg = route[si : di + 1]
                    L = len(seg)
                    if best_len is None or L < best_len:
                        best_len, best_seg = L, seg
        if best_seg is not None:
            assign_options.append((p, rid, best_len, best_seg))

# 4. Sort by ascending segment length
assign_options.sort(key=lambda x: x[2])

# 5. Greedy assignment
assigned = {}
for p, rid, length, seg in assign_options:
    if p in assigned:
        continue  # already assigned
    # check capacity on all stops in seg
    if all(remaining[rid][stop] >= passengers[p].get("count",1) for stop in seg):
        # assign
        assigned[p] = {"route": rid, "stops": seg}
        # deduct capacity
        for stop in seg:
            remaining[rid][stop] -= passengers[p].get("count",1)

# 6. Output
total_assigned = sum(passengers[p].get("count", 1) for p in assigned)
result = {
    "assigned_count": len(assigned),
    "total_passengers": len(passengers),
    "total_assigned": total_assigned,
    "assignments": [
        {"passenger": p, **assigned[p]}
        for p in assigned
    ]
}

with open("heuristic_distance_assignment.json", "w") as f:
    json.dump(result, f, indent=4)

print(f"Greedy heuristic assigned {result['assigned_count']} out of {result['total_passengers']} passengers.")
print(f"Total assigned passengers: {result['total_assigned']}")
