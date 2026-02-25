from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core import settings


def setup_cors(app: FastAPI) -> None:
    origins = [origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()]
    allow_all = not origins or origins == ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"] if allow_all else origins,
        allow_credentials=False if allow_all else True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

