"""
GPS Stop Detection & Analysis Script
====================================

This script processes raw GPS data from a CSV file to detect vehicle stops, 
merge nearby consecutive stops, classify movement states, and enrich stops with 
human-readable location names using reverse geocoding.

It is designed for analyzing GPS tracking datasets where:
- Each row contains a timestamp, latitude, and longitude.
- Gaps between points may indicate stops or GPS errors.

Key Features:
-------------
1. Detects "stop" events when there is a time gap greater than a threshold (default: 10 minutes).
2. Merges consecutive stop points that are within a small distance (default: 100m).
3. Classifies each segment as:
   - Normal (short gap, normal movement),
   - Stopped (stationary event),
   - Driving (GPS gap detected),
   - GPS Error (invalid/unrealistic speed).
4. Reverse-geocodes stop coordinates into readable addresses using OpenStreetMap (Nominatim).
5. Outputs a clean CSV (`stopped_locations.csv`) with stops, times, and addresses.

Requirements:
-------------
- Python 3.9+ recommended
- Required packages: 
  - pandas
  - geopy

Install dependencies with:
    pip install pandas geopy

Input:
------
- `output.csv` in the same directory (`output.csv`), with at least these columns:
    timestamp (Unix seconds), latitude, longitude

Output:
-------
- `stopped_locations.csv` in the same directory, with columns:
    latitude, longitude, location_name, time_arrival, time_departure, time_diff_str

Usage:
------
Run the script directly:
    python gps_stop_analysis.py

"""

import os
import pandas as pd
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

# ===================================================================
# Configurable parameters
# ===================================================================
CONFIG = {
    # File paths
    "input_csv": "../output.csv",
    "output_csv": "../stopped_locations.csv",

    # Stop detection
    "minimum_stop_duration": 600,   # seconds (10 min)
    "merge_dist_threshold": 100,    # meters for merging consecutive stops

    # Classification thresholds
    "classify_time_threshold": 600, # seconds
    "classify_dist_threshold": 250, # meters
    "stopped_speed_threshold": 0.5, # m/s (below this = stopped)
    "driving_speed_max": 40,        # m/s (~144 km/h), above = GPS error

    # Geocoding
    "geocoder_user_agent": "gps_analysis",
    "reverse_geocode_delay": 1,     # seconds delay to respect API rate limits
}


def calculate_distance(lat1, lng1, lat2, lng2):
    """Calculate the geodesic distance (in meters) between two GPS coordinates."""
    if pd.isna(lat1) or pd.isna(lng1) or pd.isna(lat2) or pd.isna(lng2):
        return None
    return geodesic((lat1, lng1), (lat2, lng2)).meters


def merge_consecutive_stops(df, dist_threshold):
    """
    Merge consecutive stop rows that are within a distance threshold.
    """
    merged_rows = []
    i = 0
    while i < len(df):
        current = df.iloc[i]
        merged = current.copy()
        j = i + 1
        while j < len(df):
            next_row = df.iloc[j]
            dist = calculate_distance(
                current["latitude"],
                current["longitude"],
                next_row["prev_latitude"],
                next_row["prev_longitude"],
            )
            if dist is not None and dist < dist_threshold:
                # Extend the stop to include the later row
                merged["timestamp"] = int(next_row["timestamp"])
                merged["latitude"] = next_row["latitude"]
                merged["longitude"] = next_row["longitude"]
                j += 1
            else:
                break
        merged_rows.append(merged)
        i = j

    merged_df = pd.DataFrame(merged_rows)
    merged_df["timestamp"] = merged_df["timestamp"].astype("int64")
    merged_df["prev_timestamp"] = (
        merged_df["prev_timestamp"].fillna(pd.NA).astype("Int64")
    )
    return merged_df


def classify_row(row, time_threshold, dist_threshold, stopped_speed, driving_speed_max):
    """
    Classify a GPS segment based on stop duration, distance, and average speed.
    """
    if row["time_difference"] <= time_threshold:
        return "Normal"

    if row["distance"] < dist_threshold:
        return "Stopped"

    speed = row["avg_speed_m_s"]
    if speed < stopped_speed:
        return "Stopped"
    elif stopped_speed <= speed <= driving_speed_max:
        return "Driving (GPS gap)"
    else:
        return "GPS Error"


def get_location_name(lat, lon):
    """
    Reverse-geocode a latitude/longitude into a human-readable address.
    """
    try:
        location = reverse((lat, lon), language="en")
        return location.address if location else "Unknown"
    except Exception:
        return "Error"


