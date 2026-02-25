import logging

from fastapi import FastAPI

from app.core.cors import setup_cors
from app.core import settings
from app.core.logging_config import setup_logging
from app.core.storage import ensure_photo_directories
from app.routers.health import router as health_router
from app.routers.photos import router as photos_router


setup_logging()
logger = logging.getLogger(__name__)
ensure_photo_directories()
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)
setup_cors(app)
app.include_router(health_router, tags=["Default"])
app.include_router(photos_router)

logger.info(
    "Application started | app=%s version=%s environment=%s openai_enabled=%s model=%s",
    settings.app_name,
    settings.app_version,
    settings.environment,
    settings.openai_enabled,
    settings.openai_model,
)
