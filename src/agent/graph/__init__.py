# src/agent/graph/__init__.py
from __future__ import annotations

from typing import Any, Dict, List, Optional, Callable
from langchain_core.runnables import RunnableLambda
from langgraph.graph import StateGraph, END
import time

State = Dict[str, Any]

# =========================
# Funciones "plug-in" (ajusta a tu lógica real)
# =========================

def your_fetch_fn(
    zones: List[Dict[str, Any]],
    filters: Optional[Dict[str, Any]],
    mcp_client: Any,
) -> List[Dict[str, Any]]:
    # TODO: Reemplaza con tu fetch real (DB/APIs/MCP).
    # Ej.: results = await mcp_client.call_tool("Get Infra Context", {"zones": zones, "filters": filters})
    # return results.get("data", [])
    return zones if zones else []


def your_preprocess_fn(raw: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return raw


def your_model_infer_fn(
    preprocessed: List[Dict[str, Any]],
    objectives: List[str],
    llm: Any,
) -> Dict[str, Any]:
    # TODO: Reemplaza con tu inferencia real (modelo FastAPI/ECS/LLM).
    return {
        "summary": {"count": len(preprocessed), "objectives": objectives},
        "recommendations": [{"idx": i, "action": "placeholder"} for i, _ in enumerate(preprocessed)],
    }


def your_postprocess_fn(model_out: Dict[str, Any]) -> Dict[str, Any]:
    return model_out


def should_continue(state: State) -> bool:
    results = state.get("results") or {}
    return not bool(results.get("recommendations"))

# =========================
# Utilidades: handler/retry compatibles con cualquier versión
# =========================

def mk_node_wrapper(
    fn: Callable[[State], State],
    node_name: str,
    max_attempts: int = 1,
    backoff_seconds: float = 0.0,
) -> Callable[[State], State]:
    """
    Envuelve un nodo para:
      - Reintentos (max_attempts)
      - Manejo de errores (acumula en state['errors'])
    Compatible con stacks donde no existen .with_error_handler/.with_retry.
    """
    def _wrapped(state: State) -> State:
        attempts = 0
        last_err: Optional[Exception] = None
        while attempts < max_attempts:
            try:
                return fn(state)
            except Exception as e:
                last_err = e
                errs = list(state.get("errors") or [])
                errs.append(f"{node_name}: {e}")
                state = dict(state)
                state["errors"] = errs
                attempts += 1
                if attempts < max_attempts and backoff_seconds > 0:
                    time.sleep(backoff_seconds)
        # Si falló todos los intentos, devolvemos el estado con error registrado.
        # No re-lanzamos para evitar 500 en FastAPI; si quieres abortar, raise aquí.
        return state
    return _wrapped

# =========================
# Nodos "puros"
# =========================

def _fetch_data(state: State) -> State:
    zones = state.get("zones") or []
    ctx = state.get("context") or {}
    filters = ctx.get("filters") or {}
    mcp = state.get("mcp_client")
    data = your_fetch_fn(zones, filters, mcp)
    new_state = dict(state)
    new_state["raw_data"] = data
    return new_state


def _preprocess(state: State) -> State:
    processed = your_preprocess_fn(state.get("raw_data") or [])
    new_state = dict(state)
    new_state["processed"] = processed
    return new_state


def _model_infer(state: State) -> State:
    llm = state.get("llm")
    objectives = (state.get("context") or {}).get("objectives") or []
    out = your_model_infer_fn(state.get("processed") or [], objectives, llm)
    new_state = dict(state)
    new_state["results"] = out
    return new_state


def _postprocess(state: State) -> State:
    post = your_postprocess_fn(state.get("results") or {})
    new_state = dict(state)
    new_state["results"] = post
    new_state["summary"] = post.get("summary")
    new_state["model_outputs"] = post
    return new_state


def _decider(state: State) -> State:
    return state

# =========================
# Construcción del grafo
# =========================

def build_graph(llm: Any, mcp_client: Any):
    """
    Recibe dependencias y compila el grafo.
    """
    graph = StateGraph(State)

    # Envolvemos cada nodo con reintentos y manejo de errores
    fetch_wrapped = mk_node_wrapper(_fetch_data, "fetch_data", max_attempts=3, backoff_seconds=0.2)
    prep_wrapped = mk_node_wrapper(_preprocess, "preprocess", max_attempts=2, backoff_seconds=0.1)
    infer_wrapped = mk_node_wrapper(_model_infer, "model_infer", max_attempts=3, backoff_seconds=0.2)
    post_wrapped  = mk_node_wrapper(_postprocess, "postprocess", max_attempts=2, backoff_seconds=0.1)
    decider_wrapped = mk_node_wrapper(_decider, "decider", max_attempts=1, backoff_seconds=0.0)

    graph.add_node("fetch_data", RunnableLambda(fetch_wrapped))
    graph.add_node("preprocess", RunnableLambda(prep_wrapped))
    graph.add_node("model_infer", RunnableLambda(infer_wrapped))
    graph.add_node("postprocess", RunnableLambda(post_wrapped))
    graph.add_node("decider", RunnableLambda(decider_wrapped))

    graph.set_entry_point("fetch_data")
    graph.add_edge("fetch_data", "preprocess")
    graph.add_edge("preprocess", "model_infer")
    graph.add_edge("model_infer", "postprocess")
    graph.add_edge("postprocess", "decider")

    graph.add_conditional_edges(
        "decider",
        lambda s: "continue" if should_continue(s) else "end",
        {"continue": "fetch_data", "end": END},
    )

    compiled = graph.compile()
    compiled._injected = {"llm": llm, "mcp_client": mcp_client}  # opcional
    return compiled
