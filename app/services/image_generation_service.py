import base64
import logging
import mimetypes
from pathlib import Path
from typing import Any

from app.core.ai_config import get_ai_config

logger = logging.getLogger(__name__)


def _extract_generated_image_base64(response: Any) -> str | None:
    payload: dict[str, Any] = {}

    if hasattr(response, "model_dump"):
        dumped = response.model_dump()
        if isinstance(dumped, dict):
            payload = dumped
    elif isinstance(response, dict):
        payload = response

    output_items = payload.get("output", [])
    if not isinstance(output_items, list):
        return None

    for item in output_items:
        if not isinstance(item, dict):
            continue

        if item.get("type") == "image_generation_call":
            result = item.get("result")
            if isinstance(result, str) and result:
                return result

        content = item.get("content", [])
        if not isinstance(content, list):
            continue

        for chunk in content:
            if not isinstance(chunk, dict):
                continue
            for key in ("image_base64", "b64_json", "data"):
                value = chunk.get(key)
                if isinstance(value, str) and value:
                    return value

    return None


def process_image(input_photo_path: Path) -> bytes:
    """
    Service de geracao de imagem.

    Regras:
    - se OPENAI_ENABLED=false, retorna a imagem original (fallback);
    - se OPENAI_ENABLED=true, chama a API da OpenAI e retorna a imagem gerada.
    """
    input_bytes = input_photo_path.read_bytes()
    ai_config = get_ai_config()
    logger.info(
        "Service called | service=image_generation_service input_file=%s openai_enabled=%s",
        input_photo_path.name,
        ai_config.enabled,
    )

    if not ai_config.enabled:
        logger.info(
            "Image processed with fallback | reason=OPENAI_DISABLED output_size_bytes=%s",
            len(input_bytes),
        )
        return input_bytes

    if not ai_config.api_key:
        logger.error("OPENAI_API_KEY missing while OPENAI_ENABLED=true")
        raise RuntimeError("OPENAI_API_KEY is required when OPENAI_ENABLED=true.")

    try:
        from openai import OpenAI
    except ImportError as exc:
        logger.exception("Failed to import OpenAI SDK")
        raise RuntimeError("OpenAI SDK is not installed. Install dependencies first.") from exc

    image_mime_type = mimetypes.guess_type(input_photo_path.name)[0] or "image/jpeg"
    image_base64 = base64.b64encode(input_bytes).decode("utf-8")
    input_image_url = f"data:{image_mime_type};base64,{image_base64}"

    tools: list[dict[str, str]] = [{"type": "image_generation"}]
    if ai_config.enable_web_search:
        tools.insert(0, {"type": "web_search_preview"})

    request_payload: dict[str, Any] = {
        "model": ai_config.model,
        "input": [
            {
                "role": "developer",
                "content": [
                    {"type": "input_text", "text": ai_config.developer_prompt},
                ],
            },
            {
                "role": "user",
                "content": [
                    {"type": "input_text", "text": ai_config.user_prompt},
                ],
            },
            {
                "role": "user",
                "content": [
                    {"type": "input_image", "image_url": input_image_url},
                ],
            },
        ],
        "reasoning": {"effort": ai_config.reasoning_effort},
        "text": {"format": {"type": "text"}, "verbosity": ai_config.text_verbosity},
        "tools": tools,
        "store": ai_config.store_response,
    }

    if ai_config.include_fields:
        request_payload["include"] = ai_config.include_fields

    logger.info(
        "Calling OpenAI | model=%s reasoning_effort=%s text_verbosity=%s tools=%s",
        ai_config.model,
        ai_config.reasoning_effort,
        ai_config.text_verbosity,
        [tool["type"] for tool in tools],
    )

    client = OpenAI(api_key=ai_config.api_key)
    try:
        response = client.responses.create(**request_payload)
    except Exception as exc:
        logger.exception("OpenAI request failed")
        raise RuntimeError("Failed to call OpenAI Responses API.") from exc

    generated_image_base64 = _extract_generated_image_base64(response)

    if not generated_image_base64:
        logger.error("OpenAI response did not include generated image")
        raise RuntimeError("The AI response did not include a generated image.")

    try:
        output_bytes = base64.b64decode(generated_image_base64)
        logger.info(
            "Image processed with OpenAI | output_size_bytes=%s",
            len(output_bytes),
        )
        return output_bytes
    except ValueError as exc:
        logger.exception("Failed to decode generated image base64")
        raise RuntimeError("Failed to decode generated image from base64.") from exc
