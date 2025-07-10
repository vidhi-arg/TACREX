import openrouteservice
from openrouteservice import convert

client = openrouteservice.Client(key="eyJvcmciOiI1YjNjZTM1OTc4NTExMTAwMDFjZjYyNDgiLCJpZCI6ImQ5YjExY2JkMzI1NDRmMDlhYjU3OTc4NWZjOGY1MzBmIiwiaCI6Im11cm11cjY0In0=")  

def get_route(start_coords, end_coords):
    try:
        route = client.directions(
            coordinates=[start_coords, end_coords],
            profile='foot-walking', 
            format='geojson'
        )
        return route
    except Exception as e:
        print("Route error:", e)
        return None

