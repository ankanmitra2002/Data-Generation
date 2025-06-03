import json
import pandas as pd
import plotly.express as px

# ------------------ Load Input Files ------------------

# Load actual optimized results (baseline) from first run
with open("optimized_routes_multi.json") as f:
    actual_data = json.load(f)["assignments"]

# Load deviated optimized results (from altered constraints or parameters)
with open("optimized_routes_multiLPP.json") as f:
    deviated_data = json.load(f)["assignments"]

# Load passenger group info to know sources, destinations, and counts
with open("./input/passengers_group.json") as f:
    passengers_group = json.load(f)

# ------------------ Create Lookup Tables ------------------

# Maps from passenger ID (e.g., "P0") to their assignment in each dataset
actual_map = {a["passenger"]: a for a in actual_data}
deviated_map = {d["passenger"]: d for d in deviated_data}

# ------------------ Compare Assignments ------------------

comparison = []

# Create a unified set of passenger IDs across both datasets
all_passengers = sorted(set(actual_map.keys()) | set(deviated_map.keys()))

for p in all_passengers:
    actual = actual_map.get(p)      # Assignment in actual data
    deviated = deviated_map.get(p)  # Assignment in deviated data
    x_val = deviated["x[p, r]"] if deviated and "x[p, r]" in deviated else 0.0

    # Determine the status of assignment for each passenger
    if actual and deviated:
        if actual["route"] == deviated["route"] and actual["stops"] == deviated["stops"]:
            status = "match"  # Perfect match: same route and stops
        else:
            status = "mismatch"  # Route or stops differ
    elif actual and not deviated:
        status = "missing"  # Missing in deviated output
    elif deviated and not actual:
        status = "extra"  # Extra in deviated output not present in original
    else:
        status = "unknown"  # Fallback for unexpected case

    # Store comparison results
    comparison.append({
        "passenger": p,
        "x_val": x_val,
        "status": status,
        "actual_route": actual["route"] if actual else None,
        "deviated_route": deviated["route"] if deviated else None,
        "actual_stops": actual["stops"] if actual else None,
        "deviated_stops": deviated["stops"] if deviated else None
    })

# ------------------ Print Summary Statistics ------------------

total_passengers = len(all_passengers)
matched = sum(1 for c in comparison if c["status"] == "match")
mismatched = sum(1 for c in comparison if c["status"] == "mismatch")
missing = sum(1 for c in comparison if c["status"] == "missing")
extra = sum(1 for c in comparison if c["status"] == "extra")

print(f"Total Passengers: {total_passengers}")
print(f"Matched: {matched} ({100*matched/total_passengers:.1f}%)")
print(f"Mismatched: {mismatched}")
print(f"Missing (in deviated): {missing}")
print(f"Extra (only in deviated): {extra}")

# ------------------ Define Color Coding for Plot ------------------

# Color map for different statuses
colors = {
    "match": "green",    # ✅ Ideal case
    "mismatch": "orange",# ⚠️ Same passenger assigned, but incorrectly
    "missing": "blue",   # ❌ Passenger not assigned in deviated output
    "extra": "red",      # ❓ Unexpected assignment in deviated output
    "unknown": "gray"    # Fallback (shouldn't occur if data is consistent)
}

# ------------------ Convert Comparison Data to DataFrame ------------------

# Pandas DataFrame for easy plotting and processing
df = pd.DataFrame(comparison)
df["index"] = range(len(df))  # Create an index for plotting (x-axis)

# ------------------ Generate Interactive Plot Using Plotly ------------------

fig = px.scatter(
    df,
    x="index",       # X-axis: passenger index
    y="x_val",       # Y-axis: assignment value (from deviated data)
    color="status",  # Color-code points based on comparison result
    color_discrete_map=colors,
    hover_data=[
        "passenger",        # Show passenger ID on hover
        "status",           # Status (match/mismatch/etc.)
        "x_val",            # Assignment value
        "actual_route",     # Route from actual data
        "deviated_route"    # Route from deviated data
    ],
    title="Passenger Assignment Deviations (Actual vs Deviated)"
)

# Customize plot layout
fig.update_layout(
    xaxis_title="Passenger Index",
    yaxis_title="x[p, r] Value",
    legend_title="Status",
    template="plotly_white"  # Clean background style
)

# ------------------ Show Plot in Browser ------------------

fig.show()

# ------------------ (Optional) Save Plot to HTML File ------------------

# fig.write_html("passenger_assignment_deviation_plot.html")