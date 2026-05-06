# GeoAI ChatBot - Proje Rehberi

> Sara Khaki | 010210931 | MYZ 305E - AI for Geomatics Eng. | 2025-2026 Spring

---

## BÖLÜM 1: Proje Nedir? (Büyük Resim)

### 1.1 Dersin İsteği

Hocamız bizden şunları istedi (MYZ305E-TP.pdf):

- Mekânsal (harita/konum ile ilgili) bir yapay zekâ problemi çözün
- En az bir **AI Agent** (yapay zekâ ajanı) kullanın
- Gerçek coğrafi veri kullanın
- Kodu GitHub'a koyun ve kısa bir demo videosu çekin
- Poster hazırlayın

### 1.2 Biz Ne Seçtik?

Hocanın verdiği örnek uygulamalar arasında şu vardı:

> **"LLM-Powered GeoChatBots for Spatial Querying"**

Yani: Kullanıcının doğal dilde (normal konuşma diliyle) soru sorduğu ve yapay zekânın harita üzerinde cevap verdiği bir chatbot.

### 1.3 Projemizin Özeti (Tek Cümle)

**İstanbul'daki herhangi bir yeri (hastane, eczane, park, okul, vb.) doğal dilde sorabildiğin, yapay zekânın sorunu anlayıp haritada gösterdiği bir chatbot yaptık.**

Örnek:
- Sen yazıyorsun: *"Kadıköy'deki hastaneleri göster"*
- Sistem: Anlıyor ki hastane arıyorsun, Kadıköy bölgesinde, OpenStreetMap'ten verileri çekiyor, haritada gösteriyor.

---

## BÖLÜM 2: Temel Kavramlar (Hiç Bilmeyenler İçin)

### 2.1 Yapay Zekâ (AI) Nedir?

Bilgisayarın insan gibi düşünmesini, anlama ve karar vermesini sağlayan teknoloji. Bizim projede yapay zekâ, senin yazdığın Türkçe cümleyi anlıyor ve ne yapması gerektiğine karar veriyor.

### 2.2 LLM (Large Language Model) Nedir?

ChatGPT'yi biliyorsun değil mi? İşte o bir LLM. Büyük dil modeli demek. Milyarlarca metin okuyarak eğitilmiş, insan dilini anlayan ve üreten bir yapay zekâ.

Biz **Claude** adında bir LLM kullanıyoruz. Claude, Anthropic şirketi tarafından geliştirilmiş bir yapay zekâ. ChatGPT'nin rakibi gibi düşünebilirsin.

### 2.3 AI Agent (Yapay Zekâ Ajanı) Nedir?

Normal bir chatbot sadece cevap verir. Ama bir **Agent** (ajan) şu özelliklere sahiptir:

1. **Düşünür** (Thought): "Kullanıcı ne istiyor?" diye düşünür
2. **Aksiyon alır** (Action): Bir araç/tool kullanır (örneğin haritadan veri çeker)
3. **Gözlemler** (Observation): Sonuçları inceler
4. **Cevap verir** (Answer): Kullanıcıya anlamlı bir cevap döner

Bu düşünce zincirine **ReAct Pattern** denir (Reasoning + Acting = Düşünme + Hareket Etme).

Örnek:
```
Sen: "Taksim'e en yakın 5 eczaneyi bul"

Agent'ın beyni:
  DÜŞÜNCE: Kullanıcı Taksim'e yakın eczane istiyor, 5 tane.
  AKSİYON: find_nearest aracını kullan (eczane, taksim, k=5)
  GÖZLEM: 5 eczane bulundu, en yakını 120m uzakta
  CEVAP: "Taksim'e en yakın 5 eczane bulundu. İşte harita:"
```

### 2.4 API Nedir?

API (Application Programming Interface) = İki yazılımın birbiriyle konuşması için kullanılan bir "ara yüz".

Örnekle anlatalım:
- Restoranda garson sana menü getirir, sen sipariş verirsin, garson mutfağa iletir, yemek gelir.
- Garson = API. Sen ile mutfak arasındaki iletişimi sağlar.

