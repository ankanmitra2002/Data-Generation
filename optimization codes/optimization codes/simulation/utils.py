import json
import pandas as pd

def time_to_minutes(tstr):
    """Converts 'HH:MM' or 'HH:MM:SS' to total minutes since 00:00."""
    parts = list(map(int, tstr.strip().split(":")))

    if len(parts) == 2:
        h, m = parts
    elif len(parts) == 3:
        h, m, _ = parts  
    else:
        raise ValueError(f"Invalid time format: '{tstr}'")

    return h * 60 + m
def load_routes():
    with open("../input/Routes.json") as f:
        return json.load(f)

def load_bus_config():
    with open("../input/bus_config.json") as f:
        raw_config = json.load(f)

    flat_config = {}
    for route_id, buses in raw_config.items():
        for bus in buses:
            flat_config[bus["bus_id"]] = {
                "route_id": route_id,
                "capacity": bus["capacity"]
            }

    return flat_config

def load_bus_timeline():
    with open("../output/bus_timeline.json") as f:
        return json.load(f)

def find_feasible_routes(p, routes):
    sources = p["source"]
    destination = p["destination"]

    feasible_routes = []

    for rid, stops in routes.items():
        for src in sources:
            if src in stops and destination in stops:
                si = stops.index(src)
                di = stops.index(destination)

                if si < di:
                    # forward direction
                    feasible_routes.append({
                        "rid": rid,
                        "stops": stops
                    })
                    break
                elif si > di:
                    # reverse direction
                    reversed_stops = list(reversed(stops))
                    feasible_routes.append({
                        "rid": rid,
                        "stops": reversed_stops
                    })
                    break  

    return feasible_routes
def calculate_lambda_ratio():
    
    with open("../heuristic_mix.json") as f:
        mix_data = json.load(f)
        total_individuals = mix_data["total_individuals"]

    # Step 2: Load comparison_results.csv
    df = pd.read_csv("../comparison_results.csv")

    # Step 3: Calculate average of heuristic_mix column
    avg_heuristic_mix = df["heuristic_mix"].mean()

    # Step 4: Calculate ratio
    ratio = avg_heuristic_mix / total_individuals

    # Step 5: Print results
    print(f"Total Individuals in heuristic_mix.json: {total_individuals}")
    print(f"Average Assigned Individuals from comparison_results.csv (heuristic_mix): {avg_heuristic_mix:.2f}")
    print(f"Ratio (Avg Assigned / Total): {ratio:.4f}")
    return ratio