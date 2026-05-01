import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from geo.osm_client import query_osm as _query_osm, get_district_coords, get_location_radius
from geo.analysis import (
    calculate_distance as _calc_dist,
    find_nearest as _find_nearest,
    cluster_points as _cluster_points,
    get_statistics as _get_statistics,
)
from geo.visualize import generate_map as _generate_map


TOOL_DESCRIPTIONS = {
    "query_osm": {
        "name": "query_osm",
        "description": "OpenStreetMap Overpass API üzerinden belirli bir bölgedeki POI'leri sorgular.",
        "parameters": {
            "poi_type": "Aranacak yer tipi (hastane, eczane, park, okul, restoran, vb.)",
            "location": "İlçe/semt adı (Kadıköy, Beşiktaş, Taksim, vb.)",
            "radius": "Arama yarıçapı (metre, varsayılan: 3000)",
        },
    },
    "calculate_distance": {
        "name": "calculate_distance",
        "description": "İki nokta arasındaki Haversine mesafesini hesaplar.",
        "parameters": {
            "point_a": "(lat, lon) tuple - birinci nokta",
            "point_b": "(lat, lon) tuple - ikinci nokta",
        },
    },
    "find_nearest": {
        "name": "find_nearest",
        "description": "Belirli bir noktaya en yakın K adet POI'yi bulur.",
        "parameters": {
            "target_lat": "Hedef enlem",
            "target_lon": "Hedef boylam",
            "poi_type": "Aranacak yer tipi",
            "location": "Opsiyonel bölge adı",
            "k": "Kaç sonuç dönsün (varsayılan: 5)",
        },
    },
    "cluster_points": {
        "name": "cluster_points",
        "description": "POI'leri K-means kümeleme ile gruplandırır.",
        "parameters": {
            "poi_type": "Yer tipi",
            "location": "Opsiyonel bölge adı",
            "n_clusters": "Küme sayısı (varsayılan: 3)",
        },
    },
    "generate_map": {
        "name": "generate_map",
        "description": "Sonuçları interaktif Folium haritası olarak gösterir.",
        "parameters": {
            "geodataframe": "Haritada gösterilecek GeoDataFrame",
            "center": "Harita merkez koordinatları",
        },
    },
    "get_statistics": {
        "name": "get_statistics",
        "description": "GeoDataFrame hakkında temel istatistikleri döner.",
        "parameters": {
            "geodataframe": "İstatistik hesaplanacak GeoDataFrame",
        },
    },
}


def execute_tool(tool_name: str, params: dict) -> dict:
    try:
        if tool_name == "query_osm":
            return _execute_query_osm(params)
        elif tool_name == "calculate_distance":
            return _execute_calculate_distance(params)
        elif tool_name == "find_nearest":
            return _execute_find_nearest(params)
        elif tool_name == "cluster_points":
            return _execute_cluster_points(params)
        elif tool_name == "generate_map":
            return _execute_generate_map(params)
        elif tool_name == "get_statistics":
            return _execute_get_statistics(params)
        else:
            return {"error": f"Bilinmeyen tool: {tool_name}"}
    except Exception as e:
        return {"error": f"Tool çalıştırma hatası ({tool_name}): {str(e)}"}


def _execute_query_osm(params: dict) -> dict:
    poi_type = params.get("poi_type", "")
    location = params.get("location")
    raw_radius = params.get("radius")

    # Use smart radius: if user didn't specify, pick based on location type
    if raw_radius is not None:
        radius = int(raw_radius)
    else:
        radius = get_location_radius(location) if location else 3000

    gdf = _query_osm(poi_type, location, radius)

    center = None
    if location:
        coords = get_district_coords(location)
        if coords:
            center = coords

    folium_map = _generate_map(gdf, center=center, poi_type=poi_type, title=f"{location or 'İstanbul'} - {poi_type}")
    stats = _get_statistics(gdf)

    return {
        "success": True,
        "gdf": gdf,
        "map": folium_map,
        "stats": stats,
        "count": len(gdf),
        "poi_type": poi_type,
        "location": location,
    }


