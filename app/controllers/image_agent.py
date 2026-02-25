import logging
from pathlib import Path

from app.services.image_generation_service import process_image

logger = logging.getLogger(__name__)


def process_image_with_agent(input_photo_path: Path) -> bytes:
    """
    Controller fino do agente.
    Delegacao da regra de geracao para a camada de service.
    """
    logger.info(
        "Controller called | controller=image_agent input_file=%s",
        input_photo_path.name,
    )
    return process_image(input_photo_path)
