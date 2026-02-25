from pathlib import Path


def process_image_with_agent(input_photo_path: Path) -> bytes:
    """
    Placeholder do agente de IA.

    Comportamento atual:
    - retorna exatamente os mesmos bytes da imagem de entrada.

    Comportamento futuro:
    - enviar a imagem ao agente de IA e retornar a imagem transformada.
    """
    return input_photo_path.read_bytes()

