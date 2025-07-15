import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import folium
from streamlit_folium import st_folium
from backend.route_engine import get_route
from backend.risk_evaluator import evaluate_route_risk
from backend.threat_ingestor import get_all_threats
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

# Set up page and geocoder
st.set_page_config(layout="wide")
st.title("TACREX: Tactical Escape Route Planner")
geolocator = Nominatim(user_agent="tacrex-geocoder")

# Input fields (city or lat,lon)
start_place = st.text_input("Start location (city, area, or coordinates)", "Khan Yunis, Gaza")
end_place = st.text_input("Destination location", "Rafah, Gaza")

# Function to geocode or parse coordinates
def resolve_location(loc_string):
    try:
        # If string matches "lat, lon" format, treat as coordinates
        parts = [x.strip() for x in loc_string.split(",")]
        if len(parts) == 2 and all(p.replace('.', '', 1).replace('-', '', 1).isdigit() for p in parts):
            lat, lon = [float(x) for x in parts]
            return [lat, lon]

        # Otherwise, use geopy to resolve place name
        location = geolocator.geocode(loc_string, timeout=10)
        if location:
            return [location.latitude, location.longitude]
        else:
            raise ValueError(f"Location '{loc_string}' not found.")

    except GeocoderTimedOut:
        raise ValueError("Geocoding service timed out. Try again.")
    except Exception as e:
        raise ValueError(f"Error resolving location '{loc_string}': {e}")


# Load threat zones from ACLED
threat_zones = get_all_threats()
st.write("Loaded threat zones:", len(threat_zones))  # Debug info

# Routing logic
try:
    # Convert user input to coordinates
    start_coords = resolve_location(start_place)
    end_coords = resolve_location(end_place)

    # Center map between start and end
    map_center = [(start_coords[0] + end_coords[0]) / 2, (start_coords[1] + end_coords[1]) / 2]
    m = folium.Map(location=map_center, zoom_start=12)

    # Draw all ACLED threat zones
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

    # Add markers for start and end
    folium.Marker(start_coords, tooltip="Start", icon=folium.Icon(color='green')).add_to(m)
    folium.Marker(end_coords, tooltip="End", icon=folium.Icon(color='red')).add_to(m)

    # Get route from OpenRouteService (requires [lon, lat])
    route = get_route(start_coords[::-1], end_coords[::-1])

    if route:
        coords = route["features"][0]["geometry"]["coordinates"]
        coords_latlon = [[c[1], c[0]] for c in coords]

        # Evaluate risk level
        risk, hits = evaluate_route_risk(coords_latlon, threat_zones)
        st.subheader(f"Route Risk Level: {risk}")

        if hits:
            with st.expander("Intersected Threat Zones"):
                for i, t in enumerate(hits, 1):
                    st.write(f"**{i}.** {t['description']} at ({t['lat']:.4f}, {t['lon']:.4f})")

        if risk == "High Risk":
            st.warning("This route intersects multiple active threat zones.")
            st.info("Consider adjusting your coordinates or waiting for safer conditions.")
        elif risk == "Borderline":
            st.warning("This route brushes near known threats. Stay cautious.")

        # Draw route on map
        color = "green" if risk == "Safe" else "orange" if risk == "Borderline" else "red"
        folium.PolyLine(locations=coords_latlon, color=color, weight=5).add_to(m)
    else:
        st.error("Could not fetch route from OpenRouteService.")

except Exception as e:
    st.warning("Routing or geocoding error occurred.")
    st.text(f"{e}")

# External conflict map
st.markdown(
    "[View live Gaza conflict map](https://israelpalestine.liveuamap.com/)",
    unsafe_allow_html=True
)

# Fallback map if previous block failed
if 'm' not in locals():
    m = folium.Map(location=[20, 0], zoom_start=2)

# Display map
st_data = st_folium(m, width=1000, height=600)





