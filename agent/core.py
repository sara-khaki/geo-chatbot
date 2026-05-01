import json
import re
import boto3
from datetime import datetime

from agent.prompts import SYSTEM_PROMPT, PARSE_PROMPT
from agent.tools import execute_tool, TOOL_DESCRIPTIONS


class GeoAgent:
    def __init__(self, region_name="us-east-1", model_id="us.anthropic.claude-sonnet-4-6"):
        self.bedrock = boto3.client("bedrock-runtime", region_name=region_name)
        self.model_id = model_id
        self.logs = []
        self.conversation_history = []

    def _log(self, step: str, content: str):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "step": step,
            "content": content,
        }
        self.logs.append(entry)

    def get_logs(self) -> list:
        return self.logs

    def clear_logs(self):
        self.logs = []

    def _call_llm(self, messages: list) -> str:
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 2048,
            "temperature": 0.1,
            "system": SYSTEM_PROMPT,
            "messages": messages,
        }

        response = self.bedrock.invoke_model(
            modelId=self.model_id,
            body=json.dumps(body),
            contentType="application/json",
        )

        result = json.loads(response["body"].read())
        return result["content"][0]["text"]

    def _parse_llm_response(self, response_text: str) -> dict:
        json_match = re.search(r"\{[\s\S]*\}", response_text)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass

        return {
            "thought": response_text,
            "actions": [],
            "answer_template": response_text,
        }

    def process_query(self, user_query: str) -> dict:
        self.clear_logs()
        self._log("USER_QUERY", user_query)

        self._log("THOUGHT", "Kullanıcı sorgusunu analiz ediyorum...")

        messages = [
            {"role": "user", "content": PARSE_PROMPT.format(query=user_query)},
        ]

        try:
            llm_response = self._call_llm(messages)
            self._log("LLM_RESPONSE", llm_response)
        except Exception as e:
            self._log("ERROR", f"LLM çağrısı başarısız: {str(e)}")
            return self._fallback_process(user_query)

        parsed = self._parse_llm_response(llm_response)
        thought = parsed.get("thought", "")
        actions = parsed.get("actions", [])
        answer_template = parsed.get("answer_template", "")

        self._log("THOUGHT", thought)

        if not actions:
            self._log("FALLBACK", "LLM aksiyon üretemedi, fallback kullanılıyor.")
            return self._fallback_process(user_query)

        results = []
        for action in actions:
            tool_name = action.get("tool", "")
            params = action.get("params", {})

            self._log("ACTION", f"Tool: {tool_name}, Params: {json.dumps(params, ensure_ascii=False)}")

            result = execute_tool(tool_name, params)

            if "error" in result:
                self._log("ERROR", f"Tool hatası: {result['error']}")
            else:
                obs_msg = f"Başarılı. "
                if "count" in result:
                    obs_msg += f"{result['count']} sonuç bulundu."
                self._log("OBSERVATION", obs_msg)

            results.append(result)

        final_result = self._merge_results(results, answer_template, thought)
        self._log("ANSWER", final_result.get("answer", ""))

        return final_result

    def _merge_results(self, results: list, answer_template: str, thought: str) -> dict:
        merged = {
            "thought": thought,
            "answer": "",
            "gdf": None,
            "map": None,
            "stats": None,
            "logs": self.logs,
        }

        for result in results:
            if "gdf" in result and result["gdf"] is not None:
                merged["gdf"] = result["gdf"]
            if "map" in result:
                merged["map"] = result["map"]
            if "stats" in result:
                merged["stats"] = result["stats"]

        count = 0
        if merged["gdf"] is not None:
            count = len(merged["gdf"])

        n_clusters = 0
        for result in results:
            if "n_clusters" in result:
                n_clusters = result["n_clusters"]

        try:
            answer = answer_template.format(
                count=count,
                n_clusters=n_clusters,
                results="sonuçlar",
            )
        except (KeyError, IndexError):
            answer = answer_template

        if count > 0:
            answer += f"\n\nToplam {count} sonuç bulundu."
        elif count == 0 and not any("error" in r for r in results):
            answer = "Bu sorgu için sonuç bulunamadı. Lütfen farklı bir bölge veya yer tipi deneyin."

        merged["answer"] = answer
        return merged

    def _fallback_process(self, query: str) -> dict:
        self._log("FALLBACK", "Fallback mekanizması devreye girdi.")

        query_lower = query.lower()

        poi_types = [
            "hastane", "hospital", "eczane", "pharmacy", "park", "okul", "school",
            "restoran", "restaurant", "kafe", "cafe", "cami", "mosque", "müze",
            "museum", "otel", "hotel", "banka", "bank", "market", "supermarket",
            "kütüphane", "library", "üniversite", "university", "atm", "benzin",
            "otopark", "parking", "metro", "durak", "otobüs",
        ]

        from geo.osm_client import _ALL_LOCATIONS, get_district_coords

        found_poi = None
        for poi in poi_types:
            if poi in query_lower:
                found_poi = poi
                break

        # Strategy for finding location in the query:
        # 1. Check all known location names (districts + neighborhoods)
        # 2. Extract candidate location words and try geocoding
        found_location = None

        # First, check all known locations (longest match first to prefer
        # "kadıköy çarşı" over "kadıköy")
        sorted_locations = sorted(_ALL_LOCATIONS.keys(), key=len, reverse=True)
        for loc_name in sorted_locations:
            if loc_name in query_lower:
                found_location = loc_name
                break

        # If no known location matched, try to extract location from the query
        # by removing known POI words and common Turkish grammar words
        if found_location is None:
            stop_words = {
                "deki", "daki", "deki", "daki", "taki", "teki",
                "deli", "dali",
                "göster", "goster", "bul", "listele", "haritada",
                "en", "yakın", "yakin", "kaç", "kac", "tane",
                "küme", "kume", "grupla", "kümele", "kumele",
                "mesafe", "uzaklık", "uzaklik", "istatistik",
                "nerede", "neredeki", "var", "olan",
                "ile", "arası", "arasi", "arasındaki", "arasindaki",
            }
            stop_words.update(poi_types)

            # Split query into words, remove stop words and POI types
            words = re.split(r"[\s''`]+", query_lower)
            candidate_words = [w.strip(",.?!") for w in words if w.strip(",.?!") and w.strip(",.?!") not in stop_words]

            # Try each candidate word and multi-word combinations as locations
            for word in candidate_words:
                coords = get_district_coords(word)
                if coords:
                    found_location = word
                    break

        is_nearest = any(w in query_lower for w in ["yakın", "nearest", "en yakın", "closest"])
        is_cluster = any(w in query_lower for w in ["küme", "cluster", "grupla", "kümele"])
        is_distance = any(w in query_lower for w in ["mesafe", "uzaklık", "distance", "kaç km", "kaç metre"])
        is_stats = any(w in query_lower for w in ["istatistik", "statistics", "kaç tane", "sayı"])

        k_match = re.search(r"(\d+)", query)
        k_val = int(k_match.group(1)) if k_match else 5

        if found_poi is None:
            return {
                "thought": "Sorgudan yer tipi çıkarılamadı.",
                "answer": "Lütfen aramak istediğiniz yer tipini belirtin (hastane, eczane, park, okul, restoran, vb.)",
                "gdf": None,
                "map": None,
                "stats": None,
                "logs": self.logs,
            }

        if is_nearest:
            self._log("ACTION", f"find_nearest tool'u çağrılıyor: {found_poi}, {found_location}, k={k_val}")
            result = execute_tool("find_nearest", {
                "poi_type": found_poi,
                "location": found_location,
                "k": k_val,
            })
        elif is_cluster:
            n = k_val if k_val <= 10 else 3
            self._log("ACTION", f"cluster_points tool'u çağrılıyor: {found_poi}, {found_location}, n={n}")
            result = execute_tool("cluster_points", {
                "poi_type": found_poi,
                "location": found_location,
                "n_clusters": n,
            })
        elif is_stats:
            self._log("ACTION", f"get_statistics tool'u çağrılıyor: {found_poi}, {found_location}")
            result = execute_tool("get_statistics", {
                "poi_type": found_poi,
                "location": found_location,
            })
        else:
            self._log("ACTION", f"query_osm tool'u çağrılıyor: {found_poi}, {found_location}")
            result = execute_tool("query_osm", {
                "poi_type": found_poi,
                "location": found_location,
            })

        if "error" in result:
            self._log("ERROR", result["error"])

        count = result.get("count", 0)
        loc_str = found_location or "İstanbul"

        if is_nearest:
            answer = f"{loc_str} bölgesine en yakın {k_val} {found_poi} bulundu."
        elif is_cluster:
            n = result.get("n_clusters", 3)
            answer = f"{loc_str} bölgesindeki {found_poi} noktaları {n} kümeye ayrıldı."
        else:
            answer = f"{loc_str} bölgesinde {count} adet {found_poi} bulundu."

        self._log("OBSERVATION", f"{count} sonuç elde edildi.")
        self._log("ANSWER", answer)

        return {
            "thought": f"Kullanıcı {loc_str} bölgesindeki {found_poi} hakkında bilgi istiyor.",
            "answer": answer,
            "gdf": result.get("gdf"),
            "map": result.get("map"),
            "stats": result.get("stats"),
            "logs": self.logs,
        }
