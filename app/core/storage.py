from pathlib import Path

from app.core import settings


BASE_DIR = Path(__file__).resolve().parents[2]


def _resolve_path(raw_path: str) -> Path:
    path = Path(raw_path)
    if path.is_absolute():
        return path
    return BASE_DIR / path


def get_input_photos_dir() -> Path:
    return _resolve_path(settings.input_photos_dir)


def get_generated_photos_dir() -> Path:
    return _resolve_path(settings.generated_photos_dir)


def get_allowed_input_extensions() -> set[str]:
    extensions = set()
    for item in settings.allowed_input_extensions.split(","):
        cleaned = item.strip().lower().lstrip(".")
        if cleaned:
            extensions.add(f".{cleaned}")
    return extensions


def ensure_photo_directories() -> None:
    get_input_photos_dir().mkdir(parents=True, exist_ok=True)
    get_generated_photos_dir().mkdir(parents=True, exist_ok=True)

