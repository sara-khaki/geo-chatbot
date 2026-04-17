"""
Realistic sample POI data for Istanbul, used as fallback when the Overpass API
is unavailable.  Every entry mirrors the Overpass "element" schema so it can be
fed directly into ``elements_to_geodataframe()``.

Usage
-----
    from data.sample_data import get_sample_elements
    elements = get_sample_elements("hastane", "kadıköy")
"""

from __future__ import annotations

import random
from typing import List, Dict, Any, Optional, Tuple


# ---------------------------------------------------------------------------
# Raw POI data keyed by (poi_type, location).
# Each value is a list of dicts with: name, lat, lon, tags.
# ---------------------------------------------------------------------------

SAMPLE_DATA: Dict[Tuple[str, str], List[Dict[str, Any]]] = {

    # ------------------------------------------------------------------
    # HASTANE (hospitals) -- Kadikoy
    # ------------------------------------------------------------------
    ("hastane", "kadıköy"): [
        {
            "name": "Kadıköy Şifa Hastanesi",
            "lat": 40.9905,
            "lon": 29.0230,
            "tags": {"amenity": "hospital", "name": "Kadıköy Şifa Hastanesi", "healthcare": "hospital", "addr:district": "Kadıköy"},
        },
        {
            "name": "Göztepe Prof. Dr. Süleyman Yalçın Şehir Hastanesi",
            "lat": 40.9787,
            "lon": 29.0525,
            "tags": {"amenity": "hospital", "name": "Göztepe Prof. Dr. Süleyman Yalçın Şehir Hastanesi", "healthcare": "hospital", "operator": "Sağlık Bakanlığı"},
        },
        {
            "name": "Medicana Kadıköy Hastanesi",
            "lat": 40.9882,
            "lon": 29.0335,
            "tags": {"amenity": "hospital", "name": "Medicana Kadıköy Hastanesi", "healthcare": "hospital", "operator": "Medicana"},
        },
        {
            "name": "Medical Park Göztepe Hastanesi",
            "lat": 40.9812,
            "lon": 29.0498,
            "tags": {"amenity": "hospital", "name": "Medical Park Göztepe Hastanesi", "healthcare": "hospital", "operator": "Medical Park"},
        },
        {
            "name": "Acıbadem Kadıköy Hastanesi",
            "lat": 40.9920,
            "lon": 29.0310,
            "tags": {"amenity": "hospital", "name": "Acıbadem Kadıköy Hastanesi", "healthcare": "hospital", "operator": "Acıbadem"},
        },
        {
            "name": "Haydarpaşa Numune Eğitim ve Araştırma Hastanesi",
            "lat": 41.0045,
            "lon": 29.0175,
            "tags": {"amenity": "hospital", "name": "Haydarpaşa Numune Eğitim ve Araştırma Hastanesi", "healthcare": "hospital", "operator": "Sağlık Bakanlığı"},
        },
        {
            "name": "Koşuyolu Yüksek İhtisas Eğitim ve Araştırma Hastanesi",
            "lat": 40.9955,
            "lon": 29.0380,
            "tags": {"amenity": "hospital", "name": "Koşuyolu Yüksek İhtisas Eğitim ve Araştırma Hastanesi", "healthcare": "hospital", "operator": "Sağlık Bakanlığı"},
        },
        {
            "name": "Florence Nightingale Hastanesi Kadıköy",
            "lat": 40.9870,
            "lon": 29.0275,
            "tags": {"amenity": "hospital", "name": "Florence Nightingale Hastanesi Kadıköy", "healthcare": "hospital"},
        },
    ],

    # ------------------------------------------------------------------
    # ECZANE (pharmacies) -- Taksim
    # ------------------------------------------------------------------
    ("eczane", "taksim"): [
        {
            "name": "Taksim Eczanesi",
            "lat": 41.0370,
            "lon": 28.9853,
            "tags": {"amenity": "pharmacy", "name": "Taksim Eczanesi", "dispensing": "yes"},
        },
        {
            "name": "İstiklal Eczanesi",
            "lat": 41.0340,
            "lon": 28.9780,
            "tags": {"amenity": "pharmacy", "name": "İstiklal Eczanesi", "dispensing": "yes"},
        },
        {
            "name": "Gümüşsuyu Eczanesi",
            "lat": 41.0365,
            "lon": 28.9900,
            "tags": {"amenity": "pharmacy", "name": "Gümüşsuyu Eczanesi", "dispensing": "yes"},
        },
        {
            "name": "Sıraselviler Eczanesi",
            "lat": 41.0355,
            "lon": 28.9830,
            "tags": {"amenity": "pharmacy", "name": "Sıraselviler Eczanesi", "dispensing": "yes"},
        },
        {
            "name": "Cihangir Eczanesi",
            "lat": 41.0320,
            "lon": 28.9820,
            "tags": {"amenity": "pharmacy", "name": "Cihangir Eczanesi", "dispensing": "yes"},
        },
        {
            "name": "Ayhan Eczanesi",
            "lat": 41.0378,
            "lon": 28.9870,
            "tags": {"amenity": "pharmacy", "name": "Ayhan Eczanesi", "dispensing": "yes"},
        },
        {
            "name": "Küçükparmakkapı Eczanesi",
            "lat": 41.0348,
            "lon": 28.9795,
            "tags": {"amenity": "pharmacy", "name": "Küçükparmakkapı Eczanesi", "dispensing": "yes"},
        },
        {
            "name": "Tarlabaşı Eczanesi",
            "lat": 41.0388,
            "lon": 28.9810,
            "tags": {"amenity": "pharmacy", "name": "Tarlabaşı Eczanesi", "dispensing": "yes"},
        },
        {
            "name": "Mete Eczanesi",
            "lat": 41.0372,
            "lon": 28.9842,
            "tags": {"amenity": "pharmacy", "name": "Mete Eczanesi", "dispensing": "yes"},
        },
        {
            "name": "Talimhane Eczanesi",
            "lat": 41.0390,
            "lon": 28.9865,
            "tags": {"amenity": "pharmacy", "name": "Talimhane Eczanesi", "dispensing": "yes"},
        },
    ],

    # ------------------------------------------------------------------
    # PARK -- Besiktas
    # ------------------------------------------------------------------
    ("park", "beşiktaş"): [
        {
            "name": "Yıldız Parkı",
            "lat": 41.0490,
            "lon": 29.0140,
            "tags": {"leisure": "park", "name": "Yıldız Parkı", "access": "yes"},
        },
        {
            "name": "Beşiktaş Barbaros Parkı",
            "lat": 41.0430,
            "lon": 29.0010,
            "tags": {"leisure": "park", "name": "Beşiktaş Barbaros Parkı", "access": "yes"},
        },
        {
            "name": "Ihlamur Kasrı Parkı",
            "lat": 41.0450,
            "lon": 28.9950,
            "tags": {"leisure": "park", "name": "Ihlamur Kasrı Parkı", "access": "yes"},
        },
        {
            "name": "Abbasağa Parkı",
            "lat": 41.0440,
            "lon": 29.0050,
            "tags": {"leisure": "park", "name": "Abbasağa Parkı", "access": "yes"},
        },
        {
            "name": "Ortaköy Dereboyu Parkı",
            "lat": 41.0480,
            "lon": 29.0260,
            "tags": {"leisure": "park", "name": "Ortaköy Dereboyu Parkı", "access": "yes"},
        },
        {
            "name": "Kuruçeşme Parkı",
            "lat": 41.0510,
            "lon": 29.0310,
            "tags": {"leisure": "park", "name": "Kuruçeşme Parkı", "access": "yes"},
        },
        {
            "name": "Bebek Parkı",
            "lat": 41.0740,
            "lon": 29.0430,
            "tags": {"leisure": "park", "name": "Bebek Parkı", "access": "yes"},
        },
        {
            "name": "Serencebey Parkı",
            "lat": 41.0460,
            "lon": 29.0080,
            "tags": {"leisure": "park", "name": "Serencebey Parkı", "access": "yes"},
        },
    ],

    # ------------------------------------------------------------------
    # CAMİ (mosques) -- Fatih
    # ------------------------------------------------------------------
    ("cami", "fatih"): [
        {
            "name": "Fatih Camii",
            "lat": 41.0197,
            "lon": 28.9500,
            "tags": {"amenity": "place_of_worship", "religion": "muslim", "name": "Fatih Camii", "building": "mosque"},
        },
        {
            "name": "Süleymaniye Camii",
            "lat": 41.0162,
            "lon": 28.9640,
            "tags": {"amenity": "place_of_worship", "religion": "muslim", "name": "Süleymaniye Camii", "building": "mosque", "historic": "yes"},
        },
        {
            "name": "Sultan Selim Camii (Yavuz Selim Camii)",
            "lat": 41.0250,
            "lon": 28.9530,
            "tags": {"amenity": "place_of_worship", "religion": "muslim", "name": "Sultan Selim Camii", "alt_name": "Yavuz Selim Camii", "building": "mosque"},
        },
        {
            "name": "Şehzade Camii",
            "lat": 41.0125,
            "lon": 28.9570,
            "tags": {"amenity": "place_of_worship", "religion": "muslim", "name": "Şehzade Camii", "building": "mosque", "historic": "yes"},
        },
        {
            "name": "Vefa Kilise Camii",
            "lat": 41.0170,
            "lon": 28.9550,
            "tags": {"amenity": "place_of_worship", "religion": "muslim", "name": "Vefa Kilise Camii", "building": "mosque"},
        },
        {
            "name": "Zeyrek Camii",
            "lat": 41.0200,
            "lon": 28.9580,
            "tags": {"amenity": "place_of_worship", "religion": "muslim", "name": "Zeyrek Camii", "building": "mosque", "historic": "yes"},
        },
        {
            "name": "Hirka-i Şerif Camii",
            "lat": 41.0180,
            "lon": 28.9460,
            "tags": {"amenity": "place_of_worship", "religion": "muslim", "name": "Hirka-i Şerif Camii", "building": "mosque"},
        },
        {
            "name": "İskender Paşa Camii",
            "lat": 41.0205,
            "lon": 28.9510,
            "tags": {"amenity": "place_of_worship", "religion": "muslim", "name": "İskender Paşa Camii", "building": "mosque"},
        },
        {
            "name": "Nişancı Mehmet Paşa Camii",
            "lat": 41.0230,
            "lon": 28.9480,
            "tags": {"amenity": "place_of_worship", "religion": "muslim", "name": "Nişancı Mehmet Paşa Camii", "building": "mosque"},
        },
        {
            "name": "Fethiye Camii",
            "lat": 41.0260,
            "lon": 28.9540,
            "tags": {"amenity": "place_of_worship", "religion": "muslim", "name": "Fethiye Camii", "building": "mosque", "historic": "yes"},
        },
    ],

    # ------------------------------------------------------------------
    # OKUL (schools) -- Sisli
    # ------------------------------------------------------------------
    ("okul", "şişli"): [
        {
            "name": "Şişli Terakki Lisesi",
            "lat": 41.0590,
            "lon": 28.9880,
            "tags": {"amenity": "school", "name": "Şişli Terakki Lisesi", "isced:level": "3", "operator:type": "private"},
        },
        {
            "name": "Halide Edip Adıvar İlkokulu",
            "lat": 41.0612,
            "lon": 28.9850,
            "tags": {"amenity": "school", "name": "Halide Edip Adıvar İlkokulu", "isced:level": "1", "operator:type": "public"},
        },
        {
            "name": "Osmanbey İlkokulu",
            "lat": 41.0480,
            "lon": 28.9870,
            "tags": {"amenity": "school", "name": "Osmanbey İlkokulu", "isced:level": "1", "operator:type": "public"},
        },
        {
            "name": "Şişli Anadolu Lisesi",
            "lat": 41.0570,
            "lon": 28.9900,
            "tags": {"amenity": "school", "name": "Şişli Anadolu Lisesi", "isced:level": "3", "operator:type": "public"},
        },
        {
            "name": "Şişli Endüstri Meslek Lisesi",
            "lat": 41.0555,
            "lon": 28.9835,
            "tags": {"amenity": "school", "name": "Şişli Endüstri Meslek Lisesi", "isced:level": "3", "operator:type": "public"},
        },
        {
            "name": "Notre Dame de Sion Lisesi",
            "lat": 41.0530,
            "lon": 28.9920,
            "tags": {"amenity": "school", "name": "Notre Dame de Sion Lisesi", "isced:level": "3", "operator:type": "private"},
        },
        {
            "name": "Şişli Mehmet Akif Ersoy Ortaokulu",
            "lat": 41.0620,
            "lon": 28.9810,
            "tags": {"amenity": "school", "name": "Şişli Mehmet Akif Ersoy Ortaokulu", "isced:level": "2", "operator:type": "public"},
        },
        {
            "name": "Feriköy İlkokulu",
            "lat": 41.0545,
            "lon": 28.9790,
            "tags": {"amenity": "school", "name": "Feriköy İlkokulu", "isced:level": "1", "operator:type": "public"},
        },
    ],

    # ------------------------------------------------------------------
    # RESTORAN (restaurants) -- Beyoglu
    # ------------------------------------------------------------------
    ("restoran", "beyoğlu"): [
        {
            "name": "Haci Abdullah Lokantası",
            "lat": 41.0355,
            "lon": 28.9772,
            "tags": {"amenity": "restaurant", "name": "Haci Abdullah Lokantası", "cuisine": "turkish", "opening_hours": "Mo-Su 11:00-23:00"},
        },
        {
            "name": "Çiçek Pasajı Restoranları",
            "lat": 41.0335,
            "lon": 28.9765,
            "tags": {"amenity": "restaurant", "name": "Çiçek Pasajı Restoranları", "cuisine": "turkish;meyhane"},
        },
        {
            "name": "Ara Kafe",
            "lat": 41.0320,
            "lon": 28.9750,
            "tags": {"amenity": "restaurant", "name": "Ara Kafe", "cuisine": "international"},
        },
        {
            "name": "Mikla Restaurant",
            "lat": 41.0345,
            "lon": 28.9785,
            "tags": {"amenity": "restaurant", "name": "Mikla Restaurant", "cuisine": "turkish;modern", "stars": "1"},
        },
        {
            "name": "Jash Restaurant",
            "lat": 41.0325,
            "lon": 28.9738,
            "tags": {"amenity": "restaurant", "name": "Jash Restaurant", "cuisine": "armenian"},
        },
        {
            "name": "Sofyalı 9",
            "lat": 41.0338,
            "lon": 28.9755,
            "tags": {"amenity": "restaurant", "name": "Sofyalı 9", "cuisine": "meyhane"},
        },
        {
            "name": "Karaköy Lokantası",
            "lat": 41.0218,
            "lon": 28.9740,
            "tags": {"amenity": "restaurant", "name": "Karaköy Lokantası", "cuisine": "turkish"},
        },
        {
            "name": "Helvetia Lokantası",
            "lat": 41.0300,
            "lon": 28.9760,
            "tags": {"amenity": "restaurant", "name": "Helvetia Lokantası", "cuisine": "turkish"},
        },
    ],

    # ------------------------------------------------------------------
    # MUZE (museums) -- Sultanahmet
    # ------------------------------------------------------------------
    ("müze", "sultanahmet"): [
        {
            "name": "Ayasofya Camii (Hagia Sophia)",
            "lat": 41.0086,
            "lon": 28.9802,
            "tags": {"tourism": "museum", "name": "Ayasofya", "name:en": "Hagia Sophia", "historic": "yes", "building": "mosque"},
        },
        {
            "name": "Topkapı Sarayı Müzesi",
            "lat": 41.0115,
            "lon": 28.9834,
            "tags": {"tourism": "museum", "name": "Topkapı Sarayı Müzesi", "name:en": "Topkapi Palace Museum", "historic": "yes"},
        },
        {
            "name": "İstanbul Arkeoloji Müzeleri",
            "lat": 41.0117,
            "lon": 28.9814,
            "tags": {"tourism": "museum", "name": "İstanbul Arkeoloji Müzeleri", "name:en": "Istanbul Archaeology Museums"},
        },
        {
            "name": "Türk ve İslam Eserleri Müzesi",
            "lat": 41.0060,
            "lon": 28.9752,
            "tags": {"tourism": "museum", "name": "Türk ve İslam Eserleri Müzesi", "name:en": "Turkish and Islamic Arts Museum"},
        },
        {
            "name": "Yerebatan Sarnıcı (Bazilika Sarnıcı)",
            "lat": 41.0084,
            "lon": 28.9779,
            "tags": {"tourism": "museum", "name": "Yerebatan Sarnıcı", "name:en": "Basilica Cistern", "historic": "yes"},
        },
        {
            "name": "Mozaik Müzesi (Büyük Saray Mozaikleri Müzesi)",
            "lat": 41.0055,
            "lon": 28.9770,
            "tags": {"tourism": "museum", "name": "Büyük Saray Mozaikleri Müzesi", "name:en": "Great Palace Mosaic Museum"},
        },
    ],

    # ------------------------------------------------------------------
    # KAFE (cafes) -- Kadikoy
    # ------------------------------------------------------------------
    ("kafe", "kadıköy"): [
        {
            "name": "Walter's Coffee Roastery",
            "lat": 40.9905,
            "lon": 29.0265,
            "tags": {"amenity": "cafe", "name": "Walter's Coffee Roastery", "cuisine": "coffee_shop"},
        },
        {
            "name": "Fazıl Bey'in Türk Kahvesi",
            "lat": 40.9898,
            "lon": 29.0243,
            "tags": {"amenity": "cafe", "name": "Fazıl Bey'in Türk Kahvesi", "cuisine": "coffee_shop"},
        },
        {
            "name": "Baylan Pastanesi",
            "lat": 40.9890,
            "lon": 29.0258,
            "tags": {"amenity": "cafe", "name": "Baylan Pastanesi", "cuisine": "pastry;coffee"},
        },
        {
            "name": "Moda Çay Bahçesi",
            "lat": 40.9820,
            "lon": 29.0310,
            "tags": {"amenity": "cafe", "name": "Moda Çay Bahçesi", "cuisine": "tea", "outdoor_seating": "yes"},
        },
        {
            "name": "Kronotrop Coffee",
            "lat": 40.9910,
            "lon": 29.0270,
            "tags": {"amenity": "cafe", "name": "Kronotrop Coffee", "cuisine": "coffee_shop"},
        },
        {
            "name": "Kahve Dünyası Kadıköy",
            "lat": 40.9915,
            "lon": 29.0250,
            "tags": {"amenity": "cafe", "name": "Kahve Dünyası Kadıköy", "cuisine": "coffee_shop", "brand": "Kahve Dünyası"},
        },
        {
            "name": "MOC Kadıköy",
            "lat": 40.9895,
            "lon": 29.0235,
            "tags": {"amenity": "cafe", "name": "MOC Kadıköy", "cuisine": "coffee_shop"},
        },
        {
            "name": "Coffee Sapiens",
            "lat": 40.9885,
            "lon": 29.0280,
            "tags": {"amenity": "cafe", "name": "Coffee Sapiens", "cuisine": "coffee_shop"},
        },
    ],
}


