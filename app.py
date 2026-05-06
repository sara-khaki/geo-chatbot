import streamlit as st
import pandas as pd
import json
import sys
import os
import folium
from streamlit_folium import st_folium
from streamlit_js_eval import get_geolocation
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))

from agent.core import GeoAgent

st.set_page_config(
    page_title="GeoAI ChatBot - Istanbul",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --primary: #6C63FF;
    --primary-light: #8B83FF;
    --primary-dark: #5A52E0;
    --accent: #00D4AA;
    --accent-light: #00F5C8;
    --bg-dark: #0A0E27;
    --bg-card: #12173D;
    --bg-card-hover: #1A1F4E;
    --text-primary: #FFFFFF;
    --text-secondary: #A0AEC0;
    --border: rgba(108, 99, 255, 0.2);
    --gradient-1: linear-gradient(135deg, #6C63FF 0%, #00D4AA 100%);
    --gradient-2: linear-gradient(135deg, #0A0E27 0%, #1A1F4E 100%);
    --shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    --shadow-glow: 0 0 40px rgba(108, 99, 255, 0.15);
}

.stApp {
    background: var(--bg-dark) !important;
    font-family: 'Inter', sans-serif !important;
}

div[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0D1235 0%, #12173D 50%, #0A0E27 100%) !important;
    border-right: 1px solid var(--border) !important;
}

div[data-testid="stSidebar"] .stMarkdown h1,
div[data-testid="stSidebar"] .stMarkdown h2,
div[data-testid="stSidebar"] .stMarkdown h3 {
    color: var(--text-primary) !important;
}

div[data-testid="stSidebar"] .stMarkdown p,
div[data-testid="stSidebar"] .stMarkdown li {
    color: var(--text-secondary) !important;
}

.hero-container {
    background: linear-gradient(135deg, rgba(108,99,255,0.08) 0%, rgba(0,212,170,0.05) 100%);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}

.hero-container::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(ellipse at center, rgba(108,99,255,0.06) 0%, transparent 70%);
    animation: pulse-bg 8s ease-in-out infinite;
}

@keyframes pulse-bg {
    0%, 100% { transform: scale(1); opacity: 0.5; }
    50% { transform: scale(1.1); opacity: 1; }
}

.hero-title {
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #6C63FF 0%, #00D4AA 50%, #6C63FF 100%);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradient-shift 4s ease infinite;
    margin: 0 0 0.3rem 0;
    position: relative;
    z-index: 1;
    letter-spacing: -0.5px;
}

@keyframes gradient-shift {
    0% { background-position: 0% center; }
    50% { background-position: 100% center; }
    100% { background-position: 0% center; }
}

.hero-subtitle {
    font-size: 1rem;
    color: var(--text-secondary);
    margin: 0;
    position: relative;
    z-index: 1;
    font-weight: 400;
}

.student-info {
    background: linear-gradient(135deg, rgba(108,99,255,0.1) 0%, rgba(0,212,170,0.08) 100%);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 1.5rem;
    font-size: 0.82rem;
    color: var(--text-secondary);
    line-height: 1.7;
}

.student-info strong {
    color: var(--accent);
}

.chat-msg-user {
    background: linear-gradient(135deg, rgba(108,99,255,0.15) 0%, rgba(108,99,255,0.08) 100%);
    border: 1px solid rgba(108,99,255,0.25);
    border-radius: 16px 16px 4px 16px;
    padding: 1rem 1.3rem;
    margin: 0.6rem 0;
    color: var(--text-primary);
    font-size: 0.95rem;
    max-width: 85%;
    margin-left: auto;
}

.chat-msg-bot {
    background: linear-gradient(135deg, rgba(0,212,170,0.08) 0%, rgba(0,212,170,0.03) 100%);
    border: 1px solid rgba(0,212,170,0.2);
    border-radius: 16px 16px 16px 4px;
    padding: 1rem 1.3rem;
    margin: 0.6rem 0;
    color: var(--text-primary);
    font-size: 0.95rem;
    max-width: 85%;
}

.stat-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.2rem;
    text-align: center;
    transition: all 0.3s ease;
}

.stat-card:hover {
    border-color: var(--primary);
    transform: translateY(-2px);
    box-shadow: var(--shadow-glow);
}

