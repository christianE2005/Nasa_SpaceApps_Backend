from __future__ import annotations

from typing import Any, Awaitable, Callable, Dict, List, TypedDict

# Firma que LangGraph inyecta a tus nodos async: emit(channel, payload)
Emit = Callable[[str, Any], Awaitable[None]]


class OrchestratorState(TypedDict, total=False):
    # Entradas
    zones: List[Dict[str, Any]]               # [{"id": "...", "lat": ..., "lon": ..., "geometry": {...}}, ...]
    mcp_client: Any                            # Cliente MCP con .call_tool(name, payload)
    context: Dict[str, Any]                    # {"filters": {...}, "objectives": [...]}

    # Producción intermedia
    model_outputs: Dict[str, Any]              # id_zona -> {"infra": ..., "inequality": ...}
    map_json: Dict[str, Any]                   # GeoJSON FeatureCollection
    summary: str                               # Resumen del análisis LLM

    # Errores
    errors: List[Dict[str, str]]               # [{"node": "run_models", "message": "..."}]
