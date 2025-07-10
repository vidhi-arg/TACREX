import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import folium
from streamlit_folium import st_folium
from backend.route_engine import get_route
from backend.risk_evaluator import evaluate_route_risk

st.set_page_config(layout="wide")
st.title("TACREX: Tactical Escape Route Planner")

# Input fields
start = st.text_input("Start coordinates (lat,lon)", "18.5204,73.8567")
end = st.text_input("Destination coordinates (lat,lon)", "18.5300,73.8600")

# Dummy threat zones
threat_zones = 
from backend.threat_ingestor import get_all_threats
threat_zones = get_all_threats()


# Create map
m = folium.Map(location=[18.525, 73.858], zoom_start=14)

try:
    # Parse user inputs
    start_coords = [float(i) for i in start.split(",")]
    end_coords = [float(i) for i in end.split(",")]

    # Add markers
    folium.Marker(start_coords, tooltip="Start", icon=folium.Icon(color='green')).add_to(m)
    folium.Marker(end_coords, tooltip="End", icon=folium.Icon(color='red')).add_to(m)

    # Get route from OpenRouteService (lon, lat)
    route = get_route(start_coords[::-1], end_coords[::-1])

    if route:
        coords = route["features"][0]["geometry"]["coordinates"]
        coords_latlon = [[c[1], c[0]] for c in coords]

        # Evaluate route risk
        risk = evaluate_route_risk(coords_latlon, threat_zones)
        st.subheader(f"Route Risk Level: {risk}")

        # Choose color by risk
        color = "green" if "Safe" in risk else "orange" if "Borderline" in risk else "red"
        folium.PolyLine(locations=coords_latlon, color=color, weight=5).add_to(m)
    else:
        st.error("Could not fetch route from OpenRouteService.")

except Exception as e:
    st.warning(f"Invalid input or routing error: {e}")
    
# Test marker from ACLED near Gaza (hardcoded)
folium.Circle(
    radius=300,
    location=[31.5019, 34.4666],
    color="red",
    fill=True,
    fill_color="crimson",
    fill_opacity=0.4,
    tooltip="Explosion: Strike hit residential building in Khan Yunis"
).add_to(m)

# Draw threat zones
for threat in threat_zones:
    folium.Circle(
        radius=threat["radius"],
        location=[threat["lat"], threat["lon"]],
        color="red",
        fill=True,
        fill_color="crimson",
        fill_opacity=0.4,
        tooltip=threat["description"]
    ).add_to(m)

# Show map
st_data = st_folium(m, width=1000, height=600)


