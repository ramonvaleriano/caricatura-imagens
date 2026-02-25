import uvicorn

from app.core import settings


if __name__ == "__main__":
    uvicorn.run(
        "app.run:app",
        host=settings.host,
        port=int(settings.port),
        reload=True,
    )
