import mimetypes
import shutil
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile, status
from fastapi.responses import FileResponse

from app.core import settings
from app.core.storage import (
    get_allowed_input_extensions,
    get_generated_photos_dir,
    get_input_photos_dir,
)
from app.models.photo_models import (
    APIErrorResponse,
    GeneratedPhotoItem,
    ListGeneratedPhotosResponse,
    UploadInputPhotoResponse,
)


router = APIRouter(prefix="/photos", tags=["Photos"])

UPLOAD_INPUT_RESPONSES = {
    400: {
        "model": APIErrorResponse,
        "description": "Arquivo vazio ou nome invalido.",
        "content": {
            "application/json": {
                "example": {
                    "detail": {
                        "code": "EMPTY_FILE",
                        "message": "O arquivo enviado esta vazio.",
                        "details": None,
                    }
                }
            }
        },
    },
    415: {
        "model": APIErrorResponse,
        "description": "Formato de arquivo nao suportado.",
        "content": {
            "application/json": {
                "example": {
                    "detail": {
                        "code": "UNSUPPORTED_FILE_FORMAT",
                        "message": "Formato de arquivo nao suportado para foto de entrada.",
                        "details": {"allowed_extensions": [".jpeg", ".jpg", ".png", ".webp"]},
                    }
                }
            }
        },
    },
    500: {
        "model": APIErrorResponse,
        "description": "Falha interna ao salvar arquivo.",
        "content": {
            "application/json": {
                "example": {
                    "detail": {
                        "code": "FAILED_TO_SAVE_INPUT_PHOTO",
                        "message": "Nao foi possivel salvar a foto de entrada.",
                        "details": {"error": "Permission denied"},
                    }
                }
            }
        },
    },
}

LIST_GENERATED_RESPONSES = {
    500: {
        "model": APIErrorResponse,
        "description": "Falha interna ao listar arquivos.",
        "content": {
            "application/json": {
                "example": {
                    "detail": {
                        "code": "FAILED_TO_LIST_GENERATED_PHOTOS",
                        "message": "Nao foi possivel listar as fotos geradas.",
                        "details": {"error": "Input/output error"},
                    }
                }
            }
        },
    }
}

GET_GENERATED_RESPONSES = {
    200: {
        "description": "Arquivo de imagem retornado com sucesso.",
        "content": {"image/*": {}},
    },
    400: {
        "model": APIErrorResponse,
        "description": "Nome da foto invalido.",
        "content": {
            "application/json": {
                "example": {
                    "detail": {
                        "code": "INVALID_PHOTO_NAME",
                        "message": "O nome da foto informado e invalido.",
                        "details": None,
                    }
                }
            }
        },
    },
    404: {
        "model": APIErrorResponse,
        "description": "Foto nao encontrada.",
        "content": {
            "application/json": {
                "example": {
                    "detail": {
                        "code": "PHOTO_NOT_FOUND",
                        "message": "Nao foi encontrada foto gerada com o nome informado.",
                        "details": {"photo_name": "output_photo1"},
                    }
                }
            }
        },
    },
    409: {
        "model": APIErrorResponse,
        "description": "Mais de uma foto com mesmo nome base.",
        "content": {
            "application/json": {
                "example": {
                    "detail": {
                        "code": "AMBIGUOUS_PHOTO_NAME",
                        "message": "Existe mais de uma foto com esse nome base. Informe nome unico.",
                        "details": {
                            "available_files": ["output_photo1.jpg", "output_photo1.png"]
                        },
                    }
                }
            }
        },
    },
    500: {
        "model": APIErrorResponse,
        "description": "Falha interna ao ler arquivo.",
        "content": {
            "application/json": {
                "example": {
                    "detail": {
                        "code": "FAILED_TO_READ_GENERATED_PHOTO",
                        "message": "Nao foi possivel ler o diretorio de fotos geradas.",
                        "details": {"error": "Input/output error"},
                    }
                }
            }
        },
    },
}


def _raise_api_error(
    status_code: int,
    code: str,
    message: str,
    details: dict[str, object] | None = None,
) -> None:
    raise HTTPException(
        status_code=status_code,
        detail={"code": code, "message": message, "details": details},
    )