Bizim projede 2 API kullanıyoruz:
1. **AWS Bedrock API**: Claude yapay zekâsına sorularımızı gönderiyoruz, cevap alıyoruz
2. **Overpass API**: OpenStreetMap'ten harita verileri çekiyoruz (hastaneler nerede, parklar nerede vs.)

### 2.5 AWS Bedrock Nedir?

**AWS** = Amazon Web Services. Amazon'un bulut bilişim platformu.
**Bedrock** = AWS içinde yapay zekâ modellerini (Claude, Llama, vb.) kullanmanı sağlayan bir servis.

Neden direkt Claude API değil de AWS Bedrock kullanıyoruz?
- Çünkü AWS üzerinden erişim daha güvenli ve kurumsal
- AWS hesabımız vardı, Bedrock üzerinden Claude'a erişim açtık
- Bedrock, modeli bizim için barındırıyor (host ediyor), biz sadece istek atıyoruz

### 2.6 OpenStreetMap (OSM) Nedir?

Dünyanın en büyük **açık kaynak** harita veritabanı. Google Maps gibi ama herkes katkıda bulunabilir ve verileri ücretsiz kullanabilirsin.

İstanbul'daki her hastane, eczane, park, cami, okul... hepsi OSM'de kayıtlı. Biz bu veriye **Overpass API** üzerinden erişiyor ve projemizde kullanıyoruz.

### 2.7 GeoAI (Geospatial AI) Nedir?

Geo = Coğrafya, mekân
AI = Yapay Zekâ

GeoAI = Coğrafi verileri kullanan yapay zekâ uygulamaları. Bizim projede yapay zekâ, konum bazlı soruları anlayıp coğrafi veri üzerinde işlem yapıyor.

---

## BÖLÜM 3: Neden Bu Teknolojileri Seçtik?

### 3.1 Neden Claude (LLM olarak)?

| Alternatif | Neden Seçmedik |
|---|---|
| GPT-4 (OpenAI) | Pahalı, ayrıca API key almak gerekiyor |
| Llama (Meta) | Kendi sunucumuzda çalıştırmak gerekiyor, kaynak lazım |
| Gemini (Google) | Olabilirdi ama Bedrock entegrasyonu yoktu |
| **Claude (Anthropic)** | **AWS Bedrock üzerinden kolay erişim, Türkçe iyi anlıyor, JSON formatında cevap vermede başarılı** |

### 3.2 Neden AWS Bedrock?

- Önceden AWS hesabımız vardı
- Bedrock, model yönetimini senin için yapar (sunucu kurma derdi yok)
- Güvenli, ölçeklenebilir
- `boto3` (Python AWS kütüphanesi) ile 3-4 satırda bağlanabiliyorsun

### 3.3 Neden OpenStreetMap + Overpass API?

| Alternatif | Neden Seçmedik |
|---|---|
| Google Maps API | Ücretli (kredi kartı gerekiyor) |
| HERE Maps | Ücretli, karmaşık |
| **OpenStreetMap** | **Tamamen ücretsiz, zengin veri, Overpass API ile kolayca sorgulanabiliyor** |

### 3.4 Neden Streamlit (Web Arayüzü)?

| Alternatif | Neden Seçmedik |
|---|---|
| Flask/Django | Çok fazla kod yazmak gerekiyor, frontend ayrı |
| React/Next.js | Frontend framework bilmek gerekiyor |
| Gradio | ML projeleri için iyi ama harita desteği zayıf |
| **Streamlit** | **Python ile 1 dosyada hem backend hem frontend yazabiliyorsun. Harita, tablo, chat desteği var. Kolay.** |

### 3.5 Neden Folium (Harita Görselleştirme)?

| Alternatif | Neden Seçmedik |
|---|---|
| Matplotlib | Statik haritalar, interaktif değil |
| Plotly | Harita desteği var ama Folium kadar zengin değil |
| **Folium** | **İnteraktif haritalar, tıklanabilir marker'lar, katman değiştirme, zoom. Streamlit ile uyumlu.** |

### 3.6 Neden GeoPandas + Shapely?

