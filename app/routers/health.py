import logging

from fastapi import APIRouter


router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/health")
def healthcheck() -> dict[str, str]:
    logger.info("Route called | method=GET path=/health")
    return {"status": "ok"}

@router.get("/")
def standard() -> dict[str, str]:
    logger.info("Route called | method=GET path=/")
    return {"status": "ok"}
