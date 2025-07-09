import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(layout="wide")
st.title("TACREX: Tactical Escape Route Planner")

# Input boxes
start = st.text_input("Start coordinates (lat,lon)", "18.5204,73.8567")
end = st.text_input("Destination coordinates (lat,lon)", "18.5300,73.8600")

# Dummy threat zones
threat_zones = [
    {"lat": 18.524, "lon": 73.857, "radius": 300, "description": "Shelling Zone"},
    {"lat": 18.526, "lon": 73.859, "radius": 200, "description": "Sniper Alert"},
]

# Create map
m = folium.Map(location=[18.525, 73.858], zoom_start=14)

# Mark start & end
try:
    start_coords = [float(i) for i in start.split(",")]
    end_coords = [float(i) for i in end.split(",")]
    folium.Marker(start_coords, tooltip="Start", icon=folium.Icon(color='green')).add_to(m)
    folium.Marker(end_coords, tooltip="End", icon=folium.Icon(color='red')).add_to(m)
except:
    st.warning("Invalid coordinate format. Use lat,lon like 18.5204,73.8567")

# Plot threat zones
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
st_data = st_folium(m, width=1000)

