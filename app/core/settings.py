import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")


app_name=os.getenv("APP_NAME", "Caricatura Imagens API")
app_version=os.getenv("APP_VERSION", "0.1.0")
environment=os.getenv("ENVIRONMENT", "development")
debug=os.getenv("DEBUG", False)
host=os.getenv("HOST", "0.0.0.0")
port=os.getenv("PORT", 8000)
cors_origins=os.getenv("CORS_ORIGINS", "*")
log_level=os.getenv("LOG_LEVEL", "INFO")
input_photos_dir=os.getenv("INPUT_PHOTOS_DIR", "app/data/input")
generated_photos_dir=os.getenv("GENERATED_PHOTOS_DIR", "app/data/output")
input_photo_default_name=os.getenv("INPUT_PHOTO_DEFAULT_NAME", "input_photo")
output_photo_default_name=os.getenv("OUTPUT_PHOTO_DEFAULT_NAME", "output_photo")
allowed_input_extensions=os.getenv("ALLOWED_INPUT_EXTENSIONS", "jpg,jpeg,png,webp")

# IA / OpenAI settings
openai_enabled=os.getenv("OPENAI_ENABLED", "false")
openai_api_key=os.getenv("OPENAI_API_KEY", "")
openai_model=os.getenv("OPENAI_MODEL", "gpt-5")
openai_developer_prompt=os.getenv(
    "OPENAI_DEVELOPER_PROMPT",
    "Create a caricature of the person in the input image and preserve identity details.",
)
openai_user_prompt=os.getenv(
    "OPENAI_USER_PROMPT",
    "You are an expert at creating fun, lively, yet realistic caricatures.",
)
openai_reasoning_effort=os.getenv("OPENAI_REASONING_EFFORT", "medium")
openai_text_verbosity=os.getenv("OPENAI_TEXT_VERBOSITY", "medium")
openai_store_response=os.getenv("OPENAI_STORE_RESPONSE", "false")
openai_enable_web_search=os.getenv("OPENAI_ENABLE_WEB_SEARCH", "false")
openai_include_fields=os.getenv(
    "OPENAI_INCLUDE_FIELDS",
    "reasoning.encrypted_content,web_search_call.action.sources",
)
