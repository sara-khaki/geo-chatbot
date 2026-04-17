import folium
from folium.plugins import MarkerCluster
import geopandas as gpd
import branca.colormap as cm

ISTANBUL_CENTER = [41.0082, 28.9784]

CLUSTER_COLORS = [
    "#e74c3c", "#3498db", "#2ecc71", "#f39c12", "#9b59b6",
    "#1abc9c", "#e67e22", "#34495e", "#e91e63", "#00bcd4",
]

POI_ICONS = {
    "hospital": ("plus-sign", "red"),
    "pharmacy": ("medkit", "green"),
    "park": ("tree-deciduous", "green"),
    "school": ("education", "blue"),
    "university": ("education", "darkblue"),
    "restaurant": ("cutlery", "orange"),
    "cafe": ("coffee", "cadetblue"),
    "mosque": ("home", "darkgreen"),
    "church": ("home", "purple"),
    "bank": ("usd", "darkblue"),
    "museum": ("picture", "darkpurple"),
    "hotel": ("bed", "cadetblue"),
    "supermarket": ("shopping-cart", "lightred"),
    "library": ("book", "darkblue"),
    "fuel": ("tint", "gray"),
    "bus_stop": ("road", "darkblue"),
    "default": ("map-marker", "blue"),
}


def _get_icon(poi_type: str = None):
    if poi_type:
        key = poi_type.lower().strip()
        if key in POI_ICONS:
            return POI_ICONS[key]
    return POI_ICONS["default"]


def generate_map(
    gdf: gpd.GeoDataFrame,
    center=None,
    poi_type: str = None,
    target_point=None,
    use_clusters_visual: bool = False,
    title: str = None,
) -> folium.Map:
    if center:
        map_center = [center[1], center[0]] if center[0] < center[1] else list(center)
    elif not gdf.empty:
        map_center = [gdf["lat"].mean(), gdf["lon"].mean()]
    else:
        map_center = ISTANBUL_CENTER

    m = folium.Map(
        location=map_center,
        zoom_start=13,
        tiles=None,
        control_scale=True,
    )

    folium.TileLayer(
        tiles="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
        attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> '
             'contributors &copy; <a href="https://carto.com/">CARTO</a>',
        name="CartoDB Positron",
    ).add_to(m)

    folium.TileLayer(
        tiles="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
        attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> '
             'contributors &copy; <a href="https://carto.com/">CARTO</a>',
        name="CartoDB Dark",
    ).add_to(m)

    folium.TileLayer(
        tiles="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
        name="OpenStreetMap",
    ).add_to(m)

    if target_point:
        folium.Marker(
            location=[target_point[0], target_point[1]],
            popup="<b>Hedef Nokta</b>",
            icon=folium.Icon(color="red", icon="star", prefix="glyphicon"),
        ).add_to(m)

    if not gdf.empty:
        has_clusters = "cluster" in gdf.columns and use_clusters_visual

        if has_clusters:
            for cluster_id in gdf["cluster"].unique():
                cluster_gdf = gdf[gdf["cluster"] == cluster_id]
                color = CLUSTER_COLORS[cluster_id % len(CLUSTER_COLORS)]
                fg = folium.FeatureGroup(name=f"Küme {cluster_id + 1}")
                for _, row in cluster_gdf.iterrows():
                    popup_html = _build_popup(row, poi_type)
                    folium.CircleMarker(
                        location=[row["lat"], row["lon"]],
                        radius=8,
                        popup=folium.Popup(popup_html, max_width=300),
                        color=color,
                        fill=True,
                        fill_color=color,
                        fill_opacity=0.7,
                        weight=2,
                    ).add_to(fg)
                fg.add_to(m)
        else:
            icon_name, icon_color = _get_icon(poi_type)
            if len(gdf) > 50:
                mc = MarkerCluster(name="Sonuçlar")
                for _, row in gdf.iterrows():
                    popup_html = _build_popup(row, poi_type)
                    folium.Marker(
                        location=[row["lat"], row["lon"]],
                        popup=folium.Popup(popup_html, max_width=300),
                        icon=folium.Icon(color=icon_color, icon=icon_name, prefix="glyphicon"),
                    ).add_to(mc)
                mc.add_to(m)
            else:
                fg = folium.FeatureGroup(name="Sonuçlar")
                for _, row in gdf.iterrows():
                    popup_html = _build_popup(row, poi_type)
                    folium.Marker(
                        location=[row["lat"], row["lon"]],
                        popup=folium.Popup(popup_html, max_width=300),
                        icon=folium.Icon(color=icon_color, icon=icon_name, prefix="glyphicon"),
                    ).add_to(fg)
                fg.add_to(m)

        if target_point and "distance_m" in gdf.columns:
            for _, row in gdf.iterrows():
                folium.PolyLine(
                    locations=[
                        [target_point[0], target_point[1]],
                        [row["lat"], row["lon"]],
                    ],
                    color="#e74c3c",
                    weight=1.5,
                    opacity=0.5,
                    dash_array="5 10",
                ).add_to(m)

    folium.LayerControl().add_to(m)

    if title:
        title_html = f"""
        <div style="position:fixed;top:10px;left:50%;transform:translateX(-50%);
                    z-index:9999;background:white;padding:8px 16px;border-radius:8px;
                    box-shadow:0 2px 8px rgba(0,0,0,0.2);font-size:14px;font-weight:bold;">
            {title}
        </div>
        """
        m.get_root().html.add_child(folium.Element(title_html))

    return m


def _build_popup(row, poi_type=None):
    name = row.get("name", "Bilinmeyen")
    parts = [f"<b>{name}</b>"]

    if "distance_km" in row.index and not (isinstance(row["distance_km"], float) and row["distance_km"] != row["distance_km"]):
        parts.append(f"Mesafe: {row['distance_km']} km")

    if "cluster" in row.index:
        parts.append(f"Küme: {int(row['cluster']) + 1}")

    addr = row.get("addr:street", "")
    if addr:
        parts.append(f"Adres: {addr}")

    phone = row.get("phone", "")
    if phone:
        parts.append(f"Tel: {phone}")

    website = row.get("website", "")
    if website:
        parts.append(f'<a href="{website}" target="_blank">Web</a>')

    parts.append(f"<small>({row['lat']:.5f}, {row['lon']:.5f})</small>")
    return "<br>".join(parts)
