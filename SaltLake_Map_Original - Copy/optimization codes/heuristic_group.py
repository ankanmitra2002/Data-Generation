import json
import random
from typing import List, Set

class PassengerGroup:
    def _init_(self, group_id: str, passengers: Set[int]):
        self.group_id = group_id
        self.passengers = passengers
        self.size = len(passengers)

def assign_bus_to_largest_groups(groups: List[PassengerGroup], bus_capacity: int) -> Set[str]:
    # Sort groups by size (descending)
    groups.sort(key=lambda g: g.size, reverse=True)

    assigned_group_ids = set()
    assigned_passengers = set()

    for group in groups:
        if group.size <= bus_capacity:
            assigned_group_ids.add(group.group_id)
            assigned_passengers.update(group.passengers)
            bus_capacity -= group.size
            if bus_capacity == 0:
                break

    return assigned_group_ids

def main():
    # 1. Load input
    with open("passengers_group.json") as f:
        passenger_data = json.load(f)

    with open("route_capacities.json") as f:
        route_capacities = json.load(f)
    groups = []
    for gid, info in passenger_data.items():
        count = info["count"]
        # Just create dummy passenger IDs from 1 to count
        passengers = set(range(1, count + 1))
        groups.append(PassengerGroup(gid, passengers))

    # 2. Set random bus capacity
    bus_capacity = random.randint(30, 60)
    print(f"Randomly selected bus capacity: {bus_capacity}")
    

    # 3. Assign
    assigned_group_ids = assign_bus_to_largest_groups(groups, bus_capacity)

    # 4. Write output
    output = {
        "bus_capacity": bus_capacity,
        "assigned_groups": sorted(assigned_group_ids),
        "assigned_count": len(assigned_group_ids),
        "total_groups": len(groups)
    }

    with open("heuristic_group_assignment.json", "w") as f:
        json.dump(output, f, indent=4)

    print(f"Assigned {output['assigned_count']} out of {output['total_groups']} groups.")

if __name__ == "_main_":
    main()