import requests
import geopandas as gpd
from shapely.geometry import Point
import pandas as pd
import time
import hashlib
import json
import os

CACHE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "cache")
OVERPASS_URLS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
]
OVERPASS_URL = OVERPASS_URLS[0]

ISTANBUL_BBOX = (28.5, 40.8, 29.5, 41.3)

DISTRICT_COORDS = {
    "kadikoy": (29.0259, 40.9927),
    "kadıköy": (29.0259, 40.9927),
    "besiktas": (29.0044, 41.0422),
    "beşiktaş": (29.0044, 41.0422),
    "taksim": (28.9869, 41.0370),
    "sultanahmet": (28.9784, 41.0054),
    "uskudar": (29.0153, 41.0234),
    "üsküdar": (29.0153, 41.0234),
    "fatih": (28.9494, 41.0186),
    "beyoglu": (28.9744, 41.0370),
    "beyoğlu": (28.9744, 41.0370),
    "sisli": (28.9872, 41.0602),
    "şişli": (28.9872, 41.0602),
    "bakirkoy": (28.8772, 40.9808),
    "bakırköy": (28.8772, 40.9808),
    "sariyer": (29.0500, 41.1667),
    "sarıyer": (29.0500, 41.1667),
    "eminonu": (28.9700, 41.0167),
    "eminönü": (28.9700, 41.0167),
    "maltepe": (29.1300, 40.9333),
    "kartal": (29.1900, 40.8900),
    "pendik": (29.2333, 40.8750),
    "atasehir": (29.1167, 40.9833),
    "ataşehir": (29.1167, 40.9833),
    "umraniye": (29.1167, 41.0167),
    "ümraniye": (29.1167, 41.0167),
    "eyup": (28.9333, 41.0500),
    "eyüp": (28.9333, 41.0500),
    "beylikduzu": (28.6333, 41.0000),
    "beylikdüzü": (28.6333, 41.0000),
    "esenyurt": (28.6667, 41.0333),
    "avcilar": (28.7167, 40.9833),
    "avcılar": (28.7167, 40.9833),
    "bagcilar": (28.8500, 41.0333),
    "bağcılar": (28.8500, 41.0333),
    "bahcelievler": (28.8500, 41.0000),
    "bahçelievler": (28.8500, 41.0000),
    "cengelkoy": (29.0500, 41.0500),
    "çengelköy": (29.0500, 41.0500),
    "ortakoy": (29.0267, 41.0486),
    "ortaköy": (29.0267, 41.0486),
    "karakoy": (28.9753, 41.0214),
    "karaköy": (28.9753, 41.0214),
    "galata": (28.9739, 41.0256),
    "istanbul": (28.9784, 41.0082),
}

POI_TAG_MAP = {
    "hastane": {"amenity": "hospital"},
    "hospital": {"amenity": "hospital"},
    "eczane": {"amenity": "pharmacy"},
    "pharmacy": {"amenity": "pharmacy"},
    "park": {"leisure": "park"},
    "okul": {"amenity": "school"},
    "school": {"amenity": "school"},
    "universite": {"amenity": "university"},
    "üniversite": {"amenity": "university"},
    "university": {"amenity": "university"},
    "restoran": {"amenity": "restaurant"},
    "restaurant": {"amenity": "restaurant"},
    "kafe": {"amenity": "cafe"},
    "cafe": {"amenity": "cafe"},
    "cami": {"amenity": "place_of_worship", "religion": "muslim"},
    "mosque": {"amenity": "place_of_worship", "religion": "muslim"},
    "kilise": {"amenity": "place_of_worship", "religion": "christian"},
    "church": {"amenity": "place_of_worship", "religion": "christian"},
    "market": {"shop": "supermarket"},
    "supermarket": {"shop": "supermarket"},
    "banka": {"amenity": "bank"},
    "bank": {"amenity": "bank"},
    "atm": {"amenity": "atm"},
    "benzin": {"amenity": "fuel"},
    "fuel": {"amenity": "fuel"},
    "otopark": {"amenity": "parking"},
    "parking": {"amenity": "parking"},
    "kutuphane": {"amenity": "library"},
    "kütüphane": {"amenity": "library"},
    "library": {"amenity": "library"},
    "muze": {"tourism": "museum"},
    "müze": {"tourism": "museum"},
    "museum": {"tourism": "museum"},
    "otel": {"tourism": "hotel"},
    "hotel": {"tourism": "hotel"},
    "metro": {"station": "subway"},
    "durak": {"public_transport": "stop_position"},
    "otobus": {"highway": "bus_stop"},
    "otobüs": {"highway": "bus_stop"},
    "bus_stop": {"highway": "bus_stop"},
}


