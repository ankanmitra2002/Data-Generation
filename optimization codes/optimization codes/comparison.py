import json
import csv
import os

# Output files from different methods
FILES = {
    "multiUserMaximize": "optimized_routes_multi.json",
    "heuristic_groups": "heuristic_routes_multi.json",
    "heuristic_destination_time": "heuristic_destination_time.json",
    "heuristic_mix": "heuristic_mix.json",
}

def extract_results():
    results = {}
    for method, filepath in FILES.items():
        if os.path.exists(filepath):
            with open(filepath) as f:
                data = json.load(f)
                if "assignments" in data:
                    total = sum(a.get("count", 0) for a in data["assignments"])
                else:
                    total = data.get("assigned_individuals", 0)
                results[method] = total
    return results

def append_to_csv(row_data, file="comparison_results.csv"):
    file_exists = os.path.exists(file) and os.path.getsize(file) > 0
    with open(file, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(FILES.keys()))
        if not file_exists:
            writer.writeheader()
        writer.writerow(row_data)

if __name__ == "__main__":
    results = extract_results()
    if set(results.keys()) == set(FILES.keys()):
        append_to_csv(results)
        print("Appended results to CSV")
    else:
        print("Could not find results from all four scripts.")
