from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.settings import get_settings

app = FastAPI()
settings = get_settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins = settings.allowed_origins or ["*"],
    allow_credentials = settings.allowed_credential,
    allow_methods = settings.allowed_methods or ["*"],
    allow_headers = settings.allowed_headers or ["*"]
)


@app.get("/")
def health():
    return {
        "Database Host": settings.database_host,
        "Database Name": settings.database_name,
        "Database Port": settings.database_port,
        "Pool Size": settings.database_pool_size,
        "Max Overflow": settings.database_max_overflow,
    }
