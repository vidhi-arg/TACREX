from shapely.geometry import LineString, Polygon

def evaluate_risk(route, threat_zones):
    route_line = LineString(route)
    for zone_coords in threat_zones:
        zone_poly = Polygon(zone_coords)
        if route_line.intersects(zone_poly):
            return "High Risk"
    return "Safe"

def evaluate_all_routes(routes, threat_zones):
    results = []
    for route in routes:
        risk = evaluate_risk(route, threat_zones)
        results.append({"route": route, "risk": risk})
    return results


