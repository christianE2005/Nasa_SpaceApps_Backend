from fastapi import APIRouter
from src.api.agent_routes import router as urban_router

api_router = APIRouter()
api_router.include_router(urban_router)
