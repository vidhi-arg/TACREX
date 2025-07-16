import openrouteservice
from openrouteservice import convert

client = openrouteservice.Client(key="eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6ImQ5YjExY2JkMzI1NDRmMDlhYjU3OTc4NWZjOGY1MzBmIiwiaCI6Im11cm11cjY0In0=")  

def get_multiple_routes(start_coords, end_coords, count=3):
    try:
        routes = []
        params = {
            "coordinates": [start_coords, end_coords],
            "alternative_routes": {
                "target_count": count,
                "share_factor": 0.6,
                "weight_factor": 1.4
            }
        }
        response = client.directions(**params)
        for r in response["routes"]:
            decoded = convert.decode_polyline(r["geometry"])
            routes.append(decoded["coordinates"])
        return routes
    except Exception as e:
        print("Multi-route error:", e)
        return []