# ---------------------------------------------------------------------------
# Normalisation helpers – allow look-ups with or without Turkish characters
# and with different casings.
# ---------------------------------------------------------------------------

_CHAR_MAP = str.maketrans({
    "ı": "i", "İ": "i",
    "ö": "o", "Ö": "o",
    "ü": "u", "Ü": "u",
    "ş": "s", "Ş": "s",
    "ç": "c", "Ç": "c",
    "ğ": "g", "Ğ": "g",
    "â": "a",
})


def _normalise(text: str) -> str:
    """Lower-case and strip Turkish-specific characters."""
    return text.lower().translate(_CHAR_MAP).strip()


# Build a fast look-up index that maps normalised keys to the original data.
_INDEX: Dict[Tuple[str, str], List[Dict[str, Any]]] = {}
for (poi, loc), entries in SAMPLE_DATA.items():
    _INDEX[(_normalise(poi), _normalise(loc))] = entries


# Also build partial-match lists so that e.g. poi_type="hospital" can match
# "hastane" data via the POI_TAG_MAP synonym mapping in osm_client.
_POI_SYNONYMS: Dict[str, str] = {
    "hospital": "hastane",
    "pharmacy": "eczane",
    "school": "okul",
    "restaurant": "restoran",
    "mosque": "cami",
    "museum": "muze",
    "cafe": "kafe",
}


