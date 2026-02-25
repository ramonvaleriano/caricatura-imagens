from app.models.photo_models import APIErrorResponse


ALLOWED_EXTENSIONS_EXAMPLE = [".jpeg", ".jpg", ".png", ".webp"]

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
                        "details": {"allowed_extensions": ALLOWED_EXTENSIONS_EXAMPLE},
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
                        "details": {"allowed_extensions": ALLOWED_EXTENSIONS_EXAMPLE},
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
