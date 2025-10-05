# src/agent/orchestrator.py
from __future__ import annotations

from typing import Any, Dict, List, Optional

from src.core.settings import Settings
from src.agent.graph import build_graph

try:
    from src.agent.llm import LLM  # tu implementación real con .instance_llm()
except Exception:
    LLM = None


def _make_llm() -> Any:
    if LLM and hasattr(LLM, "instance_llm"):
        return LLM.instance_llm()
    class _Dummy:
        def invoke(self, _): return {"text": "dummy-llm"}
    return _Dummy()


def _make_mcp_client() -> Any:
    try:
        from src.agent.mcp_client import MCPClient
    except Exception as e:
        raise RuntimeError(
            "No se pudo importar MCPClient desde src.agent.mcp_client. "
            "Incluye un cliente con: async def call_tool(name, payload)."
        ) from e

    host = Settings().mcp_host
    client = MCPClient()
    if hasattr(client, "host"):
        client.host = host
    elif hasattr(client, "configure"):
        client.configure(base_url=host)
    return client


async def run_orchestration(
    zones: List[Dict[str, Any]],
    filters: Optional[Dict[str, Any]] = None,
    objectives: Optional[List[str]] = None,
) -> Dict[str, Any]:
    llm = _make_llm()
    mcp_client = _make_mcp_client()

    graph = build_graph(llm=llm, mcp_client=mcp_client)

    initial_state: Dict[str, Any] = {
        "zones": zones or [],
        "llm": llm,
        "mcp_client": mcp_client,
        "context": {
            "filters": filters or {},
            "objectives": objectives or [],
        },
        "raw_data": None,
        "processed": None,
        "results": {},
        "errors": [],
    }

# ... dentro de run_orchestration(), al final:
    final_state: Dict[str, Any] = await graph.ainvoke(initial_state)

    model_outputs = final_state.get("model_outputs") or {}
    return {
        "summary": final_state.get("summary"),
        "map_json": final_state.get("map_json"),
        "outputs": model_outputs,          # <- lo que ya usabas
        "model_outputs": model_outputs,    # <- alias para compatibilidad
        "errors": final_state.get("errors", []),
    }