def _cache_key(query: str) -> str:
    return hashlib.md5(query.encode()).hexdigest()


def _get_cached(query: str):
    os.makedirs(CACHE_DIR, exist_ok=True)
    path = os.path.join(CACHE_DIR, f"{_cache_key(query)}.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return None


def _set_cache(query: str, data):
    os.makedirs(CACHE_DIR, exist_ok=True)
    path = os.path.join(CACHE_DIR, f"{_cache_key(query)}.json")
    with open(path, "w") as f:
        json.dump(data, f)


def get_district_coords(name: str):
    key = name.lower().strip()
    return DISTRICT_COORDS.get(key)


def get_poi_tags(poi_type: str):
    key = poi_type.lower().strip()
    return POI_TAG_MAP.get(key)


def build_overpass_query(poi_tags: dict, bbox=None, around_center=None, around_radius=3000) -> str:
    if around_center:
        lat, lon = around_center[1], around_center[0]
        filters = "".join(f'["{k}"="{v}"]' for k, v in poi_tags.items())
        return f"""[out:json][timeout:60];
(
  node{filters}(around:{around_radius},{lat},{lon});
  way{filters}(around:{around_radius},{lat},{lon});
  relation{filters}(around:{around_radius},{lat},{lon});
);
out center body;"""

    if bbox is None:
        bbox = ISTANBUL_BBOX

    s, w, n, e = bbox[1], bbox[0], bbox[3], bbox[2]
    filters = "".join(f'["{k}"="{v}"]' for k, v in poi_tags.items())
    return f"""[out:json][timeout:60];
(
  node{filters}({s},{w},{n},{e});
  way{filters}({s},{w},{n},{e});
  relation{filters}({s},{w},{n},{e});
);
out center body;"""


def query_overpass(overpass_query: str) -> list:
    cached = _get_cached(overpass_query)
    if cached is not None:
        return cached

    last_err = None
    for url in OVERPASS_URLS:
        try:
            resp = requests.post(url, data={"data": overpass_query}, timeout=90)
            resp.raise_for_status()
            elements = resp.json().get("elements", [])
            _set_cache(overpass_query, elements)
            return elements
        except Exception as e:
            last_err = e
            time.sleep(1)
            continue

    raise last_err


def elements_to_geodataframe(elements: list) -> gpd.GeoDataFrame:
    rows = []
    for el in elements:
        lat = el.get("lat") or (el.get("center", {}).get("lat"))
        lon = el.get("lon") or (el.get("center", {}).get("lon"))
        if lat is None or lon is None:
            continue
        tags = el.get("tags", {})
        name = tags.get("name", tags.get("name:tr", tags.get("name:en", "Bilinmeyen")))
        rows.append({
            "name": name,
            "lat": lat,
            "lon": lon,
            "osm_id": el.get("id"),
            "osm_type": el.get("type"),
            "geometry": Point(lon, lat),
            **{k: v for k, v in tags.items() if k not in ("name", "name:tr", "name:en")},
        })

    if not rows:
        return gpd.GeoDataFrame(columns=["name", "lat", "lon", "geometry"], geometry="geometry", crs="EPSG:4326")

    gdf = gpd.GeoDataFrame(rows, geometry="geometry", crs="EPSG:4326")
    return gdf


def query_osm(poi_type: str, location: str = None, radius: int = 3000) -> gpd.GeoDataFrame:
    poi_tags = get_poi_tags(poi_type)
    if poi_tags is None:
        poi_tags = {"name": poi_type}

    around_center = None
    if location:
        coords = get_district_coords(location)
        if coords:
            around_center = coords

    overpass_q = build_overpass_query(poi_tags, around_center=around_center, around_radius=radius)

    try:
        elements = query_overpass(overpass_q)
    except Exception:
        try:
            from data.sample_data import get_sample_elements
            elements = get_sample_elements(poi_type, location)
        except Exception:
            elements = []

    gdf = elements_to_geodataframe(elements)
    return gdf
