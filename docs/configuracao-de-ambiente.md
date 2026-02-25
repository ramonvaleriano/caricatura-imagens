# Configuracao de Ambiente

## Fonte de configuracao

As variaveis sao carregadas de `.env` em `app/core/settings.py`, via `load_dotenv` + `os.getenv`.

## Variaveis atuais

- `APP_NAME`: nome exibido na documentacao OpenAPI.
- `APP_VERSION`: versao da API.
- `ENVIRONMENT`: ambiente logico (development, staging, production).
- `DEBUG`: flag reservada para comportamento futuro.
- `HOST`: host de bind do servidor.
- `PORT`: porta de bind do servidor.
- `CORS_ORIGINS`: lista de origens permitidas (ou `*`).
- `INPUT_PHOTOS_DIR`: pasta de armazenamento da foto de entrada.
- `GENERATED_PHOTOS_DIR`: pasta de armazenamento de fotos geradas.
- `INPUT_PHOTO_DEFAULT_NAME`: nome base padrao da foto de entrada.
- `OUTPUT_PHOTO_DEFAULT_NAME`: nome base padrao para fotos de output numeradas.
- `ALLOWED_INPUT_EXTENSIONS`: extensoes aceitas no upload.

## Exemplo de `.env`

```env
APP_NAME="Caricatura Imagens API"
APP_VERSION="0.1.0"
ENVIRONMENT="development"
DEBUG="false"
HOST="0.0.0.0"
PORT="8000"
CORS_ORIGINS="*"
INPUT_PHOTOS_DIR="app/data/input"
GENERATED_PHOTOS_DIR="app/data/output"
INPUT_PHOTO_DEFAULT_NAME="input_photo"
OUTPUT_PHOTO_DEFAULT_NAME="output_photo"
ALLOWED_INPUT_EXTENSIONS="jpg,jpeg,png,webp"
```

## CORS

- `CORS_ORIGINS="*"`: libera todas as origens.
- `CORS_ORIGINS="http://localhost:3000,https://dominio.com"`: restringe por lista.

## Armazenamento de fotos

- `INPUT_PHOTOS_DIR`: diretorio da foto de entrada (sempre 1 arquivo por vez).
- `GENERATED_PHOTOS_DIR`: diretorio das fotos geradas pela IA (multiplos arquivos).
- `INPUT_PHOTO_DEFAULT_NAME`: nome base fixo para salvar foto de entrada.
- `OUTPUT_PHOTO_DEFAULT_NAME`: prefixo usado para salvar novas fotos processadas (`output_photo1`, `output_photo2`, ...).
- `ALLOWED_INPUT_EXTENSIONS`: lista de extensoes permitidas no upload.

## Dependencias relacionadas

- `python-dotenv`: carregamento de `.env`.
- `python-multipart`: suporte a upload `multipart/form-data`.

## Observacao sobre reload

Atualmente o `main.py` executa com `reload=True` de forma fixa para desenvolvimento.
