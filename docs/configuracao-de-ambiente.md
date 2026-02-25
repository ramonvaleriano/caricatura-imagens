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
- `LOG_LEVEL`: nivel de log da aplicacao (`DEBUG|INFO|WARNING|ERROR`).
- `INPUT_PHOTOS_DIR`: pasta de armazenamento da foto de entrada.
- `GENERATED_PHOTOS_DIR`: pasta de armazenamento de fotos geradas.
- `INPUT_PHOTO_DEFAULT_NAME`: nome base padrao da foto de entrada.
- `OUTPUT_PHOTO_DEFAULT_NAME`: nome base padrao para fotos de output numeradas.
- `ALLOWED_INPUT_EXTENSIONS`: extensoes aceitas no upload.
- `OPENAI_ENABLED`: ativa/desativa chamada real para OpenAI.
- `OPENAI_API_KEY`: chave da API OpenAI.
- `OPENAI_MODEL`: modelo usado no endpoint `/photos/process`.
- `OPENAI_REASONING_EFFORT`: esforco de raciocinio (`low|medium|high`).
- `OPENAI_TEXT_VERBOSITY`: verbosidade textual (`low|medium|high`).
- `OPENAI_STORE_RESPONSE`: controla armazenamento remoto da resposta.
- `OPENAI_ENABLE_WEB_SEARCH`: ativa `web_search_preview`.
- `OPENAI_INCLUDE_FIELDS`: campos extras incluidos na resposta.

As variaveis `OPENAI_*` sao consumidas e normalizadas em `app/core/ai_config.py`.
Os prompts sao carregados de arquivos `.md` por `app/core/prompt_loader.py`.

## Exemplo de `.env`

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

## CORS

- `CORS_ORIGINS="*"`: libera todas as origens.
- `CORS_ORIGINS="http://localhost:3000,https://dominio.com"`: restringe por lista.

## Logging

- `LOG_LEVEL="DEBUG"`: log detalhado para diagnostico local.
- `LOG_LEVEL="INFO"`: nivel recomendado para desenvolvimento padrao.
- `LOG_LEVEL="WARNING"` ou `ERROR`: reduzir verbosidade.

## Armazenamento de fotos

- `INPUT_PHOTOS_DIR`: diretorio da foto de entrada (sempre 1 arquivo por vez).
- `GENERATED_PHOTOS_DIR`: diretorio das fotos geradas pela IA (multiplos arquivos).
- `INPUT_PHOTO_DEFAULT_NAME`: nome base fixo para salvar foto de entrada.
- `OUTPUT_PHOTO_DEFAULT_NAME`: prefixo usado para salvar novas fotos processadas (`output_photo1`, `output_photo2`, ...).
- `ALLOWED_INPUT_EXTENSIONS`: lista de extensoes permitidas no upload.
- `OPENAI_ENABLED=false`: rota `/photos/process` usa fallback e retorna a imagem original.
- `OPENAI_ENABLED=true`: rota `/photos/process` chama OpenAI.

## Prompts da IA

Arquivos de prompt usados pelo service:

- `app/prompts/image_developer_prompt.md`
- `app/prompts/image_user_prompt.md`

Esses arquivos sao lidos em runtime e nao devem ficar no `.env`.

## Dependencias relacionadas

- `python-dotenv`: carregamento de `.env`.
- `python-multipart`: suporte a upload `multipart/form-data`.
- `openai`: integracao com Responses API para geracao de imagem.

## Observacao sobre reload

Atualmente o `main.py` executa com `reload=True` de forma fixa para desenvolvimento.
