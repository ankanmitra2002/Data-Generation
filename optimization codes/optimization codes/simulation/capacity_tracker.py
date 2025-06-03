from collections import defaultdict
from utils import load_bus_timeline,time_to_minutes


class CapacityTracker:
    def __init__(self, bus_config, routes):
        self.bus_config = bus_config
        self.routes = routes
        self.timeline = defaultdict(lambda: defaultdict(dict))  # bus_id -> time -> stop -> cap

        self.arrivals = defaultdict(lambda: defaultdict(list))  # bus_id -> stop -> list of times
        bus_timeline = load_bus_timeline()

        
        for entry in bus_timeline:
            bus_id = entry["bus_id"]
            stop = entry["stop"]
            time_min = time_to_minutes(entry["arrival_time"])
            self.arrivals[bus_id][stop].append(time_min)

            if stop not in self.timeline[bus_id][time_min]:
                route_id = self.bus_config[bus_id]["route_id"]
                cap = self.bus_config[bus_id]["capacity"]
                self.timeline[bus_id][time_min][stop] = cap

        
        for bus_id in self.arrivals:
            for stop in self.arrivals[bus_id]:
                self.arrivals[bus_id][stop].sort()

    def get_buses(self, route_id):
        return [bid for bid, conf in self.bus_config.items() if conf["route_id"] == route_id]

    def get_departure_times(self, bus_id, stop, start_time, max_wait):
        """Return arrival times at stop within [start_time, start_time + max_wait]"""
        return [
            t for t in self.arrivals[bus_id][stop]
            if start_time <= t <= start_time + max_wait
        ]

    def can_fit(self, bus_id, start_time,Travel_time_per_stop,count, src, dest, stops):
        si = stops.index(src)
        di = stops.index(dest)
        segment = stops[si:di + 1]
        for i, stop in enumerate(segment):
            t = start_time + i * Travel_time_per_stop  
            if self.timeline[bus_id].get(t, {}).get(stop, 0) < count:
                
                return False
        return True
    def allocate(self, bus_id, start_time, Travel_time_per_stop, count, src, dest, stops):
        si = stops.index(src)
        di = stops.index(dest)
        segment = stops[si:di + 1]

        for i, stop in enumerate(segment):
            t = start_time + i * Travel_time_per_stop
            self.timeline[bus_id][t][stop] -= count

    def release(self, bus_id, time, stop, count):
        self.timeline[bus_id][time][stop] += count
