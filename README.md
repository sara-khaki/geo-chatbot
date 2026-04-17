# GeoAI ChatBot - Istanbul Spatial Querying

**LLM-Powered GeoChatBot for Spatial Querying (Istanbul)**

> Sara Khaki | 010210931 | MYZ 305E – Artificial Intelligence for Geomatics Eng. | 2025-2026 Spring Term Project

---

## Overview

GeoAI ChatBot is an intelligent spatial querying assistant for Istanbul. Users ask questions in natural language (Turkish or English), and the AI agent autonomously:

1. **Parses** the query using Claude LLM (via AWS Bedrock)
2. **Generates** appropriate Overpass API queries for OpenStreetMap
3. **Fetches** geospatial data
4. **Analyzes** the data (distance calculation, clustering, statistics)
5. **Visualizes** results on an interactive map with data tables

## Architecture

The system follows the **ReAct (Reasoning + Acting)** agent pattern:

```
User Query → LLM (Thought) → Tool Selection (Action) → Execution (Observation) → Response (Answer)
```

### AI Agent Tools

| Tool | Description |
|------|-------------|
| `query_osm` | Queries OpenStreetMap via Overpass API |
| `calculate_distance` | Haversine distance between two points |
| `find_nearest` | Finds K nearest POIs to a target |
| `cluster_points` | K-means spatial clustering |
| `generate_map` | Interactive Folium map generation |
| `get_statistics` | Basic spatial statistics |

## Tech Stack

- **LLM**: Claude (AWS Bedrock) - Agent brain
- **UI**: Streamlit - Web interface
- **Geospatial**: GeoPandas, Shapely - Spatial analysis
- **Data**: Overpass API - OpenStreetMap data
- **Visualization**: Folium - Interactive maps
- **ML**: Scikit-learn - K-means clustering

## Installation

### Prerequisites

- Python 3.11+
- AWS CLI configured with Bedrock access
- AWS credentials set up (`~/.aws/credentials`)

### Setup

```bash
# Clone the repository
git clone <repo-url>
cd geo-chatbot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

### AWS Bedrock Configuration

Make sure your AWS credentials are configured:

```bash
aws configure
# Enter your AWS Access Key ID, Secret Access Key, and region
```

Ensure you have access to Claude models in AWS Bedrock.

## Usage

### Start the Application

```bash
streamlit run app.py
```

The application will open at `http://localhost:8501`.

### Example Queries

1. **Show POIs in an area:**
   > "Kadıköy'deki hastaneleri göster"
   
   Agent uses `query_osm` tool to find hospitals in Kadıköy district.

2. **Find nearest locations:**
   > "Taksim'e en yakın 5 eczaneyi bul"
   
   Agent uses `find_nearest` tool with Taksim coordinates.

3. **Cluster analysis:**
   > "Beşiktaş'taki parkları kümele"
   
   Agent uses `cluster_points` tool for K-means clustering.

4. **List and map:**
   > "Fatih'teki camileri listele ve haritada göster"
   
   Agent uses `query_osm` and `generate_map` tools.

5. **Complex queries:**
   > "Sultanahmet yakınındaki müzeleri göster"
   
   Agent determines the location, searches museums, calculates distances.

### How the Agent Works

For each query, the agent follows the ReAct pattern:

```
💭 [THOUGHT]      Kullanıcı Kadıköy'deki hastaneleri istiyor...
⚡ [ACTION]       Tool: query_osm, Params: {poi_type: "hastane", location: "kadıköy"}
👁️ [OBSERVATION]  Başarılı. 12 sonuç bulundu.
✅ [ANSWER]       Kadıköy bölgesinde 12 adet hastane bulundu.
```

## Project Structure

```
geo-chatbot/
├── app.py                 # Streamlit main application
├── agent/
│   ├── __init__.py
│   ├── core.py            # Agent main loop (ReAct)
│   ├── tools.py           # Tool definitions & execution
│   └── prompts.py         # System prompts for LLM
├── geo/
│   ├── __init__.py
│   ├── osm_client.py      # Overpass API client
│   ├── analysis.py        # Spatial analysis functions
│   └── visualize.py       # Folium map generation
├── assets/
│   └── itu_logo.png       # ITU university logo
├── data/
│   ├── __init__.py
│   └── sample_data.py     # Fallback demo data (offline mode)
├── .gitignore
├── requirements.txt
└── README.md
```

## Supported POI Types

| Turkish | English | OSM Tag |
|---------|---------|---------|
| Hastane | Hospital | amenity=hospital |
| Eczane | Pharmacy | amenity=pharmacy |
| Park | Park | leisure=park |
| Okul | School | amenity=school |
| Üniversite | University | amenity=university |
| Restoran | Restaurant | amenity=restaurant |
| Kafe | Cafe | amenity=cafe |
| Cami | Mosque | amenity=place_of_worship |
| Müze | Museum | tourism=museum |
| Otel | Hotel | tourism=hotel |
| Banka | Bank | amenity=bank |
| Market | Supermarket | shop=supermarket |
| Kütüphane | Library | amenity=library |

## Supported Istanbul Districts

Kadıköy, Beşiktaş, Taksim, Sultanahmet, Üsküdar, Fatih, Beyoğlu, Şişli, Bakırköy, Sarıyer, Eminönü, Maltepe, Kartal, Pendik, Ataşehir, Ümraniye, Eyüp, Beylikdüzü, Esenyurt, Avcılar, Bağcılar, Bahçelievler, Ortaköy, Karaköy, Galata, and more.

## Features

- Natural language spatial queries (Turkish & English)
- Autonomous AI agent with ReAct reasoning
- Interactive Folium maps with multiple tile layers
- K-means clustering visualization
- Distance calculations with Haversine formula
- Result caching for performance
- Detailed agent reasoning logs
- Responsive dark-themed UI

## License

This project was developed as a course project for MYZ 305E – Artificial Intelligence for Geomatics Engineering, Istanbul Technical University, 2025-2026 Spring Term.