@router.post(
    "/input",
    response_model=UploadInputPhotoResponse,
    summary="Salvar foto de entrada (uma por vez)",
    description=(
        "Recebe uma unica foto de entrada via `multipart/form-data` no campo `file`.\n\n"
        "- Mantem apenas uma foto de entrada por vez;\n"
        "- remove automaticamente a foto anterior;\n"
        "- salva a nova foto com nome padrao + extensao original."
    ),
    responses=UPLOAD_INPUT_RESPONSES,
)
async def upload_input_photo(
    file: UploadFile = File(
        ...,
        description=(
            "Arquivo da foto de entrada. Aceita apenas extensoes configuradas em "
            "`ALLOWED_INPUT_EXTENSIONS`."
        ),
    ),
) -> UploadInputPhotoResponse:
    """Faz upload da foto de entrada e substitui qualquer foto anterior existente."""
    if not file.filename:
        _raise_api_error(
            status.HTTP_400_BAD_REQUEST,
            "INVALID_FILE_NAME",
            "O nome do arquivo enviado e invalido.",
        )

    file_extension = Path(file.filename).suffix.lower()
    allowed_extensions = get_allowed_input_extensions()

    if file_extension not in allowed_extensions:
        _raise_api_error(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            "UNSUPPORTED_FILE_FORMAT",
            "Formato de arquivo nao suportado para foto de entrada.",
            {"allowed_extensions": sorted(allowed_extensions)},
        )

    input_dir = get_input_photos_dir()
    target_file_name = f"{settings.input_photo_default_name}{file_extension}"
    target_path = input_dir / target_file_name

    try:
        for existing_file in input_dir.iterdir():
            if existing_file.is_file() and not existing_file.name.startswith("."):
                existing_file.unlink()

        with target_path.open("wb") as output_file:
            shutil.copyfileobj(file.file, output_file)
    except OSError as exc:
        _raise_api_error(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "FAILED_TO_SAVE_INPUT_PHOTO",
            "Nao foi possivel salvar a foto de entrada.",
            {"error": str(exc)},
        )
    finally:
        await file.close()

    if not target_path.exists() or target_path.stat().st_size == 0:
        if target_path.exists():
            target_path.unlink()
        _raise_api_error(
            status.HTTP_400_BAD_REQUEST,
            "EMPTY_FILE",
            "O arquivo enviado esta vazio.",
        )

    try:
        location = str(target_path.relative_to(Path.cwd()))
    except ValueError:
        location = str(target_path)

    return UploadInputPhotoResponse(
        message="Foto de entrada salva com sucesso.",
        file_name=target_file_name,
        format=file_extension.lstrip("."),
        location=location,
    )


@router.get(
    "/output",
    response_model=ListGeneratedPhotosResponse,
    summary="Listar fotos geradas pela IA",
    description=(
        "Retorna todas as fotos presentes no diretorio de fotos geradas pela IA, "
        "como uma lista com nome completo e formato."
    ),
    responses=LIST_GENERATED_RESPONSES,
)
def list_generated_photos() -> ListGeneratedPhotosResponse:
    """Lista todas as fotos geradas pela IA atualmente salvas no diretorio de saida."""
    generated_dir = get_generated_photos_dir()

    try:
        files = sorted(
            [
                file
                for file in generated_dir.iterdir()
                if file.is_file() and not file.name.startswith(".")
            ],
            key=lambda item: item.name.lower(),
        )
    except OSError as exc:
        _raise_api_error(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "FAILED_TO_LIST_GENERATED_PHOTOS",
            "Nao foi possivel listar as fotos geradas.",
            {"error": str(exc)},
        )

    photos = [
        GeneratedPhotoItem(
            file_name=file.name,
            format=file.suffix.lower().lstrip(".") or "sem_extensao",
        )
        for file in files
    ]

    return ListGeneratedPhotosResponse(total=len(photos), photos=photos)


@router.get(
    "/output/{photo_name}",
    response_class=FileResponse,
    summary="Baixar foto gerada pelo nome (sem extensao)",
    description=(
        "Retorna uma foto gerada a partir do nome base, sem necessidade de informar "
        "extensao. Exemplo: `/photos/output/output_photo1`."
    ),
    responses=GET_GENERATED_RESPONSES,
)
def get_generated_photo(photo_name: str) -> FileResponse:
    """Retorna a foto gerada correspondente ao nome base informado na URL."""
    raw_name = photo_name.strip()
    if not raw_name:
        _raise_api_error(
            status.HTTP_400_BAD_REQUEST,
            "INVALID_PHOTO_NAME",
            "O nome da foto informado e invalido.",
        )

    if "/" in raw_name or "\\" in raw_name:
        _raise_api_error(
            status.HTTP_400_BAD_REQUEST,
            "INVALID_PHOTO_NAME",
            "O nome da foto nao pode conter barras.",
        )

    normalized_name = Path(raw_name).stem
    generated_dir = get_generated_photos_dir()

    try:
        matches = [
            file
            for file in generated_dir.iterdir()
            if file.is_file() and not file.name.startswith(".") and file.stem == normalized_name
        ]
    except OSError as exc:
        _raise_api_error(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "FAILED_TO_READ_GENERATED_PHOTO",
            "Nao foi possivel ler o diretorio de fotos geradas.",
            {"error": str(exc)},
        )

    if not matches:
        _raise_api_error(
            status.HTTP_404_NOT_FOUND,
            "PHOTO_NOT_FOUND",
            "Nao foi encontrada foto gerada com o nome informado.",
            {"photo_name": normalized_name},
        )

    if len(matches) > 1:
        _raise_api_error(
            status.HTTP_409_CONFLICT,
            "AMBIGUOUS_PHOTO_NAME",
            "Existe mais de uma foto com esse nome base. Informe nome unico.",
            {"available_files": sorted(file.name for file in matches)},
        )

    target_file = matches[0]
    media_type = mimetypes.guess_type(target_file.name)[0] or "application/octet-stream"

    return FileResponse(
        path=target_file,
        media_type=media_type,
        filename=target_file.name,
    )
