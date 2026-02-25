# Guia de Execucao Local

## Pre-requisitos

- Python 3.10+
- dependencias em `requirements.txt`

## Instalar dependencias

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Subir servidor pelo terminal

```bash
python3 main.py
```

## Subir servidor pelo VS Code

Configuracoes disponiveis em `.vscode/launch.json`:

- `API: Run (Auto Reload)`
- `API: Debug`

Ambas usam `.env` via `envFile`.

## Validar startup

1. abrir `http://localhost:8000/docs`
2. abrir `http://localhost:8000/redoc`
3. testar `GET /health`

## Fluxo rapido de teste do agente

### 1) Upload da imagem de entrada

```bash
curl -X POST "http://localhost:8000/photos/input" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/caminho/da/imagem.jpg"
```

### 2) Processar com agente

```bash
curl -X POST "http://localhost:8000/photos/process" --output processed.bin
```

### 3) Listar imagens geradas

```bash
curl -X GET "http://localhost:8000/photos/output"
```

### 4) Baixar por nome base

```bash
curl -X GET "http://localhost:8000/photos/output/output_photo1" --output output_photo1.jpg
```

## Ativar IA real (OpenAI)

No `.env`:

- `OPENAI_ENABLED="true"`
- `OPENAI_API_KEY="<SUA_CHAVE>"`

E manter prompts preenchidos em:

- `app/prompts/image_developer_prompt.md`
- `app/prompts/image_user_prompt.md`

Depois reinicie a API.

## Logs esperados no processamento

Ao chamar `POST /photos/process`, espere logs nesta sequencia:

1. `Processing input photo with agent ...`
2. `Controller called | controller=image_agent ...`
3. `Service called | service=image_generation_service ...`
4. `Calling OpenAI ...` (quando `OPENAI_ENABLED=true`)
5. `Photo processed | input_file=... output_file=...`

Se nao aparecer `Calling OpenAI`, o processamento pode ter caido em fallback.
