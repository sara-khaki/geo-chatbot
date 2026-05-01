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

# Turkish character normalization map (Turkish → ASCII)
_TR_CHAR_MAP = str.maketrans(
    "çğıöşüÇĞİÖŞÜ",
    "cgiosuCGIOSU",
)


def _normalize_turkish(text: str) -> str:
    return text.translate(_TR_CHAR_MAP).lower().strip()


# ---------- District-level locations (ilçe / büyük semt) ----------
# Stored as (lon, lat) tuples
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

# ---------- Neighborhood-level locations (mahalle / semt) ----------
# These are smaller areas; default search radius should be smaller (1500m)
NEIGHBORHOOD_COORDS = {
    # Kadıköy neighborhoods
    "suadiye": (29.0730, 40.9625),
    "moda": (29.0250, 40.9860),
    "fenerbahce": (29.0370, 40.9720),
    "fenerbahçe": (29.0370, 40.9720),
    "bostanci": (29.0920, 40.9570),
    "bostancı": (29.0920, 40.9570),
    "goztepe": (29.0570, 40.9800),
    "göztepe": (29.0570, 40.9800),
    "caddebostan": (29.0650, 40.9640),
    "kozyatagi": (29.0950, 40.9750),
    "kozyatağı": (29.0950, 40.9750),
    "erenkoy": (29.0730, 40.9730),
    "erenköy": (29.0730, 40.9730),
    "acibadem": (29.0450, 40.9920),
    "acıbadem": (29.0450, 40.9920),
    "kalamis": (29.0310, 40.9780),
    "kalamış": (29.0310, 40.9780),
    "fikirtepe": (29.0400, 40.9900),
    "yeldeğirmeni": (29.0230, 40.9910),
    "yeldegirmeni": (29.0230, 40.9910),
    "rasimpasa": (29.0230, 40.9910),
    "rasimpaşa": (29.0230, 40.9910),
    "caferaga": (29.0260, 40.9890),
    "caferağa": (29.0260, 40.9890),
    "osmanaga": (29.0280, 40.9900),
    "osmanağa": (29.0280, 40.9900),
    # Beşiktaş neighborhoods
    "bebek": (29.0440, 41.0770),
    "arnavutkoy": (29.0340, 41.0690),
    "arnavutköy": (29.0340, 41.0690),
    "kurucesme": (29.0350, 41.0600),
    "kuruçeşme": (29.0350, 41.0600),
    "etiler": (29.0300, 41.0800),
    "levent": (29.0130, 41.0820),
    "ulus": (29.0220, 41.0790),
    "akatlar": (29.0150, 41.0750),
    "dikilitas": (29.0100, 41.0550),
    "dikilitaş": (29.0100, 41.0550),
    # Şişli neighborhoods
    "nisantasi": (28.9920, 41.0500),
    "nişantaşı": (28.9920, 41.0500),
    "mecidiyekoy": (28.9950, 41.0660),
    "mecidiyeköy": (28.9950, 41.0660),
    "maslak": (29.0200, 41.1100),
    "bomonti": (28.9830, 41.0550),
    "fulya": (29.0050, 41.0580),
    "tesvikiye": (28.9960, 41.0470),
    "teşvikiye": (28.9960, 41.0470),
    # Beyoğlu neighborhoods
    "cihangir": (28.9830, 41.0330),
    "asmalimescit": (28.9760, 41.0320),
    "asmalımescit": (28.9760, 41.0320),
    "istiklal": (28.9800, 41.0340),
    # Fatih neighborhoods
    "balat": (28.9480, 41.0290),
    "fener": (28.9510, 41.0280),
    "cibali": (28.9560, 41.0250),
    "kumkapi": (28.9640, 41.0030),
    "kumkapı": (28.9640, 41.0030),
    "aksaray": (28.9510, 41.0120),
    "laleli": (28.9560, 41.0110),
    "beyazit": (28.9640, 41.0100),
    "beyazıt": (28.9640, 41.0100),
    "sirkeci": (28.9770, 41.0140),
    "cagaloglu": (28.9700, 41.0100),
    "cağaloğlu": (28.9700, 41.0100),
    # Bakırköy neighborhoods
    "florya": (28.7900, 40.9780),
    "yesilkoy": (28.8200, 40.9700),
    "yeşilköy": (28.8200, 40.9700),
    "atakoy": (28.8560, 40.9750),
    "ataköy": (28.8560, 40.9750),
    # Üsküdar neighborhoods
    "kuzguncuk": (29.0300, 41.0300),
    "beylerbeyi": (29.0400, 41.0420),
    "kandilli": (29.0600, 41.0700),
    "cengelkoy": (29.0530, 41.0470),
    "vanıköy": (29.0550, 41.0550),
    "vanikoy": (29.0550, 41.0550),
    # Sarıyer neighborhoods
    "istinye": (29.0600, 41.1100),
    "tarabya": (29.0500, 41.1250),
    "emirgan": (29.0500, 41.1070),
    "rumelihisari": (29.0570, 41.0860),
    "rumelihisarı": (29.0570, 41.0860),
    # Other notable locations
    "bagdat caddesi": (29.0650, 40.9640),
    "bağdat caddesi": (29.0650, 40.9640),
    "kadikoy carsi": (29.0240, 40.9900),
    "kadıköy çarşı": (29.0240, 40.9900),
    "haydarpasa": (29.0180, 40.9970),
    "haydarpaşa": (29.0180, 40.9970),
    "marmara adaları": (29.1200, 40.8700),
    "buyukada": (29.1200, 40.8680),
    "büyükada": (29.1200, 40.8680),
    "heybeliada": (29.0900, 40.8750),
    "burgazada": (29.0630, 40.8780),
    "kinalıada": (29.0500, 40.8900),
    "kinaliada": (29.0500, 40.8900),
}

