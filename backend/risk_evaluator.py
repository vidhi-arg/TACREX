from geopy.distance import geodesic

def evaluate_route_risk(route_coords, threat_zones):
    danger_hits = 0

    for point in route_coords:
        for threat in threat_zones:
            threat_center = (threat["lat"], threat["lon"])
            distance = geodesic(point, threat_center).meters

            if distance < threat["radius"]:
                danger_hits += 1

    if danger_hits == 0:
        return " Safe"
    elif danger_hits <= 3:
        return " Borderline"
    else:
        return " Unsafe"

