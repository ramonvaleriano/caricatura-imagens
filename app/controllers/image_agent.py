from pathlib import Path

from app.services.image_generation_service import process_image


def process_image_with_agent(input_photo_path: Path) -> bytes:
    """
    Controller fino do agente.
    Delegacao da regra de geracao para a camada de service.
    """
    return process_image(input_photo_path)
