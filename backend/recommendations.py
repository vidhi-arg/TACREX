from geopy.distance import geodesic

def get_safety_recommendations(start, end, threat_zones):
    recs = []
    if threat_zones:
        recs.append("Delay departure by 1–2 hours. Conflict activity detected near route.")
    if geodesic(start, end).km > 50:
        recs.append("Long-distance route. Consider rest points or shelters along the way.")
    return recs

def find_shelters_near_route(route_coords, all_shelters, max_dist_km=5):
    safe_shelters = []
    for shelter in all_shelters:
        for point in route_coords:
            if geodesic(point, shelter["coords"]).km < max_dist_km:
                safe_shelters.append(shelter)
                break
    return safe_shelters
