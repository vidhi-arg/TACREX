import streamlit as st
from streamlit_folium import st_folium
import folium
from geopy.geocoders import Nominatim

from backend.route_engine import get_route
from backend.risk_evaluator import evaluate_risk
from backend.threat_feed import get_all_threats
from backend.twitter_feed import get_live_threats
from backend.recommendations import get_safety_recommendations

st.set_page_config(layout="wide")
st.title("TACREX - Tactical Conflict Routing Engine")

# Geocoding input locations
geolocator = Nominatim(user_agent="tacrex-app")

def geocode_location(place):
    try:
        location = geolocator.geocode(place)
        if location:
            return (location.latitude, location.longitude)
    except:
        pass
    return None

# User inputs
start_place = st.text_input("Start Location", "Zaporizhzhia, Ukraine")
end_place = st.text_input("End Location", "Dnipro, Ukraine")

start_coords = geocode_location(start_place)
end_coords = geocode_location(end_place)

# Only run logic if geocoding successful
if start_coords and end_coords:
    # Fetch route
    route = get_route(start_coords[::-1], end_coords[::-1])

    # Load threat zones (Phase 3)
    threat_zones = get_all_threats()

    # Evaluate risk (Phase 2)
    risk = evaluate_risk(route, threat_zones)

    # Initialize map
    m = folium.Map(location=start_coords, zoom_start=9)

    # Draw route (Phase 1)
    if route:
        folium.PolyLine(route, color="blue", weight=4.5, opacity=0.9).add_to(m)

    # Draw static polygon threat zones
    for zone in threat_zones:
        folium.Polygon(locations=zone, color="red", fill=True, fill_opacity=0.4).add_to(m)

    # Add real-time threats (Phase 5)
    live_threats = get_live_threats()
    for threat in live_threats:
        folium.Circle(
            radius=300,
            location=threat["location"],
            color="orange",
            fill=True,
            fill_opacity=0.5,
            tooltip=threat["type"] + ": " + threat["description"]
        ).add_to(m)

    # Show map
    st.write("**Risk Level:**", risk)
    st_data = st_folium(m, width=1000, height=600)

    # Safety advice (Phase 6)
    recommendations = get_safety_recommendations(start_coords, end_coords, threat_zones)
    for r in recommendations:
        st.info(r)

else:
    st.warning("Unable to geocode one or both locations. Please check the inputs.")






