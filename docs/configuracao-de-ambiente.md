# Configuracao de Ambiente

## Fonte de configuracao

As variaveis sao carregadas em `app/core/settings.py` com:

- `load_dotenv(BASE_DIR / ".env", override=True)`
- `os.getenv(...)`

Com `override=True`, os valores do `.env` local prevalecem sobre variaveis ja existentes no ambiente de execucao.

## Variaveis atuais

### Metadados e servidor

- `APP_NAME`: nome exibido na documentacao OpenAPI.
- `APP_VERSION`: versao da API.
- `ENVIRONMENT`: ambiente logico (`development`, `staging`, `production`).
- `DEBUG`: flag reservada para evolucoes.
- `HOST`: host de bind do servidor.
- `PORT`: porta de bind do servidor.

### CORS e logs

- `CORS_ORIGINS`: lista CSV de origens permitidas (ou `*`).
- `LOG_LEVEL`: nivel de log (`DEBUG|INFO|WARNING|ERROR`).

### Storage de imagens

- `INPUT_PHOTOS_DIR`: pasta da foto de entrada.
- `GENERATED_PHOTOS_DIR`: pasta de fotos geradas.
- `INPUT_PHOTO_DEFAULT_NAME`: nome base da foto de entrada.
- `OUTPUT_PHOTO_DEFAULT_NAME`: nome base da foto de output numerada.
- `ALLOWED_INPUT_EXTENSIONS`: extensoes aceitas no upload (CSV).

### OpenAI

- `OPENAI_ENABLED`: ativa/desativa chamada real para OpenAI.
- `OPENAI_API_KEY`: chave da API OpenAI.
- `OPENAI_MODEL`: modelo usado em `/photos/process`.
- `OPENAI_REASONING_EFFORT`: `low|medium|high`.
- `OPENAI_TEXT_VERBOSITY`: `low|medium|high`.
- `OPENAI_STORE_RESPONSE`: persistencia remota de resposta.
- `OPENAI_ENABLE_WEB_SEARCH`: ativa `web_search_preview`.
- `OPENAI_INCLUDE_FIELDS`: campos extras retornados pela API.

As variaveis `OPENAI_*` sao normalizadas em `app/core/ai_config.py`.

## Prompts da IA

Prompts nao devem ficar em `.env`.

Arquivos oficiais:

- `app/prompts/image_developer_prompt.md`
- `app/prompts/image_user_prompt.md`

Leitura centralizada em:

- `app/core/prompt_loader.py`

## Exemplo de `.env` (template)

```env
APP_NAME="Caricatura Imagens API"
APP_VERSION="0.1.0"
ENVIRONMENT="development"
DEBUG="false"
HOST="0.0.0.0"
PORT="8000"
CORS_ORIGINS="*"
LOG_LEVEL="INFO"
INPUT_PHOTOS_DIR="app/data/input"
GENERATED_PHOTOS_DIR="app/data/output"
INPUT_PHOTO_DEFAULT_NAME="input_photo"
OUTPUT_PHOTO_DEFAULT_NAME="output_photo"
ALLOWED_INPUT_EXTENSIONS="jpg,jpeg,png,webp"
OPENAI_ENABLED="false"
OPENAI_API_KEY=""
OPENAI_MODEL="gpt-5"
OPENAI_REASONING_EFFORT="medium"
OPENAI_TEXT_VERBOSITY="medium"
OPENAI_STORE_RESPONSE="false"
OPENAI_ENABLE_WEB_SEARCH="false"
OPENAI_INCLUDE_FIELDS="reasoning.encrypted_content,web_search_call.action.sources"
```

## Configuracao para IA real

Para usar processamento real do agente com OpenAI:

1. `OPENAI_ENABLED="true"`
2. `OPENAI_API_KEY` preenchida
3. prompts `.md` preenchidos em `app/prompts`
4. reiniciar a API apos alteracao de variaveis

## Dependencias relacionadas

- `python-dotenv`: leitura de `.env`.
- `python-multipart`: upload `multipart/form-data`.
- `openai`: chamada do provider.
