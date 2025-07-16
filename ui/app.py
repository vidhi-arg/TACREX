import streamlit as st
from streamlit_folium import st_folium
import folium
from geopy.geocoders import Nominatim

from backend.route_engine import get_multiple_routes
from backend.risk_evaluator import evaluate_all_routes
from backend.threat_feed import get_all_threats
from backend.twitter_feed import get_live_threats
from backend.recommendations import get_safety_recommendations, find_shelters_near_route

st.set_page_config(layout="wide")
st.title("TACREX - Tactical Conflict Routing Engine")

# Geocoding
geolocator = Nominatim(user_agent="tacrex-app")

def geocode_location(place):
    try:
        location = geolocator.geocode(place)
        if location:
            return (location.latitude, location.longitude)
    except:
        pass
    return None

# Inputs
start_place = st.text_input("Start Location", "Zaporizhzhia, Ukraine")
end_place = st.text_input("End Location", "Dnipro, Ukraine")

start_coords = geocode_location(start_place)
end_coords = geocode_location(end_place)

if start_coords and end_coords:
    # Fetch up to 3 routes
    routes = get_multiple_routes(start_coords[::-1], end_coords[::-1])
    
    # Load threats
    threat_zones = get_all_threats()
    live_threats = get_live_threats()

    # Evaluate each route
    evaluated = evaluate_all_routes(routes, threat_zones)

    # Build map
    m = folium.Map(location=start_coords, zoom_start=9)
    color_map = {"Safe": "green", "High Risk": "red", "Moderate": "orange", "Unknown": "gray"}

    for idx, result in enumerate(evaluated):
        folium.PolyLine(
            result["route"],
            color=color_map.get(result["risk"], "blue"),
            weight=4.5,
            opacity=0.8,
            tooltip=f"Route {idx + 1} - Risk: {result['risk']}"
        ).add_to(m)

    # Draw static threat zones
    for zone in threat_zones:
        folium.Polygon(locations=zone, color="red", fill=True, fill_opacity=0.4).add_to(m)

    # Draw live threat points
    for threat in live_threats:
        folium.Circle(
            radius=300,
            location=threat["location"],
            color="orange",
            fill=True,
            fill_opacity=0.5,
            tooltip=threat["type"] + ": " + threat["description"]
        ).add_to(m)

    # Pick safest route
    safest = next((r for r in evaluated if r["risk"] == "Safe"), evaluated[0])

    # Dummy shelter database
    shelter_db = [
        {"name": "Underground Metro", "coords": [48.470, 35.015]},
        {"name": "Civilian Shelter - School 3", "coords": [48.462, 35.047]},
        {"name": "Warehouse Bunker", "coords": [48.469, 35.020]}
    ]

    # Recommend shelters near safest route
    nearby_shelters = find_shelters_near_route(safest["route"], shelter_db)

    for s in nearby_shelters:
        folium.Marker(
            location=s["coords"],
            icon=folium.Icon(color="green", icon="info-sign"),
            tooltip=f"Shelter: {s['name']}"
        ).add_to(m)

    # Safety advisories
    st.write("Safest route risk level:", safest["risk"])
    st_data = st_folium(m, width=1000, height=600)

    # Show extra recs (delays, alerts)
    extra_recs = get_safety_recommendations(start_coords, end_coords, threat_zones)
    for r in extra_recs:
        st.info(r)

else:
    st.warning("Unable to geocode one or both locations. Please check the inputs.")







