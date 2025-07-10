import streamlit as st
import folium
from streamlit_folium import st_folium
from backend.route_engine import get_route  # Make sure this file exists

st.set_page_config(layout="wide")
st.title("🛰️ TACREX: Tactical Escape Route Planner")

# Input fields
start = st.text_input("Start coordinates (lat,lon)", "18.5204,73.8567")
end = st.text_input("Destination coordinates (lat,lon)", "18.5300,73.8600")

# Dummy threat zones (replace with real API later)
threat_zones = [
    {"lat": 18.524, "lon": 73.857, "radius": 300, "description": "Shelling Zone"},
    {"lat": 18.526, "lon": 73.859, "radius": 200, "description": "Sniper Alert"},
]

# Create map
m = folium.Map(location=[18.525, 73.858], zoom_start=14)

try:
    # Parse user input
    start_coords = [float(i) for i in start.split(",")]
    end_coords = [float(i) for i in end.split(",")]

    # Add start & end markers
    folium.Marker(start_coords, tooltip="Start", icon=folium.Icon(color='green')).add_to(m)
    folium.Marker(end_coords, tooltip="End", icon=folium.Icon(color='red')).add_to(m)

    # Get route from OpenRouteService (ORS uses lon, lat)
    route = get_route(start_coords[::-1], end_coords[::-1])

    if route:
        coords = route["features"][0]["geometry"]["coordinates"]
        coords_latlon = [[c[1], c[0]] for c in coords]  # Convert to (lat, lon)
        folium.PolyLine(locations=coords_latlon, color="blue", weight=5).add_to(m)
    else:
        st.error("Failed to fetch route from OpenRouteService.")

except Exception as e:
    st.warning(f"Invalid input or routing error: {e}")

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

