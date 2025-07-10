import pandas as pd

def get_threats_from_acled(filepath="data/acled.csv"):
    df = pd.read_csv(filepath)
    zones = []

    for _, row in df.iterrows():
        try:
            zones.append({
                "lat": float(row["latitude"]),
                "lon": float(row["longitude"]),
                "radius": 300,
                "description": f'{row["event_type"]}: {row.get("notes", "")[:80]}...'
            })
        except:
            continue

    return zones

def get_all_threats():
    return get_threats_from_acled()