def _execute_calculate_distance(params: dict) -> dict:
    point_a = params.get("point_a")
    point_b = params.get("point_b")

    if isinstance(point_a, (list, tuple)) and isinstance(point_b, (list, tuple)):
        distance = _calc_dist(tuple(point_a), tuple(point_b))
        return {
            "success": True,
            "distance_m": round(distance, 1),
            "distance_km": round(distance / 1000, 2),
            "point_a": point_a,
            "point_b": point_b,
        }

    a_name = params.get("location_a", "")
    b_name = params.get("location_b", "")
    coords_a = get_district_coords(a_name) if a_name else None
    coords_b = get_district_coords(b_name) if b_name else None

    if coords_a and coords_b:
        lat_a, lon_a = coords_a[1], coords_a[0]
        lat_b, lon_b = coords_b[1], coords_b[0]
        distance = _calc_dist((lat_a, lon_a), (lat_b, lon_b))
        return {
            "success": True,
            "distance_m": round(distance, 1),
            "distance_km": round(distance / 1000, 2),
            "location_a": a_name,
            "location_b": b_name,
        }

    return {"error": "Geçerli koordinat veya bölge adı sağlanamadı."}


def _execute_find_nearest(params: dict) -> dict:
    target_lat = params.get("target_lat")
    target_lon = params.get("target_lon")
    poi_type = params.get("poi_type", "")
    location = params.get("location")
    k = int(params.get("k", 5))

    if target_lat is None or target_lon is None:
        loc_name = location or ""
        coords = get_district_coords(loc_name)
        if coords:
            target_lon, target_lat = coords
        else:
            return {"error": f"Hedef konum bulunamadı: {loc_name}"}

    search_location = location
    radius = max(5000, k * 1000)
    gdf = _query_osm(poi_type, search_location, radius)

    if gdf.empty:
        gdf = _query_osm(poi_type, search_location, radius * 2)

    if gdf.empty:
        return {
            "success": True,
            "gdf": gdf,
            "count": 0,
            "message": f"{location or 'İstanbul'} bölgesinde {poi_type} bulunamadı.",
        }

    nearest = _find_nearest(target_lat, target_lon, gdf, k)
    target_point = (target_lat, target_lon)
    center_coords = (target_lon, target_lat)
    folium_map = _generate_map(
        nearest,
        center=center_coords,
        poi_type=poi_type,
        target_point=target_point,
        title=f"En yakın {k} {poi_type} - {location or 'İstanbul'}",
    )
    stats = _get_statistics(nearest)

    return {
        "success": True,
        "gdf": nearest,
        "map": folium_map,
        "stats": stats,
        "count": len(nearest),
        "poi_type": poi_type,
        "location": location,
        "target": target_point,
    }


def _execute_cluster_points(params: dict) -> dict:
    poi_type = params.get("poi_type", "")
    location = params.get("location")
    n_clusters = int(params.get("n_clusters", 3))

    gdf = _query_osm(poi_type, location, 5000)

    if gdf.empty:
        return {
            "success": True,
            "gdf": gdf,
            "count": 0,
            "message": f"{location or 'İstanbul'} bölgesinde {poi_type} bulunamadı.",
        }

    actual_clusters = min(n_clusters, len(gdf))
    clustered = _cluster_points(gdf, actual_clusters)

    center = None
    if location:
        coords = get_district_coords(location)
        if coords:
            center = coords

    folium_map = _generate_map(
        clustered,
        center=center,
        poi_type=poi_type,
        use_clusters_visual=True,
        title=f"{poi_type} Kümeleme - {location or 'İstanbul'} ({actual_clusters} küme)",
    )
    stats = _get_statistics(clustered)

    return {
        "success": True,
        "gdf": clustered,
        "map": folium_map,
        "stats": stats,
        "count": len(clustered),
        "n_clusters": actual_clusters,
        "poi_type": poi_type,
        "location": location,
    }


def _execute_generate_map(params: dict) -> dict:
    return {"info": "Harita otomatik olarak diğer tool'lar tarafından oluşturulur."}


def _execute_get_statistics(params: dict) -> dict:
    poi_type = params.get("poi_type", "")
    location = params.get("location")

    gdf = _query_osm(poi_type, location, 5000)
    stats = _get_statistics(gdf)

    return {
        "success": True,
        "stats": stats,
        "poi_type": poi_type,
        "location": location,
    }
