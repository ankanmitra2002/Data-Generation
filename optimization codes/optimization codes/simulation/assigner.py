
import json
from collections import defaultdict
from capacity_tracker import CapacityTracker
from utils import load_routes, load_bus_config, find_feasible_routes,time_to_minutes
import csv
import os

T_UNIT = 2         
WAIT_LIMIT = 30    
TRAVEL_TIME_PER_STOP = 5  

class DynamicAssigner:
    def __init__(self):
        self.routes = load_routes()
        self.bus_config = load_bus_config()
        self.timeline = CapacityTracker(self.bus_config, self.routes)
        self.assignments = []
        self.active_passengers = defaultdict(list)  
        self.rejected = []
        self.assigned_ids = set()
    def assign_batch(self, passengers, current_time):
        if not passengers:
            return []

        max_group_count = max(p["count"] for p in passengers)

        heuristic_list = []
        for p in passengers:
            if p["id"] in self.assigned_ids:
                continue
            min_dest_index = float('inf')
            for rid, route in self.routes.items():
                if p["destination"] in route:
                    for src in p["source"]:
                        if src in route:
                            si, di = route.index(src), route.index(p["destination"])
                            if si < di:
                                min_dest_index = min(min_dest_index, di)
            score = min_dest_index * (max_group_count - p["count"] + 1) if min_dest_index != float("inf") else float("inf")
            heuristic_list.append((p, score))

        sorted_passengers = [p for p, _ in sorted(heuristic_list, key=lambda x: x[1])]

        for p in sorted_passengers:
            if p["id"] in self.assigned_ids:
                continue
            assigned = False
            group_count = p["count"]
            request_time = time_to_minutes(p["timestamp"])
            feasible = find_feasible_routes(p, self.routes)
           
            if not feasible:
                self.rejected.append({
                    "passenger_id": p["id"]
                })
                continue
            # print(feasible)
            for route_info in feasible:
                rid = route_info["rid"]
                stops = route_info["stops"]
                for src in p["source"]:
                    if src not in stops or p["destination"] not in stops:
                        continue

                    si = stops.index(src)
                    di = stops.index(p["destination"])
                    if si >= di:
                        continue

                    travel_time = (di - si) * TRAVEL_TIME_PER_STOP
                    for bus_id in self.timeline.get_buses(rid):
                        if assigned:
                            break
                        dep_times = self.timeline.get_departure_times(bus_id, src, request_time, WAIT_LIMIT)

                        for t in dep_times:
                            if self.timeline.can_fit(bus_id, t, TRAVEL_TIME_PER_STOP, group_count, src, p["destination"], stops):
                                self.timeline.allocate(bus_id, t,TRAVEL_TIME_PER_STOP, group_count, src, p["destination"], stops)
                                end_time = t + travel_time
                                self.assignments.append({
                                    "passenger_id": p["id"],
                                    "route": rid,
                                    "bus": bus_id,
                                    "start_time": t,
                                    "end_time": end_time,
                                    "count": group_count,
                                    "stops": stops[si:di + 1]
                                })
                                self.active_passengers[end_time].append((bus_id, p["destination"], group_count))
                                self.assigned_ids.add(p["id"])
                                assigned = True
                                break
                        if assigned:
                            break
                if assigned:
                    break
            if not assigned:
                self.rejected.append({
                    "passenger_id": p["id"]
                })
        return self.assignments



    def release_passengers(self, current_time):
        for bus_id, stop, count in self.active_passengers[current_time]:
            self.timeline.release(bus_id, current_time, stop, count)
        if current_time in self.active_passengers:
            del self.active_passengers[current_time]
    

    def export_logs(self, output_dir=None):
        if output_dir is None:
            output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "output"))
        os.makedirs(output_dir, exist_ok=True)

        with open(os.path.join(output_dir, "assignments.csv"), "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["passenger_id", "route", "bus", "start_time", "end_time", "count", "stops"])
            writer.writeheader()
            for a in self.assignments:
                writer.writerow({
                    "passenger_id": a["passenger_id"],
                    "route": a["route"],
                    "bus": a["bus"],
                    "start_time": a["start_time"],
                    "end_time": a["end_time"],
                    "count": a["count"],
                    "stops": " -> ".join(a["stops"])
                })

        with open(os.path.join(output_dir, "rejected_passengers.csv"), "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["passenger_id"])
            writer.writeheader()
            for r in self.rejected:
                writer.writerow(r)

        print("CSV logs exported to /output/")

