from geopy.distance import geodesic

def evaluate_route_risk(route_coords, threat_zones):
    hits = []
    for point in route_coords:
        for threat in threat_zones:
            dist = geodesic(point, [threat["lat"], threat["lon"]]).meters
            if dist < threat["radius"]:
                hits.append(threat)

    if len(hits) == 0:
        return "Safe", []
    elif len(hits) <= 2:
        return "Borderline", hits
    else:
        return "High Risk", hits

