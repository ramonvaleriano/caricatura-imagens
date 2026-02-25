import logging

from app.core import settings


LOG_FORMAT = (
    "%(asctime)s | %(levelname)s | %(name)s | "
    "%(message)s"
)


def setup_logging() -> None:
    logging.basicConfig(
        level=settings.log_level.upper(),
        format=LOG_FORMAT,
        force=True,
    )