def get_sample_elements(
    poi_type: str,
    location: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Return sample POI data in Overpass API element format.

    Parameters
    ----------
    poi_type : str
        The type of POI (e.g. "hastane", "hospital", "eczane", ...).
    location : str or None
        District / neighbourhood name (e.g. "kadıköy", "taksim").

    Returns
    -------
    list[dict]
        A list of dicts that mirror the Overpass ``elements`` schema::

            {"id": <int>, "type": "node", "lat": ..., "lon": ..., "tags": {...}}
    """
    norm_poi = _normalise(poi_type)

    # Resolve English synonyms to their Turkish keys
    norm_poi = _normalise(_POI_SYNONYMS.get(norm_poi, norm_poi))

    norm_loc = _normalise(location) if location else ""

    # Exact match
    entries = _INDEX.get((norm_poi, norm_loc))

    # If no exact match, try partial location match
    if entries is None:
        for (p, l), v in _INDEX.items():
            if p == norm_poi and (norm_loc in l or l in norm_loc):
                entries = v
                break

    # If still nothing, try matching just the POI type (any location)
    if entries is None:
        for (p, l), v in _INDEX.items():
            if p == norm_poi:
                entries = v
                break

    if entries is None:
        return []

    # Convert to Overpass element format
    elements: List[Dict[str, Any]] = []
    for idx, entry in enumerate(entries):
        element = {
            "id": 9_000_000_000 + random.randint(0, 999_999_999),
            "type": "node",
            "lat": entry["lat"],
            "lon": entry["lon"],
            "tags": dict(entry["tags"]),  # copy so callers cannot mutate originals
        }
        elements.append(element)

    return elements
