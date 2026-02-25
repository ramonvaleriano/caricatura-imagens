from typing import Any

from pydantic import BaseModel, Field


class APIErrorDetail(BaseModel):
    code: str = Field(
        ...,
        description="Codigo interno do erro para rastreabilidade.",
        examples=["PHOTO_NOT_FOUND"],
    )
    message: str = Field(
        ...,
        description="Descricao amigavel do erro.",
        examples=["Nao foi encontrada foto gerada com o nome informado."],
    )
    details: dict[str, Any] | None = Field(
        default=None,
        description="Detalhes tecnicos complementares do erro.",
    )


class APIErrorResponse(BaseModel):
    detail: APIErrorDetail


class UploadInputPhotoResponse(BaseModel):
    message: str = Field(
        ...,
        description="Mensagem de sucesso da operacao de upload.",
        examples=["Foto de entrada salva com sucesso."],
    )
    file_name: str = Field(
        ...,
        description="Nome final do arquivo salvo no diretorio de entrada.",
        examples=["input_photo.jpg"],
    )
    format: str = Field(
        ...,
        description="Formato da imagem salva (extensao sem ponto).",
        examples=["jpg"],
    )
    location: str = Field(
        ...,
        description="Caminho relativo do arquivo salvo.",
        examples=["app/data/input/input_photo.jpg"],
    )


class GeneratedPhotoItem(BaseModel):
    file_name: str = Field(
        ...,
        description="Nome completo da foto gerada, incluindo extensao.",
        examples=["output_photo1.jpg"],
    )
    format: str = Field(
        ...,
        description="Formato da foto gerada (extensao sem ponto).",
        examples=["jpg"],
    )


class ListGeneratedPhotosResponse(BaseModel):
    total: int = Field(
        ...,
        description="Quantidade total de fotos geradas no diretorio.",
        examples=[3],
    )
    photos: list[GeneratedPhotoItem] = Field(
        default_factory=list,
        description="Lista de fotos geradas disponiveis para consulta/download.",
    )
