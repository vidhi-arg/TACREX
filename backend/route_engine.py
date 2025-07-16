import openrouteservice
from openrouteservice import convert

client = openrouteservice.Client(key="YOUR_ORS_API_KEY")

def get_multiple_routes(start_coords, end_coords, count=3):
    try:
        params = {
            "coordinates": [start_coords, end_coords],
            "alternative_routes": {
                "target_count": count,
                "share_factor": 0.6,
                "weight_factor": 1.4
            },
            "profile": "driving-car",
            "format_out": "geojson",
            "instructions": False
        }
        response = client.directions(**params)
        routes = []
        for r in response["routes"]:
            decoded = convert.decode_polyline(r["geometry"])
            routes.append(decoded["coordinates"])
        return routes
    except Exception as e:
        print("Multi-route error:", e)
        return []

