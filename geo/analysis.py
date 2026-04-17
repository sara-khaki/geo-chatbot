import numpy as np
import geopandas as gpd
from shapely.geometry import Point
from sklearn.cluster import KMeans
import pandas as pd
from math import radians, sin, cos, sqrt, atan2


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371000
    phi1, phi2 = radians(lat1), radians(lat2)
    dphi = radians(lat2 - lat1)
    dlam = radians(lon2 - lon1)
    a = sin(dphi / 2) ** 2 + cos(phi1) * cos(phi2) * sin(dlam / 2) ** 2
    return R * 2 * atan2(sqrt(a), sqrt(1 - a))


def calculate_distance(point_a: tuple, point_b: tuple) -> float:
    return haversine_distance(point_a[0], point_a[1], point_b[0], point_b[1])


def find_nearest(target_lat: float, target_lon: float, gdf: gpd.GeoDataFrame, k: int = 5) -> gpd.GeoDataFrame:
    if gdf.empty:
        return gdf

    gdf = gdf.copy()
    gdf["distance_m"] = gdf.apply(
        lambda row: haversine_distance(target_lat, target_lon, row["lat"], row["lon"]),
        axis=1,
    )
    gdf = gdf.sort_values("distance_m").head(k).reset_index(drop=True)
    gdf["distance_km"] = (gdf["distance_m"] / 1000).round(2)
    return gdf


def cluster_points(gdf: gpd.GeoDataFrame, n_clusters: int = 3) -> gpd.GeoDataFrame:
    if gdf.empty or len(gdf) < n_clusters:
        gdf = gdf.copy()
        gdf["cluster"] = 0
        return gdf

    coords = gdf[["lat", "lon"]].values
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    gdf = gdf.copy()
    gdf["cluster"] = kmeans.fit_predict(coords)
    return gdf


def get_statistics(gdf: gpd.GeoDataFrame) -> dict:
    if gdf.empty:
        return {"count": 0, "message": "Veri bulunamadı."}

    stats = {
        "count": len(gdf),
        "center_lat": round(gdf["lat"].mean(), 6),
        "center_lon": round(gdf["lon"].mean(), 6),
        "lat_range": (round(gdf["lat"].min(), 6), round(gdf["lat"].max(), 6)),
        "lon_range": (round(gdf["lon"].min(), 6), round(gdf["lon"].max(), 6)),
    }

    if "distance_m" in gdf.columns:
        stats["min_distance_m"] = round(gdf["distance_m"].min(), 1)
        stats["max_distance_m"] = round(gdf["distance_m"].max(), 1)
        stats["avg_distance_m"] = round(gdf["distance_m"].mean(), 1)

    if "cluster" in gdf.columns:
        stats["n_clusters"] = gdf["cluster"].nunique()
        stats["cluster_sizes"] = gdf["cluster"].value_counts().to_dict()

    return stats


def get_bounding_box(gdf: gpd.GeoDataFrame):
    if gdf.empty:
        return None
    bounds = gdf.total_bounds
    return (bounds[0], bounds[1], bounds[2], bounds[3])
