from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.settings import get_settings
from src.api.routes import router
from src.api import api_router

app = FastAPI(
    title="NASA Space Apps - Urban EarthLens",
    description="API para consultar datos de calidad urbana filtrados por área geográfica",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)
settings = get_settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins = settings.allowed_origins or ["*"],
    allow_credentials = settings.allowed_credential,
    allow_methods = settings.allowed_methods or ["*"],
    allow_headers = settings.allowed_headers or ["*"]
)

# Registrar los endpoints de Urban Quality
app.include_router(router)
app.include_router(api_router)

@app.get("/")
def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "NASA Space Apps API está funcionando correctamente",
        "version": "1.0.0",
        "endpoints": {
            "population": "/api/v1/population",
            "education": "/api/v1/education",
            "trees": "/api/v1/trees"
        },
        "database": {
            "host": settings.database_host,
            "name": settings.database_name,
            "port": settings.database_port,
            "pool_size": settings.database_pool_size,
            "max_overflow": settings.database_max_overflow,
        }
    }