.stat-number {
    font-size: 2rem;
    font-weight: 800;
    background: var(--gradient-1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
}

.stat-label {
    font-size: 0.78rem;
    color: var(--text-secondary);
    margin: 0.3rem 0 0 0;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 500;
}

.react-log {
    background: linear-gradient(135deg, #0D1235 0%, #12173D 100%);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1rem;
    margin: 0.3rem 0;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.82rem;
}

.log-thought { color: #FFD93D; }
.log-action { color: #6C63FF; }
.log-observation { color: #00D4AA; }
.log-answer { color: #FF6B6B; }
.log-error { color: #FF4757; }
.log-timestamp { color: #4A5568; font-size: 0.72rem; }

.example-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 0.9rem 1.1rem;
    cursor: pointer;
    transition: all 0.3s ease;
    margin-bottom: 0.5rem;
}

.example-card:hover {
    border-color: var(--primary);
    background: var(--bg-card-hover);
    box-shadow: var(--shadow-glow);
    transform: translateY(-1px);
}

.example-icon { font-size: 1.3rem; margin-right: 0.5rem; }
.example-text { color: var(--text-primary); font-size: 0.88rem; }

.map-container {
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid var(--border);
    box-shadow: var(--shadow);
}

div[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid var(--border);
}

.stTextInput > div > div > input {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
    padding: 0.8rem 1rem !important;
    font-size: 0.95rem !important;
    transition: all 0.3s ease !important;
}

.stTextInput > div > div > input:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 20px rgba(108,99,255,0.2) !important;
}

.stButton > button {
    background: var(--gradient-1) !important;
    border: none !important;
    border-radius: 12px !important;
    color: white !important;
    font-weight: 600 !important;
    padding: 0.6rem 2rem !important;
    font-size: 0.9rem !important;
    transition: all 0.3s ease !important;
    letter-spacing: 0.3px !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(108,99,255,0.4) !important;
}

.stExpander {
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    background: var(--bg-card) !important;
}

div[data-testid="stExpander"] details {
    border: none !important;
}

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-dark); }
::-webkit-scrollbar-thumb { background: var(--primary-dark); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--primary); }

.section-header {
    font-size: 1.1rem;
    font-weight: 700;
    color: var(--text-primary);
    margin: 1.5rem 0 0.8rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid var(--border);
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.tool-badge {
    display: inline-block;
    background: rgba(108,99,255,0.15);
    border: 1px solid rgba(108,99,255,0.3);
    border-radius: 20px;
    padding: 0.2rem 0.7rem;
    font-size: 0.75rem;
    color: var(--primary-light);
    font-weight: 500;
    margin: 0.15rem;
}

.divider {
    height: 1px;
    background: var(--border);
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

def _fallback_direct(query: str, user_location: dict = None) -> dict:
    from agent.core import GeoAgent

    class FallbackAgent(GeoAgent):
        def __init__(self):
            self.logs = []
            self.conversation_history = []

        def _call_llm(self, messages):
            raise Exception("LLM not available")

    agent = FallbackAgent()
    return agent._fallback_process(query, user_location=user_location)


EXAMPLE_QUERIES = [
    {"icon": "📍", "text": "Bana en yakın 3 hastaneyi bul", "query": "Bana en yakın 3 hastaneyi bul"},
    {"icon": "📍", "text": "Yakınımdaki eczaneleri göster", "query": "Yakınımdaki eczaneleri göster"},
    {"icon": "🏥", "text": "Kadıköy'deki hastaneleri göster", "query": "Kadıköy'deki hastaneleri göster"},
    {"icon": "💊", "text": "Taksim'e en yakın 5 eczaneyi bul", "query": "Taksim'e en yakın 5 eczaneyi bul"},
    {"icon": "🌳", "text": "Beşiktaş'taki parkları kümele", "query": "Beşiktaş'taki parkları kümele"},
    {"icon": "🕌", "text": "Fatih'teki camileri listele", "query": "Fatih'teki camileri listele"},
    {"icon": "🏫", "text": "Şişli'deki okulları haritada göster", "query": "Şişli'deki okulları haritada göster"},
    {"icon": "🍽️", "text": "Beyoğlu'ndaki restoranları bul", "query": "Beyoğlu'ndaki restoranları bul"},
    {"icon": "🏛️", "text": "Sultanahmet yakınındaki müzeleri göster", "query": "Sultanahmet yakınındaki müzeleri göster"},
    {"icon": "☕", "text": "Kadıköy'deki kafeleri kümele", "query": "Kadıköy'deki kafeleri kümele"},
]

BEDROCK_REGION = "us-east-1"
BEDROCK_MODEL = "us.anthropic.claude-sonnet-4-6"

if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent" not in st.session_state:
    try:
        st.session_state.agent = GeoAgent(region_name=BEDROCK_REGION, model_id=BEDROCK_MODEL)
        st.session_state.agent_ready = True
    except Exception:
        st.session_state.agent = None
        st.session_state.agent_ready = False
if "agent_ready" not in st.session_state:
    st.session_state.agent_ready = False
if "selected_example" not in st.session_state:
    st.session_state.selected_example = None
if "total_queries" not in st.session_state:
    st.session_state.total_queries = 0
if "total_results" not in st.session_state:
    st.session_state.total_results = 0
if "user_location" not in st.session_state:
    st.session_state.user_location = None
if "location_map_click" not in st.session_state:
    st.session_state.location_map_click = None


with st.sidebar:
    import base64
    logo_path = os.path.join(os.path.dirname(__file__), "assets", "itu_logo.png")
    with open(logo_path, "rb") as f:
        logo_b64 = base64.b64encode(f.read()).decode()

    st.markdown(f"""
    <div style="text-align:center; padding: 1.2rem 0 0.6rem 0;">
        <img src="data:image/png;base64,{logo_b64}"
             style="width:180px; filter: brightness(0) invert(1); opacity:0.92; margin-bottom:0.6rem;" />
        <div style="font-size: 1.3rem; font-weight: 700; background: linear-gradient(135deg, #6C63FF, #00D4AA);
                    -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            GeoAI ChatBot
        </div>
        <div style="font-size: 0.75rem; color: #A0AEC0; margin-top: 0.2rem;">Istanbul Spatial Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown("### Proje Bilgileri")
    st.markdown("""
    <div class="student-info">
        <strong>Sara Khaki</strong><br>
        Öğrenci No: 010210931<br><br>
        <strong>Ders:</strong> MYZ 305E – Artificial Intelligence for Geomatics Eng.<br>
        <strong>Dönem:</strong> 2025-2026 Spring Term Project<br><br>
        <strong>Proje:</strong> LLM-Powered GeoChatBot for Spatial Querying (Istanbul)
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown("### 📍 Konumum")

    loc_col1, loc_col2 = st.columns(2)
    with loc_col1:
        use_gps = st.button("📡 Konumumu Kullan", key="gps_btn", use_container_width=True)
    with loc_col2:
        clear_loc = st.button("🗑️ Temizle", key="clear_loc_btn", use_container_width=True)

    if clear_loc:
        st.session_state.user_location = None
        st.session_state.location_map_click = None
        st.rerun()

    if use_gps:
        with st.spinner("Konum alınıyor..."):
            geo_data = get_geolocation()
            if geo_data and "coords" in geo_data:
                st.session_state.user_location = {
                    "lat": geo_data["coords"]["latitude"],
                    "lon": geo_data["coords"]["longitude"],
                }
                st.rerun()
            elif geo_data:
                st.warning("Konum alınamadı. Lütfen tarayıcı izinlerini kontrol edin.")

    st.markdown("""
    <p style="color:#A0AEC0; font-size:0.75rem; margin:0.3rem 0;">
        veya haritada bir noktaya tıklayın:
    </p>
    """, unsafe_allow_html=True)

    location_map = folium.Map(
        location=[41.0082, 28.9784],
        zoom_start=10,
        tiles="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png",
        attr="CARTO",
        width="100%",
        height=150,
    )

    if st.session_state.user_location:
        folium.Marker(
            location=[st.session_state.user_location["lat"], st.session_state.user_location["lon"]],
            icon=folium.Icon(color="red", icon="user", prefix="glyphicon"),
            popup="Konumunuz",
        ).add_to(location_map)

    map_click = st_folium(
        location_map,
        height=150,
        width=None,
        key="location_picker",
        returned_objects=["last_clicked"],
    )

    if map_click and map_click.get("last_clicked"):
        clicked = map_click["last_clicked"]
        st.session_state.user_location = {"lat": clicked["lat"], "lon": clicked["lng"]}
        st.session_state.location_map_click = clicked

    if st.session_state.user_location:
        loc = st.session_state.user_location
        st.markdown(f"""
        <div style="background: rgba(0,212,170,0.1); border: 1px solid rgba(0,212,170,0.3);
                    border-radius: 8px; padding: 0.5rem; margin: 0.3rem 0; text-align: center;">
            <span style="color: #00D4AA; font-size: 0.8rem; font-weight: 600;">
                ✓ Konum Ayarlandı
            </span><br>
            <span style="color: #A0AEC0; font-size: 0.72rem;">
                {loc['lat']:.5f}°N, {loc['lon']:.5f}°E
            </span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: rgba(108,99,255,0.08); border: 1px solid rgba(108,99,255,0.2);
                    border-radius: 8px; padding: 0.5rem; margin: 0.3rem 0; text-align: center;">
            <span style="color: #A0AEC0; font-size: 0.75rem;">
                Konum belirlenmedi
            </span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown("### Desteklenen Araçlar")
    tools_html = ""
    for t in ["query_osm", "find_nearest", "find_near_me", "cluster_points", "calculate_distance", "generate_map", "get_statistics"]:
        tools_html += f'<span class="tool-badge">{t}</span> '
    st.markdown(tools_html, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    st.markdown("### Desteklenen POI Tipleri")
    pois = [
        "hastane", "eczane", "park", "okul", "üniversite", "restoran",
        "kafe", "cami", "müze", "otel", "banka", "market",
        "kütüphane", "metro", "otobüs durağı",
    ]
    poi_html = " ".join(f'<span class="tool-badge">{p}</span>' for p in pois)
    st.markdown(poi_html, unsafe_allow_html=True)


st.markdown("""
<div class="hero-container">
    <div class="hero-title">GeoAI ChatBot</div>
    <div class="hero-subtitle">
        Istanbul mekansal sorgulama asistanı — Doğal dilde soru sorun, yapay zeka haritada göstersin.
    </div>
</div>
""", unsafe_allow_html=True)

if st.session_state.total_queries > 0:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{st.session_state.total_queries}</div>
            <div class="stat-label">Toplam Sorgu</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{st.session_state.total_results}</div>
            <div class="stat-label">Bulunan Sonuç</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{len(st.session_state.messages) // 2}</div>
            <div class="stat-label">Konuşma</div>
        </div>""", unsafe_allow_html=True)

if not st.session_state.messages:
    st.markdown('<div class="section-header">Örnek Sorgular</div>', unsafe_allow_html=True)

    cols = st.columns(2)
    for i, ex in enumerate(EXAMPLE_QUERIES):
        with cols[i % 2]:
            if st.button(f"{ex['icon']}  {ex['text']}", key=f"ex_{i}", use_container_width=True):
                st.session_state.selected_example = ex["query"]
                st.rerun()

for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="chat-msg-user">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-msg-bot">{msg["content"]}</div>', unsafe_allow_html=True)

        if "map" in msg and msg["map"] is not None:
            st.markdown('<div class="map-container">', unsafe_allow_html=True)
            st_folium(msg["map"], width=None, height=500, returned_objects=[])
            st.markdown('</div>', unsafe_allow_html=True)

        if "gdf" in msg and msg["gdf"] is not None and len(msg["gdf"]) > 0:
            with st.expander(f"Sonuç Tablosu ({len(msg['gdf'])} kayıt)", expanded=False):
                display_cols = ["name", "lat", "lon"]
                if "distance_km" in msg["gdf"].columns:
                    display_cols.append("distance_km")
                if "cluster" in msg["gdf"].columns:
                    display_cols.append("cluster")
                available = [c for c in display_cols if c in msg["gdf"].columns]
                st.dataframe(msg["gdf"][available], use_container_width=True, hide_index=True)

        if "stats" in msg and msg["stats"] is not None:
            with st.expander("İstatistikler", expanded=False):
                stats = msg["stats"]
                scol1, scol2 = st.columns(2)
                with scol1:
                    st.metric("Toplam Sonuç", stats.get("count", 0))
                    if "min_distance_m" in stats:
                        st.metric("Min Mesafe", f"{stats['min_distance_m']:.0f} m")
                with scol2:
                    if "avg_distance_m" in stats:
                        st.metric("Ort. Mesafe", f"{stats['avg_distance_m']:.0f} m")
                    if "n_clusters" in stats:
                        st.metric("Küme Sayısı", stats["n_clusters"])

        if "logs" in msg and msg["logs"]:
            with st.expander("Agent ReAct Log (Düşünce Süreci)", expanded=False):
                for log_entry in msg["logs"]:
                    step = log_entry["step"]
                    content = log_entry["content"]
                    ts = log_entry["timestamp"]

                    color_map = {
                        "THOUGHT": "log-thought",
                        "ACTION": "log-action",
                        "OBSERVATION": "log-observation",
                        "ANSWER": "log-answer",
                        "ERROR": "log-error",
                        "USER_QUERY": "log-thought",
                        "LLM_RESPONSE": "log-action",
                        "FALLBACK": "log-error",
                    }
                    css_class = color_map.get(step, "log-thought")
                    icon_map = {
                        "THOUGHT": "💭",
                        "ACTION": "⚡",
                        "OBSERVATION": "👁️",
                        "ANSWER": "✅",
                        "ERROR": "❌",
                        "USER_QUERY": "💬",
                        "LLM_RESPONSE": "🤖",
                        "FALLBACK": "🔄",
                    }
                    icon = icon_map.get(step, "📝")

                    safe_content = content.replace("<", "&lt;").replace(">", "&gt;")
                    st.markdown(f"""
                    <div class="react-log">
                        <span class="log-timestamp">{ts}</span><br>
                        <span class="{css_class}">{icon} <b>[{step}]</b> {safe_content}</span>
                    </div>
                    """, unsafe_allow_html=True)


default_value = st.session_state.selected_example if st.session_state.selected_example else ""
if st.session_state.selected_example:
    st.session_state.selected_example = None

user_input = st.chat_input("Istanbul hakkında mekansal bir soru sorun...")

if default_value and not user_input:
    user_input = default_value

if user_input:
    query_lower = user_input.lower()
    needs_location = any(w in query_lower for w in ["bana yakın", "yakınımdaki", "yakınımda", "etrafımdaki", "çevremdeki", "near me", "around me"])

    if needs_location and not st.session_state.user_location:
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({
            "role": "assistant",
            "content": "📍 Konumunuz henüz ayarlanmamış. Lütfen sol paneldeki **Konumum** bölümünden konumunuzu belirleyin (GPS butonu veya haritaya tıklayarak).",
            "map": None, "gdf": None, "stats": None, "logs": [],
        })
        st.rerun()

    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.total_queries += 1

    user_coords = None
    if needs_location and st.session_state.user_location:
        user_coords = st.session_state.user_location

    if not st.session_state.agent_ready:
        try:
            st.session_state.agent = GeoAgent(region_name=BEDROCK_REGION, model_id=BEDROCK_MODEL)
            st.session_state.agent_ready = True
        except Exception:
            pass

    with st.spinner("Agent düşünüyor..."):
        if st.session_state.agent_ready and st.session_state.agent:
            try:
                result = st.session_state.agent.process_query(user_input, user_location=user_coords)
            except Exception as e:
                from agent.tools import execute_tool
                result = _fallback_direct(user_input, user_location=user_coords)
        else:
            result = _fallback_direct(user_input, user_location=user_coords)

    answer = result.get("answer", "Bir hata oluştu.")
    gdf = result.get("gdf")
    folium_map = result.get("map")
    stats = result.get("stats")
    logs = result.get("logs", [])

    if gdf is not None:
        st.session_state.total_results += len(gdf)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "map": folium_map,
        "gdf": gdf,
        "stats": stats,
        "logs": logs,
    })

    st.rerun()


st.markdown("""
<div style="text-align:center; padding: 2rem 0 1rem 0; color: var(--text-secondary); font-size: 0.75rem;">
    <div style="margin-bottom: 0.3rem;">
        <span style="background: var(--gradient-1); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 700;">
            GeoAI ChatBot
        </span>
        &nbsp;|&nbsp; Istanbul Spatial Intelligence
    </div>
    <div>
        Sara Khaki (010210931) &bull; MYZ 305E – AI for Geomatics Eng. &bull; 2025-2026 Spring
    </div>
    <div style="margin-top: 0.3rem; color: #4A5568;">
        Powered by AWS Bedrock (Claude) &bull; OpenStreetMap &bull; Folium &bull; GeoPandas
    </div>
</div>
""", unsafe_allow_html=True)
