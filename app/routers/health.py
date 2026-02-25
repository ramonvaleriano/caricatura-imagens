from fastapi import APIRouter


router = APIRouter()


@router.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}

@router.get("/")
def standard() -> dict[str, str]:
    return {"status": "ok"}

