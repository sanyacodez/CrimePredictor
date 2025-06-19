import geopandas as gpd
import pandas as pd
from shapely.geometry import Point, LineString
import openrouteservice

# Load data and initialize once
crime_df = pd.read_excel("New_Delhi_crime.xlsx")
geometry = [Point(xy) for xy in zip(crime_df["Longitude"], crime_df["Latitude"])]
crime_gdf = gpd.GeoDataFrame(crime_df, geometry=geometry)
crime_gdf.set_crs(epsg=4326, inplace=True)

client = openrouteservice.Client(key="5b3ce3597851110001cf624845dbab0f44a54258a117be0a0a56ec75")  # Replace with your actual key

def compute_risk(route_geojson):
    coords = route_geojson['features'][0]['geometry']['coordinates']
    total_risk = 0
    for i in range(len(coords) - 1):
        segment = LineString([coords[i], coords[i + 1]])
        buffer = segment.buffer(0.0005)  # ~50 meters
        crimes_nearby = crime_gdf[crime_gdf.geometry.within(buffer)]
        total_risk += len(crimes_nearby)
    return total_risk

def get_safest_route(start_coords, end_coords):
    route_geojson = client.directions(
        coordinates=[start_coords, end_coords],
        profile='foot-walking',
        format='geojson'
    )
    risk_score = compute_risk(route_geojson)
    return {
        "geojson": route_geojson,
        "risk": risk_score
    }
