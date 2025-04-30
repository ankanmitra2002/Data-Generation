import json
import csv
import os


FILES = {
    "multiUserMaximize": "optimized_routes_multi.json",
    "multiUserMaximizeLPP": "optimized_routes_multiLPP.json",
    "heuristic_groups": "heuristic_routes_multi.json",
    "heuristic_distance": "heuristic_distance_assignment.json"
}

def extract_results():
    results = {}

    
    if os.path.exists(FILES["multiUserMaximize"]):
        with open(FILES["multiUserMaximize"]) as f:
            data = json.load(f)
            total = sum(assign["count"] for assign in data["assignments"])
            results["multiUserMaximize"] = total

    
    if os.path.exists(FILES["multiUserMaximizeLPP"]):
        with open(FILES["multiUserMaximizeLPP"]) as f:
            data = json.load(f)
            total = sum(assign["count"] for assign in data["assignments"])
            results["multiUserMaximizeLPP"] = total

    
    if os.path.exists(FILES["heuristic_groups"]):
        with open(FILES["heuristic_groups"]) as f:
            data = json.load(f)
            total = sum(assign["count"] for assign in data["assignments"])
            results["heuristic_groups"] = total

    
    if os.path.exists(FILES["heuristic_distance"]):
        with open(FILES["heuristic_distance"]) as f:
            data = json.load(f)
            total = sum(assign["count"] for assign in data["assignments"])
            results["heuristic_distance"] = total

    return results

def append_to_csv(row_data, file="comparison_results.csv"):
    write_header = not os.path.exists(file) or os.path.getsize(file) == 0
    with open(file, "a", newline="") as f:
        writer = csv.DictWriter(
            f, 
            fieldnames=["multiUserMaximize", "multiUserMaximizeLPP", "heuristic_groups", "heuristic_distance"]
        )
        if write_header:
            writer.writeheader()
        writer.writerow(row_data)

if __name__ == "__main__":
    results = extract_results()
    if len(results) == 4:
        append_to_csv(results)
        print("Appended results to CSV")
    else:
        print("Could not find results from all four scripts.")
