from functools import lru_cache
from pathlib import Path


PROMPTS_DIR = Path(__file__).resolve().parents[1] / "prompts"
DEVELOPER_PROMPT_FILE = PROMPTS_DIR / "image_developer_prompt.md"
USER_PROMPT_FILE = PROMPTS_DIR / "image_user_prompt.md"


@lru_cache
def _read_prompt(file_path: Path) -> str:
    if not file_path.exists():
        raise RuntimeError(f"Prompt file not found: {file_path}")

    content = file_path.read_text(encoding="utf-8").strip()
    if not content:
        raise RuntimeError(f"Prompt file is empty: {file_path}")

    return content


def get_image_prompts() -> tuple[str, str]:
    developer_prompt = _read_prompt(DEVELOPER_PROMPT_FILE)
    user_prompt = _read_prompt(USER_PROMPT_FILE)
    return developer_prompt, user_prompt