# ===================================================================
# Main Script Execution
# ===================================================================
geolocator = Nominatim(user_agent=CONFIG["geocoder_user_agent"])
reverse = RateLimiter(geolocator.reverse, min_delay_seconds=CONFIG["reverse_geocode_delay"])

csv_file = CONFIG["input_csv"]
output_csv = CONFIG["output_csv"]

# 1. Verify input file
if not os.path.isfile(csv_file):
    print(f"Error: The file '{csv_file}' does not exist.", flush=True)
    exit(1)
else:
    print(f"The file '{csv_file}' exists.", flush=True)

# 2. Load CSV
df = pd.read_csv(csv_file)
print(f"Number of rows: {len(df)}", flush=True)

# Sort and prepare columns
df_sorted = df.sort_values(by="timestamp")
df_sorted["prev_timestamp"] = df_sorted["timestamp"].shift(1).astype("Int64")
df_sorted["prev_latitude"] = df_sorted["latitude"].shift(1)
df_sorted["prev_longitude"] = df_sorted["longitude"].shift(1)

# 3. Find potential stops (time gaps > threshold)
df_sorted["time_difference"] = df_sorted["timestamp"] - df_sorted["prev_timestamp"]
filtered_df = df_sorted[df_sorted["time_difference"] > CONFIG["minimum_stop_duration"]].reset_index(drop=True)
print(f"Number of rows after filtering: {len(filtered_df)}", flush=True)

# 4. Merge consecutive nearby stops
merged_stops_df = merge_consecutive_stops(filtered_df, CONFIG["merge_dist_threshold"])
print(f"Number of rows after merge: {len(merged_stops_df)}", flush=True)

# 5. Compute distance, duration, speed
merged_stops_df["distance"] = merged_stops_df.apply(
    lambda row: calculate_distance(
        row["latitude"], row["longitude"], row["prev_latitude"], row["prev_longitude"]
    ),
    axis=1,
)
merged_stops_df["time_diff_str"] = merged_stops_df["time_difference"].apply(
    lambda x: (f"{(x // 3600)} hr " if x // 3600 > 0 else "")
    + (f"{round((x % 3600) / 60)} min" if pd.notna(x) else "")
)
merged_stops_df["avg_speed_m_s"] = (
    merged_stops_df["distance"] / merged_stops_df["time_difference"]
)
merged_stops_df["status"] = merged_stops_df.apply(
    classify_row,
    axis=1,
    time_threshold=CONFIG["classify_time_threshold"],
    dist_threshold=CONFIG["classify_dist_threshold"],
    stopped_speed=CONFIG["stopped_speed_threshold"],
    driving_speed_max=CONFIG["driving_speed_max"],
)
movement_counts = merged_stops_df["status"].value_counts()
print("Movement Counts:")
for status, count in movement_counts.items():
    print(f"  {status:<10} {count}")


# 6. Total stopped time
total_stopped_time = merged_stops_df["time_difference"].sum()
h = total_stopped_time // 3600
m = round((total_stopped_time % 3600) / 60)
stopped_time_str = f"{m} min" if h == 0 else f"{h} hr {m} min"
print(f"Total stopped time: {stopped_time_str}", flush=True)

# 7. Reverse-geocode stop locations
total = len(merged_stops_df)
merged_stops_df["location_name"] = ""
for idx, (i, row) in enumerate(merged_stops_df.iterrows(), 1):
    if row["status"] == "Stopped":
        merged_stops_df.at[i, "location_name"] = get_location_name(row["latitude"], row["longitude"])
    else:
        merged_stops_df.at[i, "location_name"] = ""

    # Print progress on the same line
    print(f"Processing location names: {idx}/{total}", end="\r", flush=True)
print('', flush=True)  # move to a clean new line at the end

num_valid = (
    merged_stops_df["location_name"].apply(lambda x: x not in ("Unknown", "Error")).sum()
)
num_error = (
    merged_stops_df["location_name"].apply(lambda x: x in ("Unknown", "Error")).sum()
)
print(f"Valid location names: {num_valid}", flush=True)
print(f"Errors or unknowns: {num_error}", flush=True)

# 8. Save output CSV with stop details
output_df = merged_stops_df.copy()
output_df["time_arrival"] = pd.to_datetime(output_df["prev_timestamp"], unit="s")
output_df["time_departure"] = pd.to_datetime(output_df["timestamp"], unit="s")
output_df[
    ["latitude", "longitude", "location_name", "time_arrival", "time_departure", "time_diff_str"]
].to_csv(output_csv, index=False)
print(f"Output CSV saved to {output_csv}", flush=True)