- **GeoPandas**: Coğrafi verileri tablo gibi işle. Her satır bir yer (hastane, park vs.), her satırın bir geometrisi (koordinatı) var.
- **Shapely**: Nokta, çizgi, alan gibi geometrik şekillerle çalışmayı sağlar.

Bu ikisi coğrafi veri biliminin temel kütüphaneleri. Harita üzerindeki noktaları, mesafeleri, analizi bunlarla yapıyoruz.

### 3.7 Neden Scikit-learn (K-Means)?

K-Means bir kümeleme (clustering) algoritması. "Bu eczaneleri 3 gruba ayır, hangileri birbirine yakın?" gibi sorulara cevap verir. Scikit-learn Python'daki en popüler makine öğrenmesi kütüphanesi.

---

## BÖLÜM 4: Sistem Nasıl Çalışıyor? (Adım Adım)

### Senaryo: "Kadıköy'deki hastaneleri göster"

```
ADIM 1: Kullanıcı yazıyor
         "Kadıköy'deki hastaneleri göster"
              |
              v
ADIM 2: Agent (core.py) sorguyu alıyor
         Claude LLM'e gönderiyor: "Bu sorguyu analiz et"
              |
              v
ADIM 3: Claude JSON cevap dönüyor:
         {
           "thought": "Kullanıcı Kadıköy'deki hastaneleri istiyor",
           "actions": [{"tool": "query_osm", "params": {"poi_type": "hastane", "location": "kadıköy"}}],
           "answer_template": "Kadıköy'de {count} hastane bulundu."
         }
              |
              v
ADIM 4: Agent, Claude'un söylediği aracı (query_osm) çalıştırıyor
         - osm_client.py Overpass API'ye istek atıyor
         - İstanbul/Kadıköy bölgesindeki hastaneleri çekiyor
              |
              v
ADIM 5: Veriler GeoPandas DataFrame'e dönüştürülüyor
         (isim, enlem, boylam, tip, vb.)
              |
              v
ADIM 6: Folium haritası oluşturuluyor
         - Her hastane için haritaya işaret (marker) konuyor
         - Tıklanınca isim, adres, telefon görünüyor
              |
              v
ADIM 7: Streamlit ekranında gösteriliyor:
         - Cevap metni: "Kadıköy'de 8 hastane bulundu."
         - İnteraktif harita (zoom yapabilirsin)
         - Sonuç tablosu (isim, enlem, boylam)
         - Agent'ın düşünce süreci (ReAct log)
```

---

## BÖLÜM 5: Proje Yapısını Anla (Her Dosya/Klasör Ne İşe Yarar)

```
geo-chatbot/
│
├── app.py                    ← ANA DOSYA: Uygulamayı başlatır
│
├── agent/                    ← YAPAY ZEKÂ AJANI
│   ├── __init__.py           ← Python'a "bu bir paket" der (boş)
│   ├── core.py               ← Agent'ın beyni: düşünme, karar verme
│   ├── tools.py              ← Agent'ın araçları: her tool'u çalıştıran kod
│   └── prompts.py            ← Claude'a verilen talimatlar
│
├── geo/                      ← COĞRAFİ İŞLEMLER
│   ├── __init__.py           ← Python paket dosyası (boş)
│   ├── osm_client.py         ← OpenStreetMap'ten veri çekmek
│   ├── analysis.py           ← Mesafe hesaplama, kümeleme
│   └── visualize.py          ← Harita oluşturma (Folium)
│
├── data/                     ← VERİ KATMANI
│   ├── __init__.py
│   ├── sample_data.py        ← İnternet yoksa kullanılacak örnek veri
│   └── cache/                ← Daha önce çekilmiş verilerin önbelleği
│       └── *.json            ← Önbellek dosyaları
│
├── assets/                   ← GÖRSELLER
│   └── itu_logo.png          ← İTÜ logosu (sidebar'da görünüyor)
│
├── requirements.txt          ← Gerekli Python kütüphaneleri listesi
├── README.md                 ← Projenin teknik açıklaması (İngilizce)
├── MYZ305E-TP.pdf            ← Hocanın ödev metni
└── venv/                     ← Python sanal ortamı (kütüphaneler burada)
```

