import logging

from fastapi import APIRouter

from app.core import settings
from app.models.health_models import HealthResponse, HealthSettingsPayload

router = APIRouter()
logger = logging.getLogger(__name__)


HEALTH_RESPONSES = {
    200: {
        "description": (
            "Status da API com o espelho das configuracoes carregadas em "
            "`app/core/settings.py`, sem expor o valor da chave da OpenAI."
        ),
        "content": {
            "application/json": {
                "example": {
                    "status": "ok",
                    "settings": {
                        "app_name": "Caricatura Imagens API",
                        "app_version": "0.1.0",
                        "environment": "development",
                        "debug": "false",
                        "host": "0.0.0.0",
                        "port": "8000",
                        "cors_origins": "*",
                        "log_level": "INFO",
                        "input_photos_dir": "app/data/input",
                        "generated_photos_dir": "app/data/output",
                        "input_photo_default_name": "input_photo",
                        "output_photo_default_name": "output_photo",
                        "allowed_input_extensions": "jpg,jpeg,png,webp",
                        "openai_enabled": "true",
                        "openai_api_key": True,
                        "openai_model": "gpt-5",
                        "openai_reasoning_effort": "medium",
                        "openai_text_verbosity": "medium",
                        "openai_store_response": "false",
                        "openai_enable_web_search": "false",
                        "openai_include_fields": (
                            "reasoning.encrypted_content,"
                            "web_search_call.action.sources"
                        ),
                    },
                }
            }
        },
    }
}


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Healthcheck com configuracoes da API",
    description=(
        "Retorna status da API e todas as configuracoes carregadas pelo "
        "`app/core/settings.py`.\n\n"
        "Seguranca:\n"
        "- o valor de `OPENAI_API_KEY` nao e exposto;\n"
        "- o campo `openai_api_key` retorna apenas `true` ou `false`."
    ),
    responses=HEALTH_RESPONSES,
)
def healthcheck() -> HealthResponse:
    """
    Retorna o healthcheck completo da API com o espelho das configuracoes.

    Observacao:
    `OPENAI_API_KEY` e mascarada como booleano para nao expor segredo.
    """
    logger.info("Route called | method=GET path=/health")
    return HealthResponse(
        status="ok",
        settings=HealthSettingsPayload(
            app_name=settings.app_name,
            app_version=settings.app_version,
            environment=settings.environment,
            debug=str(settings.debug),
            host=str(settings.host),
            port=str(settings.port),
            cors_origins=settings.cors_origins,
            log_level=settings.log_level,
            input_photos_dir=settings.input_photos_dir,
            generated_photos_dir=settings.generated_photos_dir,
            input_photo_default_name=settings.input_photo_default_name,
            output_photo_default_name=settings.output_photo_default_name,
            allowed_input_extensions=settings.allowed_input_extensions,
            openai_enabled=settings.openai_enabled,
            openai_api_key=bool(settings.openai_api_key.strip()),
            openai_model=settings.openai_model,
            openai_reasoning_effort=settings.openai_reasoning_effort,
            openai_text_verbosity=settings.openai_text_verbosity,
            openai_store_response=settings.openai_store_response,
            openai_enable_web_search=settings.openai_enable_web_search,
            openai_include_fields=settings.openai_include_fields,
        ),
    )


@router.get("/")
def standard() -> dict[str, str]:
    logger.info("Route called | method=GET path=/")
    return {"status": "ok"}
