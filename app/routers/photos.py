import logging
import mimetypes
import shutil
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile, status
from fastapi.responses import FileResponse

from app.controllers.image_agent import process_image_with_agent
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
logger = logging.getLogger(__name__)

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

PROCESS_INPUT_RESPONSES = {
    200: {
        "description": "Imagem processada retornada com sucesso.",
        "content": {"image/*": {}},
    },
    404: {
        "model": APIErrorResponse,
        "description": "Nenhuma foto encontrada no diretorio de input.",
        "content": {
            "application/json": {
                "example": {
                    "detail": {
                        "code": "INPUT_PHOTO_NOT_FOUND",
                        "message": "Nao existe foto no diretorio de input para processar.",
                        "details": {"input_directory": "app/data/input"},
                    }
                }
            }
        },
    },
    409: {
        "model": APIErrorResponse,
        "description": "Mais de uma foto encontrada no diretorio de input.",
        "content": {
            "application/json": {
                "example": {
                    "detail": {
                        "code": "MULTIPLE_INPUT_PHOTOS",
                        "message": "Existe mais de uma foto no diretorio de input.",
                        "details": {"files_found": ["input_photo.jpg", "input_photo.png"]},
                    }
                }
            }
        },
    },
    415: {
        "model": APIErrorResponse,
        "description": "Formato da foto de input nao suportado.",
        "content": {
            "application/json": {
                "example": {
                    "detail": {
                        "code": "UNSUPPORTED_INPUT_FILE_FORMAT",
                        "message": "Formato da foto de input nao suportado.",
                        "details": {"allowed_extensions": [".jpeg", ".jpg", ".png", ".webp"]},
                    }
                }
            }
        },
    },
    500: {
        "model": APIErrorResponse,
        "description": "Falha interna no processamento do agente.",
        "content": {
            "application/json": {
                "example": {
                    "detail": {
                        "code": "FAILED_TO_PROCESS_IMAGE",
                        "message": "Nao foi possivel processar a foto de input com o agente.",
                        "details": {"error": "Agent timeout"},
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
    if status_code >= status.HTTP_500_INTERNAL_SERVER_ERROR:
        logger.error(
            "API error | status=%s code=%s message=%s details=%s",
            status_code,
            code,
            message,
            details,
        )
    else:
        logger.warning(
            "API error | status=%s code=%s message=%s details=%s",
            status_code,
            code,
            message,
            details,
        )
    raise HTTPException(
        status_code=status_code,
        detail={"code": code, "message": message, "details": details},
    )


def _list_visible_files(directory: Path) -> list[Path]:
    return [
        file
        for file in directory.iterdir()
        if file.is_file() and not file.name.startswith(".")
    ]


def _next_output_file_name(output_dir: Path, extension: str) -> str:
    max_index = 0
    base_name = settings.output_photo_default_name

    for file in _list_visible_files(output_dir):
        stem = file.stem
        if not stem.startswith(base_name):
            continue

        suffix = stem[len(base_name):]
        if suffix.isdigit():
            max_index = max(max_index, int(suffix))

    return f"{base_name}{max_index + 1}{extension}"


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
    logger.info(
        "Route called | method=POST path=/photos/input filename=%s",
        file.filename,
    )

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

    logger.info(
        "Input photo saved | file_name=%s location=%s size_bytes=%s",
        target_file_name,
        location,
        target_path.stat().st_size,
    )

    return UploadInputPhotoResponse(
        message="Foto de entrada salva com sucesso.",
        file_name=target_file_name,
        format=file_extension.lstrip("."),
        location=location,
    )


@router.post(
    "/process",
    response_class=FileResponse,
    summary="Processar foto de input com o agente de IA",
    description=(
        "Processa a foto atual armazenada em `app/data/input` usando o agente.\n\n"
        "Comportamento do agente:\n"
        "- `OPENAI_ENABLED=false`: retorna a mesma imagem de entrada (fallback);\n"
        "- `OPENAI_ENABLED=true`: chama a OpenAI e retorna a imagem transformada.\n\n"
        "- Esta rota nao recebe payload no body;\n"
        "- espera existir exatamente 1 arquivo no diretorio de input;\n"
        "- salva o resultado em `app/data/output` com numeracao automatica;\n"
        "- retorna a imagem processada no response."
    ),
    responses=PROCESS_INPUT_RESPONSES,
)
def process_input_photo() -> FileResponse:
    """Processa a foto de input com o agente placeholder e retorna o arquivo gerado."""
    logger.info("Route called | method=POST path=/photos/process")
    input_dir = get_input_photos_dir()
    output_dir = get_generated_photos_dir()
    allowed_extensions = get_allowed_input_extensions()

    try:
        input_files = _list_visible_files(input_dir)
    except OSError as exc:
        _raise_api_error(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "FAILED_TO_READ_INPUT_DIRECTORY",
            "Nao foi possivel ler o diretorio de input.",
            {"error": str(exc)},
        )

    if not input_files:
        _raise_api_error(
            status.HTTP_404_NOT_FOUND,
            "INPUT_PHOTO_NOT_FOUND",
            "Nao existe foto no diretorio de input para processar.",
            {"input_directory": str(input_dir)},
        )

    if len(input_files) > 1:
        _raise_api_error(
            status.HTTP_409_CONFLICT,
            "MULTIPLE_INPUT_PHOTOS",
            "Existe mais de uma foto no diretorio de input.",
            {"files_found": sorted(file.name for file in input_files)},
        )

    input_photo = input_files[0]
    input_extension = input_photo.suffix.lower()

    if input_extension not in allowed_extensions:
        _raise_api_error(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            "UNSUPPORTED_INPUT_FILE_FORMAT",
            "Formato da foto de input nao suportado.",
            {"allowed_extensions": sorted(allowed_extensions)},
        )

    try:
        processed_bytes = process_image_with_agent(input_photo)
    except OSError as exc:
        _raise_api_error(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "FAILED_TO_PROCESS_IMAGE",
            "Nao foi possivel processar a foto de input com o agente.",
            {"error": str(exc)},
        )
    except Exception as exc:
        _raise_api_error(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "AGENT_RUNTIME_ERROR",
            "Falha inesperada durante a execucao do agente.",
            {"error": str(exc)},
        )

    if not processed_bytes:
        _raise_api_error(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "EMPTY_AGENT_OUTPUT",
            "O agente retornou uma imagem vazia.",
        )

    try:
        output_file_name = _next_output_file_name(output_dir, input_extension)
        output_file_path = output_dir / output_file_name
        output_file_path.write_bytes(processed_bytes)
    except OSError as exc:
        _raise_api_error(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "FAILED_TO_SAVE_OUTPUT_PHOTO",
            "Nao foi possivel salvar a foto processada no diretorio de output.",
            {"error": str(exc)},
        )

    media_type = mimetypes.guess_type(output_file_path.name)[0] or "application/octet-stream"
    logger.info(
        "Photo processed | input_file=%s output_file=%s output_size_bytes=%s",
        input_photo.name,
        output_file_name,
        len(processed_bytes),
    )

    return FileResponse(
        path=output_file_path,
        media_type=media_type,
        filename=output_file_path.name,
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
    logger.info("Route called | method=GET path=/photos/output")
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
    logger.info("Generated photos listed | total=%s", len(photos))

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
    logger.info(
        "Route called | method=GET path=/photos/output/{photo_name} photo_name=%s",
        photo_name,
    )
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
    logger.info(
        "Generated photo served | file_name=%s media_type=%s",
        target_file.name,
        media_type,
    )

    return FileResponse(
        path=target_file,
        media_type=media_type,
        filename=target_file.name,
    )