---

## BÖLÜM 6: Her Dosyanın Detaylı Açıklaması

### 6.1 `app.py` - Ana Uygulama Dosyası

**Ne yapar:** Streamlit web arayüzünü oluşturur. Kullanıcının gördüğü her şey buradan geliyor.

**İçerdiği şeyler:**
- Sayfa ayarları (başlık, ikon, layout)
- CSS stilleri (koyu tema, renkler, animasyonlar)
- Sidebar (sol panel): Öğrenci bilgileri, desteklenen araçlar, POI tipleri
- Chat arayüzü: Kullanıcı mesajı yazar, bot cevap verir
- Örnek sorgular: Tıklanınca otomatik çalışan butonlar
- Harita gösterimi: Folium haritasını ekrana gömer
- Sonuç tablosu: Bulunan yerlerin listesi
- Agent log: Düşünce sürecini gösteren panel
- İstatistikler: Toplam sorgu, bulunan sonuç sayısı

**Önemli satırlar:**
- `BEDROCK_REGION = "us-east-1"` → AWS'nin hangi bölgesini kullandığımız
- `BEDROCK_MODEL = "us.anthropic.claude-sonnet-4-6"` → Hangi Claude modeli
- `GeoAgent(...)` → Agent'ı başlatır
- `agent.process_query(user_input)` → Kullanıcının sorgusunu işleme sokar

### 6.2 `agent/core.py` - Agent'ın Beyni

**Ne yapar:** ReAct döngüsünü yönetir. Kullanıcı sorgusu gelir → Claude'a sorar → Hangi aracı kullanacağına karar verir → Aracı çalıştırır → Sonucu döner.

**Sınıf: `GeoAgent`**
- `__init__`: AWS Bedrock bağlantısını kurar
- `_call_llm`: Claude'a mesaj gönderir, cevap alır
- `_parse_llm_response`: Claude'un JSON cevabını ayrıştırır
- `process_query`: ANA METOD - tüm akışı yönetir
- `_merge_results`: Birden fazla araç sonucunu birleştirir
- `_fallback_process`: Claude cevap veremezse (internet yok, hata, vs.) basit kural tabanlı işlem yapar

**Fallback (Yedek) Mekanizma:**
Eğer Claude'a erişim olmazsa, sistem basit metin analizi yapar:
- "yakın" kelimesi varsa → `find_nearest` tool
- "küme" kelimesi varsa → `cluster_points` tool
- Yoksa → `query_osm` tool

### 6.3 `agent/prompts.py` - Claude'a Verilen Talimatlar

**Ne yapar:** Claude'un nasıl davranacağını belirleyen "sistem prompt'u" burada.

**SYSTEM_PROMPT** içeriği (özetleyerek):
- "Sen İstanbul coğrafyası konusunda uzman bir GeoAI asistanısın"
- "Şu araçların var: query_osm, calculate_distance, find_nearest, cluster_points, generate_map, get_statistics"
- "Her sorgu için şöyle düşün: Thought → Action → Observation → Answer"
- "Cevabını JSON formatında ver"
- Örnek sorgular ve beklenen JSON çıktıları

**PARSE_PROMPT**: Kullanıcı sorgusunu Claude'a gönderirken kullanılan şablon.

### 6.4 `agent/tools.py` - Agent'ın Araçları

**Ne yapar:** Claude "şu aracı kullan" dediğinde, o aracı gerçekten çalıştıran kod burada.

**6 Araç (Tool):**

