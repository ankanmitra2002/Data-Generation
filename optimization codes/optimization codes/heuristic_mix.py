import json


with open("input/Routes.json") as f:
    route_dict = json.load(f)
Routes = list(route_dict.values())
route_ids = list(route_dict.keys())

with open("input/passengers_group.json") as f:
    passengers = json.load(f)

with open("input/passenger_routes_group.json") as f:
    feasible = json.load(f)

with open("input/route_capacities.json") as f:
    capacities = json.load(f)


remaining = {
    rid: {stop: capacities[rid] for stop in Routes[i]}
    for i, rid in enumerate(route_ids)
}


max_group_count = max(p["count"] for p in passengers.values())


heuristic_list = []

for p, info in passengers.items():
    sources = info["source"]
    dest = info["destination"]
    group_size = info["count"]

    min_dest_index = float("inf")
    for ridx in feasible[p]:
        rid = f"r{ridx}"
        route = route_dict[rid]
        if dest in route:
            di = route.index(dest)
            min_dest_index = min(min_dest_index, di)

    if min_dest_index != float("inf"):
        score = min_dest_index * (max_group_count - group_size + 1)
    else:
        score = float("inf")  
    heuristic_list.append((p, score))


sorted_passengers = [pid for pid, _ in sorted(heuristic_list, key=lambda x: x[1])]


assignments = {}
for p in sorted_passengers:
    sources = passengers[p]["source"]
    dest = passengers[p]["destination"]
    count = passengers[p]["count"]

    best_rid = None
    best_segment = None
    best_dest_index = float("inf")

    for ridx in feasible[p]:
        rid = f"r{ridx}"
        route = route_dict[rid]

        if dest not in route:
            continue

        for src in sources:
            if src in route:
                si, di = route.index(src), route.index(dest)
                if si < di and di < best_dest_index:
                    segment = route[si:di + 1]
                    if all(remaining[rid][s] >= count for s in segment):
                        best_dest_index = di
                        best_rid = rid
                        best_segment = segment

    if best_rid:
        for s in best_segment:
            remaining[best_rid][s] -= count
        assignments[p] = {
            "route": best_rid,
            "stops": best_segment,
            "count": count
        }


total_groups = len(passengers)
total_groups_assigned = len(assignments)
total_passengers = sum(p["count"] for p in passengers.values())
total_assigned = sum(a["count"] for a in assignments.values())

result = {
    "total_groups": total_groups,
    "total_groups_assigned": total_groups_assigned,
    "total_individuals": total_passengers,
    "total_individuals_assigned": total_assigned,
    "assignments": [
        {"passenger": pid, **data} for pid, data in assignments.items()
    ]
}


with open("heuristic_mix.json", "w") as f:
    json.dump(result, f, indent=4)

print("Heuristic assignment complete.")
print(f"Assigned {total_assigned}/{total_passengers} individual passengers.")
print(f"Assigned {total_groups_assigned}/{total_groups} groups.")