import json
import random


with open("./input/passengers_group.json", "r") as f:
    passengers_data = json.load(f)

with open("./input/passenger_routes_group.json", "r") as f:
    feasible_routes = json.load(f)

with open("./input/Routes.json", "r") as f:
    route_dict = json.load(f)


Routes = list(route_dict.values())
route_ids = [f"r{i}" for i in range(len(Routes))]
route_map = dict(zip(route_ids, Routes))

with open("./input/route_capacities.json") as f:
    capacity = json.load(f)


route_stop_capacity = {
    rid: {stop: capacity[rid] for stop in route_map[rid]} for rid in route_ids
}


sorted_passengers = sorted(passengers_data.items(), key=lambda x: -x[1]["count"])

assignment_results = {"assignments": []}
total_groups_assigned = 0
total_passengers_assigned = 0


for p_id, pdata in sorted_passengers:
    group_count = pdata["count"]
    assigned = False

    for r_index in feasible_routes[p_id]:
        rid = f"r{r_index}"
        route_stops = route_map[rid]

       
        for src in pdata["source"]:
            if src in route_stops and pdata["destination"] in route_stops:
                if route_stops.index(src) < route_stops.index(pdata["destination"]):
                    start_idx = route_stops.index(src)
                    end_idx = route_stops.index(pdata["destination"])

                    segment = route_stops[start_idx:end_idx + 1]

                    
                    if all(route_stop_capacity[rid][stop] >= group_count for stop in segment):
                       
                        for stop in segment:
                            route_stop_capacity[rid][stop] -= group_count

                        assignment_results["assignments"].append({
                            "passenger": p_id,
                            "count": group_count,
                            "route": rid,
                            "stops": segment
                        })
                        total_groups_assigned += 1
                        total_passengers_assigned += group_count
                        assigned = True
                        break
        if assigned:
            break

with open("heuristic_routes_multi.json", "w") as file:
    json.dump(assignment_results, file, indent=4)

print("Heuristic assignment complete. Results saved to heuristic_routes_multi.json.")
print(f"Total passenger groups assigned: {total_groups_assigned}")
print(f"Total passengers assigned: {total_passengers_assigned}")
