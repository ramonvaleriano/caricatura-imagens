from dataclasses import dataclass

from app.core import settings


def _to_bool(value: object, default: bool = False) -> bool:
    if value is None:
        return default
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def _to_csv_list(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


@dataclass(frozen=True)
class AIConfig:
    enabled: bool
    api_key: str
    model: str
    reasoning_effort: str
    text_verbosity: str
    store_response: bool
    enable_web_search: bool
    include_fields: list[str]


def get_ai_config() -> AIConfig:
    return AIConfig(
        enabled=_to_bool(settings.openai_enabled, False),
        api_key=settings.openai_api_key.strip(),
        model=settings.openai_model.strip(),
        reasoning_effort=settings.openai_reasoning_effort.strip() or "medium",
        text_verbosity=settings.openai_text_verbosity.strip() or "medium",
        store_response=_to_bool(settings.openai_store_response, False),
        enable_web_search=_to_bool(settings.openai_enable_web_search, False),
        include_fields=_to_csv_list(settings.openai_include_fields),
    )
