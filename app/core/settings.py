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
input_photos_dir=os.getenv("INPUT_PHOTOS_DIR", "app/data/input")
generated_photos_dir=os.getenv("GENERATED_PHOTOS_DIR", "app/data/output")
input_photo_default_name=os.getenv("INPUT_PHOTO_DEFAULT_NAME", "input_photo")
allowed_input_extensions=os.getenv("ALLOWED_INPUT_EXTENSIONS", "jpg,jpeg,png,webp")
