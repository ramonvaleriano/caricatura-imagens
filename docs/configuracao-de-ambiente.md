# Configuracao de Ambiente

## Fonte de configuracao

As variaveis sao carregadas de `.env` em `app/core/settings.py`, via `load_dotenv` + `os.getenv`.

## Variaveis atuais

- `APP_NAME`
- `APP_VERSION`
- `ENVIRONMENT`
- `DEBUG`
- `HOST`
- `PORT`
- `CORS_ORIGINS`
- `INPUT_PHOTOS_DIR`
- `GENERATED_PHOTOS_DIR`
- `INPUT_PHOTO_DEFAULT_NAME`
- `ALLOWED_INPUT_EXTENSIONS`

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
ALLOWED_INPUT_EXTENSIONS="jpg,jpeg,png,webp"
```

## CORS

- `CORS_ORIGINS="*"`: libera todas as origens.
- `CORS_ORIGINS="http://localhost:3000,https://dominio.com"`: restringe por lista.

## Armazenamento de fotos

- `INPUT_PHOTOS_DIR`: diretorio da foto de entrada (sempre 1 arquivo por vez).
- `GENERATED_PHOTOS_DIR`: diretorio das fotos geradas pela IA (multiplos arquivos).
- `INPUT_PHOTO_DEFAULT_NAME`: nome base fixo para salvar foto de entrada.
- `ALLOWED_INPUT_EXTENSIONS`: lista de extensoes permitidas no upload.
