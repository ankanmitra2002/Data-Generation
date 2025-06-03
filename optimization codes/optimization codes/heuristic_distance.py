import json

# Load data
with open("./input/Routes.json") as f:
    route_dict = json.load(f)
Routes = list(route_dict.values())
route_ids = list(route_dict.keys())

with open("./input/passengers_group.json") as f:
    passengers = json.load(f)

with open("./input/passenger_routes_group.json") as f:
    feasible = json.load(f)

with open("./input/route_capacities.json") as f:
    capacity = json.load(f)

# Remaining capacities at each stop
remaining = {
    rid: {stop: capacity[rid] for stop in Routes[i]}
    for i, rid in enumerate(route_ids)
}

assign_options = []
for p, pdata in passengers.items():
    srcs = pdata["source"]
    dst = pdata["destination"]
    group_count = pdata["count"]

    for r_index in feasible[p]:
        rid = f"r{r_index}"
        route = route_dict[rid]

        for src in srcs:
            if src in route and dst in route:
                si, di = route.index(src), route.index(dst)
                if si < di:
                    seg = route[si:di+1]
                    assign_options.append((p, rid, len(seg), seg, group_count))

#
assign_options.sort(key=lambda x: x[2])


assigned = {}
used_capacity = remaining.copy()

for p, rid, seg_len, seg, count in assign_options:
    if p in assigned:
        continue  

    if all(remaining[rid][stop] >= count for stop in seg):
        for stop in seg:
            remaining[rid][stop] -= count
        assigned[p] = {"route": rid, "stops": seg, "count": count}


total_groups = len(passengers)
assigned_groups = len(assigned)
total_individuals = sum(p["count"] for p in passengers.values())
assigned_individuals = sum(info["count"] for info in assigned.values())

result = {
    "total_groups": total_groups,
    "assigned_groups": assigned_groups,
    "total_individuals": total_individuals,
    "assigned_individuals": assigned_individuals,
    "assignments": [{"passenger": p, **info} for p, info in assigned.items()]
}

with open("heuristic_distance_assignment.json", "w") as f:
    json.dump(result, f, indent=4)

print(f"Assigned {assigned_groups}/{total_groups} passenger groups")
print(f"Assigned {assigned_individuals}/{total_individuals} passengers")