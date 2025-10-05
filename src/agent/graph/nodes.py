from __future__ import annotations

import json
import jsonpatch
from typing import Any, Dict

from .state import OrchestratorState, Emit
from src.services.context_builder import ContextBuilder, meters_to_deg
from src.agent.llm import LLM


# ---------- Utilidades ----------
def square_from_point(lat: float, lon: float, size_m: float = 50.0) -> Dict[str, Any]:
    dlat, dlon = meters_to_deg(lat, size_m)
    coords = [
        (lon - dlon, lat - dlat),
        (lon + dlon, lat - dlat),
        (lon + dlon, lat + dlat),
        (lon - dlon, lat + dlat),
        (lon - dlon, lat - dlat),
    ]
    return {"type": "Polygon", "coordinates": [coords]}


def _to_dict(x: Any) -> Dict[str, Any]:
    if x is None:
        return {}
    if isinstance(x, dict):
        return x
    if hasattr(x, "dict"):
        try:
            return x.dict()
        except Exception:
            pass
    if hasattr(x, "model_dump"):
        try:
            return x.model_dump()
        except Exception:
            pass
    if isinstance(x, str):
        try:
            return json.loads(x)
        except Exception:
            return {"value": x}
    return {"value": x}


# ---------- NODO 1: fetch_data ----------
async def fetch_data_node(state: OrchestratorState, emit: Emit) -> OrchestratorState:
    """Inicializa estructuras necesarias antes de correr modelos."""
    await emit("step", {"node": "fetch_data"})
    state.setdefault("model_outputs", {})
    state.setdefault("map_json", {"type": "FeatureCollection", "features": []})
    return state


# ---------- NODO 2: run_models ----------
async def run_models_node(state: OrchestratorState, emit: Emit) -> OrchestratorState:
    await emit("step", {"node": "run_models"})
    mcp = state["mcp_client"]
    zones = state.get("zones", []) or []
    outputs = state.setdefault("model_outputs", {})
    feature_collection = state.setdefault("map_json", {"type": "FeatureCollection", "features": []})

    # DSN desde settings (sync si existe, si no async dsn)
    from src.core.settings import Settings
    _settings = Settings()
    dsn = getattr(_settings, "database_url_sync", None) or _settings.database_url
    ctx_builder = ContextBuilder(dsn=dsn)

    for z in zones:
        lat = float(z.get("lat"))
        lon = float(z.get("lon"))
        geometry = z.get("geometry")  # GeoJSON original

        # (1) Construye payloads completos (async en el builder)
        pop_payload = await ctx_builder.build_population_payload(geometry, lat, lon)
        ineq_payload = await ctx_builder.build_inequality_payload(geometry, lat, lon)

        # (2) Llama herramientas MCP
        infra_raw = await mcp.call_tool("City Infrastructure Model", pop_payload)
        ineq_raw = await mcp.call_tool("Population Inequality Model", ineq_payload)

        infra = _to_dict(infra_raw)
        ineq = _to_dict(ineq_raw)

        outputs[z["id"]] = {"infra": infra, "inequality": ineq}
        await emit("partial", {"zone": z["id"], "infra": infra, "inequality": ineq})

        patches = []

        # (3) Si inequality devuelve una construcción puntual (lat, lon, construction), crea polígono
        if all(k in ineq for k in ("lat", "lon", "construction")):
            try:
                poly = square_from_point(float(ineq["lat"]), float(ineq["lon"]), size_m=80.0)
                feature = {
                    "type": "Feature",
                    "properties": {
                        "use": str(ineq["construction"]).lower(),  # "park" | "school"
                        "source": "Population Inequality Model",
                        "zone_id": z["id"],
                    },
                    "geometry": poly,
                }
                patches.append({"op": "add", "path": "/features/-", "value": feature})
            except Exception as e:
                # Si hay tipo no convertible, ignora esta parte pero no detiene el flujo
                pass

        # (4) Si infraestructura devuelve Features en suggestions, agrégalas directamente
        for f in infra.get("suggestions", []):
            if isinstance(f, dict) and f.get("type") == "Feature":
                patches.append({"op": "add", "path": "/features/-", "value": f})

        if patches:
            await emit("map_patch", {"patch": patches})
            jsonpatch.apply_patch(feature_collection, patches, in_place=True)

    state["map_json"] = feature_collection
    return state


# ---------- NODO 3: analyze_results ----------
async def analyze_results_node(state: OrchestratorState, emit: Emit) -> OrchestratorState:
    """Usa el LLM para sintetizar prioridades/acciones a partir de model_outputs."""
    await emit("step", {"node": "analyze_results"})
    filters = (state.get("context") or {}).get("filters", {})
    objectives = (state.get("context") or {}).get("objectives", [])
    question = LLM.build_question(state.get("model_outputs", {}), filters, objectives)
    planner = LLM.planner_chain()

    res = await planner.ainvoke({"question": question})
    # Extrae contenido robustamente (AIMessage, dict, str)
    summary = getattr(res, "content", None) or (res.get("text") if isinstance(res, dict) else None) or str(res)
    state["summary"] = summary
    await emit("partial", {"node": "analyze_results", "summary": summary})
    return state


# ---------- NODO 4: finalize ----------
async def finalize_node(state: OrchestratorState, emit: Emit) -> OrchestratorState:
    await emit("step", {"node": "finalize"})
    return state
