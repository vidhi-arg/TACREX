import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(layout="wide")
st.title("TACREX: Tactical Escape Route Planner")

# Input boxes for start & end
start = st.text_input("Start coordinates (lat,lon)", "18.5204,73.8567")
end = st.text_input("Destination coordinates (lat,lon)", "18.5300,73.8600")

# Create map
m = folium.Map(location=[18.525, 73.858], zoom_start=14)

try:
    start_coords = [float(i) for i in start.split(",")]
    end_coords = [float(i) for i in end.split(",")]
    folium.Marker(start_coords, tooltip="Start", icon=folium.Icon(color='green')).add_to(m)
    folium.Marker(end_coords, tooltip="End", icon=folium.Icon(color='red')).add_to(m)
except:
    st.warning("Invalid coordinate format. Use lat,lon like 18.5204,73.8567")

# Show map
st_data = st_folium(m, width=1000)
