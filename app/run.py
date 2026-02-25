from fastapi import FastAPI

from app.core.cors import setup_cors
from app.core import settings
from app.routers.health import router as health_router


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)
setup_cors(app)
app.include_router(health_router, tags=["Default"])