| Araç | Ne Yapar |
|------|----------|
| `query_osm` | Belirli bölgede belirli tip yerleri arar (örnek: Kadıköy'deki hastaneler) |
| `calculate_distance` | İki nokta arasındaki mesafeyi hesaplar (kuş uçuşu) |
| `find_nearest` | Bir noktaya en yakın K yeri bulur |
| `cluster_points` | Yerleri K-Means ile gruplara ayırır |
| `generate_map` | İnteraktif harita oluşturur |
| `get_statistics` | Bulunan yerlerle ilgili istatistik verir |

### 6.5 `geo/osm_client.py` - OpenStreetMap Veri İstemcisi

**Ne yapar:** Overpass API'ye sorgu göndererek gerçek dünyadan coğrafi veri çeker.

**İçerdiği önemli şeyler:**

1. **DISTRICT_COORDS**: İstanbul ilçelerinin koordinatları (enlem/boylam)
   - Örnek: `"kadıköy": (29.0259, 40.9927)`
   - Kullanıcı "Kadıköy" dediğinde nereye bakacağını buradan biliyor

2. **POI_TAG_MAP**: Her yer tipinin OSM'deki etiketi
   - "hastane" → `{"amenity": "hospital"}`
   - "park" → `{"leisure": "park"}`
   - "cami" → `{"amenity": "place_of_worship", "religion": "muslim"}`

3. **Overpass Query Builder**: OSM'ye uygun formatta sorgu oluşturur
   - "Kadıköy merkezinden 3km içinde, amenity=hospital olan tüm node'ları ver"

4. **Cache (Önbellek)**: Aynı sorguyu tekrar tekrar atmamak için sonuçları kaydeder
   - Böylece hızlı çalışır ve API'yi gereksiz yormaz

### 6.6 `geo/analysis.py` - Mekânsal Analiz

**Ne yapar:** Coğrafi hesaplamalar ve makine öğrenmesi işlemleri.

**Fonksiyonlar:**

1. **`haversine_distance(lat1, lon1, lat2, lon2)`**
   - Dünya üzerinde iki nokta arasındaki gerçek mesafeyi hesaplar
   - Dünya yuvarlak olduğu için düz çizgi değil, kürenin üzerindeki mesafe hesabı yapar
   - Formül: Haversine formülü (çok eski bir matematik formülü)

2. **`find_nearest(target_lat, target_lon, gdf, k)`**
   - Hedef noktaya en yakın K tane yeri bulur
   - Her yere olan mesafeyi hesaplar, en yakın K tanesini döner

3. **`cluster_points(gdf, n_clusters)`**
   - K-Means algoritması ile yerleri küme gruplarına ayırır
   - Örnek: 20 eczaneyi 3 gruba ayır → Hangileri birbirine yakın görürsün

4. **`get_statistics(gdf)`**
   - Kaç yer bulundu, ortalama mesafe, min/max mesafe gibi bilgiler

### 6.7 `geo/visualize.py` - Harita Görselleştirme

**Ne yapar:** Folium kütüphanesi ile interaktif haritalar oluşturur.

**Özellikleri:**
- 3 farklı harita katmanı (açık, koyu, normal) arasında geçiş
- Her yer tipi için farklı ikon ve renk (hastane=kırmızı, park=yeşil, vb.)
- Kümeleme sonuçlarında her küme farklı renkte
- Tıklanabilir popup'lar (isim, adres, telefon, web sitesi)
- "En yakın" sorgularında hedef noktadan yerlere kesikli çizgiler
- 50'den fazla sonuç varsa otomatik marker kümeleme (MarkerCluster)

### 6.8 `data/sample_data.py` - Örnek Veri (Offline Mod)

**Ne yapar:** İnternet bağlantısı yoksa veya Overpass API cevap vermezse, önceden hazırlanmış örnek verilerle çalışır. Böylece demo sırasında internet olmasa bile uygulama çalışır.

**İçerdiği veriler:**
- Kadıköy'deki hastaneler (8 adet)
- Taksim'deki eczaneler (10 adet)
- Beşiktaş'taki parklar (8 adet)
- Fatih'teki camiler (10 adet)
- Şişli'deki okullar (8 adet)
- Beyoğlu'ndaki restoranlar (8 adet)
- Sultanahmet'teki müzeler (6 adet)
- Kadıköy'deki kafeler (8 adet)

### 6.9 `requirements.txt` - Bağımlılık Listesi

```
streamlit        → Web arayüzü framework'ü
boto3            → AWS ile iletişim (Bedrock için)
geopandas        → Coğrafi veri işleme
folium           → İnteraktif harita
streamlit-folium → Folium haritalarını Streamlit'e gömmek
shapely          → Geometrik işlemler (nokta, alan, vb.)
scikit-learn     → Makine öğrenmesi (K-Means kümeleme)
requests         → HTTP istekleri (Overpass API'ye bağlanmak)
pandas           → Veri tabloları
numpy            → Matematiksel işlemler
branca           → Harita renk skalası
```

---

## BÖLÜM 7: Hocanın Kriterlerine Göre Projemizin Açıklaması

### 7.1 AI Agent Architecture & Functionality (%40)

**Ne yaptık:**
- ReAct (Reasoning + Acting) pattern'ini uygulayan bir agent
- Claude LLM ile düşünme yeteneğine sahip
- 6 farklı araç (tool) kullanabiliyor
- Otonom çalışıyor: Sen soru soruyorsun, o hangi aracı kullanacağına kendi karar veriyor
- Fallback mekanizması: LLM erişimi yoksa bile çalışıyor

**Neden önemli:**
- Agent sadece cevap üretmiyor, **karar** da veriyor
- Hangi aracın ne zaman kullanılacağını **kendisi** belirliyor
- Bu onu basit bir chatbot'tan ayıran şey

### 7.2 Geospatial Analysis & Problem Solving (%30)

**Coğrafi veri kaynağı:** OpenStreetMap (gerçek, güncel, açık kaynak)

**Yapılan analizler:**
- POI (Point of Interest) sorgulama
- Haversine mesafe hesabı (küre üzerinde gerçek mesafe)
- K-Means kümeleme (mekânsal gruplama)
- En yakın K noktayı bulma (KNN benzeri)
- İstatistiksel analiz (min, max, ortalama mesafe)

**İstanbul'a odaklanma:**
- 25+ ilçe/semt koordinatları tanımlı
- Türkçe ve İngilizce yer tipi desteği
- Türkçe doğal dil işleme

### 7.3 Presentation & Demo Video (%15)

- Uygulama canlı çalışır halde gösterilebilir
- `streamlit run app.py` ile başlatılır
- Örnek sorgular tıklanabilir
- Agent'ın düşünce süreci görülebilir (şeffaflık)

### 7.4 Poster Design & Narrative (%15)

Poster için önemli noktalar:
- Sistem mimarisi diyagramı (User → Agent → Tools → Map)
- Örnek sorguların görsel çıktıları (harita screenshot'ları)
- Teknoloji yığını (Tech Stack) şematikçesi
- ReAct döngüsünün görsel açıklaması

---

## BÖLÜM 8: Sistem Mimarisi (Büyük Resim Şeması)

```
┌─────────────────────────────────────────────────────────────────────┐
│                         KULLANICI                                     │
│                  "Kadıköy'deki hastaneleri göster"                    │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 v
┌─────────────────────────────────────────────────────────────────────┐
│                    STREAMLIT WEB ARAYÜZÜ (app.py)                    │
│   - Chat arayüzü                                                     │
│   - Harita gösterimi                                                 │
│   - Sonuç tablosu                                                    │
│   - Agent log paneli                                                 │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 v
┌─────────────────────────────────────────────────────────────────────┐
│                    AI AGENT (agent/core.py)                           │
│                                                                      │
│   ┌──────────┐    ┌──────────┐    ┌────────────┐    ┌──────────┐   │
│   │ DÜŞÜNME  │ -> │ AKSİYON  │ -> │   GÖZLEM   │ -> │  CEVAP   │   │
│   │ (Thought)│    │ (Action) │    │(Observation)│    │ (Answer) │   │
│   └──────────┘    └──────────┘    └────────────┘    └──────────┘   │
│        |                |                                            │
│        v                v                                            │
│   Claude LLM      Tool Execution                                     │
│   (AWS Bedrock)   (agent/tools.py)                                   │
└────────┬───────────────┬────────────────────────────────────────────┘
         │               │
         v               v
┌────────────────┐  ┌────────────────────────────────────────────────┐
│  AWS BEDROCK   │  │           ARAÇLAR (TOOLS)                       │
│                │  │                                                  │
│  Claude LLM    │  │  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  Modeli        │  │  │query_osm │  │find_near │  │ cluster  │     │
│                │  │  └─────┬────┘  └─────┬────┘  └─────┬────┘     │
│  Sorguyu       │  │        │             │             │           │
│  anlar,        │  │        v             v             v           │
│  JSON üretir   │  │  ┌─────────────────────────────────────┐      │
└────────────────┘  │  │    geo/osm_client.py                 │      │
                    │  │    (Overpass API'den veri çekme)      │      │
                    │  └───────────────┬─────────────────────┘      │
                    │                  │                              │
                    │                  v                              │
                    │  ┌─────────────────────────────────────┐      │
                    │  │    geo/analysis.py                    │      │
                    │  │    (Mesafe, kümeleme, istatistik)     │      │
                    │  └───────────────┬─────────────────────┘      │
                    │                  │                              │
                    │                  v                              │
                    │  ┌─────────────────────────────────────┐      │
                    │  │    geo/visualize.py                   │      │
                    │  │    (Folium harita oluşturma)          │      │
                    │  └─────────────────────────────────────┘      │
                    └────────────────────────────────────────────────┘
                                       │
                                       v
                    ┌────────────────────────────────────────────────┐
                    │              OPENSTREETMAP                      │
                    │         (Overpass API - Gerçek Veri)            │
                    │                                                 │
                    │   İstanbul'daki tüm hastaneler, eczaneler,      │
                    │   parklar, okullar, camiler, müzeler...         │
                    └────────────────────────────────────────────────┘
```

---

## BÖLÜM 9: Kullanılan Teknoloji Yığını (Tech Stack)

| Katman | Teknoloji | Görev |
|--------|-----------|-------|
| Yapay Zekâ | Claude (Anthropic) via AWS Bedrock | Doğal dil anlama, karar verme |
| Agent Framework | Özel (kendi yazdık) | ReAct döngüsü, tool yönetimi |
| Web Arayüzü | Streamlit | Kullanıcı arayüzü |
| Coğrafi Veri | OpenStreetMap + Overpass API | Gerçek dünya verileri |
| Veri İşleme | GeoPandas + Pandas | Tablo ve coğrafi veri |
| Harita | Folium + Branca | İnteraktif harita görselleştirme |
| Mekânsal Analiz | Shapely + NumPy | Geometri ve matematik |
| Makine Öğrenmesi | Scikit-learn (K-Means) | Kümeleme analizi |
| Bulut | AWS (Bedrock) | LLM hosting |
| Programlama Dili | Python 3.11+ | Her şey Python |

---

## BÖLÜM 10: Sık Sorulan Sorular (FAQ)

### "Bu projede makine öğrenmesi var mı?"
Evet! K-Means kümeleme algoritması bir unsupervised (denetimsiz) makine öğrenmesi yöntemidir. Örneğin "Kadıköy'deki kafeleri kümele" dediğinde, kafeler konum benzerliğine göre otomatik gruplara ayrılıyor.

### "Agent'ın farkı ne? Normal chatbot da bunu yapar?"
Normal chatbot sadece metin üretir. Bizim agent:
1. Düşünür (hangi aracı kullanmalı?)
2. Araç çalıştırır (gerçek veri çeker)
3. Sonucu analiz eder
4. Kullanıcıya sunar
Bu otonom karar verme yeteneğini basit bir chatbot'ta bulamazsın.

### "İnternet olmadan çalışıyor mu?"
Kısmi olarak evet. Claude'a erişilemezse fallback (yedek) mekanizma devreye giriyor. OSM'ye erişilemezse sample_data.py'deki örnek veriler kullanılıyor.

### "Neden sadece İstanbul?"
Çünkü projeyi odaklı tutmak istedik. İlçe koordinatları, Türkçe yer isimleri, spesifik POI verileri hep İstanbul için hazır. Ama sistem mimarisi herhangi bir şehre uyarlanabilir.

### "Veri ne kadar güncel?"
OpenStreetMap sürekli güncelleniyor (gönüllüler tarafından). Her sorguda canlı veri çekilir. Cache (önbellek) sayesinde aynı sorgu tekrar gelirse hızlı cevap verilir.

### "Bu projeyi çalıştırmak için ne gerekiyor?"
1. Python 3.11+ yüklü bir bilgisayar
2. AWS hesabı (Bedrock erişimi açık)
3. `pip install -r requirements.txt`
4. `streamlit run app.py`

---

## BÖLÜM 11: Önemli Terimler Sözlüğü

| Terim | Açıklama |
|-------|----------|
| **AI Agent** | Otonom karar verebilen yapay zekâ sistemi |
| **LLM** | Large Language Model - Büyük Dil Modeli (örnek: Claude, ChatGPT) |
| **ReAct** | Reasoning + Acting - Düşün ve Hareket Et deseni |
| **API** | Yazılımlar arası iletişim arayüzü |
| **AWS Bedrock** | Amazon'un yapay zekâ model barındırma servisi |
| **OpenStreetMap** | Açık kaynak dünya haritası |
| **Overpass API** | OSM verilerine erişim sağlayan sorgu servisi |
| **POI** | Point of Interest - İlgi Noktası (hastane, park, vb.) |
| **GeoDataFrame** | Coğrafi bilgi içeren veri tablosu |
| **Haversine** | Küre üzerinde iki nokta arası mesafe formülü |
| **K-Means** | Veri noktalarını K gruba ayıran kümeleme algoritması |
| **Folium** | Python ile interaktif web haritası kütüphanesi |
| **Streamlit** | Python ile hızlı web uygulaması oluşturma aracı |
| **JSON** | JavaScript Object Notation - veri değişim formatı |
| **Cache** | Önbellek - Aynı isteğin tekrar atılmasını önler |
| **Fallback** | Yedek plan - Ana sistem çalışmayınca devreye giren B planı |
| **boto3** | Python için AWS SDK (AWS ile konuşmak için kütüphane) |
| **Tool/Araç** | Agent'ın kullandığı işlem birimi (query_osm, find_nearest, vb.) |
| **Prompt** | Yapay zekâya verilen talimat/soru |
| **Token** | LLM'in metni işleme birimi (yaklaşık bir kelime = 1-2 token) |
| **Clustering** | Kümeleme - benzer verileri gruplama |
| **Marker** | Harita üzerindeki işaret noktası |

---

## BÖLÜM 12: Projeyi Sunarken Söyleyebileceğin Şeyler

### Giriş (1-2 dakika):
"Bu projede İstanbul için bir GeoAI ChatBot geliştirdik. Kullanıcı doğal dilde soru sorabiliyor - örneğin 'Kadıköy'deki hastaneleri göster' - ve sistem yapay zekâ agent'ı kullanarak sorguyu anlıyor, OpenStreetMap'ten gerçek verileri çekiyor ve haritada gösteriyor."

### Teknik Açıklama (2-3 dakika):
"Sistemin kalbi bir ReAct Agent. ReAct, Reasoning plus Acting demek. Agent önce düşünüyor - ne isteniyor, hangi aracı kullanmalıyım diye. Sonra aksiyon alıyor - mesela Overpass API'ye sorgu atıyor. Sonra sonucu gözlemliyor ve kullanıcıya cevap veriyor. Beyni olarak AWS Bedrock üzerinden Claude LLM kullanıyoruz."

### Demo (2-3 dakika):
"Şimdi canlı göstereyim. Mesela 'Taksim'e en yakın 5 eczane' yazıyorum. Agent düşünce sürecini görebilirsiniz - find_nearest aracını seçtiği, Taksim koordinatlarını kullandığı, 5 eczane bulduğu görülüyor. Haritada kırmızı yıldız hedef noktayı, mavi işaretler eczaneleri gösteriyor. Kesikli çizgiler mesafeyi gösteriyor."

---

*Bu doküman, projenin her yönünü teknik bilgisi olmayan birine anlatmak için hazırlanmıştır. Soruların için Abtin'e danışabilirsin.*
