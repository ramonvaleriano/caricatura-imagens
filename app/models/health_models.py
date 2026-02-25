from pydantic import BaseModel, Field


class HealthSettingsPayload(BaseModel):
    app_name: str = Field(..., description="Valor de APP_NAME.")
    app_version: str = Field(..., description="Valor de APP_VERSION.")
    environment: str = Field(..., description="Valor de ENVIRONMENT.")
    debug: str = Field(..., description="Valor de DEBUG.")
    host: str = Field(..., description="Valor de HOST.")
    port: str = Field(..., description="Valor de PORT.")
    cors_origins: str = Field(..., description="Valor de CORS_ORIGINS.")
    log_level: str = Field(..., description="Valor de LOG_LEVEL.")
    input_photos_dir: str = Field(..., description="Valor de INPUT_PHOTOS_DIR.")
    generated_photos_dir: str = Field(..., description="Valor de GENERATED_PHOTOS_DIR.")
    input_photo_default_name: str = Field(
        ..., description="Valor de INPUT_PHOTO_DEFAULT_NAME."
    )
    output_photo_default_name: str = Field(
        ..., description="Valor de OUTPUT_PHOTO_DEFAULT_NAME."
    )
    allowed_input_extensions: str = Field(
        ..., description="Valor de ALLOWED_INPUT_EXTENSIONS."
    )
    openai_enabled: str = Field(..., description="Valor de OPENAI_ENABLED.")
    openai_api_key: bool = Field(
        ...,
        description=(
            "Indica se OPENAI_API_KEY esta configurada. "
            "Retorna true quando ha valor e false quando vazio."
        ),
    )
    openai_model: str = Field(..., description="Valor de OPENAI_MODEL.")
    openai_reasoning_effort: str = Field(
        ..., description="Valor de OPENAI_REASONING_EFFORT."
    )
    openai_text_verbosity: str = Field(
        ..., description="Valor de OPENAI_TEXT_VERBOSITY."
    )
    openai_store_response: str = Field(
        ..., description="Valor de OPENAI_STORE_RESPONSE."
    )
    openai_enable_web_search: str = Field(
        ..., description="Valor de OPENAI_ENABLE_WEB_SEARCH."
    )
    openai_include_fields: str = Field(
        ..., description="Valor de OPENAI_INCLUDE_FIELDS."
    )


class HealthResponse(BaseModel):
    status: str = Field(..., description="Status basico da API.", examples=["ok"])
    settings: HealthSettingsPayload