# Merge both dicts for unified lookup; neighborhoods override duplicates
_ALL_LOCATIONS = {**DISTRICT_COORDS, **NEIGHBORHOOD_COORDS}

# Locations that are neighborhoods (smaller areas) — use 1500m radius
_NEIGHBORHOOD_NAMES = set(NEIGHBORHOOD_COORDS.keys())

# Default radii
DISTRICT_RADIUS = 3000
NEIGHBORHOOD_RADIUS = 1500

# Nominatim geocoding cache (in-memory for session)
_geocode_cache = {}

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


def _geocode_nominatim(name: str):
    """Geocode a location name within Istanbul using Nominatim as a fallback.
    Returns (lon, lat) tuple or None."""
    cache_key = _normalize_turkish(name)
    if cache_key in _geocode_cache:
        return _geocode_cache[cache_key]

    try:
        resp = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={
                "q": f"{name}, Istanbul, Turkey",
                "format": "json",
                "limit": 1,
                "viewbox": "28.5,41.3,29.5,40.8",
                "bounded": 1,
            },
            headers={"User-Agent": "GeoAI-ChatBot/1.0 (student-project)"},
            timeout=10,
        )
        resp.raise_for_status()
        results = resp.json()
        if results:
            lon = float(results[0]["lon"])
            lat = float(results[0]["lat"])
            _geocode_cache[cache_key] = (lon, lat)
            return (lon, lat)
    except Exception:
        pass

    _geocode_cache[cache_key] = None
    return None


def get_district_coords(name: str):
    """Resolve a location name to (lon, lat) coordinates.

    Strategy:
    1. Exact match in combined locations dict (districts + neighborhoods)
    2. Normalized (ASCII) match — handles missing Turkish chars
    3. Nominatim geocoding fallback — handles any Istanbul location
    """
    if not name:
        return None

    key = name.lower().strip()

    # 1. Exact match
    coords = _ALL_LOCATIONS.get(key)
    if coords:
        return coords

    # 2. Normalized match (strip Turkish diacritics and compare)
    normalized_key = _normalize_turkish(key)
    for loc_name, loc_coords in _ALL_LOCATIONS.items():
        if _normalize_turkish(loc_name) == normalized_key:
            return loc_coords

    # 3. Nominatim geocoding fallback
    coords = _geocode_nominatim(name)
    if coords:
        return coords

    return None


def get_location_radius(name: str) -> int:
    """Return the appropriate search radius for a location.
    Neighborhoods get a smaller radius (1500m), districts get 3000m."""
    if not name:
        return DISTRICT_RADIUS

    key = name.lower().strip()
    normalized = _normalize_turkish(key)

    # Check if it's a known neighborhood
    for nb_name in _NEIGHBORHOOD_NAMES:
        if key == nb_name or _normalize_turkish(nb_name) == normalized:
            return NEIGHBORHOOD_RADIUS

    # If found via Nominatim (not in our dicts), use neighborhood radius
    # since specific place names tend to be small areas
    if key not in DISTRICT_COORDS and _normalize_turkish(key) not in {
        _normalize_turkish(k) for k in DISTRICT_COORDS
    }:
        return NEIGHBORHOOD_RADIUS

    return DISTRICT_RADIUS


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


def query_osm(poi_type: str, location: str = None, radius: int = None) -> gpd.GeoDataFrame:
    poi_tags = get_poi_tags(poi_type)
    if poi_tags is None:
        poi_tags = {"name": poi_type}

    around_center = None
    if location:
        coords = get_district_coords(location)
        if coords:
            around_center = coords

    # Use smart radius if not explicitly specified
    if radius is None:
        radius = get_location_radius(location) if location else DISTRICT_RADIUS

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
