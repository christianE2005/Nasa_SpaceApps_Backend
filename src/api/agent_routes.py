from fastapi import APIRouter
from sse_starlette.sse import EventSourceResponse
from src.agent.orchestrator import run_orchestration
from src.agent.llm import LLM
from src.schemas.agent import PlanRequest
from shapely.geometry import shape
import json

router = APIRouter(prefix="/urban", tags=["Urban Planning"])

def sse(evt, data):
    return {"event": evt, "data": json.dumps(data), "retry": 3000}

def _prepare_zones(req: PlanRequest):
    zones = []
    for z in req.zones:
        g = shape(z.geometry.model_dump())
        c = g.centroid
        zones.append({
            "id": z.id,
            "lat": c.y, "lon": c.x,            # para tools
            "geometry": z.geometry.model_dump(),  # conservar GeoJSON original
            "data": z.data
        })
    return zones

@router.post("/stream")
async def stream_urban(req: PlanRequest):
    async def event_stream():
        zones = _prepare_zones(req)
        filters = req.filters
        objectives = req.objectives

        yield sse("start", {"message": "Procesando zonas urbanas..."})

        # Orquestación completa: queries→payloads completos→MCP tools→mapa
        result = await run_orchestration(zones, filters, objectives)

        # LLM: prioridades/síntesis
        question = LLM.build_question(result["model_outputs"], filters, objectives)
        planner = LLM.planner_chain()
        summary = await planner.ainvoke({"question": question})

        # Streaming final: GeoJSON + resumen
        yield sse("map.update", {"featureCollection": result["map_json"]})
        yield sse("summary", {"text": summary})
        yield sse("done", {"status": "ok"})

    return EventSourceResponse(event_stream())

@router.post("/run")
async def run_urban(req: PlanRequest):
    zones = _prepare_zones(req)
    result = await run_orchestration(zones, req.filters, req.objectives)
    question = LLM.build_question(result["model_outputs"], req.filters, req.objectives)
    planner = LLM.planner_chain()
    summary = await planner.ainvoke({"question": question})
    return {
        "summary": summary,
        "featureCollection": result["map_json"],
        "models": result["model_outputs"],
    }
